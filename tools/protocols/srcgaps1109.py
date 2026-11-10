# Source-based gap fixes (approved by Dr. Assiao 9.11.2026, "מאשר הכל"): high-priority gaps from
#  - SPS Medicines Monitoring (MM261109-1), 16 items
#  - US FDA labels via openFDA (MM261109-3), 18 items + one general check for specialist drugs
#  - Israeli physician leaflets / EMA / FSRH for the 18 previously unsourced drugs (MM261109-5), high + normal priority
# Applied before handover.py, so nest.py turns thr/severe into lab checks. Each added check says which source it rests on.
from extra import dev, mon, contra

D = "9.11.2026"


def C(k, label, det, bad, src):          # contraindication: no renewal, urgent message
    c = contra(k, label, det, bad); c["src"] = src; return c


def V(k, label, det, bad, src, urgent=False):   # deviation: 1-month renewal + message
    c = dev(k, label, det, bad, urgent); c["src"] = src; return c


def M(k, label, det, clinic, src):       # monitoring test: missing -> 1 month + referral to test
    c = mon(k, label, det, clinic); c["src"] = src; return c


SPS, FDA, IL, EMA, FSRH = "SPS", "עלון FDA", "עלון לרופא", "EMA 2014", "FSRH 2022"
QT500 = lambda s: C("qtc500", "QTc אחרון מתחת ל-500", "באק\"ג האחרון QTc מתחת ל-500 msec", "QTc 500 ומעלה", s)
CRCL_DOSE = lambda s: V("crcl_dose", "מינון מותאם לתפקוד הכליות",
                        "קריאטינין מ-12 החודשים האחרונים; בפינוי קריאטינין 30–60 המינון עד חצי מהרגיל, ב-10–30 עד שליש",
                        "מינון לא מותאם לתפקוד הכליות", s)
PRL = lambda s: C("prl_tumor", "אין גידול תלוי פרולקטין", "אין ברשומה פרולקטינומה או סרטן שד", "פרולקטינומה או סרטן שד", s)
LDOPA = lambda s: C("ldopa", "לא בשילוב עם לבודופה או תרופות לפרקינסון", "ברשימת התרופות אין לבודופה או אגוניסט דופמין",
                    "שילוב עם לבודופה / תרופה לפרקינסון", s)
FEVER_CBC = lambda s: V("fever_cbc", "אין חום או כאב גרון לא מוסברים", "בפנייה או ברשומה אין חום, כאב גרון או זיהום לא מוסבר",
                        "חום או כאב גרון — ספירת דם מיידית", s, urgent=True)
SEVLIVER = lambda s: C("sev_liver", "אין מחלת כבד קשה", "אין ברשומה שחמת או מחלת כבד קשה", "מחלת כבד קשה", s)

