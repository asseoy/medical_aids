# Split the lab / pulse thresholds into one checklist item per parameter (potassium, sodium, kidney function,
# liver, pulse). Each item: ticked = normal. If not ticked and the parameter also has a severe value, the tool asks
# "is it also severe?". A parameter with only a severe value is a contraindication item.

PARAMS = [  # key, label, bad wording
    ("lab_lvl", "רמת התרופה בדם", "רמה מחוץ לטווח"),
    ("lab_cbc", "ספירת דם (WBC / נויטרופילים)", "ספירת דם חריגה"),
    ("lab_hb", "המוגלובין (Hb)", "ירידה בהמוגלובין"),
    ("lab_hct", "המטוקריט (Hct)", "המטוקריט גבוה"),
    ("lab_k", "אשלגן (K)", "אשלגן חריג"),
    ("lab_na", "נתרן (Na)", "נתרן חריג"),
    ("lab_renal", "תפקוד כליות (קריאטינין / eGFR)", "תפקוד כליות חריג"),
    ("lab_alt", "תפקודי כבד (ALT)", "ALT חריג"),
    ("lab_ck", "CPK (אם נבדק)", "CPK חריג"),
    ("pulse", "דופק במנוחה", "דופק נמוך"),
]
ORDER = [p[0] for p in PARAMS]


def _param(t):
    t = t.strip()
    if t.startswith("K "): return "lab_k"
    if t.startswith("Na "): return "lab_na"
    if t.startswith("eGFR") or t.startswith("קריאטינין"): return "lab_renal"
    if t.startswith("ALT"): return "lab_alt"
    if t.startswith("CPK"): return "lab_ck"
    if t.startswith("רמה"): return "lab_lvl"
    if t.startswith("WBC"): return "lab_cbc"
    if t.startswith("Hb"): return "lab_hb"
    if t.startswith("Hct"): return "lab_hct"
    if t.startswith("דופק"): return "pulse"
    return None


def _items(lst):
    out = []
    for t in lst:
        if t.startswith("Na או K "):                      # one HTN entry lists both
            rest = t[len("Na או K "):]
            out += ["Na " + rest, "K " + rest]
        else:
            out.append(t)
    return out


def nest(d):
    ch = d["checks"]
    old = [c for c in ch if c["k"] in ("labs", "pulse", "severe")]
    if not old:
        return
    pos = ch.index(old[0])
    thr = [t for t in _items(d.get("thr", [])) if _param(t)]
    sev = [t for t in d.get("severe", []) if _param(t)]
    new = []
    for key, label, bad in PARAMS:
        m = [t for t in thr if _param(t) == key]
        s = [t for t in sev if _param(t) == key]
        if not m and not s:
            continue
        if key == "pulse" and m:
            m = ["מתחת ל-55"]
        if key == "pulse" and s:
            s = ["מתחת ל-50"]
        parts = []
        if m: parts.append("חריג: " + " או ".join(m) + " ← חידוש לחודש + הודעה לרופא/ה")
        if s: parts.append("חמור: " + " או ".join(s) + " ← לא מחדשים, הודעה לרופא/ה")
        det = " · ".join(parts)
        SUF = {"lab_lvl": " בטווח", "lab_cbc": " תקינה"}
        crit = ("במדידה האחרונה " if key == "pulse" else "בבדיקה האחרונה ") + label + SUF.get(key, " תקין") + ". " + ". ".join(parts) + "."
        c = dict(k=key, label=label + SUF.get(key, " תקין"), det=det, doc=label + SUF.get(key, " תקין") + ".", crit=crit, opt=False, bad=bad)
        if m and s:
            c["sev"] = " או ".join(s)                    # asked only when the item is not ticked
        elif s:
            c["contra"] = True                            # only a severe value exists: not ticked = contraindication
            c["bad"] = label + ": ערך חמור"
        new.append(c)
    # keep any non-parameter thresholds (none today) in a generic item
    rest = [t for t in _items(d.get("thr", [])) if not _param(t) and t not in ("אין ערך מעבדה ייעודי", "לא מופיע בהנחיות")]
    if rest:
        l = "; ".join(rest)
        new.append(dict(k="labs", label="ערכי מעבדה", det="אין: " + l, doc="אין: " + l + ".",
                        crit="בבדיקות האחרונות אין: " + l + ". יש ← חידוש לחודש + הודעה לרופא/ה.", opt=False))
    d["checks"] = [c for c in ch[:pos] if c not in old] + new + [c for c in ch[pos:] if c not in old]
