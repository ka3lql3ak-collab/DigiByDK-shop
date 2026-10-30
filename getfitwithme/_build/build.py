#!/usr/bin/env python3
"""Builds the Get Fit With Me store.

    python3 getfitwithme/_build/build.py          # app pages, store page, Stan copy
    python3 getfitwithme/_build/build.py --pdf    # + PDF books (with fillable workbook) and cover images

Each product lands in a private access folder getfitwithme/p/<token>/:
  index.html  "thank you" access page (the link you give buyers through Stan)
  app.html    the interactive app
  <Title>.pdf the PDF book with fillable workbook
Plus covers/<slug>.png, index.html (store preview, no product links), STAN-STORE-COPY.md
and download/Get-Fit-With-Me-Products.zip with everything."""
import html, io, json, os, re, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content as C  # noqa: E402
from library import LIB  # noqa: E402

e = html.escape
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@600;700;800&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">')


# ================================================================ brand assets (purple)
import base64
BRAND = os.path.join(OUT, "brand")
def datauri(name, mime): return f"data:{mime};base64," + base64.b64encode(open(os.path.join(BRAND, name), "rb").read()).decode()
BODY = datauri("body-cutout.webp", "image/webp")      # Danielle's physique cutout
MARK = datauri("logo-mark-256.webp", "image/webp")    # round face logo
LOGO = datauri("logo-600.webp", "image/webp")         # full stacked logo
FAV = datauri("favicon.png", "image/png")
ICON = f'<link rel="icon" href="{FAV}"><link rel="apple-touch-icon" href="{MARK}">'


# ================================================================ markdown → html
def inline(t):
    t = e(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def md(src, qprefix, print_mode=False):
    """Small markdown subset: ###, paragraphs, lists (+ nested under ol), tables, > callouts, ::quiz blocks."""
    lines, out, quizzes, i = src.strip("\n").split("\n"), [], 0, 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith("::quiz"):
            q, opts, ans, ex = "", [], 0, ""
            i += 1
            while not lines[i].startswith("::"):
                l2 = lines[i]
                if l2.startswith("Q:"): q = l2[2:].strip()
                elif l2.startswith("E:"): ex = l2[2:].strip()
                elif l2[:2] in ("- ", "* "):
                    if l2[0] == "*": ans = len(opts)
                    opts.append(l2[2:].strip())
                i += 1
            i += 1
            qid = f"{qprefix}-{quizzes}"; quizzes += 1
            if print_mode:
                L = "ABCD"
                out.append(f'<div class="quiz"><div class="q-k">Check your understanding</div><p class="q-q">{inline(q)}</p><ol class="q-o" type="A">{"".join(f"<li>{inline(o)}</li>" for o in opts)}</ol>'
                           f'<p class="q-a"><b>Answer: {L[ans]}.</b> {inline(ex)}</p></div>')
            else:
                out.append(f'<div class="quiz" data-qid="{qid}" data-ans="{ans}" data-exp="{e(ex)}"><div class="q-k">Check your understanding</div><p class="q-q">{inline(q)}</p>'
                           + "".join(f'<button class="opt" data-i="{k}"><span>{"ABCD"[k]}</span>{inline(o)}</button>' for k, o in enumerate(opts)) + '<p class="qexp" hidden></p></div>')
            continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>"); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells): rows.append(cells)
                i += 1
            head, body = rows[0], rows[1:]
            out.append('<div class="table-wrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>")
            continue
        if ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip()); i += 1
            out.append(f'<aside class="callout"><p>{inline(" ".join(buf))}</p></aside>'); continue
        m = re.match(r"(\d+)\. |- ", ln)
        if m:
            tag = "ol" if ln[0].isdigit() else "ul"
            items = []
            while i < len(lines) and (re.match(r"(\d+)\. |- ", lines[i]) or re.match(r"\s{2,}- ", lines[i])):
                l2 = lines[i]
                if re.match(r"\s{2,}- ", l2):
                    items[-1][1].append(l2.strip()[2:])
                else:
                    items.append([re.sub(r"^(\d+\. |- )", "", l2), []])
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(t)}" + (f"<ul>{''.join(f'<li>{inline(s)}</li>' for s in sub)}</ul>" if sub else "") + "</li>" for t, sub in items) + f"</{tag}>")
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(### |\||> |::|\d+\. |- )", lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)


def load_guide(name, print_mode=False):
    src = open(os.path.join(HERE, "guides", name + ".md"), encoding="utf-8").read()
    chapters = []
    for n, part in enumerate(re.split(r"^## ", src, flags=re.M)[1:]):
        title, body = part.split("\n", 1)
        h = md(body, f"c{n}", print_mode)
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r'<div class="quiz".*?</div>', "", h, flags=re.S))).strip()
        chapters.append({"t": title.strip(), "html": h, "text": html.unescape(text), "min": max(2, round(len(text.split()) / 220))})
    return chapters


def pdf_name(p): return re.sub(r"[^A-Za-z0-9]+", "-", p["title"]).strip("-") + ".pdf"
def folder(p): return os.path.join(OUT, "p", p["token"])
def access_url(p): return f"{C.SITE}/p/{p['token']}/"


def lib_for(p):
    names = []
    for s in p["sections"]:
        if s["type"] == "program":
            for w in s["weeks"]:
                for d in w["days"]:
                    for x in d["ex"]:
                        if x["n"] not in names: names.append(x["n"])
    return {n: LIB[n] for n in sorted(names)}


# ================================================================ app styles
TOKENS = """
:root{--bg:#f7f4fb;--surface:#fff;--surface2:#efeaf6;--ink:#17121f;--ink2:#3a3245;--mut:#6c6478;--line:#e4dcee;
 --acc:#6b2fd6;--acc2:#7f45ea;--acc-ink:#fff;--acc-soft:#efe6ff;--ok:#2f7d5b;--warn:#b25b12;--shadow:0 1px 2px rgba(23,20,26,.04),0 8px 24px -12px rgba(23,20,26,.12);
 --r:16px;--font:Inter,system-ui,-apple-system,Segoe UI,sans-serif;--head:"Inter Tight",Inter,system-ui,sans-serif;--serif:"Instrument Serif",Georgia,serif;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f0c15;--surface:#18141f;--surface2:#221c2b;--ink:#f4eff2;--ink2:#d9d1d7;--mut:#a59ba6;--line:#2d282f;
 --acc:#b48cff;--acc2:#c9abff;--acc-ink:#1a0d33;--acc-soft:#2a1a45;--ok:#5cc196;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px -12px rgba(0,0,0,.6);color-scheme:dark}}
:root[data-theme=dark]{--bg:#0f0c15;--surface:#18141f;--surface2:#221c2b;--ink:#f4eff2;--ink2:#d9d1d7;--mut:#a59ba6;--line:#2d282f;
 --acc:#b48cff;--acc2:#c9abff;--acc-ink:#1a0d33;--acc-soft:#2a1a45;--ok:#5cc196;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px -12px rgba(0,0,0,.6);color-scheme:dark}
"""

