# iss2000-re

Reverse-engineering study of **International Superstar Soccer 2000** for the
Nintendo 64 (Konami / KCEO – Major A), focused on the **Brazilian release**
distributed by Gradiente.

## The mystery

The Brazilian manual describes a **career mode** that never appears in the
game's menus.

- The Japanese version (*Jikkyou J-League 1999: Perfect Striker 2*) has a
  career mode called **"Success"** (サクセス).
- The European N64 release kept it; the North American release dropped it.
- Is the Brazilian cartridge the NA build with a manual translated from the
  European one? Or is the mode still in the ROM, hidden or disabled?

## Roadmap

| Phase | Goal | Status |
|-------|------|--------|
| 1 | Find the career mode | in progress |
| 2 | ROM hack restoring findings (BPS patch) | — |
| 3 | Native port (likely via N64Recomp) | — |

## Quick start (Linux / WSL)

```bash
git clone https://github.com/<user>/iss2000-re.git
cd iss2000-re
git config core.hooksPath .githooks      # enables the anti-ROM commit guard
python3 tools/rom_info.py rom/YOUR_FILE --convert rom/baserom.z64
python3 tools/find_strings.py rom/baserom.z64 --entropy
```

Full guide: [`docs/phase1-guide.md`](docs/phase1-guide.md) ·
Findings: [`notes/`](notes/)

## Layout

```
tools/   analysis scripts (Python 3, standard library only)
docs/    guides
notes/   journal, hypotheses and evidence
rom/     your ROM (git-ignored)
.claude/ Claude Code project settings and commands
```

## Legal

*International Superstar Soccer 2000* is © Konami. This repository contains
only original tools and notes. **No ROM, game code or assets are, or will
be, distributed here.** You need a dump of a cartridge you own.

Tools and documentation are released under the MIT License (see `LICENSE`).
