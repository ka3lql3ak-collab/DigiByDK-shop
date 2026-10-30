#!/usr/bin/env python3
"""Renders the "30 Days to Her" TikTok/Reels series: 1080x1920 frames, end cards, rough-cut MP4s and the script book.
    python3 getfitwithme/_build/series.py"""
import html, json, os, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "series")
sys.path.insert(0, HERE)
from series_content import SERIES, EPISODES  # noqa: E402

e = html.escape
W, H = 1080, 1920
lerp = lambda a, b, t: a + (b - a) * t

SKIN, SKIN_D = "#9b6545", "#83533a"
HAIR, HAIR_D, HAIR_L = "#7a2142", "#561330", "#a3345f"
PURPLE, PURPLE_D, PURPLE_L = "#6d32d4", "#5223a8", "#8b57ee"


# ================================================================ cartoon Danielle
def danielle(b=0.0, outfit="bra", pose="idle", face="happy", prop=None, phones=False):
    """SVG group in a 420x840 box (feet at y≈830). b: 1 = Day 1 body, 0 = Day 30 buff."""
    cx = 210
    sh, ch, wa, hp = lerp(84, 90, b), lerp(74, 92, b), lerp(40, 86, b), lerp(76, 90, b)
    th = lerp(56, 68, b)
    up_w, fo_w = lerp(36, 42, b), lerp(28, 34, b)
    hy = 150 + (12 if pose == "slump" else 0)
    hrx = lerp(58, 68, b)
    top = {"hoodie": "#8e86a3", "tee": "#9b7fd4", "tank": "#1d1a22", "bra": "#1d1a22"}[outfit]
    bottom = {"hoodie": "#5d586b", "tee": "#25222b", "tank": PURPLE, "bra": PURPLE}[outfit]
    shoe = "#d9d4e2" if outfit == "hoodie" else "#f6f3fb"
    g = []
    # --- hair (back)
    if outfit != "hoodie":
        g.append(f'<path d="M{cx-hrx-6},{hy-40} Q{cx-hrx-22},{hy+110} {cx-hrx-14},{hy+200} L{cx+hrx+14},{hy+200} Q{cx+hrx+22},{hy+110} {cx+hrx+6},{hy-40} Z" fill="{HAIR_D}"/>')
    # --- legs
    g.append(f'<path d="M{cx-hp+6},425 C{cx-hp-16},485 {cx-hp-6},565 {cx-th},645 L{cx-th+14},805 L{cx-8},805 L{cx-5},560 L{cx+5},560 L{cx+8},805 L{cx+th-14},805 L{cx+th},645 C{cx+hp+6},565 {cx+hp+16},485 {cx+hp-6},425 Z" fill="{bottom}"/>')
    if outfit in ("tank", "bra"):
        g.append(f'<path d="M{cx+hp-14},450 C{cx+hp+2},520 {cx+hp-6},590 {cx+th-6},650" stroke="{PURPLE_L}" stroke-width="7" fill="none" opacity=".7"/>')
        g.append(f'<path d="M{cx-hp+14},450 C{cx-hp-2},520 {cx-hp+6},590 {cx-th+6},650" stroke="{PURPLE_L}" stroke-width="7" fill="none" opacity=".5"/>')
    for sx in (-1, 1):
        x0 = cx + sx * (th - 4) - (40 if sx > 0 else 0)
        g.append(f'<rect x="{min(cx + sx*8, cx + sx*(th-14)) - (0 if sx>0 else 0)}" y="800" width="{th-22+10}" height="30" rx="14" fill="{shoe}"/>' if False else "")
    g.append(f'<rect x="{cx-th+8}" y="798" width="{th-10}" height="32" rx="15" fill="{shoe}"/><rect x="{cx+2}" y="798" width="{th-10}" height="32" rx="15" fill="{shoe}"/>')
    g.append(f'<rect x="{cx-th+8}" y="822" width="{th-10}" height="8" rx="4" fill="#bdb4cc"/><rect x="{cx+2}" y="822" width="{th-10}" height="8" rx="4" fill="#bdb4cc"/>')
    # --- torso
    torso = (f'M{cx-sh},268 Q{cx},250 {cx+sh},268 C{cx+ch+4},300 {cx+wa+4},350 {cx+wa},398 L{cx+hp-4},432 '
             f'L{cx-hp+4},432 L{cx-wa},398 C{cx-wa-4},350 {cx-ch-4},300 {cx-sh},268 Z')
    g.append(f'<path d="{torso}" fill="{SKIN}"/>')
    if outfit == "hoodie":
        g.append(f'<path d="M{cx-sh-6},266 Q{cx},248 {cx+sh+6},266 C{cx+ch+12},305 {cx+wa+12},360 {cx+wa+8},440 L{cx-wa-8},440 C{cx-wa-12},360 {cx-ch-12},305 {cx-sh-6},266 Z" fill="{top}"/>')
        g.append(f'<path d="M{cx-34},252 Q{cx},300 {cx+34},252" stroke="#7a7290" stroke-width="16" fill="none"/>')
        g.append(f'<line x1="{cx-12}" y1="272" x2="{cx-14}" y2="330" stroke="#efeaf5" stroke-width="4"/><line x1="{cx+12}" y1="272" x2="{cx+14}" y2="326" stroke="#efeaf5" stroke-width="4"/>')
        g.append(f'<rect x="{cx-52}" y="372" width="104" height="44" rx="12" fill="#7f7795"/>')
        if b > .5:
            g.append(f'<path d="M{cx-wa+6},405 Q{cx},430 {cx+wa-6},405" stroke="#7a7290" stroke-width="5" fill="none"/>')
    elif outfit == "tee":
        g.append(f'<path d="M{cx-sh-8},266 Q{cx},250 {cx+sh+8},266 C{cx+ch+10},305 {cx+wa+10},360 {cx+wa+6},436 L{cx-wa-6},436 C{cx-wa-10},360 {cx-ch-10},305 {cx-sh-8},266 Z" fill="{top}"/>')
        g.append(f'<path d="M{cx-30},258 Q{cx},284 {cx+30},258" stroke="{SKIN}" stroke-width="10" fill="none"/>')
        g.append(f'<text x="{cx}" y="350" text-anchor="middle" font-family="Anton" font-size="26" fill="#efe8ff" opacity=".9">MOM</text>')
    else:
        low = 352 if outfit == "bra" else 420
        g.append(f'<path d="M{cx-sh+6},270 Q{cx},252 {cx+sh-6},270 C{cx+ch+2},300 {cx+ch-2},330 {cx+ch-6},{low} Q{cx},{low+12} {cx-ch+6},{low} C{cx-ch+2},330 {cx-ch-2},300 {cx-sh+6},270 Z" fill="{top}"/>')
        g.append(f'<path d="M{cx-26},262 L{cx},300 L{cx+26},262 Z" fill="{SKIN}"/>')
        if outfit == "bra":
            g.append(f'<path d="M{cx-ch+10},{low-6} Q{cx},{low+4} {cx+ch-10},{low-6}" stroke="#3a3542" stroke-width="5" fill="none"/>')
            if b < .4:  # abs + obliques
                a = 1 - b / .4
                for yy in (372, 392):
                    g.append(f'<path d="M{cx-16},{yy} q8,4 14,0 M{cx+2},{yy} q8,4 14,0" stroke="{SKIN_D}" stroke-width="3" fill="none" opacity="{.8*a:.2f}"/>')
                g.append(f'<line x1="{cx}" y1="364" x2="{cx}" y2="412" stroke="{SKIN_D}" stroke-width="3" opacity="{.7*a:.2f}"/>')
            g.append(f'<path d="M{cx-34},402 q10,-8 22,-2 q10,6 22,-2 q10,-6 20,2" stroke="#3b2a24" stroke-width="2.5" fill="none" opacity=".75"/>')  # tattoo
            g.append(f'<circle cx="{cx}" cy="414" r="3" fill="{SKIN_D}"/>')
    # waistband
    if outfit != "hoodie":
        g.append(f'<path d="M{cx-wa-2},{416 if outfit!="tee" else 432} L{cx+wa+2},{416 if outfit!="tee" else 432} L{cx+hp-4},440 L{cx-hp+4},440 Z" fill="{PURPLE_D if outfit in ("tank","bra") else "#18161d"}"/>')
    # --- neck + head
    g.append(f'<rect x="{cx-20}" y="{hy+48}" width="40" height="{262-hy-44}" fill="{SKIN_D}"/>')
    sl = sh - 8
    arms = {
        "idle": ((-18, 85), (-12, 165)), "hip": ((-46, 74), (22, 146)), "flex": ((-80, -14), (-62, -100)),
        "slump": ((-6, 92), (None, None)), "hold": None, "phone": None, "curl": None, "point": None,
    }
    def arm(side, elbow, hand, sleeve_full, sleeve_upper):
        sx, sy = cx + side * sl, 282
        ex, ey = sx + side * elbow[0] if side < 0 else sx - elbow[0], sy + elbow[1]
        hx, hy2 = (sx + side * hand[0] if side < 0 else sx - hand[0]), sy + hand[1]
        upc = top if (sleeve_full or sleeve_upper) else SKIN
        foc = top if sleeve_full else SKIN
        s = f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" stroke="{upc}" stroke-width="{up_w}" stroke-linecap="round"/>'
        s += f'<line x1="{ex}" y1="{ey}" x2="{hx}" y2="{hy2}" stroke="{foc}" stroke-width="{fo_w}" stroke-linecap="round"/>'
        if not (sleeve_full or sleeve_upper) and b < .55:  # delts
            s += f'<circle cx="{sx}" cy="{sy+2}" r="{up_w/2+4:.1f}" fill="{SKIN}"/><path d="M{sx-side*14},{sy+16} q{side*10},10 {side*22},4" stroke="{SKIN_D}" stroke-width="3" fill="none" opacity=".6"/>'
        if pose == "flex" and not sleeve_full and b < .7:  # bicep peak
            mx, my = (sx + ex) / 2, (sy + ey) / 2 - 10
            s += f'<ellipse cx="{mx}" cy="{my}" rx="{lerp(26,16,b):.0f}" ry="{lerp(20,12,b):.0f}" fill="{SKIN}"/><path d="M{mx-18},{my+6} q18,-16 36,0" stroke="{SKIN_D}" stroke-width="3" fill="none" opacity=".5"/>'
        if sleeve_full:
            s += f'<circle cx="{hx}" cy="{hy2}" r="{fo_w/2+2:.0f}" fill="#7a7290"/>'
        s += f'<circle cx="{hx}" cy="{hy2}" r="{fo_w/2+1:.0f}" fill="{SKIN}"/>'
        return s, (hx, hy2)
    full, upper = outfit == "hoodie", outfit == "tee"
    P = {
        "idle": [((-18, 85), (-12, 165)), ((-18, 85), (-12, 165))],
        "hip": [((-46, 74), (22, 146)), ((-46, 74), (22, 146))],
        "flex": [((-80, -14), (-62, -100)), ((-80, -14), (-62, -100))],
        "slump": [((-8, 92), (40, 175)), ((-8, 92), (40, 175))],
        "hold": [((-18, 85), (-12, 165)), ((-20, 88), (36, 52))],
        "phone": [((-18, 85), (-12, 165)), ((-26, 74), (40, -66))],
        "curl": [((-46, 74), (22, 146)), ((-14, 90), (-8, 22))],
        "point": [((-46, 74), (22, 146)), ((-56, -34), (-76, -128))],
    }[pose]
    a1, _ = arm(-1, P[0][0], P[0][1], full, upper)
    a2, hand = arm(1, P[1][0], P[1][1], full, upper)
    # --- head
    hd = [f'<ellipse cx="{cx}" cy="{hy}" rx="{hrx}" ry="{lerp(70,74,b):.0f}" fill="{SKIN}"/>']
    if b > .6:
        hd.append(f'<path d="M{cx-30},{hy+70} Q{cx},{hy+84} {cx+30},{hy+70}" stroke="{SKIN_D}" stroke-width="3" fill="none" opacity=".6"/>')
    # hair front
    if outfit == "hoodie":  # messy bun
        hd.append(f'<path d="M{cx-hrx-4},{hy+10} Q{cx-hrx-2},{hy-78} {cx},{hy-80} Q{cx+hrx+2},{hy-78} {cx+hrx+4},{hy+10} Q{cx+hrx-6},{hy-34} {cx+20},{hy-44} Q{cx-20},{hy-40} {cx-hrx+4},{hy-14} Z" fill="{HAIR}"/>')
        hd.append(f'<circle cx="{cx+6}" cy="{hy-96}" r="34" fill="{HAIR}"/><circle cx="{cx-14}" cy="{hy-104}" r="18" fill="{HAIR_L}" opacity=".6"/>')
        hd.append(f'<path d="M{cx-hrx+2},{hy-6} q-14,40 -4,78 M{cx+hrx-4},{hy-10} q16,36 6,70 M{cx+30},{hy-120} q22,-14 30,4" stroke="{HAIR}" stroke-width="5" fill="none"/>')
    else:
        hd.append(f'<path d="M{cx-hrx-6},{hy+20} Q{cx-hrx-6},{hy-82} {cx},{hy-82} Q{cx+hrx+6},{hy-82} {cx+hrx+6},{hy+20} Q{cx+hrx-6},{hy-38} {cx+16},{hy-48} Q{cx-24},{hy-46} {cx-hrx+2},{hy-6} Z" fill="{HAIR}"/>')
        hd.append(f'<path d="M{cx-hrx-6},{hy} Q{cx-hrx-18},{hy+90} {cx-hrx-6},{hy+150} L{cx-hrx+12},{hy+150} Q{cx-hrx+2},{hy+80} {cx-hrx+6},{hy+10} Z" fill="{HAIR}"/>')
        hd.append(f'<path d="M{cx+hrx+6},{hy} Q{cx+hrx+18},{hy+90} {cx+hrx+6},{hy+150} L{cx+hrx-12},{hy+150} Q{cx+hrx-2},{hy+80} {cx+hrx-6},{hy+10} Z" fill="{HAIR}"/>')
        hd.append(f'<path d="M{cx-20},{hy-66} Q{cx+20},{hy-74} {cx+46},{hy-50}" stroke="{HAIR_L}" stroke-width="6" fill="none" opacity=".7"/>')
    if phones:
        hd.append(f'<path d="M{cx-hrx-4},{hy+4} Q{cx-hrx-6},{hy-96} {cx},{hy-96} Q{cx+hrx+6},{hy-96} {cx+hrx+4},{hy+4}" stroke="#2b2b33" stroke-width="12" fill="none"/>')
        hd.append(f'<rect x="{cx-hrx-18}" y="{hy-26}" width="28" height="56" rx="11" fill="#2b2b33"/><rect x="{cx+hrx-10}" y="{hy-26}" width="28" height="56" rx="11" fill="#2b2b33"/>')
    hd.append(face_svg(face, cx, hy))
    return "".join(g) + a1 + "".join(hd) + a2 + prop_svg(prop, *hand)


