#!/usr/bin/env python3
"""Boot the Fabric/Iris development client under Mesa software rendering.

Stop once Iris has created an OpenGL context. This checks client startup and
the configured shader-pack selection; it does not enter a world or prove
in-world shaderpack compilation, visual output or FPS.
"""
from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "run"
BUILD_DIR = ROOT / "build"
LOG_PATH = BUILD_DIR / "iris-smoke.log"
STDOUT_PATH = BUILD_DIR / "iris-client.stdout.log"
CONFIG_PATH = RUN_DIR / "config" / "iris.properties"
GAME_LOG = RUN_DIR / "logs" / "latest.log"


def read_game_log() -> str:
    return GAME_LOG.read_text(encoding="utf-8", errors="replace") if GAME_LOG.is_file() else ""


def stop_process_group(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=10)


def fail(message: str, output: str = "") -> None:
    if output:
        print(output[-16000:], file=sys.stderr)
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not shutil.which("xvfb-run"):
        fail("xvfb-run is required (install xvfb)")

    BUILD_DIR.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["LIBGL_ALWAYS_SOFTWARE"] = "1"
    env["MESA_GL_VERSION_OVERRIDE"] = "4.5COMPAT"
    env["MESA_GLSL_VERSION_OVERRIDE"] = "450"

    command = ["xvfb-run", "-a", "./gradlew", "--no-daemon", "runShaderClient"]
    deadline = time.monotonic() + 180
    ready = False

    with STDOUT_PATH.open("w", encoding="utf-8") as stdout_file:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=env,
            stdout=stdout_file,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
        )
        while time.monotonic() < deadline:
            game_log = read_game_log()
            if "OpenGL debug context activated" in game_log and re.search(r"\bIris\b", game_log):
                ready = True
                break
            if process.poll() is not None:
                break
            time.sleep(2)

        stop_process_group(process)

    output = STDOUT_PATH.read_text(encoding="utf-8", errors="replace")
    game_log = read_game_log()
    LOG_PATH.write_text(
        "=== Gradle/client output ===\n" + output + "\n=== Minecraft latest.log ===\n" + game_log,
        encoding="utf-8",
    )

    if not ready:
        fail("Iris did not reach an active OpenGL debug context within 180 seconds", output + "\n" + game_log)
    if not CONFIG_PATH.is_file():
        fail("Iris development configuration was not generated", output + "\n" + game_log)

    config = CONFIG_PATH.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"(?m)^shaderPack=Lightning-dev\s*$", config):
        fail("Iris is not configured to select Lightning-dev", config)

    combined = output + "\n" + game_log
    if re.search(
        r"failed to load shader.?pack|failed to compile shader|shader.?pack.{0,40}(error|failed)",
        combined,
        re.IGNORECASE,
    ):
        fail("Iris reported a shader-pack loading or compilation error during startup", combined)

    print("PASS: Fabric development client started, Iris created an OpenGL context, and Lightning-dev is configured.")
    print("NOTE: this smoke test does not enter a world or verify in-world shaderpack compilation, visuals or FPS.")


if __name__ == "__main__":
    main()
