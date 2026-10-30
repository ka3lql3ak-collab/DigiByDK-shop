#!/usr/bin/env python3
"""Builds every Get Fit With Me page from content.py.
   python3 getfitwithme/_build/build.py            -> product pages, store, covers.html, STAN-STORE-COPY.md
   python3 getfitwithme/_build/build.py --covers   -> also renders covers/*.png with Playwright"""
import html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content as C  # noqa: E402

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Anton&family=Pacifico&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
e = html.escape

BASE_CSS = """
:root{--c1:#ff2e93;--c2:#8b2cf5;--bg:#0b0710;--card:#17101e;--ink:#fbeef6;--mut:#c9b3c6;--gold:#ffd36e;--line:rgba(255,255,255,.09)}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{scroll-behavior:smooth}
body{margin:0;font-family:Poppins,system-ui,sans-serif;color:var(--ink);background:var(--bg);min-height:100vh;overflow-x:hidden}
body:before{content:"";position:fixed;inset:-20%;z-index:-1;background:
 radial-gradient(40% 35% at 10% 0%,color-mix(in srgb,var(--c1) 40%,transparent),transparent 70%),
 radial-gradient(40% 35% at 100% 30%,color-mix(in srgb,var(--c2) 40%,transparent),transparent 70%),
 radial-gradient(35% 30% at 30% 100%,color-mix(in srgb,var(--c1) 25%,transparent),transparent 70%);
 animation:drift 18s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate(4%,-3%) rotate(6deg)}}
a{color:inherit}
.script{font-family:Pacifico,cursive;color:var(--gold);font-size:26px;margin:0;text-shadow:0 0 18px color-mix(in srgb,var(--gold) 60%,transparent)}
.marq{overflow:hidden;white-space:nowrap;background:linear-gradient(90deg,var(--c1),var(--c2));font:15px Anton,sans-serif;letter-spacing:2px;padding:7px 0;color:#fff}
.marq div{display:inline-block;animation:marq 22s linear infinite}
@keyframes marq{to{transform:translateX(-50%)}}
"""

