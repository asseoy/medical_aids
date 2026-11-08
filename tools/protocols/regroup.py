# Regroup all drugs by body system (decision 2.11.2026). The source protocols (HTN, DM, ...) stay as the place where
# drugs are defined; this module only decides which tab each drug is shown in, and builds each tab's rules, shared
# checks, decisions and guideline list from the source protocols that contribute drugs to it.
import re
from types import SimpleNamespace as NS

PREFIX = {"htn": "יל\"ד", "dm": "סוכרת", "resp": "נשימה", "neuro": "נוירו", "misc": "כללי", "tdm": "מעקב"}

CATS = [  # key, tab name, example search, Excel name
    ("cardio", "לב וכלי דם", "לוטן", "לב_וכלי_דם"),
    ("endo", "סוכרת ואנדוקרינולוגיה", "גלוקומין", "סוכרת_ואנדוקרינולוגיה"),
    ("resp", "נשימה ואלרגיה", "סימביקורט", "נשימה_ואלרגיה"),
    ("neuro", "נוירולוגיה", "קפרה", "נוירולוגיה"),
    ("psych", "פסיכיאטריה", "ציפרלקס", "פסיכיאטריה"),
    ("gi", "עיכול וכבד", "לוסק", "עיכול_וכבד"),
    ("renal", "כליות ודרכי שתן", "טמסולין", "כליות_ודרכי_שתן"),
    ("women", "בריאות האישה", "יסמין", "בריאות_האישה"),
    ("msk", "שלד, מפרקים וכאב", "אלוריל", "שלד_מפרקים_וכאב"),
    ("blood", "דם וויטמינים", "תרדיפרון", "דם_וויטמינים"),
    ("eyeskin", "עיניים ועור", "קסאלטן", "עיניים_ועור"),
    ("immune", "חיסון, זיהומים ומומחים", "חומירה", "חיסון_זיהומים_ומומחים"),
    ("nonchronic", "תרופות שאינן כרוניות", "ארקוקסיה", "תרופות_שאינן_כרוניות"),
]

