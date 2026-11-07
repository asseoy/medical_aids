# Decisions from the Kiryat Ono handover-booklet review (3.11.2026), applied to every drug that has a checklist.
#  - consecutive renewals: up to 3 (was 4); on the 3rd, a patient message recommending a yearly family-physician visit
#  - no clinic visit in 12 months: 1 month + booking, and also a message to the physician
#  - every renewal: quantity / units / frequency check, and an interaction-alert check; either one -> wait for the physician
RENEW = dict(k="renew", label="רצף חידושים", det="פחות מ-3 חידושים רצופים מאז ביקור אצל רופא/ה",
             doc="פחות מ-3 חידושים רצופים מאז הביקור האחרון אצל רופא/ה.", opt=False,
             crit="מאז הביקור האחרון אצל רופא/ה בוצעו פחות מ-3 חידושים רצופים ע\"י רפואן. 3 ומעלה ← ביקור רופא/ה לפני החידוש הבא.",
             bad="3 חידושים רצופים ללא ביקור רופא/ה")
THIRD = dict(k="third", label="החידוש השלישי ברצף", q="זה החידוש השלישי ברצף מאז ביקור אצל רופא/ה?",
             det="נשלחת למטופל/ת המלצה על ביקורת שנתית", doc="החידוש השלישי ברצף: נשלחה המלצה על ביקורת.", opt=True,
             crit="בחידוש השלישי ברצף: הודעה למטופל/ת \"מומלצת ביקורת אצל רופא/ת משפחה לפחות פעם בשנה\".",
             pat="מומלצת ביקורת אצל רופא/ת משפחה לפחות פעם בשנה")
QTY = dict(k="qty", label="כמות, יחידות ותדירות", det="כמות (OP), יחידות (mg או mcg) ותדירות (יומית, שבועית, חודשית) תואמות למרשם הקודם",
           doc="כמות, יחידות ותדירות תואמות למרשם הקודם.", opt=False, wait=True, bad="אי-התאמה בכמות, ביחידות או בתדירות",
           crit="לוודא כמות (2OP = 2 אריזות), יחידות (mg מול mcg) ותדירות (מתוטרקסט, אוזמפיק ואלנדרונט — פעם בשבוע). אי-התאמה ← לא מחדשים עד תשובת הרופא/ה.")
INTER = dict(k="inter", label="אין התראת אינטראקציה", det="בהפקת המרשם לא הופיעה התראת אינטראקציה (גם לא בין תרופות ותיקות)",
             doc="לא הופיעה התראת אינטראקציה.", opt=False, wait=True, bad="התראת אינטראקציה",
             crit="כל התראת אינטראקציה, גם בין תרופות שניתנות זמן רב ← החידוש ממתין לתשובת הרופא/ה.")
VISIT_NOTIFY = "אין ביקור במרפאה ב-12 החודשים האחרונים"


def apply(*drug_lists):
    for drugs in drug_lists:
        for d in drugs:
            ch = d.get("checks") or []
            if not ch:
                continue
            for c in ch:
                if c["k"] == "visit":
                    c["notify"] = VISIT_NOTIFY
            i = next((n for n, c in enumerate(ch) if c["k"] == "renew"), None)
            new = [dict(QTY), dict(INTER)]
            if i is not None:
                ch[i:i + 1] = new + [dict(RENEW), dict(THIRD)]
            else:
                ch.extend(new)

# General working instructions, shown in the tool (panel above the tabs) and in the booklet.
RESULTS_WARNING = ("תוצאות בדיקה שקופצות בפתיחת התיק: לא ללחוץ \"אשר\" — לחיצה עליו רושמת שהרופא/ה עבר/ה על התוצאות. "
                   "ללחוץ רק \"הפסק וסגור\", להשוות לבדיקות קודמות ולדווח לרופא/ה.")
GUIDE = [
    ("סדר עבודה", ["משימות מזכירה קודם, לסיים באותו יום. פניות דיגיטליות תוך 8 ימים: אישורים, תרופות, ואז השאר.",
                   "לפני סגירת משימת מזכירה: לרשום את מספר תעודת הזהות."]),
    ("תוצאות בדיקות", [RESULTS_WARNING, "לא עונים למטופל/ת על תוצאות."]),
    ("מרשמים", ["לבדוק כמות (OP = אריזות), יחידות (mg/mcg) ותדירות.",
                "התראת אינטראקציה, מרשם בכתב יד, אישור תרופה או הסרה מהקבועות: לרופא/ה.",
                "תרופה שלא נמצאת בכלי: לחפש ב-UpToDate התוויות נגד ובדיקות מעקב, להשוות לתוצאות המטופל/ת ולהעביר סיכום קצר לרופא/ה. הרופא/ה מחליט/ה."]),
    ("בדיקות והפניות", ["רק שגרה, מעקב קיים או המלצה כתובה. תסמין או בקשה חדשה: לרופא/ה. מוקד או מיון: מיד."]),
    ("לדווח לרופא/ה", ["אשפוז, פטירה במשפחה, אבחנה חדשה, או מטופל/ת שפונה שוב ושוב."]),
]
