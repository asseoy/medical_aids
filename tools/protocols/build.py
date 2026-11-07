import sys, json
import os
S = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, S)
import data as HTN, dm as DM, misc as MISC, tdm as TDM
import extra, extra2, extra3, extra4
TDM.DRUGS += extra.EXTRA_TDM; MISC.DRUGS += extra.EXTRA_MISC
TDM.DECISIONS += extra.DEC_TDM; MISC.DECISIONS += extra.DEC_MISC
TDM.DRUGS += extra2.TDM_DRUGS; MISC.DRUGS += extra2.MISC_DRUGS
TDM.DECISIONS += extra2.DEC_TDM; MISC.DECISIONS += extra2.DEC_MISC
MISC.DECISIONS[:] = [d if d[0] != 10 else (10, "משאפים לאסתמה ול-COPD", "-", "בפרוטוקול נפרד: \"נשימה\"", "החלטה מקומית", "-") for d in MISC.DECISIONS]
MISC.RENEW_RULES.append("הורמונים, שלפוחית רגיזה, PDE5, ברזל/B12, קרדיולוגיה, גסטרו ואנדוקרינולוגיה: לפי הרשימה של כל תרופה")
MISC.RENEW_RULES.append("אריתרופויאטין, קושרי זרחן ואשלגן, HIV, הפטיטיס B, ציקלוספורין/טקרולימוס, אפרמילסט ואציטרטין: חידוש ע\"י רופא/ה בלבד")
RESP, NEURO = extra2.RESP, extra2.NEURO
import multi; multi.apply(HTN.DRUGS, DM.DRUGS)
MISC.DRUGS += extra3.MISC_DRUGS; TDM.DRUGS += extra3.TDM_DRUGS; NEURO.DRUGS += extra3.NEURO_DRUGS
MISC.DECISIONS += extra3.DEC_MISC; TDM.DECISIONS += extra3.DEC_TDM; NEURO.DECISIONS += extra3.DEC_NEURO
MISC.DRUGS += extra4.MISC_DRUGS; TDM.DRUGS += extra4.TDM_DRUGS; NEURO.DRUGS += extra4.NEURO_DRUGS
MISC.DECISIONS += extra4.DEC_MISC; TDM.DECISIONS += extra4.DEC_TDM; NEURO.DECISIONS += extra4.DEC_NEURO
for _d in MISC.DRUGS:
    for _b in extra3.EXTRA_ONLY_BRANDS.get(_d["generic"], []) + extra4.EXTRA_ONLY_BRANDS.get(_d["generic"], []):
        if _b["en"].lower() not in {x["en"].lower() for x in _d["brands"]}: _d["brands"].append(_b)
for _M in (HTN, DM):
    _M.RENEW_RULES.append("תרופות עם כמה התוויות (מעכבי ACE ו-ARB בודדים, ספירונולקטון, אפלרנון, פינרנון, אנטרסטו, פוסיד, ביסופרולול, מטופרולול, קרבדילול, פרופרנולול, פורקסיגה, ג'רדיאנס, אוזמפיק/וגובי, מונג'רו): רק בדיקות משותפות; יעד הטיפול נבדק ע\"י הרופא/ה")
