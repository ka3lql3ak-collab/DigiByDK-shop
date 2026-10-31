"""Cartoon Danielle + her four kids — detailed, shaded, outlined SVG.
danielle(b, outfit, pose, face, prop, phones) -> SVG markup in a 460x940 box (feet at y≈900).
b: 1.0 = Day 1, 0.0 = Day 30.  Include DEFS once in every <svg> that uses these characters."""
import math

OL = "#2a161c"
SW = 4.5
SKIN, SKIN_D, SKIN_L, SKIN_DD = "#c48466", "#a2644b", "#e2a487", "#7e4a37"
HAIR_DULL = ("#6b2a33", "#4a1820", "#86404a")
HAIR_VIVID = ("#9b1c32", "#62101f", "#d8475f")
PURPLE, PURPLE_D, PURPLE_L = "#6d32d4", "#4a1f9e", "#9e6cf5"

lerp = lambda a, b, t: a + (b - a) * t


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(lerp(x, y, t)) for x, y in zip(a, b))


DEFS = f"""<defs>
<linearGradient id="skinG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{SKIN_L}"/><stop offset=".42" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_D}"/></linearGradient>
<radialGradient id="faceG" cx=".38" cy=".38" r=".75"><stop offset="0" stop-color="{SKIN_L}"/><stop offset=".55" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_D}"/></radialGradient>
<linearGradient id="legG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PURPLE_L}"/><stop offset=".35" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PURPLE_D}"/></linearGradient>
<linearGradient id="blackG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3444"/><stop offset=".5" stop-color="#1c1922"/><stop offset="1" stop-color="#0e0c12"/></linearGradient>
<linearGradient id="hoodG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#aaa2c0"/><stop offset=".4" stop-color="#8f87a6"/><stop offset="1" stop-color="#686182"/></linearGradient>
<linearGradient id="sweatG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a7490"/><stop offset=".4" stop-color="#5f5a70"/><stop offset="1" stop-color="#47435a"/></linearGradient>
<linearGradient id="teeG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b9a0ec"/><stop offset=".4" stop-color="#9b7fd4"/><stop offset="1" stop-color="#7a5cb8"/></linearGradient>
<linearGradient id="darkLegG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#46414f"/><stop offset=".4" stop-color="#26232d"/><stop offset="1" stop-color="#16141b"/></linearGradient>
<linearGradient id="goldG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2bf"/><stop offset=".5" stop-color="#e2b04a"/><stop offset="1" stop-color="#9c6f1c"/></linearGradient>
<linearGradient id="lipG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d98a97"/><stop offset="1" stop-color="#a5485d"/></linearGradient>
<radialGradient id="irisG" cx=".5" cy=".7" r=".7"><stop offset="0" stop-color="#b07a48"/><stop offset=".6" stop-color="#6a3f22"/><stop offset="1" stop-color="#2e170c"/></radialGradient>
<radialGradient id="groundG" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<linearGradient id="shoeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dcd5e8"/></linearGradient>
<linearGradient id="slipperG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc2d8"/><stop offset="1" stop-color="#ef8fb4"/></linearGradient>
{"".join(f'<linearGradient id="hair{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c[2]}"/><stop offset=".35" stop-color="{c[0]}"/><stop offset="1" stop-color="{c[1]}"/></linearGradient>' for k, c in (("D", HAIR_DULL), ("V", HAIR_VIVID)))}
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""


def P(d, fill, sw=SW, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{OL}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def limb(p1, p2, w1, w2, fill, shade=True):
    """Tapered limb segment: outline pass + gradient fill + shading line."""
    (x1, y1), (x2, y2) = p1, p2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    pts = [(x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x2 + nx * w2 / 2, y2 + ny * w2 / 2), (x2 - nx * w2 / 2, y2 - ny * w2 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2)]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out = (f'<polygon points="{poly}" fill="none" stroke="{OL}" stroke-width="{2*SW}" stroke-linejoin="round"/>'
           f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="{w1/2+SW:.1f}" fill="{OL}"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="{w2/2+SW:.1f}" fill="{OL}"/>')
    fill_ = (f'<polygon points="{poly}" fill="{fill}"/><circle cx="{x1:.1f}" cy="{y1:.1f}" r="{w1/2:.1f}" fill="{fill}"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="{w2/2:.1f}" fill="{fill}"/>')
    if shade:
        s = 1 if nx >= 0 else -1  # shade the side facing right (light comes from the left)
        fill_ += (f'<line x1="{x1 + s*nx*w1*.28:.1f}" y1="{y1 + s*ny*w1*.28:.1f}" x2="{x2 + s*nx*w2*.28:.1f}" y2="{y2 + s*ny*w2*.28:.1f}" stroke="#000" stroke-opacity=".12" stroke-width="{min(w1,w2)*.35:.1f}" stroke-linecap="round"/>'
                  f'<line x1="{x1 - s*nx*w1*.28:.1f}" y1="{y1 - s*ny*w1*.28:.1f}" x2="{x2 - s*nx*w2*.28:.1f}" y2="{y2 - s*ny*w2*.28:.1f}" stroke="#fff" stroke-opacity=".16" stroke-width="{min(w1,w2)*.18:.1f}" stroke-linecap="round"/>')
    return out, fill_


POSES = {  # (elbow, hand) offsets from the viewer-LEFT shoulder; right arm mirrors
    "idle":  {"L": ((-28, 96), (-22, 186)), "R": ((-28, 96), (-22, 186))},
    "slump": {"L": ((-16, 100), (46, 176)), "R": ((-16, 100), (46, 176))},
    "hip":   {"L": ((-74, 82), ("waist", 166)), "R": ((-74, 82), ("waist", 166))},
    "flex":  {"L": ((-98, 2), (-88, -94)), "R": ((-98, 2), (-88, -94))},
    "hold":  {"L": ((-28, 96), (-22, 186)), "R": ((-36, 100), (34, 74))},
    "phone": {"L": ((-28, 96), (-22, 186)), "R": ((-42, 88), (36, -62))},
    "curl":  {"L": ((-74, 82), ("waist", 166)), "R": ((-24, 104), (-32, 18))},
    "point": {"L": ((-74, 82), ("waist", 166)), "R": ((-70, -32), (-94, -134))},
    "cheer": {"L": ((-78, -44), (-62, -146)), "R": ((-78, -44), (-62, -146))},
    "face":  {"L": ((-20, 96), (52, -6)), "R": ((-20, 96), (52, -6))},   # hands covering face
}


def pose_offsets(name, b=0.0):
    """Numeric (elbow, hand) offsets for a named pose so poses can be interpolated."""
    sh, wa = lerp(96, 112, b), lerp(48, 114, b)
    belly = lerp(0, 34, max(0, (b - .35) / .65))
    sl = sh - 12
    out = {}
    for k in ("L", "R"):
        (e, h) = POSES[name][k]
        hx = (sl - (wa + belly * .6 + 12)) if h[0] == "waist" else h[0]
        out[k] = ((e[0], e[1]), (hx, h[1]))
    return out


def lerp_pose(p1, p2, t):
    t = max(0, min(1, t)); t = t * t * (3 - 2 * t)
    return {k: tuple(tuple(lerp(a, b_, t) for a, b_ in zip(pa, pb)) for pa, pb in zip(p1[k], p2[k])) for k in ("L", "R")}


def danielle(b=0.0, outfit="bra", pose="idle", face="happy", prop=None, phones=False, blink=False, talk=0.0, head_drop=None, prop_rot=0):
    cx = 230
    glam = 1 - b                     # makeup / jewelry / shine grow over the 30 days
    pose_d = pose if isinstance(pose, dict) else pose_offsets(pose, b)
    hy = 176 + (head_drop if head_drop is not None else (16 if pose in ("slump", "face") else 0))
    hrx, hry = lerp(88, 96, b), lerp(96, 98, b)
    sh, ch, wa, hp, th = lerp(96, 112, b), lerp(84, 110, b), lerp(48, 114, b), lerp(94, 118, b), lerp(72, 92, b)
    up, fo = lerp(44, 58, b), lerp(34, 47, b)
    belly = lerp(0, 34, max(0, (b - .35) / .65))
    hk = "D" if b > .5 else "V"
    hair, hair_d, hair_l = HAIR_DULL if b > .5 else HAIR_VIVID
    top, top_d = {"hoodie": ("url(#hoodG)", "#6f6888"), "tee": ("url(#teeG)", "#7a5cb8"), "tank": ("url(#blackG)", "#0e0c12"), "bra": ("url(#blackG)", "#0e0c12")}[outfit]
    legs_fill = {"hoodie": "url(#sweatG)", "tee": "url(#darkLegG)", "tank": "url(#legG)", "bra": "url(#legG)"}[outfit]
    g = []
    wy, ky, ay = 492, 724, 880
    # ground shadow
    g.append(f'<ellipse cx="{cx}" cy="{ay+30}" rx="{th+70}" ry="22" fill="url(#groundG)"/>')
    # ---------------- long hair behind
    if outfit != "hoodie":
        g.append(P(f"M{cx-hrx-12},{hy-30} C{cx-hrx-46},{hy+100} {cx-hrx-40},{hy+236} {cx-hrx+4},{hy+282} Q{cx},{hy+300} {cx+hrx-4},{hy+282} "
                   f"C{cx+hrx+40},{hy+236} {cx+hrx+46},{hy+100} {cx+hrx+12},{hy-30} Z", f"url(#hair{hk})"))
        g.append("".join(f'<path d="M{cx+s*(hrx+6-k*10)},{hy+40} C{cx+s*(hrx+20-k*8)},{hy+150} {cx+s*(hrx+12-k*12)},{hy+230} {cx+s*(hrx-6-k*14)},{hy+276}" stroke="{hair_d}" stroke-width="3" fill="none" opacity=".7"/>' for s in (-1, 1) for k in range(3)))
    # ---------------- legs
    leg = (f"M{cx-hp+4},{wy-10} C{cx-hp-24},{wy+74} {cx-hp-10},{ky-60} {cx-th},{ky} C{cx-th+6},{ky+70} {cx-th+18},{ay-30} {cx-th+22},{ay} "
           f"L{cx-10},{ay} C{cx-8},{ky+40} {cx-6},{ky-60} {cx-3},{wy+116} L{cx+3},{wy+116} C{cx+6},{ky-60} {cx+8},{ky+40} {cx+10},{ay} "
           f"L{cx+th-22},{ay} C{cx+th-18},{ay-30} {cx+th-6},{ky+70} {cx+th},{ky} C{cx+hp+10},{ky-60} {cx+hp+24},{wy+74} {cx+hp-4},{wy-10} Z")
    g.append(P(leg, legs_fill))
    # seams, knees, folds
    seam = "#3a1888" if outfit in ("tank", "bra") else "#00000055"
    g.append(f'<path d="M{cx-hp+24},{wy+40} C{cx-hp+12},{wy+120} {cx-th+14},{ky-60} {cx-th+20},{ky+40} L{cx-th+28},{ay-20}" stroke="{seam}" stroke-width="2.5" fill="none" stroke-dasharray="7 5"/>')
    g.append(f'<path d="M{cx+hp-24},{wy+40} C{cx+hp-12},{wy+120} {cx+th-14},{ky-60} {cx+th-20},{ky+40} L{cx+th-28},{ay-20}" stroke="{seam}" stroke-width="2.5" fill="none" stroke-dasharray="7 5"/>')
    g.append(f'<path d="M{cx-th+16},{ky+4} q{th/2-10},12 {th-26},0 M{cx+10},{ky+4} q{th/2-10},12 {th-26},0" stroke="#000" stroke-opacity=".18" stroke-width="4" fill="none"/>')
    g.append(f'<path d="M{cx-hp+20},{wy+30} C{cx-hp+4},{wy+120} {cx-th+6},{ky-40} {cx-th+12},{ky+10}" stroke="#fff" stroke-opacity=".22" stroke-width="10" fill="none" stroke-linecap="round"/>')
    if outfit == "hoodie":
        for x0 in (cx - th + 18, cx + 8):
            g.append(P(f"M{x0},{ay-30} h{th-26} v24 h-{th-26} Z", "#524d62"))
            g.append(f'<path d="M{x0+6},{ay-26} v16 M{x0+16},{ay-26} v16 M{x0+26},{ay-26} v16 M{x0+36},{ay-26} v16" stroke="#00000033" stroke-width="2"/>')
        g.append(f'<path d="M{cx-18},{wy+30} q-6,30 -2,60 M{cx+18},{wy+30} q6,30 2,60" stroke="#efeaf5" stroke-width="4" fill="none"/>')
    # footwear
    for x0 in (cx - th + 6, cx + 2):
        w = th - 4
        if outfit == "hoodie":  # fuzzy slippers
            g.append(P(f"M{x0-6},{ay+4} Q{x0+w/2},{ay-22} {x0+w+10},{ay+4} Q{x0+w+16},{ay+32} {x0+w/2},{ay+34} Q{x0-14},{ay+32} {x0-6},{ay+4} Z", "url(#slipperG)"))
            g.append("".join(f'<circle cx="{x0+6+i*w/6:.0f}" cy="{ay-2+(i%2)*4}" r="7" fill="#ffd3e3" opacity=".9"/>' for i in range(6)))
        else:
            g.append(P(f"M{x0},{ay+2} L{x0+w-8},{ay} Q{x0+w+12},{ay+10} {x0+w+6},{ay+32} L{x0-6},{ay+32} Q{x0-10},{ay+12} {x0},{ay+2} Z", "url(#shoeG)"))
            g.append(f'<path d="M{x0-6},{ay+24} L{x0+w+6},{ay+24}" stroke="{PURPLE}" stroke-width="7"/><path d="M{x0+14},{ay+6} l18,0 M{x0+18},{ay+13} l18,0 M{x0+22},{ay+20} l14,0" stroke="#9a92aa" stroke-width="3" stroke-linecap="round"/>'
                     f'<path d="M{x0+w-30},{ay+8} q14,-2 22,10" stroke="{PURPLE}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    # ---------------- torso
    torso = (f"M{cx-sh},304 Q{cx},284 {cx+sh},304 C{cx+ch+10},346 {cx+wa+6+belly},{404} {cx+wa+belly*.6},{462} "
             f"Q{cx+hp-2},{wy-14} {cx+hp-6},{wy} L{cx-hp+6},{wy} Q{cx-hp+2},{wy-14} {cx-wa-belly*.6},462 "
             f"C{cx-wa-6-belly},404 {cx-ch-10},346 {cx-sh},304 Z")
    g.append(P(torso, "url(#skinG)"))
    if outfit == "hoodie":
        hb = 12 + belly
        g.append(P(f"M{cx-sh-12},300 Q{cx},278 {cx+sh+12},300 C{cx+ch+24},356 {cx+wa+hb+6},428 {cx+wa+hb-4},{wy+12} Q{cx},{wy+28} {cx-wa-hb+4},{wy+12} "
                   f"C{cx-wa-hb-6},428 {cx-ch-24},356 {cx-sh-12},300 Z", top))
        g.append(P(f"M{cx-52},288 Q{cx},350 {cx+52},288 Q{cx},312 {cx-52},288 Z", top_d))
        g.append(f'<path d="M{cx-16},314 L{cx-20},380 M{cx+16},314 L{cx+20},372" stroke="#f1ecf7" stroke-width="5" stroke-linecap="round"/><circle cx="{cx-20}" cy="384" r="6" fill="#f1ecf7" stroke="{OL}" stroke-width="2"/><circle cx="{cx+20}" cy="376" r="6" fill="#f1ecf7" stroke="{OL}" stroke-width="2"/>')
        g.append(P(f"M{cx-70},{wy-62} L{cx+70},{wy-62} L{cx+80},{wy-6} L{cx-80},{wy-6} Z", top_d, 3.5))
        g.append(f'<path d="M{cx-wa-hb+8},{wy+4} Q{cx},{wy+22} {cx+wa+hb-8},{wy+4}" stroke="{OL}" stroke-opacity=".35" stroke-width="3" fill="none"/>'
                 f'<path d="M{cx-ch+4},340 q18,34 6,70 M{cx+ch-4},340 q-18,34 -6,70 M{cx-30},420 q10,10 24,6 M{cx+40},440 q-12,8 -22,2" stroke="{OL}" stroke-opacity=".3" stroke-width="3" fill="none"/>')
        g.append(f'<ellipse cx="{cx+44}" cy="410" rx="11" ry="8" fill="#b9a27e" opacity=".55"/><ellipse cx="{cx+58}" cy="402" rx="5" ry="4" fill="#b9a27e" opacity=".5"/>')  # stain
    elif outfit == "tee":
        g.append(P(f"M{cx-sh-12},300 Q{cx},280 {cx+sh+12},300 C{cx+ch+20},354 {cx+wa+18+belly},426 {cx+wa+14+belly*.6},{wy-2} Q{cx},{wy+10} {cx-wa-14-belly*.6},{wy-2} "
                   f"C{cx-wa-18-belly},426 {cx-ch-20},354 {cx-sh-12},300 Z", top))
        g.append(P(f"M{cx-38},292 Q{cx},334 {cx+38},292 Q{cx},310 {cx-38},292 Z", "url(#skinG)", 3.5))
        g.append(f'<text x="{cx}" y="408" text-anchor="middle" font-family="Anton" font-size="40" fill="#f6f1ff" stroke="{OL}" stroke-width="1.5">MOM</text>'
                 f'<path d="M{cx-22},420 l6,-8 6,8 6,-8 6,8 6,-8 6,8" stroke="#ffd84d" stroke-width="3" fill="none"/>'
                 f'<path d="M{cx-ch+8},346 q14,30 4,64 M{cx+ch-8},346 q-14,30 -4,64" stroke="{OL}" stroke-opacity=".3" stroke-width="3" fill="none"/>')
    else:
        low = 398 if outfit == "bra" else wy - 20
        g.append(P(f"M{cx-sh+8},308 Q{cx},286 {cx+sh-8},308 C{cx+ch+8},338 {cx+ch+2},372 {cx+ch-4},{low} Q{cx},{low+14} {cx-ch+4},{low} "
                   f"C{cx-ch-2},372 {cx-ch-8},338 {cx-sh+8},308 Z", top))
        g.append(P(f"M{cx-34},298 L{cx},348 L{cx+34},298 Q{cx},310 {cx-34},298 Z", "url(#skinG)", 3.5))
        g.append(f'<path d="M{cx-ch+14},{low-10} Q{cx},{low+2} {cx+ch-14},{low-10}" stroke="{PURPLE}" stroke-width="8" fill="none"/>'
                 f'<path d="M{cx-ch+14},{low-18} Q{cx},{low-6} {cx+ch-14},{low-18}" stroke="#ffffff" stroke-opacity=".25" stroke-width="2" fill="none" stroke-dasharray="6 5"/>'
                 f'<path d="M{cx-sh+18},312 L{cx-30},300 M{cx+sh-18},312 L{cx+30},300" stroke="{PURPLE}" stroke-width="5"/>'
                 f'<path d="M{cx-ch+20},330 q20,26 30,50" stroke="#fff" stroke-opacity=".18" stroke-width="10" fill="none" stroke-linecap="round"/>')
        g.append(f'<text x="{cx+34}" y="{low-26}" font-family="Anton" font-size="13" fill="{PURPLE_L}" opacity=".9">GFWM</text>')
        if outfit == "bra":
            a = max(0, 1 - b / .5)
            if a:  # abs, obliques, glow
                for yy in (420, 444):
                    g.append(f'<path d="M{cx-26},{yy} q12,7 22,0 M{cx+4},{yy} q12,7 22,0" stroke="{SKIN_DD}" stroke-width="4" fill="none" stroke-linecap="round" opacity="{.75*a:.2f}"/>'
                             f'<path d="M{cx-22},{yy-6} q10,4 16,0" stroke="{SKIN_L}" stroke-width="3" fill="none" opacity="{.7*a:.2f}"/>')
                g.append(f'<path d="M{cx},408 L{cx},466 M{cx-wa+6},412 q10,28 4,52 M{cx+wa-6},412 q-10,28 -4,52" stroke="{SKIN_DD}" stroke-width="4" fill="none" opacity="{.6*a:.2f}"/>')
            g.append(f'<path d="M{cx-44},456 q12,-10 26,-2 q12,8 26,-2 q12,-8 26,2 M{cx-30},464 q20,8 40,0" stroke="#4a2c22" stroke-width="2.6" fill="none" opacity=".8"/>')  # tattoo
            g.append(f'<circle cx="{cx}" cy="472" r="4" fill="{SKIN_DD}"/><circle cx="{cx}" cy="479" r="3.5" fill="#f2ecfb" stroke="{OL}" stroke-width="1"/>')
    if outfit != "hoodie":
        wb = wy - 24 if outfit != "tee" else wy - 6
        band = PURPLE_D if outfit in ("tank", "bra") else "#1b1920"
        g.append(P(f"M{cx-hp+2},{wy-14} Q{cx},{wy-30} {cx+hp-2},{wy-14} L{cx+hp},{wy+12} Q{cx},{wy-4} {cx-hp},{wy+12} Z", band))
        g.append(f'<path d="M{cx-hp+10},{wy-4} Q{cx},{wy-19} {cx+hp-10},{wy-4}" stroke="#fff" stroke-opacity=".3" stroke-width="2" stroke-dasharray="6 5" fill="none"/>')
    # ---------------- neck
    g.append(P(f"M{cx-24},{hy+72} L{cx-26},304 Q{cx},318 {cx+26},304 L{cx+24},{hy+72} Z", "url(#skinG)"))
    g.append(f'<path d="M{cx-24},{hy+80} Q{cx},{hy+100} {cx+24},{hy+80} L{cx+24},{hy+72} L{cx-24},{hy+72} Z" fill="{SKIN_DD}" opacity=".45"/>')
    if glam > .45:  # gold choker
        g.append(f'<path d="M{cx-27},{hy+108} Q{cx},{hy+124} {cx+27},{hy+108}" stroke="{OL}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M{cx-27},{hy+108} Q{cx},{hy+124} {cx+27},{hy+108}" stroke="url(#goldG)" stroke-width="9" fill="none" stroke-linecap="round"/>')
    # ---------------- arms
    sl = sh - 12
    full, upper_sleeve = outfit == "hoodie", outfit == "tee"
    sleeve_solid = {"hoodie": "#8f87a6", "tee": "#9b7fd4"}.get(outfit)
    arm_out, arm_fill, hands, handR = [], [], [], None
    for side, key in ((-1, "L"), (1, "R")):
        (exo, eyo), (hxo, hyo) = pose_d[key]
        sx, sy = cx + side * sl, 318
        ex, ey = sx + (exo if side < 0 else -exo), sy + eyo
        hx = sx + (hxo if side < 0 else -hxo)
        hyy = sy + hyo
        o1, f1 = limb((sx, sy), (ex, ey), up, up * .82, sleeve_solid if (full or upper_sleeve) else SKIN)
        o2, f2 = limb((ex, ey), (hx, hyy), fo, fo * .8, sleeve_solid if full else SKIN)
        arm_out += [o1, o2]; arm_fill += [f1, f2]
        if upper_sleeve:
            arm_fill.append(f'<circle cx="{(sx*.45+ex*.55):.1f}" cy="{(sy*.45+ey*.55):.1f}" r="{up*.55:.1f}" fill="#9b7fd4" stroke="{OL}" stroke-width="3"/>')
        if not (full or upper_sleeve) and b < .65:
            arm_fill.append(f'<path d="M{sx+side*up*.45:.1f},{sy-4} q{side*14},{18} {side*4},{up*.9:.1f}" stroke="{SKIN_DD}" stroke-width="3.5" fill="none" opacity=".6"/>'
                            f'<path d="M{sx-side*4},{sy-up*.3:.1f} q{side*14},-4 {side*22},10" stroke="{SKIN_L}" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>')
            if eyo < 20 and hyo < -40:  # arm raised in a flex: bicep peak
                mx, my = (sx + ex) / 2, (sy + ey) / 2 - up * .22
                arm_fill.append(f'<path d="M{sx+side*6:.1f},{sy-up*.42:.1f} Q{mx:.1f},{my-up*.75:.1f} {ex+side*10:.1f},{ey-up*.4:.1f}" stroke="{OL}" stroke-width="{up*.5+2*SW:.0f}" fill="none" stroke-linecap="round" opacity="0"/>'
                                f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="{lerp(30,20,b):.0f}" ry="{lerp(22,14,b):.0f}" fill="{SKIN}"/>'
                                f'<path d="M{mx-16:.1f},{my-8:.1f} q12,-8 24,2" stroke="{SKIN_L}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                                f'<path d="M{mx-20:.1f},{my+14:.1f} q20,8 40,-2" stroke="{SKIN_DD}" stroke-width="3" fill="none" opacity=".6"/>')
        if full:
            hands.append(f'<circle cx="{hx:.1f}" cy="{hyy:.1f}" r="{fo/2+5:.1f}" fill="#6f6888" stroke="{OL}" stroke-width="{SW}"/>')
        nail = PURPLE if glam > .4 else "#c9a593"
        hands.append(f'<circle cx="{hx:.1f}" cy="{hyy:.1f}" r="{fo/2+1:.1f}" fill="url(#skinG)" stroke="{OL}" stroke-width="{SW}"/>'
                     f'<path d="M{hx-fo*.28:.1f},{hyy+fo*.18:.1f} q{fo*.28:.1f},6 {fo*.56:.1f},0" stroke="{SKIN_DD}" stroke-width="2.5" fill="none" opacity=".6"/>'
                     + "".join(f'<ellipse cx="{hx-fo*.24+i*fo*.16:.1f}" cy="{hyy+fo*.38:.1f}" rx="3" ry="2.4" fill="{nail}"/>' for i in range(4)))
        if side > 0: handR = (hx, hyy)
    behind = pose == "slump" or (isinstance(pose, dict) and pose_d["L"][1][0] > 20 and pose_d["L"][1][1] > 120)
    arms = "".join(arm_out) + "".join(arm_fill) + "".join(hands)
    if behind: g.append(arms)
    # ---------------- head
    hd = []
    head_path = (f"M{cx-hrx},{hy} C{cx-hrx},{hy-hry*1.15} {cx+hrx},{hy-hry*1.15} {cx+hrx},{hy} C{cx+hrx},{hy+hry*.72} {cx+hrx*.42},{hy+hry} {cx},{hy+hry} "
                 f"C{cx-hrx*.42},{hy+hry} {cx-hrx},{hy+hry*.72} {cx-hrx},{hy} Z")
    hd.append(P(head_path, "url(#faceG)"))
    hd.append(f'<path d="M{cx+hrx-14},{hy+10} C{cx+hrx-10},{hy+50} {cx+hrx*.5},{hy+hry-6} {cx+10},{hy+hry-2}" stroke="{SKIN_DD}" stroke-width="7" fill="none" opacity=".22" stroke-linecap="round"/>')
    if b > .55:
        hd.append(f'<path d="M{cx-40},{hy+hry+6} Q{cx},{hy+hry+28} {cx+40},{hy+hry+6}" stroke="{OL}" stroke-width="4" fill="none" opacity=".5"/>')
    # cheekbone highlight
    hd.append(f'<ellipse cx="{cx-52}" cy="{hy+22}" rx="14" ry="6" fill="#fff" opacity="{.18+.25*glam:.2f}" transform="rotate(-18 {cx-52} {hy+22})"/>'
              f'<ellipse cx="{cx+52}" cy="{hy+22}" rx="12" ry="5" fill="#fff" opacity="{.12+.2*glam:.2f}" transform="rotate(18 {cx+52} {hy+22})"/>')
    # hair
    if outfit == "hoodie":
        hd.append(P(f"M{cx-hrx-8},{hy+16} C{cx-hrx-12},{hy-118} {cx+hrx+12},{hy-118} {cx+hrx+8},{hy+16} C{cx+hrx-8},{hy-46} {cx+26},{hy-64} {cx-6},{hy-58} "
                    f"C{cx-44},{hy-52} {cx-hrx+4},{hy-32} {cx-hrx-8},{hy+16} Z", f"url(#hair{hk})"))
        hd.append(P(f"M{cx-44},{hy-100} C{cx-72},{hy-160} {cx+56},{hy-186} {cx+52},{hy-108} C{cx+38},{hy-84} {cx-22},{hy-82} {cx-44},{hy-100} Z", f"url(#hair{hk})"))
        hd.append(f'<path d="M{cx-30},{hy-74} C{cx-10},{hy-92} {cx+20},{hy-90} {cx+46},{hy-70}" stroke="#cfcfd6" stroke-width="7" fill="none" stroke-linecap="round" opacity=".9"/>'
                  f'<path d="M{cx-10},{hy-140} q20,-16 40,-6 M{cx-hrx-6},{hy-6} q-14,46 -2,92" stroke="#d8d8de" stroke-width="4" fill="none" stroke-linecap="round" opacity=".85"/>')
        hd.append("".join(f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round"/>' for d, c, w in (
            (f"M{cx-30},{hy-140} q34,-18 60,4", hair_l, 5), (f"M{cx-20},{hy-118} q28,-10 48,8", hair_d, 4), (f"M{cx-40},{hy-108} q-6,-30 20,-44", hair_d, 3),
            (f"M{cx+44},{hy-156} q36,-24 44,12", hair, 5), (f"M{cx-54},{hy-138} q-30,-16 -34,16", hair, 5), (f"M{cx+30},{hy-170} q8,-26 30,-26", hair, 4),
            (f"M{cx-hrx+2},{hy-6} q-20,54 -4,104", hair, 6), (f"M{cx+hrx-2},{hy-12} q22,50 6,98", hair, 6), (f"M{cx-hrx+10},{hy-40} q30,-30 70,-30", hair_d, 3))))
    else:
        hd.append(P(f"M{cx-hrx-12},{hy+34} C{cx-hrx-18},{hy-126} {cx+hrx+18},{hy-126} {cx+hrx+12},{hy+34} C{cx+hrx-2},{hy-40} {cx+44},{hy-64} {cx+6},{hy-70} "
                    f"C{cx-36},{hy-62} {cx-hrx+6},{hy-30} {cx-hrx-12},{hy+34} Z", f"url(#hair{hk})"))
        for s_ in (-1, 1):
            x1 = cx + s_ * (hrx + 8)
            hd.append(P(f"M{x1},{hy-8} C{x1+s_*26},{hy+86} {x1+s_*18},{hy+182} {x1+s_*6},{hy+226} L{x1-s_*24},{hy+226} C{x1-s_*10},{hy+160} {x1-s_*10},{hy+76} {x1-s_*16},{hy+6} Z", f"url(#hair{hk})"))
            hd.append("".join(f'<path d="M{x1-s_*(2+k*7)},{hy+20+k*8} C{x1+s_*(10-k*4)},{hy+100} {x1+s_*(6-k*5)},{hy+170} {x1-s_*(4+k*6)},{hy+218}" stroke="{c}" stroke-width="{w}" fill="none" opacity=".85"/>'
                              for k, (c, w) in enumerate(((hair_l, 4), (hair_d, 2.5), (hair_l, 2.5)))))
        if b > .3:
            hd.append(f'<path d="M{cx-44},{hy-60} C{cx-20},{hy-84} {cx+10},{hy-86} {cx+30},{hy-74}" stroke="#d8d8de" stroke-width="5" fill="none" stroke-linecap="round" opacity="{min(1,(b-.3)*2):.2f}"/>')
        hd.append(f'<path d="M{cx-30},{hy-70} C{cx+8},{hy-86} {cx+46},{hy-72} {cx+62},{hy-38}" stroke="{hair_l}" stroke-width="{6+5*glam:.0f}" fill="none" stroke-linecap="round" opacity=".9"/>'
                  f'<path d="M{cx-56},{hy-50} C{cx-30},{hy-74} {cx-4},{hy-78} {cx+14},{hy-76}" stroke="#ffd1d8" stroke-width="3" fill="none" stroke-linecap="round" opacity="{.25+.45*glam:.2f}"/>'
                  )
        if not phones and glam > .3:  # gold hoops
            for s_ in (-1, 1):
                ex_ = cx + s_ * (hrx + 4)
                hd.append(f'<circle cx="{ex_}" cy="{hy+86}" r="20" fill="none" stroke="{OL}" stroke-width="9"/><circle cx="{ex_}" cy="{hy+86}" r="20" fill="none" stroke="#e2b04a" stroke-width="5"/><path d="M{ex_-12},{hy+72} q-6,8 -6,16" stroke="#fff6cc" stroke-width="2.5" fill="none"/>')
    if phones:
        band = f"M{cx-hrx-8},{hy+10} C{cx-hrx-12},{hy-134} {cx+hrx+12},{hy-134} {cx+hrx+8},{hy+10}"
        hd.append(f'<path d="{band}" stroke="{OL}" stroke-width="22" fill="none"/><path d="{band}" stroke="#3a3a46" stroke-width="13" fill="none"/><path d="{band}" stroke="#6a6a78" stroke-width="3" fill="none" transform="translate(0,-3)"/>')
        for s_ in (-1, 1):
            hd.append(f'<rect x="{cx + s_*(hrx+8) - 23}" y="{hy-38}" width="46" height="80" rx="18" fill="#3a3a46" stroke="{OL}" stroke-width="{SW}"/>'
                      f'<rect x="{cx + s_*(hrx+8) - 13}" y="{hy-26}" width="26" height="56" rx="10" fill="#26262f"/><circle cx="{cx + s_*(hrx+8)}" cy="{hy+2}" r="5" fill="{PURPLE_L}"/>')
    hd.append(face_svg(face, cx, hy, b, blink, talk))
    out = "".join(g) + "".join(hd) + ("" if behind else arms)
    if prop and handR:
        ps = prop_svg(prop, *handR)
        out += f'<g transform="rotate({prop_rot} {handR[0]:.1f} {handR[1]:.1f})">{ps}</g>' if prop_rot else ps
    return out


def face_svg(face, cx, hy, b=0, blink=False, talk=0.0):
    glam = 1 - b
    ex, ey = 34, hy + 10
    sclera = mix("#ffffff", "#ecd77a", max(0, (b - .3) / .7))  # liver damage tint
    f = [f'<ellipse cx="{cx-54}" cy="{hy+40}" rx="{17+6*b:.0f}" ry="10" fill="#e07a8a" opacity="{.25+.15*glam:.2f}"/><ellipse cx="{cx+54}" cy="{hy+40}" rx="{17+6*b:.0f}" ry="10" fill="#e07a8a" opacity="{.25+.15*glam:.2f}"/>']

    def eye(x, o=1.0, look=0, side=1):
        s = ""
        if blink:
            return f'<path d="M{x-20},{ey} Q{x},{ey+10} {x+20},{ey-2} l{side*8},-5" stroke="#140a0a" stroke-width="5" fill="none" stroke-linecap="round"/>'

        if glam > .25:  # purple eyeshadow
            s += f'<path d="M{x-21},{ey-4} Q{x},{ey-30-6*glam:.0f} {x+21},{ey-6} Q{x},{ey-14} {x-21},{ey-4} Z" fill="#8a4fd0" opacity="{.25+.35*glam:.2f}"/>'
        h = 15 * o
        s += f'<path d="M{x-22},{ey} Q{x},{ey-h*1.4:.1f} {x+22},{ey-2} Q{x},{ey+h*1.05:.1f} {x-22},{ey} Z" fill="{sclera}" stroke="{OL}" stroke-width="2.5"/>'
        if o > .2:
            s += (f'<circle cx="{x+look}" cy="{ey}" r="{11 if o>.6 else 8}" fill="url(#irisG)"/><circle cx="{x+look}" cy="{ey}" r="5.5" fill="#120805"/>'
                  f'<circle cx="{x+look+4}" cy="{ey-4}" r="3.4" fill="#fff"/><circle cx="{x+look-3}" cy="{ey+4}" r="1.6" fill="#fff" opacity=".8"/>')
        if o < .8:
            s += f'<path d="M{x-22},{ey+1} Q{x},{ey-h*1.3:.1f} {x+22},{ey-1} Q{x},{ey-30} {x-22},{ey+1} Z" fill="{SKIN}"/>'
        lid_y = ey - h * .62
        wing = 6 + 8 * glam
        s += f'<path d="M{x-21},{ey+1} Q{x},{lid_y-8:.1f} {x+21},{ey-2} l{side*wing:.0f},{-wing*.7:.0f}" stroke="#140a0a" stroke-width="{4+2*glam:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        for k in range(4 if glam > .3 else 2):
            lx = x - 10 + k * 8 + side * 4
            s += f'<path d="M{lx},{lid_y - 2 + abs(k-1.5)*2:.1f} q{side*2},-8 {side*6},-11" stroke="#140a0a" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
        s += f'<path d="M{x-16},{ey+5} Q{x},{ey+h*.8+4:.1f} {x+18},{ey+2}" stroke="#5a3226" stroke-width="1.8" fill="none" opacity=".7"/>'
        return s

    def brow(x, tilt=0, lift=0, side=1):
        y = ey - 34 - lift
        return P(f"M{x-side*22},{y+6+tilt} Q{x-side*4},{y-10} {x+side*20},{y-tilt+2} Q{x+side*4},{y-2} {x-side*22},{y+6+tilt} Z", "#2a1510", 1.5)

    def lips(curve=4, up=0, open_=False):
        my = hy + 54
        if open_:
            return (f'<path d="M{cx-30},{my-6} Q{cx},{my+36} {cx+30},{my-6} Z" fill="#5c1626" stroke="{OL}" stroke-width="3"/>'
                    f'<path d="M{cx-26},{my-4} L{cx+26},{my-4} L{cx+21},{my+7} L{cx-21},{my+7} Z" fill="#fff"/><path d="M{cx-14},{my+22} Q{cx},{my+14} {cx+14},{my+22}" fill="#d16a7c"/>'
                    f'<path d="M{cx-33},{my-6} Q{cx-16},{my-16} {cx-4},{my-12} Q{cx},{my-10} {cx+4},{my-12} Q{cx+16},{my-16} {cx+33},{my-6} Q{cx},{my-2} {cx-33},{my-6} Z" fill="url(#lipG)" stroke="{OL}" stroke-width="2.5"/>'
                    f'<path d="M{cx-28},{my+4} Q{cx},{my+44} {cx+28},{my+4} Q{cx},{my+30} {cx-28},{my+4} Z" fill="url(#lipG)" stroke="{OL}" stroke-width="2.5"/><ellipse cx="{cx-6}" cy="{my+28}" rx="8" ry="3" fill="#fff" opacity=".55"/>')
        return (f'<path d="M{cx-28},{my-up} Q{cx-14},{my-12} {cx-3},{my-7} Q{cx},{my-5} {cx+3},{my-7} Q{cx+14},{my-12} {cx+28},{my+up} Q{cx},{my+2} {cx-28},{my-up} Z" fill="url(#lipG)" stroke="{OL}" stroke-width="2.5"/>'
                f'<path d="M{cx-26},{my-up+1} Q{cx},{my+24+curve} {cx+26},{my+up+1} Q{cx},{my+4} {cx-26},{my-up+1} Z" fill="url(#lipG)" stroke="{OL}" stroke-width="2.5"/>'
                f'<path d="M{cx-26},{my-up+1} Q{cx},{my+5+curve*.3} {cx+26},{my+up+1}" stroke="#6e2232" stroke-width="2.5" fill="none"/>'
                f'<ellipse cx="{cx-5}" cy="{my+12+curve*.4}" rx="{7+3*glam:.0f}" ry="3" fill="#fff" opacity="{.3+.4*glam:.2f}"/>'
                f'<path d="M{cx-10},{my+1} h20 v7 q-5,3 -10,0 q-5,3 -10,0 Z" fill="#fffdf2" stroke="{OL}" stroke-width="1.8"/><path d="M{cx},{my+1} v8" stroke="#d8d2c4" stroke-width="1.5"/>')
    if face == "happy":
        f += [eye(cx - ex, 1, 0, -1), eye(cx + ex, 1, 0, 1), brow(cx - ex, 0, 2, -1), brow(cx + ex, 0, 2, 1), lips(open_=True)]
    elif face == "smirk":
        f += [eye(cx - ex, .78, 2, -1), eye(cx + ex, .78, 2, 1), brow(cx - ex, 0, 0, -1), brow(cx + ex, -5, 8, 1), lips(2, 7)]
    elif face == "determined":
        f += [eye(cx - ex, .7, 0, -1), eye(cx + ex, .7, 0, 1), brow(cx - ex, -8, -2, -1), brow(cx + ex, -8, -2, 1), lips(0)]
    elif face == "shocked":
        f += [eye(cx - ex, 1.25, 0, -1), eye(cx + ex, 1.25, 0, 1), brow(cx - ex, 0, 14, -1), brow(cx + ex, 0, 14, 1)]
        f.append(f'<ellipse cx="{cx}" cy="{hy+62}" rx="17" ry="22" fill="#4e1220" stroke="url(#lipG)" stroke-width="9"/><ellipse cx="{cx}" cy="{hy+62}" rx="22" ry="27" fill="none" stroke="{OL}" stroke-width="2.5"/>')
    elif face == "tired":
        f += [eye(cx - ex, .45, 0, -1), eye(cx + ex, .45, 0, 1), brow(cx - ex, 3, -4, -1), brow(cx + ex, 3, -4, 1), lips(-6)]
        f.append(f'<path d="M{cx-ex-16},{ey+18} q16,10 32,0 M{cx+ex-16},{ey+18} q16,10 32,0" stroke="#6b3a2a" stroke-width="4" fill="none" opacity=".75"/>')
    elif face in ("sad", "crying"):
        if face == "sad":
            f += [eye(cx - ex, .72, -3, -1), eye(cx + ex, .72, -3, 1)]
        else:
            f.append(f'<path d="M{cx-ex-20},{ey} Q{cx-ex},{ey+14} {cx-ex+20},{ey} M{cx+ex-20},{ey} Q{cx+ex},{ey+14} {cx+ex+20},{ey}" stroke="#140a0a" stroke-width="5" fill="none" stroke-linecap="round"/>')
            for s_ in (-1, 1):
                tx = cx + s_ * (ex + 8)
                f.append(f'<path d="M{tx},{ey+10} C{tx+s_*14},{ey+56} {tx+s_*8},{ey+100} {tx+s_*2},{ey+126} C{tx-s_*8},{ey+100} {tx-s_*6},{ey+56} {tx},{ey+10} Z" fill="#9fdcff" stroke="#4aa3d8" stroke-width="2" opacity=".92"/>'
                         f'<path d="M{tx+s_*2},{ey+40} q{s_*4},24 0,48" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/><circle cx="{tx+s_*4}" cy="{ey+140}" r="6" fill="#9fdcff" stroke="#4aa3d8" stroke-width="1.5"/>')
        for s_ in (-1, 1):
            bx, by = cx + s_ * ex, ey - 30
            f.append(P(f"M{bx-s_*20},{by-14} Q{bx-s_*2},{by-12} {bx+s_*22},{by+4} Q{bx+s_*2},{by-4} {bx-s_*20},{by-6} Z", "#2a1510", 1.5))
        my = hy + 60
        f.append(f'<path d="M{cx-24},{my+8} Q{cx},{my-12} {cx+24},{my+8} Q{cx},{my} {cx-24},{my+8} Z" fill="url(#lipG)" stroke="{OL}" stroke-width="2.5"/>')
        f.append(f'<path d="M{cx-ex-16},{ey+20} q16,10 32,0 M{cx+ex-16},{ey+20} q16,10 32,0" stroke="#6b3a2a" stroke-width="4" fill="none" opacity=".7"/>')
    if talk > .05:  # talking mouth replaces the expression's mouth
        my = hy + 58
        f.append(f'<rect x="{cx-40}" y="{hy+38}" width="80" height="50" fill="url(#faceG)"/>')
        f.append(f'<ellipse cx="{cx}" cy="{my}" rx="{16+6*talk:.1f}" ry="{4+14*talk:.1f}" fill="#4e1220" stroke="url(#lipG)" stroke-width="8"/><ellipse cx="{cx}" cy="{my}" rx="{20+6*talk:.1f}" ry="{8+14*talk:.1f}" fill="none" stroke="{OL}" stroke-width="2.5"/>')
    # nose + stud
    f.append(f'<path d="M{cx-2},{hy+4} L{cx-4},{hy+26}" stroke="#fff" stroke-width="4" opacity=".28" stroke-linecap="round"/>'
             f'<path d="M{cx-6},{hy+16} Q{cx-4},{hy+30} {cx-16},{hy+34} Q{cx-2},{hy+44} {cx},{hy+40} Q{cx+2},{hy+44} {cx+16},{hy+34}" stroke="{SKIN_DD}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
             f'<circle cx="{cx+2}" cy="{hy+34}" r="5" fill="#fff" opacity=".25"/>'
             f'<circle cx="{cx+18}" cy="{hy+33}" r="4" fill="#fff" stroke="#9aa" stroke-width="1"/><path d="M{cx+18},{hy+28} v10 M{cx+13},{hy+33} h10" stroke="#fff" stroke-width="1.4" opacity="{.4+.5*glam:.2f}"/>')
    return "".join(f)


def prop_svg(p, x, y):
    S = f'stroke="{OL}" stroke-width="4" stroke-linejoin="round"'
    if p == "phone": return f'<g transform="translate({x-28},{y-62})"><rect width="56" height="104" rx="12" fill="#17141c" {S}/><rect x="6" y="10" width="44" height="82" rx="6" fill="#8fbaff"/><path d="M12,20 h30 M12,32 h22" stroke="#fff" stroke-width="4" opacity=".7"/></g>'
    if p == "dumbbell": return f'<g transform="translate({x},{y})"><rect x="-56" y="-8" width="112" height="16" rx="7" fill="#8a8494" {S}/><rect x="-74" y="-32" width="26" height="64" rx="7" fill="{PURPLE}" {S}/><rect x="48" y="-32" width="26" height="64" rx="7" fill="{PURPLE}" {S}/><rect x="-70" y="-26" width="6" height="52" rx="3" fill="#fff" opacity=".3"/></g>'
    if p == "basket": return f'<g transform="translate({x-84},{y-50})"><circle cx="48" cy="-6" r="15" fill="#ff8fb1" {S}/><rect x="74" y="-20" width="36" height="26" rx="5" fill="#8fbaff" {S}/><path d="M0,0 L168,0 L150,98 L18,98 Z" fill="#f3f0f8" {S}/><path d="M22,26 H146 M26,50 H142 M30,74 H138" stroke="#cfc8da" stroke-width="6"/></g>'
    if p == "shake": return f'<g transform="translate({x-24},{y-74})"><rect x="6" y="-16" width="36" height="22" rx="5" fill="#34343e" {S}/><rect width="48" height="98" rx="11" fill="{PURPLE}" {S}/><rect x="6" y="8" width="8" height="80" rx="4" fill="#fff" opacity=".25"/><text x="24" y="60" text-anchor="middle" font-family="Anton" font-size="17" fill="#fff">PRO</text></g>'
    if p == "letter": return f'<g transform="translate({x-58},{y-76}) rotate(-8)"><rect width="116" height="142" rx="5" fill="#fbfaf6" {S}/><path d="M14,28 H100 M14,48 H90 M14,68 H100 M14,88 H74" stroke="#c9c3bb" stroke-width="6"/><text x="58" y="126" text-anchor="middle" font-family="Anton" font-size="24" fill="#e23b3b" transform="rotate(-10 58 120)">PAST DUE</text></g>'
    if p == "jeans": return f'<g transform="translate({x-54},{y-86})"><path d="M0,0 H108 L102,180 H62 L54,62 L46,180 H6 Z" fill="#4a72b8" {S}/><path d="M0,0 H108 V18 H0 Z" fill="#3b5d99" {S}/><circle cx="54" cy="9" r="5" fill="#e5c07b"/><path d="M20,30 q10,40 6,120 M88,30 q-10,40 -6,120" stroke="#fff" stroke-opacity=".2" stroke-width="6" fill="none"/></g>'
    if p == "plate": return f'<g transform="translate({x},{y})"><circle r="74" fill="#26232c" {S}/><circle r="52" fill="none" stroke="#3a3642" stroke-width="8"/><circle r="13" fill="#9a94a6" {S}/><text y="-28" text-anchor="middle" font-family="Anton" font-size="22" fill="#cfc8da">45 LB</text></g>'
    if p == "wine": return f'<g transform="translate({x-18},{y-120})"><path d="M11,0 H25 V32 Q38,46 38,68 V150 Q38,158 30,158 H6 Q-2,158 -2,150 V68 Q-2,46 11,32 Z" fill="#3d1626" {S}/><rect x="0" y="84" width="36" height="38" fill="#e9dcc3"/><rect x="4" y="40" width="6" height="100" rx="3" fill="#fff" opacity=".18"/></g>'
    if p == "labs": return (f'<g transform="translate({x-60},{y-80}) rotate(-6)"><rect width="124" height="150" rx="4" fill="#fbfdff" {S}/><rect width="124" height="26" fill="#3b82c4"/>'
                            f'<text x="62" y="19" text-anchor="middle" font-family="Anton" font-size="15" fill="#fff">LAB RESULTS</text><path d="M12,40 h70 M12,56 h90 M12,72 h60" stroke="#c9cdd6" stroke-width="5"/>'
                            f'<text x="62" y="104" text-anchor="middle" font-family="Anton" font-size="17" fill="#e23b3b">LIVER: CRITICAL</text><rect x="14" y="114" width="96" height="26" fill="none" stroke="#e23b3b" stroke-width="3"/>'
                            f'<text x="62" y="133" text-anchor="middle" font-family="Anton" font-size="14" fill="#e23b3b">STOP DRINKING</text></g>')
    if p == "glass": return f'<g transform="translate({x},{y+10})"><path d="M-26,-92 h52 q0,58 -26,64 q-26,-6 -26,-64 Z" fill="#ffffff30" {S}/><path d="M-23,-70 h46 q-4,38 -23,42 q-19,-4 -23,-42 Z" fill="#8a1530"/><path d="M0,-28 v40 M-22,12 h44" {S} fill="none"/><path d="M-18,-84 q-2,20 4,34" stroke="#fff" stroke-width="3" opacity=".5" fill="none"/></g>'
    if p == "mealprep": return f'<g transform="translate({x-70},{y-36})"><rect width="140" height="72" rx="12" fill="#f6f3fb" {S}/><rect x="10" y="10" width="56" height="52" rx="6" fill="#fff8e7"/><rect x="72" y="10" width="58" height="24" rx="6" fill="#d7a26b"/><rect x="72" y="38" width="58" height="24" rx="6" fill="#58b368"/></g>'
    return ""


# ================================================================ kids (same detail level as mom)
KIDS = [  # oldest sister, slightly younger sister, little sister, little brother (youngest)
    {"id": "k1", "name": "oldest sister", "girl": True, "age": 3, "skin": "#c88a6b", "skin_d": "#a66a50", "skin_l": "#e4a98a",
     "hair": "#2a1612", "hair_l": "#5a3328", "top": ("#ffd166", "#e3ad3a", "#fff0b8"), "bottom": ("#4a72b8", "#34558f", "#7397d6"),
     "do": "braids", "h": 1.30, "graphic": "heart", "outfit": "sweatshirt"},
    {"id": "k2", "name": "older sister", "girl": True, "age": 2, "skin": "#b97a5b", "skin_d": "#975c44", "skin_l": "#d79a7a",
     "hair": "#2a1612", "hair_l": "#5a3328", "top": ("#5fc7a8", "#3fa587", "#a6ecd8"), "bottom": ("#6d32d4", "#4a1f9e", "#9e6cf5"),
     "do": "ponytail", "h": 1.15, "graphic": "star", "outfit": "tee"},
    {"id": "k3", "name": "little sister", "girl": True, "age": 1, "skin": "#cf9475", "skin_d": "#ad7258", "skin_l": "#ecb497",
     "hair": "#2a1612", "hair_l": "#5a3328", "top": ("#ff8fb1", "#e8739a", "#ffd0df"), "bottom": ("#b48cff", "#8a62e0", "#d6c2ff"),
     "do": "puffs", "h": .98, "graphic": "rainbow", "outfit": "dress"},
    {"id": "k4", "name": "little brother", "girl": False, "age": 0, "skin": "#c48466", "skin_d": "#a2644b", "skin_l": "#e2a487",
     "hair": "#1f140f", "hair_l": "#4a3026", "top": ("#8fbaff", "#6f9ce8", "#cfe0ff"), "bottom": ("#3a3644", "#26232d", "#5a5466"),
     "do": "curls", "h": .80, "graphic": "dino", "outfit": "shorts"},
]


def kid(st, mood="happy", talk=0.0, blink=False, arms=None):
    """Detailed kid in a 200x390 box (feet at ~380)."""
    k, cx = st["id"], 100
    sk, skd, skl = st["skin"], st["skin_d"], st["skin_l"]
    t0, t1, t2 = st["top"]; b0, b1, b2 = st["bottom"]
    S = f'stroke="{OL}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
    g = [f'<defs><linearGradient id="{k}sk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{skl}"/><stop offset=".45" stop-color="{sk}"/><stop offset="1" stop-color="{skd}"/></linearGradient>'
         f'<radialGradient id="{k}fc" cx=".38" cy=".36" r=".75"><stop offset="0" stop-color="{skl}"/><stop offset=".55" stop-color="{sk}"/><stop offset="1" stop-color="{skd}"/></radialGradient>'
         f'<linearGradient id="{k}tp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t2}"/><stop offset=".4" stop-color="{t0}"/><stop offset="1" stop-color="{t1}"/></linearGradient>'
         f'<linearGradient id="{k}bt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{b2}"/><stop offset=".4" stop-color="{b0}"/><stop offset="1" stop-color="{b1}"/></linearGradient>'
         f'<linearGradient id="{k}hr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{st["hair_l"]}"/><stop offset=".4" stop-color="{st["hair"]}"/><stop offset="1" stop-color="#0d0705"/></linearGradient></defs>',
         f'<ellipse cx="{cx}" cy="384" rx="74" ry="11" fill="url(#groundG)"/>']
    # ---- legs
    shorts = st["outfit"] == "shorts"
    for s_ in (-1, 1):
        hx = cx + s_ * 20
        o, f_ = limb((hx, 280), (hx + s_ * 2, 360), 30, 24, sk if shorts else b0, shade=True)
        g += [o, f_]
    if shorts:
        g.append(P(f"M{cx-44},262 L{cx+44},262 L{cx+46},312 L{cx+4},312 L{cx},298 L{cx-4},312 L{cx-46},312 Z", f"url(#{k}bt)"))
        g.append(f'<path d="M{cx-40},300 h32 M{cx+8},300 h32" stroke="#fff" stroke-opacity=".25" stroke-width="2" stroke-dasharray="5 4"/>')
    else:
        g.append(f'<path d="M{cx-26},300 L{cx-25},352 M{cx+14},300 L{cx+15},352" stroke="#fff" stroke-opacity=".2" stroke-width="5" stroke-linecap="round"/>')
    # ---- sneakers
    for x0 in (cx - 42, cx + 4):
        g.append(P(f"M{x0},{360} L{x0+30},{358} Q{x0+46},{364} {x0+42},{380} L{x0-4},{380} Q{x0-6},{366} {x0},{360} Z", "url(#shoeG)", 3.5))
        g.append(f'<path d="M{x0-4},{374} H{x0+42}" stroke="{t1}" stroke-width="5"/><path d="M{x0+8},{364} h12 M{x0+10},{369} h12" stroke="#9a92aa" stroke-width="2.5" stroke-linecap="round"/>')
    # ---- torso / outfit
    if st["outfit"] == "dress":
        g.append(P(f"M{cx-44},176 Q{cx},162 {cx+44},176 L{cx+40},236 Q{cx+70},282 {cx+66},304 Q{cx},318 {cx-66},304 Q{cx-70},282 {cx-40},236 Z", f"url(#{k}tp)"))
        g.append(f'<path d="M{cx-40},236 Q{cx},248 {cx+40},236" stroke="{t1}" stroke-width="7" fill="none"/><path d="M{cx-30},250 q-8,30 -16,50 M{cx},252 v54 M{cx+30},250 q8,30 16,50" stroke="{OL}" stroke-opacity=".25" stroke-width="3" fill="none"/>'
                 f'<path d="M{cx-64},300 Q{cx},314 {cx+64},300" stroke="#fff" stroke-width="4" stroke-dasharray="2 8" stroke-linecap="round" fill="none"/>')
    else:
        low = 272 if st["outfit"] == "sweatshirt" else 268
        g.append(P(f"M{cx-46},176 Q{cx},160 {cx+46},176 L{cx+48},{low} Q{cx},{low+10} {cx-48},{low} Z", f"url(#{k}tp)"))
        if st["outfit"] == "sweatshirt":
            g.append(f'<path d="M{cx-48},{low-12} Q{cx},{low-2} {cx+48},{low-12}" stroke="{t1}" stroke-width="8" fill="none"/>'
                     + "".join(f'<path d="M{cx-44+i*8},{low-14} v12" stroke="{OL}" stroke-opacity=".2" stroke-width="2"/>' for i in range(12)))
        g.append(f'<path d="M{cx-32},196 q-6,30 2,56 M{cx+34},200 q6,26 -2,50" stroke="{OL}" stroke-opacity=".22" stroke-width="3" fill="none"/>')
        if not shorts and st["outfit"] != "dress":
            g.append(P(f"M{cx-46},{low-2} Q{cx},{low+8} {cx+46},{low-2} L{cx+46},{low+12} Q{cx},{low+20} {cx-46},{low+12} Z", b1, 3.5))
    g.append(P(f"M{cx-24},172 Q{cx},196 {cx+24},172 Q{cx},182 {cx-24},172 Z", t1, 3.5))  # collar
    gr = st["graphic"]
    if gr == "heart": g.append(P(f"M{cx},246 C{cx-34},222 {cx-22},196 {cx},212 C{cx+22},196 {cx+34},222 {cx},246 Z", "#ff5f8f", 3) + f'<path d="M{cx-14},212 q4,-6 10,-4" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>')
    if gr == "star": g.append(P(f"M{cx},198 l9,18 20,3 -14,14 3,20 -18,-9 -18,9 3,-20 -14,-14 20,-3 Z", "#ffd84d", 3))
    if gr == "rainbow": g.append(f'<path d="M{cx-26},236 a26,26 0 0 1 52,0" stroke="#ff5f5f" stroke-width="7" fill="none"/><path d="M{cx-19},236 a19,19 0 0 1 38,0" stroke="#ffd84d" stroke-width="7" fill="none"/><path d="M{cx-12},236 a12,12 0 0 1 24,0" stroke="#5fc7a8" stroke-width="7" fill="none"/><circle cx="{cx-28}" cy="238" r="7" fill="#fff"/><circle cx="{cx+28}" cy="238" r="7" fill="#fff"/>')
    if gr == "dino": g.append(P(f"M{cx-34},248 q4,-32 30,-32 q16,-20 34,-6 q-6,8 -16,8 q4,16 -2,30 Z", "#5fc7a8", 3) + f'<circle cx="{cx+22}" cy="214" r="2.6" fill="{OL}"/><path d="M{cx-20},218 l5,-9 5,9 M{cx-6},214 l5,-9 5,9" stroke="{OL}" stroke-width="2.5" fill="#3fa587"/>')
    # ---- arms
    pose = arms or {"cheer": [((-70, -40), (-60, -92))] * 2}.get(mood, [((-12, 50), (-10, 96))] * 2)
    arms = []
    for side, ((eo, eyo), (ho, hyo)) in zip((-1, 1), pose):
        sx, sy = cx + side * 42, 186
        ex, ey = sx + (eo if side < 0 else -eo), sy + eyo
        hx, hy_ = sx + (ho if side < 0 else -ho), sy + hyo
        o1, f1 = limb((sx, sy), (ex, ey), 22, 19, sk)
        o2, f2 = limb((ex, ey), (hx, hy_), 19, 16, sk)
        arms += [o1, o2, f1, f2]
        ang = math.degrees(math.atan2(ey - sy, ex - sx)) - 90
        mx_, my_ = sx + (ex - sx) * .22, sy + (ey - sy) * .22
        sleeve = f'<ellipse cx="{mx_:.1f}" cy="{my_:.1f}" rx="17" ry="21" fill="url(#{k}tp)" stroke="{OL}" stroke-width="3.5" transform="rotate({ang:.1f} {mx_:.1f} {my_:.1f})"/>'
        arms.append(sleeve)
        arms.append(f'<circle cx="{hx:.1f}" cy="{hy_:.1f}" r="11" fill="{sk}" stroke="{OL}" stroke-width="4"/><path d="M{hx-5:.1f},{hy_+4:.1f} q5,3 10,0" stroke="{skd}" stroke-width="2" fill="none"/>')
    g.append("".join(arms))
    # ---- neck + head
    g.append(P(f"M{cx-14},146 L{cx-15},176 Q{cx},184 {cx+15},176 L{cx+14},146 Z", sk, 3.5))
    hd = []
    if st["do"] == "braids":
        for s_ in (-1, 1):
            bx = cx + s_ * 56
            hd.append(f'<path d="M{bx},70 C{bx+s_*8},150 {bx+s_*2},230 {bx-s_*4},290" stroke="{OL}" stroke-width="24" fill="none" stroke-linecap="round"/><path d="M{bx},70 C{bx+s_*8},150 {bx+s_*2},230 {bx-s_*4},290" stroke="url(#{k}hr)" stroke-width="16" fill="none" stroke-linecap="round"/>')
            hd.append("".join(f'<path d="M{bx+s_*(6-i*.2)-8:.1f},{96+i*16} q8,6 16,0" stroke="{st["hair_l"]}" stroke-width="2.5" fill="none"/>' for i in range(11)))
            hd.append(f'<rect x="{bx-s_*4-10}" y="250" width="20" height="10" rx="3" fill="url(#goldG)" stroke="{OL}" stroke-width="2"/><rect x="{bx-s_*2-10}" y="180" width="20" height="8" rx="3" fill="url(#goldG)" stroke="{OL}" stroke-width="2"/>')
    if st["do"] == "ponytail":
        hd.append(P(f"M{cx+40},24 C{cx+104},20 {cx+108},120 {cx+82},196 C{cx+80},140 {cx+70},86 {cx+34},60 Z", f"url(#{k}hr)"))
        hd.append(f'<path d="M{cx+56},44 C{cx+84},76 {cx+90},120 {cx+82},170 M{cx+70},40 C{cx+96},80 {cx+96},120 {cx+90},150" stroke="{st["hair_l"]}" stroke-width="3" fill="none"/>')
    hd.append(P(f"M{cx-62},92 C{cx-62},10 {cx+62},10 {cx+62},92 C{cx+62},138 {cx+30},156 {cx},156 C{cx-30},156 {cx-62},138 {cx-62},92 Z", f"url(#{k}fc)"))
    hd.append(f'<path d="M{cx+54},100 C{cx+52},134 {cx+28},150 {cx+6},152" stroke="{skd}" stroke-width="7" fill="none" opacity=".35" stroke-linecap="round"/>')
    d = st["do"]
    cap = f"M{cx-64},88 C{cx-66},6 {cx+66},6 {cx+64},88 C{cx+56},44 {cx+20},36 {cx},40 C{cx-24},38 {cx-56},48 {cx-64},88 Z"
    if d == "puffs":
        for s_ in (-1, 1):
            px = cx + s_ * 62
            hd.append(P(f"M{px-30},34 a30,30 0 1 1 60,0 a30,30 0 1 1 -60,0 Z", f"url(#{k}hr)") + "".join(f'<circle cx="{px-14+i*9}" cy="{22+(i%2)*14}" r="5" fill="{st["hair_l"]}" opacity=".7"/>' for i in range(4)))
            hd.append(P(f"M{px-16},58 l-14,-10 0,20 Z M{px+16},58 l14,-10 0,20 Z", "#ff6f9f", 2.5) + f'<circle cx="{px}" cy="58" r="6" fill="#ff8fb1" stroke="{OL}" stroke-width="2.5"/>')
        hd.append(P(cap, f"url(#{k}hr)"))
    elif d == "curls":
        hd.append(P(f"M{cx-60},84 C{cx-62},20 {cx+62},20 {cx+60},84 C{cx+52},52 {cx+30},44 {cx},46 C{cx-30},44 {cx-52},52 {cx-60},84 Z", "#3a2a24"))
        hd.append("".join(P(f"M{cx-48+i*16},{30+(i%2)*6} a12,12 0 1 1 0.1,0 Z", f"url(#{k}hr)", 3) for i in range(7)))
        hd.append("".join(f'<path d="M{cx-44+i*16},{24+(i%2)*6} q4,-4 8,0" stroke="{st["hair_l"]}" stroke-width="2" fill="none"/>' for i in range(7)))
    else:
        hd.append(P(cap, f"url(#{k}hr)"))
        hd.append(f'<path d="M{cx-34},44 C{cx-6},30 {cx+24},32 {cx+44},46" stroke="{st["hair_l"]}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".9"/><path d="M{cx},28 L{cx+2},42" stroke="#120a08" stroke-width="2.5"/>')
        if d == "ponytail":
            hd.append(f'<circle cx="{cx+46}" cy="34" r="12" fill="#ff8fb1" stroke="{OL}" stroke-width="3"/><path d="M{cx+40},28 q6,-4 12,2" stroke="#fff" stroke-width="2.5" fill="none" opacity=".7"/>')
    if st["girl"] and st["age"] >= 2:  # small gold hoops
        for s_ in (-1, 1):
            hd.append(f'<circle cx="{cx+s_*60}" cy="112" r="8" fill="none" stroke="{OL}" stroke-width="5"/><circle cx="{cx+s_*60}" cy="112" r="8" fill="none" stroke="#e2b04a" stroke-width="2.5"/>')
    # face
    fy = 98
    hd.append(f'<ellipse cx="{cx-36}" cy="{fy+24}" rx="11" ry="7" fill="#e07a8a" opacity=".4"/><ellipse cx="{cx+36}" cy="{fy+24}" rx="11" ry="7" fill="#e07a8a" opacity=".4"/>'
              f'<ellipse cx="{cx-34}" cy="{fy+14}" rx="8" ry="3.5" fill="#fff" opacity=".3"/>')
    for s_ in (-1, 1):
        x = cx + s_ * 24
        if mood == "sleep" or blink:
            hd.append(f'<path d="M{x-12},{fy} q12,9 24,0" stroke="{OL}" stroke-width="4" fill="none" stroke-linecap="round"/>' + (f'<path d="M{x+s_*10},{fy+2} l{s_*5},-4" stroke="{OL}" stroke-width="2.5"/>' if st["girl"] else ""))
            continue
        hd.append(f'<path d="M{x-15},{fy} Q{x},{fy-20} {x+15},{fy} Q{x},{fy+17} {x-15},{fy} Z" fill="#fff" stroke="{OL}" stroke-width="2.5"/>'
                  f'<circle cx="{x}" cy="{fy+1}" r="9" fill="url(#irisG)"/><circle cx="{x}" cy="{fy+1}" r="4.5" fill="#120805"/><circle cx="{x+3}" cy="{fy-3}" r="3" fill="#fff"/><circle cx="{x-3}" cy="{fy+5}" r="1.4" fill="#fff"/>'
                  f'<path d="M{x-15},{fy} Q{x},{fy-20} {x+15},{fy-1}" stroke="#140a0a" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
        if st["girl"]:
            hd.append("".join(f'<path d="M{x+s_*(4+i*5)},{fy-9+i*2} l{s_*3},-6" stroke="#140a0a" stroke-width="2" stroke-linecap="round"/>' for i in range(3)))
        by = fy - 24 - (4 if mood in ("happy", "cheer") else 0)
        tilt = -7 if mood == "sad" else (9 if mood == "mad" else 0)   # sad: inner end raised, mad: inner end down
        hd.append(P(f"M{x-s_*13},{by+4+tilt} Q{x},{by-6} {x+s_*13},{by+2-tilt*.4} Q{x},{by} {x-s_*13},{by+4+tilt} Z", st["hair"], 1.5))
    hd.append(f'<path d="M{cx-2},{fy+10} Q{cx-6},{fy+22} {cx-1},{fy+24} Q{cx+6},{fy+24} {cx+6},{fy+20}" stroke="{skd}" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="{cx+1}" cy="{fy+17}" r="3" fill="#fff" opacity=".3"/>')
    my = fy + 36
    if talk > .05 and mood == "mad":
        hd.append(f'<path d="M{cx-16},{my-4} Q{cx},{my-10} {cx+16},{my-4} Q{cx+12},{my+6+12*talk:.1f} {cx},{my+8+12*talk:.1f} Q{cx-12},{my+6+12*talk:.1f} {cx-16},{my-4} Z" fill="#6e2030" stroke="{OL}" stroke-width="3"/><path d="M{cx-12},{my-4} h24 v4 h-24 Z" fill="#fff"/>')
    elif talk > .05:
        hd.append(f'<ellipse cx="{cx}" cy="{my+2}" rx="{8+4*talk:.1f}" ry="{3+10*talk:.1f}" fill="#6e2030" stroke="{OL}" stroke-width="3"/>'
                  + (f'<path d="M{cx-26},{fy+10} q-4,16 0,24" stroke="#9fdcff" stroke-width="5" fill="none" stroke-linecap="round"/>' if mood == "sad" else ""))
    elif mood in ("happy", "cheer"):
        hd.append(f'<path d="M{cx-18},{my-6} Q{cx},{my+20} {cx+18},{my-6} Z" fill="#6e2030" stroke="{OL}" stroke-width="3"/><path d="M{cx-14},{my-5} L{cx+14},{my-5} L{cx+11},{my+1} L{cx-11},{my+1} Z" fill="#fff"/><path d="M{cx-8},{my+9} Q{cx},{my+4} {cx+8},{my+9}" fill="#d16a7c"/>'
                  + (f'<path d="M{cx-19},{my-6} Q{cx},{my-12} {cx+19},{my-6}" stroke="#c87888" stroke-width="3.5" fill="none" stroke-linecap="round"/>' if st["girl"] and st["age"] >= 2 else ""))
    elif mood == "sad":
        hd.append(f'<path d="M{cx-12},{my+4} Q{cx},{my-6} {cx+12},{my+4}" stroke="#6e2030" stroke-width="4.5" fill="none" stroke-linecap="round"/><path d="M{cx-26},{fy+10} q-4,16 0,24" stroke="#9fdcff" stroke-width="5" fill="none" stroke-linecap="round"/>')
    elif mood == "sleep":
        hd.append(f'<ellipse cx="{cx}" cy="{my}" rx="5" ry="4" fill="#6e2030"/><text x="{cx+56}" y="{fy-40}" font-family="Anton" font-size="26" fill="#cfc4ff">z</text><text x="{cx+74}" y="{fy-62}" font-family="Anton" font-size="20" fill="#cfc4ff">z</text>')
    else:
        hd.append(f'<path d="M{cx-12},{my} Q{cx},{my+6} {cx+12},{my}" stroke="#6e2030" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
    return "".join(g) + "".join(hd)


def kid_head_sleeping(st):
    """Head-only sleeping kid for beds: the full kid scaled into the head area."""
    return f'<g transform="translate(-10,-10)">{"".join(kid(st, "sleep").split("<!--body-->")[-1:])}</g>'
