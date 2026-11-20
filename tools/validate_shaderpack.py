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
for option in ["profile.Performance=", "profile.Quality=", "screen.ADVANCED_SCREEN", "program.shadow.enabled=SHADOW_CASTING", "program.composite1.enabled=BLOOM || DOF", "program.composite2.enabled=AA_TYPE || MOTION_BLUR"]:
    if option not in properties_text:
        fail(f"shader options/profile configuration missing: {option}")

performance_profile = next((line for line in properties_text.splitlines() if line.startswith("profile.Performance=")), "")
quality_profile = next((line for line in properties_text.splitlines() if line.startswith("profile.Quality=")), "")
if "VOL_LIGHT=1" not in performance_profile:
    fail("Performance profile must retain the cheaper depth-based godray path (VOL_LIGHT=1)")
if "VOL_LIGHT=2" not in quality_profile:
    fail("Quality profile must retain the full shadow-aware volumetric-light path (VOL_LIGHT=2)")

# Guard the user-required feature set in the actual low-cost profile, not just
# in config.glsl. Exact whitespace tokens avoid accidental substring matches.
required_performance_tokens = [
    "SHADOW_CASTING", "COLORED_SHADOW", "DOF", "MOTION_BLUR",
    "CLOUD_REFLECTION", "END_CLOUDS", "BLOOM", "MATERIAL_GLOSS",
    "REFLECTION_SLIDER=2", "REFRACTION=1", "SUN_REFLECTION=1",
    "AO=1", "AA_TYPE=2", "V_CLOUDS=1", "VOL_LIGHT=1",
]
performance_tokens = set(performance_profile.split())
for token in required_performance_tokens:
    if token not in performance_tokens:
        fail(f"Performance profile has dropped a required rendering feature: {token}")
    if "!" + token in performance_tokens:
        fail(f"Performance profile explicitly disables a required rendering feature: {token}")
for token in ["AOSTEPS=4", "CLOUD_STEPS_AVG=7", "MOTION_BLUR_SAMPLES=3", "BLOOM_SAMPLES=2.0"]:
    if token not in performance_profile:
        fail(f"Performance profile is missing its bounded feature budget: {token}")

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
    verified_rows = [row for row in rows if row.get("zip_comparison") == "ZIP_GIT_BLOB_HASH_MATCH"]
    if len(verified_rows) != 346:
        fail(f"expected 346 verified source-to-port rows, found {len(verified_rows)}")
    exceptions = {row.get("source_path"): row for row in rows if row.get("source_path") in {
        "shaders/lib/config.glsl", "shaders/shaders.properties"
    }}
    if set(exceptions) != {"shaders/lib/config.glsl", "shaders/shaders.properties"}:
        fail("the two documented uploaded-archive exceptions are missing from the ledger")
else:
    fail("reference/source-file-map.csv is missing")

exception_hashes = {
    "shaders/lib/config.glsl": "7c8f086dfa749f2c61707782786897620a3564d5",
    "shaders/shaders.properties": "712ebede6b2ad78a92ee6cb39bf1f5fb07bdfdb1",
}
for path, expected_hash in exception_hashes.items():
    row = next((item for item in rows if item.get("source_path") == path), None)
    if row is None or row.get("uploaded_archive_git_blob_sha1") != expected_hash:
        fail(f"uploaded archive source hash is missing or incorrect in the ledger: {path}")
    active_path = ROOT / path if path != "shaders/shaders.properties" else ROOT / "shaders.properties"
    if not active_path.is_file():
        fail(f"active tuned/merged exception file is missing: {path}")


print(f"PASS: {len(shader_files)} shader source files inspected")
print("PASS: all #include targets resolve")
print("PASS: all .fsh/.vsh entrypoints declare GLSL 330")
print("PASS: required feature modules are present")
print("NOTE: static checks only; GLSL compilation, Iris loading, visual parity and FPS are not tested")
