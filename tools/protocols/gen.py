# Build everything: data -> out/data.json + Excels, then the page (repo root) and a body-only copy (out/protocols-rofan.html).
# Usage: python3 tools/protocols/gen.py   (from anywhere)
import json, subprocess, os, sys
S = os.path.dirname(os.path.abspath(__file__)) + "/"
REPO = os.path.abspath(S + "../..") + "/"
OUT = S + "out/"
os.makedirs(OUT, exist_ok=True)
subprocess.run([sys.executable, S + "build.py"], check=True, cwd=OUT)
s = open(S + "template.html").read()
d = json.load(open(OUT + "data.json")); data = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
art = s.replace("__DATA__", data); open(OUT + "protocols-rofan.html", "w").write(art)
src=art.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
U="https://asseoy.github.io/medical_aids/"
DESC="פרוטוקולי רפואן לחידוש מרשמים כרוניים (לפי מערכות גוף) ולהפקת אישורים ומענה לפניות מקוונות — טיוטות לבדיקה ואישור"
head=f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#13233D">
<meta name="description" content="{DESC}">
<link rel="icon" href="protocols-icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="protocols-180.png">
<link rel="manifest" href="manifest-protocols.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="פרוטוקולים">
<meta name="mobile-web-app-capable" content="yes">
<meta property="og:type" content="website">
<meta property="og:url" content="{U}protocols-rofan.html">
<meta property="og:title" content="פרוטוקולים לאישור">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{U}protocols-og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
'''
i=src.index("</style>")+len("</style>")
page=head+src[:i]+"\n</head>\n<body>\n"+src[i:]+"\n</body>\n</html>\n"
page=page.replace("body{background:var(--bg);","body{margin:0;background:var(--bg);",1)
open(REPO + "protocols-rofan.html", "w").write(page)

import shutil
for f in ["protocols-icon.svg","protocols-180.png","protocols-192.png","protocols-512.png","protocols-og.png"]:
    shutil.copy(S + "assets/" + f, REPO + f)
sys.path.insert(0, S)
import regroup_names
RECALC = "/mnt/skills/public/xlsx/scripts/recalc.py"
for k, xn in regroup_names.NAMES:
    f = OUT + f"פרוטוקול_רפואן_{xn}.xlsx"
    if os.path.exists(RECALC):     # caches formula values (optional; Excel recalculates on open anyway)
        subprocess.run([sys.executable, RECALC, f], check=True, capture_output=True)
    shutil.copy(f, REPO + f"protocols-rofan-{k}.xlsx")
import yoman; yoman.run()   # task-log template (assets/), synced with the drug lists and the two flag columns
for _k in ("vac", "cert", "req"):   # kind tabs: generated from kinds.json, so they always match the tool
    if os.path.exists(OUT + f"protocols-rofan-{_k}.xlsx"):
        shutil.copy(OUT + f"protocols-rofan-{_k}.xlsx", REPO + f"protocols-rofan-{_k}.xlsx")
