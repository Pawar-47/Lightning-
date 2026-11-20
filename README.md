# Lightning

A feature-preserving Minecraft shaderpack project tuned for Intel HD Graphics 5500 and low-power Intel Core i3 hardware.

## Project roots

Lightning is a separate project built from these two authorized roots:

1. The user-supplied MakeUp Ultra Fast v9.6 archive, used as the rendering-feature and source-reference baseline.
2. [ascpixi/minecraft-shader-template](https://github.com/ascpixi/minecraft-shader-template), used as the Gradle, Iris development-client and packaging foundation.

No Aetheris-Shaders files, commits, branches or releases are used as Lightning's foundation.

## Target machine

- Intel Core i3-5005U, 2 cores / 4 threads, 2.00 GHz
- Intel HD Graphics 5500 (OpenGL 4.3)
- 8 GB RAM
- Linux Mint
- Minecraft Java with Iris and Sodium

The development template currently pins Minecraft 1.21.5, Iris 1.8.11 and Sodium 0.6.12. Confirm the user's installed game profile before treating those as the final supported versions.

## Feature-preserving profiles

The current pack includes **Performance** and **Quality** profiles. Performance reduces shadow distance/resolution and sample budgets while keeping the major rendering features enabled in the shader code:

- Dynamic and coloured shadows
- Volumetric clouds, cloud reflections and End clouds
- Screen-space reflections, water refraction and sun/moon reflections
- Enhanced ambient occlusion
- Temporal antialiasing (with TAA+FXAA available in Quality)
- Bloom and depth-based godrays in Performance; full shadow-aware volumetric lighting in Quality
- Material gloss, depth of field and motion blur

The Performance profile uses reduced budgets (AO 4 steps, SSR 5 steps, volumetric clouds 7 samples, godrays 4 steps, bloom 2 sample pairs and motion blur 3 samples). These are code/profile settings to test—not a promise of a particular FPS or unchanged visual quality.

## Build and development

```bash
# Build a distributable shaderpack ZIP
./gradlew --no-daemon zipShaderpack

# Launch the Iris development client with the shaderpack staged
./gradlew runShaderClient
```

The packaged ZIP is written under `build/releases/`. GitHub Actions runs static source checks and builds the ZIP on pushes and pull requests.

## Validation status

- Static shader include/version checks: passing in CI.
- Feature macro/profile and performance-budget checks: passing in CI.
- Reference language and texture asset checks: passing in the latest completed CI run.
- Gradle shaderpack ZIP packaging: passing in CI.
- GLSL stage compile/link: not yet verified.
- Iris runtime loading and visual comparison: not yet verified.
- FPS/frame-time benchmark on the target laptop: not yet verified.
- No finished release has been published yet.

For a reproducible uploaded-ZIP source comparison, run `python tools/verify_source_port.py /path/to/Shader.zip` from a local checkout.

See:
- [Porting status](docs/PORTING_STATUS.md)
- [Feature preservation map](docs/FEATURE_PRESERVATION_MAP.md)
- [Performance design](docs/PERFORMANCE_DESIGN.md)
- [Third-party notices and attribution](THIRD_PARTY_NOTICES.md)
- [Source file ledger](reference/source-file-map.csv)

## Licensing and attribution

The reference source identifies MakeUp Ultra Fast v9.6 by Javier Garduño (KDXavier) and carries LGPL-3.0 source headers. The applicable full license is included in `LICENSES/LGPL-3.0.txt`. Preserve upstream copyright and license notices in derivative files and include the corresponding source when distributing covered code. See `THIRD_PARTY_NOTICES.md`.
