# Handover-booklet decisions, part B (3.11.2026): stimulants, opioids, benzodiazepines.
#  - stimulants: renewable by the assistant when on the chronic list, 3 months (future prescriptions); separate child and adult
#    entries; children also need weight, height, pulse and BP every 6 months
#  - opioids: the assistant checks the pain diagnosis and the interval, then the physician gives final approval ("הכנה")
#  - benzodiazepines / Z-drugs: physician decides; the assistant collects the facts first ("הכנה")
#  - addictive drugs: about 3 months since the last prescription (early request -> wait for the physician)
import copy
from extra import mon, dev, contra, cond, BUY, VISIT, RENEW, excl_item

INTERVAL = dict(k="interval", label="עברו כ-3 חודשים מהמרשם הקודם", det="לפי הרכישות והמרשם האחרון: אין בקשה מוקדמת ואין רכישות עודפות",
                doc="עברו כ-3 חודשים מהמרשם הקודם.", opt=False, wait=True, bad="בקשה מוקדמת או רכישות עודפות",
                crit="תרופה עם פוטנציאל התמכרות: בקשה לפני שעברו כ-3 חודשים, או רכישות מעבר לכמות שנרשמה ← החידוש ממתין לתשובת הרופא/ה.")
CHRONIC = dict(cond("התרופה רשומה בתרופות הקבועות ונרשמה בעבר ע\"י רופא/ה"), label="רשומה בתרופות הקבועות", bad="לא רשומה בתרופות הקבועות")
DX = dev("dx", "אבחנה מתועדת ומצורפת למרשם", "אבחנת ADHD (או נרקולפסיה) ברשימת האבחנות, ומצורפת למרשם (\"ADD במעקב שלי\")",
         "אין אבחנה מתועדת או לא מצורפת למרשם")
FIRST = dev("first", "מרשם ראשון ע\"י המומחה המתאים", "אטנט, אדרל או ויואנס: המרשם הראשון ניתן ע\"י נוירולוג/ית או פסיכיאטר/ית. מעבר מריטלין לאטנט — רק בהמלצת מומחה",
            "אין מרשם ראשון או המלצה של מומחה")
KID = [mon("growth", "משקל וגובה מתועדים", "משקל וגובה מ-6 החודשים האחרונים (עקומת גדילה)", "מדידת משקל וגובה"),
       mon("bp", "דופק ול\"ד מתועדים", "דופק ול\"ד מ-6 החודשים האחרונים", "מדידת דופק ול\"ד"),
       dev("gr_ok", "אין ירידה במשקל או האטה בגדילה", "המשקל לא ירד והגדילה לא הואטה לעומת המדידה הקודמת", "ירידה במשקל או האטה בגדילה")]
ADHD_COMP = [("ירידה בתיאבון ובמשקל", "לרופא"), ("דפיקות לב, כאב בחזה או עילפון", "דחוף"), ("מחשבות אובדניות או שינוי חד במצב הרוח", "דחוף")]


def stim_pair(d, generic, he, extra_first):
    base = dict(cls="ADHD · ממריץ (סם מסוכן)", brands=d["brands"], suit="בתנאים", labs="ילדים: משקל, גובה, דופק ול\"ד כל 6 חודשים",
                thr=["אין ערך מעבדה ייעודי"], severe=[], excl=[], comp=ADHD_COMP, src="החלטה מקומית (3.11.2026); NICE NG87 (מעקב בילדים)",
                cond="רשומה בתרופות הקבועות", maxm=None)
    common = [CHRONIC, DX] + ([FIRST] if extra_first else []) + [INTERVAL, dict(BUY), dict(VISIT), dict(RENEW)]
    why = "סם מסוכן: מחודש ע\"י רפואן רק כשרשום בתרופות הקבועות, עם אבחנה מצורפת למרשם. אפשר ל-3 חודשים (מרשמים עתידיים)."
    adult = dict(base, generic=generic + " (adults)", he=he + " (מבוגרים)", why=why, checks=copy.deepcopy(common))
    child = dict(base, generic=generic + " (children)", he=he + " (ילדים ובני נוער)", why=why + " בילדים גם משקל, גובה, דופק ול\"ד כל 6 חודשים.",
                 checks=copy.deepcopy([CHRONIC, DX] + ([FIRST] if extra_first else []) + KID + [INTERVAL, dict(BUY), dict(VISIT), dict(RENEW)]))
    return [adult, child]


