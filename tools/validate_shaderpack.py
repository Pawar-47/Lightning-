#!/usr/bin/env python3
"""Static structure validator for Lightning. This does not compile GLSL."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SHADERS = ROOT / "shaders"
INCLUDE = re.compile(r'^\s*#\s*include\s+"([^"]+)"', re.MULTILINE)
VERSION = re.compile(r'^\s*#\s*version\s+(\d+)(?:\s+(\w+))?', re.MULTILINE)

def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)

if not SHADERS.is_dir():
    fail("shaders/ directory is missing")

shader_files = sorted(p for p in SHADERS.rglob("*") if p.is_file() and p.suffix in {".fsh", ".vsh", ".glsl"})
if not shader_files:
    fail("no shader source files found")

missing = []
versions = []
for path in shader_files:
    text = path.read_text(encoding="utf-8", errors="replace")
    for target in INCLUDE.findall(text):
        candidate = (SHADERS / target.lstrip("/")) if target.startswith("/") else (path.parent / target)
        if not candidate.is_file():
            missing.append((path.relative_to(ROOT).as_posix(), target))
    if path.suffix in {".fsh", ".vsh"}:
        match = VERSION.search(text)
        if not match:
            versions.append((path.relative_to(ROOT).as_posix(), "missing #version"))
        elif match.group(1) != "330":
            versions.append((path.relative_to(ROOT).as_posix(), f"GLSL {match.group(1)}"))
if missing:
    for source, target in missing:
        print(f"MISSING INCLUDE: {source} -> {target}")
    fail(f"{len(missing)} unresolved include(s)")
if versions:
    for source, issue in versions:
        print(f"VERSION ISSUE: {source}: {issue}")
    fail(f"{len(versions)} shader stage(s) do not declare GLSL 330")

required = [
    "lib/config.glsl", "lib/water.glsl", "lib/ao.glsl",
    "lib/volumetric_clouds.glsl", "lib/bloom.glsl",
    "lib/fast_taa.glsl", "lib/fxaa.glsl", "lib/motion_blur.glsl",
    "lib/volumetric_light.glsl", "lib/shadow_frag.glsl",
    "lib/material_gloss_fragment.glsl",
    "common/solid_blocks_fragment.glsl", "common/deferred_fragment.glsl",
    "common/composite_fragment.glsl",
]
for relative in required:
    if not (SHADERS / relative).is_file():
        fail(f"required feature source missing: shaders/{relative}")

print(f"PASS: {len(shader_files)} shader source files inspected")
print("PASS: all #include targets resolve")
print("PASS: all .fsh/.vsh entrypoints declare GLSL 330")
print("PASS: required feature modules are present")
print("NOTE: static checks only; GLSL compilation, Iris loading, visual parity and FPS are not tested")