PRODUCT_CSS = BASE_CSS + """
header{text-align:center;padding:26px 16px 8px;position:relative}
.brand{font:13px Anton;letter-spacing:4px;color:var(--mut);margin-bottom:8px}
h1{font:clamp(40px,11vw,76px)/.95 Anton,sans-serif;margin:6px 0 10px;text-transform:uppercase;letter-spacing:1px;
 background:linear-gradient(180deg,#fff 30%,color-mix(in srgb,var(--c1) 70%,#fff));-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 0 22px color-mix(in srgb,var(--c1) 60%,transparent))}
.sub{color:var(--mut);margin:0 auto 14px;max-width:520px}
.ring{--p:0;width:92px;height:92px;border-radius:50%;margin:8px auto;display:grid;place-items:center;
 background:conic-gradient(var(--c1) calc(var(--p)*1%),var(--c2) 0 calc(var(--p)*1%),rgba(255,255,255,.08) 0);box-shadow:0 0 30px color-mix(in srgb,var(--c1) 45%,transparent)}
.ring div{width:74px;height:74px;border-radius:50%;background:var(--bg);display:grid;place-items:center;text-align:center;line-height:1}
.ring b{font:24px Anton}.ring small{font-size:10px;color:var(--mut);letter-spacing:1px}
nav{position:sticky;top:0;z-index:5;display:flex;gap:8px;overflow-x:auto;padding:10px 16px;background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(12px);scrollbar-width:none;border-bottom:1px solid var(--line)}
nav::-webkit-scrollbar{display:none}
.tab{flex:none;border:1px solid var(--line);background:rgba(255,255,255,.04);color:var(--ink);border-radius:999px;padding:9px 15px;font:600 14px Poppins;cursor:pointer;display:flex;gap:6px;align-items:center}
.tab.on{background:linear-gradient(90deg,var(--c1),var(--c2));border-color:transparent;box-shadow:0 6px 20px color-mix(in srgb,var(--c1) 45%,transparent)}
main{max-width:760px;margin:0 auto;padding:14px 16px 120px}
.sectitle{font:30px Anton;letter-spacing:1px;margin:12px 0;text-transform:uppercase}
.card{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:18px;margin:14px 0;position:relative}
.card.glow{border-color:color-mix(in srgb,var(--c1) 45%,transparent);box-shadow:0 0 0 1px color-mix(in srgb,var(--c1) 20%,transparent),0 18px 50px -20px color-mix(in srgb,var(--c1) 70%,transparent)}
.card p{line-height:1.6}
.card h3{font:22px Anton;letter-spacing:.5px;margin:0 0 4px;text-transform:uppercase}
.card h4{font:16px Anton;letter-spacing:1px;margin:18px 0 6px;color:var(--gold);text-transform:uppercase}
.sig{font-family:Pacifico;color:var(--c1);font-size:22px;text-align:right;margin:0}
.muted{color:var(--mut);margin:2px 0 8px;font-size:14px}.fine{color:var(--mut);font-size:12px}.center{text-align:center}
.eyebrow{font:12px Anton;letter-spacing:2px;color:var(--c1);margin:0}
.chips{display:flex;gap:8px;overflow-x:auto;padding:4px 0 8px;scrollbar-width:none}
.chip{flex:none;border:1px solid var(--line);background:rgba(255,255,255,.05);color:var(--ink);border-radius:14px;padding:8px 14px;font:600 14px Poppins;cursor:pointer}
.chip.on{background:var(--ink);color:var(--bg)}.chip.done:not(.on){border-color:var(--c1);color:var(--c1)}
.phase{background:linear-gradient(90deg,color-mix(in srgb,var(--c1) 22%,transparent),color-mix(in srgb,var(--c2) 22%,transparent));border-radius:16px;padding:12px 14px;font-size:14px;line-height:1.5}
.tag{display:inline-block;background:var(--gold);color:#1a0f12;font:13px Anton;letter-spacing:1.5px;padding:3px 9px;border-radius:8px;margin-right:8px}
.dayhead{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
.day.complete{border-color:var(--c1)}
.stamp{flex:none;font:14px Anton;letter-spacing:1.5px;color:var(--c1);border:3px solid var(--c1);border-radius:10px;padding:4px 8px;transform:rotate(8deg);animation:stamp .4s cubic-bezier(.3,1.6,.6,1)}
@keyframes stamp{from{transform:rotate(8deg) scale(2.2);opacity:0}}
.ex{border-top:1px solid var(--line);padding:12px 0}
.exhead{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.exhead b{flex:1 1 100%;font-size:16px}
.pill{background:color-mix(in srgb,var(--c1) 22%,transparent);color:#fff;border-radius:999px;padding:3px 10px;font-size:12.5px;font-weight:600}
.pill.ghost{background:rgba(255,255,255,.06);color:var(--mut)}
.exrow{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:10px;flex-wrap:wrap}
.sets{display:flex;gap:8px;flex-wrap:wrap}
.set{width:42px;height:42px;border-radius:14px;border:2px solid color-mix(in srgb,var(--c1) 55%,transparent);background:transparent;color:var(--ink);font:700 15px Poppins;cursor:pointer;transition:.15s}
.set.on{background:linear-gradient(135deg,var(--c1),var(--c2));border-color:transparent;transform:scale(1.06);box-shadow:0 0 16px color-mix(in srgb,var(--c1) 60%,transparent)}
.wt{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--mut)}
input,select,textarea{font:500 16px Poppins;color:var(--ink);background:rgba(255,255,255,.06);border:1px solid var(--line);border-radius:12px;padding:10px 12px;width:100%}
.wt input{width:78px;text-align:center}
input:focus,select:focus,textarea:focus{outline:2px solid var(--c1);outline-offset:1px}
select option{background:#1b1220}
textarea{min-height:96px;resize:vertical;margin-top:6px}
details summary{cursor:pointer;color:var(--c1);font-size:13px;font-weight:600;margin-top:8px}
details p{font-size:14px;color:var(--mut);margin:6px 0 0}
.acc{border-bottom:1px solid var(--line);padding:6px 0 10px}.acc summary{font-size:16px;color:var(--ink);padding:6px 0}
.btn{display:inline-block;text-decoration:none;text-align:center;border:none;border-radius:16px;padding:12px 18px;font:700 15px Poppins;cursor:pointer;color:#fff;background:rgba(255,255,255,.1)}
.btn.big{display:block;width:100%;margin-top:14px;font:20px Anton;letter-spacing:1.5px;padding:15px;background:linear-gradient(90deg,var(--c1),var(--c2));box-shadow:0 10px 30px -8px color-mix(in srgb,var(--c1) 80%,transparent);transition:transform .1s}
.btn.big:active{transform:scale(.97)}.btn.ghost{background:rgba(255,255,255,.08);box-shadow:none;color:var(--mut)}
.bar{position:relative;height:26px;border-radius:999px;background:rgba(255,255,255,.07);overflow:hidden;margin:8px 0 12px}
.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--c1),var(--c2),var(--gold));transition:width .5s;border-radius:999px}
.bar span{position:absolute;inset:0;display:grid;place-items:center;font:600 12px Poppins;letter-spacing:.5px}
.check{display:flex;gap:12px;align-items:center;padding:11px 12px;border-radius:14px;background:rgba(255,255,255,.04);margin:7px 0;cursor:pointer;user-select:none;transition:.2s}
.check .box{flex:none;width:26px;height:26px;border-radius:8px;border:2px solid var(--c1);display:grid;place-items:center;font-weight:800}
.check.done{background:color-mix(in srgb,var(--c1) 16%,transparent)}.check.done span:last-child{text-decoration:line-through;opacity:.7}
.check.done .box{background:var(--c1);color:#fff}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:10px 0}
.stats div{background:var(--card);border:1px solid var(--line);border-radius:18px;text-align:center;padding:12px 4px}
.stats b{display:block;font:30px Anton}.stats span{font-size:12px;color:var(--mut)}
.grid30{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.dbtn{aspect-ratio:1;border-radius:14px;border:1px solid var(--line);background:rgba(255,255,255,.05);color:var(--ink);font:18px Anton;cursor:pointer}
.dbtn.on{background:linear-gradient(135deg,var(--c1),var(--c2));border:none}.dbtn.sel{outline:3px solid var(--gold);outline-offset:2px}
.moves{list-style:none;padding:0;margin:8px 0}.moves li{display:flex;justify-content:space-between;gap:10px;padding:9px 0;border-bottom:1px dashed var(--line)}
.moves b{color:var(--gold);white-space:nowrap}
.prompt{font-family:Pacifico;font-size:19px;color:var(--ink);line-height:1.5;margin:6px 0}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin:14px 0}
.tile{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:16px}
.tile.gold{border-color:var(--gold);box-shadow:0 0 24px -6px color-mix(in srgb,var(--gold) 60%,transparent)}
.ti{font-size:32px}.tile h4{font:18px Anton;letter-spacing:.5px;margin:6px 0 4px;text-transform:uppercase}.tile p{margin:0;color:var(--mut);font-size:14px;line-height:1.5}
.tile .big{color:var(--gold);font-size:18px}
.form{display:grid;grid-template-columns:1fr 1fr;gap:10px}.form label{font-size:13px;color:var(--mut);display:grid;gap:4px}.form .full{grid-column:1/-1}
.macros{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:16px 0 8px}
.mac{background:rgba(255,255,255,.05);border-radius:16px;padding:12px 4px;text-align:center}.mac b{display:block;font:24px Anton}.mac span{font-size:12px;color:var(--mut)}
.mac.cal{grid-column:1/-1;background:linear-gradient(90deg,var(--c1),var(--c2))}.mac.cal b{font-size:44px}.mac.cal span{color:#fff}
.meal{border-top:1px solid var(--line);padding:10px 0}.meal p{margin:4px 0 6px}
.hist{display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:center;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.hist span:first-child{color:var(--mut);font-size:12px}
.x{background:none;border:none;color:var(--mut);cursor:pointer;font-size:16px}
.ups{display:grid;gap:8px;margin:12px 0}
.up{display:flex;align-items:center;gap:10px;text-decoration:none;background:rgba(255,255,255,.05);border:1px solid var(--line);border-radius:16px;padding:12px;text-align:left}
.up span{font-size:24px}.up b{flex:1}.up em{font-style:normal;color:var(--gold);font-weight:700}
#tfab{position:fixed;right:16px;bottom:18px;z-index:9;width:62px;height:62px;border-radius:50%;border:none;font-size:28px;cursor:pointer;color:#fff;
 background:linear-gradient(135deg,var(--c1),var(--c2));box-shadow:0 10px 30px color-mix(in srgb,var(--c1) 60%,transparent)}
#timer{position:fixed;right:16px;bottom:92px;z-index:9;width:min(300px,calc(100vw - 32px));background:#1d1324;border:1px solid var(--c1);border-radius:22px;padding:16px;text-align:center;
 transform:translateY(20px) scale(.9);opacity:0;pointer-events:none;transition:.2s;box-shadow:0 20px 60px #000}
#timer.open{transform:none;opacity:1;pointer-events:auto}
#tnum{font:56px Anton;letter-spacing:2px}#timer.run #tnum{color:var(--gold);animation:pulse 1s infinite}
@keyframes pulse{50%{opacity:.6}}
#timer .row{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:8px}#timer .btn{padding:8px 11px;font-size:14px}
#toast{position:fixed;left:50%;top:18px;z-index:20;transform:translate(-50%,-140%);background:linear-gradient(90deg,var(--c1),var(--c2));color:#fff;font:18px Anton;letter-spacing:1px;padding:12px 20px;border-radius:999px;transition:.35s cubic-bezier(.3,1.5,.6,1);box-shadow:0 10px 30px #000a;text-align:center;max-width:90vw}
#toast.show{transform:translate(-50%,0)}
#confetti{position:fixed;inset:0;pointer-events:none;z-index:19}
footer{text-align:center;color:var(--mut);font-size:12px;padding:20px 16px 100px;max-width:640px;margin:0 auto;line-height:1.6}
footer button{background:none;border:1px solid var(--line);color:var(--mut);border-radius:10px;padding:6px 10px;cursor:pointer;margin-top:8px}
@media (max-width:480px){.macros{grid-template-columns:repeat(2,1fr)}.grid30{grid-template-columns:repeat(5,1fr)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

MARQ = " • ".join(["NO EXCUSES", "GET FIT WITH ME", "LIFT HEAVY", "GLOW LOUD", "STRONG IS SEXY", "BOOTY GAINS LOADING", "YOU BELONG HERE"]) + " • "


def product_page(p, engine, others):
    data = {"slug": p["slug"], "c1": p["c1"], "c2": p["c2"], "sections": p["sections"]}
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b0710"><meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{e(p['short'])}">
<title>{e(p['title'])} · {C.BRAND}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>{p['emoji']}</text></svg>">
{FONTS}
<style>{PRODUCT_CSS}:root{{--c1:{p['c1']};--c2:{p['c2']}}}</style></head><body>
<div class="marq" aria-hidden="true"><div>{MARQ * 6}</div></div>
<header>
 <div class="brand">{e(C.BRAND.upper())} · BY {e(C.COACH.upper())}</div>
 <p class="script">{e(p['script'])}</p>
 <h1>{e(p['title'])}</h1>
 <p class="sub">{e(p['sub'])}</p>
 <div class="ring" id="ring"><div><span><b id="ringn">0%</b><br><small>DONE</small></span></div></div>
</header>
<nav id="nav"></nav>
<main id="main"></main>
<footer>{e(C.DISCLAIMER)}<br>© 2026 {e(C.COACH)} · {e(C.BRAND)}. For personal use only — please don't share or resell 💜<br><button id="reset">Reset my progress</button></footer>
<button id="tfab" aria-label="Rest timer">⏱</button>
<div id="timer"><div class="eyebrow">REST TIMER</div><div id="tnum">0:00</div>
 <div class="row"><button class="btn" data-t="45">45s</button><button class="btn" data-t="60">1:00</button><button class="btn" data-t="90">1:30</button><button class="btn" data-t="120">2:00</button><button class="btn" data-t="180">3:00</button><button class="btn" data-t="+15">+15</button><button class="btn" data-t="stop">Stop</button></div>
 <p class="fine">Starts automatically when you tap off a set.</p></div>
<div id="toast" role="status"></div><canvas id="confetti"></canvas>
<script>const P={json.dumps(data, ensure_ascii=False)};const OTHERS={json.dumps(others, ensure_ascii=False)};
{engine}</script></body></html>"""


