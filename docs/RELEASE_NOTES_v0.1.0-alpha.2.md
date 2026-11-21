# Lightning v0.1.0-alpha.2

**Pre-release for testing — not a stable or hardware-validated release.**

## Project and compatibility

Lightning is a feature-preserving port based on the user-supplied **MakeUp Ultra Fast v9.6** source archive and the asc pixi Minecraft shader template. It is not a BSL-source port.

The development baseline is Minecraft Java 1.21.5, Fabric Loader 0.16.14, Iris 1.8.11, Sodium 0.6.12 and Java 21. The intended target is Windows 10 with an Intel Core i3-5005U, Intel HD Graphics 5500 and 8 GB RAM, launched through SK Launcher. The target machine has not yet been benchmarked.

## Included

- One shaderpack ZIP; no companion resource/source pack is required.
- Performance and Quality profiles that keep the major requested effects available.
- Reduced AO, SSR, cloud, godray, bloom and motion-blur budgets for the Performance profile.
- Original MakeUp settings UI retained, with Lightning's feature-preserving profiles.
- Two bounded cloud-opacity early exits.
- Original SSR fallback code retained byte-for-byte after an earlier non-equivalent early-return experiment was reverted.
- LGPL-3.0 license text and third-party attribution included.

## Validation completed

- 346 of 348 uploaded source files reproducibly verified through exact copies or documented deterministic transformations; the two config/options exceptions have been semantically reconciled.
- Static source/include, feature and profile checks pass.
- All 212 distributable vertex/fragment entrypoints pass the offline glslangValidator syntax compilation matrix. The test supplies compile-only Iris/Distant Horizons interface shims; this is not GPU-driver or Iris program-link validation.
- Gradle shaderpack ZIP packaging passes.
- A headless Fabric/Iris development-client startup test passes. The log confirms Minecraft 1.21.5, Iris 1.8.11, Sodium 0.6.12 and an active OpenGL debug context; Lightning-dev is configured in Iris. The test does not enter a world or prove that the shaderpack loads or compiles in-world.

## Not yet validated

- In-world Iris shaderpack loading and program linking
- Visual quality and correctness across all dimensions and major rendering paths
- Windows Intel HD Graphics 5500 driver behaviour
- FPS and frame-time improvements on the target laptop

No FPS gain or visual-equivalence claim is made. Treat this release as an installable test build and report runtime issues before considering a stable release.

## Installation

Copy `Lightning-0.1.0-alpha.2-shaderpack.zip` into the matching SK Launcher instance's `.minecraft/shaderpacks` directory, launch the matching Fabric/Iris profile and select Lightning in Iris. Start with the Performance profile.

See [Target hardware validation](TARGET_HARDWARE_VALIDATION.md) for the test procedure.
