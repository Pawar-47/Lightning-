# Porting status and verified checkpoint

Last updated: 2026-11-21

## Project roots and boundary

- New project repository: `Pawar-47/Lightning-`
- Development/build foundation: `ascpixi/minecraft-shader-template`, upstream revision `ab2b99c9e1715cb951936157fe3c2ef94890233b`
- User-supplied reference archive: `Shader.zip`, identified as MakeUp Ultra Fast v9.6 by Javier Garduño (KDXavier)
- No Aetheris-Shaders source, commits, branches or releases are used as Lightning's foundation.

## Uploaded archive inventory

The uploaded archive contains 348 actual files (742,051 uncompressed bytes) after excluding macOS `__MACOSX` metadata.

| Source family | Files |
|---|---:|
| `shaders/common/` | 41 |
| `shaders/lib/` | 38 |
| `shaders/src/` | 22 |
| `shaders/world0/` | 58 |
| `shaders/world-1/` | 55 |
| `shaders/world1/` | 57 |
| Other root, language, texture and metadata files | 115 |

## Current implementation checkpoint

- Template Gradle build foundation imported; project identity changed to Lightning (`dev.pawar47.lightning`, `0.1.0-alpha.1`).
- **Source-to-port comparison: 346/348 files verified.** The 136 unchanged files are byte-identical to the uploaded ZIP. All 210 `.fsh/.vsh` entrypoints are verified against the uploaded ZIP after only the `#version 120` → `#version 330 compatibility` migration.
- The 100 shared modules comprise 41 `common/`, 37 non-config `lib/`, and 22 `src/` files. Their uploaded-ZIP Git blob hashes match their active repository destinations.
- All 17 metadata/Voxy files have exact uploaded-ZIP hash matches.
- All 19 documentation, language and texture assets have exact uploaded-ZIP hash matches.
- The two archive-specific exceptions (`shaders/lib/config.glsl` and `shaders/shaders.properties`) are intentionally customized/merged. Their exact original Git blob hashes are recorded in the final column of `reference/source-file-map.csv`; the active config is feature-restored and tuned, while the active root properties file merges the original settings UI with Lightning profiles.
- The source `shaders/shaders.properties` is intentionally relocated/merged into the pack-root `shaders.properties`.
- All 210 entrypoints declare GLSL 330. Shared shader modules retain their source contents.
- Full MakeUp settings UI and original option screens are present. Lightning adds `Performance` and `Quality` profiles.
- Performance profile retains the major effects. It uses bounded budgets and the cheaper depth-based godray path (`VOL_LIGHT=1`); Quality retains the full shadow-aware volumetric-light path (`VOL_LIGHT=2`).
- Added `tools/validate_shaderpack.py` and `.github/workflows/shaderpack-validation.yml`.

See [`SOURCE_PORT_VERIFICATION.md`](SOURCE_PORT_VERIFICATION.md) for the per-family aggregate hashes and [`ARCHIVE_EXCEPTION_RECONCILIATION.md`](ARCHIVE_EXCEPTION_RECONCILIATION.md) for the two intentional config/options-file changes.

## CI evidence

- Latest verified run: [44816752848](https://github.com/Pawar-47/Lightning-/actions/runs/44816752848) — completed successfully on commit `0ec483c41b0e0f86f2218efe25344f871444f501`.
- All workflow steps passed: static shader structure/include checks, source-port audit-tool syntax check, Java/Gradle setup, shaderpack ZIP packaging and artifact upload.
- The uploaded CI artifact is `Lightning-shaderpack`, 374,381 bytes (artifact ID `14668494255`; SHA-256 `7c27d4fa5a037ea8a730ffd5b3745c92ef6f02537444998f78f250c728c537a5`).
- The workflow syntax-checks `tools/verify_source_port.py`; it does not execute the full ZIP comparison because the private user-uploaded archive is not stored in the repository.
- CI structure/package checks are not GLSL stage compilation, Iris runtime loading, visual comparison or target-hardware benchmarking.

## Known gaps — do not mark complete

1. Complete semantic/line-by-line review of the two archive-specific files against the active tuned config and merged properties file.
2. No full GLSL stage compile/link matrix has run.
3. No Minecraft + Iris + Sodium runtime shader-load test has run.
4. No visual comparison across Overworld, Nether, End, water, clouds, shadows and post-processing has run.
5. No FPS/frame-time benchmark has run on the Intel Core i3-5005U / Intel HD 5500 / 8 GB Linux Mint target laptop.
6. The installed Minecraft/Iris/Sodium versions have not yet been confirmed; template defaults are provisional.
7. No release has been created. Do not present the current CI ZIP as a finished, hardware-validated release.

## Next work order

1. Complete the semantic diff/reconciliation of the two archive-specific files.
2. Add real GLSL compilation using Iris-compatible preprocessing, not only static include checks.
3. Run Iris runtime loading and dimension/feature smoke tests.
4. Compare visual output and tune performance budgets without silently removing major effects.
5. Benchmark on the target laptop.
6. Prepare a release only after the above checks pass.