APP_CSS = TOKENS + """
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.55 var(--font);-webkit-font-smoothing:antialiased}
a{color:var(--acc)}
.ic{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}.ic.sm{width:15px;height:15px}
.app{display:grid;grid-template-columns:minmax(0,1fr);min-height:100vh}
.side,.content{min-width:0}
.side{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.brandbar{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px 4px}
.wordmark{font:800 12px/1 var(--head);letter-spacing:.18em;text-transform:uppercase;color:var(--ink)}
.wordmark span{color:var(--acc)}
.brandlock{display:flex;align-items:center;gap:10px}.bmark{width:34px;height:34px;border-radius:50%;box-shadow:0 0 0 2px var(--acc-soft)}
.hero{position:relative}.hero-body{display:none}
@media (min-width:760px){.content .hero{padding-right:230px;min-height:460px}.hero-body{display:block;position:absolute;right:16px;top:40px;height:390px;aspect-ratio:922/2082;border-radius:22px;overflow:hidden;background:url(BODYURI) left top/100% 100% no-repeat,radial-gradient(90% 60% at 100% 0%,#a46bff,transparent 70%),linear-gradient(160deg,#5b22c4,#24104f);box-shadow:0 20px 40px -18px rgba(60,20,120,.55)}}
.iconbtn{display:inline-grid;place-items:center;width:38px;height:38px;border-radius:12px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}
.side-title,.side-prog,.side-foot{display:none}
#nav{display:flex;gap:4px;overflow-x:auto;padding:8px 12px 10px;scrollbar-width:none}
#nav::-webkit-scrollbar{display:none}
#nav button{flex:none;border:0;background:none;color:var(--mut);font:600 14px var(--font);padding:8px 12px;border-radius:10px;cursor:pointer;white-space:nowrap}
#nav button.on{background:var(--ink);color:var(--bg)}
.content{min-width:0}
.hero{padding:28px 16px 8px;max-width:820px;margin:0 auto}
.kicker{font:600 12px var(--font);letter-spacing:.14em;text-transform:uppercase;color:var(--acc)}
.hero h1{font:800 clamp(32px,7vw,52px)/1.02 var(--head);letter-spacing:-.025em;margin:10px 0 10px}
.hero .by{font:italic 400 20px var(--serif);color:var(--mut);margin:0 0 12px}
.hero .sub{color:var(--ink2);margin:0 0 16px;max-width:560px;font-size:17px}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px;padding:0;list-style:none}
.meta li{font:600 12.5px var(--font);border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:6px 11px;color:var(--ink2)}
.overall{display:flex;align-items:center;gap:12px;font:600 13px var(--font);color:var(--mut)}
.overall .track{flex:1;max-width:320px}
main{max-width:820px;margin:0 auto;padding:8px 16px 140px}
.sec-head h2{font:800 26px/1.1 var(--head);letter-spacing:-.02em;margin:22px 0 14px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:20px;margin:0 0 14px;box-shadow:var(--shadow)}
.card.complete{border-color:color-mix(in srgb,var(--ok) 50%,var(--line))}
.card h3{font:700 20px/1.2 var(--head);letter-spacing:-.01em;margin:4px 0 0}
.card h4{font:700 13px var(--font);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin:22px 0 8px}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:10px}
.card-head select{max-width:52%}
.eyebrow{display:block;font:600 11.5px var(--font);letter-spacing:.12em;text-transform:uppercase;color:var(--acc)}
.muted{color:var(--mut);font-size:14.5px}.fine{color:var(--mut);font-size:12.5px;line-height:1.5}.center{text-align:center}
.badge{flex:none;font:700 12px var(--font);color:var(--ok);background:color-mix(in srgb,var(--ok) 12%,transparent);border-radius:999px;padding:5px 10px}
.pill{flex:none;font:600 12px var(--font);color:var(--acc);background:var(--acc-soft);border-radius:999px;padding:4px 9px;white-space:nowrap}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:1px solid transparent;border-radius:12px;padding:12px 18px;font:600 15px var(--font);cursor:pointer;text-decoration:none;transition:transform .08s,background .15s}
.btn:active{transform:scale(.98)}
.btn.primary{background:var(--acc);color:var(--acc-ink)}.btn.primary:hover{background:var(--acc2)}
.btn.ghost{background:var(--surface);border-color:var(--line);color:var(--ink)}
.btn.danger{background:none;border-color:#c0392b;color:#c0392b}
.btn.wide{width:100%;margin-top:14px}
.link{background:none;border:0;padding:0;color:var(--acc);font:600 14px var(--font);cursor:pointer}
.row-between{display:flex;justify-content:space-between;gap:10px;margin-top:16px}
input,select,textarea{font:500 16px var(--font);color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 12px;width:100%;min-width:0}
input:focus,select:focus,textarea:focus{outline:2px solid var(--acc);outline-offset:-1px;border-color:transparent}
textarea{min-height:92px;resize:vertical;line-height:1.5}
.meter{margin:0 0 16px}.meter-top{display:flex;justify-content:space-between;font:600 13px var(--font);color:var(--mut);margin-bottom:6px}
.track{height:6px;border-radius:99px;background:var(--surface2);overflow:hidden}.track i{display:block;height:100%;background:var(--acc);border-radius:99px;transition:width .4s}
.search{position:relative;margin:0 0 12px}.search svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:18px;height:18px;fill:none;stroke:var(--mut);stroke-width:2}
.search input{padding-left:38px;height:46px}
/* guide */
.toc{list-style:none;margin:0;padding:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow)}
.toc li+li{border-top:1px solid var(--line)}
.toc-row{all:unset;box-sizing:border-box;display:grid;grid-template-columns:40px 1fr auto;gap:12px;align-items:center;width:100%;padding:15px 16px;cursor:pointer}
.toc-row:hover{background:var(--surface2)}
.toc-n{font:700 14px var(--head);color:var(--mut)}.toc-t{font:600 15.5px/1.35 var(--font)}.toc-m{font:500 12.5px var(--font);color:var(--mut)}
.toc-row.is-read .toc-n{color:var(--ok)}.ic.ok{color:var(--ok)}
.snip{display:block;font:400 13px/1.45 var(--font);color:var(--mut);margin-top:4px}.snip mark{background:var(--acc-soft);color:var(--acc);border-radius:3px;padding:0 2px}
.reader-bar{display:flex;justify-content:space-between;align-items:center;gap:10px;font:500 13px var(--font);color:var(--mut);margin-bottom:6px}
.prose{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:clamp(20px,5vw,40px);box-shadow:var(--shadow);font-size:17px;line-height:1.7}
.prose h2{font:800 clamp(26px,5vw,34px)/1.12 var(--head);letter-spacing:-.02em;margin:0 0 18px}
.prose h3{font:700 19px/1.3 var(--head);margin:30px 0 8px}
.prose p{margin:0 0 14px}.prose ul,.prose ol{padding-left:22px;margin:0 0 16px}.prose li{margin:6px 0}.prose li::marker{color:var(--acc);font-weight:700}
.prose strong{font-weight:650;color:var(--ink)}
.callout{border-left:3px solid var(--acc);background:var(--acc-soft);border-radius:0 12px 12px 0;padding:14px 18px;margin:20px 0}.callout p{margin:0;font-size:15.5px}
.table-wrap{overflow-x:auto;margin:16px 0 20px;border:1px solid var(--line);border-radius:12px}
.tbl{width:100%;border-collapse:collapse;font-size:14.5px;line-height:1.45}
.tbl th{text-align:left;font:700 12px var(--font);letter-spacing:.06em;text-transform:uppercase;color:var(--mut);background:var(--surface2);padding:10px 12px;white-space:nowrap}
.tbl td{padding:10px 12px;border-top:1px solid var(--line);vertical-align:top}
.tbl tr.hl td{font-weight:700;color:var(--acc)}
.card>.tbl{border:1px solid var(--line);border-radius:12px;overflow:hidden;border-collapse:separate;border-spacing:0}
.quiz{border:1px solid var(--line);border-radius:14px;padding:18px;margin:24px 0;background:var(--surface2)}
.q-k{font:700 11.5px var(--font);letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:6px}
.q-q{font-weight:650;margin:0 0 12px!important}
.opt{display:flex;gap:12px;align-items:center;width:100%;text-align:left;font:500 15px var(--font);color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:11px 12px;margin:6px 0;cursor:pointer}
.opt span{display:grid;place-items:center;flex:none;width:26px;height:26px;border-radius:8px;background:var(--surface2);font-weight:700;font-size:13px}
.opt:hover:not(:disabled){border-color:var(--acc)}
.opt.right{border-color:var(--ok);background:color-mix(in srgb,var(--ok) 10%,var(--surface))}.opt.right span{background:var(--ok);color:#fff}
.opt.wrong{border-color:#c0392b;background:color-mix(in srgb,#c0392b 8%,var(--surface))}.opt.wrong span{background:#c0392b;color:#fff}
.opt:disabled{cursor:default}
.qexp{margin:10px 0 0!important;font-size:15px}
.reader-foot{display:flex;justify-content:space-between;gap:10px;margin-top:16px}
/* program */
.seg{display:flex;gap:4px;padding:4px;background:var(--surface2);border-radius:12px;overflow-x:auto;scrollbar-width:none;margin:0 0 14px}
.seg::-webkit-scrollbar{display:none}
.seg button{flex:1 0 auto;border:0;background:none;color:var(--mut);font:600 13.5px var(--font);padding:9px 12px;border-radius:9px;cursor:pointer;white-space:nowrap}
.seg button.on{background:var(--surface);color:var(--ink);box-shadow:var(--shadow)}.seg button.done:not(.on){color:var(--ok)}
.phase{background:var(--ink);color:var(--bg);border-radius:var(--r);padding:16px 18px;margin:0 0 14px}
.phase .eyebrow{color:color-mix(in srgb,var(--bg) 70%,var(--acc))}.phase p{margin:4px 0 0;font-size:15px;opacity:.9}
.day{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);margin:0 0 12px;box-shadow:var(--shadow);overflow:hidden}
.day.complete{border-color:color-mix(in srgb,var(--ok) 45%,var(--line))}
.day-head{all:unset;box-sizing:border-box;display:grid;grid-template-columns:36px 1fr auto 20px;gap:12px;align-items:center;width:100%;padding:16px;cursor:pointer}
.day-status{display:grid;place-items:center;width:36px;height:36px;border-radius:10px;background:var(--surface2);font:700 15px var(--head)}
.day.complete .day-status{background:var(--ok);color:#fff}
.day-title b{display:block;font:700 16px/1.3 var(--head)}.day-title small{display:block;color:var(--mut);font-size:13px;line-height:1.35;margin-top:2px}
.day-count{font:600 12.5px var(--font);color:var(--mut)}
.chev{color:var(--mut);transition:transform .2s}.day.open .chev,details[open] .chev{transform:rotate(180deg)}
.day-body{padding:0 16px 18px}
.ex{border-top:1px solid var(--line);padding:16px 0}
.ex-head{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 12px;align-items:baseline}
.ex-name{all:unset;cursor:pointer;font:700 16px var(--head);display:inline-flex;gap:6px;align-items:center}.ex-name svg{color:var(--mut)}
.ex-name:hover{color:var(--acc)}
.ex-meta{display:flex;gap:6px;flex-wrap:wrap}.ex-meta span{font:600 12px var(--font);color:var(--ink2);background:var(--surface2);border-radius:7px;padding:4px 8px}
.last{font-size:13px;color:var(--mut);margin:8px 0 0}.last b{color:var(--ink2)}
.sets{margin-top:10px}
.set-h,.set{display:grid;grid-template-columns:34px 1fr 1fr 46px;gap:8px;align-items:center}
.set-h{font:700 11px var(--font);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);padding:0 0 4px}
.set{margin:6px 0}.set input{height:44px;text-align:center;font-weight:600}
.set-n{display:grid;place-items:center;height:44px;font:700 14px var(--head);color:var(--mut)}
.tick{display:grid;place-items:center;height:44px;border-radius:10px;border:1.5px solid var(--line);background:var(--surface);color:transparent;cursor:pointer;transition:.15s}
.set.on .tick{background:var(--ok);border-color:var(--ok);color:#fff}
.set.on input{background:color-mix(in srgb,var(--ok) 7%,var(--surface));border-color:color-mix(in srgb,var(--ok) 35%,var(--line))}
.notes{display:block;margin-top:14px}.notes span{display:block;font:700 12px var(--font);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin-bottom:6px}
/* challenge */
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:0 0 14px}
.stats div{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px;box-shadow:var(--shadow)}
.stats b{display:block;font:800 28px/1 var(--head)}.stats span{font-size:12.5px;color:var(--mut)}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin:0 0 14px}
.cal button{aspect-ratio:1;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:600 14px var(--font);cursor:pointer}
.cal button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}.cal button.sel{outline:2px solid var(--acc);outline-offset:2px}
.moves{list-style:none;padding:0;margin:8px 0}.moves li{display:flex;justify-content:space-between;gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}
.moves b{color:var(--acc);white-space:nowrap}
.rounds{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.rounds button{flex:1;border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:10px;font:600 14px var(--font);color:var(--ink);cursor:pointer}
.rounds button.on{background:var(--ok);border-color:var(--ok);color:#fff}
.check{display:flex;gap:12px;align-items:center;padding:12px;border-radius:12px;border:1px solid var(--line);margin:8px 0;cursor:pointer;user-select:none;transition:.15s;background:var(--surface)}
.check .box{display:grid;place-items:center;width:24px;height:24px;flex:none;border-radius:7px;border:1.5px solid var(--mut);color:transparent}
.check.done{background:var(--surface2)}.check.done .box{background:var(--ok);border-color:var(--ok);color:#fff}.check.done span:last-child{color:var(--mut);text-decoration:line-through}
.prompt{font:italic 400 22px/1.35 var(--serif);margin:6px 0 12px;padding:0;color:var(--ink)}
/* progress */
.chart{width:100%;height:auto;display:block;margin:6px 0}
.chart .grid{stroke:var(--line);stroke-dasharray:3 4}.chart text{fill:var(--mut);font:500 12px var(--font)}
.chart .line{fill:none;stroke:var(--acc);stroke-width:2.5;stroke-linejoin:round}.chart .area{fill:var(--acc);opacity:.08}
.chart circle{fill:var(--surface);stroke:var(--acc);stroke-width:2.5}
.up{color:var(--ok)}
.empty{border:1.5px dashed var(--line);border-radius:12px;padding:22px;text-align:center;color:var(--mut);font-size:14.5px;margin:6px 0}
.pr-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
.pr{border:1px solid var(--line);border-radius:12px;padding:12px}.pr span{display:block;font:600 13px var(--font);color:var(--mut)}
.pr b{display:block;font:800 20px var(--head);margin-top:4px}.pr small{color:var(--mut);font-size:12.5px}.pr.has{border-color:color-mix(in srgb,var(--acc) 40%,var(--line))}
.add{margin-top:14px}.add summary{cursor:pointer;color:var(--acc);font-weight:600;font-size:14px}
.form3{display:grid;grid-template-columns:1fr;gap:8px;margin-top:10px}
.form-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:10px 0}.form-grid.two{grid-template-columns:1fr 1fr}
.form-grid label{display:grid;gap:5px;font:600 12.5px var(--font);color:var(--mut)}.form-grid .full{grid-column:1/-1}.form-grid small{font-weight:500}
.x{background:none;border:0;color:var(--mut);font-size:20px;cursor:pointer;line-height:1}
.kpis{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:14px 0}.kpis.four{grid-template-columns:repeat(4,1fr)}
.kpi{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:var(--surface)}
.kpi span{display:block;font:600 12px var(--font);color:var(--mut);letter-spacing:.04em}.kpi b{display:block;font:800 24px/1.15 var(--head);margin-top:2px}.kpi small{color:var(--mut);font-size:12px}
.kpi.big{grid-column:1/-1;background:var(--ink);color:var(--bg);border-color:var(--ink)}.kpi.big span,.kpi.big small{color:color-mix(in srgb,var(--bg) 70%,transparent)}.kpi.big b{font-size:40px}
.split{display:flex;height:10px;border-radius:99px;overflow:hidden;margin:4px 0 10px}.split .p{background:var(--acc)}.split .c{background:#d9a441}.split .f{background:#5b8c85}
.plate{display:inline-grid;place-items:center;min-width:38px;height:38px;border-radius:8px;margin:2px;font:700 13px var(--font);color:#fff;background:#444}
.plate.p45{background:#b0273f}.plate.p35{background:#c28e0e}.plate.p25{background:#2e7d4f}.plate.p10{background:#3b5ba5}.plate.p5{background:#666}.plate.p2_5{background:#999}
/* library & recipes */
.chips{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;margin:0 0 14px}.chips::-webkit-scrollbar{display:none}
.chips button{flex:none;border:1px solid var(--line);background:var(--surface);color:var(--ink2);font:600 13.5px var(--font);padding:8px 13px;border-radius:999px;cursor:pointer}
.chips button.on{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.lib{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.lib-card{all:unset;box-sizing:border-box;cursor:pointer;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px;box-shadow:var(--shadow);transition:border-color .15s}
.lib-card:hover{border-color:var(--acc)}.lib-card b{display:block;font:700 16px/1.3 var(--head);margin:6px 0 4px}.lib-card small{color:var(--mut);font-size:13px;line-height:1.4;display:block}
.macros-mini{display:flex;gap:10px;flex-wrap:wrap;font:600 12.5px var(--font);color:var(--mut);margin-top:6px}
.meal{border-top:1px solid var(--line);padding:14px 0}.meal-row{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.meal-row p{margin:4px 0 6px;font-weight:500}
.acc{border-bottom:1px solid var(--line)}.acc:last-child{border-bottom:0}
.acc summary{list-style:none;display:flex;justify-content:space-between;gap:12px;align-items:center;cursor:pointer;padding:14px 0;font:650 16px var(--font)}
.acc summary::-webkit-details-marker{display:none}.acc p{margin:0 0 16px;color:var(--ink2)}
.ups{display:grid;gap:8px;margin:14px 0}
.up{display:flex;justify-content:space-between;align-items:center;gap:12px;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:12px;padding:14px}
.up:hover{border-color:var(--acc)}.up b{display:block;font:700 15px var(--head)}.up small{color:var(--mut);font-size:13px}.up em{font-style:normal;font-weight:700;color:var(--acc)}
/* sheet */
#sheet{width:min(640px,100vw);max-width:100vw;max-height:min(92vh,900px);margin:auto auto 0;border:0;border-radius:20px 20px 0 0;padding:0;background:var(--surface);color:var(--ink);box-shadow:0 -10px 40px rgba(0,0,0,.25)}
@media(min-width:700px){#sheet{margin:auto;border-radius:20px}}
#sheet::backdrop{background:rgba(15,13,16,.55);backdrop-filter:blur(3px)}
#sheetClose{position:sticky;top:12px;float:right;margin:12px 12px 0 0;z-index:2}
#sheetBody{padding:24px 22px 32px;overflow:auto}
#sheetBody h2{font:800 28px/1.15 var(--head);letter-spacing:-.02em;margin:6px 0 8px}
#sheetBody h4{font:700 12.5px var(--font);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin:22px 0 8px}
#sheetBody ol,#sheetBody ul{padding-left:20px;margin:0}#sheetBody li{margin:6px 0}
.cues li::marker{color:var(--ok)}.mist li::marker{color:#c0392b}
.vars{display:grid;grid-template-columns:1fr;gap:10px;margin-top:20px}.vars div{background:var(--surface2);border-radius:12px;padding:12px 14px}.vars p{margin:4px 0 0;font-size:14.5px}
/* timer + toast */
#tfab{position:fixed;right:16px;bottom:16px;z-index:30;display:grid;place-items:center;width:56px;height:56px;border-radius:50%;border:0;background:var(--ink);color:var(--bg);cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.25)}
#timer{position:fixed;right:16px;bottom:84px;z-index:30;width:min(300px,calc(100vw - 32px));background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:18px;box-shadow:0 20px 50px rgba(0,0,0,.25);text-align:center;opacity:0;transform:translateY(10px);pointer-events:none;transition:.2s}
#timer.open{opacity:1;transform:none;pointer-events:auto}
.tdial{position:relative;width:140px;height:140px;margin:6px auto 10px}.tdial svg{width:100%;height:100%;transform:rotate(-90deg)}
.tdial circle{fill:none;stroke-width:6}.tdial .bg{stroke:var(--surface2)}.tdial .fg{stroke:var(--acc);stroke-linecap:round;stroke-dasharray:283;transition:stroke-dashoffset .25s linear}
#tnum{position:absolute;inset:0;display:grid;place-items:center;font:800 34px var(--head);font-variant-numeric:tabular-nums}
.tbtns{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}.tbtns button{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:9px;padding:8px 0;font:600 13px var(--font);cursor:pointer}
@media (max-width:999px){
 #timer{left:12px;right:80px;bottom:16px;width:auto;padding:8px 10px 8px 14px;display:flex;align-items:center;gap:8px;text-align:left;border-radius:16px}
 #timer>.eyebrow,#timer>.fine,.tdial svg{display:none}
 .tdial{width:auto;height:auto;margin:0}#tnum{position:static;display:block;font-size:24px;min-width:60px}
 .tbtns{display:flex;gap:5px;margin-left:auto}.tbtns button{padding:8px 9px;white-space:nowrap}
 #timer.run .tbtns [data-t="60"],#timer.run .tbtns [data-t="90"],#timer.run .tbtns [data-t="120"],#timer.run .tbtns [data-t="180"],#timer:not(.run) .tbtns [data-t="+15"],#timer:not(.run) .tbtns [data-t="stop"]{display:none}
 .tbtns [data-t="hide"]{grid-column:auto!important}
}
#toast{position:fixed;left:50%;bottom:24px;z-index:40;transform:translate(-50%,calc(100% + 40px));opacity:0;background:var(--ink);color:var(--bg);font:600 14.5px var(--font);padding:12px 18px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.25);transition:transform .3s;max-width:calc(100vw - 32px);text-align:center}
#toast.show{transform:translate(-50%,0);opacity:1}
footer{max-width:820px;margin:0 auto;padding:0 16px 120px;color:var(--mut);font-size:12.5px;line-height:1.6}
@media (min-width:1000px){
 .app{grid-template-columns:280px minmax(0,1fr)}
 .side{height:100vh;border-bottom:0;border-right:1px solid var(--line);display:flex;flex-direction:column;background:var(--surface)}
 .brandbar{padding:24px 22px 0}.brandbar .iconbtn{display:none}
 .side-title{display:block;padding:18px 22px 4px;font:700 17px/1.3 var(--head)}
 .side-prog{display:block;padding:8px 22px 14px}.side-prog .meter-top{font-size:12px}
 #nav{flex-direction:column;overflow:visible;padding:8px 12px;gap:2px;flex:1}
 #nav button{text-align:left;padding:10px 12px;font-size:14.5px}
 #nav button.on{background:var(--acc-soft);color:var(--acc)}
 .side-foot{display:grid;gap:8px;padding:16px 22px 24px;border-top:1px solid var(--line)}
 .hero{padding-top:56px}.hero .overall{display:none}
 .form3{grid-template-columns:2fr 1fr 1fr auto}
 .vars{grid-template-columns:repeat(3,1fr)}
}
@media (max-width:520px){.form-grid{grid-template-columns:1fr 1fr}.kpis.four{grid-template-columns:1fr 1fr}.prose{font-size:16.5px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

GEAR = '<svg viewBox="0 0 24 24" class="ic"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>'


def others():
    o = [{"slug": p["slug"], "short": p["short"], "sub": p["stan"]["thumb_sub"], "price": p["stan"]["price"]} for p in C.PRODUCTS]
    o.insert(1, {"slug": "complete-collection", "short": "The Complete Collection", "sub": C.BUNDLE["thumb_sub"], "price": C.BUNDLE["price"]})
    return o


def product_page(p, engine):
    has_prog = any(s["type"] == "program" for s in p["sections"])
    data = {"slug": p["slug"], "sections": p["sections"], "guide": [{k: c[k] for k in ("t", "html", "text", "min")} for c in load_guide(p["guide"])],
            "lib": lib_for(p), "recipes": C.RECIPES if any(s["type"] == "recipes" for s in p["sections"]) else None,
            "others": others(), "pdf": pdf_name(p), "stan": C.STAN_URL}
    timer = ('<button id="tfab" aria-label="Rest timer"><svg viewBox="0 0 24 24" class="ic"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2 2M9 2h6"/></svg></button>'
             '<div id="timer" role="dialog" aria-label="Rest timer"><span class="eyebrow">Rest timer</span><div class="tdial"><svg viewBox="0 0 100 100"><circle class="bg" cx="50" cy="50" r="45"/><circle class="fg" id="tring" cx="50" cy="50" r="45"/></svg><div id="tnum">0:00</div></div>'
             '<div class="tbtns"><button data-t="60">1:00</button><button data-t="90">1:30</button><button data-t="120">2:00</button><button data-t="180">3:00</button><button data-t="+15">+15s</button><button data-t="stop">Stop</button><button data-t="hide" style="grid-column:span 2" aria-label="Hide timer">Hide</button></div>'
             '<p class="fine">Starts automatically when you complete a set.</p></div>') if has_prog else ""
    nav = "".join(f'<button data-tab="{s["id"]}">{e(s["label"])}</button>' for s in p["sections"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#f7f4fb" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0f0c15" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="{e(p['short'])}">
<meta name="description" content="{e(p['sub'])}"><meta name="robots" content="noindex,nofollow">
<title>{e(p['title'])} · {C.BRAND}</title>
{ICON}
{FONTS}<style>{APP_CSS.replace("BODYURI", BODY)}</style></head><body>
<div class="app">
 <aside class="side">
  <div class="brandbar"><div class="brandlock"><img class="bmark" src="{MARK}" alt="Danielle Dawson logo"><div class="wordmark">Get Fit <span>With Me</span></div></div><button class="iconbtn" id="settingsBtn" aria-label="Settings">{GEAR}</button></div>
  <div class="side-title">{e(p['title'])}</div>
  <div class="side-prog"><div class="meter-top"><span>Overall progress</span><span id="overallN2"></span></div><div class="track"><i id="overall2"></i></div></div>
  <nav id="nav" aria-label="Sections">{nav}</nav>
  <div class="side-foot"><a class="btn ghost" href="{pdf_name(p)}" download>Download PDF book</a><button class="btn ghost" id="settingsBtn2">Settings & backup</button></div>
 </aside>
 <div class="content">
  <header class="hero"><div class="hero-body" role="img" aria-label="Danielle Dawson"></div><span class="kicker">{e(p['kicker'])}</span><h1>{e(p['title'])}</h1><p class="by">by {e(C.COACH)}</p><p class="sub">{e(p['sub'])}</p>
   <ul class="meta">{''.join(f'<li>{e(m)}</li>' for m in p['meta'])}</ul>
   <div class="overall"><div class="track"><i id="overall"></i></div><span id="overallN">0%</span></div></header>
  <main id="main"></main>
  <footer>{e(C.DISCLAIMER)}<br>© 2026 {e(C.COACH)} · {e(C.BRAND)}. Licensed for personal use only. Please don't share or resell.</footer>
 </div>
</div>
{timer}
<dialog id="sheet"><button class="iconbtn" id="sheetClose" aria-label="Close"><svg viewBox="0 0 24 24" class="ic"><path d="M18 6 6 18M6 6l12 12"/></svg></button><div id="sheetBody"></div></dialog>
<div id="toast" role="status" aria-live="polite"></div>
<script>window.P={json.dumps(data, ensure_ascii=False)};
{engine}
(function(){{const o=document.getElementById('overall'),o2=document.getElementById('overall2'),n2=document.getElementById('overallN2');new MutationObserver(()=>{{o2.style.width=o.style.width;n2.textContent=document.getElementById('overallN').textContent}}).observe(o,{{attributes:true}});o2.style.width=o.style.width;n2.textContent=document.getElementById('overallN').textContent}})();
</script></body></html>"""


