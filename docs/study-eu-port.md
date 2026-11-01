# Study: port the career mode from the European build

Status: **planned** (registered 2026-11-01). It starts after Phase 1, Step 1.

## Goal

1. Compare the Brazilian ROM against the European ROM.
2. Identify the code and data that implement the career mode in the European
   build.
3. Port that functionality into the Brazilian build.

## When this study applies

The result of Step 1 (`/rom-check`) decides the path:

| Step 1 result | Meaning | Path |
|---------------|---------|------|
| Brazilian ROM is NA-based (H1/H3) | the mode is missing or only partly present | this study: full comparison and port |
| Brazilian ROM is EU-based (H2/H4) | the mode is likely in the ROM | narrow this study to finding the gate or the missing menu entry |

## Prerequisites

- A European cartridge dump **owned by the person doing the work**, stored as
  `rom/eu.z64` (git-ignored). It must never be committed, the same as the
  Brazilian ROM.
- Both ROMs identified with `tools/rom_info.py`, with results recorded in
  `notes/rom-identification.md`.

## Method (draft)

1. **Coarse diff.** Compare the two ROMs block by block to find identical,
   shifted and unique regions. This needs a new tool, `tools/rom_diff.py`
   (stdlib only). It should print offsets and similarity scores, never bytes.
2. **Locate the mode in the EU build.**
   - Search the EU ROM for career-mode menu strings with `tools/find_strings.py`.
   - Find the menu tables and the handlers they point to.
   - In Project64, set breakpoints while entering the mode to find the entry
     function and its RAM state.
3. **Map EU functions to BR functions.** Shared engine code should match
   once relocated addresses are masked. Use instruction-pattern matching and
   Ghidra's Version Tracking. Build a symbol table of matched functions.
4. **Inventory what the mode depends on.** Check which code, data tables,
   text, textures and save-data layout are present in BR, which are present
   but changed, and which are absent.
5. **Port.**
   - Find free ROM and RAM space.
   - Relocate the career-mode code and fix the calls into shared functions,
     using the map from step 3.
   - Add a menu entry, and adapt save data (Controller Pak / EEPROM) if the
     mode needs it.
6. **Validate.** Run the patched ROM in Project64 first, then on hardware if
   possible.

## Risks and open questions

- **Distribution.** A BPS patch that carries ported code would contain Konami
  code bytes, which conflicts with hard rule 1. Before Phase 2 we must decide
  what can be published. Options: patch only, published outside this
  repository, or a patch generated locally from both ROMs, so that the
  repository holds only the tool.
- The NA/BR build may have changed shared data structures since the EU build.
  If so, porting needs adaptation, not a plain copy.
- Text: the mode's strings are in European languages. A Portuguese
  translation is a separate effort.
- Compression: if the EU assets or code overlays are compressed, we need a
  decompressor first.

## Output

- Findings go in `notes/`, with evidence as usual.
- Tools go in `tools/`.
- The patch is a Phase 2 deliverable, subject to the distribution decision
  above.
