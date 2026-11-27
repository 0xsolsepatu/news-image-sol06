#!/usr/bin/env python3
"""news-image-20261127 v2 — entry-point runner.

Copies the built front page (entry.png, next to this file) into the
harness output directory and refuses to emit anything that is not a
complete, in-limit PNG. Standard library only; no network, no fonts,
no image decoding — the file is treated as opaque bytes and verified
by its header, its trailer and its size.

Usage: python3 main.py
  Reads  MAKEFUN_OUTPUT_DIR (default /output) and writes entry.png there.
  Exits 0 on a byte-identical copy, 1 on any failed check.
"""

import hashlib
import os
import sys

# The image gate for this competition: PNG or JPEG, at most 1 MiB.
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(reason):
    print(f"main.py: FAIL: {reason}", file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return fail(f"cannot read {src}: {exc}")

    if len(data) > MAX_BYTES:
        return fail(f"entry.png is {len(data)} bytes, over the "
                    f"{MAX_BYTES}-byte limit")
    if not data.startswith(PNG_MAGIC):
        return fail("entry.png does not start with the PNG magic bytes")
    # The IEND chunk is exactly 12 bytes: length 0, "IEND", CRC ae 42 60 82.
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return fail("entry.png does not end with the exact IEND chunk")

    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(data)
        with open(dst, "rb") as fh:
            written = fh.read()
    except OSError as exc:
        return fail(f"cannot write {dst}: {exc}")

    if written != data:
        return fail("written copy differs from entry.png")

    digest = hashlib.sha256(data).hexdigest()
    print(f"main.py: wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
