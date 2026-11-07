# One-by-one review of the 59 physician-only items (7.11.2026, Dr. Assiao): nothing stays blocked by default.
#  - red  (suit "הכנה" + red=True): the assistant prepares, the physician double-checks before approval ("דגל אדום")
#  - regular (suit "בתנאים", or "הכנה" for non-chronic courses): the assistant works through the checklist
#  - doctor (suit "לא"): unchanged, message only
# The interaction check of the prescribing system is the base safeguard; an item gets a red flag only where the
# protocol adds a safeguard of its own. Quantity / interaction / consecutive-renewal checks are added by handover.py.
import copy
from extra import BUY, VISIT, RENEW, cond, dev, mon

SRC = "סקירת פריטים חסומים, החלטה מקומית (7.11.2026)"
COND = "טיפול כרוני במינון קבוע שנקבע ע\"י מומחה/ית"


def spec(who, k="spec"):
    return dev(k, f"הנחיה עדכנית של {who}", f"מכתב או סיכום של {who} מ-12 החודשים האחרונים, עם אותה תרופה ומינון",
               f"אין הנחיה עדכנית של {who}")


def follow(who, k="follow"):
    return dev(k, f"מעקב מסודר אצל {who}", f"ביקור אצל {who} בתקופה שנקבעה במעקב, ואין פער במעקב", f"אין מעקב מסודר אצל {who}")


def chronic(extra, c=COND):
    return [dict(BUY), dict(VISIT), cond(c)] + list(extra) + [dict(RENEW)]


def red(why, checks, labs="-"):
    return dict(suit="הכנה", red=True, why=why, checks=checks, labs=labs, src=SRC, doctitle="הכנת מרשם לאישור הרופא/ה (דגל אדום)")


def regular(why, checks, labs="-"):
    return dict(suit="בתנאים", red=False, why=why, checks=checks, labs=labs, src=SRC)


# ---- batch 1: heart, endocrine, respiratory, neurology -------------------------------------------------------
DECISIONS = {
    "Cardiology specialist drugs": red(
        "טפמידיס ומבקמטן נקבעים ע\"י קרדיולוג/ית מומחה/ית. הרפואן מכין עם המכתב העדכני, והרופא/ה בודק/ת שוב לפני האישור.",
        chronic([spec("הקרדיולוג/ית")])),
    "Low-molecular-weight heparins": red(
        "נוגד קרישה בזריקה: מינון לפי משקל ותפקוד כליות, ומשך לפי ההתוויה. הרפואן מרכז את המדדים ואת סיבת הטיפול, והרופא/ה מאשר/ת.",
        chronic([mon("weight", "משקל עדכני", "משקל מתועד מ-3 החודשים האחרונים", "שקילה במרפאה"),
                 mon("renal", "תפקוד כליות", "קראטינין ו-eGFR מ-3 החודשים האחרונים", "בדיקת דם: קראטינין"),
                 mon("cbc", "ספירת דם", "ספירת דם עם טסיות מ-3 החודשים האחרונים", "בדיקת דם: ספירה"),
                 dev("indic", "סיבת הטיפול ומשכו המתוכנן", "במסמכים הרפואיים מתועדות ההתוויה (למשל אחרי ניתוח, פקקת, היריון) ומשך הטיפול שנקבע, והמשך לא עבר",
                     "אין סיבה או משך מתועדים, או שמשך הטיפול עבר")],
                c="טיפול שנקבע במסמך רפואי, באותו מינון"),
        labs="משקל, קראטינין ו-eGFR, ספירת דם — מ-3 החודשים האחרונים"),
    "Growth hormone": red(
        "הורמון גדילה נקבע ומנוטר ע\"י אנדוקרינולוג/ית (לרוב ילדים). הרפואן מכין עם ההנחיה העדכנית, והרופא/ה מאשר/ת.",
        chronic([spec("האנדוקרינולוג/ית")])),
    "Phentermine": red(
        "פנטרמין (רזין) הוא ממריץ במרשם מיוחד, לטווח קצר. הרפואן מכין עם משקל, לחץ דם ומשך הטיפול עד כה, והרופא/ה מאשר/ת.",
        [mon("weight", "משקל עדכני", "משקל מתועד מהחודש האחרון", "שקילה במרפאה"),
         mon("bp", "לחץ דם ודופק", "מדידת לחץ דם ודופק מהחודש האחרון", "מדידת לחץ דם במרפאה"),
         dev("dur", "משך הטיפול עד כה", "תאריך תחילת הטיפול ומספר החודשים מאז מתועדים בסיכום לרופא/ה", "משך הטיפול לא ידוע"),
         dict(VISIT), dict(RENEW)],
        labs="משקל, לחץ דם ודופק מהחודש האחרון"),
    "Somatostatin analogues / pegvisomant": red(
        "אנלוגים לסומטוסטטין ופגויזומנט נקבעים ע\"י אנדוקרינולוג/ית או אונקולוג/ית. הרפואן מכין עם המכתב העדכני, והרופא/ה מאשר/ת.",
        chronic([spec("המומחה/ית המטפל/ת")])),
    "Pulmonary hypertension / IPF drugs": red(
        "תרופות ליל\"ד ריאתי ולפיברוזיס ריאתי נקבעות במרכז מומחה. בוסנטן (טרקליר) טרטוגני ומחייב תפקודי כבד חודשיים. "
        "הרפואן מכין, והרופא/ה מאשר/ת.",
        chronic([spec("מרכז המומחה"),
                 mon("lft", "תפקודי כבד (בבוסנטן ובאמבריסנטן)", "ALT ו-AST מהחודש האחרון בבוסנטן; לפי ההנחיה בשאר התרופות", "בדיקת דם: תפקודי כבד"),
                 dev("preg", "אין היריון (בבוסנטן, אמבריסנטן, מאסיטנטן)", "באישה בגיל הפוריות: אמצעי מניעה מתועד ואין היריון", "היריון או אין אמצעי מניעה")]),
        labs="בוסנטן: ALT ו-AST חודשיים"),
    "Cystic fibrosis modulators": regular(
        "מווסתי CFTR נקבעים ע\"י מרכז CF. חידוש כשיש מעקב מסודר ותפקודי כבד בטווח.",
        chronic([follow("מרכז ה-CF"),
                 mon("lft", "תפקודי כבד", "ALT ו-AST מ-6 החודשים האחרונים (שנה ראשונה: כל 3 חודשים)", "בדיקת דם: תפקודי כבד")]),
        labs="ALT ו-AST כל 3–6 חודשים"),
    "Allergen immunotherapy": regular(
        "אקריזקס: המנה הראשונה ניתנת בהשגחת אלרגולוג/ית. בחידוש — אסתמה מאוזנת ואין תגובה קשה.",
        chronic([follow("האלרגולוג/ית"),
                 dev("asthma", "אסתמה מאוזנת", "אין התקף אסתמה, קורס סטרואידים או פנייה למיון בחודשים האחרונים", "אסתמה לא מאוזנת"),
                 dev("react", "אין תגובה קשה", "אין נפיחות בגרון, קשיי בליעה או נשימה, או פריחה כללית מאז תחילת הטיפול", "תגובה קשה — לרופא/ה", urgent=True)],
                c="טיפול שהתחיל אצל אלרגולוג/ית, אותו מינון")),
    "Specialist movement-disorder drugs": regular(
        "אפומורפין, טטרבנזין ודומיהן נקבעים ע\"י נוירולוג/ית מומחה/ית. חידוש לפי ההנחיה העדכנית.",
        chronic([spec("הנוירולוג/ית")])),
    "Specialist epilepsy drugs": regular(
        "תרופות אפילפסיה של מרכז מומחה (רופינאמיד, סולטיאם, קנבידיול, פנפלורמין). חידוש לפי ההנחיה העדכנית.",
        chronic([spec("הנוירולוג/ית")])),
    "Narcolepsy drugs": regular(
        "פיטוליסנט וסולריאמפטול נקבעים ע\"י מרפאת שינה. חידוש לפי ההנחיה העדכנית.",
        chronic([spec("מרפאת השינה")])),
}

