# Optional U1 integrations

The next portable candidate includes two wheel packages under `resources/u1_plugins`.
The native plugin manager stages missing bundled packages into this application's own
`ultimate_u1_data_dir/orca_plugins` directory. They appear in the manager **disabled**.
Existing packages, versions, permissions and user changes are not replaced. Enable a
package explicitly, approve its requested dependencies/permissions, then Run its script
capability. The older `experimental-windows-b3fcd387d861` release predates this integration.

Before launching, authorize input/output directories with the same operator-owned
setting used by the MCP file policy. PowerShell example:

```powershell
$env:U1_MCP_ALLOWED_ROOTS='["C:/Users/you/Models"]'
& './OrcaSlicer/orca-slicer.exe'
```

Save your current project, then enter that saved file's absolute path in the plugin.
Permission prompts in the native host still apply. No plugin changes presets, enables
printing, executes macros or provides a second MCP server.

## Snapmaker Studio inspection

Pinned MIT core: `DVOpenLabs/snapmaker-studio` at
`6d2e7f0485bfb7fa24caa9a58a4bd5fd37431222`. Original notices and file hashes live in
`third_party/snapmaker-studio`. The wheel declares `lxml==6.1.3`; the existing native
plugin dependency mechanism installs it only when the operator enables the package.

The integration reads 3MF/STL project traits and evaluates preflight against an optional
Studio-format printer snapshot. It does not contact hardware. Unknown observations
remain unknown. It does not expose Studio's conversion rules, negative raft-expansion
replacement, printer controls or generic scripting. Internal reference data are not
installed as calibrated filament/printer presets. Another already-loaded Studio core
is rejected rather than silently substituted for the audited version.

## Bambu-to-U1 converter connector

Contract audited against `thadius83/bambu-to-snapmaker-u1` at
`630bc8a92eb128464be14cc5a94838e4e2d2a101`. That project's implementation, reference
profiles and rules use PolyForm Noncommercial and **are not included**. This package is
an independent connector to a separately installed service you are licensed to use.
Its licensing restrictions are not removed by using a plugin.

Start/configure your own service separately; the upstream Docker example exposes
`http://127.0.0.1:8084`. The connector accepts literal loopback addresses with explicit
ports only, disables proxies and redirects, lists reference profile identifiers, and
requires explicit licensing acknowledgment before uploading a selected file. Automatic
rules, speed clamping and swap pauses are not requested. Returned archives are checked
for container/size/path integrity and saved exclusively into a new authorized file.
Review the conversion diff, verify assignments/macros and slice afresh. The connector
never uploads to a printer or starts a job. A structurally valid conversion is not
certification of U1 G-code or physical compatibility.

## Validation and limits

`tools/u1/tests/test_plugin_integrations.py` runs real pinned Studio inspection and a
local HTTP-contract fixture. A separate actual upstream FastAPI service round trip
produced a new 3MF while preserving the input SHA-256; the temporary service was stopped.
`tests/slic3rutils/test_u1_plugin_packages.cpp` installs/loads the actual wheels and
checks disabled, non-overwriting bundled discovery. Windows portable CI separately
checks package hashes, staged catalog entries and disabled activation state.

The entire Snapmaker Studio desktop product is not embedded. Generic Moonraker is not
Snapmaker gateway/pairing/RFID/camera/feeder parity, and neither plugin substitutes for
missing slicing-kernel features. See the functional parity audit and implementation
backlog before relying on a particular U1 function.