# ---------------------------------------------------------------- store page
def store_items():
    items = []
    for p in C.PRODUCTS:
        items.append({**p["stan"], "slug": p["slug"], "emoji": p["emoji"], "c1": p["c1"], "c2": p["c2"],
                      "big": p["title"], "script": p["script"], "link": p["slug"] + ".html"})
    items.insert(1, {**C.BUNDLE, "slug": "whole-baddie-bundle", "emoji": "👑", "c1": "#ffd36e", "c2": "#ff2e93",
                     "big": "Whole Baddie Bundle", "script": "everything. all of it.", "link": ""})
    for i, c in enumerate(C.COACHING):
        items.append({**c, "slug": ["form-check-call", "online-coaching"][i], "emoji": ["🎥", "💜"][i],
                      "c1": ["#3b82f6", "#8b2cf5"][i], "c2": "#ff2e93", "big": ["Form Check Call", "1:1 Coaching"][i],
                      "script": ["let's fix it", "work with me"][i], "link": ""})
    return items


def cover(it, size=""):
    return f"""<div class="cover {size}" style="--c1:{it['c1']};--c2:{it['c2']}"><div class="cv-in">
 <div class="cv-brand">GET FIT WITH ME</div><div class="cv-emoji">{it['emoji']}</div>
 <div class="cv-script">{e(it['script'])}</div><div class="cv-title">{e(it['big'])}</div>
 <div class="cv-by">BY DANIELLE DAWSON</div></div></div>"""


