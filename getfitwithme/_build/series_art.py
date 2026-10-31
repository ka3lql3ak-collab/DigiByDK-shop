#!/usr/bin/env python3
"""Thumbnail + profile pictures for the "30 Days to Her" account.
    python3 getfitwithme/_build/series_art.py"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import character as C  # noqa: E402
import scenes as Sc  # noqa: E402
import rooms as Rm  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "series", "art")
DEFS = C.DEFS + Sc.SCENE_DEFS + Rm.ROOM_DEFS


def mom(pose, face, x, foot, scale, prop=None, b=1, outfit="hoodie", head_drop=None):
    return f'<g transform="translate({x - 230*scale:.1f},{foot - 905*scale:.1f}) scale({scale})">{C.danielle(b, outfit, pose, face, prop, False, False, 0, head_drop)}</g>'


def kid(i, mood, x, foot, scale):
    st = C.KIDS[i]; s = scale * st["h"]
    return f'<g transform="translate({x - 100*s:.1f},{foot - 385*s:.1f}) scale({s:.4f})">{C.kid(st, mood)}</g>'


def txt(x, y, s, size, fill, anchor="middle", stroke=16, extra=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Anton" font-size="{size}" fill="{fill}" stroke="#000" stroke-width="{stroke}" paint-order="stroke" stroke-linejoin="round" {extra}>{s}</text>'


def thumbnail():
    """1080x1920 cover. Everything important sits in the middle 1080x1350 so Instagram's 3:4 grid crop keeps it."""
    tears = ""
    return (f'<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}'
            f'{Rm.doctor_office()}<rect width="1080" height="1920" fill="#160a2e" opacity=".55"/>'
            f'<radialGradient id="tg" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="#ff3d6e" stop-opacity=".55"/><stop offset="1" stop-color="#ff3d6e" stop-opacity="0"/></radialGradient>'
            f'<rect width="1080" height="1920" fill="url(#tg)"/>'
            # close-up: crying Danielle holding the lab results
            f'{mom("hold", "crying", 540, 2640, 2.25, prop="labs")}{tears}'
            f'<rect width="1080" height="1920" fill="url(#vig)" opacity=".75"/>'
            # kids peeking in at the bottom corner
            f'{kid(3, "sad", 900, 1990, 1.55)}'
            # headline
            f'<g transform="rotate(-3 540 330)"><rect x="70" y="250" width="940" height="140" rx="18" fill="#ffd84d" stroke="#000" stroke-width="8"/>'
            f'{txt(540, 352, "THE DOCTOR GAVE HER", 88, "#1a0d33", stroke=0)}</g>'
            f'{txt(540, 640, "30 DAYS", 250, "#fff", stroke=22)}'
            f'{txt(540, 1650, "TELL OR SECRET?", 100, "#ff5fa8", stroke=16)}'
            # episode badge + day
            f'<g transform="translate(900,150) rotate(8)"><rect x="-90" y="-62" width="180" height="124" rx="22" fill="#ff3d6e" stroke="#000" stroke-width="8"/>{txt(0, 34, "EP 1", 84, "#fff", stroke=0)}</g>'
            f'<rect x="60" y="110" width="270" height="84" rx="42" fill="#0c0918" stroke="#ffffff55" stroke-width="3"/>{txt(195, 170, "DAY 1/30", 54, "#ffd84d", stroke=0)}'
            f'{txt(540, 1770, "30 DAYS TO HER", 64, "#cfc4ff", stroke=10, extra="letter-spacing=\'6\'")}'
            f'</svg>')