def apply(misc):
    out = []
    for d in misc.DRUGS:
        g = d["generic"]
        if g == "Methylphenidate":
            out += stim_pair(d, "Methylphenidate", "מתילפנידאט", False)
        elif g == "Lisdexamfetamine":
            out += stim_pair(d, "Lisdexamfetamine", "ליסדקסאמפטמין", True)
        elif g == "Amphetamine salts / modafinil":
            amph = [b for b in d["brands"] if b["en"].lower().startswith("attent")]
            moda = [b for b in d["brands"] if b not in amph]
            out += stim_pair(dict(d, brands=amph), "Amphetamine salts", "מלחי אמפטמין", True)
            out.append(dict(d, generic="Modafinil / armodafinil", he="מודפיניל / ארמודפיניל", cls="תרופות ערנות", brands=moda,
                            only="מודפיניל וארמודפיניל לערנות (נרקולפסיה) במרשם מיוחד. חידוש ע\"י רופא/ה בלבד.",
                            why="מודפיניל וארמודפיניל לערנות (נרקולפסיה) במרשם מיוחד. חידוש ע\"י רופא/ה בלבד."))
        elif g == "Opioids":
            out.append(dict(d, suit="הכנה", only=None, labs="-", thr=["-"], src="החלטה מקומית (3.11.2026)",
                            why="אופיואיד: הרפואן בודק אבחנת כאב, התאמה לתרופה ומרווח זמן, ומכין סיכום. האישור הסופי בידי הרופא/ה.",
                            checks=[dev("pain", "אבחנת כאב מתועדת", "אבחנת כאב ברשימת האבחנות הקבועות או בביקור האחרון", "אין אבחנת כאב מתועדת"),
                                    dev("match", "האבחנה מתאימה לתרופה", "האבחנה מצדיקה את האופיואיד ואת המינון (למשל כאב סרטני, כאב גב כרוני)", "האבחנה לא מתאימה לתרופה"),
                                    dev("attach", "האבחנה מצורפת למרשם", "אבחנת הכאב מצורפת למרשם עצמו", "האבחנה לא מצורפת למרשם"),
                                    INTERVAL, dict(BUY), dict(VISIT)],
                            comp=[("ישנוניות, בלבול או נשימה איטית", "דחוף"), ("עצירות קשה", "לרופא"), ("בקשה מוקדמת או אובדן מרשם", "לרופא")]))
        elif g == "Benzodiazepines / Z-drugs":
            out.append(dict(d, suit="הכנה", only=None, labs="-", thr=["-"], src="ספר חפיפה עוזרי רופא; החלטה מקומית (3.11.2026)",
                            why="ההחלטה בידי הרופא/ה. הרפואן אוסף את הנתונים, מסמן אותם ומעביר סיכום.",
                            checks=[dev("dur", "משך הנטילה ורציפות תועדו", "כמה זמן נוטל/ת ואם ברצף — לפי הרכישות והרשומה", "משך או רציפות לא ידועים"),
                                    dev("freq", "השימוש לא נעשה תכוף יותר", "לפי הרכישות: אין עלייה בתדירות לאחרונה", "השימוש נעשה תכוף יותר"),
                                    dev("talk", "תיעוד שיחה על שינה או חרדה", "ברשומה יש שיחה על הרגלי שינה, ניסיון טיפול אחר או הפניה למעבדת שינה (ומתי)", "אין תיעוד שיחה על הרגלי שינה"),
                                    INTERVAL, dict(VISIT)],
                            comp=[("נפילות או בלבול (בגיל מבוגר)", "לרופא"), ("בקשה מוקדמת או אובדן מרשם", "לרופא")]))
        else:
            out.append(d)
    misc.DRUGS[:] = out