# explicit placement of drugs from the mixed protocols (misc, tdm, neuro); htn/dm/resp go whole to one tab
G = {
    "cardio": """Atorvastatin|Rosuvastatin|Simvastatin|Pravastatin|Ezetimibe|Atorvastatin + Ezetimibe|Rosuvastatin + Ezetimibe|Evolocumab|Alirocumab|
        Aspirin (low dose)|Clopidogrel|Bezafibrate|Ticagrelor|Prasugrel|Isosorbide mononitrate|Flecainide|Propafenone|Dronedarone|Inclisiran|Midodrine|
        Pentoxifylline|Dipyridamole|Cardiology specialist drugs|Bempedoic acid|Omega-3 / icosapent ethyl|Ciprofibrate|Vericiguat|Nitroglycerin (sublingual)|
        Low-molecular-weight heparins|Digoxin|Amiodarone|Warfarin|Apixaban|Rivaroxaban|Dabigatran""",
    "endo": """Levothyroxine|Hydrocortisone (replacement)|Alfacalcidol|Cinacalcet|Cabergoline|Desmopressin|Growth hormone|Orlistat|Phentermine|
        Somatostatin analogues / pegvisomant|Methimazole|Propylthiouracil|Testosterone|Prednisone (chronic)|Methylprednisolone (chronic)""",
    "resp": """Antihistamines (2nd generation)|Pulmonary hypertension / IPF drugs|Cystic fibrosis modulators""",
    "psych": """Escitalopram|Citalopram|Sertraline|Fluoxetine|Paroxetine|Venlafaxine|Duloxetine|Methylphenidate (adults)|Methylphenidate (children)|Lisdexamfetamine (adults)|Lisdexamfetamine (children)|Benzodiazepines / Z-drugs|
        Amphetamine salts (adults)|Amphetamine salts (children)|Modafinil / armodafinil|Lithium carbonate|Clozapine|Mirtazapine|Trazodone|Bupropion|Vortioxetine|Fluvoxamine|Amitriptyline|Nortriptyline|
        Clomipramine|Atomoxetine|Guanfacine|Varenicline|Melatonin|Mianserin|Maprotiline|Doxepin|Buspirone|Daridorexant|Lemborexant|Milnacipran|Reboxetine""",
    "neuro": """Gabapentin|Pregabalin|Multiple sclerosis drugs|Cinnarizine|Betahistine|Carbamazepine|Valproate""",
    "gi": """Omeprazole|Esomeprazole|Lansoprazole|Pantoprazole|Dexlansoprazole|Mesalazine (oral)|Budesonide (oral)|Ursodeoxycholic acid|Lactulose|Famotidine|
        Pancreatin|Rifaximin|Domperidone|Metoclopramide|Mebeverine|Prucalopride|Laxatives|Hepatitis B antivirals|Hepatitis C / D antivirals|Other specialist drugs""",
    "renal": """Tamsulosin|Alfuzosin|Dutasteride|Dutasteride + Tamsulosin|Terazosin|Finasteride|Solifenacin|Tolterodine|Fesoterodine|Trospium|Oxybutynin|
        Mirabegron|Sildenafil|Tadalafil|Vardenafil|Erythropoiesis-stimulating agents|Phosphate binders|Potassium binders|CKD bone-mineral drugs|
        Sodium bicarbonate (tablets)|UTI prophylaxis|Nitrofurantoin (prophylaxis)""",
    "women": """Estradiol (systemic)|Estradiol + dydrogesterone|Estradiol + norethisterone|Estradiol + drospirenone|Estradiol + norgestrel|
        Progesterone / progestogens (oral)|Estradiol (vaginal)|Combined hormonal contraception|Progestogen-only pill|Dienogest|Fezolinetant|Elinzanetant|
        Conjugated estrogens + bazedoxifene|Prasterone (vaginal)|Medroxyprogesterone (depot injection)""",
    "msk": """Allopurinol|Febuxostat|Alendronate|Risedronate|Raloxifene|Opioids|Zoledronic acid (osteoporosis)|Paracetamol / dipyrone (chronic)|
        Osteoanabolic (specialist)|Methotrexate (oral)|Leflunomide|Sulfasalazine|Tofacitinib|Baricitinib|Upadacitinib|Hydroxychloroquine|Colchicine (chronic)|
        Denosumab (osteoporosis)|Teriparatide|Apremilast""",
    "blood": """Iron (oral)|Vitamin B12|Folic acid|Calcium (oral)|Vitamin D|Haematology specialist drugs|Hydroxyurea""",
    "eyeskin": """Itraconazole|Isotretinoin|Acitretin|Prostaglandin analogue (eye drops)|Timolol (eye drops)|
        Carbonic anhydrase inhibitor (eye drops)|Brimonidine (eye drops)|Glaucoma combination with timolol|Doxycycline / minocycline (long course)""",
    "nonchronic": """NSAIDs (strong, prescription)|Terbinafine (oral)|Drug not on the chronic list|Steroid eye drops|Topical steroids""",
    "immune": """Letrozole|Anastrozole|Exemestane|Tamoxifen|HIV antiretrovirals|Calcineurin inhibitors|Biologic drugs|Oral oncology and hormonal cancer therapy|
        Transplant immunosuppressants (mTOR)|Valaciclovir / aciclovir (suppression)|Rare metabolic / orphan drugs|Azathioprine|Mycophenolate""",
}
PLACE = {g.strip(): k for k, s in G.items() for g in s.split("|")}
PSY_CLS = ("נוגד פסיכוזה",)
WHOLE = {"htn": "cardio", "dm": "endo", "resp": "resp"}


def place(src, d):
    g = d["generic"]
    if d.get("tab"):
        return d["tab"]
    if g in PLACE:
        return PLACE[g]
    if src in WHOLE:
        return WHOLE[src]
    if src == "tdm" and d["cls"].startswith(PSY_CLS):
        return "psych"
    if src == "neuro":
        return "neuro"
    raise KeyError(f"no tab for {src}:{g}")