# Multiple sclerosis: drugs that need routine blood tests get a red flag; glatiramer (Copaxone) is regular.
MS_RED = red(
    "תרופות לטרשת נפוצה שמחייבות בדיקות דם (לימפוציטים, ספירה, תפקודי כבד) — נקבעות ע\"י מרכז MS. הרפואן מכין עם הבדיקות, והרופא/ה מאשר/ת.",
    chronic([spec("מרכז ה-MS"),
             mon("cbc", "ספירת דם ולימפוציטים", "ספירת דם מלאה מ-6 החודשים האחרונים", "בדיקת דם: ספירה"),
             mon("lft", "תפקודי כבד", "ALT ו-AST מ-6 החודשים האחרונים", "בדיקת דם: תפקודי כבד")]),
    labs="ספירת דם, לימפוציטים ותפקודי כבד — כל 6 חודשים או לפי ההנחיה")
MS_REG = regular("קופקסון (גלטירמר) לטרשת נפוצה, נקבע ע\"י מרכז MS ואינו מחייב בדיקות דם שגרתיות. חידוש לפי ההנחיה העדכנית.",
                 chronic([spec("מרכז ה-MS")]))


def _set(d, upd):
    d.pop("only", None)
    d.update(copy.deepcopy(upd))


def apply(lists):
    allp = [d for L in lists for d in L]
    by = {d["generic"]: d for d in allp}
    for g, upd in DECISIONS.items():
        assert g in by, "review1107: no entry " + g
        assert by[g]["suit"] == "לא", "review1107: not physician-only " + g
        _set(by[g], upd)
    # split MS: Copaxone becomes its own regular entry
    for L in lists:
        for i, d in enumerate(L):
            if d["generic"] == "Multiple sclerosis drugs":
                cop = copy.deepcopy(d)
                cop.update(generic="Glatiramer (MS)", he="גלטירמר לטרשת נפוצה (קופקסון)",
                           brands=[b for b in d["brands"] if "copaxone" in b["en"].lower() or "glatiramer" in b["en"].lower()], tab="neuro")
                cop.pop("mixed", None)
                d["brands"] = [b for b in d["brands"] if b not in cop["brands"]]
                _set(d, MS_RED); _set(cop, MS_REG)
                L.insert(i + 1, cop)
                return
    raise AssertionError("review1107: no MS entry")
