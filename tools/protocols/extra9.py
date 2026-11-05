# Ninth batch (5.11.2026, "כן תוסיף הכל"): the ~170 community brand names from the registry still missing after batches 5–8.
import re
import regbrands as RB
from extra import B, ONLY
from otc import O, N, checks, cat, DOC


def RG(*prefixes, note=""):
    """Registry products whose English name starts with one of the prefixes, one brand per base name."""
    out, seen = [], set()
    for p in prefixes:
        for en, he, ing, _ in RB._ROWS:
            if en.upper().startswith(p.upper()) and not re.search(r"INJ|\bI\.?V\b|INFUS", en, re.I):
                b = RB._base(en)
                if b.lower() not in seen:
                    seen.add(b.lower()); out.append(B(b.title() if b.isupper() else b, he, note))
    assert out, "no registry product for " + str(prefixes)
    return out


BRANDS = {
    "Topical steroids": RG("TRIDERM", "CLOTRISONE", "FUCICORT", "COMAGIS", "BETRIEN", "ENSTILAR", "XAMIOL", "SOREL COMBO", "HYCOMYCIN")
                        + RG("TARIOL", note="קלציפוטריול, בלי סטרואיד"),
    "Topical antifungals": RG("POLYCUTAN", "TEVACUTAN", "NIZORAL CREAM", "SPIRIT WHITFIELD"),
    "Topical antibiotics": RG("GENTATRIM", "CHLORPHENICOL SKIN"),
    "Topical acne treatment": RG("TWYNEO", "LINDAC", "TAROCLINDIN", "ZINDACLIN"),
    "Topical calcineurin / PDE4 inhibitors (eczema)": RG("PROTOPIC"),
    "Ivermectin cream (rosacea)": RG("ROZEX", note="מטרונידזול"),
    "Wart treatment": RG("VERRUMAL", "TOPISALEN", "SALIKAREN", "SPIRIT SALICYL"),
    "Burn and wound creams": RG("ICHTHAMMOL"),
    "Sedating antihistamine": RG("MEDI-DENE DROPS", "TINDEN DROPS"),
    "Antihistamines (2nd generation)": RG("ALLERGYX", "DESLORATADINE - TRIMA"),
    "Nasal decongestant spray": RG("VIBROCIL"),
    "Intranasal corticosteroid (seasonal)": RG("RYALTRIS", "STERONASE"),
    "Antibiotic eye and ear drops": [B("Oflox", "אופלוקס")] + RG("OFLOXACIN EDOL", "CIPLOX", "LACROMYCIN", "OPTI GENTA", "LEVOCORT", "LEVODESA", "MOXIFLOXAN", "DESOREN"),
    "Steroid eye drops": RG("AFLUMYCIN", "THREOLONE"),
    "Decongestant eye drops": RG("VISINE", "VIEW", "DEXEFRIN"),
    "Artificial tears": RG("OFTASTERIL"),
    "Paracetamol (short course)": RG("SUPRAMOL 500", "RAZAMOL") + RG("MUSCOL", note="עם אורפנדרין"),
    "Ibuprofen / naproxen (short course)": RG("COMBODEX", note="עם פרצטמול") + RG("ACETOSAL", "EXIDOL", note="אספירין"),
    "Cold and flu combinations (decongestant)": RG("TEVA - COLD", note="עם פרצטמול, כלורפנירמין, פנילאפרין, קפאין")
                                                + RG("EXCEDRIN", note="פרצטמול, אספירין וקפאין — בלי מכווץ כלי דם"),
    "Topical NSAID gel": RG("DICLOVIT", "DICLOPLAST"),
    "Comfrey and herbal topical pain": RG("BENGAY", "TIGER BALM", "RADIAN B"),
    "Local anaesthetic cream (before a procedure)": RG("LMX4", "ESRACAIN", "XYLOCAINE PUMP", "PLIAGLIS"),
    "Throat lozenges and sprays": RG("CLEAROCIN"),
    "Antacids and alginates": RG("RENNIE"),
    "Stimulant laxatives and suppositories": RG("RAZALAX ADULT"),
    "Iron (oral)": RG("FERRIPEL"),
    "Folic acid": RG("FOROL", "FORIC"),
    "Vitamin B12": RG("TRIO B", "SHALOSH B"),
    "Opioids": RG("ZALDIAR", "ABSTRAL", "FENTAMED", "FENTORA", "PECFENT", "ACTIQ", "SUBLOCADE", "BUPENSAN", "BUPREVENIR", "NYXOID"),
    "Atorvastatin + Ezetimibe": [B("Atozet", "אטוזט")],
    "Propranolol": RG("SYRIPRALOL"),
    "Terbutaline": RG("TERBULIN"),
    "Vardenafil": RG("VARDENAFIL INOVAMED"),
    "HIV antiretrovirals": RG("DOLUTREMED"),
    "Amphetamine salts (adults)": RG("AMFEXON", "DEXTAMINE"),
    "Bupropion": RG("AUVELITY", note="עם דקסטרומתורפן"),
    "Minoxidil (hair loss)": RG("PROPECIA", note="פינסטריד 1 מ\"ג, לגברים"),
    "Antibiotics for a new symptom": RG("MACROBID", "OFLODEX", "OFLOXACIN TEVA"),
    "GnRH antagonists (endometriosis, fibroids)": RG("RYEQO"),
    "Misoprostol": RG("MIFEGYNE"),
    "Oral oncology and hormonal cancer therapy": RG("HYCAMTIN", "VESANOID", "PALOXI", "NAVELBINE"),
    "Rare metabolic / orphan drugs": RG("KETOCONAZOLE ESTEVE", "NUEDEXTA"),
    "Herbal cough and sinus preparations": RG("TESALIN", note="פטסיטס, לנזלת אלרגית"),
    "Oral corticosteroid course": RG("BETNESOL", "STEROCORT"),
    "Eye-specialist drops and implants": RG("DICLOFTIL", "LOCALIN", "ANESTOCIL", "OXYBUPROCAINE"),
    "Other specialist drugs": RG("RECTOSONIDE", note="בודסוניד רקטלי, גסטרו"),
    "Omeprazole": RG("PROMEZOLE", note="תרחיף"),
    "Cystic fibrosis modulators": RG("TOBI ", note="טוברמיצין בשאיפה"),
    "Vaginal and oral antifungals": RG("ZIDOVAL", note="מטרונידזול נרתיקי") + RG("CALINDA", note="קלינדמיצין נרתיקי"),
    "Dermatology specialist topicals": RG("SUNACTIC", "FLUTAROL", "FILSUVEZ"),
    "Skin and mouth antiseptics": RG("SEPTADINE", "ALCOHOL CHLORHEXIDINE", "IODICARE", "IODO-VIT", "POLYSKIN", "SAVIOR", "MERFEN", "SEPTOL",
                                     "ALCOHOL 70", "SOLODENT", "TARODENT", "DERMAX", "SEPTAL SCRUB"),
    "Antipruritic lotion": RG("MEDI-DENE GEL", "TINDEN GEL", "ZINC LOTION", "BALNEUM PLUS"),
}