def face_svg(face, cx, hy):
    ex, ey = 26, hy + 2
    f = []
    f.append(f'<ellipse cx="{cx-40}" cy="{hy+28}" rx="13" ry="8" fill="#d1797f" opacity=".35"/><ellipse cx="{cx+40}" cy="{hy+28}" rx="13" ry="8" fill="#d1797f" opacity=".35"/>')
    def eye(x, open_=1.0, look=0):
        s = f'<ellipse cx="{x}" cy="{ey}" rx="12" ry="{9*open_:.1f}" fill="#fff"/><circle cx="{x+look}" cy="{ey+1}" r="{6.5 if open_>.5 else 5}" fill="#2a1a14"/><circle cx="{x+look+2}" cy="{ey-2}" r="2" fill="#fff"/>'
        s += f'<path d="M{x-14},{ey-4*open_-2} Q{x},{ey-11*open_-4} {x+15},{ey-6*open_-3}" stroke="#1b110d" stroke-width="4" fill="none" stroke-linecap="round"/>'
        if open_ < .8:
            s += f'<path d="M{x-13},{ey-1} Q{x},{ey-12} {x+13},{ey-1} L{x+13},{ey-8} L{x-13},{ey-8} Z" fill="{SKIN}"/><path d="M{x-13},{ey} Q{x},{ey-6} {x+13},{ey}" stroke="#1b110d" stroke-width="3" fill="none"/>'
        return s
    brow = lambda x, a, y0=-22: f'<path d="M{x-14},{ey+y0+a} Q{x},{ey+y0-6} {x+14},{ey+y0-a}" stroke="#2a1510" stroke-width="5" fill="none" stroke-linecap="round"/>'
    my = hy + 42
    if face == "happy":
        f += [eye(cx - ex), eye(cx + ex), brow(cx - ex, 0), brow(cx + ex, 0)]
        f.append(f'<path d="M{cx-22},{my-4} Q{cx},{my+22} {cx+22},{my-4} Z" fill="#7a2a35"/><path d="M{cx-18},{my-3} L{cx+18},{my-3} L{cx+15},{my+3} L{cx-15},{my+3} Z" fill="#fff"/><path d="M{cx-22},{my-4} Q{cx},{my-10} {cx+22},{my-4}" stroke="#c66b7c" stroke-width="5" fill="none"/>')
    elif face == "smirk":
        f += [eye(cx - ex, .85), eye(cx + ex, .85), brow(cx - ex, 0), brow(cx + ex, -4, -26)]
        f.append(f'<path d="M{cx-18},{my} Q{cx},{my+6} {cx+20},{my-8}" stroke="#b55d6e" stroke-width="9" fill="none" stroke-linecap="round"/>')
    elif face == "determined":
        f += [eye(cx - ex, .8), eye(cx + ex, .8)]
        f.append(f'<path d="M{cx-ex-14},{ey-24} L{cx-ex+14},{ey-16}" stroke="#2a1510" stroke-width="6" stroke-linecap="round"/><path d="M{cx+ex+14},{ey-24} L{cx+ex-14},{ey-16}" stroke="#2a1510" stroke-width="6" stroke-linecap="round"/>')
        f.append(f'<path d="M{cx-18},{my} Q{cx},{my+5} {cx+18},{my}" stroke="#b55d6e" stroke-width="9" fill="none" stroke-linecap="round"/>')
    elif face == "shocked":
        f += [eye(cx - ex, 1.25), eye(cx + ex, 1.25), brow(cx - ex, 0, -30), brow(cx + ex, 0, -30)]
        f.append(f'<ellipse cx="{cx}" cy="{my+4}" rx="12" ry="16" fill="#5e1f2a"/><ellipse cx="{cx}" cy="{my+4}" rx="12" ry="16" fill="none" stroke="#c66b7c" stroke-width="4"/>')
    elif face == "tired":
        f += [eye(cx - ex, .45), eye(cx + ex, .45)]
        f.append(f'<path d="M{cx-ex-12},{ey+12} q12,6 24,0 M{cx+ex-12},{ey+12} q12,6 24,0" stroke="#6b4030" stroke-width="3" fill="none" opacity=".7"/>')
        f.append(f'<path d="M{cx-16},{my+2} L{cx+16},{my+2}" stroke="#b55d6e" stroke-width="8" stroke-linecap="round"/>')
    elif face in ("sad", "crying"):
        f += [eye(cx - ex, .7, -2) if face == "sad" else "", eye(cx + ex, .7, -2) if face == "sad" else ""]
        if face == "crying":
            f.append(f'<path d="M{cx-ex-12},{ey+2} Q{cx-ex},{ey+10} {cx-ex+12},{ey+2} M{cx+ex-12},{ey+2} Q{cx+ex},{ey+10} {cx+ex+12},{ey+2}" stroke="#1b110d" stroke-width="4" fill="none" stroke-linecap="round"/>')
            f.append(f'<path d="M{cx-ex-4},{ey+8} q-8,30 -2,64 q4,4 8,0 q2,-34 -2,-64 Z M{cx+ex+4},{ey+8} q8,30 2,64 q-4,4 -8,0 q-2,-34 2,-64 Z" fill="#8fd3ff" opacity=".9"/>')
        f.append(f'<path d="M{cx-ex-14},{ey-18} L{cx-ex+12},{ey-26}" stroke="#2a1510" stroke-width="5" stroke-linecap="round"/><path d="M{cx+ex+14},{ey-18} L{cx+ex-12},{ey-26}" stroke="#2a1510" stroke-width="5" stroke-linecap="round"/>')
        f.append(f'<path d="M{cx-18},{my+8} Q{cx},{my-8} {cx+18},{my+8}" stroke="#b55d6e" stroke-width="8" fill="none" stroke-linecap="round"/>')
    f.append(f'<path d="M{cx-4},{hy+12} Q{cx-10},{hy+26} {cx},{hy+28} Q{cx+8},{hy+28} {cx+8},{hy+22}" stroke="{SKIN_D}" stroke-width="3.5" fill="none"/><circle cx="{cx+11}" cy="{hy+24}" r="2.6" fill="#f5f5f5"/>')
    return "".join(f)


