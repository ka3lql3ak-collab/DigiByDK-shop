"""Highly detailed rooms for "30 Days to Her" (1080x1920). Each returns static SVG; animated bits live in animate2.py."""
import random
from character import OL, KIDS, kid

S = f'stroke="{OL}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
S3 = f'stroke="{OL}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'

ROOM_DEFS = """<defs>
<pattern id="wallStars" width="120" height="120" patternUnits="userSpaceOnUse"><rect width="120" height="120" fill="#2b2a5c"/>
 <path d="M30,20 l4,10 10,2 -8,7 2,10 -8,-5 -8,5 2,-10 -8,-7 10,-2 Z" fill="#3e3d7a"/><circle cx="90" cy="80" r="6" fill="#3e3d7a"/><circle cx="80" cy="30" r="3" fill="#4a4890"/></pattern>
<pattern id="wallDamask" width="140" height="160" patternUnits="userSpaceOnUse"><rect width="140" height="160" fill="#1d2140"/>
 <path d="M70,20 q22,30 0,60 q-22,-30 0,-60 Z M70,100 q14,18 0,40 q-14,-22 0,-40 Z" fill="#232850"/><circle cx="0" cy="80" r="10" fill="#232850"/><circle cx="140" cy="80" r="10" fill="#232850"/></pattern>
<pattern id="wood" width="200" height="60" patternUnits="userSpaceOnUse"><rect width="200" height="60" fill="#3a2b2a"/><path d="M0,58 H200 M120,0 V60" stroke="#2a1f1e" stroke-width="4"/><path d="M10,20 q40,-6 80,0 M130,36 q30,-6 60,0" stroke="#45332f" stroke-width="3" fill="none"/></pattern>
<pattern id="quilt1" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="#ffd166"/><rect width="30" height="30" fill="#ffbf3a"/><rect x="30" y="30" width="30" height="30" fill="#ffbf3a"/><path d="M15,15 l4,0" stroke="#fff" stroke-width="3"/></pattern>
<pattern id="quilt2" width="50" height="50" patternUnits="userSpaceOnUse"><rect width="50" height="50" fill="#5fc7a8"/><circle cx="25" cy="25" r="9" fill="#a6ecd8"/></pattern>
<pattern id="quilt3" width="56" height="56" patternUnits="userSpaceOnUse"><rect width="56" height="56" fill="#ff8fb1"/><path d="M28,14 c-10,-10 -22,4 0,20 c22,-16 10,-30 0,-20 Z" fill="#ffd0df"/></pattern>
<pattern id="quilt4" width="60" height="40" patternUnits="userSpaceOnUse"><rect width="60" height="40" fill="#8fbaff"/><path d="M0,20 q15,-14 30,0 t30,0" stroke="#cfe0ff" stroke-width="6" fill="none"/></pattern>
<pattern id="tiles" width="90" height="90" patternUnits="userSpaceOnUse"><rect width="90" height="90" fill="#2c3352"/><rect x="2" y="2" width="86" height="86" fill="#323a5c"/><path d="M8,8 h30" stroke="#3e4870" stroke-width="4"/></pattern>
<pattern id="rugStripes" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#ff8fb1"/><rect width="20" height="40" fill="#ffd166"/></pattern>
<radialGradient id="bulbG" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff2b3"/><stop offset=".35" stop-color="#ffd166" stop-opacity=".6"/><stop offset="1" stop-color="#ffd166" stop-opacity="0"/></radialGradient>
<radialGradient id="candleG" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffe0a0" stop-opacity=".9"/><stop offset=".4" stop-color="#ff9d4a" stop-opacity=".35"/><stop offset="1" stop-color="#ff9d4a" stop-opacity="0"/></radialGradient>
<linearGradient id="tvG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9fb4ff"/><stop offset="1" stop-color="#4a5aa8"/></linearGradient>
<linearGradient id="moonBeam" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe3ff" stop-opacity=".42"/><stop offset="1" stop-color="#cfe3ff" stop-opacity="0"/></linearGradient>
</defs>"""