# ================================================================ PDF book
BOOK_CSS = """
@page{size:Letter;margin:.8in .85in .95in}
@page cover{margin:0}
*{box-sizing:border-box}
body{margin:0;font:400 10.5pt/1.6 Inter,sans-serif;color:#1d1a1f;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.cover{page:cover;width:8.5in;height:11in;position:relative;overflow:hidden;color:#fff;background:#120d12;break-after:page}
.cover .glow{position:absolute;inset:0;background:radial-gradient(70% 55% at 85% 10%,hsl(var(--h) 70% 38% / .95),transparent 70%),radial-gradient(60% 50% at 0% 100%,hsl(var(--h) 60% 25% / .9),transparent 70%)}
.cover .in{position:absolute;inset:.85in;display:flex;flex-direction:column;z-index:1}
.cover .cbody{position:absolute;left:-.45in;top:0;height:11in;aspect-ratio:922/2082;background:var(--bodyimg) left top/100% 100% no-repeat;z-index:0}
.cover .cmark{width:.9in;height:.9in;border-radius:50%;background:var(--markimg) center/cover;box-shadow:0 0 0 3px rgba(255,255,255,.7);margin-bottom:.25in}
.cover .in{left:4.65in;right:.6in}.cover .in h1{font-size:30pt!important}.cover .in .big{font-size:110pt!important}.cover .in .sub{font-size:11pt!important}.cover .in .by{flex-direction:column;align-items:flex-start;gap:6px}
.cover .wm{font:800 9pt "Inter Tight";letter-spacing:.3em;text-transform:uppercase;opacity:.9}
.cover .big{font:800 150pt/0.8 "Inter Tight";letter-spacing:-.04em;margin-top:auto;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.55)}
.cover .unit{font:600 11pt Inter;letter-spacing:.3em;text-transform:uppercase;opacity:.8;margin:10px 0 28px}
.cover .kick{font:600 10pt Inter;letter-spacing:.2em;text-transform:uppercase;color:hsl(var(--h) 80% 78%)}
.cover h1{font:800 40pt/1.02 "Inter Tight";letter-spacing:-.03em;margin:12px 0 14px;max-width:6in}
.cover .sub{font:400 13pt/1.45 Inter;opacity:.85;max-width:5in;margin:0 0 30px}
.cover .by{display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid rgba(255,255,255,.3);padding-top:16px}
.cover .by b{font:italic 400 22pt "Instrument Serif"}.cover .by span{font:600 8.5pt Inter;letter-spacing:.2em;text-transform:uppercase;opacity:.7}
.front{break-after:page}
.front h2,.toc h2,.part h2{font:800 26pt/1.1 "Inter Tight";letter-spacing:-.02em;margin:0 0 16px}
.front p{max-width:5.6in}
.tapbtn{display:block;text-align:center;background:#6b2fd6;color:#fff;text-decoration:none;font:700 15pt "Inter Tight";padding:18px;border-radius:12px;margin:22px 0 6px}
.ctap{display:inline-block;align-self:flex-start;background:#fff;color:#120d12;text-decoration:none;font:700 11pt Inter;padding:11px 18px;border-radius:999px;margin:0 0 26px}
.box{border:1px solid #e5ded6;border-radius:10px;padding:14px 16px;margin:16px 0;background:#f8f5fc}
.box b{color:#6b2fd6}
.toc{break-after:page}
.toc ol{list-style:none;padding:0;margin:0}
.toc .ph{font:700 8.5pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#6b2fd6;margin:18px 0 6px}
.toc a{display:flex;gap:10px;align-items:baseline;color:#1d1a1f;text-decoration:none;padding:5px 0;border-bottom:1px solid #eee7df;font-size:10.5pt}
.toc a .n{width:26px;color:#9a9199;font-weight:600}.toc a .t{flex:1}.toc a .p{font-weight:600;color:#6f6772}
.part{break-before:page;padding-top:2.2in}
.part .pk{font:700 9pt Inter;letter-spacing:.2em;text-transform:uppercase;color:#6b2fd6}
.part h2{font-size:38pt}.part p{max-width:5in;color:#4a434d;font-size:12pt}
.chap{break-before:page}
.chap .ck{font:700 8.5pt Inter;letter-spacing:.18em;text-transform:uppercase;color:#6b2fd6;margin-bottom:6px}
.chap h2{font:800 24pt/1.12 "Inter Tight";letter-spacing:-.02em;margin:0 0 18px;padding-bottom:14px;border-bottom:2px solid #1d1a1f}
.chap h3{font:700 13pt/1.3 "Inter Tight";margin:20px 0 6px;break-after:avoid}
.chap p{margin:0 0 9px}.chap ul,.chap ol{padding-left:18px;margin:0 0 10px}.chap li{margin:3px 0}.chap li::marker{color:#6b2fd6}
.callout{border-left:3px solid #6b2fd6;background:#f1e9ff;padding:10px 14px;margin:14px 0;break-inside:avoid}.callout p{margin:0}
.table-wrap{margin:10px 0 14px;break-inside:avoid}
.tbl{width:100%;border-collapse:collapse;font-size:9pt;line-height:1.4}
.tbl th{text-align:left;font:700 7.5pt Inter;letter-spacing:.06em;text-transform:uppercase;color:#6f6772;background:#f3eee8;padding:6px 8px}
.tbl td{padding:6px 8px;border-top:1px solid #e9e2da;vertical-align:top}
.quiz{border:1px solid #e5ded6;border-radius:8px;padding:10px 14px;margin:14px 0;break-inside:avoid;background:#fbf9f7}
.q-k{font:700 7.5pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#6b2fd6}.q-q{font-weight:600;margin:4px 0}.q-o{margin:4px 0 6px;padding-left:20px}
.q-a{font-size:9pt;color:#4a434d;margin:0;border-top:1px dashed #ddd;padding-top:6px}
.wk{break-before:page}
.wk-h{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #1d1a1f;padding-bottom:8px;margin-bottom:6px}
.wk-h h2{font:800 22pt "Inter Tight";margin:0}.wk-h span{font:700 8.5pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#6b2fd6}
.wk .note{color:#4a434d;margin:6px 0 10px}
.pday{break-inside:avoid;margin:12px 0 4px}.pday h3{font:700 12pt "Inter Tight";margin:0 0 2px}.pday .f{color:#6f6772;font-size:9pt;margin:0 0 6px}
.lex{break-inside:avoid;border-top:1px solid #e5ded6;padding:12px 0}
.lex h3{font:700 13pt "Inter Tight";margin:0 0 2px}.lex .lm{font-size:8.5pt;color:#6f6772;margin:0 0 6px}
.lex .cols{display:grid;grid-template-columns:1fr 1fr;gap:4px 18px}.lex h4{font:700 7.5pt Inter;letter-spacing:.12em;text-transform:uppercase;color:#6b2fd6;margin:6px 0 2px}
.lex ol,.lex ul{margin:0;padding-left:16px;font-size:9pt}.lex li{margin:1px 0}.lex p{font-size:9pt;margin:0}
.rec{break-inside:avoid;border-top:1px solid #e5ded6;padding:12px 0}.rec h3{font:700 13pt "Inter Tight";margin:0}
.rec .mm{display:flex;gap:14px;font:600 8.5pt Inter;color:#6f6772;margin:3px 0 6px}.rec .cols{display:grid;grid-template-columns:1fr 1.3fr;gap:16px}
.rec ul,.rec ol{margin:0;padding-left:16px;font-size:9pt}
.cday{break-inside:avoid;border-top:1px solid #e5ded6;padding:8px 0;display:grid;grid-template-columns:1.1in 1fr;gap:12px}
.cday b{font:700 11pt "Inter Tight"}.cday small{display:block;color:#6f6772}.cday ul{margin:0;padding:0;list-style:none;columns:2;font-size:9pt}.cday li{display:flex;justify-content:space-between;gap:6px;padding:1px 10px 1px 0}
.cday .pr{grid-column:2;font:italic 400 11pt "Instrument Serif";color:#4a434d}
"""

