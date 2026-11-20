# Reference-to-Lightning port status

## Source baseline

- Archive: user-supplied `Shader.zip`
- Identified upstream: MakeUp Ultra Fast v9.6 by Javier Garduño (KDXavier)
- Actual source files after excluding macOS `__MACOSX` metadata: **348**
- Uncompressed source size: **742,051 bytes**
- File inventory and SHA-256 manifest prepared locally before repository bootstrap.
- Source families: root documentation/properties/wrappers; `shaders/common`; `shaders/lib`; `shaders/src`; Overworld (`world0`); Nether (`world-1`); End (`world1`); language files; textures and animation metadata.

## Porting rules

Every source file must receive an explicit disposition. Allowed dispositions:

- **ported** — behavior-preserving GLSL 330/Iris translation, with a recorded source/destination mapping.
- **copied** — retained byte-for-byte where format and runtime compatibility permit.
- **rewritten** — replaced with a documented equivalent because the template/runtime architecture differs.
- **not shipped** — only when there is a concrete technical, licensing, or compatibility reason; document the reason and replacement behavior.

A file is not complete because a similarly named destination exists. Record semantic equivalence and validation independently.

## Current checkpoint

| Work item | Status |
|---|---|
| Uploaded archive extraction and inventory | Complete locally |
| Source feature/disabled-feature audit | Complete locally |
| New Lightning repository bootstrap | Complete |
| Template build foundation | In progress; core Gradle files and initial shader wrappers imported |
| Full template file parity | Pending |
| Full 348-file source-to-destination mapping committed | Pending |
| GLSL 120 to GLSL 330/Iris port | Not started |
| Feature-preserving Performance profile | Design stage |
| Static validation | Not started |
| Shader-stage compilation | Not started |
| Iris runtime load test | Not started |
| Visual comparison | Not started |
| Intel HD 5500 frame-time/FPS benchmark | Not started |
| Release artifact | Not started |

## Validation labels

- **Static**: file presence, include resolution, option/property consistency, preprocessor and syntax checks.
- **Compile**: actual vertex/fragment stage compilation and link checks with the intended Iris preprocessing.
- **Runtime**: shaderpack loads in the selected Minecraft + Iris + Sodium combination.
- **Visual**: scene-by-scene comparison for lighting, shadows, water, clouds, AO and post-processing.
- **Performance**: repeatable frame-time/FPS measurements on the target laptop, with settings and scene recorded.

Do not mark later validation stages complete based on earlier-stage success.
