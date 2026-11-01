# Investigation journal

Newest entries at the bottom. Format: see `.claude/commands/log.md`.

---

## 2026-11-01 — Setup: repository created

- Done: repository scaffold, analysis tools (`rom_info.py`,
  `find_strings.py`), Phase 1 guide, hypotheses H1–H4.
- Evidence: tools tested against synthetic ROMs in z64/v64/n64 byte orders;
  conversions byte-identical.
- Result: ready for Step 1.
- Hypotheses affected: none.
- Next step: run `/rom-check` on the owner's ROM.

## 2026-11-01 — Planning: register BR vs EU comparison and port study

- Done: published the repository on GitHub, added `CONTRIBUTING.md`, and
  registered the next study in `docs/study-eu-port.md`. The study compares
  the Brazilian ROM against the European ROM, locates the career-mode code,
  and ports it to the Brazilian build.
- Evidence: none yet (planning entry).
- Result: study planned. Its scope depends on Step 1: full port if BR is
  NA-based, gate/menu search if BR is EU-based.
- Hypotheses affected: none. The study tests H1/H3, and its scope narrows if
  H2/H4 hold.
- Next step: Step 1 (`/rom-check`). Then obtain an owned EU dump
  (`rom/eu.z64`) and write `tools/rom_diff.py`.