WB_CSS = """
@page{size:Letter;margin:0}
*{box-sizing:border-box}
body{margin:0;font:400 9.5pt/1.4 Inter,sans-serif;color:#1d1a1f;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:816px;height:1056px;padding:62px 66px 70px;position:relative;overflow:hidden;break-after:page}
.page:last-child{break-after:auto}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #1d1a1f;padding-bottom:8px;margin-bottom:12px}
.hd h2{font:800 20pt/1.1 "Inter Tight";margin:0;letter-spacing:-.01em}.hd span{font:700 7.5pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#6b2fd6}
.sub{color:#6f6772;margin:0 0 10px;font-size:9pt}
.f{display:inline-block;border-bottom:1px solid #b9b0a8;height:20px;vertical-align:bottom}
.fb{display:block;border:1px solid #cfc6bd;border-radius:6px;background:#fbf9f7}
.cb{display:inline-block;width:14px;height:14px;border:1.2px solid #8a8189;border-radius:3px;vertical-align:middle;background:#fff}
table{width:100%;border-collapse:collapse}
th{font:700 7pt Inter;letter-spacing:.06em;text-transform:uppercase;color:#6f6772;text-align:left;padding:4px 4px;border-bottom:1px solid #1d1a1f}
td{padding:3px 4px;border-bottom:1px solid #e9e2da;vertical-align:middle;font-size:8.5pt}
td .f{width:100%}
.exn{font-weight:600;font-size:8.5pt;line-height:1.2}.exm{display:block;font-size:7pt;color:#8a8189;font-weight:500}
.lbl{font:700 7pt Inter;letter-spacing:.1em;text-transform:uppercase;color:#6f6772;margin:12px 0 4px}
.row{display:flex;gap:14px;align-items:flex-end;margin:4px 0}.row label{flex:1;font-size:8pt;color:#6f6772}.row label .f{width:100%}
.ck{display:flex;align-items:center;gap:8px;padding:4px 0;border-bottom:1px solid #f0ebe5;font-size:9pt}
.cols2{columns:2;column-gap:28px}.cols2 .ck{break-inside:avoid}
.prompt{font:italic 400 13pt/1.3 "Instrument Serif";margin:14px 0 6px}
.ft{position:absolute;left:66px;right:66px;bottom:34px;display:flex;justify-content:space-between;font:600 7pt Inter;letter-spacing:.14em;text-transform:uppercase;color:#a39aa3}
"""


