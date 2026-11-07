# Review booklet (PDF) of every protocol: rules, shared checks, decisions, and every drug / certificate / request type
# with its full checklist. Built from out/data.json, so it always matches the published tool.
# Usage: python3 tools/protocols/booklet.py   (after gen.py) -> out/booklet.html, out/booklet.pdf
import json, os, html, shutil, datetime
from collections import Counter

S = os.path.dirname(os.path.abspath(__file__)) + "/"
OUT = S + "out/"
REPO = os.path.abspath(S + "../..") + "/"
A = json.load(open(OUT + "data.json"))
E = lambda x: html.escape(str(x if x is not None else ""))
SUIT = {"כן": ("yes", "מתאים"), "בתנאים": ("cond", "בתנאים"), "לא": ("no", "רופא/ה בלבד"), "הכנה": ("cond", "הכנה לאישור רופא/ה")}
KIND_TITLE = {"cert": "סוגי אישורים", "req": "סוגי פניות", "vac": "חיסונים"}
TODAY = datetime.date.today().strftime("%d.%m.%Y")

drug_tabs = [k for k in A["order"] if not A[k].get("kind")]
kind_tabs = [k for k in A["order"] if A[k].get("kind")]
all_drugs = [d for k in drug_tabs for d in A[k]["drugs"]]
cnt = Counter(d["suit"] for d in all_drugs)
nred = sum(1 for d in all_drugs if d.get("red"))


def pill(s):
    c, t = SUIT.get(s, ("cond", s))
    return f'<span class="pill {c}">{E(t)}</span>'


def pillD(d):
    return '<span class="pill red">דגל אדום</span>' if d.get("red") else pill(d["suit"])


def ul(items):
    return "<ul>" + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>" if items else ""


