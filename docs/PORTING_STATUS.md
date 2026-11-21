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
| Shader-root files and metadata | 58 |
| Language files | 9 |
| Texture files and metadata | 6 |
| Archive-root documentation/reference files | 4 |
| **Total** | **348** |

## Current implementation checkpoint

- Template Gradle build foundation imported; project identity changed to Lightning (`dev.pawar47.lightning`, `0.1.0-alpha.1`).
- **Source-to-port comparison: 346/348 files are reproducibly verified through deterministic transformations.** 134 files are byte-identical to the uploaded ZIP; all 210 `.fsh/.vsh` entrypoints differ only by the `#version 120` → `#version 330 compatibility` migration; two library modules have explicitly documented, reproducible cloud-opacity early-exit optimizations. The two config/options exceptions remain separately identified.
- The 100 shared modules comprise 41 `common/`, 37 non-config `lib/`, and 22 `src/` files. Of the 37 non-config library files, 35 remain byte-identical and two are tracked deterministic optimization derivatives.
- All 15 language/texture assets have exact uploaded-ZIP hash matches.
- All 17 reference and shader metadata files are separately accounted for in the source ledger.
- The two archive-specific exceptions (`shaders/lib/config.glsl` and `shaders/shaders.properties`) are intentionally customized/merged. Their exact original Git blob hashes are recorded in the final column of `reference/source-file-map.csv`; the active config is feature-restored and tuned, while the active root properties file merges the original settings UI with Lightning profiles.
- The source `shaders/shaders.properties` is intentionally relocated/merged into the pack-root `shaders.properties`.
- All 210 archive-derived entrypoints declare GLSL 330. The template foundation contributes two additional `gbuffers_textured_lit` vertex/fragment entrypoints, bringing the distributable compiler matrix to 212 stages. Shared shader modules retain their source contents except for the two documented deterministic cloud-opacity early-exit derivatives.
- Full MakeUp settings UI and original option screens are present. Lightning adds `Performance` and `Quality` profiles.
- Performance profile retains the major effects. It uses bounded budgets and the cheaper depth-based godray path (`VOL_LIGHT=1`); Quality retains the full shadow-aware volumetric-light path (`VOL_LIGHT=2`).
- Added `tools/validate_shaderpack.py`, `tools/verify_source_port.py` and `.github/workflows/shaderpack-validation.yml`.

See [`SOURCE_PORT_VERIFICATION.md`](SOURCE_PORT_VERIFICATION.md) for the per-family aggregate hashes and [`ARCHIVE_EXCEPTION_RECONCILIATION.md`](ARCHIVE_EXCEPTION_RECONCILIATION.md) for the two intentional config/options-file changes.

## CI evidence

- Latest pre-compilation validation run: [44819794407](https://github.com/Pawar-47/Lightning-/actions/runs/44819794407) — completed successfully on commit `f61bacc4cf3123405a4538c0387eac82c58a6772`.
- That run passed static shader structure/include checks, required-feature and early-exit optimization assertions, audit-tool syntax check, Java/Gradle setup, shaderpack ZIP packaging and artifact upload.
- The distributable CI artifact was `Lightning-shaderpack`, 378,244 bytes (artifact ID `14672295007`; archive digest `sha256:53df5105e02572187658145d85c45fe2c7da56c2945d49a9ecfd7b8ca099b7f6`). The nested distributable ZIP carries the LGPL license text and third-party attribution notice.
- The workflow now adds a real offline GLSL compiler pass for all 210 vertex/fragment entrypoints using `glslangValidator`. Its first CI result is pending.
- The uploaded ZIP comparison remains reproducible locally with `python tools/verify_source_port.py /path/to/Shader.zip`; the source archive is intentionally not included in the distributable.
- A successful glslang run still does not prove Iris runtime loading, GPU-driver compilation, visual parity or target-hardware performance.

## Known gaps — do not mark complete

1. Pass the new GLSL compiler gate for all 212 entrypoints and resolve any genuine source failures.
3. Minecraft + Iris + Sodium runtime shader-load and dimension/feature smoke tests.
4. Visual comparison across Overworld, Nether, End, water, clouds, shadows and post-processing.
5. FPS/frame-time benchmark on the Intel Core i3-5005U / Intel HD 5500 / 8 GB Linux Mint target laptop.
6. The installed Minecraft/Iris/Sodium versions have not yet been confirmed; template defaults are provisional.
7. No published release yet. Do not present a CI ZIP as a finished, hardware-validated release.

## Next work order

1. Pass the new GLSL compiler gate and resolve any genuine shader compile failures.
3. Run Iris runtime loading and dimension/feature smoke tests.
4. Compare visual output and tune performance budgets without silently removing major effects.
5. Benchmark on the target laptop.
6. Publish a versioned release with exact validation boundaries and reproducible artifacts.