HTN.DECISIONS.append((max(int(x[0]) for x in HTN.DECISIONS if str(x[0]).isdigit()) + 1, "תרופות עם כמה התוויות", "-", "חוסמי בטא (ביסופרולול, מטופרולול, קרבדילול, פרופרנולול), מעכבי ACE ו-ARB בודדים (לא בשילוב קבוע), ספירונולקטון, אפלרנון, פינרנון, אנטרסטו ופוסיד: בלי יעד ל\"ד ובלי סעיף גיל 80; במקום זה טווח בטיחות: סיסטולי 100 ומעלה ומתחת ל-160/100. דופק, אשלגן וכליות כמו קודם", "החלטה מקומית (2.11.2026)", "-"))
DM.DECISIONS.append((max(int(x[0]) for x in DM.DECISIONS if str(x[0]).isdigit()) + 1, "תרופות עם כמה התוויות", "-", "דפגליפלוזין ואמפגליפלוזין: בלי HbA1c; eGFR מתחת ל-25 ← הודעה (במקום 45). סמגלוטייד וטירזפטייד: בלי HbA1c; מדידת משקל שנתית", "החלטה מקומית (2.11.2026)", "-"))
MISC.RENEW_RULES.append("טיפות לגלאוקומה: ביקורת שנתית אצל רופא/ת עיניים. NSAID ממושך: כליות, אשלגן, ל\"ד ודימום")
MISC.RENEW_RULES.append("רואקוטן, ממריצים, אופיואידים ובנזודיאזפינים: חידוש ע\"י רופא/ה בלבד (רואקוטן — רופא/ת עור)")
TDM.RENEW_RULES.append("סטרואידים, נוגדי פסיכוזה ותרופות מדכאות חיסון לא נעצרים ע\"י רפואן מלבד ערך חמור או התווית נגד")
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.formatting.rule import CellIsRule

F = "Arial"
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HDR = PatternFill("solid", fgColor="1F4E78")
SEC = PatternFill("solid", fgColor="DDEBF7")
NOTE = PatternFill("solid", fgColor="FFF2CC")


def setup(ws, headers, widths):
    ws.sheet_view.rightToLeft = True
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        c = ws.cell(row=1, column=i, value=h)
        c.font = Font(name=F, bold=True, color="FFFFFF", size=11)
        c.fill = HDR
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
        ws.column_dimensions[c.column_letter].width = w
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 34


def add(ws, row, values, fill=None, bold=False):
    for i, v in enumerate(values, start=1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = Font(name=F, size=10, bold=bold)
        c.alignment = Alignment(horizontal="right", vertical="top", wrap_text=True)
        c.border = BORDER
        if fill:
            c.fill = fill


def section(ws, row, text, n):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=n)
    c = ws.cell(row=row, column=1, value=text)
    c.font = Font(name=F, size=11, bold=True, color="1F4E78")
    c.fill = SEC


def note(ws, row, text, n, h=48):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=n)
    c = ws.cell(row=row, column=1, value=text)
    c.font = Font(name=F, size=10, italic=True)
    c.fill = NOTE
    c.alignment = Alignment(horizontal="right", vertical="top", wrap_text=True)
    ws.row_dimensions[row].height = h


