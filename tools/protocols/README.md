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
| `handover.py` | Kiryat Ono handover-booklet decisions (3.11.2026) applied to every drug: 3 consecutive renewals + 3rd-renewal patient message, visit-missing also notifies the physician, quantity/units/frequency and interaction checks ("wait for the physician"), the results warning and the general-instructions panel (`GUIDE`). |
| `stage_b.py` | Stimulants (child/adult entries, renewable when chronic), opioids and benzodiazepines (prepared for physician approval, suit `הכנה`), 3-month interval for addictive drugs. |
| `stage_c.py` | Tab "תרופות שאינן כרוניות": drugs not on the chronic list, strong NSAIDs, terbinafine, steroid eye drops, topical steroids (fixed patient note `patnote`). |
| `review1107.py` | One-by-one review of the 59 physician-only items (7.11.2026): each opened as regular (own checklist) or red flag (suit `הכנה` + `red`), three stay physician-only; splits MS (Copaxone), adds the strep exception, splits tetanus / anti-D (rabies removed); fixes the rule and decision texts that listed them. |
| `multi.py` | Drugs with several indications: generic checklist only. |
| `nest.py` | Splits lab thresholds into one checklist item per parameter (K, Na, kidney, ALT…). |
| `regroup.py` | Places every drug in one of the 12 body-system tabs; builds each tab's rules, shared checks and decisions. |
| `kinds.json` | Non-drug protocols kept as data: `cert` (certificates), `req` (digital requests) and `vac` (vaccines), with their `out` and `msg` fields. Edit here, not in the page. |
| `regbrands.py` + `data/medicines-registry.txt` | Brand names from the Israeli registry export (Medicines.xlsx, 7.10.2026). |
| `build.py` | Assembles all sources, writes the Excels and `out/data.json`. |
| `yoman.py` | Builds `protocols-rofan-yoman.xlsx` from the hand-made template in `assets/`: adds missing drugs to the item lists, keeps the red-flag list, and adds the two flag columns (orange deviation, red flag). Called by `gen.py`. |
| `gen.py` | Runs `build.py`, injects the data into `template.html`, writes the page and copies files. |
| `assets/` | Icons, OG image, manifest-related images; `protocols-rofan-yoman.xlsx`, the task-log template (edited by hand; `yoman.py` syncs it on build). |

## Adding or changing

- A drug: add it in the relevant source module (or a new `extraN.py` imported in `build.py`) and place it in a tab in `regroup.py` (`G` dict) if its source protocol is mixed.
- A tab's rules: `regroup.py` (`BASE_RULES`, `EXTRA_RULES`).
- Certificates or digital requests: `kinds.json` (data) and the `kind` code in `template.html`.

Publishing: commit on the `refuan` branch, merge to `main` (GitHub Pages serves `main`).

## Review booklet (PDF)

`python3 tools/protocols/booklet.py` (after `gen.py`) builds `out/booklet.pdf`: every tab's rules, shared checks, decisions,
a tick-box list, and the full checklist of every item, from `out/data.json`. It also copies the PDF to the repo root as
`protocols-rofan-booklet.pdf`, which every tab of the page links to ("חוברת בקרה"). Rebuild and commit it after protocol changes. Needs Python Playwright (Chromium). Fonts: Heebo (OFL) in `fonts/`.

## Item fields used by the template

`suit`: כן / בתנאים / הכנה (assistant prepares, physician approves; outcome preset to "waiting") / לא (message only).
Check fields: `opt` + `q` (yes/no question), `sev` (severe value asked when not ticked), `contra`, `clinic` (booking),
`notify` (also message the physician), `wait` (renewal waits for the physician), `pat` (yes/no question that adds a patient message).
Drug fields: `red` (red flag: the physician double-checks before approval; shown as a red badge, in the documentation text and in the booklet), `drnote` (fixed line to the physician in the documentation text), `doctitle` (title of the copied text), `patnote` (fixed patient instruction), `defout` (default outcome in kind tabs).
