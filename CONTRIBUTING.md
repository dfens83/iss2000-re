# Contributing to iss2000-re

Thanks for helping. This is a public reverse-engineering study, so a few rules
are strict. Please read this page before your first commit.

## The golden rule: no ROM or extracted game data

**Never commit a game ROM, a fragment of one, game code, or data extracted
from a ROM.** This includes code bytes, textures, audio, bulk text dumps and
decompressed data.

Maintainers may commit photographs and scans of Brazilian retail physical
media under `assets/physical-media/` and `docs/references/` for identification
and research. These reference materials contain third-party content and are
not covered by the repository's MIT license. This exception does not permit
ROM data or material extracted from the game.

Two guards enforce this:

- `.gitignore` ignores `rom/*`, the usual ROM extensions and `notes/dumps/`.
- `.githooks/pre-commit` blocks files with ROM-like extensions or the N64 ROM
  signature. It also blocks files larger than 1 MiB except approved image
  files under `assets/physical-media/` and PDFs under `docs/references/`.

The hook is **not** enabled automatically by `git clone`. Enable it once per
clone:

```bash
git config core.hooksPath .githooks
```

Do not weaken the ROM checks or bypass the hook (`--no-verify` included).

You may quote short excerpts that a finding needs: an address, a single
instruction or a short string. Bulk output goes to `notes/dumps/`, which is
git-ignored.

## Setup

```bash
git clone https://github.com/dfens83/iss2000-re.git
cd iss2000-re
git config core.hooksPath .githooks
```

Use a dump of a cartridge you own. Put it in `rom/` and normalize it to
big-endian `.z64`:

```bash
python3 tools/rom_info.py rom/YOUR_FILE --convert rom/baserom.z64
```

Then follow [`docs/phase1-guide.md`](docs/phase1-guide.md).

## Evidence standard for `notes/`

Every claim must be reproducible. Each one needs:

- the **location**: ROM offset or RAM address;
- the **method**: the tool, emulator or breakpoint used;
- **how to reproduce** it: the command line or the steps.

Unverified ideas go in `notes/hypotheses.md` as hypotheses, not as facts.
Record work sessions in `notes/journal.md`, newest entry at the bottom.

## Tools

- Python 3, **standard library only**, one small script per task in `tools/`.
- Every script starts with a docstring that explains its usage.
- Scripts print small, targeted ranges, never whole-ROM dumps.

## Language and style

- Everything committed is in **English**: code, comments, docs, notes and
  commit messages.
- Keep commits small and descriptive, one logical change each.

## Workflow

- **Collaborators:** create a branch, push it and open a pull request against
  `main`.
- **Everyone else:** fork the repository, then open a pull request.
- If a pull request changes the state of a hypothesis, it must also update
  `notes/hypotheses.md` and add a journal entry.

## Claude Code (optional)

The repository ships with Claude Code project settings and commands
(`/rom-check`, `/find-text`, `/log`, `/hypothesis`). `CLAUDE.md` describes the
project context and the rules that the assistant follows.