ADD = {
    # ---- Israeli physician leaflets (previously unsourced) ----
    "Domperidone": [C("domp_heart", "אין מחלת לב או הפרעת אלקטרוליטים",
                      "אין ברשומה אי ספיקת לב, הארכת QT, הפרעת קצב או הפרעה משמעותית באלקטרוליטים", "מחלת לב / הפרעת אלקטרוליטים", IL + " · " + EMA),
                    V("domp_dur", "משך קצר ומינון עד 30 מ\"ג ליום",
                      "הטיפול עד שבוע בדרך כלל, 10 מ\"ג עד 3 פעמים ביום (עד 30 מ\"ג ליום)", "טיפול ממושך או מעל 30 מ\"ג ליום", IL + " · " + EMA),
                    C("domp_liver", "אין פגיעה כבדית בינונית או קשה", "אין ברשומה מחלת כבד בינונית או קשה", "פגיעה כבדית בינונית-קשה", IL)],
    "Sertindole": [C("sert_heart", "אין מחלת לב משמעותית",
                     "אין ברשומה מחלת לב משמעותית, אי ספיקת לב, היפרטרופיה של הלב, הפרעת קצב, או דופק מתחת ל-50", "מחלת לב / דופק מתחת ל-50", IL),
                   M("sert_kmg", "אשלגן ומגנזיום", "אשלגן ומגנזיום בטווח, מ-3 החודשים האחרונים (ובכל הקאות, שלשולים או משתנים מורידי אשלגן)", "בדיקת דם: אשלגן ומגנזיום", IL),
                   SEVLIVER(IL)],
    "Amisulpride": [CRCL_DOSE(IL), PRL(IL), FEVER_CBC(IL)],
    "Sulpiride": [CRCL_DOSE(IL), PRL(IL), FEVER_CBC(IL),
                  V("sulp_bp", "לחץ דם בשנה האחרונה", "לחץ דם מתועד בשנה האחרונה; ביתר לחץ דם — מאוזן", "יתר לחץ דם לא מאוזן", IL)],
    "Clotiapine": [C("clot_seiz", "אין אפילפסיה או סיכון לפרכוס",
                     "אין ברשומה אפילפסיה או פגיעה מוחית", "אפילפסיה / גורם סיכון לפרכוס", IL),
                   C("clot_glauc", "אין גלאוקומה של זווית סגורה", "אין ברשומה גלאוקומה של זווית סגורה", "גלאוקומה של זווית סגורה", IL),
                   V("clot_bp65", "לחץ דם (גיל 65 ומעלה)", "בגיל 65 ומעלה: לחץ דם מתועד ב-6 החודשים האחרונים", "אין מדידת לחץ דם בגיל 65+", IL),
                   FEVER_CBC(IL)],
    "Levomepromazine": [C("levo_heart", "אין מחלת לב קשה", "אין ברשומה מחלת לב איסכמית קשה או אי ספיקת לב (לפי העלון מ-2014)", "מחלת לב קשה", IL + " 2014 (זמני)"),
                        FEVER_CBC(IL)],
    "Nalmefene": [C("nalm_renal", "eGFR 30 ומעלה", "eGFR מ-12 החודשים האחרונים 30 ומעלה", "eGFR מתחת ל-30", IL),
                  SEVLIVER(IL),
                  V("nalm_review", "מעקב התגובה לטיפול", "מעקב תקופתי מתועד (למשל חודשי); מעל שנה — החלטת רופא/ה להמשיך", "אין מעקב / מעל שנה בלי החלטה", IL)],
    "Dienogest": [C("dien_cv", "אין מחלת לב וכלי דם או קרישיות",
                    "אין ברשומה אוטם, שבץ, מחלה איסכמית, פקקת ורידים פעילה או סוכרת עם מעורבות כלי דם", "מחלת לב וכלי דם / קרישיות", IL),
                  C("dien_ca", "אין סרטן תלוי הורמונים", "אין ברשומה סרטן תלוי הורמוני מין או גידול כבד", "סרטן תלוי הורמונים", IL),
                  V("dien_bp", "לחץ דם תקין", "לחץ דם אחרון מתחת ל-140/90", "יתר לחץ דם מתמשך", IL)],
    "Biperiden": [C("antichol_ci", "אין התווית נגד אנטי-כולינרגית",
                    "אין ברשומה גלאוקומה של זווית סגורה לא מטופלת, הגדלת ערמונית, או היצרות / חסימה במערכת העיכול", "התווית נגד", IL)],
    "Procyclidine": [C("antichol_ci", "אין התווית נגד אנטי-כולינרגית",
                       "אין ברשומה גלאוקומה של זווית סגורה או חסימה במערכת העיכול", "התווית נגד", IL)],
    "Betahistine": [C("phaeo", "אין פאוכרומוציטומה", "אין ברשומה פאוכרומוציטומה", "פאוכרומוציטומה", IL)],
    "Mianserin": [SEVLIVER(IL), V("mian_mania", "אין היפומאניה", "בפנייה או ברשומה אין סימני היפומאניה או מאניה", "היפומאניה — הפסקת טיפול", IL, urgent=True)],
    "Reboxetine": [V("rebox_age", "לא בקשישים", "לפי העלון לא מומלץ בקשישים; בגיל 65 ומעלה — החלטת רופא/ה מתועדת", "גיל 65+ בלי החלטה", IL)],
    "Progestogen-only pill": [C("pop_ci", "אין התווית נגד",
                                "אין ברשומה פקקת ורידים פעילה, מחלת כבד קשה, גידול כבד, סרטן תלוי הורמונים, או דימום נרתיקי לא מבורר", "התווית נגד", IL + " · " + FSRH),
                              V("pop_age", "גיל עד 55", "לפי FSRH: עד גיל 55", "גיל מעל 55", FSRH)],
    "Allergen immunotherapy": [V("ait_effect", "יש שיפור אחרי שנה", "אחרי השנה הראשונה יש שיפור מתועד; גיל עד 65", "אין שיפור אחרי שנה / גיל מעל 65", IL),
                               C("ait_immune", "אין מחלה אוטואימונית פעילה או דיכוי חיסוני",
                                 "אין ברשומה מחלה אוטואימונית פעילה, חסר חיסוני, טיפול מדכא חיסון או ממאירות פעילה", "התווית נגד", IL)],
    "Zuclopenthixol": [V("zuc_qt", "אין גורם סיכון ל-QT", "אין ברשומה אשלגן או מגנזיום נמוכים, דופק מתחת ל-50, אוטם טרי או אי ספיקת לב", "גורם סיכון להארכת QT", IL)],

    # ---- SPS (16) ----
    "Apixaban": None, "Rivaroxaban": None, "Dabigatran": None,      # filled below (DOAC)
    "Prednisone (chronic)": None, "Methylprednisolone (chronic)": None,
    "Finasteride": None, "Dutasteride": None, "Dutasteride + Tamsulosin": None,
    "Amiodarone": [M("amio_lytes", "אשלגן, מגנזיום ותפקודי כליות", "מ-6 החודשים האחרונים", "בדיקת דם: אשלגן, מגנזיום, קריאטינין", SPS),
                   V("amio_eye", "בדיקת עיניים", "בדיקת עיניים בשנה האחרונה (ומיידית בכל תסמין ראייה)", "אין בדיקת עיניים בשנה", SPS)],
    "Dronedarone": [M("drone_ecg", "אק\"ג", "אק\"ג מ-6 החודשים האחרונים", "אק\"ג", SPS),
                    M("drone_lft", "תפקודי כבד ואלקטרוליטים", "תפקודי כבד, אשלגן, מגנזיום וקריאטינין מ-6 החודשים האחרונים", "בדיקת דם: תפקודי כבד, אלקטרוליטים", SPS)],
    "Digoxin": [M("dig_camg", "סידן ומגנזיום", "סידן ומגנזיום מהשנה האחרונה", "בדיקת דם: סידן ומגנזיום", SPS)],
    "Lithium carbonate": [V("li_freq", "תדירות בדיקות בקבוצת סיכון",
                            "בגיל 65 ומעלה, רמה 0.8 ומעלה, או פגיעה בכליות או בבלוטת התריס: רמה, כליות ונתרן מ-3 החודשים האחרונים",
                            "קבוצת סיכון בלי בדיקה ב-3 חודשים", SPS),
                          M("li_wt", "משקל", "משקל מתועד בשנה האחרונה", "שקילה", SPS)],
    "Valproate": [M("vpa_wt", "משקל", "משקל מתועד בשנה האחרונה", "שקילה", SPS)],
    "Carbamazepine": [M("cbz_renal", "תפקודי כליות וויטמין D", "קריאטינין וויטמין D מהשנה האחרונה", "בדיקת דם: קריאטינין, ויטמין D", SPS)],
    "Mesalazine (oral)": [M("mesa_renal", "תפקודי כליות", "קריאטינין ו-eGFR מהשנה האחרונה", "בדיקת דם: קריאטינין", SPS)],
    "Doxycycline / minocycline (long course)": [V("mino_6m", "מינוציקלין מעל 6 חודשים",
                                                   "במינוציקלין מעל 6 חודשים: תפקודי כבד מ-3 החודשים האחרונים, ואין פיגמנטציה או סימני זאבת", "חסרות בדיקות במינוציקלין ממושך", SPS)],
    "Donepezil": [M("ache_pulse", "דופק", "דופק מתועד ב-6 החודשים האחרונים", "מדידת דופק", SPS)],
    "Rivastigmine": [M("ache_pulse", "דופק", "דופק מתועד ב-6 החודשים האחרונים", "מדידת דופק", SPS)],
    "Furosemide": [M("furo_6m", "אלקטרוליטים וקריאטינין", "מ-6 החודשים האחרונים", "בדיקת דם: אלקטרוליטים וקריאטינין", SPS)],
    "Alfacalcidol": [M("alfa_ca", "סידן ופוספט", "סידן ופוספט מ-3 החודשים האחרונים", "בדיקת דם: סידן ופוספט", SPS)],
    "Theophylline": [M("theo_lvl", "רמת תאופילין", "רמה מ-12 החודשים האחרונים", "רמת תאופילין", SPS)],

    # ---- openFDA (18) ----
    "Citalopram": [V("cit_ecg", "אק\"ג בסיכון לבבי", "במחלת לב, הפרעת קצב או אלקטרוליטים: אק\"ג מהשנה האחרונה", "סיכון לבבי בלי אק\"ג", FDA), QT500(FDA)],
    "Ziprasidone": [QT500(FDA)],
    "Thioridazine": [QT500(FDA)],
    "Methylphenidate (adults)": None, "Lisdexamfetamine (adults)": None, "Amphetamine salts (adults)": None,
    "Clozapine": [M("cloz_metab", "משקל, סוכר ושומנים", "משקל, סוכר או HbA1c ושומנים מהשנה האחרונה", "בדיקת דם: סוכר ושומנים; שקילה", FDA),
                  V("cloz_anc", "תדירות ספירה", "חודשים 1–6: שבועית; 7–12: כל שבועיים; משנה שנייה: חודשית", "ספירה לא בתדירות הנדרשת", FDA)],
    "Primidone": [M("prim_lab", "ספירת דם וכימיה", "ספירת דם וכימיה מ-6 החודשים האחרונים", "בדיקת דם: ספירה וכימיה", FDA)],
    "Acarbose": [V("acar_lft", "תפקודי כבד בשנה הראשונה", "בשנה הראשונה לטיפול: ALT מ-3 החודשים האחרונים", "שנה ראשונה בלי ALT", FDA)],
    "Desmopressin": [C("ddavp_crcl", "פינוי קריאטינין 50 ומעלה", "פינוי קריאטינין (או eGFR) מהשנה האחרונה 50 ומעלה", "פינוי קריאטינין מתחת ל-50", FDA)],
    "Methyldopa": [M("mdopa_cbc", "ספירת דם", "ספירת דם מהשנה האחרונה (אנמיה המוליטית)", "בדיקת דם: ספירה", FDA)],
    "Amiloride + HCTZ": [V("amil_dm", "אלקטרוליטים בסוכרת או בפגיעה כלייתית", "בסוכרת או קריאטינין מעל 1.5: אלקטרוליטים וקריאטינין מ-3 החודשים האחרונים", "סוכרת / פגיעה כלייתית בלי בדיקה ב-3 חודשים", FDA)],
    "Metoclopramide": [C("meto_12w", "עד 12 שבועות", "הטיפול הרצוף עד 12 שבועות (אזהרת קופסה שחורה)", "מעל 12 שבועות", FDA)],
    "UTI prophylaxis": [V("tmp_cbc", "ספירת דם (טריפרים)", "בטריפרים (TMP-SMX): ספירת דם מהשנה האחרונה", "טריפרים בלי ספירה", FDA)],
    "Urinary alkalinisers": [M("kcit_lab", "אלקטרוליטים, קריאטינין וספירה", "מ-4 החודשים האחרונים", "בדיקת דם: אלקטרוליטים, קריאטינין, ספירה", FDA)],
    "Tamoxifen": [V("tam_gyn", "בדיקה גינקולוגית שנתית", "בדיקה גינקולוגית בשנה האחרונה", "אין בדיקה גינקולוגית בשנה", FDA)],
    "Medroxyprogesterone (depot injection)": [V("dmpa_bmd", "צפיפות עצם בשימוש מעל שנתיים", "מעל שנתיים שימוש: צפיפות עצם מתועדת", "מעל שנתיים בלי צפיפות עצם", FDA)],
    "Fezolinetant": [C("fez_hy", "אין ALT מעל פי 3 עם בילירובין מעל פי 2", "בבדיקה האחרונה אין ALT או AST מעל פי 3 יחד עם בילירובין מעל פי 2", "ALT מעל פי 3 + בילירובין מעל פי 2", FDA),
                     V("fez_sched", "בדיקות כבד בחודשים 1, 2, 3, 6 ו-9", "תפקודי כבד בכל אחד מהמועדים שעברו (חודשים 1, 2, 3, 6, 9)", "חסרה בדיקת כבד במועד", FDA)],
    "Denosumab (osteoporosis)": [V("dmab_ca", "סידן בפגיעה כלייתית קשה", "ב-eGFR מתחת ל-30: סידן שבועי בחודש הראשון אחרי הזריקה, ואז חודשי", "eGFR מתחת ל-30 בלי מעקב סידן", FDA)],
    "Acitretin": [C("acit_tg", "טריגליצרידים מתחת ל-800", "טריגליצרידים אחרונים מתחת ל-800 מ\"ג/ד\"ל (סכנת פנקריאטיטיס)", "טריגליצרידים 800 ומעלה", FDA)],
    "Hepatitis B antivirals": [M("tdf_renal", "תפקודי כליות (טנופוביר)", "בטנופוביר: קריאטינין ו-eGFR מהשנה האחרונה", "בדיקת דם: קריאטינין", FDA)],
    "HIV antiretrovirals": [C("tdf_crcl", "פינוי קריאטינין מספיק (טנופוביר)", "בטנופוביר: ב-PrEP פינוי קריאטינין 60 ומעלה; בשילובים לטיפול 50 ומעלה", "פינוי קריאטינין מתחת לסף", FDA)],
    "Specialist anti-infectives": [V("bdq_qt", "בדאקווילין: אק\"ג", "בבדאקווילין: אק\"ג מהחודש האחרון עם QTc מתחת ל-500", "אין אק\"ג / QTc 500 ומעלה", FDA)],
}