COVER_CSS = """
.cover{--c1:#ff2e93;--c2:#8b2cf5;position:relative;aspect-ratio:1;border-radius:18px;overflow:hidden;background:#0b0710;container-type:inline-size}
.cover:before{content:"";position:absolute;inset:0;background:radial-gradient(70% 60% at 20% 10%,var(--c1),transparent 70%),radial-gradient(70% 60% at 100% 100%,var(--c2),transparent 70%);opacity:.9}
.cover:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.05) 0 2px,transparent 2px 14px)}
.cv-in{position:relative;z-index:1;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:8cqw;color:#fff}
.cv-brand{font:4.6cqw Anton,sans-serif;letter-spacing:1.2cqw;opacity:.9}
.cv-emoji{font-size:20cqw;line-height:1.1;filter:drop-shadow(0 2cqw 4cqw rgba(0,0,0,.4))}
.cv-script{font:7cqw Pacifico,cursive;color:#ffd36e;text-shadow:0 0 4cqw rgba(0,0,0,.5)}
.cv-title{font:13cqw/.95 Anton,sans-serif;text-transform:uppercase;text-shadow:0 1cqw 0 rgba(0,0,0,.35),0 0 6cqw rgba(0,0,0,.4)}
.cv-by{font:3.8cqw Poppins,sans-serif;font-weight:700;letter-spacing:.8cqw;margin-top:4cqw;opacity:.85}
"""


