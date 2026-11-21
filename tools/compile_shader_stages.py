#!/usr/bin/env python3
"""Compile every Lightning .fsh/.vsh entrypoint with glslangValidator.

This is an offline GLSL syntax/semantic smoke test, not an Iris runtime test.
Iris shaderpack-root includes are expanded in memory for the compiler only.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHADERS = ROOT / "shaders"
INCLUDE = re.compile(r'^\s*#\s*include\s+"([^"]+)"')


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def expand_includes(path: Path, stack: tuple[Path, ...] = ()) -> str:
    resolved = path.resolve()
    if resolved in stack:
        chain = " -> ".join(p.relative_to(SHADERS).as_posix() for p in (*stack, resolved))
        fail(f"circular shader include: {chain}")
    if not resolved.is_file():
        fail(f"shader include does not exist: {resolved}")

    output: list[str] = []
    for line_number, line in enumerate(resolved.read_text(encoding="utf-8").splitlines(), 1):
        match = INCLUDE.match(line)
        if not match:
            output.append(line)
            continue

        include_name = match.group(1)
        if include_name.startswith("/"):
            target = SHADERS / include_name.lstrip("/")
        else:
            target = resolved.parent / include_name
        if not target.is_file():
            fail(f"{resolved.relative_to(SHADERS)}:{line_number}: unresolved include {include_name}")

        output.append(f"// BEGIN INCLUDE {target.relative_to(SHADERS).as_posix()}")
        output.append(expand_includes(target, (*stack, resolved)))
        output.append(f"// END INCLUDE {target.relative_to(SHADERS).as_posix()}")
    return "\n".join(output) + "\n"


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
        for source in stages:
            relative = source.relative_to(SHADERS)
            stage = "vert" if source.suffix == ".vsh" else "frag"
            expanded = expand_includes(source)
            if relative.name.startswith("dh_"):
                # Iris injects these symbols for Distant Horizons programs.
                # The compile-only preamble mirrors the interface documented
                # by Iris; it is not written into the distributable shaders.
                injected = ["#define DISTANT_HORIZONS 1", "#define TRANSITION_DH_INF 0.0"]
                if stage == "vert":
                    injected.append("in int dhMaterialId;")
                lines = expanded.splitlines()
                if not lines or not lines[0].startswith("#version"):
                    fail(f"{relative.as_posix()}: missing leading #version")
                expanded = "\n".join([lines[0], *injected, *lines[1:]]) + "\n"

            temporary_entry = temp_root / relative
            temporary_entry.parent.mkdir(parents=True, exist_ok=True)
            temporary_entry.write_text(expanded, encoding="utf-8")

            command = [compiler, "-S", stage, str(temporary_entry)]
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