def tbl(head, rows):
    return ('<div class="table-wrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")


def book_html(p, pages=None):
    """pages: {anchor: page_number} from a previous pass, used to fill the table of contents."""
    pages = pages or {}
    guide = load_guide(p["guide"], print_mode=True)
    big = {"glute-starter": ("03", "Workouts"), "30-day-challenge": ("30", "Days"), "glute-specialist": ("08", "Weeks"), "press-like-a-boss": ("06", "Weeks"),
           "fuel-like-a-baddie": ("17", "Chapters"), "gym-girl-confidence-kit": ("02", "Weeks")}[p["guide"]]
    toc, body = [], []

    meta = {}

    def anchor(aid, title, num="", phase=None):
        meta[aid] = (title, num, title.startswith("Part "))
        return ""

    # Part I: guide
    body.append(f'<section class="part" id="part1">{anchor("part1", "Part I · " + ("The Handbook" if "Specialist" in p["title"] or "Boss" in p["title"] else "The Guide"), "", "Contents")}<div class="pk">Part I</div><h2>{"The Handbook" if "Specialist" in p["title"] or "Boss" in p["title"] else "The Guide"}</h2><p>{len(guide)} chapters. Read Chapters 1–{min(4, len(guide))} before you start, and use the rest as a reference.</p></section>')
    for i, c in enumerate(guide):
        aid = f"ch{i + 1}"
        body.append(f'<section class="chap" id="{aid}">{anchor(aid, c["t"], f"{i + 1:02d}")}<div class="ck">Chapter {i + 1}</div><h2>{e(c["t"])}</h2>{c["html"]}</section>')
    # Part II: product-specific material
    parts = []
    for s in p["sections"]:
        if s["type"] == "program":
            html_ = []
            for wi, w in enumerate(s["weeks"]):
                aid = f"wk{wi + 1}"
                days = "".join(f'<div class="pday"><h3>{e(d["name"])}</h3><p class="f">{e(d["focus"])}</p>' + tbl(["Exercise", "Sets × reps", "RIR", "Rest"], [[e(x["n"]), e(f'{x["s"]} × {x["r"]}'), e(x["rir"]), e(x["rest"])] for x in d["ex"]]) + "</div>" for d in w["days"])
                html_.append(f'<section class="wk" id="{aid}">{anchor(aid, f"{w["name"]} · {w["phase"]}", "")}<div class="wk-h"><h2>{e(w["name"])}</h2><span>{e(w["phase"])} phase</span></div><p class="note">{e(w["note"])}</p>{days}</section>')
            parts.append(("The Program", "Every workout, week by week. Log your sets in the app or in the fillable workbook at the back of this book.", html_))
        elif s["type"] == "challenge":
            html_ = [f'<section class="wk" id="days">{anchor("days", "The 30 Days", "")}<div class="wk-h"><h2>The 30 Days</h2><span>Daily plan</span></div>']
            for i, d in enumerate(s["days"]):
                html_.append(f'<div class="cday"><div><b>Day {i + 1}</b><small>{e(d["t"])}{f" · {d["rounds"]} rounds" if d["rounds"] else ""}</small></div><ul>{"".join(f"<li><span>{e(x["n"])}</span><b>{e(x["r"])}</b></li>" for x in d["ex"])}</ul><p class="pr">{e(d["prompt"])}</p></div>')
            html_.append("</section>")
            parts.append(("The Challenge", "Your daily workouts and prompts. Track your days in the app or in the fillable 30-day tracker at the back.", html_))
        elif s["type"] == "meals":
            html_ = [f'<section class="wk" id="meals">{anchor("meals", "7-Day Meal Plan", "")}<div class="wk-h"><h2>7-Day Meal Plan</h2><span>High protein</span></div>'
                     + "".join(f'<div class="pday"><h3>{e(d["name"])}</h3>' + tbl(["Meal", "What to eat", "Protein"], [[e(m[0]), e(m[1]), f"~{m[2]} g"] for m in d["meals"]]) + "</div>" for d in s["days"]) + "</section>"]
            parts.append(("Plans & Recipes", "Your meal plan, recipes, grocery list and eating-out guide.", html_))
        elif s["type"] == "recipes":
            parts[-1][2].append(f'<section class="wk" id="recipes">{anchor("recipes", "Recipes", "")}<div class="wk-h"><h2>Recipes</h2><span>{len(s["items"])} recipes</span></div>'
                                + "".join(f'<div class="rec"><h3>{e(r["n"])}</h3><div class="mm"><span>{e(r["t"])}</span><span>{e(r["time"])}</span><span>{r["m"][0]} kcal</span><span>P {r["m"][1]} g</span><span>C {r["m"][2]} g</span><span>F {r["m"][3]} g</span></div>'
                                          f'<div class="cols"><ul>{"".join(f"<li>{e(i)}</li>" for i in r["ing"])}</ul><ol>{"".join(f"<li>{e(t)}</li>" for t in r["steps"])}</ol></div></div>' for r in s["items"])
                                + '<p style="font-size:8.5pt;color:#6f6772">Macros are approximate per serving and vary by brand.</p></section>')
        elif s["type"] == "accordion" and parts:
            parts[-1][2].append(f'<section class="wk" id="{s["id"]}">{anchor(s["id"], s["label"], "")}<div class="wk-h"><h2>{e(s["label"])}</h2><span>Guide</span></div>'
                                + tbl(["Where", "What to order"], [[f"<b>{e(it['q'])}</b>", e(it["a"])] for it in s["items"]]) + "</section>")
    for k, (title, intro, secs) in enumerate(parts):
        pid = f"part2_{k}"
        body.append(f'<section class="part" id="{pid}">{anchor(pid, "Part II · " + title)}<div class="pk">Part II</div><h2>{e(title)}</h2><p>{e(intro)}</p></section>')
        body.extend(secs)
    lib = lib_for(p)
    if lib:
        body.append(f'<section class="part" id="part3">{anchor("part3", "Part III · Exercise Library", "")}<div class="pk">Part III</div><h2>Exercise Library</h2><p>Setup, execution, cues, common mistakes and swaps for all {len(lib)} exercises in this program.</p></section>')
        body.append('<section class="chap" id="lib" style="break-before:page">')
        for n, x in lib.items():
            li = lambda a: "".join(f"<li>{e(t)}</li>" for t in a)
            body.append(f'<div class="lex"><h3>{e(n)}</h3><p class="lm">{e(x["cat"])} · {e(x["m"])} · Equipment: {e(x["eq"])}</p><div class="cols">'
                        f'<div><h4>Setup</h4><ol>{li(x["setup"])}</ol></div><div><h4>Execution</h4><ol>{li(x["do"])}</ol></div>'
                        f'<div><h4>Cues</h4><ul>{li(x["cues"])}</ul></div><div><h4>Common mistakes</h4><ul>{li(x["mist"])}</ul></div>'
                        f'<div><h4>Easier / Harder</h4><p>{e(x["easier"])} / {e(x["harder"])}</p></div><div><h4>Swaps</h4><p>{e(x["swap"])}</p></div></div></div>')
        body.append("</section>")
    entries = [(aid, *meta[aid]) for aid in re.findall(r'<section class="\w+" id="(\w+)"', "".join(body)) if aid in meta]
    for aid, title, num, is_part in entries:
        if is_part: toc.append(f'<li class="ph">{e(title.split(" · ")[0])}</li>')
        toc.append(f'<li><a href="#{aid}"><span class="n">{num}</span><span class="t">{e(title.split(" · ", 1)[1] if is_part else title)}</span><span class="p">{pages.get(aid, "")}</span></a></li>')
    toc.append(f'<li class="ph">Part {"IV" if lib else "III"}</li><li><a href="#workbook"><span class="n"></span><span class="t">Fillable Workbook</span><span class="p">{pages.get("workbook", "")}</span></a></li>')

    front = f"""<section class="front"><h2>How to use this book</h2>
<p>This book is the companion to your interactive app. The app is the fastest way to train: it logs every set, remembers your weights, runs your rest timer and charts your progress. This PDF gives you the same material in a format you can read, print and fill in.</p>
<a class="tapbtn" href="{C.SITE}/p/{p['token']}/app.html">Tap here to open your interactive program →</a>
<div class="box">The interactive program tracks every set, runs your rest timer, charts your progress and includes every chapter with quizzes. On your phone, tap <i>Share → Add to Home Screen</i> so it opens like an app.</div>
<p><b>This PDF is interactive.</b> Tap any entry in the table of contents to jump to it, use your PDF reader's bookmarks panel to navigate, and fill in the workbook pages at the back directly in Adobe Acrobat, Apple Books/Preview, or most PDF apps. Your entries save with the file.</p>
<p style="margin-top:28px;font-size:9pt;color:#6f6772">{e(C.DISCLAIMER)}</p>
<p style="font-size:9pt;color:#6f6772">© 2026 {e(C.COACH)} · {e(C.BRAND)}. All rights reserved. This book is licensed for the personal use of the purchaser only. Copying, sharing or reselling is prohibited.</p></section>"""
    return entries, f"""<!doctype html><html><head><meta charset="utf-8"><title>{e(p['title'])}</title>{FONTS}<style>{BOOK_CSS}</style></head><body style="--h:{p['hue']}">
<section class="cover" style="--bodyimg:url({BODY});--markimg:url({MARK})"><div class="glow"></div><div class="cbody"></div><div class="in"><div class="cmark"></div><div class="wm">Get Fit With Me</div>
<div class="big">{big[0]}</div><div class="unit">{big[1]}</div><div class="kick">{e(p['kicker'])}</div><h1>{e(p['title'])}</h1><p class="sub">{e(p['sub'])}</p>
<a class="ctap" href="{C.SITE}/p/{p['token']}/app.html">Tap to open the interactive program →</a>
<div class="by"><b>{e(C.COACH)}</b><span>{' · '.join(e(m) for m in p['meta'][:3])}</span></div></div></section>
{front}
<section class="toc"><h2>Contents</h2><ol>{''.join(toc)}</ol></section>
{''.join(body)}
</body></html>"""


# ---------------------------------------------------------------- workbook (fixed pages + form fields)
class WB:
    def __init__(s, title): s.pages, s.n, s.title = [], 0, title

    def fid(s, kind, extra=""):
        s.n += 1
        return f'data-f="{kind}" data-name="wb{s.n}" {extra}'

    def text(s, w="100%"): return f'<span class="f" {s.fid("text")} style="width:{w}"></span>'
    def box(s, h, multi=True): return f'<span class="fb" {s.fid("multi" if multi else "text")} style="height:{h}px"></span>'
    def cb(s): return f'<span class="cb" {s.fid("check")}></span>'

    def page(s, title, kicker, inner):
        s.pages.append(f'<div class="page"><div class="hd"><h2>{e(title)}</h2><span>{e(kicker)}</span></div>{inner}<div class="ft"><span>Get Fit With Me · {e(s.title)}</span><span>Workbook</span></div></div>')

    def html(s):
        return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{WB_CSS}</style></head><body>{"".join(s.pages)}</body></html>'


def workbook(p):
    wb = WB(p["short"])
    for s in p["sections"]:
        if s["type"] == "program":
            for w in s["weeks"]:
                for d in w["days"]:
                    mx = max(x["s"] for x in d["ex"])
                    head = "<tr><th style='width:30%'>Exercise</th>" + "".join(f"<th>Set {i + 1}<br><small>lb × reps</small></th>" for i in range(mx)) + "<th style='width:28px'>✓</th></tr>"
                    rows = "".join(f"<tr><td><span class='exn'>{e(x['n'])}</span><span class='exm'>{e(str(x['s']))} × {e(x['r'])} · RIR {e(x['rir'])} · {e(x['rest'])}</span></td>"
                                   + "".join(f"<td>{wb.text() if i < x['s'] else ''}</td>" for i in range(mx)) + f"<td>{wb.cb()}</td></tr>" for x in d["ex"])
                    inner = (f'<div class="row"><label>Date {wb.text()}</label><label>Bodyweight {wb.text()}</label><label>Energy (1–10) {wb.text()}</label><label>Sleep (hrs) {wb.text()}</label></div>'
                             f'<p class="sub">{e(w["phase"])} phase · {e(d["focus"])}</p><table>{head}{rows}</table>'
                             f'<div class="lbl">Warm-up notes</div>{wb.box(60)}<div class="lbl">How did it feel? What will you change next time?</div>{wb.box(130)}'
                             f'<div class="row" style="margin-top:12px"><label>Workout complete {wb.cb()}</label><label>Total sets {wb.text()}</label><label>New PR? {wb.text()}</label></div>')
                    wb.page(d["name"], w["name"] + " · Log", inner)
        if s["type"] == "challenge":
            rows = "".join(f"<tr><td><b>Day {i + 1}</b> <span class='exm' style='display:inline'>{e(d['t'])}</span></td>" + "".join(f"<td style='text-align:center'>{wb.cb()}</td>" for _ in range(5)) + "</tr>" for i, d in enumerate(s["days"][:15]))
            rows2 = "".join(f"<tr><td><b>Day {i + 16}</b> <span class='exm' style='display:inline'>{e(d['t'])}</span></td>" + "".join(f"<td style='text-align:center'>{wb.cb()}</td>" for _ in range(5)) + "</tr>" for i, d in enumerate(s["days"][15:]))
            th = "<tr><th>Day</th><th>Workout</th><th>Water</th><th>Steps</th><th>Protein</th><th>Journal</th></tr>"
            wb.page("30-Day Tracker · Days 1–15", "Check off each habit", f'<table>{th}{rows}</table><div class="lbl">Notes</div>{wb.box(150)}')
            wb.page("30-Day Tracker · Days 16–30", "Check off each habit", f'<table>{th}{rows2}</table><div class="lbl">Notes</div>{wb.box(150)}')
            for k in range(0, 30, 3):
                inner = "".join(f'<div class="prompt">Day {k + j + 1}: {e(s["days"][k + j]["prompt"])}</div>{wb.box(215)}' for j in range(3))
                wb.page(f"Journal · Days {k + 1}–{k + 3}", "Mindset prompts", inner)
        if s["type"] == "journal":
            for k in range(0, len(s["prompts"]), 2):
                inner = "".join(f'<div class="prompt">{e(q)}</div>{wb.box(370)}' for q in s["prompts"][k:k + 2])
                wb.page("Confidence Journal", f"Prompts {k + 1}–{min(k + 2, len(s['prompts']))}", inner)
        if s["type"] == "checklist":
            for g in s["groups"]:
                items = "".join(f'<div class="ck">{wb.cb()}<span>{e(it)}</span></div>' for it in g["items"])
                wb.page(g["title"], s["label"], f'<div class="cols2">{items}</div><div class="lbl">Notes</div>{wb.box(160)}')
        if s["type"] == "macro":
            inner = (f'<p class="sub">Use the My Macros calculator in the app, then record your numbers here. Recalculate every 4 weeks or after 5 lb of change.</p>'
                     + "".join(f'<div class="row"><label>{a} {wb.text()}</label><label>{b} {wb.text()}</label><label>{c} {wb.text()}</label></div>' for a, b, c in
                               [("Date", "Weight (lb)", "Height"), ("Age", "Activity level", "Goal"), ("Maintenance kcal", "Target kcal", "Water (oz)"), ("Protein (g)", "Carbs (g)", "Fat (g)"), ("Protein per meal", "Carbs per meal", "Fat per meal")])
                     + f'<div class="lbl">My why: what will hitting these numbers change for me?</div>{wb.box(160)}<div class="lbl">My non-negotiables this month</div>{wb.box(160)}')
            wb.page("My Macro Targets", "Worksheet", inner)
            meal_rows = "".join(f"<tr><td><b>{d}</b></td>" + "".join(f"<td>{wb.box(58)}</td>" for _ in range(4)) + "</tr>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
            for n in (1, 2):
                wb.page(f"Weekly Meal Planner {n}", "Plan your week", f'<div class="row"><label>Week of {wb.text()}</label><label>Prep day {wb.text()}</label></div><table><tr><th style="width:44px"></th><th>Breakfast</th><th>Lunch</th><th>Snack</th><th>Dinner</th></tr>{meal_rows}</table>')
        if s["type"] == "progress" and s.get("measure"):
            th = "<tr><th>Date</th><th>Weight</th><th>Waist</th><th>Hips</th><th>Glutes</th><th>Thigh</th><th>Arm</th><th>Notes</th></tr>"
            rows = "".join("<tr>" + "".join(f"<td>{wb.text()}</td>" for _ in range(8)) + "</tr>" for _ in range(14))
            wb.page("Measurements & Check-Ins", "Every 2 weeks", f'<p class="sub">Measure in the morning, before eating, at the same spots each time. Photos: front, side and back, same lighting.</p><table>{th}{rows}</table><div class="lbl">Reflections</div>{wb.box(150)}')
    if p["guide"] in ("glute-specialist", "press-like-a-boss"):
        th = "<tr><th>Lift</th><th>Date</th><th>Weight</th><th>Reps</th><th>Est. 1RM</th><th>Notes</th></tr>"
        rows = "".join("<tr>" + "".join(f"<td>{wb.text()}</td>" for _ in range(6)) + "</tr>" for _ in range(22))
        wb.page("PR Log", "Personal records", f'<p class="sub">Estimated 1RM = weight × (1 + reps ÷ 30).</p><table>{th}{rows}</table>')
    return wb


# ---------------------------------------------------------------- PDF pipeline
def make_pdfs(slugs_only=None):
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import Color, HexColor
    tmp = tempfile.mkdtemp()
    jobs = []
    for p in C.PRODUCTS:
        if slugs_only and p["slug"] not in slugs_only: continue
        open(os.path.join(tmp, p["slug"] + "-book1.html"), "w").write(book_html(p)[1])
        wb = workbook(p)
        open(os.path.join(tmp, p["slug"] + "-wb.html"), "w").write(wb.html())
        jobs.append(p)
    # pass 1: book (for page numbers) + workbook (with field geometry)
    subprocess.run(["node", os.path.join(HERE, "pdf.js"), tmp] + [p["slug"] for p in jobs], check=True)
    for p in jobs:
        slug = p["slug"]
        r1 = PdfReader(os.path.join(tmp, slug + "-book1.pdf"))
        pages = {k.lstrip("/"): r1.get_destination_page_number(v) + 1 for k, v in r1.named_destinations.items()}
        pages["workbook"] = len(r1.pages) + 1
        p["_entries"], h2 = book_html(p, pages)
        open(os.path.join(tmp, slug + "-book2.html"), "w").write(h2)
    subprocess.run(["node", os.path.join(HERE, "pdf.js"), tmp, "--pass2"] + [p["slug"] for p in jobs], check=True)
    for p in jobs:
        slug = p["slug"]
        book = PdfReader(os.path.join(tmp, slug + "-book2.pdf"))
        nbook = len(book.pages)
        # footer stamps (skip cover)
        sbuf = io.BytesIO(); c = canvas.Canvas(sbuf, pagesize=(612, 792))
        for i in range(nbook):
            if i > 0:
                c.setFont("Helvetica-Bold", 6.5); c.setFillColor(HexColor("#a39aa3"))
                c.drawString(61, 34, f"GET FIT WITH ME  ·  {p['title'].upper()}"); c.drawRightString(551, 34, str(i + 1))
            c.showPage()
        c.save(); stamps = PdfReader(sbuf)
        w = PdfWriter(clone_from=book)
        for i, pg in enumerate(w.pages): pg.merge_page(stamps.pages[i])
        # workbook: build a form-field layer, put the rendered page underneath
        wbpdf = PdfReader(os.path.join(tmp, slug + "-wb.pdf"))
        fields = json.load(open(os.path.join(tmp, slug + "-wb.json")))
        fbuf = io.BytesIO(); c = canvas.Canvas(fbuf, pagesize=(612, 792)); form = c.acroForm
        by_page = {}
        for f in fields: by_page.setdefault(f["p"], []).append(f)
        clear = Color(0, 0, 0, alpha=0)
        for i in range(len(wbpdf.pages)):
            for f in by_page.get(i, []):
                x, y, fw, fh = f["x"] * .75, 792 - (f["y"] + f["h"]) * .75, f["w"] * .75, f["h"] * .75
                n = f"{slug[:6]}_{f['name']}"
                if f["k"] == "check":
                    form.checkbox(name=n, x=x, y=y, size=min(fw, fh), buttonStyle="check", borderWidth=0, borderColor=clear, fillColor=clear, textColor=HexColor("#6b2fd6"), forceBorder=False)
                else:
                    form.textfield(name=n, x=x + 1, y=y + 1, width=fw - 2, height=fh - 2, borderWidth=0, borderColor=clear, fillColor=clear, textColor=HexColor("#1d1a1f"),
                                   fontName="Helvetica", fontSize=0 if f["k"] == "multi" else 8, fieldFlags="multiline" if f["k"] == "multi" else "", forceBorder=False)
            c.showPage()
        c.save()
        layer = PdfReader(fbuf)
        lw = PdfWriter(clone_from=layer)
        for i, pg in enumerate(lw.pages): pg.merge_page(wbpdf.pages[i], over=False)
        lw.set_need_appearances_writer(True)
        wbuf = io.BytesIO(); lw.write(wbuf)
        start = len(w.pages)
        w.append(PdfReader(wbuf), import_outline=False)
        dest = {k.lstrip("/"): book.get_destination_page_number(v) for k, v in book.named_destinations.items()}
        w.add_outline_item("Cover", 0); w.add_outline_item("How to use this book", 1); w.add_outline_item("Contents", 2)
        parent = None
        for aid, title, num, is_part in p["_entries"]:
            if aid not in dest: continue
            if is_part: parent = w.add_outline_item(title, dest[aid])
            else: w.add_outline_item((f"{num}  " if num else "") + title, dest[aid], parent=parent)
        w.add_outline_item("Fillable Workbook", start)
        w.add_metadata({"/Title": f"{p['title']} · {C.BRAND}", "/Author": C.COACH, "/Subject": p["sub"]})
        w.page_mode = "/UseOutlines"
        os.makedirs(folder(p), exist_ok=True)
        out = os.path.join(folder(p), pdf_name(p))
        with open(out, "wb") as fh: w.write(fh)
        print(f"  {slug}.pdf: {len(w.pages)} pages ({nbook} book + {len(wbpdf.pages)} workbook), {len(fields)} fillable fields")


# ================================================================ store page, covers, Stan copy
def store_items():
    items = []
    for p in C.PRODUCTS:
        items.append({**p["stan"], "slug": p["slug"], "token": p["token"], "hue": p["hue"], "title": p["title"], "kicker": p["kicker"], "meta": p["meta"], "link": access_url(p)})
    items.insert(1, {**C.BUNDLE, "slug": "complete-collection", "hue": 272, "title": "The Complete Collection", "kicker": "Bundle · Save 37%", "meta": ["5 programs", "5 PDF books"], "link": ""})
    for i, c in enumerate(C.COACHING):
        items.append({**c, "slug": ["form-check-call", "online-coaching"][i], "hue": [258, 292][i], "title": c["thumb_title"],
                      "kicker": ["30-minute call", "Monthly coaching"][i], "meta": [["1:1", "Video call"], ["1:1", "Custom plan"]][i], "link": ""})
    return items


BIG = {"glute-starter-pack-free-g7f2": ("03", "Workouts"), "complete-collection": ("05", "Programs"), "30-day-get-fit-challenge-c9x4": ("30", "Days"),
       "booty-builder-8-week-b3k8": ("08", "Weeks"), "press-like-a-boss-p5m1": ("06", "Weeks"), "fuel-like-a-baddie-f2q6": ("17", "Chapters"),
       "gym-girl-confidence-kit-k4t9": ("02", "Weeks"), "form-check-call": ("30", "Minutes"), "online-coaching": ("1:1", "Coaching")}

COVER_CSS_BASE = """
.cover{--h:340;position:relative;aspect-ratio:1;overflow:hidden;background:#120d12;color:#fff;container-type:inline-size;border-radius:inherit}
.cv-body{position:absolute;left:0;top:0;height:100%;aspect-ratio:922/2082;background:var(--bodyimg) left top/100% 100% no-repeat;z-index:0}
.cover:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent 30%,rgba(18,13,18,.35) 60%,transparent);pointer-events:none}
.cover:before{content:"";position:absolute;inset:0;background:radial-gradient(75% 60% at 90% 0%,hsl(var(--h) 70% 40% / .95),transparent 70%),radial-gradient(70% 60% at 0% 100%,hsl(var(--h) 60% 24% / .9),transparent 70%)}
.cv{position:absolute;inset:7cqw 6cqw 7cqw 49cqw;display:flex;flex-direction:column;z-index:1}
.cv-top{display:flex;align-items:center;gap:2.4cqw}.cv-mark{flex:none;width:9cqw;height:9cqw;border-radius:50%;background:var(--markimg) center/cover;box-shadow:0 0 0 .45cqw rgba(255,255,255,.75)}
.cv-wm{font:800 2.4cqw/1.2 "Inter Tight",sans-serif;letter-spacing:.24em;text-transform:uppercase}
.cv-big{font:800 24cqw/.8 "Inter Tight",sans-serif;letter-spacing:-.04em;margin-top:auto;color:transparent;-webkit-text-stroke:.35cqw rgba(255,255,255,.6)}
.cv-unit{font:600 2.6cqw Inter,sans-serif;letter-spacing:.3em;text-transform:uppercase;opacity:.8;margin:2.2cqw 0 4cqw}
.cv-kick{font:600 2.6cqw Inter,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:hsl(var(--h) 85% 80%)}
.cv-title{font:800 6.4cqw/1.04 "Inter Tight",sans-serif;letter-spacing:-.03em;margin:1.6cqw 0 4cqw}
.cv-by{display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid rgba(255,255,255,.3);padding-top:2.6cqw}
.cv-by{flex-direction:column;align-items:flex-start;gap:1cqw}.cv-by b{font:italic 400 5cqw "Instrument Serif",serif}.cv-by span{font:600 2.2cqw Inter,sans-serif;letter-spacing:.2em;text-transform:uppercase;opacity:.75}
"""


COVER_CSS = COVER_CSS_BASE + f":root{{--bodyimg:url({BODY});--markimg:url({MARK})}}\n"


def cover(it):
    b = BIG[it["slug"]]
    return (f'<div class="cover" style="--h:{it["hue"]}"><div class="cv-body"></div><div class="cv"><div class="cv-top"><div class="cv-mark"></div><div class="cv-wm">Get Fit With Me</div></div><div class="cv-big">{b[0]}</div><div class="cv-unit">{b[1]}</div>'
            f'<div class="cv-kick">{e(it["kicker"])}</div><div class="cv-title">{e(it["title"])}</div><div class="cv-by"><b>{e(C.COACH)}</b><span>{" · ".join(e(m) for m in it["meta"][:2])}</span></div></div></div>')


def store_page(items):
    cards = []
    for it in items:
        bump = f'<label class="bump"><input type="checkbox"><span><b>{e(it["bump"]["title"])}</b><small>{e(it["bump"]["desc"])}</small></span></label>' if it.get("bump") else ""
        preview = ""
        price = f'<span class="price">{e(it["price"])}</span>' + (f' <s>{e(it["strike"])}</s>' if it["strike"] else "")
        cards.append(f"""<article class="prod" id="{it['slug']}">
 <button class="pcard" data-open="{it['slug']}">{cover(it)}<span class="pinfo"><b>{e(it['thumb_title'])}</b><small>{e(it['thumb_sub'])}</small><span>{price}</span></span></button>
 <button class="btn primary wide" data-open="{it['slug']}">{e(it['button'])}</button>
 <dialog id="d-{it['slug']}"><button class="x" data-close aria-label="Close">×</button>
  <div class="dl-cover">{cover(it)}</div><div class="dl-body">
  <h2>{e(it['checkout_title'])}</h2><div class="pr">{price}</div><p>{e(it['desc'])}</p>
  <ul>{''.join(f'<li>{e(b)}</li>' for b in it['bullets'])}</ul>{bump}
  <div class="fields"><input placeholder="Full name"><input type="email" placeholder="Email address"></div>
  <button class="btn primary wide" type="button">{e(it['cta'])}</button>{preview}
  <p class="note">Store preview: Stan's real checkout replaces this form.</p></div></dialog></article>""")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{C.BRAND} · {C.COACH}</title><meta name="description" content="{e(C.STORE['bio'])}"><meta name="robots" content="noindex,nofollow">
{ICON}
{FONTS}<style>{TOKENS}{COVER_CSS}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.55 var(--font);-webkit-font-smoothing:antialiased}}
.wrap{{max-width:520px;margin:0 auto;padding:40px 16px 60px}}
.hero{{position:relative;overflow:hidden;text-align:left;border-radius:24px;padding:26px 22px 24px;margin:0 0 22px;color:#fff;background:radial-gradient(90% 70% at 100% 0%,#9b5cff,transparent 70%),linear-gradient(160deg,#4a1aa6,#22104d)}}
.hero .bd{{position:absolute;left:0;top:0;height:100%;aspect-ratio:922/2082;background:var(--bodyimg) left top/100% 100% no-repeat}}
.hero{{min-height:360px;padding-left:min(46%,190px)!important}}.hero>*:not(.bd){{position:relative}}.hero h1{{font-size:32px}}.intro{{padding:0 4px;margin:-6px 0 22px}}.intro .bio{{margin:0 0 12px;color:var(--ink2);font-size:15px}}.intro .soc{{justify-content:flex-start;margin:0}}.hero .wm{{color:#d9c4ff}}.hero h1{{color:#fff}}.hero .tag{{color:#e3d6ff}}.hero .bio{{color:#eee6ff;margin:12px 0 16px}}
.hero .soc{{justify-content:flex-start;flex-wrap:wrap;margin:0}}.hero .soc a{{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.25);color:#fff}}
.logoimg{{width:96px;height:96px;border-radius:50%;box-shadow:0 0 0 3px #d9c4ff;margin-bottom:14px;display:block}}
.av{{width:104px;height:104px;border-radius:50%;margin:0 auto 16px;display:grid;place-items:center;background:var(--ink);color:var(--bg);font:800 34px var(--head);letter-spacing:-.02em;box-shadow:0 0 0 4px var(--bg),0 0 0 5px var(--line)}}
.wm{{font:800 12px var(--head);letter-spacing:.24em;text-transform:uppercase;color:var(--acc)}}
h1{{font:800 40px/1.05 var(--head);letter-spacing:-.03em;margin:8px 0 4px}}.tag{{font:italic 400 21px var(--serif);color:var(--mut);margin:0}}
.bio{{color:var(--ink2);font-size:15px;margin:14px auto 18px;max-width:420px}}
.soc{{display:flex;justify-content:center;gap:8px;margin:0 0 30px}}.soc a{{font:600 13px var(--font);color:var(--ink);text-decoration:none;border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:8px 14px}}
.prod{{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:12px;margin:0 0 14px;box-shadow:var(--shadow)}}
.prod:nth-of-type(2){{border:1.5px solid var(--acc)}}.prod:nth-of-type(2):before{{content:"Best value";display:inline-block;font:700 11px var(--font);letter-spacing:.12em;text-transform:uppercase;color:var(--acc-ink);background:var(--acc);border-radius:999px;padding:4px 10px;margin:2px 0 10px 2px}}
.pcard{{all:unset;box-sizing:border-box;cursor:pointer;display:grid;grid-template-columns:104px 1fr;gap:14px;align-items:center;width:100%}}
.pcard .cover{{border-radius:12px}}.pinfo b{{display:block;font:700 17px/1.25 var(--head)}}.pinfo small{{display:block;color:var(--mut);font-size:13.5px;line-height:1.4;margin:3px 0 6px}}
.price{{font:800 18px var(--head);color:var(--ink)}}s{{color:var(--mut);font-size:14px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;border:1px solid transparent;border-radius:12px;padding:13px 18px;font:600 15px var(--font);cursor:pointer;text-decoration:none}}
.btn.primary{{background:var(--acc);color:var(--acc-ink)}}.btn.ghost{{background:var(--surface);border-color:var(--line);color:var(--ink)}}.btn.wide{{width:100%;margin-top:10px}}
dialog{{width:min(560px,100vw);max-height:94vh;border:0;border-radius:20px;padding:0;background:var(--surface);color:var(--ink);overflow:auto}}
dialog::backdrop{{background:rgba(15,13,16,.6);backdrop-filter:blur(3px)}}
.dl-cover .cover{{border-radius:0}}.dl-body{{padding:22px 22px 26px}}
dialog h2{{font:800 28px/1.12 var(--head);letter-spacing:-.02em;margin:0 0 6px}}.pr{{margin:0 0 12px}}dialog p{{color:var(--ink2)}}
dialog ul{{list-style:none;padding:0;margin:14px 0}}dialog li{{padding:9px 0 9px 28px;border-top:1px solid var(--line);position:relative;font-size:15px}}
dialog li:before{{content:"";position:absolute;left:4px;top:15px;width:12px;height:7px;border-left:2px solid var(--ok);border-bottom:2px solid var(--ok);transform:rotate(-45deg)}}
.bump{{display:flex;gap:12px;border:1.5px dashed var(--acc);border-radius:12px;padding:12px 14px;background:var(--acc-soft);cursor:pointer;margin:14px 0}}
.bump input{{width:20px;height:20px;accent-color:var(--acc);flex:none;margin-top:2px}}.bump b{{display:block;font-size:14.5px}}.bump small{{color:var(--ink2);font-size:13.5px}}
.fields{{display:grid;gap:8px;margin:12px 0 0}}.fields input{{font:16px var(--font);padding:12px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink)}}
.x{{position:sticky;top:10px;float:right;margin:10px 10px -46px 0;z-index:2;width:36px;height:36px;border-radius:50%;border:0;background:rgba(0,0,0,.45);color:#fff;font-size:22px;cursor:pointer}}
.note{{font-size:12px;color:var(--mut);text-align:center;margin-top:12px}}footer{{text-align:center;color:var(--mut);font-size:12.5px;margin-top:28px}}
</style></head><body><div class="wrap"><section class="hero"><div class="bd" role="img" aria-label="Danielle Dawson"></div><img class="logoimg" src="{MARK}" alt="Get Fit With Me logo">
<div class="wm">{e(C.BRAND)}</div><h1>{e(C.COACH)}</h1><p class="tag">{e(C.STORE['tagline'])}</p></section>
<div class="intro"><p class="bio">{e(C.STORE['bio'])}</p><div class="soc"><a href="#">Instagram</a><a href="#">TikTok</a><a href="#">YouTube</a></div></div>
{''.join(cards)}<footer>© 2026 {e(C.COACH)} · {e(C.BRAND)}</footer></div>
<script>
document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>document.getElementById('d-'+b.dataset.open).showModal());
document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>b.closest('dialog').close());
document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',ev=>{{if(ev.target===d)d.close()}}));
const h=location.hash.slice(1);if(h&&document.getElementById('d-'+h))document.getElementById('d-'+h).showModal();
</script></body></html>"""


def covers_page(items):
    return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0}}{COVER_CSS}.cover{{width:1080px}}</style></head><body>' + "".join(f'<div id="c-{it["slug"]}">{cover(it)}</div>' for it in items) + "</body></html>"


def copy_md(items):
    L = [f"# {C.BRAND}: Stan Store Copy", "", f"Everything to paste into Stan for **{C.COACH}'s** store. Each product comes with:",
         "", "- **Buyer access link**: a private thank-you page with a big *Open your interactive program* button and a *Download your PDF book* button. Paste it into Stan as the product's delivery link (redirect URL or confirmation message).",
         "- **PDF book**: clickable contents, bookmarks, fillable workbook and a *Tap to open the interactive program* button on the cover. Upload it to Stan as the digital file too.",
         "- **Cover image** (`covers/<product>.png`, 1080×1080) for the Stan thumbnail.", "",
         "## Store profile", "", f"- **Display name:** {C.COACH}", f"- **Store name:** {C.BRAND}", f"- **Bio:** {C.STORE['bio']}", f"- **Tagline:** {C.STORE['tagline']}",
         "- **Theme:** soft lavender-white background `#f7f4fb`, ink `#17121f`, purple accent `#6b2fd6` (her favorite color). Logo and body cutout are in the ZIP's Brand folder. Fonts: Inter Tight (headings), Inter (body), Instrument Serif italic (accents).",
         "- **Profile photo:** a clean, well-lit photo of you in the gym. Natural light, neutral background.", "", "## Product order", ""]
    L += [f"{i + 1}. {it['thumb_title']}: {it['price']}" for i, it in enumerate(items)]
    for it in items:
        L += ["", "---", "", f"## {it['thumb_title']}", "", f"- **Stan product type:** {it['kind']}", f"- **Price:** {it['price']}" + (f" (shown as a discount from {it['strike']})" if it["strike"] else "")]
        if it["link"]:
            L += [f"- **Buyer access link (put this in Stan, keep it private):** {it['link']}", "- **PDF file to upload:** in the ZIP download"]
        L += [f"- **Cover image:** `getfitwithme/covers/{it['slug']}.png`", "", "**Thumbnail**", f"- Title: {it['thumb_title']}", f"- Subtitle: {it['thumb_sub']}", f"- Button: {it['button']}", "",
              "**Checkout page**", f"- Title: {it['checkout_title']}", "- Description:", "", f"> {it['desc']}", "", "- Bullets:"]
        L += [f"  - {b}" for b in it["bullets"]]
        L += [f"- Checkout button: {it['cta']}", "- Collect: name + email only"]
        if it.get("bump"):
            L += ["", "**Order bump**", f"- Headline: {it['bump']['title']}", f"- Description: {it['bump']['desc']}"]
        L += ["", "**Confirmation message**", f"> {it['thanks']}"]
    L += ["", "---", "", "## Launch kit", "", "**Captions**", ""] + [f"{i + 1}. {c}" for i, c in enumerate(C.LAUNCH["captions"])]
    L += ["", "**Launch-day story sequence**", ""] + [f"- {s}" for s in C.LAUNCH["story"]]
    L += ["", "**Comment-to-DM funnel**", "", C.LAUNCH["dm_keywords"], "", "**Pricing strategy**", "",
          "- The free guide builds your email list, so every follower can become a buyer later.",
          "- $12–$37 programs are easy first purchases straight from a Reel.",
          "- The $67 bundle sits second in the list so its value is obvious next to the individual prices.",
          "- The $49 call and $149/month coaching are your highest-paying offers. Mention them in your stories every week.",
          "- Order bumps on every checkout raise your average order value without any new content.", ""]
    return "\n".join(L)


# ================================================================ access page + download zip
def access_page(p):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Your {e(p['title'])} · {C.BRAND}</title>
{ICON}
{FONTS}<style>{TOKENS}{COVER_CSS}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.55 var(--font);-webkit-font-smoothing:antialiased}}
.wrap{{max-width:520px;margin:0 auto;padding:28px 16px 60px}}
.cv-wrap{{border-radius:20px;overflow:hidden;box-shadow:var(--shadow)}}
.wm{{font:800 12px var(--head);letter-spacing:.24em;text-transform:uppercase;color:var(--acc);margin:26px 0 6px}}
h1{{font:800 32px/1.08 var(--head);letter-spacing:-.025em;margin:0 0 8px}}.lead{{color:var(--ink2);margin:0 0 22px}}
.go{{display:flex;align-items:center;justify-content:center;gap:10px;background:var(--acc);color:var(--acc-ink);text-decoration:none;font:700 19px var(--head);padding:20px;border-radius:16px;box-shadow:0 12px 30px -12px var(--acc)}}
.go:active{{transform:scale(.98)}}
.dl{{display:flex;align-items:center;justify-content:center;gap:10px;margin-top:10px;background:var(--surface);color:var(--ink);text-decoration:none;font:600 16px var(--font);padding:16px;border-radius:14px;border:1px solid var(--line)}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin-top:18px}}
.card h2{{font:700 13px var(--font);letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin:0 0 10px}}
.card ol{{margin:0;padding-left:20px}}.card li{{margin:6px 0}}.card p{{margin:0;color:var(--ink2);font-size:15px}}
footer{{text-align:center;color:var(--mut);font-size:12.5px;margin-top:26px;line-height:1.6}}
</style></head><body><div class="wrap">
<div class="cv-wrap">{cover({"slug": p["slug"], "hue": p["hue"], "kicker": p["kicker"], "title": p["title"], "meta": p["meta"]})}</div>
<div style="display:flex;align-items:center;gap:12px;margin-top:24px"><img src="{MARK}" alt="" style="width:52px;height:52px;border-radius:50%;box-shadow:0 0 0 2px var(--acc-soft)"><div class="wm" style="margin:0">{e(C.BRAND)}</div></div><h1 style="margin-top:12px">You're in. Welcome!</h1>
<p class="lead">Thank you for {"grabbing" if p['stan']['price'] == "FREE" else "purchasing"} <b>{e(p['title'])}</b>. Everything you need is right here.</p>
<a class="go" href="app.html">Open your interactive program <span aria-hidden="true">→</span></a>
<a class="dl" href="{pdf_name(p)}" download>Download your PDF book</a>
<div class="card"><h2>Save it to your phone</h2><ol>
<li>Tap <b>Open your interactive program</b>.</li>
<li><b>iPhone:</b> tap the Share icon, then <b>Add to Home Screen</b>.<br><b>Android:</b> tap the ⋮ menu, then <b>Add to Home screen</b>.</li>
<li>Open it from your home screen like an app. Your progress saves automatically.</li></ol></div>
<div class="card"><h2>Bookmark this page</h2><p>This is your personal access page. Bookmark it, or keep the email it came in, so you can always get back to your program and PDF.</p></div>
<div class="card"><h2>Need help?</h2><p>Message me at <b>{e(C.SUPPORT)}</b> and I'll take care of you.</p></div>
<footer>© 2026 {e(C.COACH)} · {e(C.BRAND)}<br>This link is for your personal use only. Please don't share it.</footer>
</div></body></html>"""


def make_zip(items):
    os.makedirs(os.path.join(OUT, "download"), exist_ok=True)
    zp = os.path.join(OUT, "download", "Get-Fit-With-Me-Products.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("START HERE.txt", "\n".join([
            "GET FIT WITH ME - YOUR PRODUCT FILES", "",
            "Each product folder has:",
            "  - the PDF book (upload it to Stan as the digital download)",
            "  - the interactive app (.html file - opens in any web browser)",
            "  - the access page (.html - the thank-you page buyers see)",
            "  - Cover for Stan.png (the product thumbnail)",
            "  - BUYER ACCESS LINK.txt (the private link to paste into Stan)", "",
            "STAN-STORE-COPY.md has every title, description, button, price and order bump.", ""]))
        for n, p in enumerate(C.PRODUCTS, 1):
            d = f"{n:02d} {p['title']}/"
            pdf = os.path.join(folder(p), pdf_name(p))
            if os.path.exists(pdf): z.write(pdf, d + pdf_name(p))
            z.write(os.path.join(folder(p), "app.html"), d + f"{p['title']} - Interactive App.html")
            z.write(os.path.join(folder(p), "index.html"), d + f"{p['title']} - Access Page.html")
            cv = os.path.join(OUT, "covers", p["slug"] + ".png")
            if os.path.exists(cv): z.write(cv, d + "Cover for Stan.png")
            z.writestr(d + "BUYER ACCESS LINK.txt", f"{p['title']}\n\nGive buyers this link through Stan (after checkout):\n{access_url(p)}\n\n"
                       "It opens a thank-you page with an 'Open your interactive program' button and a 'Download your PDF book' button.\n")
        for it in items:
            cv = os.path.join(OUT, "covers", it["slug"] + ".png")
            if os.path.exists(cv): z.write(cv, "All Stan Covers/" + it["thumb_title"].replace("/", "-") + ".png")
        for f in ("logo.png", "logo-mark.png", "body-cutout.png"):
            z.write(os.path.join(BRAND, f), "Brand/" + f)
        z.write(os.path.join(OUT, "STAN-STORE-COPY.md"), "STAN-STORE-COPY.md")
    print("zip:", os.path.getsize(zp) // 1024, "KB")


# ================================================================ main
def main():
    engine = open(os.path.join(HERE, "engine.js"), encoding="utf-8").read()
    for p in C.PRODUCTS:
        os.makedirs(folder(p), exist_ok=True)
        with open(os.path.join(folder(p), "app.html"), "w", encoding="utf-8") as f: f.write(product_page(p, engine))
        with open(os.path.join(folder(p), "index.html"), "w", encoding="utf-8") as f: f.write(access_page(p))
    items = store_items()
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f: f.write(store_page(items))
    with open(os.path.join(OUT, "STAN-STORE-COPY.md"), "w", encoding="utf-8") as f: f.write(copy_md(items))
    print("built", len(C.PRODUCTS), "apps + store page + Stan copy")
    if "--pdf" in sys.argv:
        tmp = tempfile.mkdtemp()
        cp = os.path.join(tmp, "covers.html"); open(cp, "w").write(covers_page(items))
        subprocess.run(["node", os.path.join(HERE, "covers.js"), cp, os.path.join(OUT, "covers")] + [it["slug"] for it in items], check=True)
        print("rendered", len(items), "covers")
        make_pdfs()
    make_zip(items)


if __name__ == "__main__":
    main()
