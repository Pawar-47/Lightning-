#!/usr/bin/env python3
"""Compile every Lightning .fsh/.vsh entrypoint with glslangValidator.

This is an offline GLSL syntax/semantic smoke test, not an Iris runtime test.
Iris-style root-relative includes are normalized in a temporary copy only.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHADERS = ROOT / "shaders"
INCLUDE = re.compile(r'(?m)^(\s*#\s*include\s+)"/([^"]+)"')
VERSION = re.compile(r"(?m)^(\s*#\s*version\s+\d+[^\n]*)(\n|$)")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    compiler = shutil.which("glslangValidator")
    if not compiler:
        fail("glslangValidator is required (install the glslang-tools package)")

    stages = sorted(
        path for path in SHADERS.rglob("*")
        if path.is_file() and path.suffix in {".fsh", ".vsh"}
    )
    if len(stages) != 212:
        fail(f"expected 212 shader entrypoints (210 ported plus 2 template-provided), found {len(stages)}")

    failures: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="lightning-glsl-") as temporary:
        temp_root = Path(temporary)
        shadow_root = temp_root / "shaders"
        shutil.copytree(SHADERS, shadow_root)

        # Iris treats a leading slash in #include paths as shaderpack-root
        # relative. glslang uses ordinary include search paths, so normalize
        # that syntax in the temporary copy without touching tracked sources.
        for path in shadow_root.rglob("*"):
            if path.is_file() and path.suffix in {".fsh", ".vsh", ".glsl"}:
                content = path.read_text(encoding="utf-8")
                content = INCLUDE.sub(lambda match: match.group(1) + '"' + os.path.relpath(shadow_root / match.group(2), path.parent) + '"', content)
                path.write_text(content, encoding="utf-8")

        for source in stages:
            relative = source.relative_to(SHADERS)
            stage = "vert" if source.suffix == ".vsh" else "frag"
            content = (shadow_root / relative).read_text(encoding="utf-8")
            match = VERSION.search(content)
            if not match:
                failures.append((relative.as_posix(), "missing #version directive"))
                continue

            # GL_GOOGLE_include_directive is used only for this compiler
            # smoke test; Iris itself supplies its own shaderpack preprocessor.
            insertion = match.end(1)
            content = content[:insertion] + "\n#extension GL_GOOGLE_include_directive : require" + content[insertion:]
            temporary_entry = shadow_root / relative
            temporary_entry.write_text(content, encoding="utf-8")

            command = [
                compiler,
                "-S", stage,
                str(temporary_entry),
            ]
            result = subprocess.run(
                command,
                cwd=temp_root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            if result.returncode:
                failures.append((relative.as_posix(), result.stdout.strip()))

    if failures:
        for path, output in failures[:30]:
            print(f"FAIL: {path}\n{output}")
        if len(failures) > 30:
            print(f"... and {len(failures) - 30} additional compiler failure(s)")
        fail(f"{len(failures)} of {len(stages)} shader entrypoints failed GLSL compilation")

    print(f"PASS: glslangValidator compiled all {len(stages)} GLSL 330 vertex/fragment entrypoints (210 archive-derived plus 2 template-provided)")
    print("NOTE: this does not replace Iris runtime loading, GPU-driver compilation, visual testing or FPS benchmarking")


if __name__ == "__main__":
    main()