R = random.Random(21)


def frame_pic(x, y, w, h, rot, inner, color="#c9a96e"):
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect width="{w}" height="{h}" fill="{color}" {S}/>'
            f'<rect x="10" y="10" width="{w-20}" height="{h-20}" fill="#e9e0ff"/>{inner}<path d="M10,10 L{w-10},{h-10}" stroke="#fff" stroke-width="2" opacity=".35"/></g>')


def family_inner(w, h, n=5):
    cols = ("#9b1c32", "#ffd166", "#5fc7a8", "#ff8fb1", "#8fbaff")
    out = f'<rect x="10" y="{h*.6:.0f}" width="{w-20}" height="{h*.4-10:.0f}" fill="#b6e3a8"/><circle cx="{w-34}" cy="34" r="14" fill="#ffd166"/>'
    for i in range(n):
        x = 30 + i * (w - 60) / (n - 1); big = i == 0
        out += (f'<rect x="{x-10:.0f}" y="{h*.45:.0f}" width="{22 if big else 16}" height="{h*.32:.0f}" rx="6" fill="{cols[i]}"/>'
                f'<circle cx="{x+1:.0f}" cy="{h*.4:.0f}" r="{13 if big else 9}" fill="#c48466" stroke="{OL}" stroke-width="1.5"/>')
    return out


def crayon_drawing(x, y, rot, kind, label=None):
    inner = ""
    if kind == "house":
        inner = '<path d="M30,90 L30,50 L60,24 L90,50 L90,90 Z" fill="none" stroke="#ff5f5f" stroke-width="5"/><rect x="50" y="62" width="18" height="28" fill="none" stroke="#4a72b8" stroke-width="4"/><circle cx="104" cy="22" r="12" fill="none" stroke="#ffbf3a" stroke-width="5"/>'
    if kind == "family":
        inner = "".join(f'<circle cx="{20+i*24}" cy="{50-(i==0)*6}" r="{9 if i else 12}" fill="none" stroke="#6d32d4" stroke-width="4"/><path d="M{20+i*24},{60} v26 M{12+i*24},{70} h16" stroke="#6d32d4" stroke-width="4"/>' for i in range(5))
    if kind == "heart":
        inner = '<path d="M60,90 C20,62 30,30 60,46 C90,30 100,62 60,90 Z" fill="none" stroke="#ff4f8f" stroke-width="6"/>'
    if kind == "rainbow":
        inner = "".join(f'<path d="M{18+k*8},88 a{42-k*8},{42-k*8} 0 0 1 {84-k*16},0" stroke="{c}" stroke-width="7" fill="none"/>' for k, c in enumerate(("#ff5f5f", "#ffbf3a", "#5fc7a8", "#8fbaff")))
    lab = f'<text x="64" y="118" text-anchor="middle" font-family="Anton" font-size="18" fill="#ff4f8f">{label}</text>' if label else ""
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect width="128" height="128" fill="#fffdf6" {S3}/>{inner}{lab}'
            f'<rect x="44" y="-8" width="40" height="16" fill="#ffffff99" transform="rotate(-6 64 0)"/></g>')


