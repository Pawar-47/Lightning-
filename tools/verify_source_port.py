#!/usr/bin/env python3
"""Reproduce the uploaded Shader.zip -> Lightning source-port comparison.

Run from a Lightning checkout:
    python tools/verify_source_port.py /path/to/Shader.zip
The full archive is deliberately not part of the distributable shaderpack.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reference/source-file-map.csv"
EXCEPTION_HASHES = {
    "shaders/lib/config.glsl": "7c8f086dfa749f2c61707782786897620a3564d5",
    "shaders/shaders.properties": "712ebede6b2ad78a92ee6cb39bf1f5fb07bdfdb1",
}
EXPECTED_AGGREGATES = {
    "docs": "883f28d4020f987f169bf2b437f8c5b5c3049814",
    "reference": "a4e3f6b1604919363344cb18c318d849dce157d0",
    "shaders": "996a5b107aed0631922cef032186567acc9dced7",
    "shaders/common": "3bba39394ee1cd1435b3bd608b80945902f160b0",
    "shaders/lang": "4a11948f1234304693f5c439b051de7522e54762",
    "shaders/lib": "6f8c1f1830c77721e9ae7ed5a07ed66ef6a194f4",
    "shaders/src": "8cd0591c09888f627db47f5a0f47d1995deb6c27",
    "shaders/textures": "6fb4e2c8db743a8888e08b0a80e0b2aa63f76d19",
    "shaders/world-1": "fefad057c8a689bbde69adab937dbef40d992ea4",
    "shaders/world0": "38bd1d3bba10b060c855b7a9953595abd8fe22d3",
    "shaders/world1": "a431a544435b6c705a5012b9593577f66d90edc3",
}
VERSION_DIRECTIVE = re.compile(rb"(?m)^#version[ \t]+120")


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + bytes([0])
    return hashlib.sha1(header + data).hexdigest()


def group_for(destination: str) -> str:
    parts = destination.split("/")
    if destination.startswith("shaders/"):
        return "/".join(parts[:2]) if len(parts) > 2 else "shaders"
    return parts[0]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="path to the original uploaded Shader.zip")
    args = parser.parse_args()

    if not args.archive.is_file():
        fail(f"archive does not exist: {args.archive}")
    if not LEDGER.is_file():
        fail(f"source ledger is missing: {LEDGER}")

    with LEDGER.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 348:
        fail(f"expected 348 ledger rows, found {len(rows)}")

    try:
        with zipfile.ZipFile(args.archive) as archive:
            archive_files = {
                name: archive.read(name)
                for name in archive.namelist()
                if not name.endswith("/") and not name.startswith("__MACOSX/")
            }
    except (OSError, zipfile.BadZipFile) as error:
        fail(f"cannot read source ZIP: {error}")

    ledger_paths = {row["source_path"] for row in rows}
    archive_paths = set(archive_files)
    if ledger_paths != archive_paths:
        missing = sorted(ledger_paths - archive_paths)
        extra = sorted(archive_paths - ledger_paths)
        fail(f"archive/ledger path mismatch; missing={missing[:8]}, extra={extra[:8]}")

    grouped: dict[str, list[tuple[str, str]]] = {}
    unchanged = 0
    version_ported = 0
    exceptions = 0
    failures = []

    for row in rows:
        source_path = row["source_path"]
        destination = row["planned_destination"]
        source_bytes = archive_files[source_path]

        if len(source_bytes) != int(row["source_bytes"]):
            failures.append(f"{source_path}: source byte count differs from ledger")
            continue

        source_blob = git_blob_sha(source_bytes)
        if source_path in EXCEPTION_HASHES:
            expected = EXCEPTION_HASHES[source_path]
            if source_blob != expected or row.get("uploaded_archive_git_blob_sha1") != expected:
                failures.append(f"{source_path}: uploaded source Git blob hash mismatch")
                continue
            active_path = ROOT / destination
            if source_path == "shaders/shaders.properties":
                active_path = ROOT / "shaders.properties"
            if not active_path.is_file():
                failures.append(f"{source_path}: active customized destination is missing")
                continue
            exceptions += 1
            continue

        expected_bytes = source_bytes
        is_stage = source_path.endswith((".fsh", ".vsh"))
        if is_stage:
            matches = list(VERSION_DIRECTIVE.finditer(source_bytes))
            if len(matches) != 1:
                failures.append(f"{source_path}: expected exactly one #version 120 directive, found {len(matches)}")
                continue
            expected_bytes = VERSION_DIRECTIVE.sub(b"#version 330 compatibility", source_bytes, count=1)

        active_path = ROOT / destination
        if not active_path.is_file():
            failures.append(f"{source_path}: destination missing ({destination})")
            continue
        actual_bytes = active_path.read_bytes()
        if actual_bytes != expected_bytes:
            failures.append(f"{source_path}: destination differs from expected source port")
            continue

        unchanged += not is_stage
        version_ported += is_stage
        destination_blob = git_blob_sha(expected_bytes)
        grouped.setdefault(group_for(destination), []).append((destination, destination_blob))

    if failures:
        for failure in failures:
            print(f"DIFF: {failure}")
        fail(f"{len(failures)} source-port comparison failure(s)")

    if unchanged != 136 or version_ported != 210 or exceptions != 2:
        fail(f"unexpected disposition counts: unchanged={unchanged}, version_ported={version_ported}, exceptions={exceptions}")

    for group, expected_hash in EXPECTED_AGGREGATES.items():
        pairs = sorted(grouped.get(group, []), key=lambda item: item[0])
        aggregate_input = "".join(path + chr(0) + blob + chr(10) for path, blob in pairs).encode("utf-8")
        actual_hash = hashlib.sha1(aggregate_input).hexdigest()
        if actual_hash != expected_hash:
            fail(f"{group}: aggregate mismatch ({actual_hash} != {expected_hash})")
        print(f"PASS: {group}: {len(pairs)} files, {actual_hash}")

    if set(grouped) != set(EXPECTED_AGGREGATES):
        fail(f"unexpected source groups: {sorted(set(grouped) ^ set(EXPECTED_AGGREGATES))}")

    print(f"PASS: {unchanged} byte-identical files; {version_ported} GLSL 330 version-only ports; {exceptions} documented exceptions")
    print("NOTE: this validates source-to-port bytes, not GLSL compilation, Iris runtime, visual parity or FPS.")


if __name__ == "__main__":
    main()
