# Sixth batch (5.11.2026), registry gap stage 2: specialist drugs. All renewed by the physician only (suit "לא"),
# except pilocarpine eye drops and the eczema / rosacea creams, which follow the specialist-set rules of their tab.
import regbrands as RB
from extra import B, D, ONLY, VISIT, RENEW, cond
from extra3 import eye

ORAL = r"INJ|VIAL|INFUS|CONCENTRATE|S\.C\.|/ ?\d* ?ML|LIPOSOMAL|POWDER FOR|I\.V"


def RO(ings, drop=None):
    out, seen = [], set()
    for i in ings:
        for b in RB.brands([i], exclude=ORAL, exact=False):
            k = b["en"].lower()
            if k in seen or (drop and any(x in k for x in drop)):
                continue
            seen.add(k); out.append(b)
    return out


ONCO = ["ACALABRUTINIB", "AFATINIB", "ALECTINIB", "ASCIMINIB", "AXITINIB", "AZACITIDINE", "BELZUTIFAN", "BINIMETINIB", "BOSUTINIB",
        "BRIGATINIB", "BUSULFAN", "CABOZANTINIB", "CAPIVASERTIB", "CAPMATINIB", "COBIMETINIB", "CRIZOTINIB", "DABRAFENIB", "ELACESTRANT",
        "ENCORAFENIB", "ENTRECTINIB", "ERDAFITINIB", "ERLOTINIB", "FEDRATINIB", "FRUQUINTINIB", "GEFITINIB", "GILTERITINIB", "INAVOLISIB",
        "IVOSIDENIB", "IXAZOMIB", "LAPATINIB", "LAROTRECTINIB", "LAZERTINIB", "LENVATINIB", "LORLATINIB", "MERCAPTOPURINE", "MIDOSTAURIN",
        "MITOTANE", "MOMELOTINIB", "NERATINIB", "NIROGACESTAT", "PAZOPANIB", "PEMIGATINIB", "PIRTOBRUTINIB", "POMALIDOMIDE", "PONATINIB",
        "REGORAFENIB", "RIPRETINIB", "RUCAPARIB", "SELINEXOR", "SELPERCATINIB", "SELUMETINIB", "SONIDEGIB", "SORAFENIB", "SOTORASIB",
        "SUNITINIB", "TALAZOPARIB", "TEPOTINIB", "THALIDOMIDE", "TIPIRACIL", "TRAMETINIB", "TUCATINIB", "VANDETANIB", "VEMURAFENIB",
        "VENETOCLAX", "VISMODEGIB", "VORASIDENIB", "ZANUBRUTINIB", "SEVABERTINIB", "ZONGERTINIB", "TELOTRISTAT", "EFLORNITHINE",
        "APREPITANT", "GRANISETRON", "NETUPITANT"]

RARE = ["AMIFAMPRIDINE", "IDEBENONE", "ATALUREN", "BETAINE", "CHOLIC ACID", "GLYCEROL PHENYLBUTYRATE", "SODIUM PHENYLBUTYRATE",
        "LEVOCARNITINE", "BEROTRALSTAT", "AVACOPAN", "BELUMOSUDIL", "LENIOLISIB", "DANICOPAN", "VAMOROLONE", "RISDIPLAM", "TROFINETIDE",
        "OMAVELOXOLONE", "LEVACETYLLEUCINE", "GIVINOSTAT", "LONAFARNIB", "MARALIXIBAT", "ODEVIXIBAT", "SEPIAPTERIN", "CARGLUMIC ACID",
        "MERCAPTAMINE", "METYRAPONE", "OSILODROSTAT", "MIDODRINE HYDROCHLORIDE MORNINGSIDE"]

BRANDS = {
    "Oral oncology and hormonal cancer therapy": RO(ONCO, drop=["kalceks", "seacross", "palonosetron"]),
    "HIV antiretrovirals": RO(["ATAZANAVIR", "ETRAVIRINE", "MARAVIROC", "RITONAVIR", "ZIDOVUDINE"], drop=["paxlovid"]),
    "Rare metabolic / orphan drugs": RO(RARE, drop=["midodrine", "ursofalk", "ursolit", "ocaliva"]),
}