def shelf(x, y, w, items):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="18" rx="4" fill="#8a6a52" {S3}/><path d="M{x+20},{y+18} l0,26 M{x+w-20},{y+18} l0,26" stroke="#6a4f3b" stroke-width="8"/>'
    cx = x + 12
    for it in items:
        if it == "books":
            for k in range(5):
                h = R.randint(54, 80); c = R.choice(("#ff5f5f", "#4a72b8", "#ffbf3a", "#5fc7a8", "#9b7fd4", "#ff8fb1"))
                out += f'<rect x="{cx}" y="{y-h}" width="16" height="{h}" fill="{c}" {S3}/><path d="M{cx+4},{y-h+10} h8" stroke="#fff" stroke-width="2" opacity=".6"/>'
                cx += 18
            cx += 10
        elif it == "bear":
            out += (f'<circle cx="{cx+10}" cy="{y-62}" r="10" fill="#a8744f" {S3}/><circle cx="{cx+44}" cy="{y-62}" r="10" fill="#a8744f" {S3}/>'
                    f'<ellipse cx="{cx+27}" cy="{y-22}" rx="26" ry="24" fill="#b98258" {S3}/><circle cx="{cx+27}" cy="{y-52}" r="22" fill="#b98258" {S3}/>'
                    f'<circle cx="{cx+20}" cy="{y-56}" r="3" fill="{OL}"/><circle cx="{cx+34}" cy="{y-56}" r="3" fill="{OL}"/><ellipse cx="{cx+27}" cy="{y-46}" rx="7" ry="5" fill="#e8c9a6"/>')
            cx += 64
        elif it == "trophy":
            out += f'<path d="M{cx},{y-70} h40 v14 q0,24 -20,28 q-20,-4 -20,-28 Z" fill="#e2b04a" {S3}/><rect x="{cx+14}" y="{y-28}" width="12" height="16" fill="#e2b04a"/><rect x="{cx+4}" y="{y-14}" width="32" height="14" rx="3" fill="#9c6f1c" {S3}/>'
            cx += 54
        elif it == "plant":
            out += (f'<path d="M{cx+6},{y-34} h40 l-6,34 h-28 Z" fill="#c76b3b" {S3}/>'
                    f'<path d="M{cx+26},{y-34} q-30,-40 -18,-66 M{cx+26},{y-34} q6,-46 26,-62 M{cx+26},{y-34} q-4,-30 -2,-54" stroke="#7a6a3a" stroke-width="5" fill="none"/>'
                    f'<path d="M{cx+8},{y-100} q-8,-4 -6,8 M{cx+52},{y-96} q8,-2 6,8" stroke="#8a7a3a" stroke-width="5" fill="none"/>')
            cx += 60
        elif it == "dino":
            out += f'<path d="M{cx},{y} q4,-40 34,-40 q16,-24 40,-10 q-6,10 -18,10 q6,22 -4,40 Z" fill="#5fc7a8" {S3}/><circle cx="{cx+64}" cy="{y-44}" r="3" fill="{OL}"/>'
            cx += 84
        elif it == "blocks":
            for k, (c, l) in enumerate((("#ff5f5f", "M"), ("#ffbf3a", "O"), ("#5fc7a8", "M"))):
                out += f'<rect x="{cx+k*34}" y="{y-32}" width="32" height="32" fill="{c}" {S3}/><text x="{cx+k*34+16}" y="{y-8}" text-anchor="middle" font-family="Anton" font-size="24" fill="#fff">{l}</text>'
            cx += 110
    return out


def string_lights(x1, y1, x2, y2, n=12, sag=60, glow=1.0):
    out = f'<path d="M{x1},{y1} Q{(x1+x2)/2},{(y1+y2)/2+sag} {x2},{y2}" stroke="#2a2a2a" stroke-width="3" fill="none"/>'
    cols = ("#ffd166", "#ff8fb1", "#8fbaff", "#5fc7a8", "#ffb36b")
    for i in range(n):
        u = (i + .5) / n
        x = (1 - u) ** 2 * x1 + 2 * (1 - u) * u * (x1 + x2) / 2 + u ** 2 * x2
        y = (1 - u) ** 2 * y1 + 2 * (1 - u) * u * ((y1 + y2) / 2 + sag) + u ** 2 * y2
        c = cols[i % len(cols)]
        out += (f'<circle cx="{x:.0f}" cy="{y+14:.0f}" r="{30*glow:.0f}" fill="{c}" opacity="{.18*glow:.2f}"/>'
                f'<ellipse cx="{x:.0f}" cy="{y+14:.0f}" rx="8" ry="11" fill="{c}" stroke="{OL}" stroke-width="2"/><rect x="{x-4:.0f}" y="{y:.0f}" width="8" height="6" fill="#444"/>')
    return out


