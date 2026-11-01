---
description: Identify and normalize the ROM, then fill notes/rom-identification.md
argument-hint: [path to ROM, default rom/baserom.z64]
---

Identify the owner's ROM.

1. ROM path: `$ARGUMENTS` (if empty, use the only file in `rom/` other than
   `README.md`; if there are several, ask which one).
2. Run `python3 tools/rom_info.py <path> --convert rom/baserom.z64`
   (skip `--convert` if the path already is `rom/baserom.z64`).
3. Never Read the ROM file itself.
4. Fill `notes/rom-identification.md` with the output.
5. Interpret the region letter against `docs/phase1-guide.md` (Step 1 table)
   and state which hypotheses it supports or weakens.
6. Update `notes/hypotheses.md` and add a journal entry (`/log` format).
7. Explain the result to the owner in Brazilian Portuguese, then propose a commit.