def build(M, out, title):
    COMMON, RENEW_RULES, DRUGS, DECISIONS, GUIDE, VERSION = M.COMMON, M.RENEW_RULES, M.DRUGS, M.DECISIONS, M.GUIDE, M.VERSION
    VERIFY = M.VERIFY
    wb = Workbook()
    # ---- sheet 1
    ws1 = wb.active
    ws1.title = "מעקב משותף"
    h1 = ["תחום", "מה הרפואן בודק", "קריטריון", "אם לא מתקיים", "מקור"]
    setup(ws1, h1, [22, 34, 56, 40, 30])
    r, cur = 2, None
    section(ws1, r, "כללי חידוש", 5); r += 1
    for rule in RENEW_RULES:
        ws1.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
        add(ws1, r, [rule]); r += 1
    for sec, topic, check, rule, fail, src in COMMON:
        if sec != cur:
            section(ws1, r, sec, 5); r += 1; cur = sec
        add(ws1, r, [topic, check, rule, fail, src]); r += 1
    r += 1
    note(ws1, r, f"מקור: {GUIDE}. \"החלטה N\" מפנה לגיליון \"החלטות\". {VERSION}", 5, 32)

    # ---- sheet 2
    ws2 = wb.create_sheet("לפי חומר פעיל")
    h2 = ["קבוצה תרפויטית", "חומר פעיל", "שמות מסחריים בישראל", "בדיקות מעקב ותדירות", "ערכי סף להחזרה לרופא",
          "תלונות שמחייבות החלפה או הפסקה", "מצבים שמוציאים מהפרוטוקול", "מתאים לרפואן", "נימוק", "מקור"]
    setup(ws2, h2, [18, 20, 36, 36, 30, 44, 38, 11, 30, 20])


    def brands_txt(bs):
        return "; ".join(f"{b['en']} ({b['he']})" + (f" - {b['note']}" if b["note"] else "") for b in bs)


    for i, d in enumerate(DRUGS, start=2):
        add(ws2, i, [d["cls"], d["generic"], brands_txt(d["brands"]), d["labs"], "; ".join(d["thr"]),
                     "; ".join(f"{c} ← {a}" for c, a in d["comp"]), "; ".join(d.get("excl_x", d["excl"])), d["suit"] + (" (דגל אדום)" if d.get("red") else ""), d["why"], d["src"]])
        ws2.cell(row=i, column=8).alignment = Alignment(horizontal="center", vertical="top")
    last = 1 + len(DRUGS)
    rng = f"H2:H{last}"
    for val, col in (("כן", "C6EFCE"), ("בתנאים", "FFEB9C"), ("לא", "FFC7CE")):
        ws2.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{val}"'], fill=PatternFill("solid", fgColor=col)))
    ws2.auto_filter.ref = f"A1:J{last}"
    note(ws2, last + 2, f"שמות מסחריים: מאגר התרופות בפרויקט (7.10.2026). \"{VERIFY}\" = לא נמצא במאגר. "
         "עמודות \"מתאים לרפואן\" ו\"נימוק\" הן החלטת הפרוטוקול, לא ציטוט מההנחיה. מקור: " + GUIDE + ".", 10)
    add(ws2, last + 4, ["סיכום", "כן", "בתנאים", "לא"], fill=SEC, bold=True)
    add(ws2, last + 5, ["מספר חומרים", f'=COUNTIF({rng},"כן")', f'=COUNTIF({rng},"בתנאים")', f'=COUNTIF({rng},"לא")'])

    # ---- sheet 3
    ws3 = wb.create_sheet("החלטות")
    h3 = ["#", "נושא", "מה ההנחיה הישראלית אומרת", "ההחלטה לפרוטוקול", "סוג", "מקור בהנחיה"]
    setup(ws3, h3, [5, 22, 46, 50, 18, 26])
    for i, d in enumerate(DECISIONS, start=2):
        add(ws3, i, list(d))
    k = 1 + len(DECISIONS)
    note(ws3, k + 2, "סוג: \"הכרעה\" = פרקים בהנחיה סותרים ונבחרה אפשרות אחת. \"החלטה מקומית\" = ההנחיה לא נותנת ערך, והערך נקבע ע\"י הרופא האחראי. "
         f"כל ההחלטות לאישור ניהול סיכונים לפני הפעלה. {VERSION}", 6)

    for ws in wb.worksheets:
        ws.page_setup.orientation = "landscape"
    wb.save(out)


