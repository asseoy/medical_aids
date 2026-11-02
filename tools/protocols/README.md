# פרוטוקולים לאישור — generator

`protocols-rofan.html` (repo root) and the `protocols-rofan-*.xlsx` files are **generated**. Do not edit them by hand:
the next rebuild overwrites hand edits. Change the sources here and run:

```
python3 tools/protocols/gen.py
```

This writes `protocols-rofan.html`, one Excel per drug tab (`protocols-rofan-<tab>.xlsx`) and the icons into the repo root,
plus `tools/protocols/out/` (ignored by git): `data.json`, a body-only copy of the page, and the Excels under their Hebrew names.
It needs Python 3 with `openpyxl`.

## Where things live

| File | What it holds |
|---|---|
| `template.html` | The whole UI (CSS + JS). `__DATA__` is replaced by the data JSON. Protocols with a `kind` field (`cert`, `req`) use their own card and documentation code. |
| `data.py` | HTN drugs, rules, decisions (Israeli HTN guideline 2026). |
| `dm.py` | Diabetes (ADA 2026 + Israeli guidance). |
| `misc.py`, `tdm.py` | Other chronic drugs; close-lab-monitoring drugs. |
| `extra.py` … `extra4.py` | Later batches; `extra2.py` also defines the respiratory and neuro source protocols. |
| `multi.py` | Drugs with several indications: generic checklist only. |
| `nest.py` | Splits lab thresholds into one checklist item per parameter (K, Na, kidney, ALT…). |
| `regroup.py` | Places every drug in one of the 12 body-system tabs; builds each tab's rules, shared checks and decisions. |
| `kinds.json` | Non-drug protocols kept as data: `cert` (certificates) and `req` (digital requests), with their `out` and `msg` fields. Edit here, not in the page. |
| `regbrands.py` + `data/medicines-registry.txt` | Brand names from the Israeli registry export (Medicines.xlsx, 7.10.2026). |
| `build.py` | Assembles all sources, writes the Excels and `out/data.json`. |
| `gen.py` | Runs `build.py`, injects the data into `template.html`, writes the page and copies files. |
| `assets/` | Icons, OG image, manifest-related images. |

## Adding or changing

- A drug: add it in the relevant source module (or a new `extraN.py` imported in `build.py`) and place it in a tab in `regroup.py` (`G` dict) if its source protocol is mixed.
- A tab's rules: `regroup.py` (`BASE_RULES`, `EXTRA_RULES`).
- Certificates or digital requests: `kinds.json` (data) and the `kind` code in `template.html`.

Publishing: commit on the `refuan` branch, merge to `main` (GitHub Pages serves `main`).
