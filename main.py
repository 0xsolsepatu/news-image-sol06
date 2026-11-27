#!/usr/bin/env python3
"""Entrypoint for news-image-20261127: copies the rendered front page to
the grader's output path. Standard library only, no network, deterministic:
the same bytes are written on every run.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")
MAX_BYTES = 1048576

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IEND = b"IEND"


def main():
    with open(SRC, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_MAGIC):
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if IEND not in data[-16:]:
        print("entry.png has no IEND trailer", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "wb") as fh:
        fh.write(data)
    # Verify the copy byte for byte before reporting success.
    with open(OUT, "rb") as fh:
        copied = fh.read()
    if copied != data:
        print("copy mismatch: output differs from entry.png",
              file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {OUT} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
