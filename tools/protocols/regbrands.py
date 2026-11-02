# Brand names straight from the Israeli registry text (Medicines.xlsx, 7.10.2026) in the project.
import re

import os
REG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "medicines-registry.txt")
_ROWS = []
for _l in open(REG, encoding="utf-8"):
    _p = [x.strip() for x in _l.split("|")]
    if len(_p) == 4 and not _l.startswith("#"):
        _ROWS.append(_p)

NONORAL = r"INJ|VIAL|AMP|INFUS|CREAM|GEL\b|OINT|LOTION|SHAMPOO|DROPS|EYE|EAR|NASAL|SPRAY|SUPPOS|RECTAL|FOAM|ENEMA|SYRUP|SUSP|SOLUTION|PATCH|VAGINAL|PESSAR|IMPLANT|IUD|IUS|\bMG ?/ ?\d* ?ML|MG/ML|U/ML|%"


def _base(name):
    n = re.sub(r"[®™]", " ", name)
    n = re.sub(r"\s+\d.*$", "", n)                      # drop strength and everything after it
    n = re.sub(r"\s+(TABLETS?|CAPSULES?|CAPLETS|F\.?C\.?|FILM.*|CHEWABLE.*)$", "", n, flags=re.I)
    return re.sub(r"\s+", " ", n).strip(" -–")


def brands(ings, include=None, exclude=NONORAL, extra_exclude=None, exact=True):
    """ings: list of ingredient words that must all appear (and, if exact, no others)."""
    out, seen = [], set()
    for en, he, ing, _ in _ROWS:
        U = ing.upper()
        parts = [re.split(r"\s\d", x.strip())[0] for x in U.split(",")]
        if not all(any(i in p for p in parts) for i in ings):
            continue
        if exact and len(parts) != len(ings):
            continue
        blob = en.upper() + " " + U
        if include and not re.search(include, blob, re.I):
            continue
        if exclude and re.search(exclude, blob, re.I):
            continue
        if extra_exclude and re.search(extra_exclude, blob, re.I):
            continue
        b_en, b_he = _base(en), _base(he)
        if b_en.upper() in seen:
            continue
        seen.add(b_en.upper())
        out.append(dict(en=b_en.title() if b_en.isupper() else b_en, he=b_he, note=""))
    return out