import os, copy, urllib.parse
from nest import nest
import regroup, ingredients
OUT = S + "out/"
os.makedirs(OUT, exist_ok=True)
X = "https://asseoy.github.io/medical_aids/"
V = lambda u: "https://view.officeapps.live.com/op/view.aspx?src=" + urllib.parse.quote(u, safe="")
SRC_LINKS = {
    "htn": [["יתר לחץ דם בישראל — אבחנה, טיפול ואיזון (2026, PDF)", "https://www.ish.org.il/images/hbp-guidelines2026.pdf"]],
    "dm": [["ADA Standards of Care 2026", "https://diabetesjournals.org/care/issue/49/Supplement_1"],
           ["קווי הכוונה לטיפול בסוכרת סוג 2, עדכון 13.01.2021 (PDF)", "https://emekmed.co.il/wp-content/uploads/2022/12/13.1.2021-%D7%A7%D7%95%D7%95%D7%99-%D7%94%D7%9B%D7%95%D7%95%D7%A0%D7%94-%D7%9C%D7%98%D7%99%D7%A4%D7%95%D7%9C-%D7%91%D7%A1%D7%95%D7%9B%D7%A8%D7%AA-%D7%A1%D7%95%D7%92-2-%D7%A2%D7%93%D7%9B%D7%95%D7%9F.pdf"]],
    "resp": [["GINA 2026 — Summary Guide", "https://ginasthma.org/reports/"]],
    "misc": [["הנחיות ישראליות לטיפול בדיסליפידמיה 2020 (PDF)", "https://www.ias.org.il/ias-dislipidemia-guideslines-2020.pdf"]],
    "tdm": [["עלון לצרכן לפונקס (PDF)", "https://www.alpha-med.co.il/html5/Web/9415/leponex.pdf"]],
}
LINK_FOR = {"cardio": ["htn", "misc"], "endo": ["dm"], "resp": ["resp"], "psych": ["tdm"]}
import stage_b; stage_b.apply(MISC)
import stage_c; stage_c.apply(MISC)
import otc; MISC.DRUGS.extend(otc.NEW)
import extra5; extra5.apply([HTN.DRUGS, DM.DRUGS, RESP.DRUGS, NEURO.DRUGS, TDM.DRUGS, MISC.DRUGS])
import extra6; extra6.apply([HTN.DRUGS, DM.DRUGS, RESP.DRUGS, NEURO.DRUGS, TDM.DRUGS, MISC.DRUGS])
import extra7; extra7.apply([HTN.DRUGS, DM.DRUGS, RESP.DRUGS, NEURO.DRUGS, TDM.DRUGS, MISC.DRUGS])
import extra9; extra9.apply([HTN.DRUGS, DM.DRUGS, RESP.DRUGS, NEURO.DRUGS, TDM.DRUGS, MISC.DRUGS])
import extra8; extra8.apply([HTN.DRUGS, DM.DRUGS, RESP.DRUGS, NEURO.DRUGS, TDM.DRUGS, MISC.DRUGS])
import review1107; review1107.apply([HTN.DRUGS, DM.DRUGS, RESP.DRUGS, NEURO.DRUGS, TDM.DRUGS, MISC.DRUGS])
import handover; handover.apply(HTN.DRUGS, DM.DRUGS, RESP.DRUGS, NEURO.DRUGS, MISC.DRUGS, TDM.DRUGS)
CATS = regroup.regroup({"htn": HTN, "dm": DM, "resp": RESP, "neuro": NEURO, "misc": MISC, "tdm": TDM})
review1107.texts(CATS)
ALL = {"draft": HTN.DRAFT, "order": [k for k, *_ in regroup.CATS], "warn": handover.RESULTS_WARNING, "guide": handover.GUIDE}
for k, C in CATS.items():
    build(C, OUT + "פרוטוקול_רפואן_" + C.xname + ".xlsx", C.NAME)
    drugs = copy.deepcopy(C.DRUGS)
    for d in drugs: nest(d); ingredients.annotate(d)
    f = "protocols-rofan-" + k + ".xlsx"
    links = [["הטבלה המסכמת (Excel)", [["צפייה", V(X + f)], ["הורדה", X + f]]]]
    g = [l for s in LINK_FOR.get(k, []) for l in SRC_LINKS[s]]
    if g: links.append(["הנחיות", g])
    ALL[k] = {"key": k, "name": C.NAME, "example": C.example, "links": links, "drugs": drugs, "common": C.COMMON,
              "rules": C.RENEW_RULES, "decisions": C.DECISIONS, "guide": C.GUIDE, "version": C.VERSION}
# non-drug protocols with a "kind" (cert = certificates, req = digital requests): kept as data in kinds.json
for _k, _v in json.load(open(S + "kinds.json")).items():
    ALL[_k] = _v; ALL["order"].append(_k)