def prop_svg(p, x, y):
    if not p: return ""
    if p == "phone": return f'<g transform="translate({x-22},{y-50})"><rect width="44" height="84" rx="8" fill="#16131b"/><rect x="4" y="8" width="36" height="66" rx="4" fill="#7fb4ff"/></g>'
    if p == "dumbbell": return f'<g transform="translate({x},{y})"><rect x="-44" y="-6" width="88" height="12" rx="5" fill="#555"/><rect x="-54" y="-22" width="18" height="44" rx="5" fill="{PURPLE}"/><rect x="36" y="-22" width="18" height="44" rx="5" fill="{PURPLE}"/></g>'
    if p == "basket": return f'<g transform="translate({x-70},{y-40})"><path d="M0,0 L140,0 L126,80 L14,80 Z" fill="#f3f0f8" stroke="#bdb4cc" stroke-width="4"/><path d="M20,20 H120 M24,40 H116 M28,60 H112" stroke="#cfc8da" stroke-width="5"/><circle cx="40" cy="-6" r="12" fill="#ff8fb1"/><rect x="62" y="-16" width="30" height="20" rx="4" fill="#7fb4ff"/></g>'
    if p == "shake": return f'<g transform="translate({x-18},{y-60})"><rect width="36" height="80" rx="8" fill="{PURPLE}"/><rect x="4" y="-12" width="28" height="16" rx="4" fill="#2b2b33"/><text x="18" y="50" text-anchor="middle" font-family="Anton" font-size="14" fill="#fff">PRO</text></g>'
    if p == "letter": return f'<g transform="translate({x-46},{y-60}) rotate(-8)"><rect width="92" height="116" rx="4" fill="#fbfaf6"/><path d="M12,22 H80 M12,38 H72 M12,54 H80 M12,70 H60" stroke="#c9c3bb" stroke-width="5"/><text x="46" y="102" text-anchor="middle" font-family="Anton" font-size="18" fill="#e23b3b" transform="rotate(-10 46 98)">PAST DUE</text></g>'
    if p == "jeans": return f'<g transform="translate({x-44},{y-70})"><path d="M0,0 H88 L84,150 H52 L44,50 L36,150 H4 Z" fill="#4a72b8"/><path d="M0,0 H88 V14 H0 Z" fill="#3b5d99"/><circle cx="44" cy="7" r="4" fill="#e5c07b"/></g>'
    if p == "plate": return f'<g transform="translate({x},{y})"><circle r="62" fill="#26232c"/><circle r="44" fill="none" stroke="#3a3642" stroke-width="6"/><circle r="10" fill="#9a94a6"/><text y="-22" text-anchor="middle" font-family="Anton" font-size="18" fill="#cfc8da">45</text></g>'
    if p == "mealprep": return f'<g transform="translate({x-60},{y-30})"><rect width="120" height="60" rx="10" fill="#f6f3fb" stroke="#cfc8da" stroke-width="4"/><rect x="8" y="8" width="48" height="44" rx="6" fill="#fff8e7"/><rect x="62" y="8" width="50" height="20" rx="6" fill="#d7a26b"/><rect x="62" y="32" width="50" height="20" rx="6" fill="#58b368"/></g>'
    return ""