SPEC_DERM = "נקבע ע\"י רופא/ת עור, אותו טיפול ב-3 החודשים האחרונים"
NEW = [
    eye("Pilocarpine (eye drops)", "פילוקרפין (טיפות עיניים)", "גלאוקומה · כולינרגי", [B("Pilocarpine 2 % Vitamed", "פילוקרפין 2% ויטאמד")],
        "מצר אישונים: ראייה חשוכה בלילה. ביקורת שנתית אצל רופא/ת עיניים") | {"tab": "eyeskin"},
    D("Topical calcineurin / PDE4 inhibitors (eczema)", "משחות לאטופיק דרמטיטיס ללא סטרואיד (אלידל, סטקוויס)", "אקזמה · לא סטרואיד",
      [B("Elidel Cream 1 %", "אלידל קרם 1%"), B("Staquis", "סטקוויס")],
      "נקבע ע\"י רופא/ת עור או ילדים. צריבה בהתחלה — צפויה. זיהום בעור (מוגלה, הרפס) ← להפסיק ולפנות לרופא/ה.", "אין מעקב מעבדה",
      [dict(k="inf", label="אין זיהום בעור", det="בפנייה אין מוגלה, שלפוחיות או פצעים מזוהמים באזור הטיפול", doc="אין זיהום בעור.",
            bad="זיהום בעור", opt=False, crit="בפנייה אין מוגלה, שלפוחיות או פצעים מזוהמים. לא ← לרופא/ה."),
       dict(VISIT), cond(SPEC_DERM), dict(RENEW)], suit="בתנאים", tab="eyeskin",
      comp=[("מוגלה, שלפוחיות או הרפס", "לרופא/ה"), ("החמרה למרות טיפול", "לרופא/ת עור")]),
    D("Ivermectin cream (rosacea)", "איברמקטין קרם לרוזציאה (סולנטרה)", "רוזציאה",
      [B("Soolantra", "סולנטרה")],
      "נקבע ע\"י רופא/ת עור או משפחה. החמרה זמנית בשבועות הראשונים אפשרית.", "אין מעקב מעבדה",
      [dict(VISIT), cond(SPEC_DERM.replace("רופא/ת עור", "רופא/ת עור או משפחה")), dict(RENEW)], suit="בתנאים", tab="eyeskin",
      comp=[("כאב או אודם בעין", "לרופא/ה"), ("החמרה", "לרופא/ה")]),
    ONLY("Dermatology specialist topicals", "טיפולים מקומיים של רופא/ת עור (אפודיקס, אלדרה, קליסירי)", "עור · מומחה",
         [B("Efudix Cream 5%", "אפודיקס קרם 5%"), B("Aldara 5 %", "אלדרה 5%"), B("Aquimod Cream 5 %", "אקווימוד קרם 5%"),
          B("Klisyri Ointment", "קליסירי משחה"), B("Esomed Gel", "אסומד ג'ל", "הידרוקינון"), B("Leshcutan Ointment", "לשקוטן משחה"),
          B("Toctino 10 MG", "טוקטינו 10 מ\"ג"), B("Toctino 30 MG", "טוקטינו 30 מ\"ג"), B("Ledaga", "לדגה")],
         "טיפולים לקרטוזיס אקטינית, יבלות באיברי המין, כתמים, לישמניה ואקזמה בידיים: נקבעים ומנוטרים ע\"י רופא/ת עור. להעביר לרופא/ה.") | {"tab": "eyeskin"},
    ONLY("Allergen immunotherapy", "חיסון לאלרגיה (אקריזקס)", "אלרגיה · מומחה",
         [B("Acarizax", "אקריזקס")],
         "טיפול באלרגנים נקבע ומנוטר ע\"י אלרגולוג/ית (מנה ראשונה במרפאה). להעביר לרופא/ה.") | {"tab": "resp"},
    ONLY("Oral pilocarpine (dry mouth)", "פילוקרפין בבליעה ליובש בפה (סלגן, סלבקל)", "ראומטולוגיה · מומחה",
         [B("Salagen", "סלגן"), B("Salvakal", "סלבקל")],
         "ליובש בפה בסיוגרן או אחרי הקרנות: נקבע ע\"י מומחה. אסור באסתמה לא מאוזנת ובגלאוקומה עם זווית סגורה. להעביר לרופא/ה.") | {"tab": "immune"},
    ONLY("Nalmefene", "נלמפן (סלינקרו)", "התמכרות לאלכוהול · מומחה",
         [B("Selincro 18 MG", "סלינקרו 18 מ\"ג")],
         "להפחתת שתיית אלכוהול, במסגרת טיפול ומעקב. אסור עם אופיואידים. להעביר לרופא/ה.") | {"tab": "psych"},
    ONLY("GnRH antagonists (endometriosis, fibroids)", "אנטגוניסטים ל-GnRH (אוריליסה, יסלטי)", "גינקולוגיה · מומחה",
         [B("Orilissa 150 MG", "אוריליסה 150 מ\"ג"), B("Orilissa 200 MG", "אוריליסה 200 מ\"ג"), B("Yselty 100 MG", "יסלטי 100 מ\"ג"),
          B("Yselty 200 MG", "יסלטי 200 מ\"ג")],
         "לאנדומטריוזיס ולשרירנים: נקבע ע\"י גינקולוג/ית, מוגבל בזמן (צפיפות עצם). להעביר לרופא/ה.") | {"tab": "women"},
    ONLY("Urinary alkalinisers", "אשלגן ציטרט ומשנני שתן (יורוציט-קיי, אוראליט-U)", "אבנים בכליות · מומחה",
         [B("Urocit-K 10 mEq", "יורוציט-קיי 10 mEq"), B("Uralyt-U", "אוראליט-U")],
         "למניעת אבנים: נקבע ע\"י נפרולוג/ית או אורולוג/ית. מעקב אשלגן ותפקוד כליות. להעביר לרופא/ה.") | {"tab": "renal"},
    ONLY("Specialist anti-infectives", "תרופות אנטי-זיהומיות של מומחה (פטריות, CMV, שחפת, קלוסטרידיום)", "זיהומים · מומחה",
         RO(["VALGANCICLOVIR", "POSACONAZOLE", "VORICONAZOLE", "ISAVUCONAZOLE", "FIDAXOMICIN", "LINEZOLID", "RIFABUTIN", "BEDAQUILINE",
             "AMINOSALICYLIC", "MARIBAVIR", "LETERMOVIR", "QUININE", "QUINIDINE", "MILTEFOSINE"], drop=["valganvir", "nuedexta"]),
         "תרופות שנקבעות ע\"י מומחה/ית למחלות זיהומיות או במסגרת השתלה, שחפת או זיהום עמיד. להעביר לרופא/ה.") | {"tab": "immune"},
]


def apply(lists):
    allp = [d for L in lists for d in L]
    names = {d["generic"] for d in allp}
    for g in BRANDS:
        assert g in names, "extra6: no entry " + g
    for d in allp:
        have = {b["en"].lower() for b in d["brands"]}
        for b in BRANDS.get(d["generic"], []):
            if b["en"].lower() not in have:
                d["brands"].append(b); have.add(b["en"].lower())
    lists[-1].extend(NEW)