def store_page(items):
    cards = []
    for it in items:
        bump = f"""<div class="bump"><label><input type="checkbox"> <b>YES! {e(it['bump']['title'])}</b></label><p>{e(it['bump']['desc'])}</p></div>""" if it.get("bump") else ""
        preview = f'<a class="btn ghost" href="{it["link"]}" target="_blank">👀 Preview the product</a>' if it["link"] else ""
        price = f'<span class="price">{e(it["price"])}</span>' + (f' <s>{e(it["strike"])}</s>' if it["strike"] else "")
        cards.append(f"""<article class="prod" id="{it['slug']}">
  <button class="pcard" data-open="{it['slug']}">{cover(it, 'sm')}
   <div class="pinfo"><h3>{e(it['thumb_title'])}</h3><p>{e(it['thumb_sub'])}</p><div>{price}</div></div></button>
  <button class="cta" data-open="{it['slug']}">{e(it['button'])}</button>
  <dialog id="d-{it['slug']}"><form method="dialog"><button class="close" aria-label="Close">✕</button></form>
   {cover(it)}
   <h2>{e(it['checkout_title'])}</h2><div class="pr">{price}</div>
   <p>{e(it['desc'])}</p>
   <ul>{''.join(f'<li>{e(b)}</li>' for b in it['bullets'])}</ul>
   {bump}
   <div class="form"><input placeholder="Full name"><input placeholder="Email address" type="email"></div>
   <button class="cta big" type="button">{e(it['cta'])}</button>
   {preview}
   <p class="note">Mock checkout — on Stan the real checkout replaces this.</p>
  </dialog></article>""")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0b0710"><title>{C.BRAND} · {C.COACH}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💪🏽</text></svg>">
{FONTS}<style>{BASE_CSS}{COVER_CSS}
.wrap{{max-width:480px;margin:0 auto;padding:28px 16px 60px}}
.hero{{text-align:center}}
.av{{width:118px;height:118px;border-radius:50%;margin:0 auto 12px;display:grid;place-items:center;font:44px Anton;color:#fff;position:relative;
 background:linear-gradient(135deg,var(--c1),var(--c2));box-shadow:0 0 0 4px var(--bg),0 0 0 7px var(--gold),0 0 50px var(--c1)}}
