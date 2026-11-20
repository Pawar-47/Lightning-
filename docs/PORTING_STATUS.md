# Porting status and verified checkpoint

Last updated: 2026-11-21

## Project roots and boundary

- New project repository: `Pawar-47/Lightning-`
- Development/build foundation: `ascpixi/minecraft-shader-template`, upstream revision `ab2b99c9e1715cb951936157fe3c2ef94890233b`
- User-supplied reference archive: `Shader.zip`, identified as MakeUp Ultra Fast v9.6 by Javier Garduño (KDXavier)
- No Aetheris-Shaders source, commits, branches or releases are used as Lightning's foundation.

## Uploaded archive inventory

The uploaded archive contains 348 actual files (742,051 uncompressed bytes) after excluding macOS `__MACOSX` metadata. The complete local inventory and SHA-256 manifest were generated before repository bootstrap.

Source families:

| Family | Files |
|---|---:|
| `shaders/common/` | 41 |
| `shaders/lib/` | 38 |
| `shaders/src/` | 22 |
| `shaders/world0/` | 58 |
| `shaders/world-1/` | 55 |
| `shaders/world1/` | 57 |
| Root docs, wrappers, properties, language files, textures and metadata | Remaining files |

The archive-specific `shaders/lib/config.glsl` and `shaders/shaders.properties` differ from the current upstream GitHub branch. Their uploaded-archive SHA-1 values are respectively:

- `config.glsl`: `7c8f086dfa749f2c61707782786897620a3564d5`
- `shaders.properties`: `712ebede6b2ad78a92ee6cb39bf1f5fb07bdfdb1`

Do not overwrite these archive-specific variants with current upstream versions and then describe them as byte-identical to the ZIP.

## Current implementation checkpoint

### Present and checked

- Template Gradle build foundation imported.
- Gradle project identity changed to Lightning:
  - archive name: `Lightning`
  - group: `dev.pawar47.lightning`
  - version: `0.1.0-alpha.1`
- MakeUp source modules currently present at active shader paths:
  - `shaders/common/`: 41 files; Git blob hashes match upstream MakeUp tree.
  - `shaders/lib/`: 38 files; Git blob hashes match upstream MakeUp tree.
  - `shaders/src/`: 22 files; Git blob hashes match upstream MakeUp tree.
- One common module (`solid_blocks_fragment.glsl`) was also hash-checked directly against the uploaded ZIP and matched.
- All 9 `shaders/lang/*.lang` files and all 3 PNG textures plus their 3 `.mcmeta` animation files are now present; their Git blob hashes match the uploaded ZIP exactly.
- All 210 vertex/fragment entrypoints now declare `#version 330`; sampled root, Overworld, Nether and End wrappers retain the source structure with the GLSL compatibility-version migration. A complete per-wrapper text diff is still pending.
- The source tree contains 344 files under `shaders/`; 343 now exist at their active destination paths. The source `shaders/shaders.properties` is intentionally relocated/merged into the pack-root `shaders.properties`.
- Root and dimension-specific wrapper samples were checked against upstream. Their main migration is `#version 120` to `#version 330 compatibility`; the shared source includes remain unchanged.
- Upstream developer documentation, README, helpful notes and upstream shader properties are retained under `reference/makeup-ultra-fast-upstream/` where imported. This is not yet a complete byte-for-byte mirror of the uploaded archive.
- Full MakeUp settings UI and original option screens have been restored into the pack-root `shaders.properties`; added Lightning `Performance` and `Quality` profiles.
- Performance budgets currently set in `shaders/lib/config.glsl`: AO 4 steps, motion blur 3 samples, SSR 5 steps, volumetric clouds 7 samples, godrays 4 steps, bloom 2 samples, shorter shadow distance and lower shadow-map quality tier. DOF and motion blur are enabled. Major effects are not removed from the code.
- Added `tools/validate_shaderpack.py` to check shader-stage version declarations, include resolution and required feature-module presence.
- Added GitHub Actions workflow `.github/workflows/shaderpack-validation.yml`.

### CI evidence

- Workflow run `44808050870` passed static validation and Gradle shaderpack packaging.
- Run `44808317936` passed the static validator and completed the `zipShaderpack` build and artifact upload; GitHub was still finalizing post-job cleanup when last checked.
- Run `44808367005` was still in progress at the last check.
- These are structure/package checks, not GLSL stage compilation, Iris runtime loading, visual equivalence or hardware performance benchmarks.

## Known gaps — do not mark complete

1. Exact byte-for-byte comparison of all 348 uploaded ZIP files against repository files is incomplete.
2. The source archive's config and properties variants still need exact recovery/porting; current active config originated from upstream and was then tuned, not copied byte-for-byte from the ZIP.
3. All dimension-specific wrappers and root shader entrypoints need a full automated source-to-port comparison, not just spot checks.
4. The template's standard `gradle-wrapper.jar` has not been imported. CI uses Gradle 8.12.1 directly; the checked-in `gradlew` scripts therefore need a wrapper-JAR fix before claiming local wrapper execution works.
5. No complete Iris/OptiFine shader-stage compile matrix has run.
6. No Minecraft + Iris + Sodium client runtime load test has run.
7. No visual comparison across Overworld, Nether, End, water, clouds, shadows and post-processing has run.
8. No FPS/frame-time benchmark has run on the user's Intel Core i3-5005U / Intel HD 5500 / 8 GB Linux Mint machine.
9. No release has been created. Do not release the current CI ZIP as a finished shaderpack.

## Next work order

1. Complete exact archive-to-repository per-file checksums and disposition records.
2. Recover the archive-specific config/properties and integrate the Performance profile without losing option screens, textures, dimension rules or pipeline passes.
3. Finish root and dimension wrapper port checks, then audit all buffer/pass dependencies.
4. Finish exact ZIP comparison for the 210 wrapper stages and all remaining root/property files; preserve the archive-specific config/properties differences.
5. Add actual GLSL compile/link validation using the same Iris preprocessing path as the template.
6. Run Iris runtime loading and dimension/feature smoke tests.
7. Compare visual output and tune performance budgets.
8. Benchmark on the target laptop; only then prepare a release.