def table(head, rows, cls=""):
    return (f'<table class="{cls}"><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>")


def item_block(sec, n, d, kind=None):
    tdm = ' <span class="pill tdm">מעקב צמוד</span>' if d.get("tdm") else ""
    head = (f'<div class="dh"><span class="num">{sec}.{n}</span> <b>{E(d["he"])}</b>'
            + (f' · <span class="ltr">{E(d["generic"])}</span>' if not kind else "") + f' {pillD(d)}{tdm}</div>'
            + f'<div class="cls">{E(d["cls"])}</div>')
    br = [(b.get("he") or "") + (" · " + b["en"] if b.get("en") and not kind else "") + (f' ({b["note"]})' if b.get("note") else "") for b in d["brands"]]
    rows = []
    if br:
        rows.append(("נקרא גם" if kind else f"שמות מסחריים ({len(br)})", E(" | ".join(br))))
    rows.append(("נימוק / הערה", E(d.get("why", ""))))
    if d.get("only"):
        rows.append(("הנחיה", "<b>" + E(d["only"]) + "</b>"))
    body = "".join(f'<tr><th>{E(a)}</th><td>{b}</td></tr>' for a, b in rows)
    out = f'<div class="item" id="d{sec}-{n}">{head}<table class="kv">{body}</table>'
    if d.get("checks"):
        cr = []
        for i, c in enumerate(d["checks"], 1):
            lab = E(c["label"]) + (f'<div class="q">שאלה: {E(c["q"])}</div>' if c.get("opt") and c.get("q") else "")
            act = E(c.get("crit", ""))
            if c.get("sev"):
                act += f'<div class="sev">חמור: {E(c["sev"])} ← לא מחדשים</div>'
            tag = "התווית נגד" if c.get("contra") or c["k"] == "excl" else ("זימון" if c.get("clinic") or c["k"] in ("bp", "a1c", "annual", "visit") else ("שאלה" if c.get("opt") else ""))
            cr.append((str(i), lab, act, E(tag)))
        out += table(["#", "בדיקה", "קריטריון ופעולה", "סוג"], cr, "checks")
    extra = []
    if d.get("labs") and d["labs"] not in ("-",):
        extra.append(("מעקב מעבדה", E(d["labs"])))
    thr = [t for t in d.get("thr", []) if t not in ("-", "אין ערך מעבדה ייעודי")]
    if thr:
        extra.append(("ספי החזרה לרופא/ה", E("; ".join(thr))))
    if d.get("severe"):
        extra.append(("ערך חמור", E("; ".join(d["severe"]))))
    if d.get("excl"):
        extra.append(("מצבים שמוציאים מהפרוטוקול", E("; ".join(d["excl"]))))
    if d.get("comp"):
        extra.append(("תלונות בפנייה או ברשומה", E("; ".join(f"{c} ← {a}" for c, a in d["comp"]))))
    if d.get("msg"):
        extra.append(("הודעה למטופל/ת", E(d["msg"]).replace("\n", "<br>")))
    if d.get("patnote"):
        extra.append(("הוראות ואזהרות למטופל/ת", E(d["patnote"]).replace("\n", "<br>")))
    if d.get("src"):
        extra.append(("מקור", E(d["src"])))
    if extra:
        out += '<table class="kv">' + "".join(f'<tr><th>{E(a)}</th><td>{b}</td></tr>' for a, b in extra) + "</table>"
    out += '<div class="review">אושר ☐ &nbsp; לתיקון ☐ &nbsp; הערות: ______________________________________________</div></div>'
    return out


def section(sec, k):
    P = A[k]; kind = P.get("kind")
    ds = P["drugs"]
    c = Counter(d["suit"] for d in ds)
    h = f'<section class="tab"><h1 id="s{sec}">{sec}. {E(P["name"])}<span class="mk">ZQ{sec}AZ</span></h1>'
    h += f'<p class="meta">{len(ds)} {"פריטים" if kind else "תרופות"} · ' + " · ".join(f"{SUIT.get(s, ('', s))[1]}: {n}" for s, n in c.items()) + f' · {E(P["version"])}</p>'
    h += f'<p class="meta">מקורות: {E(P["guide"])}</p>'
    h += f'<h2>{sec}.א כללים</h2>' + ul(P["rules"])
    if P.get("out"):
        h += f'<h2>{sec}.ב תוצאות אפשריות</h2>' + table(["תוצאה", "נוסח בתיעוד"], [(E(o[1]), E(o[2])) for o in P["out"]])
    if P.get("common"):
        h += f'<h2>{sec}.ג בדיקות משותפות</h2>' + table(["שלב", "נושא", "מה בודקים", "קריטריון", "אם לא מתקיים", "מקור"], [tuple(E(x) for x in r) for r in P["common"]], "small")
    if P.get("decisions"):
        h += f'<h2>{sec}.ד החלטות</h2>' + table(["#", "נושא", "מה ההנחיה אומרת", "ההחלטה לפרוטוקול", "סוג", "מקור"], [tuple(E(x) for x in r) for r in P["decisions"]], "small")
    h += f'<h2>{sec}.ה רשימת {KIND_TITLE.get(kind, "התרופות")} (לסימון)<span class="mk">ZQ{sec}LZ</span></h2>'
    h += table(["#", "שם", "" if kind else "גנרי", "קבוצה", "התאמה", "אושר", "הערות"],
               [(f"{sec}.{i}", E(d["he"]), "" if kind else f'<span class="ltr">{E(d["generic"])}</span>', E(d["cls"]), pillD(d) + (" ⚗" if d.get("tdm") else ""), "☐", "")
                for i, d in enumerate(ds, 1)], "list")
    h += f'<h2 class="pb">{sec}.ו פירוט מלא<span class="mk">ZQ{sec}DZ</span></h2>' + "".join(item_block(sec, i, d, kind) for i, d in enumerate(ds, 1))
    return h + "</section>"


# cross-tab list: everything renewed by a physician only (each item also appears in its own chapter)
only_rows = []
for i, k in enumerate(drug_tabs, 1):
    for j, d in enumerate(A[k]["drugs"], 1):
        if d["suit"] == "לא":
            names = " | ".join(b.get("he") or b["en"] for b in d["brands"][:12]) + (f" … (+{len(d['brands']) - 12})" if len(d["brands"]) > 12 else "")
            only_rows.append((f'<a href="#d{i}-{j}">{i}.{j}</a>', E(A[k]["name"]), "<b>" + E(d["he"]) + "</b><br>" + f'<span class="ltr">{E(d["generic"])}</span>',
                              E(names), E(d.get("only") or d.get("why", "")), "☐"))
only_sec = f'''<section><h1 id="sonly">רשימה מרוכזת: תרופות שמחודשות ע"י רופא/ה בלבד ({len(only_rows)})<span class="mk">ZQOAZ</span></h1>
<p>בתרופות אלה הכלי לא מציג רשימת בדיקות: מוצגת הודעה, והבקשה עוברת לרופא/ה. אחרי סקירת הפריטים החסומים (7.11.2026) נשארו כאן רק
רואקוטן (רופא/ת עור), אנטיביוטיקה לתסמין חדש ותרופות נגד שפעת. כל פריט מופיע גם בפרק המערכת שלו (המספר בעמודה הראשונה).</p>
{table(["#", "מערכת", "תרופה / קבוצה", "שמות מסחריים", "ההודעה בכלי", "אושר"], only_rows, "small")}</section>'''

prep_rows = [(f'<a href="#d{i}-{j}">{i}.{j}</a>', E(A[k]["name"]), "<b>" + E(d["he"]) + "</b>", E(d.get("why", "")), "☐")
             for i, k in enumerate(drug_tabs, 1) for j, d in enumerate(A[k]["drugs"], 1) if d["suit"] == "הכנה" and not d.get("red")]
red_rows = [(f'<a href="#d{i}-{j}">{i}.{j}</a>', E(A[k]["name"]), "<b>" + E(d["he"]) + "</b>", E(d.get("why", "")),
             E(" · ".join(c["label"] for c in d["checks"] if c["k"] not in ("buy", "visit", "cond", "qty", "inter", "renew", "third"))), "☐")
            for i, k in enumerate(drug_tabs, 1) for j, d in enumerate(A[k]["drugs"], 1) if d.get("red")]
only_sec += f'''<section><h2>רשימה מרוכזת: דגל אדום — בדיקה כפולה מול הרופא/ה ({len(red_rows)})</h2>
<p>תרופות בסיכון גבוה יותר (סקירה 7.11.2026): הרפואן מכין לפי רשימת הבדיקות, והרופא/ה בודק/ת שוב לפני האישור — גם כשהכול תקין.
חריגה מהפרוטוקול מסומנת בנפרד, ותרופה יכולה לשאת את שני הסימונים.</p>
{table(["#", "מערכת", "תרופה / קבוצה", "נימוק", "בדיקות ייעודיות", "אושר"], red_rows, "small")}</section>'''
only_sec += f'''<section><h2>רשימה מרוכזת: הרפואן מכין, הרופא/ה מאשר/ת ({len(prep_rows)})</h2>
<p>בתרופות אלה יש רשימת בדיקות, אבל הרפואן לא מנפיק: מכין סיכום, והאישור הסופי בידי הרופא/ה.</p>
{table(["#", "מערכת", "תרופה / קבוצה", "מה נבדק", "אושר"], prep_rows, "small")}</section>'''


def toc_html(PG):
    g = lambda key: str(PG.get(key, "000"))
    rows = [("0", '<a href="#s0">עקרונות כלליים</a>', "", g("0A"), "", ""),
            ("", '<a href="#sonly">רשימה מרוכזת: רופא/ה בלבד</a>', str(len(only_rows)), g("OA"), "", "")]
    for i, k in enumerate(A["order"], 1):
        rows.append((str(i), f'<a href="#s{i}"><b>{E(A[k]["name"])}</b></a>', str(len(A[k]["drugs"])), g(f"{i}A"), g(f"{i}L"), g(f"{i}D")))
    return ('<table class="tocT"><thead><tr><th>#</th><th>פרק</th><th>פריטים</th><th>עמוד פתיחה</th><th>רשימה לסימון</th><th>פירוט מלא</th></tr></thead><tbody>'
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>")
general = f'''
<section><h1 id="s0">0. עקרונות כלליים<span class="mk">ZQ0AZ</span></h1>
<h2>מה הכלי עושה</h2>
<p>סטודנט/ית לרפואה המסייע/ת לרופא/ה (רפואן) מחדש/ת מרשמים כרוניים, מפיק/ה אישורים ועונה לפניות מקוונות לפי רשימת בדיקות קבועה לכל פריט. אין שיחה עם המטופל/ת בחידוש מרשם; הבדיקה מתבססת על הרשומה, הבדיקות והרכישות. הרפואן לא משנה מינון ולא מחליף תרופה.</p>
<h2>שלושה מסלולים בחידוש מרשם</h2>
{table(["מצב", "תוצאה", "פעולה"], [
    ("כל הבדיקות תקינות", "חידוש ל-3 חודשים (קלוזפין: חודש)", "—"),
    ("חסרה מדידה, בדיקה או ביקורת שנתית", "חידוש לחודש אחד", "זימון למרפאה להשלמה"),
    ("ערך חריג (מעל סף ההחזרה)", "חידוש לחודש אחד", "הודעה לרופא/ה"),
    ("התווית נגד או ערך חמור", "לא מחדשים", "הודעה לרופא/ה"),
    ("התראת אינטראקציה, אי-התאמה בכמות, ביחידות או בתדירות, או בקשה מוקדמת בתרופה ממכרת", "לא מחדשים עדיין", "ממתין לתשובת הרופא/ה"),
])}
<p>אין התווית נגד ← תמיד מחדשים לפחות לחודש אחד, כדי לא להפסיק טיפול. ביקור במרפאה אצל רופא/ת המשפחה פעם בשנה (אין ביקור: חידוש לחודש, זימון והודעה לרופא/ה); עד 3 חידושים רצופים ואז ביקור רופא, ובחידוש השלישי הודעה למטופל/ת שמומלצת ביקורת שנתית; רכישות 80% מהימים ומעלה ב-6 החודשים האחרונים.</p>
<h2>סימונים</h2>
<p>{pill("כן")} מתאים לרפואן · {pill("בתנאים")} רק טיפול כרוני במינון קבוע (ותנאים נוספים לפי התרופה) · {pill("הכנה")} הרפואן בודק ומכין, הרופא/ה מאשר/ת (אופיואידים, בנזודיאזפינים, תרופות שאינן כרוניות) · <span class="pill red">דגל אדום</span> הרפואן מכין, והרופא/ה בודק/ת שוב לפני האישור (סיכון גבוה יותר) · {pill("לא")} חידוש ע"י רופא/ה בלבד — הכלי מציג הודעה ולא רשימת בדיקות ·
<span class="pill tdm">מעקב צמוד</span> (⚗) תרופה עם מעקב תכוף (מעבדה, אק"ג, עיניים או צילום — לפי התרופה); בכלי מופיע פס אדום בראש הכרטיס עם המעקב הנדרש.</p>
<h2>תרופות עם כמה התוויות</h2>
<p>חוסמי בטא, מעכבי ACE ו-ARB בודדים, MRA, אנטרסטו, פוסיד, פורקסיגה, ג'רדיאנס, אוזמפיק/וגובי ומונג'רו: נבדקים רק תנאים משותפים לכל ההתוויות (טווח בטיחות ל"ד במקום יעד; בלי HbA1c). יעד הטיפול נבדק ע"י הרופא/ה בביקורת.</p>
<h2>תפקוד כליות לא תקין</h2>
<p>כשפריט תפקוד הכליות לא תקין, הרפואן רושם ערכי eGFR קודמים וסימון אם יש אבחנה של אי-ספיקת כליות כרונית, והם עוברים בהודעה לרופא/ה.</p>
<h2>טקסט התיעוד</h2>
<p>שורת כותרת עם הפריט והפרוטוקול · "הוקלד ע"י סטודנט/ית לרפואה המסייע/ת לרופא/ה [שם], בהוראת ד"ר [שם הרופא/ה]" · "כל הבדיקות לפי הפרוטוקול תקינות", או רק מה שלא תקין או חסר · התוצאה · מה הועבר למטופל/ת · מה הועבר לרופא/ה.</p>
<p>שני סימונים נפרדים מעל טקסט התיעוד ובשורת "סימון" בתוכו: <span class="pill" style="background:#c25a00;color:#fff;border-color:#c25a00">חריגה מהפרוטוקול</span> — התווית נגד, ממצא שעובר לרופא/ה, התראת אינטראקציה או אי-התאמה בכמות; הרופא/ה מחליט/ה. <span class="pill red">דגל אדום</span> — תרופה בסיכון גבוה יותר, בדיקה כפולה תמיד. תרופה יכולה לשאת את שניהם. ביומן התיעוד (Excel) — שתי עמודות נפרדות באותם צבעים.</p>
<p>התוצאה נבחרת אוטומטית לפי הסימונים (התווית נגד ← לא מחדשים; אינטראקציה או אי-התאמה ← ממתין; חסר או חריג ← חודש אחד; הכל תקין ← 3 חודשים). הסטודנט/ית יכול/ה לשנות ידנית. כל בדיקה מסומנת בנפרד.</p>
<h2>הנחיות כלליות לעבודה (ספר החפיפה, החלטות 3.11.2026)</h2>
{"".join(f"<h3>{E(h)}</h3>" + ul(items) for h, items in A.get("guide", []))}
<h2>מקורות</h2>
<p>ערכים שאין להם הנחיה בפרויקט מסומנים "החלטה מקומית (הצעה)" ומחכים לאישור. שמות מסחריים: מאגר התרופות של משרד הבריאות (קובץ 7.10.2026).</p>
</section>'''

body = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>פרוטוקולים לאישור — חוברת בקרה</title><style>
@font-face{{font-family:H;src:url(fonts/heebo-hebrew-400-normal.woff2)}}@font-face{{font-family:H;src:url(fonts/heebo-latin-400-normal.woff2);unicode-range:U+0000-024F}}
@font-face{{font-family:H;font-weight:700;src:url(fonts/heebo-hebrew-700-normal.woff2)}}@font-face{{font-family:H;font-weight:700;src:url(fonts/heebo-latin-700-normal.woff2);unicode-range:U+0000-024F}}
@font-face{{font-family:H;font-weight:500;src:url(fonts/heebo-hebrew-500-normal.woff2)}}@font-face{{font-family:H;font-weight:500;src:url(fonts/heebo-latin-500-normal.woff2);unicode-range:U+0000-024F}}
@page{{size:A4;margin:16mm 14mm 16mm 14mm}}
body{{font-family:H,sans-serif;font-size:9.4pt;line-height:1.45;color:#1b2430;margin:0}}
h1{{font-size:18pt;color:#13233D;border-bottom:2px solid #13233D;padding-bottom:4px;margin:0 0 8px;page-break-before:always}}
h3{{font-size:10.5pt;margin:8px 0 2px;color:#13233D}} h2{{font-size:12pt;color:#1F4E78;margin:14px 0 6px}} h2.pb{{page-break-before:always}}
p{{margin:4px 0}} ul{{margin:4px 0;padding-inline-start:18px}} li{{margin:1px 0}}
.meta{{color:#5b6573;font-size:8.6pt}}
table{{width:100%;border-collapse:collapse;margin:6px 0;page-break-inside:auto}} tr{{page-break-inside:avoid}}
th,td{{border:1px solid #c9d1db;padding:3px 5px;text-align:right;vertical-align:top}} thead th{{background:#13233D;color:#fff;font-weight:500}}
table.small{{font-size:8.2pt}} table.list{{font-size:8.4pt}} table.list td:nth-child(6){{text-align:center;width:28px}} table.list td:nth-child(7){{width:22%}}
table.kv th{{background:#eef2f7;color:#13233D;font-weight:500;width:18%;white-space:nowrap}}
table.checks{{font-size:8.6pt}} table.checks td:first-child{{width:16px;text-align:center}} table.checks td:nth-child(2){{width:24%;font-weight:500}} table.checks td:last-child{{width:52px;font-size:7.8pt;color:#8a2a2a}}
.item{{border:1px solid #9fb0c4;border-radius:6px;padding:6px 8px;margin:0 0 10px;page-break-inside:avoid}}
.item .dh{{font-size:11pt}} .item .num{{color:#5b6573;font-size:9pt}} .item .cls{{color:#5b6573;font-size:8.6pt;margin-bottom:3px}}
.q{{font-weight:400;color:#1F4E78;font-size:8pt}} .sev{{color:#a01c1c;font-weight:500}}
.pill{{display:inline-block;border-radius:999px;padding:0 7px;font-size:8pt;font-weight:500;border:1px solid}}
.pill.yes{{background:#e3f4e8;color:#1f6b35;border-color:#9fd3ae}} .pill.cond{{background:#fff4d6;color:#7a5600;border-color:#e8cf86}}
.pill.no{{background:#eceef1;color:#444;border-color:#b9c0c8}} .pill.red{{background:#a01c1c;color:#fff;border-color:#a01c1c}} .pill.tdm{{background:#a01c1c;color:#fff;border-color:#a01c1c}}
.ltr{{direction:ltr;unicode-bidi:isolate}}
.review{{margin-top:4px;font-size:8.4pt;color:#5b6573}}
.cover{{height:250mm;display:flex;flex-direction:column;justify-content:center;text-align:center}}
.cover h1{{border:0;font-size:30pt;page-break-before:avoid}} .cover .sub{{font-size:14pt;color:#1F4E78}} .cover .draft{{margin:18px auto;padding:8px 14px;border:1px solid #d9a3a3;background:#fbecec;color:#8a1f1f;border-radius:6px;max-width:130mm}}
.cover table{{max-width:120mm;margin:14px auto}}
.mk{{font-size:1px;color:#fff;position:absolute}} .tocT{{font-size:11pt}} .tocT td{{padding:5px 8px}} .tocT td:nth-child(n+3){{text-align:center;width:13%;font-weight:700;color:#13233D}} .tocT a{{color:#13233D;text-decoration:none}} .tocT thead th{{text-align:center}}
.toc h1{{page-break-before:always}} .toc ol{{list-style:none;padding:0;columns:1;font-size:12pt}} .toc li{{margin:6px 0}} .toc a{{color:#13233D;text-decoration:none}} .tn{{color:#5b6573;font-size:10pt}}
</style></head><body>
<div class="cover"><h1>פרוטוקולים לאישור</h1><div class="sub">חוברת בקרה — כל הפרוטוקולים, ההחלטות והתרופות</div>
<div class="draft"><b>טיוטה לבדיקה.</b> טרם אושר ע"י הייעוץ המשפטי וניהול סיכונים. לא לשימוש בפועל.</div>
{table(["", ""], [("פרוטוקולי תרופות (מערכות)", str(len(drug_tabs))), ("פריטי תרופות", str(len(all_drugs))),
                  ("שמות מסחריים", str(len({b["en"].lower() for d in all_drugs for b in d["brands"]}))),
                  ("מתאים / בתנאים / הכנה לרופא/ה / דגל אדום / רופא בלבד", f'{cnt["כן"]} / {cnt["בתנאים"]} / {cnt["הכנה"] - nred} / {nred} / {cnt["לא"]}'),
                  ("מעקב צמוד", str(sum(1 for d in all_drugs if d.get("tdm")))),
                  ("פרוטוקולים נוספים", " · ".join(A[k]["name"] + f' ({len(A[k]["drugs"])})' for k in kind_tabs)),
                  ("הופק", TODAY + " · מתוך הכלי שפורסם (asseoy.github.io/medical_aids/protocols-rofan.html)")])}
<p>ד"ר יונתן אסיאו · asseo_y@mac.org.il</p></div>
<div class="toc"><h1>תוכן העניינים</h1>__TOC__
<p class="meta">בכל פרק: א. כללים · ב. תוצאות (באישורים ובפניות) · ג. בדיקות משותפות · ד. החלטות · ה. רשימה לסימון · ו. פירוט מלא של כל פריט עם משבצת אישור.</p></div>
{general}
{only_sec}
{"".join(section(i, k) for i, k in enumerate(A["order"], 1))}
</body></html>'''

os.makedirs(OUT + "fonts", exist_ok=True)
for f in os.listdir(S + "fonts"):
    shutil.copy(S + "fonts/" + f, OUT + "fonts/" + f)
from playwright.sync_api import sync_playwright
import subprocess, re


def render(PG):
    open(OUT + "booklet.html", "w").write(body.replace("__TOC__", toc_html(PG)))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://" + OUT + "booklet.html"); pg.wait_for_timeout(500)
        pg.pdf(path=OUT + "booklet.pdf", format="A4", print_background=True, outline=True, tagged=True,
               display_header_footer=True, margin=dict(top="16mm", bottom="16mm", left="14mm", right="14mm"),
               header_template='<div style="font-size:7pt;color:#888;width:100%;text-align:center;font-family:sans-serif">Protocols for approval — review booklet (draft)</div>',
               footer_template='<div style="font-size:8pt;color:#666;width:100%;text-align:center;font-family:sans-serif"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
        b.close()
    txt = subprocess.run(["pdftotext", OUT + "booklet.pdf", "-"], capture_output=True, text=True).stdout
    found = {}
    for n, page in enumerate(txt.split("\f"), 1):
        for m in re.findall(r"ZQ(\w+?)Z", page):
            found.setdefault(m, n)
    return found


PG = render({})          # pass 1: placeholder page numbers (same width), find where each chapter landed
PG2 = render(PG)         # pass 2: real page numbers
assert PG2 == PG, "page numbers moved between passes"
shutil.copy(OUT + "booklet.pdf", REPO + "protocols-rofan-booklet.pdf")   # linked from every tab of the tool
print("booklet", os.path.getsize(OUT + "booklet.pdf") // 1024, "KB")
