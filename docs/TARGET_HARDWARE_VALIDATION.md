# Target-hardware validation guide

This guide is for the intended Windows 10 machine: Intel Core i3-5005U, Intel HD Graphics 5500 and 8 GB RAM. The CI checks do not substitute for this test.

## Match the development baseline

The repository's current template baseline is:

- Minecraft Java 1.21.5
- Fabric Loader 0.16.14
- Iris 1.8.11
- Sodium 0.6.12
- Java 21

Use a separate SK Launcher instance for this test. The installed game profile has not yet been confirmed, so do not assume another Minecraft/Iris version is supported.

## Install

1. Download the single `Lightning-0.1.0-alpha.2-shaderpack.zip` asset from the Lightning GitHub release.
2. Place the ZIP, without extracting it, in that SK Launcher instance's `.minecraft/shaderpacks` directory.
3. Start the matching Fabric profile and select **Lightning** in Iris.
4. Start with the **Performance** profile. Test **Quality** separately.

No companion resource pack or companion source pack is required.

## Keep comparisons fair

- Use the same world, coordinates, camera direction, time of day and weather for every run.
- Keep resolution, render distance, simulation distance and all Minecraft video settings unchanged between the no-shader baseline, Performance and Quality.
- Close browsers and other heavy background applications; do not change Java heap allocation between comparisons.
- Let the scene settle, then record FPS and frame-time behaviour for at least 60 seconds rather than relying on a momentary F3 reading.
- Record the GPU driver version and the exact Minecraft/Iris/Sodium versions shown by the launcher.

## Required scenes

1. Overworld forest: foliage, wind, shadows and ambient occlusion.
2. Open Overworld sky: volumetric clouds, sun/moon and godrays.
3. Water shoreline: reflections, refraction, transparency and edge stability.
4. Night/rain: coloured shadows, cloud rendering and temporal effects.
5. Nether: fog, lava and dimension-specific lighting.
6. End: End sky/cloud path and dimension-specific effects.
7. If Distant Horizons is installed, separately test its terrain and water integration.

## Report back

Capture screenshots and the latest Minecraft log after each profile. Record:

- No-shader baseline average FPS and observed frame-time stability
- Performance profile average FPS and any visual defects
- Quality profile average FPS and any visual defects
- Crashes, shader compile errors, missing effects or flickering

Do not treat the CI GLSL pass or headless client startup as proof of FPS improvement. No target-hardware performance result is claimed until these measurements are completed.
