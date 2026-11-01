---
description: Search keywords (ASCII, Latin-1, Shift-JIS) in rom/baserom.z64
argument-hint: [extra keywords separated by spaces, optional]
---

Search the ROM for text.

1. Build `-k` flags from `$ARGUMENTS` (quote multi-word terms as given).
2. Run `python3 tools/find_strings.py rom/baserom.z64 <flags> --entropy`.
3. First check whether **visible menu text** (e.g. `EXHIBITION`) is found.
   If not, warn that text is likely compressed and negative keyword results
   prove nothing.
4. Report hits as a table: offset, keyword, encoding, short context.
5. For any promising hit, run a targeted dump into `notes/dumps/` and inspect
   only the surrounding strings (menus tend to be grouped).
6. Log findings with evidence; explain to the owner in Brazilian Portuguese.
