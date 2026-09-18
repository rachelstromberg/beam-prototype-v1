#!/usr/bin/env python3
"""Verify frozen snapshot checksums and compare released versions to their tags."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VERSIONS = ROOT / "versions"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )


def main() -> None:
    if not VERSIONS.exists():
        raise SystemExit("No frozen versions found.")

    failures: list[str] = []
    checked = 0
    for version_dir in sorted(path for path in VERSIONS.iterdir() if path.is_dir()):
        manifest_path = version_dir / "SHA256SUMS"
        metadata_path = version_dir / "VERSION.json"
        if not manifest_path.exists() or not metadata_path.exists():
            failures.append(f"{version_dir.name}: missing VERSION.json or SHA256SUMS")
            continue

        expected: dict[str, str] = {}
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            checksum, relative_path = line.split("  ", 1)
            expected[relative_path] = checksum

        actual_paths = {
            path.relative_to(version_dir).as_posix(): path
            for path in version_dir.rglob("*")
            if path.is_file()
            and path.name != "SHA256SUMS"
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        }
        if set(expected) != set(actual_paths):
            failures.append(f"{version_dir.name}: manifest file list differs from snapshot")
        for relative_path, path in actual_paths.items():
            if expected.get(relative_path) != sha256(path):
                failures.append(f"{version_dir.name}: checksum mismatch for {relative_path}")

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        tag = metadata["immutableTag"]
        if git("rev-parse", "--verify", "--quiet", f"refs/tags/{tag}").returncode == 0:
            comparison = git("diff", "--quiet", tag, "--", version_dir.relative_to(ROOT).as_posix())
            if comparison.returncode != 0:
                failures.append(f"{version_dir.name}: differs from released tag {tag}")
        checked += 1

    if failures:
        raise SystemExit("Frozen version verification failed:\n- " + "\n- ".join(failures))
    print(f"Verified {checked} frozen version(s).")


if __name__ == "__main__":
    main()
