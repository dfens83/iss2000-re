# Phase 1 guide — hunting the career mode

Goal: find out whether the career mode described in the Brazilian manual
exists in the ROM and, if so, how to reach it.

Every step ends with a journal entry (`notes/journal.md`, or `/log` in
Claude Code). Do not skip steps: Step 1 alone may answer half the question.

---

## Step 0 — Environment

Inside WSL (Ubuntu):

```bash
sudo apt update && sudo apt install -y python3 git
git clone https://github.com/<user>/iss2000-re.git
cd iss2000-re
git config core.hooksPath .githooks
```

On the Windows host (needed from Step 3 on):

- **Project64** 3.x or newer: emulator with debugger, breakpoints and
  memory search.
- **Ghidra** + **JDK 21**, plus the **N64LoaderWV** extension (GitHub) so
  Ghidra can load N64 ROMs.

> Windows files are reachable from WSL under `/mnt/c/...`.

---

## Step 1 — Identify the ROM

```bash
python3 tools/rom_info.py rom/YOUR_FILE --convert rom/baserom.z64
```

Record title, game code, region, revision and SHA-1 in
`notes/rom-identification.md`.

**Why it matters:** the game code tells which build the Brazilian cartridge
was derived from.

| Code ends in | Likely meaning | Consequence |
|---|---|---|
| `E` (e.g. `NISE`) | North American ROM resold by Gradiente | Mode was cut from NA; look for leftovers (H1/H3) |
| `P`/`X`/`Y` (e.g. `NISP`, `NISY`) | European ROM | Mode should exist; find why it is hidden (H2/H4) |
| `B` | Brazil-specific build | Rare; compare with other builds |

**Ideal:** dump your own cartridge (Sanni Cart Reader, Retrode with N64
adapter, etc.) and confirm the SHA-1 matches the file you already have.

---

## Step 2 — Text search

```bash
python3 tools/find_strings.py rom/baserom.z64
python3 tools/find_strings.py rom/baserom.z64 --dump notes/dumps/strings.txt --entropy
```

What to look for:

1. Hits for `SUCCESS`, `CAREER`, `サクセス` and variants.
2. Menu text you **can see** in the game (`EXHIBITION`, `WORLD LEAGUE`).
   If found, text is not compressed and the keyword search is meaningful.
   If not, negative results prove nothing — go to Step 3.
3. In the dump, look around the menu strings: menus are usually grouped.
   An extra item in the group that never shows on screen is exactly the
   kind of clue we want.

```bash
python3 tools/find_strings.py rom/baserom.z64 --only-mine -k "EXHIBITION" -k "PENALTY"
```

---

## Step 3 — Dynamic analysis in the emulator

Technique: find where the game stores the main-menu cursor and how many
items it accepts.

1. In Project64, enable the debugger in the advanced settings.
2. Boot the game and go to the **main menu** (game modes).
3. Open **memory search** and look for the cursor value (8-bit):
   - cursor on item 1 → search `0`;
   - move down one item → refine with `1`; again → `2`; repeat until only
     a few addresses remain.
4. Record the address (e.g. `0x801XXXXX`).
5. Set a **write breakpoint** on it and move the cursor. The emulator stops
   on the instruction that writes the value.
6. Around it, look for a comparison with a constant (`slti`, `sltiu`, or a
   `beq`/`bne` against a loaded immediate). That constant is often **the
   number of menu items**.
7. Experiment: patch the constant in memory, or write a value above the
   maximum into the cursor address, and confirm the selection. A hidden mode
   may open — or the game may crash, which is also useful information.

Record addresses, instructions and outcomes.

---

## Step 4 — Static analysis in Ghidra

Only after Step 3, with concrete addresses in hand.

1. Create a Ghidra project outside the repo, or inside `ghidra/`
   (git-ignored).
2. Import `rom/baserom.z64` with the N64LoaderWV loader.
3. Jump to the instruction found in Step 3 and read the whole function in
   the decompiler window.
4. Look for:
   - **function-pointer tables** near the menu code — one entry per game
     mode; an entry beyond the visible item count is suspicious;
   - **unreferenced functions** next to the other modes' functions;
   - **region checks** (reads of header byte `0x3E` or a language global)
     that branch away from the mode.

---

## Phase 1 exit criteria

One of three answers, with logged evidence:

- **A)** The mode exists and was re-enabled (addresses + reproduction steps).
- **B)** Leftovers exist (text, functions, tables) but the mode is incomplete.
- **C)** No trace: the ROM is the NA build and the manual was wrong.

All three are valid, documentable results.