def bunk_bed(x, top_kid, bot_kid, quilt_top, quilt_bot, sleeping=True):
    """Bunk bed at x (left edge), floor at y=1540. Kids drawn lying under quilts."""
    W_ = 470
    out = f'<rect x="{x}" y="900" width="26" height="640" fill="#8a6a52" {S}/><rect x="{x+W_-26}" y="900" width="26" height="640" fill="#8a6a52" {S}/>'
    for by, st, q in ((1070, top_kid, quilt_top), (1390, bot_kid, quilt_bot)):
        out += f'<rect x="{x+10}" y="{by}" width="{W_-20}" height="90" rx="12" fill="#efeaf8" {S}/>'
        out += f'<ellipse cx="{x+100}" cy="{by+6}" rx="70" ry="32" fill="#fff" {S}/><path d="M{x+46},{by} q40,-10 90,2" stroke="#d9d2e8" stroke-width="4" fill="none"/>'
        if st is not None:
            out += f'<g transform="translate({x+28},{by+82}) rotate(-90) scale(.78)">{kid(st, "sleep" if sleeping else "sad")}</g>'
        out += (f'<path d="M{x+150},{by-36} Q{x+300},{by-64} {x+W_-14},{by-24} L{x+W_-14},{by+90} L{x+140},{by+90} Q{x+118},{by+20} {x+150},{by-36} Z" fill="url(#{q})" {S}/>'
                f'<path d="M{x+160},{by-20} Q{x+300},{by-46} {x+W_-20},{by-8}" stroke="#fff" stroke-width="5" opacity=".35" fill="none"/>'
                f'<rect x="{x}" y="{by+90}" width="{W_}" height="34" rx="8" fill="#8a6a52" {S}/>')
    out += f'<rect x="{x}" y="900" width="{W_}" height="30" rx="8" fill="#8a6a52" {S}/>'
    for k in range(5):  # ladder
        out += f'<rect x="{x+W_-90}" y="{1130+k*52}" width="60" height="12" rx="5" fill="#a5836a" {S3}/>'
    out += f'<rect x="{x+W_-96}" y="1110" width="12" height="290" fill="#8a6a52" {S3}/><rect x="{x+W_-36}" y="1110" width="12" height="290" fill="#8a6a52" {S3}/>'
    return out