def build_vac(V, out):
    """Excel for the vaccines tab (kind "vac"), same layout as the drug tabs: shared checks, per vaccine, decisions."""
    wb = Workbook()
    ws1 = wb.active; ws1.title = "לפני כל חיסון"
    setup(ws1, ["תחום", "מה הרפואן בודק", "קריטריון", "אם לא מתקיים", "מקור"], [20, 34, 50, 44, 24])
    r = 2
    section(ws1, r, "כללים", 5); r += 1
    for rule in V["rules"]:
        ws1.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5); add(ws1, r, [rule]); r += 1
    section(ws1, r, "בדיקות משותפות", 5); r += 1
    for sec, topic, check, rule, fail, src in V["common"]:
        add(ws1, r, [topic, check, rule, fail, src]); r += 1
    note(ws1, r + 1, f"מקור: {V['guide']}. {V['version']}", 5, 32)
    ws2 = wb.create_sheet("לפי חיסון")
    setup(ws2, ["חיסון", "שמות נוספים", "מתאים לרפואן", "הערות", "מה הרפואן בודק", "אם לא מתקיים ← לרופא/ה", "הודעה למטופל/ת", "מקור"],
          [26, 24, 11, 36, 60, 44, 50, 26])
    for i, d in enumerate(V["drugs"], start=2):
        names = "; ".join(b["he"] + (f" ({b['en']})" if b["en"] else "") for b in d["brands"])
        checks = "\n".join(f"• {c['label']}: {c['det']}" for c in d["checks"])
        fails = "\n".join(f"• {c['crit']}" for c in d["checks"] if c.get("crit"))
        add(ws2, i, [d["he"], names, d["suit"], d["why"], checks, fails, d.get("msg", ""), d["src"]])
        ws2.cell(row=i, column=3).alignment = Alignment(horizontal="center", vertical="top")
    last = 1 + len(V["drugs"])
    for val, col in (("כן", "C6EFCE"), ("בתנאים", "FFEB9C"), ("לא", "FFC7CE")):
        ws2.conditional_formatting.add(f"C2:C{last}", CellIsRule(operator="equal", formula=[f'"{val}"'], fill=PatternFill("solid", fgColor=col)))
    ws2.auto_filter.ref = f"A1:H{last}"
    ws3 = wb.create_sheet("החלטות")
    setup(ws3, ["#", "נושא", "מה ההנחיה אומרת", "ההחלטה לפרוטוקול", "סוג", "מקור"], [5, 22, 40, 50, 22, 22])
    for i, d in enumerate(V["decisions"], start=2):
        add(ws3, i, list(d))
    for ws in wb.worksheets:
        ws.page_setup.orientation = "landscape"
    wb.save(out)


if "vac" in ALL:
    build_vac(ALL["vac"], OUT + "protocols-rofan-vac.xlsx")
    _f = X + "protocols-rofan-vac.xlsx"
    ALL["vac"]["links"] = [["הטבלה המסכמת (Excel)", [["צפייה", V(_f)], ["הורדה", _f]]]] + ALL["vac"]["links"]
for _k in ALL["order"]:          # review booklet of all protocols (built by booklet.py)
    if not any(l[0].startswith("חוברת בקרה") for l in ALL[_k]["links"]):
        ALL[_k]["links"] = ALL[_k]["links"] + [["חוברת בקרה של כל הפרוטוקולים (PDF)", [["פתיחה", X + "protocols-rofan-booklet.pdf"]]]]
    _y = X + "protocols-rofan-yoman.xlsx"   # task-log template (static file in assets/), for review
    if not any(l[0].startswith("יומן תיעוד") for l in ALL[_k]["links"]):
        ALL[_k]["links"] = ALL[_k]["links"] + [["יומן תיעוד משימות (Excel)", [["צפייה", V(_y)], ["הורדה", _y]]]]
json.dump(ALL, open(OUT + "data.json", "w"), ensure_ascii=False)
print("ok", {k: len(C.DRUGS) for k, C in CATS.items()})
