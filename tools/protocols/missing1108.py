# Registry gap batch (8.11.2026, approved 1–18 by Dr. Assiao): drugs in the Israeli registry that were missing from the tool.
# New entries get their decision here (same helpers as review1107); approved brands join existing group entries.
import copy
from extra import B, dev, mon, BUY, VISIT, RENEW, cond
from otc import O, N, checks as nc_checks, cat
from review1107 import chronic, spec, follow, regular, red

SRC = "פער מול הרג'יסטרי, החלטה מקומית (8.11.2026)"


def prep(why, checks, labs="-"):
    return dict(suit="הכנה", red=False, why=why, checks=checks, labs=labs, src=SRC, doctitle="הכנת מרשם לאישור הרופא/ה")


def entry(generic, he, cls, brands, tab, decision, comp=()):
    d = dict(generic=generic, he=he, cls=cls, brands=brands, thr=["-"], severe=[], excl=[], comp=list(comp), tab=tab)
    d.update(decision)
    d["src"] = SRC
    return d


NEW = [
    # 1 — glucagon rescue kit
    entry("Glucagon (rescue kit)", "גלוקגון — ערכת חירום להיפוגליקמיה (גלוקגן היפוקיט)", "סוכרת · ערכת חירום",
          [B("GlucaGen HypoKit", "גלוקגן היפוקיט")], "endo",
          regular("ערכת חירום להיפוגליקמיה קשה. מחדשים למטופל/ת באינסולין או בסולפונילאוריאה, כשהערכה הקודמת נוצלה או שפג תוקפה. "
                  "שימוש בערכה = היפוגליקמיה קשה: הרופא/ה צריך/ה לדעת.",
                  [dict(VISIT),
                   dev("ins", "טיפול באינסולין או בסולפונילאוריאה", "ברשימת התרופות יש אינסולין או סולפונילאוריאה", "אין טיפול שמצדיק ערכת גלוקגון"),
                   dev("why", "הערכה הקודמת נוצלה או שפג תוקפה", "בפנייה: הערכה נוצלה, פג תוקפה, או שזו ערכה ראשונה שהרופא/ה המליץ/ה עליה",
                       "בקשה לערכה נוספת בלי שימוש ובלי פקיעת תוקף"),
                   dev("hypo", "אם הערכה נוצלה: האירוע דווח לרופא/ה", "אם הערכה נוצלה — הרופא/ה יודע/ת על אירוע ההיפוגליקמיה",
                       "שימוש בגלוקגון (היפוגליקמיה קשה) שלא דווח לרופא/ה", urgent=True)]),
          comp=[("היפוגליקמיה קשה, אובדן הכרה או פרכוס", "דחוף — מד\"א 101")]),
    # 3 — buccal midazolam
    entry("Midazolam buccal (seizure rescue)", "מידזולם לחלל הפה להפסקת פרכוס (בוקולאם)", "נוירולוגיה · תרופת הצלה",
          [B("Buccolam", "בוקולאם")], "neuro",
          prep("תרופת הצלה בפרכוס ממושך, לפי תוכנית של הנוירולוג/ית. בנזודיאזפין — הרפואן מכין, הרופא/ה מאשר/ת.",
               [dict(VISIT), spec("הנוירולוג/ית"),
                dev("use", "מספר השימושים מאז המרשם הקודם מתועד", "בפנייה או ברשומה: כמה פעמים נעשה שימוש ומתי",
                    "שימוש תכוף בתרופת ההצלה או פרכוסים חוזרים")]),
          comp=[("פרכוס שלא נעצר 5 דקות אחרי המנה, או קושי בנשימה", "דחוף — מד\"א 101")]),
    # 5 — fertility drugs
    entry("Fertility drugs (IVF)", "תרופות לטיפולי פוריות (גונל-אף, מנופור, צטרוטייד, אוביטרל)", "פוריות · מומחה",
          [B("Gonal-F", "גונאל-אף"), B("Ovaleap", "אובליפ"), B("Pergoveris", "פרגובריס"), B("Puregon", "פיורגון"), B("Menopur", "מנופור"),
           B("Elonva", "אלונבה"), B("Cetrotide", "צטרוטייד"), B("Orgalutran", "אורגלוטרן"), B("Ovitrelle", "אוביטרל")], "women",
          prep("תרופות הזרקה לטיפולי פוריות, לפי פרוטוקול של יחידת הפוריות (IVF) למחזור הנוכחי. הרפואן מכין לפי הפרוטוקול, הרופא/ה מאשר/ת.",
               [dev("ivf", "פרוטוקול עדכני מיחידת הפוריות", "מכתב או פרוטוקול מיחידת הפוריות למחזור הנוכחי, עם התרופות והמינונים",
                    "אין פרוטוקול עדכני ליחידת הפוריות"),
                dev("approv", "אישור מימון בתוקף", "אישור לטיפולי פוריות (סל או ביטוח) בתוקף למחזור הנוכחי", "אין אישור מימון בתוקף")]),
          comp=[("כאב בטן חזק, נפיחות בבטן או קוצר נשימה (גירוי יתר של השחלות)", "דחוף — יחידת הפוריות או מיון נשים")]),
    # 6 — terpene preparations
    O("Terpene preparations (urinary / biliary)", "תכשירי טרפנים לאבנים בדרכי השתן ובדרכי המרה (רווהטינקס, רווהכול)",
      cat("כליות ודרכי מרה"), [B("Rowatinex", "רווהטינקס", "דרכי השתן"), B("Rowachol", "רווהכול", "דרכי המרה")],
      "תכשירי צמחים (טרפנים) כתוספת בטיפול באבנים. לא מחליפים בירור של כאב, חום או דם בשתן.",
      nc_checks("עד חודש", "אין חום, כאב חזק בצד או בבטן, צהבת או הקאות",
                [N("dx", "אבחנה מתועדת של אבנים", "ברשומה יש אבחנה של אבנים בדרכי השתן או המרה", "אין אבחנה מתועדת — לרופא/ה")]),
      "לפי ההוראות שבעלון. חום, כאב חזק בצד או בבטן, צהבת או הקאות — לפנות לרופא/ה או למוקד.",
      comp=[("חום עם כאב בצד או צמרמורות", "דחוף — מוקד או מיון"), ("צהבת או כאב בטן חזק", "דחוף")], src=SRC),
    # 7 — tibolone (checks copied from systemic estradiol in apply())
    entry("Tibolone", "טיבולון (ליויאל)", "טיפול הורמונלי במנופאוזה · טיבולון", [B("Livial", "ליויאל", "לא בסל")], "women",
          regular("טיבולון לתסמיני גיל המעבר: אותן בדיקות כמו בטיפול הורמונלי (ממוגרפיה, ל\"ד, דימום). לא נותנים פרוגסטוגן בנוסף.", [])),
    # 8 — xanomeline-trospium
    entry("Xanomeline-trospium", "קסנומלין-טרוספיום (קובנפי)", "נוגד פסיכוזה · מוסקריני", [B("Cobenfy", "קובנפי", "לא בסל")], "psych",
          prep("נוגד פסיכוזה חדש, נקבע ע\"י פסיכיאטר/ית. אצירת שתן ועליית אנזימי כבד; לא במחלת כבד. הרפואן מכין, הרופא/ה מאשר/ת.",
               chronic([spec("הפסיכיאטר/ית"),
                        mon("lft", "תפקודי כבד", "ALT, AST ובילירובין מ-6 החודשים האחרונים", "בדיקת דם: תפקודי כבד"),
                        dev("ret", "אין אצירת שתן", "ברשומה או בפנייה אין קושי במתן שתן או אצירת שתן", "אצירת שתן")],
                       c="נקבע ע\"י פסיכיאטר/ית, אותו מינון ב-3 החודשים האחרונים"),
               labs="תפקודי כבד"),
          comp=[("קושי במתן שתן", "לרופא"), ("צהבת או שתן כהה", "דחוף")]),
    # 9 — alprostadil injection
    entry("Alprostadil (intracavernosal)", "אלפרוסטדיל בזריקה לפין (קברג'קט)", "אורולוגיה · אין-אונות", [B("Caverject", "קאברג'קט", "לא בסל")],
          "renal",
          prep("זריקה לפין לאין-אונות, אחרי הדרכה של אורולוג/ית. הרפואן מכין, הרופא/ה מאשר/ת.",
               [dict(VISIT), spec("האורולוג/ית"),
                dev("priap", "אין זקפה ממושכת מדווחת", "ברשומה או בפנייה אין זקפה שנמשכה מעל 4 שעות", "זקפה ממושכת בעבר")]),
          comp=[("זקפה מעל 4 שעות", "דחוף — מיון")]),
    # 16 — bethanechol
    entry("Bethanechol", "בתנכול (מיוכולין)", "אורולוגיה · אצירת שתן", [B("Myocholine-Glenwood", "מיוכולין גלנווד", "לא בסל")], "renal",
          regular("כולינרגי לאצירת שתן. התוויות נגד: אסתמה, דופק איטי, כיב פעיל, חסימה במערכת השתן או העיכול.",
                  chronic([dev("contra", "אין התווית נגד", "ברשומה אין אסתמה, דופק איטי, כיב פעיל, או חסימה במערכת השתן או העיכול",
                               "התווית נגד ברשומה")])),
          comp=[("קוצר נשימה או צפצופים", "לרופא"), ("סחרחורת או עילפון", "לרופא")]),
]

