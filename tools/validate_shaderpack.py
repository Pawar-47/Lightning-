#!/usr/bin/env python3
"""Static structure validator for Lightning. This does not compile GLSL."""
from pathlib import Path
import csv
import json
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



language_files = [
    "en_US.lang", "es_AR.lang", "es_ES.lang", "es_MX.lang",
    "ko_KR.lang", "ru_RU.lang", "sv_SE.lang", "tr_TR.lang", "zh_CN.lang",
]
for name in language_files:
    if not (SHADERS / "lang" / name).is_file():
        fail(f"reference shader language file missing: shaders/lang/{name}")

texture_files = [
    "clouds_blocky_512_R_8bit.png",
    "clouds_blocky_512_R_8bit.png.mcmeta",
    "clouds_natural_512_R_8bit.png",
    "clouds_natural_512_R_8bit.png.mcmeta",
    "water_256_RG_8bit.png",
    "water_256_RG_8bit.png.mcmeta",
]
for name in texture_files:
    path = SHADERS / "textures" / name
    if not path.is_file():
        fail(f"reference texture/animation metadata missing: shaders/textures/{name}")
    if name.endswith(".png") and path.read_bytes()[:8] != bytes.fromhex("89504e470d0a1a0a"):
        fail(f"invalid PNG signature: shaders/textures/{name}")
    if name.endswith(".mcmeta"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            fail(f"invalid animation metadata {name}: {error}")

config_text = (SHADERS / "lib/config.glsl").read_text(encoding="utf-8", errors="replace")
properties_text = (ROOT / "shaders.properties").read_text(encoding="utf-8", errors="replace")
required_defines = [
    r"^\s*#\s*define\s+DOF\b",
    r"^\s*#\s*define\s+MOTION_BLUR\b",
    r"^\s*#\s*define\s+COLORED_SHADOW\b",
    r"^\s*#\s*define\s+CLOUD_REFLECTION\b",
    r"^\s*#\s*define\s+END_CLOUDS\b",
    r"^\s*#\s*define\s+BLOOM\b",
    r"^\s*#\s*define\s+MATERIAL_GLOSS\b",
    r"^\s*#\s*define\s+SHADOW_CASTING\b",
]
for pattern in required_defines:
    if not re.search(pattern, config_text, re.MULTILINE):
        fail(f"feature define is not enabled: {pattern}")
for option in ["profile.Performance=", "profile.Quality=", "screen.ADVANCED_SCREEN", "program.shadow.enabled=SHADOW_CASTING"]:
    if option not in properties_text:
        fail(f"shader options/profile configuration missing: {option}")

def numeric_define(name: str):
    match = re.search(rf"^\s*#\s*define\s+{re.escape(name)}\s+(\d+(?:\.\d+)?)", config_text, re.MULTILINE)
    return float(match.group(1)) if match else None

budgets = {"AOSTEPS": 4, "RAYMARCH_STEPS": 5, "CLOUD_STEPS_AVG": 7, "GODRAY_STEPS": 4, "MOTION_BLUR_SAMPLES": 3, "BLOOM_SAMPLES": 2}
for name, maximum in budgets.items():
    value = numeric_define(name)
    if value is None or value > maximum:
        fail(f"{name} budget is missing or exceeds the Performance target ({value} > {maximum})")

map_path = ROOT / "reference/source-file-map.csv"
if map_path.is_file():
    with map_path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 348:
        fail(f"source-file ledger should contain 348 rows, found {len(rows)}")
    paths = [row.get("source_path", "") for row in rows]
    if len(set(paths)) != len(paths) or any(not p for p in paths):
        fail("source-file ledger contains blank or duplicate source paths")
else:
    fail("reference/source-file-map.csv is missing")

print(f"PASS: {len(shader_files)} shader source files inspected")
print("PASS: all #include targets resolve")
print("PASS: all .fsh/.vsh entrypoints declare GLSL 330")
print("PASS: required feature modules are present")
print("NOTE: static checks only; GLSL compilation, Iris loading, visual parity and FPS are not tested")