# ================================================================ kids
KID_STYLES = [
    {"skin": "#8a5a3c", "hair": "#2a1a14", "shirt": "#ff8fb1", "pants": "#4a72b8", "do": "puffs", "h": 1.0},
    {"skin": "#9b6545", "hair": "#1d1310", "shirt": "#7fd1b9", "pants": "#3a3542", "do": "fade", "h": 1.18},
    {"skin": "#a06a48", "hair": "#2a1a14", "shirt": "#ffd166", "pants": "#6d32d4", "do": "braids", "h": 1.32},
    {"skin": "#8f5d40", "hair": "#1d1310", "shirt": "#8fb4ff", "pants": "#3a3542", "do": "curls", "h": .86},
]


def kid(st, mood="happy"):
    s, cx = st, 80
    g = [f'<rect x="52" y="210" width="24" height="92" rx="10" fill="{s["pants"]}"/><rect x="84" y="210" width="24" height="92" rx="10" fill="{s["pants"]}"/>',
         f'<rect x="46" y="294" width="34" height="14" rx="7" fill="#fff"/><rect x="80" y="294" width="34" height="14" rx="7" fill="#fff"/>',
         f'<path d="M44,120 Q80,104 116,120 L120,220 L40,220 Z" fill="{s["shirt"]}"/>']
    if mood == "cheer":
        g.append(f'<line x1="48" y1="128" x2="22" y2="60" stroke="{s["skin"]}" stroke-width="16" stroke-linecap="round"/><line x1="112" y1="128" x2="138" y2="60" stroke="{s["skin"]}" stroke-width="16" stroke-linecap="round"/>')
    else:
        g.append(f'<line x1="46" y1="128" x2="36" y2="200" stroke="{s["skin"]}" stroke-width="16" stroke-linecap="round"/><line x1="114" y1="128" x2="124" y2="200" stroke="{s["skin"]}" stroke-width="16" stroke-linecap="round"/>')
    g.append(f'<circle cx="{cx}" cy="62" r="44" fill="{s["skin"]}"/>')
    d = s["do"]
    if d == "puffs": g.append(f'<path d="M38,58 Q40,18 80,16 Q120,18 122,58 Q110,34 80,32 Q50,34 38,58Z" fill="{s["hair"]}"/><circle cx="40" cy="22" r="20" fill="{s["hair"]}"/><circle cx="120" cy="22" r="20" fill="{s["hair"]}"/>')
    if d == "fade": g.append(f'<path d="M36,56 Q38,16 80,14 Q122,16 124,56 Q118,30 80,28 Q42,30 36,56Z" fill="{s["hair"]}"/>')
    if d == "braids": g.append(f'<path d="M36,60 Q38,16 80,14 Q122,16 124,60 Q112,32 80,30 Q48,32 36,60Z" fill="{s["hair"]}"/><path d="M38,60 L30,150 M122,60 L130,150" stroke="{s["hair"]}" stroke-width="12" stroke-linecap="round"/>')
    if d == "curls": g.append("".join(f'<circle cx="{40+i*16}" cy="{26+(i%2)*6}" r="14" fill="{s["hair"]}"/>' for i in range(6)))
    if mood == "sleep":
        g.append('<path d="M58,66 q8,6 16,0 M86,66 q8,6 16,0" stroke="#1b110d" stroke-width="4" fill="none"/><path d="M72,86 q8,4 16,0" stroke="#7a3a3a" stroke-width="4" fill="none"/>')
    else:
        g.append('<circle cx="64" cy="64" r="6" fill="#1b110d"/><circle cx="96" cy="64" r="6" fill="#1b110d"/><circle cx="66" cy="62" r="2" fill="#fff"/><circle cx="98" cy="62" r="2" fill="#fff"/>')
        if mood in ("happy", "cheer"):
            g.append('<path d="M64,82 Q80,100 96,82 Z" fill="#7a2a35"/>')
        else:
            g.append('<path d="M68,88 Q80,82 92,88" stroke="#7a3a3a" stroke-width="4" fill="none"/>')
    return "".join(g)