BRANDS = {
    "Multiple sclerosis drugs": [B("Fampyra", "פמפירה", "פמפרידין"), B("Fampridine S.K.", "פמפרידין אס.קיי."), B("Fampridine Teva", "פמפרידין טבע")],
    "Rare metabolic / orphan drugs": [B("Firazyr", "פירזיר", "אנגיואדמה תורשתית"), B("Icatibant Teva", "איקטיבנט טבע", "אנגיואדמה תורשתית"),
                                      B("Takhzyro", "טאקזירו", "אנגיואדמה תורשתית"), B("Berinert", "ברינרט", "אנגיואדמה תורשתית"),
                                      B("Andembry", "אנדמברי", "אנגיואדמה תורשתית"),
                                      B("Crysvita", "קריסויטה"), B("Voxzogo", "ווקסוגו"), B("Livmarli", "ליבמרלי"), B("Givlaari", "גיבלרי"),
                                      B("Yorvipath", "יורביפאט"), B("Agamree", "אגאמרי"), B("Strensiq", "סטרנסיק"), B("Increlex", "אינקרלקס")],
    "Biologic drugs": [B("Kineret", "קינרט"), B("Ilaris", "אילאריס"), B("Vyvgart", "ויוגרט", "מיאסטניה גרביס"),
                       B("Enspryng", "אנספרינג", "NMOSD"), B("Imaavy", "אימאווי", "מיאסטניה גרביס")],
    "Cystic fibrosis modulators": [B("Pulmozyme", "פולמוזיים", "בשאיפה"), B("Cayston", "קאיסטון", "אזטראונם בשאיפה")],
    "Pulmonary hypertension / IPF drugs": [B("Winrevair", "וינרוור")],
    "Haematology specialist drugs": [B("Nplate", "אנפלייט"), B("Besremi", "בסרמי"), B("Reblozyl", "רבלוזיל")],
    "Methotrexate (oral)": [B("Metoject", "מטוג'קט", "זריקה תת-עורית"), B("Metoject Pen", "מטוג'קט עט", "זריקה תת-עורית")],
    "Cough preparations": [B("Oxacatin", "אוקסקטין", "לא בסל")],
}


def apply(lists):
    allp = [d for L in lists for d in L]
    by = {d["generic"]: d for d in allp}
    for g, bs in BRANDS.items():
        d = by[g]   # KeyError = entry renamed
        have = {b["en"].lower() for b in d["brands"]}
        for b in bs:
            if b["en"].lower() not in have:
                d["brands"].append(b); have.add(b["en"].lower())
    mtx = by["Methotrexate (oral)"]
    mtx["he"] = "מתוטרקסט (בבליעה ובזריקה)"
    mtx["why"] = mtx.get("why", "") + " מטוג'קט: אותן בדיקות, זריקה תת-עורית פעם בשבוע."
    new = copy.deepcopy(NEW)
    tib = next(d for d in new if d["generic"] == "Tibolone")
    est = by["Estradiol (systemic)"]
    tib["checks"] = [copy.deepcopy(c) for c in est["checks"] if "פרוגסטוגן" not in c.get("label", "")]
    for k in ("cond", "excl", "excl_x"):
        if k in est: tib[k] = copy.deepcopy(est[k])
    for d in new:
        if d["suit"] == "בתנאים" and "cond" not in d:
            d["cond"] = "טיפול כרוני במינון קבוע"
    lists[-1].extend(new)