def kids_room(lights_on=True):
    out = ['<rect width="1080" height="1920" fill="url(#wallStars)"/>']
    # window with curtains + moon
    out.append(f'<rect x="380" y="330" width="320" height="380" rx="12" fill="#0b1030" {S}/><circle cx="600" cy="420" r="52" fill="#f6f1d8"/><circle cx="582" cy="406" r="11" fill="#e3dcc0"/><circle cx="616" cy="440" r="8" fill="#e3dcc0"/>'
               + "".join(f'<circle cx="{R.randint(400, 690)}" cy="{R.randint(350, 690)}" r="2" fill="#fff" opacity=".8"/>' for _ in range(16))
               + f'<line x1="540" y1="330" x2="540" y2="710" stroke="{OL}" stroke-width="6"/><line x1="380" y1="520" x2="700" y2="520" stroke="{OL}" stroke-width="6"/>'
               f'<path d="M350,310 q30,220 6,440 h70 q-26,-220 0,-440 Z" fill="#7a5cc4" {S}/><path d="M730,310 q-30,220 -6,440 h-70 q26,-220 0,-440 Z" fill="#7a5cc4" {S}/>'
               + "".join(f'<circle cx="{366+k%2*24}" cy="{350+k*40}" r="5" fill="#ffd166" opacity=".8"/><circle cx="{690+k%2*20}" cy="{350+k*40}" r="5" fill="#ffd166" opacity=".8"/>' for k in range(10))
               + f'<rect x="330" y="296" width="420" height="22" rx="10" fill="#b9a2e8" {S}/>')
    # growth chart
    out.append(f'<rect x="980" y="620" width="56" height="560" fill="#fffdf6" {S3}/>' + "".join(f'<path d="M980,{640+k*44} h{18 if k%2 else 30}" stroke="{OL}" stroke-width="3"/>' for k in range(12))
               + "".join(f'<path d="M1000,{y} h36" stroke="{c}" stroke-width="5"/><text x="1008" y="{y-6}" font-family="Anton" font-size="14" fill="{c}">{n}</text>' for y, c, n in ((700, "#ff5f5f", "A"), (800, "#5fc7a8", "J"), (880, "#ff4f8f", "M"), (980, "#4a72b8", "K"))))
    # drawings + poster + banner
    out.append(crayon_drawing(60, 330, -6, "family", "I &#10084; MOM") + crayon_drawing(210, 360, 5, "house") + crayon_drawing(790, 340, 4, "rainbow") + crayon_drawing(80, 520, 3, "heart"))
    out.append(f'<g transform="translate(780,520) rotate(-3)"><rect width="170" height="230" fill="#123a4f" {S}/><path d="M24,190 q10,-80 60,-80 q30,-40 70,-16 q-10,14 -30,14 q10,40 -6,82 Z" fill="#5fc7a8" {S3}/>'
               f'<text x="85" y="60" text-anchor="middle" font-family="Anton" font-size="34" fill="#ffd166">DINO</text><text x="85" y="94" text-anchor="middle" font-family="Anton" font-size="26" fill="#fff">ROAR!</text></g>')
    out.append(string_lights(20, 270, 1060, 270, 16, 70, 1.0 if lights_on else .25))
    # shelves
    out.append(shelf(30, 820, 300, ["books", "bear"]) + shelf(380, 860, 320, ["blocks", "trophy", "plant"]))
    # floor
    out.append('<rect y="1540" width="1080" height="380" fill="url(#wood)"/><ellipse cx="540" cy="1720" rx="420" ry="110" fill="url(#rugStripes)" stroke="#2a161c" stroke-width="5"/><ellipse cx="540" cy="1720" rx="330" ry="78" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="14 12" opacity=".6"/>')
    # bunk beds
    out.append(bunk_bed(20, KIDS[0], KIDS[2], "quilt1", "quilt3") + bunk_bed(590, KIDS[1], KIDS[3], "quilt2", "quilt4"))
    # floor clutter: backpacks, sneakers, toys, cloud nightlight
    out.append(f'<g transform="translate(480,1420)"><rect width="110" height="130" rx="30" fill="#ff8fb1" {S}/><rect x="16" y="56" width="78" height="50" rx="14" fill="#ffb3cb" {S3}/><path d="M24,8 q31,-40 62,0" stroke="{OL}" stroke-width="6" fill="none"/><circle cx="55" cy="30" r="8" fill="#ffd166"/></g>')
    out.append(f'<g transform="translate(150,1800)"><path d="M0,0 h60 q18,8 14,24 h-78 q-4,-16 4,-24 Z" fill="#fff" {S3}/><path d="M-4,18 h78" stroke="#ff5f5f" stroke-width="5"/></g>'
               f'<g transform="translate(240,1830) rotate(18)"><path d="M0,0 h50 q14,8 12,20 h-66 q-2,-14 4,-20 Z" fill="#fff" {S3}/><path d="M-4,14 h66" stroke="#4a72b8" stroke-width="5"/></g>'
               f'<g transform="translate(820,1790)"><rect width="70" height="34" rx="8" fill="#ff5f5f" {S3}/><circle cx="16" cy="38" r="10" fill="#333"/><circle cx="54" cy="38" r="10" fill="#333"/><rect x="12" y="-18" width="40" height="22" rx="6" fill="#8fbaff" {S3}/></g>'
               f'<g transform="translate(680,1850)">' + "".join(f'<rect x="{k*26}" y="{-(k%2)*8}" width="24" height="24" fill="{c}" {S3}/>' for k, c in enumerate(("#ffbf3a", "#5fc7a8", "#ff8fb1"))) + '</g>'
               f'<g transform="translate(500,1600)"><path d="M0,30 q0,-30 30,-30 q10,-24 40,-16 q30,-14 46,12 q24,2 24,34 Z" fill="#fff6d6" {S3}/><circle cx="70" cy="20" r="80" fill="#ffd166" opacity=".14"/></g>')
    return "".join(out)


