# CLAUDE.md — iss2000-re

Context file for Claude Code. Read it fully at the start of every session.

## Project in one paragraph

Reverse-engineering study of *International Superstar Soccer 2000* for the
Nintendo 64 (Konami / KCEO – Major A), **Brazilian release distributed by
Gradiente**. The Brazilian manual describes a **career mode** that no player
ever found in the game. Finding out whether that mode exists in the ROM —
and how to reach it — is the first goal. Long-term goals are a ROM hack that
restores what is found and, later, a native PC port.

## Owner and communication

- Owner: Junior (Brazil). Beginner in reverse engineering, MIPS assembly and
  C. Engineer by profession: comfortable with technical reasoning, new to this
  domain. Explain *why* a step matters, briefly, before asking him to run it.
- **Talk to the owner in Brazilian Portuguese**, formal and technical, direct.
- **Everything committed to the repository is in English** (code, comments,
  docs, notes, commit messages). The repository is public.
- Ask clarifying questions before long or detailed work.

## Hard rules

1. **Never commit a game ROM, a fragment of one, game code, or data extracted
   from a ROM** (including textures, audio, bulk text dumps and decompressed
   data). Maintainers may add photographs and scans of Brazilian retail
   physical media under `assets/physical-media/` and `docs/references/` for
   identification and research. These third-party reference materials are not
   covered by the repository's MIT license. This exception never permits ROM
   data. `.gitignore` and `.githooks/pre-commit` guard game data; do not weaken
   those checks.
2. **Never load the ROM into context** with Read or `cat`/`xxd` of large
   ranges. Use the scripts in `tools/`, and print only small, targeted ranges
   (offsets + a few dozen bytes) when needed.
3. Short excerpts needed to explain a finding (an address, an instruction,
   a short string) are fine in notes. Bulk dumps go to `notes/dumps/`
   (git-ignored).
4. Every claim in `notes/` must carry evidence: ROM offset or RAM address,
   method used, and how to reproduce.
5. Prefer small, dependency-free Python 3 scripts in `tools/`. Each script
   has a docstring with usage.

## Known facts (with sources)

- Developer: Major A / Konami Computer Entertainment Osaka; same studio made
  ISS 64 and ISS '98, so the engine is likely shared. (MobyGames)
- Japanese version: *Jikkyou J-League 1999: Perfect Striker 2*, has the
  career mode "Success" (サクセス). (Wikipedia)
- Success mode exists in the European N64 release, not in the North American
  one. (Wikipedia)
- No public decompilation project for this game was found (2026-11-01).
- Known GameShark addresses exist (e.g. player stats around `0x801A840C`,
  NTSC-U), useful as RAM landmarks. (almarsguides.com)

## Working hypotheses

Tracked in `notes/hypotheses.md`. Summary:

- **H1** Brazilian ROM = North American ROM; mode removed; manual translated
  from the European one.
- **H2** ROM is European-based; mode exists but is hidden.
- **H3** Residual career-mode code in the NA-based ROM, no menu entry.
- **H4** Mode gated by a region/language check.

## Current status

- Phase 1, **Step 1 pending**: owner must run `/rom-check` on his ROM and
  report the game code and SHA-1. The region letter decides between H1/H3
  and H2/H4.
- Next study (planned): compare BR vs EU ROMs, locate the career-mode code
  and port it to the BR build. Plan: `docs/study-eu-port.md`.

## Phases

| Phase | Goal |
|-------|------|
| 1 | Find the career mode (guide: `docs/phase1-guide.md`) |
| 2 | ROM hack restoring findings (patch format: BPS) |
| 3 | Native port, likely via N64Recomp |

## Repository layout

```
CLAUDE.md            this file
README.md            public overview
.claude/             Claude Code settings and slash commands
.githooks/           pre-commit guard against ROM commits
assets/physical-media/ reference photos of the Brazilian retail release
tools/               analysis scripts (Python 3, stdlib only)
docs/                guides, technical documentation and references
docs/references/     scans of physical documentation
notes/               journal, hypotheses, ROM identification (evidence)
notes/dumps/         bulk outputs, git-ignored
rom/                 owner's ROM, git-ignored (expected: rom/baserom.z64)
```

## Toolchain

- WSL2 (Ubuntu) for scripts and git.
- Windows host: Project64 3.x+ (debugger, memory search, breakpoints),
  Ghidra + JDK 21 + N64LoaderWV extension.
- Later phases: splat, m2c, asm-differ, N64Recomp.

## Slash commands

- `/rom-check [path]`  identify and normalize the ROM, fill the ID sheet
- `/find-text [words]` keyword search in the ROM
- `/log [summary]`     add a dated journal entry
- `/hypothesis [id] [update]` update the hypotheses table

## Session checklist

1. Read `notes/journal.md` (latest entries) and `notes/hypotheses.md`.
2. Confirm with the owner what he wants to do today.
3. After any finding: update journal + hypotheses, then propose a commit.
4. Update **Current status** above when a step completes.

## Git

- Enable the guard once per clone: `git config core.hooksPath .githooks`
- Small, descriptive commits in English.
