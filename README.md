# Lightning

A Minecraft shader pack project tailored for Intel HD Graphics 5500 and the Intel Core i3-5005U class of low-power hardware.

## Project status

This repository is the dedicated, independent development home for Lightning. It is being built from two authorized roots:

- The user-supplied MakeUp Ultra Fast v9.6 shader archive, used as the feature and source-reference baseline.
- `ascpixi/minecraft-shader-template`, used as the development and build foundation.

No Aetheris-Shaders files or commits are used as a project base.

## Design goals

- Preserve the reference pack's major rendering features, including dynamic and coloured shadows, volumetric clouds, cloud reflections, End clouds, screen-space reflections, refraction, sun/moon reflections, enhanced ambient occlusion, anti-aliasing, bloom, volumetric light, material gloss, depth of field, and motion blur.
- Provide a feature-preserving Performance profile for Intel HD 5500 rather than gaining FPS by silently deleting effects or pipeline passes.
- Keep effects configurable and use lower-cost algorithms, reduced sample counts, sensible render distances, and appropriately scaled intermediate buffers where compatible with Iris.
- Validate source coverage, GLSL compilation, Iris runtime loading, visual output, and real-device performance separately. No unmeasured FPS or visual-quality claims are made.

## Hardware target

Primary target: Intel Core i3-5005U, Intel HD Graphics 5500 (OpenGL 4.3), 8 GB RAM, Linux Mint, Minecraft Java with Iris and Sodium.

The exact Minecraft/Iris/Sodium versions will be pinned after compatibility verification against the target installation.

## Licensing and attribution

The reference shader identifies itself as MakeUp Ultra Fast v9.6 by Javier Garduño (KDXavier), with LGPL-3.0 source headers. Preserve upstream copyright notices and the full applicable license when porting or redistributing its code. See `THIRD_PARTY_NOTICES.md` and the source attribution in the ported files.

## Current status

Initial repository bootstrap. The complete source inventory, file-by-file port map, compatibility work, and feature reactivation are tracked in project documentation as implementation proceeds.