def kids_row(mood):
    spots = [(40, 1630, 0), (210, 1640, 2), (800, 1640, 1), (950, 1630, 3)]
    out = []
    for x, foot, i in spots:
        st = KID_STYLES[i]; sc = 1.15 * st["h"]
        out.append(f'<g transform="translate({x},{foot - 310*sc}) scale({sc})">{kid(st, mood)}</g>')
    return "".join(out)


def kids_sleeping():
    beds = []
    for bx, idx in ((30, (0, 3)), (690, (1, 2))):
        beds.append(f'<rect x="{bx}" y="1330" width="360" height="160" rx="18" fill="#2f2856"/><rect x="{bx}" y="1300" width="360" height="40" rx="14" fill="#3c3468"/>')
        for k, i in enumerate(idx):
            st = KID_STYLES[i]
            beds.append(f'<g transform="translate({bx + 40 + k*150},1230) scale(.85)"><rect x="10" y="40" width="140" height="60" rx="20" fill="#f1edf8"/>{kid_head(st)}</g>')
        beds.append(f'<path d="M{bx},1350 Q{bx+180},1320 {bx+360},1350 L{bx+360},1470 L{bx},1470 Z" fill="#6d32d4" opacity=".9"/>')
    return "".join(beds)


def kid_head(st):
    return (f'<circle cx="80" cy="62" r="40" fill="{st["skin"]}"/><path d="M42,58 Q44,20 80,18 Q116,20 118,58 Q106,36 80,34 Q54,36 42,58Z" fill="{st["hair"]}"/>'
            '<path d="M60,66 q8,6 16,0 M86,66 q8,6 16,0" stroke="#1b110d" stroke-width="4" fill="none"/>')