DOAC = [M("doac_lft", "תפקודי כבד", "תפקודי כבד מהשנה האחרונה", "בדיקת דם: תפקודי כבד", SPS),
        V("doac_renal", "תדירות בדיקת כליות",
          "בגיל 75 ומעלה או חולשה: קריאטינין מ-4 החודשים האחרונים; בפינוי קריאטינין מתחת ל-60: כל (פינוי ÷ 10) חודשים, לפי Cockcroft-Gault",
          "בדיקת כליות לא בתדירות הנדרשת", SPS)]
STER = [V("ster_eye", "בדיקת עיניים", "בדיקת עיניים ב-12 החודשים האחרונים", "אין בדיקת עיניים", SPS),
        M("ster_lab", "HbA1c, אשלגן וטריגליצרידים", "HbA1c מ-3 החודשים האחרונים; אשלגן וטריגליצרידים מהשנה האחרונה", "בדיקת דם: HbA1c, אשלגן, טריגליצרידים", SPS)]
PSA = [V("psa", "PSA במעקב", "PSA אחרי 6 חודשי טיפול (בסיס חדש) ומהשנה האחרונה; כל עלייה מהשפל על הטיפול ← לרופא/ה (הערך על הטיפול הוא כחצי)",
         "אין PSA / עלייה ב-PSA", SPS)]
