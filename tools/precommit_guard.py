"""Guard staged files against ROM data and unapproved oversized files.

Usage: python3 tools/precommit_guard.py
"""

import os
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROM_EXTENSIONS = {".z64", ".v64", ".n64", ".rom", ".bin"}
ROM_SIGNATURES = {bytes.fromhex(value) for value in ("80371240", "37804012", "40123780")}
MAX_UNAPPROVED_SIZE = 1_048_576
REFERENCE_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
GAMEPLAY_REFERENCE_EXTENSIONS = {".png", ".gif", ".mp4"}


def is_reference_media(filename: str) -> bool:
    normalized = filename.replace("\\", "/").lower()
    suffix = PurePosixPath(normalized).suffix
    if normalized.startswith("assets/physical-media/"):
        return suffix in REFERENCE_IMAGE_EXTENSIONS
    if normalized.startswith("docs/references/"):
        return suffix == ".pdf"
    if normalized.startswith("assets/gameplay/"):
        return suffix in GAMEPLAY_REFERENCE_EXTENSIONS
    return False


def main() -> int:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM", "-z"],
        check=True,
        stdout=subprocess.PIPE,
    )
    failures = 0

    for raw_name in result.stdout.split(b"\0"):
        if not raw_name:
            continue
        filename = os.fsdecode(raw_name)
        path = Path(filename)
        if not path.is_file():
            continue

        if path.suffix.lower() in ROM_EXTENSIONS:
            print(f"BLOCKED: ROM-like extension: {filename}", file=sys.stderr)
            failures += 1
            continue

        with path.open("rb") as stream:
            signature = stream.read(4)
        if signature in ROM_SIGNATURES:
            print(f"BLOCKED: N64 ROM signature found in: {filename}", file=sys.stderr)
            failures += 1
            continue

        if path.stat().st_size > MAX_UNAPPROVED_SIZE and not is_reference_media(filename):
            print(
                f"BLOCKED: file larger than 1 MiB outside approved reference paths: {filename}",
                file=sys.stderr,
            )
            failures += 1

    if failures:
        print(
            "Commit aborted: no ROM, game code, or ROM-extracted data may be committed.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
