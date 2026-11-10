# Minimal physician-instructions log (10.11.2026): one row per request, eight columns, mostly dropdowns.
# Purpose: document the physician's instruction to the student, and allow later audit by patient ID and date.
# The details of what was done are in the medical record (documentation line) and the same-day screenshots.
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

S = os.path.dirname(os.path.abspath(__file__)) + "/"
REPO = os.path.abspath(S + "../..") + "/"
F = "Arial"
HEAD = ["תאריך", "ת״ז מטופל/ת", "רופא/ה", "רפואן", "סוג הבקשה", "הוראת הרופא/ה", "חזר לרופא/ה", "החלטת הרופא/ה (רק כשחזר)"]
WID = [12, 14, 14, 14, 18, 30, 18, 40]
TYPES = ["תרופות", "אישור", "פנייה מקוונת", "חיסון", "סיכום רפואי", "בקשה משולבת", "אחר"]
ORDERS = ["לבצע לפי הפרוטוקול", "להכין לאישור הרופא/ה", "לא לבצע — הרופא/ה מטפל/ת", "אחר (לפרט בהחלטה)"]
BACK = ["לא", "חריגה (כתום)", "דגל אדום", "כתום + אדום", "שאלה אחרת"]
DOCS = ["ד״ר ________"]
STUD = ["________"]


def run(out=REPO + "protocols-rofan-yoman-lite.xlsx"):
    wb = Workbook()
    ws = wb.active; ws.title = "יומן"; ws.sheet_view.rightToLeft = True
    thin = Side(style="thin", color="C9D3D1")
    hfill = PatternFill("solid", fgColor="13233D"); pick = PatternFill("solid", fgColor="E3EBF6")
    for i, (h, w) in enumerate(zip(HEAD, WID), 1):
        c = ws.cell(1, i, h); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = hfill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"
    N = 1000
    ws.auto_filter.ref = f"A1:H{N}"
    # example row (to delete)
    import datetime; ex = [datetime.date(2026, 11, 11), "000000000", DOCS[0], STUD[0], "בקשה משולבת", ORDERS[0], BACK[1], "K 5.8 — לחדש לחודש, לחזור על בדיקה בעוד שבוע"]
    for i, v in enumerate(ex, 1):
        c = ws.cell(2, i, v); c.font = Font(name=F, italic=True, color="5B6A72")
    for r in range(2, N + 1):
        for i in range(1, 9):
            c = ws.cell(r, i); c.border = Border(bottom=thin)
            if r > 2: c.font = Font(name=F)
            c.alignment = Alignment(vertical="top", wrap_text=(i == 8))
            if i in (3, 4, 5, 6, 7): c.fill = pick
        ws.cell(r, 1).number_format = "dd/mm/yyyy"
        ws.cell(r, 2).number_format = "@"
    # lists
    L = wb.create_sheet("רשימות"); L.sheet_view.rightToLeft = True
    cols = [("רופאים", DOCS), ("רפואנים", STUD), ("סוג הבקשה", TYPES), ("הוראת הרופא/ה", ORDERS), ("חזר לרופא/ה", BACK)]
    for j, (h, vals) in enumerate(cols, 1):
        c = L.cell(1, j, h); c.font = Font(name=F, bold=True)
        L.column_dimensions[c.column_letter].width = 26
        for k, v in enumerate(vals, 2): L.cell(k, j, v).font = Font(name=F)
    for j, col in zip((3, 4, 5, 6, 7), "ABCDE"):
        dv = DataValidation(type="list", formula1=f"='רשימות'!${col}$2:${col}$40", allow_blank=True, showErrorMessage=False)
        ws.add_data_validation(dv); dv.add(f"{ws.cell(2, j).column_letter}2:{ws.cell(2, j).column_letter}{N}")
    # legend
    G = wb.create_sheet("הסבר"); G.sheet_view.rightToLeft = True; G.column_dimensions["A"].width = 100
    rows = [("מטרת היומן", True),
            ("לתעד את הוראת הרופא/ה לסטודנט/ית לכל בקשה, ולאפשר בקרה לפי ת״ז ותאריך. פרטי הביצוע נמצאים בתיק (שורת התיעוד) ובצילומי המסך.", False),
            ("", False), ("איך ממלאים (שורה לכל בקשה, גם בקשה משולבת)", True),
            ("• תאריך: Ctrl + ; מכניס את התאריך של היום. ת״ז: 9 ספרות.", False),
            ("• העמודות בתכלת נבחרות מרשימה (Alt + ↓). מותר גם להקליד ערך חופשי.", False),
            ("• \"חזר לרופא/ה\": לא — הבקשה בוצעה כפי שהורה הרופא/ה. כתום — חריגה מהפרוטוקול. אדום — תרופה בסיכון גבוה. שאלה אחרת — כל ספק.", False),
            ("• \"החלטת הרופא/ה\": רק כשהבקשה חזרה לרופא/ה. במשפט אחד.", False),
            ("• השורה האפורה היא דוגמה — למחוק לפני שימוש. את שמות הרופאים והרפואנים מעדכנים בגיליון \"רשימות\".", False),
            ("", False), ("בקרה", True),
            ("• החץ בכותרת: סינון לפי ת״ז, תאריך, רופא/ה, רפואן או \"חזר לרופא/ה\". Ctrl+F: חיפוש ת״ז.", False),
            ("• היומן נשמר רק במערכות מכבי (תיקייה ארגונית), לא במחשב פרטי ולא בוואטסאפ.", False)]
    for k, (t, b) in enumerate(rows, 1):
        c = G.cell(k, 1, t); c.font = Font(name=F, bold=b, size=12 if b else 11); c.alignment = Alignment(wrap_text=True)
    wb.save(out)
    return out


if __name__ == "__main__":
    print(run())