.av:after{{content:"✨";position:absolute;right:-6px;top:0;font-size:26px;animation:spin 4s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
h1{{font:44px/1 Anton;margin:6px 0 2px;text-transform:uppercase;letter-spacing:1px;filter:drop-shadow(0 0 16px var(--c1))}}
.who{{font-weight:600;margin:0}}.bio{{color:var(--mut);font-size:14.5px;line-height:1.55;margin:10px 0}}
.soc{{display:flex;justify-content:center;gap:10px;margin:12px 0 22px}}
.soc a{{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.08);text-decoration:none;font:700 13px Poppins}}
.prod{{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:12px;margin:14px 0}}
.pcard{{all:unset;cursor:pointer;display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:center;width:100%}}
.pcard .cover{{border-radius:14px}}
.pinfo h3{{font:19px/1.15 Anton;letter-spacing:.3px;margin:0 0 4px;text-transform:uppercase}}.pinfo p{{margin:0 0 6px;color:var(--mut);font-size:13px;line-height:1.4}}
.price{{font:20px Anton;color:var(--gold)}}s{{color:var(--mut);font-size:14px}}
.cta{{display:block;width:100%;margin-top:12px;border:none;border-radius:16px;padding:14px;font:18px Anton;letter-spacing:1.2px;color:#fff;cursor:pointer;
 background:linear-gradient(90deg,var(--c1),var(--c2));box-shadow:0 10px 26px -10px var(--c1);text-transform:uppercase}}
.prod:nth-of-type(2){{border:2px solid var(--gold);box-shadow:0 0 40px -10px var(--gold)}}
.prod:nth-of-type(2):before{{content:"🔥 BEST VALUE";display:block;font:13px Anton;letter-spacing:2px;color:var(--gold);margin:0 0 8px 4px}}
dialog{{width:min(520px,calc(100vw - 24px));max-height:92vh;border:1px solid var(--c1);border-radius:26px;background:#140d1a;color:var(--ink);padding:18px;overflow-y:auto}}
dialog::backdrop{{background:#000c;backdrop-filter:blur(6px)}}
dialog .cover{{width:100%}}
dialog h2{{font:30px/1.05 Anton;text-transform:uppercase;margin:16px 0 6px}}dialog p{{line-height:1.6;color:#e8d7e4}}
dialog ul{{padding:0;list-style:none}}dialog li{{padding:7px 0 7px 30px;position:relative;border-bottom:1px solid var(--line)}}
dialog li:before{{content:"✓";position:absolute;left:4px;color:var(--c1);font-weight:800}}
.close{{position:sticky;top:0;float:right;z-index:3;width:38px;height:38px;border-radius:50%;border:none;background:#fff2;color:#fff;font-size:18px;cursor:pointer}}
.bump{{border:2px dashed var(--gold);border-radius:16px;padding:12px;margin:14px 0;background:#ffd36e12}}.bump p{{margin:4px 0 0;font-size:14px}}
.form{{display:grid;gap:8px}}.form input{{font:16px Poppins;padding:12px;border-radius:12px;border:1px solid var(--line);background:#ffffff0d;color:#fff}}
.cta.big{{font-size:22px;padding:17px}}
.btn.ghost{{display:block;text-align:center;margin-top:10px;padding:12px;border-radius:14px;background:#ffffff10;text-decoration:none;font-weight:600}}
.note{{font-size:12px;color:var(--mut);text-align:center}}
footer{{text-align:center;color:var(--mut);font-size:12px;margin-top:30px}}
</style></head><body>
<div class="marq" aria-hidden="true"><div>{MARQ * 6}</div></div>
<div class="wrap"><section class="hero">
 <div class="av" aria-label="Profile photo">DD</div>
 <p class="script">{e(C.STORE['tagline'])}</p>
 <h1>{e(C.BRAND)}</h1><p class="who">{e(C.COACH)} · {e(C.HANDLE)}</p>
 <p class="bio">{e(C.STORE['bio'])}</p>
 <div class="soc"><a href="#" aria-label="Instagram">IG</a><a href="#" aria-label="TikTok">TT</a><a href="#" aria-label="YouTube">YT</a><a href="#" aria-label="Email">✉️</a></div>
</section>
{''.join(cards)}
<footer>© 2026 {e(C.COACH)} · {e(C.BRAND)}</footer></div>
<script>
document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>document.getElementById('d-'+b.dataset.open).showModal());
document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',ev=>{{if(ev.target===d)d.close()}}));
const h=location.hash.slice(1);if(h&&document.getElementById('d-'+h))document.getElementById('d-'+h).showModal();
</script></body></html>"""


def covers_page(items):
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#000}}{COVER_CSS}
.cover{{width:1080px;border-radius:0;margin:0 0 20px}}</style></head><body>
{''.join(f'<div id="c-{it["slug"]}">{cover(it)}</div>' for it in items)}</body></html>"""


# ---------------------------------------------------------------- Stan copy doc
def copy_md(items, base_url):
    L = [f"# {C.BRAND} — Stan Store Copy", "", f"Everything to paste into Stan for **{C.COACH}'s** store. Cover images are in `getfitwithme/covers/`.", "",
         "## Store profile", "", f"- **Store name / display name:** {C.BRAND}", f"- **Name:** {C.COACH}", f"- **Bio:** {C.STORE['bio']}",
         f"- **Tagline (header):** {C.STORE['tagline']}", "- **Theme:** dark background, hot pink `#ff2e93` + purple `#8b2cf5`, gold accent `#ffd36e`. Fonts: Anton (headings) and Poppins (body).",
         "- **Profile photo:** a bright, close-up gym selfie (you smiling with the dumbbells works great).", "",
         "## Product order (top to bottom)", ""]
    L += [f"{i + 1}. {it['thumb_title']} — {it['price']}" for i, it in enumerate(items)]
    L.append("")
    for it in items:
        L += [f"---", "", f"## {it['thumb_title']}", "", f"**Stan product type:** {it['kind']}  ", f"**Price:** {it['price']}" + (f" (strike-through/discount from {it['strike']})" if it['strike'] else ""), ""]
        if it["link"]:
            L += [f"**Product link to deliver (paste as the URL / redirect):** {base_url}/{it['link']}", ""]
        L += ["### Thumbnail (store button)", f"- **Title:** {it['thumb_title']}", f"- **Subtitle:** {it['thumb_sub']}", f"- **Button:** {it['button']}", f"- **Cover image:** `covers/{it['slug']}.png`", "",
              "### Checkout page", f"- **Title:** {it['checkout_title']}", f"- **Description:**", "", f"> {it['desc']}", "", "- **Bullets:**"]
        L += [f"  - ✅ {b}" for b in it["bullets"]]
        L += [f"- **Checkout button:** {it['cta']}", "- **Collect:** Name + Email (keep it short; every extra field costs sales)"]
        if it.get("bump"):
            L += ["", "### Order bump", f"- **Headline:** {it['bump']['title']}", f"- **Description:** {it['bump']['desc']}"]
        L += ["", "### Confirmation / thank-you message", f"> {it['thanks']}", ""]
    L += ["---", "", "## Launch promo kit", "", "### Captions"]
    L += [f"{i + 1}. {c}" for i, c in enumerate(C.LAUNCH["captions"])]
    L += ["", "### Launch-day Instagram story sequence"] + [f"- {s}" for s in C.LAUNCH["story"]]
    L += ["", "### Comment-to-DM funnel", C.LAUNCH["dm_keywords"], "",
          "### Pricing strategy", "- **Free Glute Starter Pack** collects emails, so every follower can become a buyer later.",
          "- **$12 to $37 products** are easy impulse buys from a Reel.", "- **The $67 bundle** sits at #2 so it's the obvious deal next to the individual prices.",
          "- **$49 call and $149/mo coaching** are your highest-paying offers. Mention them in your stories every week.",
          "- **Order bumps** on every checkout raise your average order without extra content.", ""]
    return "\n".join(L)


def main():
    engine = open(os.path.join(HERE, "engine.js"), encoding="utf-8").read()
    others = [{"slug": p["slug"], "short": p["short"], "emoji": p["emoji"], "price": p["stan"]["price"]} for p in C.PRODUCTS]
    others.insert(1, {"slug": "whole-baddie-bundle", "short": "The Whole Baddie Bundle", "emoji": "👑", "price": C.BUNDLE["price"]})
    for p in C.PRODUCTS:
        with open(os.path.join(OUT, p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(product_page(p, engine, others))
    items = store_items()
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(store_page(items))
    with open(os.path.join(HERE, "covers.html"), "w", encoding="utf-8") as f:
        f.write(covers_page(items))
    with open(os.path.join(OUT, "STAN-STORE-COPY.md"), "w", encoding="utf-8") as f:
        f.write(copy_md(items, "https://ka3lql3ak-collab.github.io/digibydk-shop/getfitwithme"))
    if "--covers" in sys.argv:
        subprocess.run(["node", os.path.join(HERE, "covers.js"), os.path.join(HERE, "covers.html"), os.path.join(OUT, "covers")] +
                       [it["slug"] for it in items], check=True)
    print("built", len(C.PRODUCTS), "products + store")


if __name__ == "__main__":
    main()
