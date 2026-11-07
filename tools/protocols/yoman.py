# Task log (יומן הנחיות): keeps the hand-made template in assets/ and, on every build, syncs it with the tool:
#  - every drug of every tab is in the "פריטים" list of its task type (only missing ones are added, in the same "name – brands" form)
#  - two flag columns (decision 7.11.2026): "חריגה מהפרוטוקול" (orange; any finding other than "ללא חריגה") and
#    "דגל אדום" (red; the item is on the red-flag list, kept in "רשימות"). Both are formulas the user can overwrite.
# Usage: called from gen.py (after build.py); writes protocols-rofan-yoman.xlsx in the repo root.
import json, os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import TableColumn

S = os.path.dirname(os.path.abspath(__file__)) + "/"
REPO = os.path.abspath(S + "../..") + "/"
ROWS = 5000
DEV, RED = "חריגה מהפרוטוקול", "דגל אדום"


def label(d):
    names = []
    for b in d["brands"]:
        h = (b.get("he") or b["en"]).strip()
        if h and h not in names:
            names.append(h)
    return d["he"] + (" – " + ", ".join(names[:3]) if names else "")


def run(data_path=S + "out/data.json", src=S + "assets/protocols-rofan-yoman.xlsx", dst=REPO + "protocols-rofan-yoman.xlsx"):
    A = json.load(open(data_path))
    wb = openpyxl.load_workbook(src)
    items, log, lists = wb["פריטים"], wb["יומן הנחיות"], wb["רשימות"]
    head = {c.value: c.column for c in items[1] if c.value}
    red_labels = []
    for k in A["order"]:
        T = A[k]
        if T.get("kind"):
            continue
        col = head.get("תרופה שאינה כרונית" if k == "nonchronic" else "מרשם כרוני · " + T["name"])
        if not col:
            raise KeyError("yoman: no item column for tab " + k)
        have = [items.cell(row=r, column=col).value for r in range(2, items.max_row + 2)]
        have = [v for v in have if v]
        keys = {v.split(" – ")[0] for v in have}
        other = "אחר" if "אחר" in have else None
        if other:
            have.remove("אחר")
        for d in T["drugs"]:
            lab = label(d)
            if d["he"] not in keys:
                have.append(lab); keys.add(d["he"])
            if d.get("red"):
                red_labels.append(next(v for v in have if v.split(" – ")[0] == d["he"]))
        if other:
            have.append(other)
        for r in range(2, max(items.max_row, len(have) + 1) + 1):
            items.cell(row=r, column=col).value = have[r - 2] if r - 2 < len(have) else None

    # red-flag list in "רשימות" (next free column)
    rc = lists.max_column + 1 if lists.cell(row=1, column=lists.max_column).value != RED else lists.max_column
    lists.cell(row=1, column=rc, value=RED).font = Font(bold=True)
    for r in range(2, max(lists.max_row, len(red_labels) + 1) + 1):
        lists.cell(row=r, column=rc).value = red_labels[r - 2] if r - 2 < len(red_labels) else None
    L = openpyxl.utils.get_column_letter(rc)

    # two flag columns after the last one
    t = log.tables["Hanchayot"]
    last = log.max_column
    names = [c.value for c in log[1]]
    if DEV in names:
        cdev, cred = names.index(DEV) + 1, names.index(RED) + 1
    else:
        cdev, cred = last + 1, last + 2
    hf, hfill = log.cell(row=1, column=1).font, log.cell(row=1, column=1).fill
    for c, name, w in ((cdev, DEV, 16), (cred, RED, 12)):
        h = log.cell(row=1, column=c, value=name)
        h.font, h.fill = hf.copy(), hfill.copy()
        h.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        log.column_dimensions[openpyxl.utils.get_column_letter(c)].width = w
    D, R = openpyxl.utils.get_column_letter(cdev), openpyxl.utils.get_column_letter(cred)
    for r in range(2, ROWS + 1):
        log.cell(row=r, column=cdev, value=f'=IF(OR($I{r}="",$I{r}="ללא חריגה"),"","{DEV}")')
        log.cell(row=r, column=cred, value=f'=IF($H{r}="","",IF(COUNTIF(רשימות!${L}$2:${L}$300,$H{r})>0,"{RED}",""))')
        for c in (cdev, cred):
            log.cell(row=r, column=c).alignment = Alignment(horizontal="center")
    log.conditional_formatting.add(f"{D}2:{D}{ROWS}", CellIsRule(operator="equal", formula=[f'"{DEV}"'],
                                   fill=PatternFill("solid", fgColor="F4B183"), font=Font(bold=True, color="7F3F00")))
    log.conditional_formatting.add(f"{R}2:{R}{ROWS}", CellIsRule(operator="equal", formula=[f'"{RED}"'],
                                   fill=PatternFill("solid", fgColor="C00000"), font=Font(bold=True, color="FFFFFF")))
    for c, val in ((D, DEV), (R, RED)):
        dv = DataValidation(type="list", formula1=f'"{val}"', allow_blank=True, showErrorMessage=False)
        dv.add(f"{c}2:{c}{ROWS}"); log.add_data_validation(dv)
    if DEV not in names:
        t.tableColumns.append(TableColumn(id=len(t.tableColumns) + 1, name=DEV))
        t.tableColumns.append(TableColumn(id=len(t.tableColumns) + 1, name=RED))
    t.ref = f"A1:{R}{ROWS}"
    if t.autoFilter is not None:
        t.autoFilter.ref = t.ref

    # explanation sheet
    ex = wb["הסבר"]
    if not any(c.value and str(c.value).startswith("• שני סימונים") for c in ex["A"]):
        ex.append([None])
        ex.append(["• שני סימונים נפרדים (מתמלאים לבד, אפשר לשנות): ״חריגה מהפרוטוקול״ בכתום — כל ממצא שאינו ״ללא חריגה״, הרופא/ה מחליט/ה; "
                   "״דגל אדום״ באדום — תרופה בסיכון גבוה יותר, תמיד בדיקה כפולה מול הרופא/ה. תרופה יכולה לשאת את שניהם."])
    wb.save(dst)
    return len(red_labels)


if __name__ == "__main__":
    print("yoman red:", run())
