#!/usr/bin/env python3
"""
rom_info.py - Identify a Nintendo 64 ROM and normalize it to .z64 (big-endian).

Usage:
    python3 tools/rom_info.py rom/original.n64
    python3 tools/rom_info.py rom/original.v64 --convert rom/baserom.z64

What it does:
  * Detects byte order from the first 4 bytes
    (z64 = native big-endian, v64 = byte-swapped, n64 = little-endian).
  * Parses the header: internal title, game code, region, revision,
    entry point, CRC1/CRC2.
  * Computes SHA-1 and MD5 of the normalized z64 image, the format used
    by every decompilation tool (splat, Ghidra loaders).
  * Optionally writes the converted z64 file.

No ROM data ever leaves your machine.
"""

import argparse
import hashlib
import struct
import sys
from pathlib import Path

MAGIC_Z64 = bytes([0x80, 0x37, 0x12, 0x40])
MAGIC_V64 = bytes([0x37, 0x80, 0x40, 0x12])
MAGIC_N64 = bytes([0x40, 0x12, 0x37, 0x80])

# Destination code (header byte 0x3E)
REGIONS = {
    "A": "All regions",
    "B": "Brazil",
    "C": "China",
    "D": "Germany",
    "E": "North America (NTSC-U)",
    "F": "France",
    "G": "Gateway 64 (NTSC)",
    "H": "Netherlands",
    "I": "Italy",
    "J": "Japan",
    "K": "Korea",
    "L": "Gateway 64 (PAL)",
    "N": "Canada",
    "P": "Europe (PAL)",
    "S": "Spain",
    "U": "Australia",
    "W": "Scandinavia",
    "X": "Europe (PAL, alternate)",
    "Y": "Europe (PAL, alternate)",
    "Z": "Europe (PAL, alternate)",
}


def detect_format(data: bytes) -> str:
    head = data[:4]
    if head == MAGIC_Z64:
        return "z64"
    if head == MAGIC_V64:
        return "v64"
    if head == MAGIC_N64:
        return "n64"
    return "unknown"


def to_z64(data: bytes, fmt: str) -> bytes:
    """Convert any supported byte order to big-endian (z64)."""
    if fmt == "z64":
        return data
    if len(data) % 4:
        print("Warning: size is not a multiple of 4 bytes; the dump may be "
              "corrupt. Trailing bytes were kept unconverted.", file=sys.stderr)
    usable = len(data) - len(data) % 4
    arr = bytearray(data[:usable])
    if fmt == "v64":
        # swap each byte pair: AB CD -> BA DC
        arr[0::2], arr[1::2] = arr[1::2], arr[0::2]
    elif fmt == "n64":
        # reverse each 32-bit word: ABCD -> DCBA
        for i in range(0, usable, 4):
            arr[i:i + 4] = arr[i:i + 4][::-1]
    else:
        raise ValueError("Unknown format; cannot convert.")
    return bytes(arr) + data[usable:]


def read_header(z64: bytes) -> dict:
    entry, = struct.unpack(">I", z64[0x08:0x0C])
    crc1, crc2 = struct.unpack(">II", z64[0x10:0x18])
    title = z64[0x20:0x34].decode("ascii", errors="replace").rstrip(" \x00")
    category = chr(z64[0x3B]) if 32 <= z64[0x3B] < 127 else "?"
    game_id = z64[0x3C:0x3E].decode("ascii", errors="replace")
    region = chr(z64[0x3E]) if 32 <= z64[0x3E] < 127 else "?"
    return {
        "title": title,
        "code": f"{category}{game_id}{region}",
        "game_id": game_id,
        "region": region,
        "region_name": REGIONS.get(region, "unknown"),
        "revision": z64[0x3F],
        "entry_point": entry,
        "crc1": crc1,
        "crc2": crc2,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Identify and normalize an N64 ROM.")
    ap.add_argument("rom", type=Path, help="Path to the ROM (.z64, .v64 or .n64)")
    ap.add_argument("--convert", type=Path, metavar="OUT",
                    help="Write the ROM converted to z64 to this path")
    args = ap.parse_args()

    if not args.rom.is_file():
        print(f"File not found: {args.rom}", file=sys.stderr)
        return 1

    data = args.rom.read_bytes()
    fmt = detect_format(data)
    if fmt == "unknown":
        print("Not an N64 ROM (unrecognized magic bytes).", file=sys.stderr)
        return 2

    z64 = to_z64(data, fmt)
    h = read_header(z64)

    print(f"File           : {args.rom}")
    print(f"Size           : {len(data):,} bytes ({len(data) * 8 // (1024 * 1024)} Mbit)")
    print(f"Format         : {fmt}" + ("" if fmt == "z64" else "  (normalized to z64)"))
    print(f"Internal title : {h['title']}")
    print(f"Game code      : {h['code']}  (id '{h['game_id']}', revision 1.{h['revision']})")
    print(f"Region         : {h['region']} = {h['region_name']}")
    print(f"Entry point    : 0x{h['entry_point']:08X}")
    print(f"CRC1 / CRC2    : 0x{h['crc1']:08X} / 0x{h['crc2']:08X}")
    print(f"SHA-1 (z64)    : {hashlib.sha1(z64).hexdigest()}")
    print(f"MD5   (z64)    : {hashlib.md5(z64).hexdigest()}")

    if args.convert:
        args.convert.parent.mkdir(parents=True, exist_ok=True)
        args.convert.write_bytes(z64)
        print(f"\nConverted ROM written to: {args.convert}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
