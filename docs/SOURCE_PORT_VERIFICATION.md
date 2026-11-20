# Uploaded-source to Lightning port verification

Checkpoint: 2026-11-21  
Repository: `Pawar-47/Lightning-`  
Reference: the user-uploaded MakeUp Ultra Fast v9.6 `Shader.zip`

## Result

**346 of 348 uploaded files are verified against their active repository destinations.**

- 136 files are byte-for-byte copies of the uploaded ZIP.
- 210 vertex/fragment entrypoints differ only by the deliberate GLSL version migration: the first `#version 120` directive is replaced with `#version 330 compatibility`. All remaining bytes are preserved.
- Two archive-specific files are intentionally customized/merged rather than copied unchanged:
  - `shaders/lib/config.glsl`
  - `shaders/shaders.properties`

The exact original Git blob hashes for the two source exceptions are recorded in the final column of `reference/source-file-map.csv`. The original uploaded ZIP remains the source authority; these two active files are intentionally customized/merged rather than represented as byte-identical copies.

## Verification method

For every source file, compute its Git blob SHA-1 as:

`SHA1("blob " + byte_length + NUL + file_bytes)`

For the 210 shader stages, apply only the documented first-line version replacement before computing the expected blob hash. Compare the expected hash and destination path with the committed Git tree. The aggregate digests below are SHA-1 values over the sorted sequence:

`destination_path + NUL + destination_git_blob_sha1 + newline`

The same aggregate was computed from the uploaded ZIP's expected destination bytes and the live `main` tree. Each pair matches. Reproduce the per-file comparison locally with `python tools/verify_source_port.py /path/to/Shader.zip` from a Lightning checkout.

| Destination family | Files | Verified aggregate SHA-1 |
|---|---:|---|
| `docs/` | 1 | `883f28d4020f987f169bf2b437f8c5b5c3049814` |
| `reference/` | 3 | `a4e3f6b1604919363344cb18c318d849dce157d0` |
| `shaders/` root entrypoints and metadata | 57 | `996a5b107aed0631922cef032186567acc9dced7` |
| `shaders/common/` | 41 | `3bba39394ee1cd1435b3bd608b80945902f160b0` |
| `shaders/lang/` | 9 | `4a11948f1234304693f5c439b051de7522e54762` |
| `shaders/lib/` excluding customized `config.glsl` | 37 | `6f8c1f1830c77721e9ae7ed5a07ed66ef6a194f4` |
| `shaders/src/` | 22 | `8cd0591c09888f627db47f5a0f47d1995deb6c27` |
| `shaders/textures/` | 6 | `6fb4e2c8db743a8888e08b0a80e0b2aa63f76d19` |
| `shaders/world-1/` | 55 | `fefad057c8a689bbde69adab937dbef40d992ea4` |
| `shaders/world0/` | 58 | `38bd1d3bba10b060c855b7a9953595abd8fe22d3` |
| `shaders/world1/` | 57 | `a431a544435b6c705a5012b9593577f66d90edc3` |
| **Total verified** | **346** | |

## The two intentional exceptions

The original archive versions are identified by their Git blob hashes in the source ledger and the validator checks that the expected hashes are recorded in the source ledger:

- `shaders/lib/config.glsl`: `7c8f086dfa749f2c61707782786897620a3564d5`
- `shaders/shaders.properties`: `712ebede6b2ad78a92ee6cb39bf1f5fb07bdfdb1`

The active config restores the requested rendering features and applies Lightning's lower-cost budgets. The active pack-root `shaders.properties` merges the original settings UI with Lightning's Performance and Quality profiles. It also retains the source's conditional composite-pass rules so those passes execute whenever their effects are enabled. Their line-by-line semantic diff remains a separate review item; neither is falsely labelled byte-identical.

## What this does not prove

This source-port verification does not prove GLSL compilation, Iris runtime loading, visual parity, frame-time performance or compatibility with the user's installed Minecraft version. Those checks remain open and are tracked in `PORTING_STATUS.md`.