BASE_RULES = [
    "חידוש רגיל: 3 חודשים",
    "ביקור במרפאה אצל רופא/ת המשפחה פעם בשנה",
    "עד 3 חידושים רצופים, ואז ביקור רופא",
    "אין התווית נגד ← תמיד מחדשים לפחות לחודש אחד",
    "חסרה מדידה, בדיקה או ביקורת שנתית: חידוש לחודש אחד + זימון למרפאה",
    "חריגה מספי ההחזרה: חידוש לחודש אחד + הודעה לרופא/ה",
    "התווית נגד או ערך חמור: לא מחדשים, הודעה לרופא/ה (הסף של כל תרופה מופיע ברשימה שלה)",
    "רפואן לא משנה מינון ולא מחליף תרופה. \"מעקב צמוד\" = תרופה עם מעקב תכוף (מעבדה, אק\"ג, עיניים או צילום) — לבדוק כל ערך בקפידה",
]
EXTRA_RULES = {
    "cardio": ["ערך חמור ביל\"ד: K ≥5.5; באלדקטון K ≥5.0; eGFR <30 ב-ACEi, ARB ו-MRA; דופק <50 בתרופות מאטות דופק (חוסמי בטא, ורפמיל, דילטיאזם, דיגוקסין, אמיודרון). תיאזיד בלבד עם eGFR <30: חודש + הודעה",
               "תרופות עם כמה התוויות (ACEi/ARB בודדים, MRA, אנטרסטו, פוסיד, חוסמי בטא): בלי יעד ל\"ד; טווח בטיחות סיסטולי 90 עד מתחת ל-160/100; מתחת ל-90 או תסמין ← לרופא/ה",
               "נוגדי קרישה ונוגדי טסיות לא נעצרים ע\"י רפואן מלבד ערך חמור; דימום ← הודעה דחופה"],
    "endo": ["ערך חמור בסוכרת: מטפורמין eGFR <30; גליבנקלמיד וגלימפיריד eGFR <60; סולפונילאוריאה אחרת eGFR <15; פיוגליטזון ALT מעל פי 2.5. מטפורמין עם eGFR 30–45 ומינון מעל 1,000 מ\"ג ליום ← הודעה",
             "אינסולין בטיפול קבוע וכל הבדיקות תקינות: 3 חודשים. כל חריגה ← חודש באותו מינון + הודעה; אינסולין לא נעצר ע\"י רפואן",
             "פורקסיגה, ג'רדיאנס, אוזמפיק/וגובי ומונג'רו (כמה התוויות): בלי HbA1c; יעד הטיפול נבדק ע\"י הרופא/ה",
             "לבותירוקסין, הידרוקורטיזון וסטרואידים לא נעצרים ע\"י רפואן: כל חריגה ← חודש + הודעה"],
    "resp": ["3 משאפי הרגעה ומעלה בשנה או התקף ב-12 החודשים האחרונים: חודש + הודעה",
             "LABA או LAMA-LABA בלי סטרואיד אצל מטופל/ת עם אסתמה: חודש + הודעה דחופה",
             "משאף הרגעה לפי הצורך: לא בודקים כיסוי רכישות, אלא כמות משאפים בשנה"],
    "neuro": ["נוגדי פרכוסים, תרופות לפרקינסון, בקלופן וגואנפצין לא נעצרים ע\"י רפואן: כל חריגה ← חודש + הודעה",
              "פריחה בלמוטריגין, התנהגות כפייתית או החמרה במיאסתניה ← הודעה דחופה",
              "טריפטנים לפי הצורך: 10 ימי טיפול ומעלה בחודש ← הודעה"],
    "psych": ["מחשבות אובדניות או החמרה נפשית ← הודעה דחופה",
              "קלוזפין: חידוש לחודש אחד בלבד, לפי ספירת דם",
              "ממריצים, בנזודיאזפינים ותרופות שינה Z: חידוש ע\"י רופא/ה בלבד",
              "נוגדי פסיכוזה: מעקב מטבולי שנתי; לא נעצרים ע\"י רפואן מלבד ערך חמור"],
    "gi": ["מעכבי משאבת פרוטונים: נדרשת התוויה מתועדת לטיפול ממושך",
           "דם בצואה, ירידה במשקל או שינוי חדש ביציאות ← הודעה לרופא/ה"],
    "renal": ["מעכבי PDE5: ניטרטים = התווית נגד",
              "אנטי-כולינרגיים לשלפוחית: גיל 75+ ← אישור רופא/ה; אצירת שתן ← דחוף",
              "תרופות לאי-ספיקת כליות מתקדמת (ESA, קושרים): חידוש ע\"י רופא/ה בלבד"],
    "women": ["דימום וגינלי לא סדיר ← הודעה דחופה",
              "אסטרוגן מערכתי כשיש רחם: חייב פרוגסטוגן",
              "אמצעי מניעה משולב: עישון בגיל 35+, מיגרנה עם הילה או פקקת בעבר = התווית נגד"],
    "msk": ["ביספוספונט: eGFR <35 = ערך חמור; 5 שנות טיפול ← הודעה",
            "אופיואידים: חידוש ע\"י רופא/ה בלבד",
            "NSAID ממושך: כליות, אשלגן, ל\"ד, דימום והגנת קיבה",
            "מתוטרקסט ו-DMARD: ספירת דם ותפקודי כבד לפי התרופה; חום או זיהום ← דחוף"],
    "blood": ["ברזל מעל 6 חודשים בלי התוויה מתועדת ← הודעה"],
    "eyeskin": ["טיפות לגלאוקומה: ביקורת שנתית אצל רופא/ת עיניים; טימולול: דופק ואסתמה",
                "רואקוטן ואציטרטין: רופא/ת עור בלבד",
                "נוגדי פטרת וטטרציקלינים: רק בתוך משך הקורס"],
    "nonchronic": ["כל בקשה בלשונית זו מוכנה ע\"י הרפואן ומאושרת ע\"י הרופא/ה. לא מפיקים באופן עצמאי",
                   "מתחת לגיל 18 ← לרופא/ה (מינון לפי משקל)",
                   "הרפואן לא שואל שאלות רפואיות חדשות: בודק רשומה ופנייה. סימן אזהרה בפנייה ← הודעה דחופה לרופא/ה",
                   "תכשיר עם ריכוז אחר, אריזה גדולה או בקשה חוזרת תכופה ← לרופא/ה",
                   "בקשה להמרת מרשם שנכתב בכתב יד: מציגים לרופא/ה לפענוח. לא מפענחים ולא מקלידים לבד.",
                   "הסיכום לרופא/ה: איפה תועד, תאריך, שם הרופא/ה ותפקידו/ה, האבחנה וההמלצה",
                   "נוגדי דלקת חזקים: לבדוק כיב קיבה בעבר ותפקוד כליות. טרבינפין: ALT לפני ואחרי חודש",
                   "משחה סטרואידלית: לא לשימוש כרוני; כשמאושרת — ההוראה הקבועה נכנסת להודעה למטופל/ת"],
    "immune": ["רוב התרופות כאן מחודשות ע\"י רופא/ה או מומחה/ית בלבד",
               "חום או זיהום בתרופה מדכאת חיסון ← הודעה דחופה"],
}


