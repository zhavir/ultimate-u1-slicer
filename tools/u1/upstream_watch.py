#!/usr/bin/env python3
"""Watch pinned upstream branches, recent releases and tags; open deduplicated review issues."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote


def gh_api(endpoint, payload=None):
    command = ["gh", "api", endpoint]
    if payload is not None:
        command += ["--method", "POST", "--input", "-"]
    result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"GitHub API failed for {endpoint}: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def repository(source):
    match = re.fullmatch(r"https://github\.com/([\w.-]+/[\w.-]+)\.git", source["url"])
    if not match:
        raise ValueError("upstream URL must be a public GitHub HTTPS Git URL")
    return match[1]


def snapshot(lock, api=gh_api):
    result, metadata = {}, {}
    for alias, source in lock["sources"].items():
        repo = repository(source)
        branch = source.get("branch", source.get("default_branch", "main"))
        try:
            result[alias] = observe_source(repo, branch, metadata, api)
        except RuntimeError as error:
            result[alias] = {"repository": repo, "branch": branch, "error": str(error)}
    return {"schema": 1, "sources": result}


def observe_source(repo, branch, metadata, api):
    if repo not in metadata:
        releases = api(f"repos/{repo}/releases?per_page=30")
        tags = api(f"repos/{repo}/tags?per_page=30")
        metadata[repo] = {
            "releases": {str(item["id"]): {"tag": item["tag_name"], "updated_at": item["updated_at"],
                          "url": item["html_url"], "prerelease": item["prerelease"]}
                         for item in releases if not item["draft"]},
            "tags": {item["name"]: item["commit"]["sha"] for item in tags},
        }
    head = api(f"repos/{repo}/commits/{quote(branch, safe='')}")
    return {"repository": repo, "branch": branch, "head": head["sha"], **metadata[repo]}

def event(alias, kind, identity, current, previous, url):
    value = {"source": alias, "kind": kind, "identity": identity, "current": current,
             "previous": previous, "url": url}
    value["fingerprint"] = hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
    return value


def changes(lock, baseline, current):
    events, seen = [], set()
    for alias, observed in current["sources"].items():
        source = lock["sources"][alias]
        old = baseline["sources"].get(alias)
        if old is None:
            raise ValueError(f"missing baseline for {alias}; capture and review it first")
        repo = observed["repository"]
        if "error" in observed:
            events.append(event(alias, "monitor-error", observed["branch"], observed["error"], None,
                                f"https://github.com/{repo}"))
            continue
        pin = source["sha"]
        if observed["head"] != pin:
            events.append(event(alias, "branch", observed["branch"], observed["head"], pin,
                                f"https://github.com/{repo}/compare/{pin}...{observed['head']}"))
        # A repository may be watched on two branches (official main and MCP). Releases/tags
        # belong to the repository, so notify once, not once per alias.
        if repo in seen:
            continue
        seen.add(repo)
        release_tags = set()
        for identifier, release in observed["releases"].items():
            before = old["releases"].get(identifier)
            if before != release:
                events.append(event(alias, "release", identifier, release, before, release["url"]))
                release_tags.add(release["tag"])
        for tag, sha in observed["tags"].items():
            if old["tags"].get(tag) != sha and tag not in release_tags:
                events.append(event(alias, "tag", tag, sha, old["tags"].get(tag),
                                    f"https://github.com/{repo}/tree/{quote(tag, safe='')}"))
    return events


def existing_fingerprints(target, api=gh_api):
    fingerprints = set()
    page = 1
    while True:
        issues = api(f"repos/{target}/issues?state=all&labels=upstream-update&per_page=100&page={page}")
        for issue in issues:
            if "pull_request" not in issue:
                fingerprints.update(re.findall(r"<!-- u1-upstream-event:([a-f0-9]{64}) -->", issue.get("body") or ""))
        if len(issues) < 100:
            return fingerprints
        page += 1


def notify(target, events, assignee=None, api=gh_api, limit=25):
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", target):
        raise ValueError("invalid notification repository")
    known = existing_fingerprints(target, api)
    pending = [item for item in events if item["fingerprint"] not in known]
    created = []
    for item in pending[:limit]:
        identity = str(item["identity"]).replace("@", "＠").replace("\n", " ")
        title = f"Upstream {item['kind']}: {item['source']} / {identity}"[:240]
        body = (f"<!-- u1-upstream-event:{item['fingerprint']} -->\n"
                f"Detected a change in **{item['source']}** ({item['kind']}).\n\n"
                f"[Inspect upstream change]({item['url']})\n\n"
                "```json\n" + json.dumps({k: v for k, v in item.items() if k != "fingerprint"}, indent=2) + "\n```\n\n"
                "This is a notification, not an integration or compatibility claim. No upstream code was executed or merged.\n\n"
                "Use `.claude/skills/ultimate-u1-maintenance/SKILL.md` and `AGENTS.md`: inspect the source diff and license, "
                "classify engine/schema/MCP/profiles/connectivity/build changes, choose isolated patches, run the relevant "
                "U1 regressions, update source pins and feature evidence, then close this issue with the integration commit "
                "or an explicit deferral. Preserve the known-good build; never automatically print or merge upstream code.")
        payload = {"title": title, "body": body, "labels": ["upstream-update"]}
        if assignee:
            payload["assignees"] = [assignee]
        issue = api(f"repos/{target}/issues", payload)
        created.append(issue["html_url"])
    return {"created": created, "deduplicated": len(events) - len(pending), "deferred": max(0, len(pending) - limit)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-baseline", action="store_true")
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("build/upstream-watch.json"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    lock = json.loads((root / "tools/u1/sources.lock.json").read_text())
    configuration = json.loads((root / ".github/u1-maintenance.json").read_text())
    baseline_path = root / ".github/u1-upstream-baseline.json"
    current = snapshot(lock)
    if args.capture_baseline:
        if args.notify:
            parser.error("baseline capture cannot send notifications")
        if any("error" in source for source in current["sources"].values()):
            raise SystemExit("Cannot capture an incomplete baseline; fix upstream API errors first")
        baseline_path.write_text(json.dumps(current, indent=2) + "\n")
        print("Captured current release/tag observations; reviewed integration pins remain unchanged")
        return
    baseline = json.loads(baseline_path.read_text())
    events = changes(lock, baseline, current)
    result = {"source_integration_performed": False, "observed": current, "events": events}
    if args.notify:
        result["notifications"] = notify(configuration["repository"], events, configuration.get("notification_assignee"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Observed {len(current['sources'])} sources; {len(events)} candidate events; report: {args.output}")
    if result.get("notifications", {}).get("deferred"):
        raise SystemExit("Notification limit reached; remaining events will be processed on the next run")


if __name__ == "__main__":
    main()