STIM = [M("stim_bp", "לחץ דם ודופק", "לחץ דם ודופק מתועדים בשנה האחרונה", "מדידת לחץ דם ודופק", FDA)]
for g in ("Apixaban", "Rivaroxaban", "Dabigatran"): ADD[g] = DOAC
for g in ("Prednisone (chronic)", "Methylprednisolone (chronic)"): ADD[g] = STER
for g in ("Finasteride", "Dutasteride", "Dutasteride + Tamsulosin"): ADD[g] = PSA
for g in ("Methylphenidate (adults)", "Lisdexamfetamine (adults)", "Amphetamine salts (adults)"): ADD[g] = STIM

ACEARB = ("Enalapril", "Ramipril", "Cilazapril", "Captopril", "Perindopril", "Lisinopril", "Losartan", "Valsartan", "Candesartan",
          "Irbesartan", "Telmisartan", "Olmesartan", "Sacubitril/Valsartan")
DMARD_THR = {"thr": ["WBC מתחת ל-3,500, נויטרופילים מתחת ל-1,600, טסיות מתחת ל-140,000 או MCV מעל 105",
                     "ALT או AST מעל 100", "קריאטינין עלה מעל 30% או eGFR מתחת ל-60", "אלבומין מתחת ל-30"]}
JAK_TB = ("Tofacitinib", "Baricitinib", "Upadacitinib", "Biologic drugs")


