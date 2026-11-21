#!/usr/bin/env python3
"""Boot the Fabric/Iris development client under Mesa software rendering.

This checks client startup and the configured shader-pack selection. It does
not enter a world, prove every Iris program links, or replace target-GPU tests.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "run"
LOG_PATH = ROOT / "build" / "iris-smoke.log"
CONFIG_PATH = RUN_DIR / "config" / "iris.properties"
GAME_LOG = RUN_DIR / "logs" / "latest.log"


def fail(message: str, output: str = "") -> None:
    if output:
        print(output[-16000:], file=sys.stderr)
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not shutil.which("xvfb-run") or not shutil.which("timeout"):
        fail("xvfb-run and timeout are required (install xvfb)")

    env = os.environ.copy()
    env["LIBGL_ALWAYS_SOFTWARE"] = "1"
    env["MESA_GL_VERSION_OVERRIDE"] = "4.5COMPAT"
    env["MESA_GLSL_VERSION_OVERRIDE"] = "450"

    command = [
        "xvfb-run", "-a", "timeout", "--signal=TERM", "--kill-after=10s", "150s",
        "./gradlew", "--no-daemon", "runShaderClient",
    ]
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        fail("Iris development client exceeded the 180-second smoke-test limit", exc.stdout or "")

    build_dir = ROOT / "build"
    build_dir.mkdir(exist_ok=True)
    game_log = GAME_LOG.read_text(encoding="utf-8", errors="replace") if GAME_LOG.is_file() else ""
    output = result.stdout or ""
    LOG_PATH.write_text(
        "=== Gradle/client output ===\n" + output + "\n=== Minecraft latest.log ===\n" + game_log,
        encoding="utf-8",
    )

    if result.returncode not in (0, 124):
        fail(f"development client exited unexpectedly with code {result.returncode}", output + "\n" + game_log)
    if not CONFIG_PATH.is_file():
        fail("Iris development configuration was not generated", output + "\n" + game_log)

    config = CONFIG_PATH.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"(?m)^shaderPack=Lightning-dev\s*$", config):
        fail("Iris is not configured to select Lightning-dev", config)

    combined = output + "\n" + game_log
    if not re.search(r"\bIris\b", combined, re.IGNORECASE):
        fail("Iris did not appear in the client startup logs", combined)
    if re.search(
        r"failed to load shader.?pack|failed to compile shader|shader.?pack.{0,40}(error|failed)",
        combined,
        re.IGNORECASE,
    ):
        fail("Iris reported a shader-pack loading or compilation error", combined)

    print("PASS: Fabric development client started with Iris present and Lightning-dev selected.")
    print("NOTE: this smoke test does not enter a world or verify in-world rendering, visual output or FPS.")


if __name__ == "__main__":
    main()