def _fix_ref(text, src):
    return re.sub(r"החלט(ה|ות) (\d+(?:-\d+)?)", lambda m: "החלט" + m.group(1) + " " + PREFIX[src] + "-" + m.group(2), str(text))


STOP = {"טיפול", "כרוני", "ממושך", "(טיפול", "teva", "טבע", "tablets", "oral", "chronic", "מניעה", "(מניעה)", "long", "term", "drugs", "תרופות", "specialist", "מומחה", "בבליעה", "זריקה", "מדבקה"}


def regroup(sources):
    """sources: dict src_key -> module (with DRUGS, COMMON, DECISIONS, GUIDE, VERSION, VERIFY)."""
    cats = {k: NS(key=k, NAME=n, example=ex, xname=xn, DRUGS=[], srcs=[]) for k, n, ex, xn in CATS}
    for src, M in sources.items():
        for d in M.DRUGS:
            k = place(src, d)
            d["src"] = _fix_ref(d.get("src", ""), src)
            d["srcp"] = src
            if src == "tdm":
                d["tdm"] = True
            cats[k].DRUGS.append(d)
            if src not in cats[k].srcs:
                cats[k].srcs.append(src)
    for k, C in cats.items():
        # the non-chronic tab is not a renewal: chronic renewal rules and shared renewal rows do not apply
        C.RENEW_RULES = EXTRA_RULES.get(k, []) if k == "nonchronic" else BASE_RULES + EXTRA_RULES.get(k, [])
        seen, C.COMMON = set(), []
        for s in C.srcs:
            for row in sources[s].COMMON:
                row = tuple(_fix_ref(x, s) for x in row)
                if row[1:4] not in seen:
                    seen.add(row[1:4]); C.COMMON.append(row)
        C.DECISIONS = [(PREFIX[s] + "-" + str(d[0]),) + tuple(d[1:]) for s in C.srcs for d in sources[s].DECISIONS]
        # keep only shared rows and decisions that concern this tab's drugs (a tab gets drugs from several source protocols)
        toks = set()
        for d in C.DRUGS:
            for t in [d["he"], d["generic"]] + [b["he"] for b in d["brands"]]:
                for w in re.split(r"[\s/()·,+\-]+", str(t)):
                    if len(w) >= 4 and w.lower() not in STOP: toks.add(w.lower())
        GEN = re.compile("^(רכישות|ביקורת שנתית|רצף חידושים)$")
        rel = lambda txt: any(t in txt.lower() for t in toks)
        whole = {s for s in C.srcs if s in WHOLE and WHOLE[s] == k}     # source protocol that lives entirely in this tab
        C.DECISIONS = [d for d in C.DECISIONS if d[0].split("-")[0] in {PREFIX[s] for s in whole} or rel(" ".join(map(str, d[1:4]))) or GEN.search(str(d[1]))]
        whole_rows = [tuple(_fix_ref(x, s) for x in row) for s in whole for row in sources[s].COMMON]
        keep, seen_t = [], set()
        for r in C.COMMON:
            if GEN.search(str(r[1])):
                if r[1] in seen_t or k == "nonchronic": continue
                seen_t.add(r[1]); keep.append(r)
            elif rel(" ".join(map(str, r[1:5]))) or r in whole_rows:
                keep.append(r)
        C.COMMON = keep
        C.GUIDE = "; ".join(dict.fromkeys(sources[s].GUIDE for s in C.srcs))
        C.VERSION = "גרסה 2 · חלוקה לפי מערכות · 2.11.2026"
        C.VERIFY = "לאימות מול מאגר משרד הבריאות"
    return cats