# ================================================================ backgrounds
def bg(name):
    if name == "apartment_night":
        return ('<rect width="1080" height="1920" fill="#1b2034"/><rect y="1440" width="1080" height="480" fill="#221e2c"/>'
                '<rect x="620" y="440" width="340" height="420" rx="8" fill="#0d1222" stroke="#2e3550" stroke-width="16"/><line x1="790" y1="440" x2="790" y2="860" stroke="#2e3550" stroke-width="10"/>'
                '<path d="M860,470 l-30,90 h30 l-40,110" stroke="#fff6b0" stroke-width="6" fill="none" opacity=".8"/>'
                '<rect x="40" y="1180" width="460" height="230" rx="40" fill="#3a3352"/><rect x="40" y="1120" width="460" height="110" rx="40" fill="#453c62"/>'
                '<rect x="700" y="1330" width="300" height="20" rx="6" fill="#4a3f3a"/><rect x="720" y="1350" width="14" height="110" fill="#4a3f3a"/><rect x="966" y="1350" width="14" height="110" fill="#4a3f3a"/>'
                '<g transform="translate(760,1270) rotate(-6)"><rect width="110" height="60" fill="#f4f1ea"/><rect x="18" y="-14" width="110" height="60" fill="#ece8df"/><text x="70" y="30" font-family="Anton" font-size="20" fill="#e23b3b" text-anchor="middle">PAST DUE</text></g>'
                '<circle cx="150" cy="1520" r="22" fill="#ff8fb1"/><rect x="900" y="1500" width="50" height="34" rx="6" fill="#ffd166"/>'
                '<path d="M160,700 L120,1040 H200 Z" fill="#3a3352"/><ellipse cx="160" cy="680" rx="70" ry="40" fill="#ffd98a" opacity=".35"/>')
    if name in ("bedroom_night", "bedroom_morning"):
        n = name.endswith("night")
        wall, floor, sky = ("#211b3d", "#2a2448", "#0e0b22") if n else ("#f6dbe9", "#d9b7cf", "#9fd3ff")
        orb = '<circle cx="860" cy="560" r="44" fill="#f3efff"/>' if n else '<circle cx="860" cy="560" r="54" fill="#ffd24a"/>'
        return (f'<rect width="1080" height="1920" fill="{wall}"/><rect y="1440" width="1080" height="480" fill="{floor}"/>'
                f'<rect x="680" y="440" width="320" height="380" rx="10" fill="{sky}" stroke="{"#3b3366" if n else "#fff"}" stroke-width="16"/>{orb}'
                f'<rect x="90" y="520" width="150" height="200" rx="6" fill="{"#3b3366" if n else "#c9a7ff"}"/><text x="165" y="640" text-anchor="middle" font-family="Anton" font-size="44" fill="{"#6d32d4" if n else "#fff"}">YOU</text>'
                f'<rect x="270" y="560" width="110" height="140" rx="6" fill="{"#2f2856" if n else "#ffd1e3"}"/>'
                f'<ellipse cx="540" cy="1700" rx="420" ry="70" fill="{"#332b59" if n else "#e7c8dd"}"/>')
    if name == "bathroom":
        tiles = "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#b8c6d8" stroke-width="3"/>' for y in range(200, 1440, 90))
        tiles += "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1440" stroke="#b8c6d8" stroke-width="3"/>' for x in range(0, 1080, 90))
        return (f'<rect width="1080" height="1920" fill="#d3deeb"/>{tiles}<rect y="1440" width="1080" height="480" fill="#9aa9bd"/>'
                '<rect x="250" y="360" width="580" height="760" rx="30" fill="#e9f2fb" stroke="#8a97ab" stroke-width="18"/><path d="M300,420 L420,420 L300,560 Z" fill="#fff" opacity=".7"/>'
                '<rect x="200" y="1180" width="680" height="60" rx="14" fill="#f4f7fb"/><ellipse cx="540" cy="1196" rx="120" ry="22" fill="#c7d3e2"/>')
    if name == "street_dawn":
        bld = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{1460-y}" fill="#3a2a5c" opacity=".9"/>' for x, y, w in ((0, 900, 180), (170, 760, 160), (330, 980, 140), (700, 820, 170), (860, 700, 220)))
        win = "".join(f'<rect x="{x}" y="{y}" width="22" height="30" fill="#ffd98a" opacity=".8"/>' for x in (30, 90, 210, 270, 740, 800, 900, 980) for y in (960, 1060, 1160))
        return ('<defs><linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4b2a8c"/><stop offset=".45" stop-color="#ff7aa8"/><stop offset=".75" stop-color="#ffb36b"/></linearGradient></defs>'
                f'<rect width="1080" height="1920" fill="url(#dawn)"/><circle cx="540" cy="1250" r="170" fill="#ffd98a"/>{bld}{win}'
                '<rect y="1460" width="1080" height="460" fill="#4b4560"/><rect y="1460" width="1080" height="40" fill="#6b6480"/>'
                '<rect x="940" y="980" width="14" height="500" fill="#2a2240"/><circle cx="947" cy="975" r="22" fill="#fff3c4"/>')
    if name == "kitchen":
        return ('<rect width="1080" height="1920" fill="#f6efe6"/><rect y="1440" width="1080" height="480" fill="#e2d5ef"/>'
                + "".join(f'<rect x="{x}" y="{1440 + (x//120)%2*0}" width="120" height="120" fill="{"#d4c3e8" if (x//120)%2 else "#e9def5"}"/>' for x in range(0, 1080, 120)) +
                '<rect x="40" y="480" width="560" height="260" rx="12" fill="#6d32d4"/><line x1="320" y1="480" x2="320" y2="740" stroke="#5223a8" stroke-width="8"/>'
                '<rect x="40" y="1180" width="740" height="270" fill="#8b57ee"/><rect x="30" y="1160" width="760" height="34" rx="8" fill="#e9e2f2"/>'
                '<rect x="820" y="600" width="220" height="850" rx="16" fill="#cfd5de"/><line x1="820" y1="900" x2="1040" y2="900" stroke="#aab2bf" stroke-width="6"/><rect x="840" y="760" width="12" height="100" rx="6" fill="#8a93a3"/>'
                '<rect x="660" y="360" width="140" height="160" rx="8" fill="#9fd3ff" stroke="#fff" stroke-width="10"/>')
    if name == "office":
        blinds = "".join(f'<line x1="640" y1="{y}" x2="960" y2="{y}" stroke="#d9cbb4" stroke-width="8"/>' for y in range(460, 800, 30))
        return (f'<rect width="1080" height="1920" fill="#efe6d8"/><rect y="1440" width="1080" height="480" fill="#bfae95"/><rect x="640" y="440" width="320" height="360" fill="#bfe3ff"/>{blinds}'
                '<rect x="80" y="560" width="200" height="140" rx="6" fill="#fff" stroke="#c7b79e" stroke-width="10"/><text x="180" y="645" text-anchor="middle" font-family="Anton" font-size="34" fill="#6d32d4">HIRING</text>'
                '<rect x="120" y="1300" width="840" height="40" rx="10" fill="#7a5c45"/><rect x="150" y="1340" width="30" height="200" fill="#6a4f3b"/><rect x="900" y="1340" width="30" height="200" fill="#6a4f3b"/>'
                '<path d="M960,1200 q-30,-120 40,-160 q-20,80 10,160 Z" fill="#58b368"/><rect x="950" y="1200" width="60" height="100" rx="8" fill="#c9b08f"/>')
    if name == "gym":
        racks = "".join(f'<rect x="{x}" y="1240" width="70" height="36" rx="10" fill="{c}"/>' for x, c in ((60, "#6d32d4"), (150, "#2b2b33"), (240, "#6d32d4"), (780, "#2b2b33"), (870, "#6d32d4"), (960, "#2b2b33")))
        return ('<rect width="1080" height="1920" fill="#2a1d4a"/><rect y="400" width="1080" height="700" fill="#3a2a66"/>'
                + "".join(f'<rect x="{x}" y="420" width="250" height="660" fill="#4a3a7a" opacity=".6"/>' for x in (20, 290, 560, 830)) +
                '<text x="540" y="360" text-anchor="middle" font-family="Anton" font-size="90" fill="#6d32d4" opacity=".5" letter-spacing="10">GET FIT WITH ME</text>'
                '<rect x="40" y="1230" width="320" height="16" fill="#555"/><rect x="760" y="1230" width="300" height="16" fill="#555"/>' + racks +
                '<rect y="1440" width="1080" height="480" fill="#1c1a22"/>' + "".join(f'<circle cx="{(i*137)%1080}" cy="{1460+(i*71)%440}" r="3" fill="#3a3642"/>' for i in range(60)))
    return '<rect width="1080" height="1920" fill="#222"/>'


def mood_layer(ep, scene):
    out = ""
    if scene.get("rain"):
        drops = "".join(f'<line x1="{(i*53)%1100}" y1="{(i*97)%1920}" x2="{(i*53)%1100-18}" y2="{(i*97)%1920+60}" stroke="#a9c4ff" stroke-width="3" opacity=".35"/>' for i in range(170))
        out += f'<rect width="1080" height="1920" fill="#0b1030" opacity=".35"/>{drops}'
    dark = {1: .38, 2: .28, 3: .12, 4: .06, 5: .1}.get(ep["n"], 0)
    if scene.get("face") in ("crying", "sad"): dark = max(dark, .22)
    if dark:
        out += f'<rect width="1080" height="1920" fill="url(#vig)" opacity="{dark*2:.2f}"/>'
    if ep["n"] >= 9:
        out += "".join(f'<path d="M{x},{y} l6,16 l16,6 l-16,6 l-6,16 l-6,-16 l-16,-6 l16,-6 Z" fill="#ffe27a" opacity=".85"/>' for x, y in ((120, 520), (960, 600), (200, 1000), (900, 1120), (80, 1300), (1000, 880)))
    return out


DEFS = ('<defs><radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#05040c" stop-opacity="1"/></radialGradient></defs>')


