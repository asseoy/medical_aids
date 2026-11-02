# Active ingredient of each trade name, from the registry. Used so that a group entry (e.g. "Biologic drugs") shows only
# the trade names that share the searched drug's active ingredient.
import re
import regbrands as R

_ING = {}
for en, he, ing, _ in R._ROWS:
    key = R._base(en).upper()
    # active moiety only: first word, first 7 letters (drops salts: "METHYLPHENIDATE HCL" = "METHYLPHENIDATE", "MYCOPHENOLATE" = "MYCOPHENOLIC")
    parts = sorted({re.sub(r"[^A-Z]", "", x.strip().split(" ")[0])[:7] for x in ing.upper().split(",") if x.strip()} - {""})
    _ING.setdefault(key, "+".join(parts))


def ingredient(en):
    k = re.sub(r"\s+", " ", str(en).upper().replace("®", "")).strip()
    k = re.sub(r"\s*\(.*?\)", "", k)
    if k in _ING:
        return _ING[k]
    for cand in (k + " ", k + "-"):
        hits = {v for key, v in _ING.items() if key.startswith(cand)}
        if len(hits) == 1:
            return hits.pop()
    return None


def annotate(d):
    ings = [ingredient(b["en"]) for b in d["brands"]]
    if len({i for i in ings if i}) > 1:          # mixed group: remember each brand's ingredient
        d["mixed"] = True
        for b, i in zip(d["brands"], ings):
            if i: b["ing"] = i
