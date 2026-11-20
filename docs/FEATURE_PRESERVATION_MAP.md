# Feature preservation and performance mapping

This map records where the MakeUp-derived feature implementation lives and which budget is currently used for Lightning's Performance profile. It is a source-level map, not proof of runtime correctness.

| Feature | Source implementation / pipeline | Performance budget | State |
|---|---|---|---|
| Dynamic shadows | `lib/shadow_frag.glsl`, `lib/shadow_vertex.glsl`, dimension `shadow.fsh/.vsh` wrappers | Shadow tier 1, distance tier 0; shadow culling enabled | Enabled in config/profile; compile/runtime pending |
| Coloured shadows | `config.glsl` `COLORED_SHADOW`, shadow and deferred colour path | Keep colour path; constrain shadow distance/map tier | Enabled; visual validation pending |
| Volumetric clouds | `lib/volumetric_clouds.glsl`, `lib/volumetric_clouds_vertex.glsl`, deferred wrappers | Static volumetric mode; 7 average steps | Enabled; visual/performance validation pending |
| Cloud reflections | Cloud code plus `lib/water.glsl` reflection path | Keep enabled; SSR/cloud reflection sampling remains bounded | Enabled; water-scene validation pending |
| End clouds | `lib/volumetric_clouds_end.glsl`, End dimension wrappers | Shared reduced cloud budget | Enabled; End runtime validation pending |
| Screen-space reflections | `lib/water.glsl`, `REFLECTION_SLIDER=2`, `RAYMARCH_STEPS` | 5 raymarch steps | Enabled; artifact/ghosting validation pending |
| Refraction | `lib/water.glsl`, water G-buffer path | Reuse existing water normal/depth data; bounded offsets | Enabled; water validation pending |
| Sun/moon reflections | `lib/water.glsl`, `SUN_REFLECTION` | Existing analytic/directional path | Enabled; visual validation pending |
| Enhanced AO | `lib/ao.glsl`, deferred fragment path | 4 AO steps | Enabled; halo/quality validation pending |
| TAA / FXAA | `lib/fast_taa.glsl`, `lib/fxaa.glsl`, composite2 | TAA enabled in Performance; FXAA+TAA available in Quality profile | Source preserved; runtime validation pending |
| Bloom | `lib/bloom.glsl`, `lib/blur.glsl`, composite1 | 2 bloom sample pairs | Enabled; brightness/halo validation pending |
| Volumetric light / godrays | `lib/volumetric_light.glsl`, composite path | True volumetric mode, 4 godray steps in Performance and Quality | Enabled in Performance; higher-cost volumetric mode in Quality |
| Material gloss | `lib/material_gloss_fragment.glsl`, `lib/material_gloss_fragment_voxy.glsl` | Existing material classification; no external PBR pack dependency | Enabled; material validation pending |
| Depth of field | `config.glsl`, depth helpers and composite1 | DOF enabled at existing 0.09 strength | Enabled; scene/performance validation pending |
| Motion blur | `lib/motion_blur.glsl`, composite2 | 3 samples, reduced strength 0.75 in Performance | Enabled; ghosting/performance validation pending |

## Pass-preservation rules

- Keep the shadow pass active whenever shadow casting is enabled.
- Keep deferred processing active for AO, cloud composition and scene preparation.
- Keep composite1 active for bloom/DOF.
- Keep composite2 active for temporal AA/motion blur.
- Do not drop any pass solely to improve an FPS number.
- If a pass can be skipped only when all of its effects are disabled, document the exact condition and ensure the Performance profile does not satisfy that condition.

## Important technical caveats

- The current root `shaders.properties` is based on the upstream options file with Lightning profiles added. The uploaded ZIP's properties file is a known different variant and still needs an exact archive comparison/merge.
- The active config was taken from the upstream source and tuned. It is not byte-identical to the uploaded ZIP's `config.glsl`; the archive-specific file has a known different SHA-1 and must be reconciled before the source-port ledger can be closed.
- The current CI validates include resolution, GLSL version declarations, enabled feature macros, performance budgets and shaderpack ZIP packaging. It does not compile/link GLSL stages or run Iris.
