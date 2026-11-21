# Lightning performance design

## Target

Primary hardware target: Intel Core i3-5005U (2 cores / 4 threads, 15 W), Intel HD Graphics 5500 (OpenGL 4.3), 8 GB RAM, Windows 10. The iGPU shares system memory; actual RAM channel configuration and driver behavior must be measured on the target laptop.

The initial development baseline in the authorized template is Minecraft 1.21.5, Iris 1.8.11, Sodium 0.6.12 and Java 21. This is a provisional template baseline, not yet a confirmed match for the user's installed Minecraft profile.

## Non-negotiable visual feature set

The Performance profile must keep these features available and must not gain FPS by silently removing their pipeline passes:

- Dynamic shadows and coloured shadows
- Volumetric clouds, cloud reflections and End clouds
- Screen-space reflections, refraction and sun/moon reflections
- Enhanced ambient occlusion
- TAA and/or FXAA
- Bloom
- Volumetric light / godrays
- Material gloss
- Depth of field
- Motion blur

Individual effects may be user-configurable, but the Performance profile must use a lower-cost implementation rather than silently forcing them off.

## Candidate optimizations (to validate, not benchmark claims)

| Feature | Performance-oriented implementation to investigate |
|---|---|
| Dynamic shadows | One shadow pass; conservative map resolution/distance; Iris shadow culling; reduced PCF taps; measure CPU geometry cost |
| Coloured shadows | Keep colour-shadow path; limit eligible translucent casters; minimize colour-buffer cost |
| Volumetric clouds | Fixed low step budget, exact early exit once accumulated opacity reaches the final clamp threshold, distance LOD and cheaper far-field noise |
| Cloud reflections | Limited-sample reflection approximation; do not raymarch the full cloud volume for every water pixel |
| End clouds | Dimension-specific reduced step budget, not a disabled feature |
| SSR | Bounded depth-aware march, immediate return on out-of-screen rays, edge rejection and fallback reflections |
| Refraction | Reuse water normals; bounded screen offset and fewer redundant texture reads |
| Sun/moon reflections | Analytic directional highlight plus bounded screen-space contribution |
| AO | Compact sample kernel; evaluate half-resolution plus depth-aware upsampling; avoid halos |
| TAA/FXAA | Conservative history weight, disocclusion rejection, selectable FXAA fallback/finishing pass |
| Bloom | Low-resolution bright extraction and short separable blur |
| Volumetric light | Low-step depth-based shaft path in Performance; preserve higher-cost shadow-aware path as a quality option |
| Material gloss | Restrict to mapped material classes; bounded analytic specular, no required PBR resource pack |
| DOF | Retain depth-aware blur with a bounded sample count and user controls |
| Motion blur | Retain velocity/depth-aware path with bounded taps and user controls |

## Constraints

- GLSL 330 is the template baseline. Do not introduce compute shaders, SSBOs or other higher-version requirements without confirming support in Iris and the target driver.
- Do not downscale a framebuffer that a G-buffer pass writes to unless Iris explicitly supports that pass/buffer arrangement. Scaled intermediate buffers belong only in compatible deferred/composite stages.
- No FPS or visual-equivalence target is considered met until measured on the target laptop.
- Keep all pipeline passes and document every buffer dependency.
