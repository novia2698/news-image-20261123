#!/usr/bin/env python3
"""news-image-20261123 entrypoint.

Copies the pre-rendered front page (entry.png, built at build time from
real 23 November 2026 world news) into the grader's output directory.

Stdlib only, on purpose: the grading image (python:3.13) has no Pillow,
so this program must never import it. The picture is rendered once by
render_news.py on the builder machine and committed as entry.png; this
file only moves bytes.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    # Optional format check, stdlib only: the file must start with the
    # PNG magic bytes. No Pillow, no optional import, so this can never
    # fail for a missing imaging library.
    with open(dest, "rb") as f:
        magic = f.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("error: output is not a PNG file", file=sys.stderr)
        return 1
    size = os.path.getsize(dest)
    try:
        with open(dest, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
    except OSError:
        digest = "unavailable"
    print(f"wrote {dest} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
