# Uploaded archive exception reconciliation

Checkpoint: 2026-11-21

This document records the intentional changes to the two uploaded-archive files that cannot be copied byte-for-byte into the active Lightning pack. The exact source Git blob hashes are in `reference/source-file-map.csv`. The uploaded `Shader.zip` remains the source of truth.

## 1. `shaders/lib/config.glsl`

The uploaded ZIP is an FPS-tuned configuration with expensive features disabled. Lightning re-enables the requested effects and keeps their implementations and pipeline passes.

| Setting | Uploaded ZIP | Active Lightning config | Reason |
|---|---:|---:|---|
| `REFLECTION_SLIDER` | 0 | 2 | Restore screen-space raymarched reflections |
| `REFRACTION` | 0 | 1 | Restore water refraction |
| `AO` | 0 | 1 | Restore enhanced ambient occlusion |
| `AOSTEPS` | 3 | 4 | Keep AO enabled with a bounded sample budget |
| `AA_TYPE` | 0 | 2 | Restore temporal antialiasing |
| `SUN_REFLECTION` | 0 | 1 | Restore sun/moon water highlights |
| `V_CLOUDS` | 0 | 1 | Restore static volumetric clouds |
| `VOL_LIGHT` | 0 | 1 | Restore the cheaper depth-based godray path |
| `MOTION_BLUR_SAMPLES` | 4 | 3 | Keep motion blur with fewer taps |
| `CLOUD_STEPS_AVG` | 7 | 7 | Retain the low cloud sample budget |
| `RAYMARCH_STEPS` | 5 | 5 | Retain the low SSR sample budget |
| `GODRAY_STEPS` | 4 | 4 | Retain the bounded volumetric-light budget |
| `CHEAP_GODRAY_SAMPLES` | 4 | 4 | Retain the bounded depth-based godray budget |
| `BLOOM_SAMPLES` | 2.0 | 2.0 | Retain the minimum bloom sample-pair budget |
| `SHADOW_QTY_SLIDER` | 1 | 1 | Keep the lowest shadow-map tier |
| `SHADOW_DISTANCE_SLIDER` | 0 | 0 | Keep the shortest shadow distance |

The following feature defines are restored in the active config: dynamic shadow casting, coloured shadows, DOF, motion blur, cloud reflections, End clouds, bloom and material gloss. They are also included in the Performance profile. Their shader modules were not deleted.

## 2. `shaders/shaders.properties`

The uploaded options file includes the complete MakeUp settings UI and legacy profiles. Lightning relocates the active options file to the shaderpack root, preserves the original option screens, and adds dedicated `Performance` and `Quality` profiles.

### Performance profile

- Dynamic and coloured shadows remain enabled at the lowest shadow tier and shortest distance.
- SSR, refraction and sun/moon reflections remain enabled.
- AO remains enabled at 4 steps.
- TAA remains enabled.
- Volumetric clouds remain enabled at 7 average steps; cloud reflections and End clouds remain enabled.
- Bloom remains enabled at 2 sample pairs.
- DOF and motion blur remain enabled; motion blur uses 3 samples and reduced strength.
- `VOL_LIGHT=1` selects the cheaper depth-based godray path.

### Quality profile

- Retains the same feature set with higher shadow, AO, cloud, bloom and motion-blur budgets.
- `AA_TYPE=3` enables the TAA+FXAA path.
- `VOL_LIGHT=2` selects the full shadow-aware volumetric-light path.

### Pipeline routing

The source's conditional pass rules have been restored:

- `program.composite1.enabled=BLOOM || DOF`
- `program.composite2.enabled=AA_TYPE || MOTION_BLUR`

Both composite passes execute in Performance and Quality because their effects are enabled. They are skipped only when all effects served by that pass are disabled in another profile. The shadow pass remains conditional on `SHADOW_CASTING`.

The source's `MAX_FPS` and `MAX_FPS_NOFOG` profiles were not carried into the active options because they disable multiple required effects and explicitly skip composite passes. The Lightning Performance profile is the supported low-cost profile instead.

## Review boundary

## Completed semantic diff against the uploaded ZIP\n\nA direct line-by-line comparison of both active packaged files against the uploaded archive was completed on 2026-11-21 using the current CI shaderpack artifact. The diff is limited to the intentional changes below; no other config defaults, option-screen entries or UI mappings differ.\n\n### Config diff\n\nExactly 17 option lines change in `config.glsl`: reflection mode, refraction, DOF activation, AO activation and steps, AA mode, motion blur activation and sample count, sun/moon reflections, coloured shadows, volumetric cloud mode, cloud reflections, End clouds, bloom, volumetric light mode, material gloss and shadow casting. All other 314 lines are identical to the uploaded archive. The changes restore the user-required feature set while retaining reduced sample budgets.\n\n### Properties diff\n\nThe original `MAX_FPS` and `MAX_FPS_NOFOG` profiles are removed because they disable the major requested effects and skip composite passes. They are replaced by the dedicated `Performance` and `Quality` profiles. The original options screens and remaining legacy profiles are retained. The two composite pass conditions are unchanged in meaning and are present exactly once in the active file. No other option UI or uniform mapping changes were found.\n\nThe two exception files are therefore **semantically reconciled**. This does not substitute for Iris runtime loading or visual verification.