RENAME = {"Antipruritic lotion": "תכשירים לגרד מקומי (קלמין, פניסטיל ג'ל, צינק)",
          "Ivermectin cream (rosacea)": "טיפול מקומי ברוזציאה (סולנטרה, רוזקס)",
          "Minoxidil (hair loss)": "טיפול בנשירת שיער (מינוקסידיל, פרופסיה)",
          "Comfrey and herbal topical pain": "משחות מחממות וצמחים לכאב שרירים (טראומפלנט, בנגיי, טייגר באלם)",
          "Local anaesthetic cream (before a procedure)": "הרדמה מקומית לפני פעולה (אמלה, LMX4, עזרקאין)",
          "Vaginal and oral antifungals": "טיפול בפטרת או בזיהום נרתיקי (פלוקונזול, אגיסטן V, זידובל)",
          "Misoprostol": "מיזופרוסטול ומיפפריסטון (ציטוטק, מיפג'ין)",
          "Cold and flu combinations (decongestant)": "תכשירי צינון ושפעת משולבים (פסאודואפדרין, פנילאפרין)",
          "Ibuprofen / naproxen (short course)": "איבופרופן / נפרוקסן / אספירין — קורס קצר"}

NVP_NOTE = ("הוראות לטיפול בבחילות בהיריון:\n"
            "• לקחת לפי ההוראה: בדרך כלל 2 טבליות לפני השינה, ולפי הצורך תוספת בבוקר ובצהריים.\n"
            "• גורם לישנוניות: לא לנהוג אם יש ישנוניות.\n"
            "• לאכול ארוחות קטנות ותכופות ולשתות לאורך היום.\n"
            "• אם אי אפשר לשמור נוזלים יותר מ-24 שעות, יש ירידה במשקל, שתן כהה ומעט, סחרחורת, כאב בטן, חום או דם בהקאה — לפנות לרופא באותו יום.")

