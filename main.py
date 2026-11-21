#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR with verification.

Stdlib only: no Pillow, no system fonts. The grader image has neither.
Locates entry.png via MAKEFUN_BOT_DIR when set, else next to this file.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "3bb7170848647bb7140541cd4293e80f38369b3a522d20b6e939b48f736b966c"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        src = os.path.join(bot_dir, "entry.png")
    else:
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

    if not os.path.isfile(src):
        return fail("entry.png not found: " + src)

    with open(src, "rb") as handle:
        head = handle.read(8)
    if head != PNG_SIGNATURE:
        return fail("entry.png is not a PNG file: " + src)

    digest = hashlib.sha256()
    with open(src, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    if digest.hexdigest() != EXPECTED_SHA256:
        return fail("entry.png sha256 mismatch")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)

    out_size = os.path.getsize(dst)
    if out_size <= 0:
        return fail("output entry.png is empty: " + dst)

    out_digest = hashlib.sha256()
    with open(dst, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            out_digest.update(chunk)
    if out_digest.hexdigest() != EXPECTED_SHA256:
        return fail("output entry.png sha256 mismatch")
    if out_size != os.path.getsize(src):
        return fail("output entry.png size mismatch")

    print(
        "wrote %s (%d bytes, sha256 %s)"
        % (dst, out_size, out_digest.hexdigest()[:16])
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