def apartment():
    out = ['<rect width="1080" height="1920" fill="url(#wallDamask)"/>']
    # ceiling water stain + crack
    out.append('<ellipse cx="760" cy="60" rx="170" ry="60" fill="#3a3b52" opacity=".7"/><ellipse cx="760" cy="56" rx="110" ry="36" fill="#454760" opacity=".7"/><path d="M640,0 l30,40 -20,30 40,50" stroke="#14152a" stroke-width="4" fill="none"/>')
    # window with city + rain streaks
    city = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{860-y}" fill="#0b0e22"/>' for x, y, w in ((620, 620, 90), (700, 560, 70), (770, 640, 110), (870, 590, 80), (940, 670, 100)))
    lit = "".join(f'<rect x="{R.randint(630, 1020)}" y="{R.randint(590, 840)}" width="10" height="14" fill="#ffd98a" opacity="{R.uniform(.3,.9):.2f}"/>' for _ in range(40))
    out.append(f'<rect x="600" y="400" width="420" height="480" fill="#05060f"/>{city}{lit}'
               + "".join(f'<path d="M{R.randint(610, 1010)},{R.randint(410, 840)} q-4,20 0,{R.randint(20, 50)}" stroke="#bcd0ff" stroke-width="3" fill="none" opacity=".7"/>' for _ in range(40))
               + f'<rect x="596" y="396" width="428" height="488" fill="none" stroke="#3b3560" stroke-width="18"/><line x1="810" y1="400" x2="810" y2="880" stroke="#3b3560" stroke-width="12"/>'
               f'<path d="M560,370 q40,280 20,560 l70,0 q-30,-300 0,-560 Z" fill="#4a2d5c" {S}/><path d="M1060,370 q-40,280 -20,560 l-70,0 q30,-300 0,-560 Z" fill="#4a2d5c" {S}/><rect x="540" y="350" width="540" height="26" rx="8" fill="#5a4a7a" {S}/>')
    # calendar RENT DUE
    cal = "".join(f'<rect x="{12+(k%7)*24}" y="{56+(k//7)*22}" width="22" height="20" fill="#fff" stroke="#ccc" stroke-width="1"/>' for k in range(28))
    out.append(f'<g transform="translate(330,430) rotate(3)"<rect width="190" height="170" fill="#fffdf6" {S}/><rect width="190" height="44" fill="#e23b3b"/><text x="95" y="32" text-anchor="middle" font-family="Anton" font-size="26" fill="#fff">OCTOBER</text>{cal}'
               f'<circle cx="131" cy="111" r="20" fill="none" stroke="#e23b3b" stroke-width="5"/><text x="95" y="196" text-anchor="middle" font-family="Anton" font-size="26" fill="#e23b3b" transform="rotate(-6 95 190)">RENT DUE!!</text></g>'.replace('rotate(3)"<rect', 'rotate(3)"><rect'))
    # photos
    out.append(frame_pic(60, 380, 230, 170, -6, family_inner(230, 170)) + frame_pic(120, 600, 140, 180, 4, '<circle cx="70" cy="80" r="34" fill="#c48466"/><path d="M30,170 q40,-70 80,0" fill="#9b1c32"/><path d="M34,60 q36,-50 72,0" fill="#9b1c32"/>', "#8a6a52"))
    # TV static glow on a stand (left-back)
    out.append(f'<rect x="40" y="880" width="300" height="190" rx="12" fill="#1a1a22" {S}/><rect x="56" y="896" width="268" height="158" fill="url(#tvG)"/>'
               + "".join(f'<rect x="{R.randint(56, 310)}" y="{R.randint(896, 1046)}" width="{R.randint(4, 14)}" height="3" fill="#fff" opacity=".7"/>' for _ in range(60))
               + f'<text x="190" y="990" text-anchor="middle" font-family="Anton" font-size="30" fill="#fff" opacity=".8">NO SIGNAL</text><rect x="20" y="1070" width="340" height="150" fill="#3e2a22" {S}/><rect x="40" y="1090" width="140" height="110" fill="#2e1f19" {S3}/>')
    # dying plant
    out.append(f'<g transform="translate(470,1060)"><path d="M0,0 h70 l-10,80 h-50 Z" fill="#c76b3b" {S3}/><path d="M35,0 q-40,-50 -30,-110 M35,0 q20,-60 50,-90 M35,0 q-6,-40 0,-80" stroke="#7a6a3a" stroke-width="6" fill="none"/>'
               f'<path d="M-2,-104 q-14,6 -8,20 M82,-86 q14,4 6,18 M30,-76 q-12,-2 -12,12" stroke="#a08a40" stroke-width="7" fill="none"/><path d="M60,80 q10,20 30,24" stroke="#8a7a3a" stroke-width="4" fill="none"/></g>')
    # floor + rug + couch with laundry
    out.append('<rect y="1400" width="1080" height="520" fill="url(#wood)"/><ellipse cx="540" cy="1720" rx="500" ry="110" fill="#3a2a5c" opacity=".85"/><ellipse cx="540" cy="1720" rx="430" ry="80" fill="none" stroke="#5a4a7a" stroke-width="8" stroke-dasharray="20 14"/>')
    out.append(f'<path d="M240,1120 q0,-60 60,-60 h540 q60,0 60,60 v300 h-660 Z" fill="url(#couchG)" {S}/><rect x="210" y="1230" width="90" height="230" rx="40" fill="#3a3258" {S}/><rect x="840" y="1230" width="90" height="230" rx="40" fill="#3a3258" {S}/>'
               f'<path d="M680,1130 q90,-40 160,40 q-40,130 -160,150 Z" fill="#8f87a6" {S}/><path d="M320,1140 q60,-30 120,10 l-20,70 q-60,10 -100,-20 Z" fill="#ff8fb1" {S3}/><path d="M440,1150 q50,-20 90,10 l-10,60 q-50,6 -80,-20 Z" fill="#5fc7a8" {S3}/>'
               f'<rect x="560" y="1170" width="90" height="70" rx="10" fill="#ffd166" {S3}/>')
    # coffee table: bottles, pizza box, bills, phone
    out.append(f'<path d="M150,1600 h780 l-40,40 h-700 Z" fill="#5a3f33" {S}/><rect x="200" y="1640" width="24" height="120" fill="#3e2a22" {S}/><rect x="856" y="1640" width="24" height="120" fill="#3e2a22" {S}/>'
               f'<g transform="translate(560,1540) rotate(-4)"><rect width="200" height="60" fill="#e9c58a" {S}/><path d="M0,0 l30,-36 h170 l-30,36" fill="#f3d6a0" {S}/><text x="100" y="40" text-anchor="middle" font-family="Anton" font-size="24" fill="#c0392b">PIZZA</text><circle cx="40" cy="22" r="6" fill="#c0392b"/></g>')
    return "".join(out)


