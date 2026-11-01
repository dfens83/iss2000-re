# Hypotheses — career mode in the Brazilian release

Statuses: `open`, `supported`, `weakened`, `confirmed`, `rejected`.

| ID | Hypothesis | Test | Status | Evidence |
|----|------------|------|--------|----------|
| H1 | Brazilian ROM is the North American build (`NISE`); the mode was removed and the manual was translated from the European one | Step 1: game code | open | — |
| H2 | ROM is European-based; the mode exists but is hidden (code, button combo or unlock condition) | Steps 2–3 | open | — |
| H3 | Career-mode code is left over in the NA-based ROM without a menu entry | Steps 3–4: menu tables, unreferenced functions | open | — |
| H4 | The mode is gated by a region/language check | Step 4: reads of header byte `0x3E` or a language global | open | — |

## Known facts

- Japanese version: career mode "Success" (サクセス).
- European N64 release: has the mode.
- North American release: does not.
- Brazilian manual (Gradiente): describes a career mode.
