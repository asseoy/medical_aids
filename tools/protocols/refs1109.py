# Monitoring source per drug (9.11.2026): SPS Medicines Monitoring (NHS) page or the US FDA label on DailyMed,
# from the Mac mini reports MM261109-1 (SPS) and MM261109-3 (openFDA). refs1109.json maps generic -> [{t, u}].
# The links are shown under "מקור" in the tool; the clinical content is not changed here.
import json, os
S = os.path.dirname(os.path.abspath(__file__)) + "/"
NO_SRC = "לא מופיע בהנחיות שבפרויקט"


def apply(lists):
    refs = json.load(open(S + "refs1109.json"))
    n = 0
    for L in lists:
        for d in L:
            r = refs.get(d["generic"])
            if not r:
                continue
            d["refs"] = r
            kinds = []
            if any(x["t"].startswith("SPS") for x in r): kinds.append("SPS Medicines Monitoring (NHS)")
            if any(x["t"].startswith("עלון FDA") for x in r): kinds.append("עלון ה-FDA (DailyMed)")
            if any(x["t"].startswith("עלון לרופא") for x in r): kinds.append("העלון לרופא (משרד הבריאות)")
            if any(x["t"].startswith(("EMA", "FSRH")) for x in r): kinds.append(" ו".join(x["t"].split(" —")[0] for x in r if x["t"].startswith(("EMA", "FSRH"))))
            tag = "מעקב: " + " ו".join(kinds)
            src = (d.get("src") or "").strip()
            d["src"] = tag if (not src or src == NO_SRC) else src + "; " + tag
            n += 1
    return n