def kitchen_dark():
    out = ['<rect width="1080" height="1920" fill="#141a2e"/>']
    out.append("".join(f'<rect x="{x}" y="{y}" width="58" height="38" fill="#18203a" stroke="#1f2742" stroke-width="3"/>' for x in range(0, 1080, 60) for y in range(820, 1180, 40)))
    out.append(f'<rect x="20" y="360" width="640" height="320" rx="10" fill="#272c4a" {S}/><line x1="340" y1="360" x2="340" y2="680" stroke="{OL}" stroke-width="4"/><circle cx="320" cy="520" r="8" fill="#8a8fb0"/><circle cx="360" cy="520" r="8" fill="#8a8fb0"/>')
    out.append(f'<circle cx="840" cy="300" r="62" fill="#f3efe6" {S}/><text x="840" y="396" text-anchor="middle" font-family="Anton" font-size="32" fill="#ff5f5f">2:14 AM</text>')
    out.append(f'<rect y="1180" width="760" height="300" fill="#2a2f4c" {S}/><rect x="-10" y="1150" width="790" height="44" rx="8" fill="#545a7a" {S}/>'
               + "".join(f'<ellipse cx="205" cy="{1140-i*16}" rx="{90-i*4}" ry="14" fill="#e9e6f2" {S3}/>' for i in range(6))
               + f'<rect x="360" y="1040" width="70" height="110" rx="6" fill="#ffbf3a" {S3}/><text x="395" y="1100" text-anchor="middle" font-family="Anton" font-size="18" fill="#c0392b">O\'s</text>'
               f'<rect x="450" y="1080" width="90" height="70" rx="14" fill="#ff8fb1" {S3}/><rect x="560" y="1080" width="90" height="70" rx="14" fill="#8fbaff" {S3}/>')
    out.append(f'<path d="M800,560 L1060,560 L1060,1480 L800,1480 Z" fill="#c9d4e2" {S}/><path d="M820,600 h220" stroke="{OL}" stroke-width="3"/>'
               f'<rect x="830" y="640" width="90" height="110" fill="#fff" transform="rotate(-5 875 695)" {S3}/><text x="875" y="700" text-anchor="middle" font-family="Anton" font-size="18" fill="#6d32d4" transform="rotate(-5 875 695)">MOMMY</text>'
               f'<circle cx="980" cy="680" r="14" fill="#ff5f5f" {S3}/><circle cx="1010" cy="760" r="12" fill="#5fc7a8" {S3}/>')
    out.append('<rect y="1480" width="1080" height="440" fill="#1c2036"/>' + "".join(f'<rect x="{x}" y="1480" width="120" height="440" fill="{"#20253f" if (x//120)%2 else "#191d33"}"/>' for x in range(0, 1080, 120)))
    return "".join(out)