def profile(variant):
    """1080x1080, designed for a circle crop."""
    if variant == 1:  # Danielle on Day 1 with the 30 badge
        return (f'<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">{DEFS}'
                f'<radialGradient id="pg1" cx=".5" cy=".42" r=".7"><stop offset="0" stop-color="#8b57ee"/><stop offset=".65" stop-color="#3a1284"/><stop offset="1" stop-color="#14062e"/></radialGradient>'
                f'<rect width="1080" height="1080" fill="url(#pg1)"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".5"/>' for x, y, r in ((180, 220, 5), (900, 260, 4), (840, 820, 6), (220, 860, 4), (980, 560, 3), (100, 520, 4)))
                + f'{mom("idle", "determined", 540, 1690, 1.65)}'
                f'<g transform="translate(780,770)"><circle r="140" fill="#ffd84d" stroke="#000" stroke-width="10"/>{txt(0, 52, "30", 160, "#1a0d33", stroke=0)}'
                f'{txt(0, 104, "DAYS", 40, "#1a0d33", stroke=0, extra="letter-spacing=\'4\'")}</g></svg>')
    # variant 2: bold "30" type mark with her silhouette
    return (f'<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">{DEFS}'
            f'<rect width="1080" height="1080" fill="#0f0a1f"/><circle cx="540" cy="540" r="470" fill="#6d32d4"/><circle cx="540" cy="540" r="470" fill="none" stroke="#ffd84d" stroke-width="16"/>'
            f'{txt(540, 690, "30", 640, "#ffd84d", stroke=24)}'
            f'<clipPath id="pc2"><circle cx="540" cy="540" r="470"/></clipPath><g clip-path="url(#pc2)">{mom("idle", "sad", 540, 1620, 1.45)}</g>'
            f'<rect x="200" y="800" width="680" height="120" rx="60" fill="#0f0a1f" stroke="#ffd84d" stroke-width="6"/>{txt(540, 885, "DAYS TO HER", 76, "#fff", stroke=0, extra="letter-spacing=\'4\'")}</svg>')


def profile_strong(variant):
    """Cute profile picture: strong Danielle flexing (Day-30 look), circle-crop safe, no text."""
    spark = "".join(f'<path d="M{x},{y-r} L{x+r*.25},{y-r*.25} L{x+r},{y} L{x+r*.25},{y+r*.25} L{x},{y+r} L{x-r*.25},{y+r*.25} L{x-r},{y} L{x-r*.25},{y-r*.25} Z" fill="#fff" opacity=".9"/>'
                    for x, y, r in ((190, 260, 26), (880, 230, 20), (930, 640, 16), (150, 640, 18), (300, 140, 12), (780, 120, 14)))
    if variant == 1:
        bg = ('<radialGradient id="ps1" cx=".5" cy=".45" r=".7"><stop offset="0" stop-color="#b98cff"/><stop offset=".55" stop-color="#6d32d4"/><stop offset="1" stop-color="#2a1260"/></radialGradient>'
              '<rect width="1080" height="1080" fill="url(#ps1)"/><circle cx="540" cy="520" r="360" fill="#ffffff" opacity=".08"/>')
        face, x, foot, sc = "happy", 540, 1700, 1.75
    else:
        bg = ('<linearGradient id="ps2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff8fc4"/><stop offset="1" stop-color="#8b57ee"/></linearGradient>'
              '<rect width="1080" height="1080" fill="url(#ps2)"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".18"/>' for x, y, r in ((120, 900, 160), (980, 160, 190), (900, 980, 110))))
        face, x, foot, sc = "smirk", 540, 1700, 1.75
    body = C.danielle(0, "bra", "flex", face, None, False, False, 0, None)
    return (f'<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">{DEFS}{bg}'
            f'<g transform="translate({x - 230*sc:.1f},{foot - 905*sc:.1f}) scale({sc})">{body}</g>{spark}</svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()
    jobs = [[os.path.join(OUT, "Episode-1-Thumbnail.png"), thumbnail(), 1080, 1920],
            [os.path.join(OUT, "Profile-Picture-Strong-1.png"), profile_strong(1), 1080, 1080],
            [os.path.join(OUT, "Profile-Picture-Strong-2.png"), profile_strong(2), 1080, 1080]]
    js = os.path.join(tmp, "r.js")
    open(js, "w").write("""const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();
for (const [path,svg,w,h] of jobs){const p=await b.newPage({viewport:{width:w,height:h}});
await p.setContent('<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Anton&display=swap" rel="stylesheet"><style>body{margin:0}svg{display:block}</style></head><body>'+svg+'</body></html>',{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready);await p.screenshot({path,clip:{x:0,y:0,width:w,height:h}});await p.close();}
await b.close()})();""")
    jf = os.path.join(tmp, "j.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", js, jf], check=True)
    print("ok")


if __name__ == "__main__":
    main()
