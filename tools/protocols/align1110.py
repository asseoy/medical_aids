# Decision 10.11.2026: where the protocol was stricter (or looser) than the guideline, follow the guideline.
# Applied after srcgaps1109 and before handover/nest, so thr/severe edits become the lab checks.
SPS = "SPS Medicines Monitoring"


def _drug(lists, generic):
    for L in lists:
        for d in L:
            if d.get("generic") == generic:
                return d
    return None


def _check(d, k):
    return next((c for c in d["checks"] if c.get("k") == k), None)


def _set(c, det, label=None, crit=None, clinic=None):
    c["det"] = det
    if label:
        c["label"] = label
    c["doc"] = c.get("label", "") + ": " + det + "."
    if crit:
        c["crit"] = crit
    if clinic:
        c["clinic"] = clinic


def _no_level(d):
    d["thr"] = [t for t in d.get("thr", []) if not t.startswith("רמה")]
    d["severe"] = [t for t in d.get("severe", []) if not t.startswith("רמה")]


def _lvl_if(rng, toxic=None):
    det = "אם נבדקה רמה (בחשד לרעילות, אי-היענות או אינטראקציה): בטווח " + rng
    crit = "רמה שגרתית לא נדרשת (SPS). אם נבדקה: מחוץ לטווח ← חידוש לחודש + הודעה לרופא/ה" + (
        "; " + toxic + " ← לא מחדשים, הודעה לרופא/ה." if toxic else ".")
    return dict(k="lvl_if", label="רמה (רק אם נבדקה)", det=det, doc="רמה (רק אם נבדקה): " + det + ".", crit=crit, opt=True,
                q="נבדקה רמת התרופה בשנה האחרונה?", bad="רמה מחוץ לטווח")


def apply(lists):
    n = 0
    # Digoxin: no routine level; Ca, creatinine, Mg, K, U&E yearly (SPS)
    d = _drug(lists, "Digoxin")
    if d:
        _no_level(d)
        d["checks"] = [c for c in d["checks"] if c.get("k") != "level"]
        d["checks"].insert(0, _lvl_if("עד 1.2 ng/mL", "2.0 ng/mL ומעלה"))
        c = _check(d, "annual")
        _set(c, "מ-12 החודשים האחרונים: אשלגן, קריאטינין/eGFR ואלקטרוליטים", label="בדיקות שנתיות")
        d["labs"] = "אשלגן, קריאטינין, סידן ומגנזיום שנתי; רמת דיגוקסין רק בחשד לרעילות, תרופה מתקשרת, הרעה בכליות או שינוי מינון (SPS)"
        d["src"] = "מעקב: " + SPS
        n += 1
    # Carbamazepine / valproate: no routine level (SPS)
    d = _drug(lists, "Carbamazepine")
    if d:
        _no_level(d)
        _set(_check(d, "level"), "נתרן, ספירת דם, ALT וכליות מ-12 החודשים האחרונים", label="בדיקות מתועדות")
        d["checks"].insert(1, _lvl_if("4-12 mg/L"))
        d["labs"] = "נתרן, ספירת דם, ALT, כליות וויטמין D תקופתי; רמה רק בחשד לאי-היענות, רעילות או אינטראקציה (SPS)"
        n += 1
    d = _drug(lists, "Valproate")
    if d:
        _no_level(d)
        _set(_check(d, "level"), "ALT, ספירת דם ומשקל מ-12 החודשים האחרונים", label="בדיקות מתועדות")
        d["checks"].insert(1, _lvl_if("50-100 mg/L"))
        d["labs"] = "ALT, ספירת דם ומשקל שנתי; רמה רק בחשד לאי-היענות, רעילות או אינטראקציה (SPS)"
        n += 1
    # Phenytoin: no routine level (SPS)
    d = _drug(lists, "Phenytoin")
    if d:
        _no_level(d)
        c = _check(d, "level")
        if c:
            _set(c, "ALT וקריאטינין מ-12 החודשים האחרונים", label="בדיקות מתועדות")
        d["checks"].insert(1, _lvl_if("10-20 mg/L", "מעל 25"))
        d["labs"] = "כליות, ALT וויטמין D תקופתי; רמה רק בחשד לאי-היענות, רעילות או אינטראקציה (SPS)"
        n += 1
    # Vitamin B12: do not repeat the level on treatment (NICE NG239)
    d = _drug(lists, "Vitamin B12")
    if d:
        d["checks"] = [c for c in d["checks"] if c.get("k") not in ("level", "lvl")]
        d["labs"] = "אין בדיקת רמה שגרתית בטיפול; מעקב לפי תסמינים (NICE NG239)"
        d["src"] = "מעקב: NICE NG239 (2024)"
        n += 1
    # NOACs: yearly; age ≥75 / frail every 4 months; CrCl ≤60 every CrCl/10 months (EHRA 2021) — already in doac_renal
    for g in ("Apixaban", "Rivaroxaban", "Dabigatran", "Edoxaban"):
        d = _drug(lists, g)
        if d:
            c = _check(d, "annual")
            if c:
                _set(c, "מ-12 החודשים האחרונים (בגיל 75+, חולשה או eGFR ≤60 — לפי הבדיקה הבאה)")
            d["labs"] = "המוגלובין, כליות וכבד שנתי; גיל 75+ או חולשה — כל 4 חודשים; eGFR ≤60 — כל (eGFR/10) חודשים (EHRA 2021)"
            n += 1
    # Dronedarone: ECG at least every 6 months (MHRA) — drone_ecg already 6 months
    d = _drug(lists, "Dronedarone")
    if d:
        c = _check(d, "level")
        if c:
            _set(c, "ALT וקריאטינין/eGFR מ-6 החודשים האחרונים")
        d["labs"] = "תפקודי כבד וקריאטינין כל 6 חודשים (חודשי בחצי השנה הראשונה); אק\"ג לפחות כל 6 חודשים (MHRA)"
        n += 1
    # Amiodarone: ECG yearly; no routine chest X-ray; eye exam only with visual symptoms (SPS)
    d = _drug(lists, "Amiodarone")
    if d:
        c = _check(d, "annual")
        if c:
            _set(c, "אק\"ג מ-12 החודשים האחרונים", label="אק\"ג שנתי", clinic="אק\"ג")
        c = _check(d, "amio_eye")
        if c:
            c.update(opt=True, q="יש תסמין ראייה חדש?")
            _set(c, "אין תסמין ראייה חדש (בדיקת עיניים רק בתסמינים; אופטומטריסט שנתי מומלץ)", label="אין תסמין ראייה",
                 crit="תסמין ראייה ← הפניה לבדיקת עיניים והודעה לרופא/ה.")
            c.pop("clinic", None)
        d["labs"] = "תפקודי כבד, TSH, אשלגן, מגנזיום וכליות כל 6 חודשים; אק\"ג שנתי; בדיקת עיניים רק בתסמינים (SPS)"
        n += 1
    # Long-term azithromycin: LFTs every 6 months; ECG at baseline and 1 month (BTS 2020)
    for g in ("Azithromycin (long-term)",):
        d = _drug(lists, g)
        if d:
            c = _check(d, "level")
            if c:
                _set(c, "ALT מ-6 החודשים האחרונים; אק\"ג מתועד מתחילת הטיפול (בסיס ואחרי חודש)")
            d["labs"] = "תפקודי כבד אחרי חודש ואז כל 6 חודשים; אק\"ג לפני ואחרי חודש, וחוזר עם תרופה חדשה שמאריכה QT (BTS 2020)"
            n += 1
    return n