def bathroom_candle():
    out = ['<rect width="1080" height="1920" fill="url(#tiles)"/>']
    out.append(f'<rect x="548" y="398" width="464" height="904" rx="34" fill="#8a8fb0" {S}/><rect x="560" y="410" width="440" height="880" rx="26" fill="#2a2850"/>')
    out.append(f'<rect x="510" y="1310" width="540" height="70" rx="16" fill="#e9eef8" {S}/><ellipse cx="780" cy="1330" rx="130" ry="22" fill="#b9c3d6"/>'
               f'<rect x="590" y="1240" width="70" height="80" rx="10" fill="#8fbaff" {S3}/>'
               + "".join(f'<rect x="{598+i*12}" y="{1200-(i%2)*14}" width="8" height="70" rx="4" fill="{c}"/>' for i, c in enumerate(("#9b1c32", "#ffd166", "#5fc7a8", "#ff8fb1", "#8fbaff")))
               + f'<g transform="translate(930,1270)"><ellipse cx="0" cy="20" rx="34" ry="26" fill="#ffd166" {S3}/><circle cx="14" cy="-8" r="18" fill="#ffd166" {S3}/><path d="M28,-8 l16,4 -16,6 Z" fill="#ff8a3a" {S3}/><circle cx="18" cy="-12" r="3" fill="{OL}"/></g>'
               f'<rect x="40" y="420" width="40" height="560" fill="#ff8fb1" {S3}/><rect x="60" y="420" width="140" height="300" rx="10" fill="#b9a2e8" {S3}/><path d="M60,600 h140" stroke="#fff" stroke-width="6" opacity=".5"/>')
    out.append('<rect y="1500" width="1080" height="420" fill="#181b30"/>')
    return "".join(out)
