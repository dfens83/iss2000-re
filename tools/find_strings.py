#!/usr/bin/env python3
"""
find_strings.py - Search for text and keywords inside an N64 ROM (z64 format).

Usage:
    # default career-mode keywords
    python3 tools/find_strings.py rom/baserom.z64

    # extra keywords (repeat -k as needed)
    python3 tools/find_strings.py rom/baserom.z64 -k "EURO" -k "LEAGUE"

    # only your own keywords
    python3 tools/find_strings.py rom/baserom.z64 --only-mine -k "EXHIBITION"

    # dump every readable string to a file (git-ignored)
    python3 tools/find_strings.py rom/baserom.z64 --dump notes/dumps/strings.txt

    # entropy map (helps locate compressed regions)
    python3 tools/find_strings.py rom/baserom.z64 --entropy

Searched encodings:
  * ASCII      menu text in English/European builds
  * Shift-JIS  Japanese text; the career mode "Success" is サクセス
  * Latin-1    accented European words (CARRIÈRE, etc.)

Note: if the game compresses its text, nothing will show up as plain text.
The entropy map then shows where compressed blocks live, and the
investigation moves to the emulator (see docs/phase1-guide.md).
"""

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

MAGIC_Z64 = bytes([0x80, 0x37, 0x12, 0x40])

DEFAULT_KEYWORDS = [
    # English
    "SUCCESS", "CAREER", "CAREER MODE", "SCENARIO", "WORLD LEAGUE",
    "INTERNATIONAL CUP", "EUROPEAN", "TRAINING", "DEBUG", "TEST",
    # other European languages
    "CARRIERE", "CARRIÈRE", "KARRIERE", "CARRIERA", "CARRERA", "CARREIRA",
    # Japanese (searched as Shift-JIS)
    "サクセス",       # Success
    "サクセスモード",   # Success Mode
    "育成",           # player development
    "選手",           # player
]


def strings_ascii(data: bytes, minimum: int):
    pattern = re.compile(rb"[\x20-\x7E]{%d,}" % minimum)
    for m in pattern.finditer(data):
        yield m.start(), m.group().decode("ascii")


def strings_sjis(data: bytes, min_chars: int):
    """Runs of 2-byte Shift-JIS characters (kana, kanji, full-width)."""
    i, n = 0, len(data)
    while i < n - 1:
        start = i
        chars = []
        while i < n - 1:
            b1 = data[i]
            if (0x81 <= b1 <= 0x9F) or (0xE0 <= b1 <= 0xEF):
                try:
                    chars.append(data[i:i + 2].decode("shift_jis"))
                    i += 2
                    continue
                except UnicodeDecodeError:
                    pass
            break
        if len(chars) >= min_chars:
            yield start, "".join(chars)
        i = max(i, start + 1)


def search_keywords(data: bytes, keywords):
    results = []
    upper = data.upper()  # only affects ASCII a-z bytes
    for kw in keywords:
        targets = set()
        if kw.isascii():
            targets.add(("ascii", kw.upper().encode("ascii")))
        else:
            try:
                targets.add(("latin-1", kw.upper().encode("latin-1")))
            except UnicodeEncodeError:
                pass
            try:
                targets.add(("shift-jis", kw.encode("shift_jis")))
            except UnicodeEncodeError:
                pass
        for enc, target in targets:
            haystack = data if enc == "shift-jis" else upper
            pos = haystack.find(target)
            while pos != -1:
                results.append((pos, kw, enc))
                pos = haystack.find(target, pos + 1)
    return sorted(set(results))


def context(data: bytes, pos: int, radius: int = 24) -> str:
    chunk = data[max(0, pos - radius):pos + radius]
    return "".join(chr(b) if 0x20 <= b < 0x7F else "." for b in chunk)


def entropy(block: bytes) -> float:
    if not block:
        return 0.0
    counts = Counter(block)
    total = len(block)
    return -sum(c / total * math.log2(c / total) for c in counts.values())


def main() -> int:
    ap = argparse.ArgumentParser(description="Search text and keywords in an N64 ROM.")
    ap.add_argument("rom", type=Path, help="ROM in z64 format (run rom_info.py --convert first)")
    ap.add_argument("-k", "--keyword", action="append", dest="keywords",
                    help="Additional keyword (repeatable)")
    ap.add_argument("--only-mine", action="store_true",
                    help="Use only the -k keywords, skip the default list")
    ap.add_argument("--min", type=int, default=5, help="Minimum ASCII string length (default 5)")
    ap.add_argument("--dump", type=Path, help="Write every string found to this file")
    ap.add_argument("--entropy", action="store_true", help="Print an entropy map per 64 KB block")
    args = ap.parse_args()

    if not args.rom.is_file():
        print(f"File not found: {args.rom}", file=sys.stderr)
        return 1
    data = args.rom.read_bytes()
    if data[:4] != MAGIC_Z64:
        print("ROM is not in z64 format. Run first:\n"
              "  python3 tools/rom_info.py YOUR_ROM --convert rom/baserom.z64", file=sys.stderr)
        return 2

    keywords = [] if args.only_mine else list(DEFAULT_KEYWORDS)
    keywords += args.keywords or []

    print(f"== Keywords ({len(keywords)}) ==")
    hits = search_keywords(data, keywords)
    if not hits:
        print("No plain-text matches (text may be compressed).")
    for pos, kw, enc in hits:
        print(f"0x{pos:08X}  {kw:<16} [{enc:<9}]  ...{context(data, pos)}...")

    if args.dump:
        args.dump.parent.mkdir(parents=True, exist_ok=True)
        with args.dump.open("w", encoding="utf-8") as f:
            f.write("# offset\tencoding\ttext\n")
            for pos, s in strings_ascii(data, args.min):
                f.write(f"0x{pos:08X}\tascii\t{s}\n")
            for pos, s in strings_sjis(data, 3):
                f.write(f"0x{pos:08X}\tsjis\t{s}\n")
        print(f"\nAll strings written to: {args.dump}")

    if args.entropy:
        print("\n== Entropy per 64 KB block (0-8 bits/byte) ==")
        print("   >7.5 = likely compressed | <1 = empty/padding")
        size = 0x10000
        for start in range(0, len(data), size):
            e = entropy(data[start:start + size])
            flag = "  <- compressed?" if e > 7.5 else ""
            print(f"0x{start:08X}  {e:4.2f}  {'#' * int(e * 5)}{flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