def hud(ep, label=None):
    pct = ep["pct"]
    s = (f'<g font-family="Anton"><rect x="50" y="110" width="250" height="124" rx="18" fill="#0f0b1d" opacity=".82"/>'
         f'<text x="175" y="150" text-anchor="middle" font-size="26" fill="#cfc4ff" letter-spacing="3">DAY</text>'
         f'<text x="175" y="214" text-anchor="middle" font-size="64" fill="#ffd84d">{ep["day"]}<tspan font-size="30" fill="#cfc4ff">/30</tspan></text>'
         f'<rect x="320" y="110" width="710" height="124" rx="18" fill="#0f0b1d" opacity=".82"/>'
         f'<text x="675" y="150" text-anchor="middle" font-size="26" fill="#cfc4ff" letter-spacing="3">GLOW-UP</text>'
         f'<rect x="350" y="168" width="650" height="46" rx="23" fill="#2a2240"/><rect x="350" y="168" width="{max(46, 650*pct/100):.0f}" height="46" rx="23" fill="url(#bar)"/>'
         f'<text x="675" y="206" text-anchor="middle" font-size="38" fill="#fff">{pct}%</text></g>'
         '<defs><linearGradient id="bar"><stop offset="0" stop-color="#8b57ee"/><stop offset="1" stop-color="#ff7ac8"/></linearGradient></defs>'
         f'<text x="1010" y="290" text-anchor="end" font-family="Inter" font-weight="700" font-size="24" fill="#fff" opacity=".75">{e(SERIES["handle"])}</text>')
    if label:
        s += (f'<g><rect x="50" y="262" width="{60 + len(label)*24}" height="70" rx="16" fill="#ffd84d"/>'
              f'<text x="80" y="315" font-family="Anton" font-size="44" fill="#1a0d33">{e(label)}</text></g>')
    return s


def place(ep, sc, scale=1.25, x=540, foot=1610):
    phones = sc["bg"] == "gym" and ep["outfit"] != "hoodie"
    g = danielle(ep["body"], ep["outfit"], sc["pose"], sc["face"], sc.get("prop"), phones)
    return f'<g transform="translate({x - 210*scale},{foot - 830*scale}) scale({scale})">{g}</g>'


def frame(ep, sc, label=None):
    kids = ""
    if sc.get("kids"):
        if sc["bg"] == "bedroom_night" and sc["face"] in ("crying", "sad"): kids = kids_sleeping()
        else: kids = kids_row("cheer" if ep["n"] >= 9 or sc["face"] == "happy" else ("happy" if ep["pct"] >= 30 else "neutral"))
    back = kids if sc["bg"] == "bedroom_night" and "Z\"" in kids and sc["face"] in ("crying", "sad") else ""
    front = "" if back else kids
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{DEFS}{bg(sc["bg"])}{back}'
            f'{place(ep, sc)}{front}{mood_layer(ep, sc)}{hud(ep, label)}</svg>')


def phone_frame(ep, ov, label=None):
    msgs = "".join(f'<g transform="translate(300,{760 + i*170})"><rect width="480" height="{130 if len(m) > 34 else 96}" rx="28" fill="#2c2838"/>'
                   f'<foreignObject x="24" y="18" width="440" height="110"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 30px Inter;color:#fff;line-height:1.25">{e(m)}</div></foreignObject></g>' for i, m in enumerate(ov["msgs"]))
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{DEFS}'
            '<defs><radialGradient id="pg" cx=".5" cy=".45" r=".7"><stop offset="0" stop-color="#3b1f7a"/><stop offset="1" stop-color="#0c0818"/></radialGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#pg)"/>'
            '<rect x="250" y="480" width="580" height="1100" rx="70" fill="#0e0c14" stroke="#4a3f66" stroke-width="10"/><rect x="276" y="506" width="528" height="1048" rx="52" fill="#16131f"/>'
            f'<circle cx="340" cy="640" r="34" fill="#6d32d4"/><text x="340" y="652" text-anchor="middle" font-family="Anton" font-size="30" fill="#fff">{e(ov["from"][0])}</text>'
            f'<text x="392" y="652" font-family="Inter" font-weight="800" font-size="32" fill="#fff">{e(ov["from"])}</text>{msgs}'
            f'{mood_layer(ep, {})}{hud(ep, label)}</svg>')


def end_card(ep):
    c = ep["choice"]
    halves = []
    for k, (x0, col, glow) in (("a", (0, "#ffd84d", "#4a1aa6")), ("b", (540, "#7fe0ff", "#0f3a4a"))):
        o = c[k]
        sc = {"bg": "gym", "pose": o["pose"], "face": o["face"], "prop": o.get("prop")}
        fs = 120 if len(o["word"]) <= 6 else (92 if len(o["word"]) <= 9 else 70)
        halves.append(f'<rect x="{x0}" y="0" width="540" height="1920" fill="{glow}"/>'
                      f'<text x="{x0+270}" y="640" text-anchor="middle" font-family="Anton" font-size="{fs}" fill="{col}">{e(o["word"])}</text>'
                      f'<foreignObject x="{x0+40}" y="670" width="460" height="120"><div xmlns="http://www.w3.org/1999/xhtml" style="font:700 30px Inter;color:#fff;text-align:center;line-height:1.25">{e(o["sub"])}</div></foreignObject>'
                      f'{place(ep, sc, scale=.92, x=x0+270, foot=1640)}')
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{DEFS}{"".join(halves)}'
            '<rect x="535" y="380" width="10" height="1300" fill="#ffd84d" opacity=".8"/>'
            f'<text x="540" y="430" text-anchor="middle" font-family="Anton" font-size="64" fill="#ffd84d" letter-spacing="4">COMMENT ONE WORD</text>'
            f'<text x="540" y="1790" text-anchor="middle" font-family="Anton" font-size="58" fill="#fff">{e(c["q"])}</text>{hud(ep)}</svg>')


# ================================================================ render pipeline
def plan():
    """Returns [(episode, [(filename, svg, voiceover)])]."""
    out = []
    for i, ep in enumerate(EPISODES):
        frames = []
        prev = EPISODES[i - 1] if i else None
        sc0 = ep["scenes"]
        for j, sc in enumerate(sc0):
            label = ep["hook"] if j == 0 else None
            if "overlay" in sc:
                frames.append((f"{j+1:02d}-scene.png", phone_frame(ep, sc, label), sc["vo"]))
            else:
                frames.append((f"{j+1:02d}-scene.png", frame(ep, sc, label), sc["vo"]))
        frames.append(("90-choice.png", end_card(ep), ep["vo_choice"]))
        for k, sc in ep["outcomes"].items():
            frames.append((f"next-episode-opener-{ep['choice'][k]['word'].replace(' ', '-')}.png", frame(ep, sc), sc["vo"]))
        out.append((ep, frames))
    return out