NEW = [
    O("Doxylamine + pyridoxine (nausea of pregnancy)", "בחילות בהיריון (דיקלקטין, לדוקסיה, בונג'סטה)", "היריון · בחילות",
      RG("DICLECTIN", "LADOXIA", "BONJESTA"),
      "קו ראשון לבחילות והקאות בהיריון. בטוח בהיריון. סימני הקאות היריון קשות (התייבשות, ירידה במשקל) — לרופא/ה באותו יום.",
      [N("preg", "היריון מתועד", "היריון ידוע ומתועד ברשומה (שבוע ההיריון)", "היריון לא מתועד"),
       N("severe", "אין סימני הקאות קשות", "בפנייה: שומרת על נוזלים, אין ירידה במשקל, שתן כהה ומעט, סחרחורת או חולשה", "סימני התייבשות או ירידה במשקל — באותו יום"),
       N("other", "אין סימן לסיבה אחרת", "אין חום, כאב בטן, כאב ראש חזק, צרבת חזקה, שלשול או דם בהקאה", "סימן לסיבה אחרת"),
       N("sedat", "אין תרופות מרדימות קבועות", "אין בנזודיאזפינים, אופיואידים או תרופות שינה בתרופות הקבועות", "תרופה מרדימה קבועה"),
       N("dur", "כמות לחודש", "מרשם לחודש, לפי ההוראה", "כמות גדולה יותר")],
      NVP_NOTE, tab="women", doctitle="הכנת מרשם לבחילות בהיריון", src="הנחיה: בחילות והקאות בהיריון (מסמך הפרויקט); עלון לרופא",
      comp=[("לא שומרת נוזלים מעל 24 שעות", "לרופא/ה באותו יום"), ("כאב בטן, חום או דם בהקאה", "דחוף")]),
    ONLY("Intrauterine devices (hormonal)", "התקן תוך-רחמי הורמונלי (מירנה, קיילינה)", "בריאות האישה · התקן",
         RG("MIRENA", "KYLEENA"),
         "התקן הורמונלי מוחדר ע\"י גינקולוג/ית, וההחלפה לפי משך התקן (מירנה עד 8 שנים, קיילינה עד 5). מרשם ע\"י רופא/ה. להעביר לרופא/ה.") | {"tab": "women"},
    ONLY("Progesterone (fertility, pregnancy)", "פרוגסטרון נרתיקי לפוריות ולהיריון (אנדומטרין, קרינון)", "פוריות · מומחה",
         RG("ENDOMETRIN", "CRINONE"),
         "נקבע ע\"י רופא/ת פוריות או מעקב היריון בסיכון. להעביר לרופא/ה.") | {"tab": "women"},
    ONLY("Eye-specialist drops and implants", "טיפות וטיפולים של רופא/ת עיניים (נבנק, ברומסייט, אוזורדקס, מרחיבי אישונים)", "עיניים · מומחה",
         RG("NEVANAC", "BROMSITE", "OZURDEX", "CYCLOPENTOLATE", "ATROSPAN", "MYDRAMIDE", "PHENYLEPHRINE VISION", "EFRIN", "IOPIDINE", "CYSTADROPS"),
         "טיפות אחרי ניתוח, מרחיבי אישונים ושתלים לעין — לפי רופא/ת עיניים. מרשם או חידוש ע\"י רופא/ה.") | {"tab": "eyeskin"},
    ONLY("Ciclosporin eye drops (dry eye)", "ציקלוספורין טיפות עיניים ליובש (רסטזיס, סיקווה)", "עיניים · מומחה",
         RG("RESTASIS", "CEQUA"),
         "ליובש עיניים קשה, נקבע ע\"י רופא/ת עיניים ודורש אישור מימון. להעביר לרופא/ה.") | {"tab": "eyeskin"},
    DOC("St John's wort", "היפריקום (רמוטיב)", "רופא/ה בלבד · צמחים",
        RG("REMOTIV"),
        "צמח למצב רוח עם אינטראקציות חמורות: מוריד רמות של גלולות, נוגדי קרישה, תרופות לב, HIV ומדכאי חיסון, ומסוכן עם SSRI. "
        "דיכאון צריך הערכה. להעביר לרופא/ה."),
    DOC("Anal fissure treatment", "טיפול בפיסורה (רקטוג'סיק, אנטרולין)", "רופא/ה בלבד · פיסורה",
        RG("RECTOGESIC", "ANTROLIN"),
        "כאב חד ביציאה עם דם טרי מצריך בדיקה. רקטוג'סיק (ניטרוגליצרין) — כאב ראש, ואסור עם סילדנפיל או טדלפיל. להעביר לרופא/ה."),
]


def apply(lists):
    lists[-1].extend(NEW)
    allp = [d for L in lists for d in L]
    names = {d["generic"] for d in allp}
    for g in list(BRANDS) + list(RENAME):
        assert g in names, "extra9: no entry " + g
    for d in allp:
        have = {b["en"].lower() for b in d["brands"]}
        for b in BRANDS.get(d["generic"], []):
            if b["en"].lower() not in have:
                d["brands"].append(b); have.add(b["en"].lower())
        if d["generic"] in RENAME:
            d["he"] = RENAME[d["generic"]]