def apply(lists):
    by = {d["generic"]: d for L in lists for d in L}
    n = 0
    for g, cs in ADD.items():
        d = by[g]
        have = {c["k"] for c in d["checks"]}
        for c in cs:
            if c["k"] not in have:
                d["checks"].append(dict(c)); n += 1
    # domperidone: heart disease is now a contraindication (leaflet + EMA), so the old "ECG in heart disease, then renew" check goes
    by["Domperidone"]["checks"] = [c for c in by["Domperidone"]["checks"] if c["k"] != "ecg"]
    # statins: CK >5x ULN (SPS), ALT >3x stop
    for d in by.values():
        if d["generic"].split(" +")[0] in ("Atorvastatin", "Rosuvastatin", "Simvastatin", "Pravastatin", "Fluvastatin"):
            d["severe"] = ["CPK מעל פי 5 מהגבול העליון", "ALT מעל פי 3 מהגבול העליון"]
            d["thr"] = [t for t in d.get("thr", []) if not t.startswith("ALT")]
    # ACEi/ARB: Na <132 to the doctor (SPS); heart failure every 3–6 months
    for g in ACEARB:
        for d in [x for x in by.values() if x["generic"] == g or x["generic"].startswith(g + " +")]:
            if "Na מתחת ל-132" not in d.get("thr", []): d["thr"] = list(d.get("thr", [])) + ["Na מתחת ל-132"]
            if "hf_freq" not in {c["k"] for c in d["checks"]}:
                d["checks"].append(V("hf_freq", "אי ספיקת לב: בדיקות כל 3–6 חודשים", "באי ספיקת לב: אשלגן וקריאטינין מ-6 החודשים האחרונים",
                                     "אי ספיקת לב בלי בדיקה ב-6 חודשים", SPS)); n += 1
    # Furosemide: K below 3 to the doctor
    by["Furosemide"]["thr"] = list(by["Furosemide"].get("thr", [])) + ["K מתחת ל-3"]
    # DMARDs: absolute SPS thresholds; leflunomide / azathioprine every 2–3 months
    for g in ("Methotrexate (oral)", "Leflunomide", "Sulfasalazine", "Azathioprine", "Mycophenolate"):
        by[g]["thr"] = list(DMARD_THR["thr"])
        by[g]["checks"].append(M("dmard_freq", "בדיקות בתדירות SPS", "ספירה, תפקודי כבד, קריאטינין ואלבומין מ-3 החודשים האחרונים; אלבומין מתחת ל-30 ← לרופא/ה",
                                  "בדיקת דם: ספירה, כבד, כליות, אלבומין", SPS)); n += 1
    # specialist drugs: tests asked for in the specialist letter done on time (openFDA review); TB during biologics / JAK
    for d in by.values():
        ks = {c["k"] for c in d["checks"]}
        if ("spec" in ks or "follow" in ks) and "speclabs" not in ks:
            d["checks"].append(V("speclabs", "בדיקות המעקב שבמכתב המומחה בוצעו",
                                 "הבדיקות שהמומחה ביקש במכתב האחרון (דם, אק\"ג, אקו, עיניים ועוד) בוצעו בזמן", "חסרה בדיקת מעקב שהמומחה ביקש", FDA)); n += 1
    for g in JAK_TB:
        if "tb" not in {c["k"] for c in by[g]["checks"]}:
            by[g]["checks"].append(V("tb", "בדיקת שחפת במהלך הטיפול", "בדיקת שחפת (TB) לפי הנחיית המומחה, ואין תסמיני שחפת", "אין בדיקת TB / תסמינים", FDA)); n += 1
    for d in by.values():
        if any(c.get("src") in (SPS, FDA) or str(c.get("src", "")).startswith((IL, EMA, FSRH)) for c in d["checks"]):
            d["why"] = (d.get("why") or "") + f" בדיקות שנוספו לפי מקור (SPS / עלון FDA / עלון לרופא) — אושר {D}."
    # no drug-combination checks anywhere in the tool (decision 10.11.2026): the clinic system's interaction alert covers them.
    # The general "no interaction alert in the system" check (k="inter", added by handover) stays.
    COMBO_K = {"combo"}
    def is_combo(t):
        t = t.strip()
        return t.startswith("שילוב") or t.startswith("NSAIDs באופן קבוע") or t.startswith("תרופה חדשה ברשימה (אינטראקציות")
    for d in by.values():
        d["checks"] = [c for c in d["checks"] if c["k"] not in COMBO_K]
        for f in ("excl", "excl_x"):
            if isinstance(d.get(f), list):
                d[f] = [x for x in d[f] if not (isinstance(x, str) and is_combo(x))]
        for c in d["checks"]:
            if c["k"] == "excl" and isinstance(c.get("det"), str):
                parts = [x for x in c["det"].split("; ") if not is_combo(x)]
                c["det"] = "; ".join(parts)
                if isinstance(c.get("crit"), str) and parts:
                    c["crit"] = c["det"] + c["crit"][c["crit"].find(". "):] if ". " in c["crit"] else c["crit"]
        d["checks"] = [c for c in d["checks"] if not (c["k"] == "excl" and not c.get("det"))]
    return n
