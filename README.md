# Lightning

A feature-preserving Minecraft shaderpack project targeted at Intel HD Graphics 5500 and low-power Intel Core i3 hardware.

## Project roots

Lightning is a separate project built from these two authorized roots:

1. The user-supplied MakeUp Ultra Fast v9.6 archive, used as the rendering-feature and source-reference baseline.
2. [ascpixi/minecraft-shader-template](https://github.com/ascpixi/minecraft-shader-template), used as the Gradle, Iris development-client and packaging foundation.

The uploaded source archive identifies as MakeUp Ultra Fast v9.6; Lightning is a MakeUp-derived port, not a BSL-source port. No Aetheris-Shaders files, commits, branches or releases are used as Lightning's foundation.

## Target machine

- Intel Core i3-5005U, 2 cores / 4 threads, 2.00 GHz
- Intel HD Graphics 5500 (OpenGL 4.3)
- 8 GB RAM
- Windows 10
- Minecraft Java launched through SK Launcher with Iris and Sodium

The development template currently pins Minecraft 1.21.5, Iris 1.8.11 and Sodium 0.6.12. Confirm the installed game profile before treating those as the final supported versions.

## Feature-preserving profiles

The current pack includes **Performance** and **Quality** profiles. Performance reduces shadow distance/resolution and sample budgets while keeping the major rendering features enabled in the shader code:

- Dynamic and coloured shadows
- Volumetric clouds, cloud reflections and End clouds
- Screen-space reflections, water refraction and sun/moon reflections
- Enhanced ambient occlusion
- Temporal antialiasing (with TAA+FXAA available in Quality)
- Bloom and depth-based godrays in Performance; full shadow-aware volumetric lighting in Quality
- Material gloss, depth of field and motion blur

The Performance profile uses reduced budgets (AO 4 steps, SSR 5 steps, volumetric clouds 7 samples, godrays 4 steps, bloom 2 sample pairs and motion blur 3 samples). These are candidate settings to benchmark—not a promise of a particular FPS or unchanged visual quality.

The cloud loops stop sampling once accumulated opacity reaches the final clamp threshold. The original SSR out-of-screen fallback remains unchanged; an attempted early-return optimization was reverted because it changed the final fallback coordinate.

## Build and development

```bash
# Build a distributable shaderpack ZIP
./gradlew --no-daemon zipShaderpack

# Compile every vertex/fragment entrypoint with the offline GLSL checker
python tools/compile_shader_stages.py

# Launch the Iris development client with the shaderpack staged
./gradlew runShaderClient

# Run the headless Iris client-startup smoke test (CI environment)
python tools/run_iris_smoke.py
```

The packaged ZIP is written under `build/releases/`. The distributable is one shaderpack ZIP; no companion source/resource pack is required. GitHub Actions validates source structure, compiles all entrypoints, builds the ZIP and performs a headless Iris client-startup smoke test. A marked release commit publishes the pre-release to this same repository.

## Validation status

- Source inventory and deterministic source-port audit: 346/348 files reproducibly verified; the two config/options exceptions have been semantically reconciled.
- Static shader structure, includes, feature macros and performance-budget assertions: passing in CI.
- Offline GLSL syntax compilation: **212/212 vertex/fragment entrypoints pass** with compile-only Iris/Distant Horizons interface shims.
- Gradle shaderpack ZIP packaging: passing in CI.
- Headless Fabric/Iris startup: passing; Minecraft 1.21.5, Iris 1.8.11 and Sodium 0.6.12 load, and Iris activates an OpenGL debug context. The test confirms Lightning-dev is configured in Iris, but it does not enter a world or load/compile the shaderpack in-world.
- Iris in-world shader loading/linking, visual comparisons, Windows/Intel HD 5500 driver validation and target-hardware FPS/frame-time benchmarking: **not yet verified**.

The `v0.1.0-alpha.2` release is a test pre-release, not a stable or hardware-validated release. Do not interpret the compiler checks as a performance benchmark.

For a reproducible uploaded-ZIP source comparison, run `python tools/verify_source_port.py /path/to/Shader.zip` from a local checkout. The uploaded source archive is intentionally not bundled into the distributable.

See:
- [Porting status](docs/PORTING_STATUS.md)
- [Feature preservation map](docs/FEATURE_PRESERVATION_MAP.md)
- [Performance design](docs/PERFORMANCE_DESIGN.md)
- [Target hardware validation guide](docs/TARGET_HARDWARE_VALIDATION.md)
- [Third-party notices and attribution](THIRD_PARTY_NOTICES.md)
- [Source file ledger](reference/source-file-map.csv)
- [v0.1.0-alpha.2 release](https://github.com/Pawar-47/Lightning-/releases/tag/v0.1.0-alpha.2)

## Licensing and attribution

The reference source identifies MakeUp Ultra Fast v9.6 by Javier Garduño (KDXavier) and carries LGPL-3.0 source headers. The applicable full license is included in `LICENSES/LGPL-3.0.txt`. Preserve upstream copyright and license notices in derivative files and include the corresponding source when distributing covered code. See `THIRD_PARTY_NOTICES.md`.
