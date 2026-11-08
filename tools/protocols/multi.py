# Drugs with several indications (decision 2.11.2026: "generic checklist only").
# The checklist keeps only checks that hold for every indication; indication-specific targets (BP target, HbA1c)
# are left to the physician at the annual visit.
from extra import mon, dev

NOTE = "תרופה עם כמה התוויות: נבדקים רק תנאים משותפים לכל ההתוויות. יעד הטיפול (ל\"ד, HbA1c, משקל) נבדק ע\"י הרופא/ה בביקורת. "
BB = {"Bisoprolol": "יל\"ד, אי-ספיקת לב, פרפור, מחלת לב איסכמית", "Metoprolol": "יל\"ד, אי-ספיקת לב, פרפור, מחלת לב איסכמית",
      "Carvedilol": "יל\"ד, אי-ספיקת לב, מחלת לב איסכמית", "Propranolol": "יל\"ד, רעד, מניעת מיגרנה, דליות ושט"}
RAAS = {g: "יל\"ד, אי-ספיקת לב, מחלת כליות כרונית, אחרי אוטם" for g in ("Enalapril", "Ramipril", "Cilazapril", "Captopril", "Losartan", "Candesartan", "Valsartan")}
RAAS.update({"Spironolactone": "יל\"ד, אי-ספיקת לב, בצקות, היפרקלמיה נמוכה/אלדוסטרון", "Eplerenone": "אי-ספיקת לב, יל\"ד",
             "Finerenone": "מחלת כליות סוכרתית, אי-ספיקת לב", "Sacubitril/Valsartan": "אי-ספיקת לב",
             "Furosemide": "בצקות, אי-ספיקת לב, מחלת כליות, יל\"ד"})
BB.update(RAAS)
SGLT2 = {"Dapagliflozin": "סוכרת, אי-ספיקת לב, מחלת כליות כרונית", "Empagliflozin": "סוכרת, אי-ספיקת לב, מחלת כליות כרונית"}
INCRETIN = {"Semaglutide": "סוכרת (אוזמפיק), השמנה (וגובי), מניעה קרדיווסקולרית", "Tirzepatide": "סוכרת, השמנה"}

BP_SAFE = dev("bp_safe", "ל\"ד בטווח בטיחות", "ל\"ד אחרון: סיסטולי 90 ומעלה ומתחת ל-160/100, בלי סחרחורת או עילפון מתועדים",
              "ל\"ד נמוך מ-90, 160/100 ומעלה, או סחרחורת / עילפון")
WEIGHT = mon("weight", "משקל מתועד", "מדידת משקל מ-12 החודשים האחרונים", "מדידת משקל")


def _ins(checks, after_k, item):
    i = next((n for n, c in enumerate(checks) if c["k"] == after_k), -1)
    checks.insert(i + 1, dict(item))


def apply(htn, dm):
    for d in htn:
        if d["generic"] in BB:
            d["checks"] = [c for c in d["checks"] if c["k"] not in ("target", "age80")]
            _ins(d["checks"], "bp", BP_SAFE)
            d["why"] = NOTE + "התוויות: " + BB[d["generic"]] + ". " + d["why"]
            d["multi"] = BB[d["generic"]]
    for d in dm:
        g = d["generic"]
        if g in SGLT2 or g in INCRETIN:
            d["checks"] = [c for c in d["checks"] if c["k"] not in ("a1c", "target")]
            ind = SGLT2.get(g) or INCRETIN.get(g)
            d["why"] = NOTE + "התוויות: " + ind + ". " + d["why"]
            d["multi"] = ind
        if g in SGLT2:
            d["thr"] = ["eGFR <25"]                         # common threshold for all indications (was <45 for diabetes)
        if g in INCRETIN:
            d["checks"].insert(0, dict(WEIGHT))