def render(P, tmp):
    pages = []
    for ep, frames in P:
        d = os.path.join(OUT, f"ep{ep['n']:02d}")
        os.makedirs(d, exist_ok=True)
        for fn, svg, _ in frames:
            pages.append((os.path.join(d, fn), svg))
    js = os.path.join(tmp, "render.js")
    open(js, "w").write("""
const { chromium } = require('playwright'); const fs = require('fs');
(async()=>{ const jobs = JSON.parse(fs.readFileSync(process.argv[2]));
 const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1920}});
 const head = '<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@600;700;800&display=swap" rel="stylesheet"><style>body{margin:0}svg{display:block}</style></head><body>';
 await p.setContent(head + '<div style="font-family:Anton">x</div><div style="font-family:Inter">x</div></body></html>', {waitUntil:'networkidle'});
 for (const [path, svg] of jobs) { await p.setContent(head + svg + '</body></html>', {waitUntil:'load'}); await p.evaluate(()=>document.fonts.ready); await p.screenshot({path, clip:{x:0,y:0,width:1080,height:1920}}); }
 await b.close(); })();""")
    jf = os.path.join(tmp, "jobs.json"); json.dump(pages, open(jf, "w"))
    subprocess.run(["node", js, jf], check=True)
    print("rendered", len(pages), "frames")


def rough_cuts(P, tmp):
    for ep, frames in P:
        d = os.path.join(OUT, f"ep{ep['n']:02d}")
        lst = os.path.join(tmp, f"ep{ep['n']}.txt")
        main = [f for f in frames if not f[0].startswith("next-")]
        with open(lst, "w") as fh:
            for fn, _, vo in main:
                fh.write(f"file '{os.path.join(d, fn)}'\nduration {max(3.0, len(vo.split()) / 2.6 + .6):.2f}\n")
            fh.write(f"file '{os.path.join(d, main[-1][0])}'\n")
        out = os.path.join(d, f"Episode-{ep['n']:02d}-rough-cut.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf", "fps=30,format=yuv420p",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-movflags", "+faststart", out], check=True)
    print("rough cuts done")


def script_book(P):
    eps = []
    for ep, frames in P:
        d = f"ep{ep['n']:02d}"
        rows = "".join(f'<div class="sc"><img src="{d}/{fn}" alt=""><div><span class="k">{"Choice" if fn.startswith("90") else ("Next episode opener" if fn.startswith("next") else "Scene " + fn[:2].lstrip("0"))}</span><p>{e(vo)}</p></div></div>' for fn, _, vo in frames)
        c = ep["choice"]
        eps.append(f'''<section id="{d}"><div class="eh"><span class="k">Episode {ep["n"]} · Day {ep["day"]} of 30 · Glow-up {ep["pct"]}%</span><h2>{e(ep["title"])}</h2>
<p class="cap"><b>Post caption:</b> {e(ep["caption"])}</p>
<p><b>The choice:</b> {e(c["a"]["word"])} ({e(c["a"]["sub"])}) or {e(c["b"]["word"])} ({e(c["b"]["sub"])})</p>
<a class="btn" href="{d}/Episode-{ep["n"]:02d}-rough-cut.mp4" download>Download rough-cut video</a></div>{rows}</section>''')
    toc = "".join(f'<a href="#ep{ep["n"]:02d}"><b>{ep["n"]}</b> Day {ep["day"]} · {e(ep["title"])}</a>' for ep, _ in P)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>{e(SERIES["title"])} · Script Book</title>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#f7f4fb;color:#17121f;font:400 16px/1.55 Inter,sans-serif}}.w{{max-width:760px;margin:0 auto;padding:28px 16px 80px}}
h1{{font:400 46px/1 Anton;margin:6px 0;color:#4a1aa6}}h2{{font:400 34px/1.1 Anton;margin:4px 0 8px}}.k{{font:700 12px Inter;letter-spacing:.12em;text-transform:uppercase;color:#6b2fd6}}
.box{{background:#fff;border:1px solid #e4dcee;border-radius:16px;padding:18px;margin:16px 0}}.toc a{{display:block;padding:10px 0;border-top:1px solid #eee;color:#17121f;text-decoration:none}}.toc b{{display:inline-block;width:28px;color:#6b2fd6}}
section{{background:#fff;border:1px solid #e4dcee;border-radius:18px;padding:18px;margin:22px 0}}.cap{{background:#efe6ff;border-radius:12px;padding:10px 12px}}
.sc{{display:grid;grid-template-columns:120px 1fr;gap:14px;align-items:start;border-top:1px solid #eee;padding:14px 0}}.sc img{{width:120px;border-radius:12px;display:block}}.sc p{{margin:4px 0 0;font-size:17px}}
.btn{{display:inline-block;background:#6b2fd6;color:#fff;text-decoration:none;font-weight:700;padding:11px 16px;border-radius:12px;margin:6px 0 4px}}ol li{{margin:6px 0}}</style></head><body><div class="w">
<span class="k">Get Fit With Me · TikTok / Reels series</span><h1>{e(SERIES["title"])}</h1><p><i>{e(SERIES["tagline"])}</i></p>
<div class="box"><b>The premise.</b> {e(SERIES["premise"])}</div>
<div class="box"><b>How to post each episode</b><ol>
<li>Open the episode's <b>rough-cut video</b> (or import the frames) in CapCut. Scene frames are timed to the voiceover length.</li>
<li>Record the <b>voiceover</b> by reading each scene's script below. Dramatic, slow, emotional. Let it breathe.</li>
<li>Turn on <b>Auto Captions</b> (big bold style), add a dramatic sound under the voice, and post with the caption.</li>
<li>After 24–48 hours, count the comments. The winning word decides the next episode: <b>start the next episode with that choice's "next episode opener" frame and script.</b></li>
<li>Pin a comment: "Most comments wins. Episode 2 drops tomorrow 💜"</li></ol></div>
<div class="box toc"><b>Episodes</b>{toc}</div>{"".join(eps)}</div></body></html>"""


def main():
    tmp = tempfile.mkdtemp()
    os.makedirs(OUT, exist_ok=True)
    P = plan()
    render(P, tmp)
    rough_cuts(P, tmp)
    open(os.path.join(OUT, "index.html"), "w").write(script_book(P))
    zp = os.path.join(os.path.dirname(OUT), "download", "30-Days-To-Her-Series.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(OUT, "index.html"), "30 Days to Her/SCRIPT BOOK (open me).html")
        for ep, frames in P:
            d = f"ep{ep['n']:02d}"
            for fn, _, _ in frames: z.write(os.path.join(OUT, d, fn), f"30 Days to Her/{d}/{fn}")
            z.write(os.path.join(OUT, d, f"Episode-{ep['n']:02d}-rough-cut.mp4"), f"30 Days to Her/{d}/Episode-{ep['n']:02d}-rough-cut.mp4")
    print("zip:", os.path.getsize(zp) // 1024, "KB")


if __name__ == "__main__":
    if "--preview" in sys.argv:  # render a few frames only
        tmp = tempfile.mkdtemp(); P = plan()
        pick = [(P[0][0], P[0][1][:1] + P[0][1][3:4]), (P[4][0], P[4][1][:1]), (P[9][0], P[9][1][:1]), (P[0][0], [f for f in P[0][1] if f[0].startswith("90")])]
        render(pick, tmp)
    else:
        main()
