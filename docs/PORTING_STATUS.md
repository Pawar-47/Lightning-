# Porting status and verified checkpoint

Last updated: 2026-11-21

## Project roots and boundary

- Project repository: `Pawar-47/Lightning-`
- Development/build foundation: `ascpixi/minecraft-shader-template`, upstream revision `ab2b99c9e1715cb951936157fe3c2ef94890233b`
- User-supplied reference archive: `Shader.zip`, identified as MakeUp Ultra Fast v9.6 by Javier Garduño (KDXavier)
- Lightning is MakeUp-derived because that is the source archive supplied for this repository. It is not a BSL-source port.
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

- Template Gradle build foundation imported; project identity is Lightning (`dev.pawar47.lightning`).
- **Source-to-port comparison: 346/348 files are reproducibly verified through deterministic transformations.** 134 files are byte-identical to the uploaded ZIP; all 210 archive-derived `.fsh/.vsh` entrypoints differ only by the `#version 120` → `#version 330 compatibility` migration; two library modules have explicitly documented, reproducible cloud-opacity early-exit optimizations. The two config/options exceptions are separately identified and semantically reconciled.
- The 100 shared modules comprise 41 `common/`, 37 non-config `lib/`, and 22 `src/` files. Of the 37 non-config library files, 35 remain byte-identical and two are tracked deterministic cloud-opacity optimization derivatives.
- All 15 language and texture assets have exact uploaded-ZIP hash matches.
- The two archive-specific exceptions (`shaders/lib/config.glsl` and `shaders/shaders.properties`) are intentionally customized/merged. Their exact original Git blob hashes are recorded in the final column of `reference/source-file-map.csv`.
- The active config restores the requested visual features and applies Lightning's reduced budgets. The active root properties file retains the original options UI while replacing the legacy effect-disabling profiles with Lightning's Performance and Quality profiles.
- The source `shaders/shaders.properties` is intentionally relocated/merged into the pack-root `shaders.properties`.
- All 210 archive-derived entrypoints declare GLSL 330. The template foundation contributes two additional `gbuffers_textured_lit` vertex/fragment entrypoints, bringing the distributable compiler matrix to 212 stages.
- Performance keeps the major effects available. It uses bounded budgets and the cheaper depth-based godray path (`VOL_LIGHT=1`); Quality retains the full shadow-aware volumetric-light path (`VOL_LIGHT=2`).
- The SSR early-return experiment was reverted after source comparison showed it changed the original out-of-screen fallback coordinate. `shaders/lib/water.glsl` is byte-identical to the uploaded ZIP.
- The only retained deterministic early exits are in Overworld and End volumetric-cloud loops, after accumulated opacity reaches the final clamp threshold.
- Added source validation, uploaded-archive verification, GLSL compilation and Iris client-startup smoke-test tooling.

See [`SOURCE_PORT_VERIFICATION.md`](SOURCE_PORT_VERIFICATION.md) for per-family verification and [`ARCHIVE_EXCEPTION_RECONCILIATION.md`](ARCHIVE_EXCEPTION_RECONCILIATION.md) for the completed config/options semantic diff.

## CI evidence

- Full validation run: [44842412214](https://github.com/Pawar-47/Lightning-/actions/runs/44842412214) — successful on commit `69b7804ca30f721bf5d4149590c9674852178694`.
- Static shader structure/include checks, feature/profile assertions, source-audit syntax checks, all 212 offline GLSL entrypoints, Gradle ZIP packaging and the headless Iris client-startup smoke test passed.
- The smoke log confirms Minecraft 1.21.5, Fabric Loader 0.16.14, Iris 1.8.11, Sodium 0.6.12 and an active OpenGL debug context. `Lightning-dev` is configured in Iris; the test does not enter a world or prove in-world shaderpack compilation.
- Shaderpack artifact: `Lightning-shaderpack`, 378,182 bytes (artifact ID `14681393040`; artifact digest `sha256:4fa8282a066bd0939ac4610c165597a1befe6739b17f0c3d8a775be19da0368a`). The distributable contains the LGPL license and third-party attribution.
- The uploaded ZIP comparison remains reproducible locally with `python tools/verify_source_port.py /path/to/Shader.zip`; the source archive is intentionally not included in the distributable.

## Known gaps — do not mark complete

1. Iris shaderpack loading and actual program compilation/linking after entering a world.
2. Visual comparison across Overworld, Nether, End, water, clouds, shadows and post-processing.
3. FPS/frame-time benchmark on the Intel Core i3-5005U / Intel HD 5500 / 8 GB Windows 10 target laptop.
4. Confirmation that the user's installed Minecraft/Iris/Sodium versions match the template baseline.
5. Stable-release readiness; `v0.1.0-alpha.2` is a test pre-release, not a hardware-validated stable release.

## Next work order

1. Install the pre-release in the user's SK Launcher instance and test in-world shader loading.
2. Capture comparable baseline, Performance and Quality frame-time/FPS results on the target laptop.
3. Check all dimensions and major visual paths; tune budgets without silently disabling requested effects.
4. Fix any runtime/visual issues and publish a stable release only after target-hardware validation.
