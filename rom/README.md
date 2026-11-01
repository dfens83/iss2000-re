# ROM folder

Place the ROM dumped from **your own cartridge** here. Everything in this
folder is git-ignored except this file.

Expected name after normalization: `baserom.z64`

```bash
python3 tools/rom_info.py rom/YOUR_FILE --convert rom/baserom.z64
```

Record the SHA-1 in `notes/rom-identification.md`.
