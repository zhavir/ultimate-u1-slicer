# Experimental Windows x64 portable build

## New plugin candidate — pending Windows validation

Source `237a930cbf3308d589e009768a29a160c2f5367e` is building in [run 42093341824](https://github.com/zhavir/ultimate-u1-slicer/actions/runs/42093341824). It adds both optional plugin packages, disabled-by-default native discovery, two reviewed engine fixes and trusted-signature verification support. Windows component checks passed; the full application, portable startup checks and complete unit suite are still pending at this checkpoint. No signing identity is configured. This is not a newly published or signed release. See [plugin instructions](../plugins/integrations.md) and [signing requirements](../releasing/windows-signing.md).

## Previously published candidate

Source: `b3fcd387d8610da34b39357afc4df5e71e42dcdb`. [Download prerelease](https://github.com/zhavir/ultimate-u1-slicer/releases/tag/experimental-windows-b3fcd387d861). [Native CI run](https://github.com/zhavir/ultimate-u1-slicer/actions/runs/41964174657). This is not a stable U1 release.

Extract the complete ZIP into a new writable folder. Open its `OrcaSlicer` directory and launch `orca-slicer.exe`. Preserve the adjacent `ultimate_u1_data_dir` directory; it selects portable settings. Do not copy files into an existing slicer installation or overwrite its user configuration. No installer is needed.

The archive SHA-256 is `7f6011530bcf46e7d2b6839249f19df1c8f8aa871671b3e8844569f7dffba010`. It contains 4085 entries and 224865319 bytes. Its CRCs, paths, portable marker, absence of generated MCP credentials and published checksum were checked independently. The release includes `SHA256SUMS`, native `verification.json` and `windows-unit-tests.json`.

Native Windows checks passed for help, GUI readiness, authenticated MCP HTTP initialization, packaged stdio discovery/initialization, portable storage and absence of automatic URL registration. The full configured unit suite passed all 3,462 tests in 346 seconds. Inherited `NotWorking` and `RequiresApp` labels are excluded by the original runner; no new exclusions or waived failures were added. This does not establish end-to-end Codex/Claude client behavior or Windows GUI slicing of every U1 project.

Linux validation additionally passed the full FFF suite (1,230 JUnit case records, two inherited skips) and five affected recording/plugin cases (69 assertions, separate isolated processes). [Final structured evidence](evidence/windows-portable-final.json), [initial Windows failure](evidence/windows-initial-regression-failure.json), [second Windows attempt](evidence/windows-second-validation.json), and [targeted Linux regressions](evidence/gui-affected-regressions.json) preserve the progression.

Original Snapmaker projects using automatic support expansion `-1` still require [geometry migration](../architecture/support-expansion-migration.md). Complete FOrca per-nozzle/Color Patch migration and current Snapmaker gateway/feeding parity remain release gates. No native macOS application or physical U1 printing has been validated. Review [feature status](../architecture/feature-matrix.md) and [roadmap](../roadmap.md) before relying on a capability.

For repeat builds, push reviewed source changes to main or dispatch `.github/workflows/u1-windows-portable.yml`. Its optional publish job requires both native portable verification and the complete configured Windows unit job. The initial prerelease uses the already-verified artifact from the linked run, with no duplicate rebuild. Keep publication tied to the exact compiled source revision.
