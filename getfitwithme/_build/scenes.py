"""Detailed, cinematic 1080x1920 scene backgrounds + frame composer for "30 Days to Her"."""
import html, math, random
from character import DEFS as CHAR_DEFS, danielle, kid, KIDS, OL, prop_svg

e = html.escape
W, H = 1080, 1920

SCENE_DEFS = """<defs>
<radialGradient id="vig" cx=".5" cy=".46" r=".78"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#03020a" stop-opacity=".92"/></radialGradient>
<radialGradient id="lampGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffcf7a" stop-opacity=".75"/><stop offset=".45" stop-color="#ff9f4a" stop-opacity=".22"/><stop offset="1" stop-color="#ff9f4a" stop-opacity="0"/></radialGradient>
<linearGradient id="nightWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151a33"/><stop offset="1" stop-color="#232a4a"/></linearGradient>
<linearGradient id="floorN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2238"/><stop offset="1" stop-color="#120e1a"/></linearGradient>
<linearGradient id="skyN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05060f"/><stop offset="1" stop-color="#1c2448"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe3ff" stop-opacity=".38"/><stop offset="1" stop-color="#cfe3ff" stop-opacity="0"/></linearGradient>
<linearGradient id="fridgeBeam" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#e8f6ff" stop-opacity=".55"/><stop offset="1" stop-color="#e8f6ff" stop-opacity="0"/></linearGradient>
<radialGradient id="bulb" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff1c2" stop-opacity=".95"/><stop offset=".4" stop-color="#ffcf7a" stop-opacity=".35"/><stop offset="1" stop-color="#ffcf7a" stop-opacity="0"/></radialGradient>
<radialGradient id="mirrorGlow" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="#b98cff" stop-opacity=".85"/><stop offset=".6" stop-color="#6d32d4" stop-opacity=".35"/><stop offset="1" stop-color="#2a1260" stop-opacity="0"/></radialGradient>
<linearGradient id="woodG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4a3a"/><stop offset="1" stop-color="#3e2a22"/></linearGradient>
<linearGradient id="couchG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4c4270"/><stop offset="1" stop-color="#2c2546"/></linearGradient>
<linearGradient id="hudBar"><stop offset="0" stop-color="#8b57ee"/><stop offset="1" stop-color="#ff7ac8"/></linearGradient>
<filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="mirrorFx"><feGaussianBlur stdDeviation="1.2" result="b"/><feColorMatrix in="b" type="matrix" values=".55 .2 .45 0 0  .25 .25 .5 0 0  .6 .3 .9 0 0  0 0 0 1 0"/></filter>
<clipPath id="mirrorClip"><rect x="560" y="430" width="440" height="860" rx="26"/></clipPath>
</defs>"""

S = f'stroke="{OL}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
R = random.Random(7)


def rain(n=220, op=.35):
    return "".join(f'<line x1="{x}" y1="{y}" x2="{x-14}" y2="{y+58}" stroke="#a9c4ff" stroke-width="{R.choice((2,2,3))}" opacity="{op*R.uniform(.5,1):.2f}"/>'
                   for x, y in ((R.randint(0, 1100), R.randint(0, 1900)) for _ in range(n)))


def wine_bottle(x, y, rot=0, empty=False):
    return (f'<g transform="translate({x},{y}) rotate({rot})"><path d="M-10,-120 h20 v34 q14,14 14,36 v86 q0,8 -8,8 h-32 q-8,0 -8,-8 v-86 q0,-22 14,-36 Z" fill="{"#2c1220" if empty else "#4a1530"}" {S}/>'
            f'<rect x="-16" y="-34" width="32" height="38" fill="#e9dcc3"/><rect x="-14" y="-110" width="6" height="140" rx="3" fill="#fff" opacity=".16"/>'
            + ("" if empty else '<rect x="-17" y="-2" width="34" height="34" fill="#7a1530" opacity=".55"/>') + '</g>')


def wine_glass(x, y, full=.5):
    return (f'<g transform="translate({x},{y})"><path d="M-26,-90 h52 q0,56 -26,62 q-26,-6 -26,-62 Z" fill="#ffffff22" {S}/>'
            f'<path d="M-22,{-90+50*(1-full):.0f} h44 q-4,36 -22,40 q-18,-4 -22,-40 Z" fill="#8a1530"/><path d="M0,-28 v34 M-20,8 h40" {S} fill="none"/>'
            f'<path d="M-18,-82 q-2,20 4,34" stroke="#fff" stroke-width="3" opacity=".5" fill="none"/></g>')


def bills(x, y, label="PAST DUE", rot=-6):
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect x="16" y="-14" width="150" height="100" fill="#ece6da" {S}/><rect width="150" height="100" fill="#f7f3ea" {S}/>'
            f'<path d="M14,22 h90 M14,40 h110 M14,58 h70" stroke="#c9c1b4" stroke-width="6"/>'
            f'<g transform="rotate(-12 100 70)"><rect x="40" y="52" width="{len(label)*14+20}" height="34" fill="none" stroke="#e23b3b" stroke-width="4" rx="4"/>'
            f'<text x="{50}" y="78" font-family="Anton" font-size="24" fill="#e23b3b">{e(label)}</text></g></g>')


def teddy(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><circle cx="-26" cy="-58" r="14" fill="#a8744f" {S}/><circle cx="26" cy="-58" r="14" fill="#a8744f" {S}/>'
            f'<ellipse cx="0" cy="10" rx="40" ry="44" fill="#b98258" {S}/><circle cx="0" cy="-40" r="32" fill="#b98258" {S}/><ellipse cx="0" cy="-30" rx="14" ry="10" fill="#e8c9a6"/>'
            f'<circle cx="-11" cy="-46" r="4" fill="{OL}"/><circle cx="11" cy="-46" r="4" fill="{OL}"/><circle cx="0" cy="-33" r="4" fill="{OL}"/><ellipse cx="0" cy="16" rx="20" ry="22" fill="#e8c9a6"/></g>')


# ================================================================ backgrounds
def bg_apartment(storm=True):
    city = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{900-y}" fill="#0b0e22"/>' for x, y, w in ((620, 640, 90), (700, 580, 70), (770, 660, 110), (870, 600, 80), (940, 690, 100)))
    lit = "".join(f'<rect x="{R.randint(630, 1020)}" y="{R.randint(600, 860)}" width="10" height="14" fill="#ffd98a" opacity="{R.uniform(.3,.9):.2f}"/>' for _ in range(40))
    return (f'<rect width="1080" height="1920" fill="url(#nightWall)"/>'
            + "".join(f'<rect x="{x}" y="0" width="34" height="1500" fill="#ffffff" opacity=".018"/>' for x in range(0, 1080, 90)) +
            # window + storm
            f'<rect x="600" y="420" width="420" height="500" fill="url(#skyN)"/>{city}{lit}'
            + (f'<path d="M880,430 l-40,110 h40 l-60,140 l110,-170 h-44 l40,-80 Z" fill="#fff6c4" opacity=".95"/><rect x="600" y="420" width="420" height="500" fill="#cfd8ff" opacity=".18"/>' if storm else "") +
            f'<g opacity=".7">{"".join(f"<path d=\'M{R.randint(610,1010)},{R.randint(430,860)} q-4,20 0,{R.randint(20,50)}\' stroke=\'#bcd0ff\' stroke-width=\'3\' fill=\'none\'/>" for _ in range(40))}</g>'
            f'<rect x="596" y="416" width="428" height="508" fill="none" stroke="#3b3560" stroke-width="18"/><line x1="810" y1="420" x2="810" y2="920" stroke="#3b3560" stroke-width="12"/><line x1="600" y1="670" x2="1020" y2="670" stroke="#3b3560" stroke-width="12"/>'
            f'<path d="M560,380 q40,280 20,600 l70,0 q-30,-320 0,-600 Z" fill="#3a2d5c" {S}/><path d="M1060,380 q-40,280 -20,600 l-70,0 q30,-320 0,-600 Z" fill="#3a2d5c" {S}/>'
            f'<rect x="540" y="360" width="540" height="26" rx="8" fill="#5a4a7a" {S}/>'
            # crooked family photo
            f'<g transform="translate(150,520) rotate(-7)"><rect width="260" height="190" fill="#c9a96e" {S}/><rect x="16" y="16" width="228" height="158" fill="#e9d9ff"/>'
            + "".join(f'<circle cx="{50+i*40}" cy="{80+(i%2)*6}" r="{20 if i==0 else 13}" fill="#c48466" stroke="{OL}" stroke-width="2"/><rect x="{38+i*40}" y="{100+(i%2)*6}" width="{24 if i==0 else 18}" height="40" rx="8" fill="{("#9b1c32","#ffd166","#5fc7a8","#ff8fb1","#8fbaff")[i]}"/>' for i in range(5))
            + '<path d="M16,16 L244,174" stroke="#fff" stroke-width="3" opacity=".5"/><path d="M60,16 L30,60 L80,90" stroke="#fff" stroke-width="2" fill="none" opacity=".7"/></g>'
            # lamp
            f'<ellipse cx="140" cy="960" rx="300" ry="300" fill="url(#lampGlow)"/><path d="M80,820 L200,820 L230,920 L50,920 Z" fill="#f2c47a" {S}/><rect x="132" y="920" width="16" height="230" fill="#4a3a30" {S}/>'
            f'<rect x="40" y="1150" width="200" height="22" rx="6" fill="url(#woodG)" {S}/><rect x="60" y="1172" width="160" height="200" fill="#3e2a22" {S}/>'
            # floor + rug + couch
            f'<rect y="1400" width="1080" height="520" fill="url(#floorN)"/><ellipse cx="540" cy="1720" rx="500" ry="110" fill="#3a2a5c" opacity=".8"/><ellipse cx="540" cy="1720" rx="430" ry="80" fill="none" stroke="#5a4a7a" stroke-width="8" stroke-dasharray="20 14"/>'
            f'<path d="M260,1120 q0,-60 60,-60 h520 q60,0 60,60 v300 h-640 Z" fill="url(#couchG)" {S}/><rect x="230" y="1230" width="90" height="230" rx="40" fill="#3a3258" {S}/><rect x="840" y="1230" width="90" height="230" rx="40" fill="#3a3258" {S}/>'
            f'<path d="M700,1140 q80,-30 140,40 q-40,120 -140,140 Z" fill="#8f87a6" {S}/><rect x="330" y="1150" width="170" height="110" rx="30" fill="#6d5e9a" {S} transform="rotate(-8 415 1205)"/>'
            # coffee table + evidence
            f'<path d="M150,1600 h780 l-40,40 h-700 Z" fill="url(#woodG)" {S}/><rect x="200" y="1640" width="24" height="120" fill="#3e2a22" {S}/><rect x="856" y="1640" width="24" height="120" fill="#3e2a22" {S}/>'
            + wine_bottle(250, 1590) + wine_bottle(840, 1585, 0, True) + f'<g transform="translate(330,1590) rotate(84)">{wine_bottle(0, 0, 0, True)}</g>' + wine_glass(770, 1598, .35)
            + bills(420, 1500, "PAST DUE", -8) + bills(560, 1520, "FINAL NOTICE", 5) +
            f'<rect x="690" y="1556" width="40" height="70" rx="8" fill="#16131c" {S}/><rect x="695" y="1562" width="30" height="56" rx="4" fill="#8fbaff" opacity=".9"/><ellipse cx="710" cy="1590" rx="60" ry="40" fill="#8fbaff" opacity=".15"/>'
            + teddy(980, 1830, .9) + f'<rect x="60" y="1800" width="70" height="30" rx="8" fill="#ff5f5f" {S}/><circle cx="75" cy="1834" r="9" fill="#333"/><circle cx="115" cy="1834" r="9" fill="#333"/>')


def bg_kitchen_night():
    return (f'<rect width="1080" height="1920" fill="#141a2e"/>'
            + "".join(f'<rect x="{x}" y="{y}" width="58" height="38" fill="none" stroke="#1f2742" stroke-width="3"/>' for x in range(0, 1080, 60) for y in range(820, 1180, 40)) +
            f'<rect x="20" y="380" width="620" height="300" rx="10" fill="#272c4a" {S}/><line x1="330" y1="380" x2="330" y2="680" stroke="{OL}" stroke-width="4"/><circle cx="310" cy="530" r="8" fill="#8a8fb0"/><circle cx="350" cy="530" r="8" fill="#8a8fb0"/>'
            # clock 2:07
            f'<circle cx="720" cy="420" r="62" fill="#f3efe6" {S}/><path d="M720,420 L720,374 M720,420 L744,434" stroke="{OL}" stroke-width="7" stroke-linecap="round"/><text x="720" y="516" text-anchor="middle" font-family="Anton" font-size="32" fill="#ff5f5f">2:07 AM</text>'
            # counter, sink, dishes, bills
            f'<rect y="1180" width="760" height="300" fill="#2a2f4c" {S}/><rect x="-10" y="1150" width="790" height="44" rx="8" fill="#545a7a" {S}/>'
            f'<rect x="80" y="1160" width="250" height="30" rx="8" fill="#3a4060"/>'
            + "".join(f'<ellipse cx="{205}" cy="{1140-i*16}" rx="{90-i*4}" ry="14" fill="#e9e6f2" {S}/>' for i in range(6)) +
            f'<rect x="380" y="1080" width="60" height="70" rx="8" fill="#c9c3d8" {S}/><rect x="460" y="1060" width="44" height="90" rx="10" fill="#4a1530" {S}/>'
            + bills(520, 1040, "SHUT-OFF NOTICE", -4) +
            # open fridge with light
            f'<path d="M800,560 L1060,560 L1060,1480 L800,1480 Z" fill="#dde7f2" {S}/><path d="M816,580 h228 v880 h-228 Z" fill="#f4fbff"/>'
            + "".join(f'<line x1="816" y1="{y}" x2="1044" y2="{y}" stroke="#b8c6d6" stroke-width="6"/>' for y in (780, 980, 1180)) +
            f'<rect x="840" y="1100" width="50" height="78" rx="6" fill="#fff" {S}/><text x="865" y="1150" text-anchor="middle" font-family="Anton" font-size="16" fill="#4a72b8">MILK</text>'
            f'<rect x="960" y="920" width="34" height="58" rx="8" fill="#e23b3b" {S}/><rect x="900" y="1404" width="80" height="40" rx="10" fill="#ffd166" {S}/>'
            f'<path d="M800,560 L640,620 L640,1520 L800,1480 Z" fill="#c9d4e2" {S}/><rect x="660" y="700" width="110" height="140" fill="#fff" transform="rotate(-6 715 770)" {S}/>'
            f'<path d="M680,740 q20,-30 40,0 M690,800 h50" stroke="#ff5f8f" stroke-width="5" fill="none"/><text x="715" y="830" text-anchor="middle" font-family="Anton" font-size="18" fill="#6d32d4" transform="rotate(-6 715 770)">MOMMY</text>'
            f'<path d="M800,600 L0,1500 L0,1920 L800,1500 Z" fill="url(#fridgeBeam)"/>'
            f'<rect y="1480" width="1080" height="440" fill="#1c2036"/>' + "".join(f'<rect x="{x}" y="1480" width="120" height="440" fill="{"#20253f" if (x//120)%2 else "#191d33"}"/>' for x in range(0, 1080, 120)))


def bed_with_kid(x, y, st, flip=False):
    sc = .86
    body = f'<g transform="translate({x+40},{y+60}) rotate(-90) scale({sc})">{kid(st, "sleep")}</g>'
    return (f'<g><rect x="{x-20}" y="{y-80}" width="40" height="230" rx="10" fill="url(#woodG)" {S}/>'
            f'<rect x="{x}" y="{y}" width="430" height="120" rx="20" fill="#e9e4f4" {S}/>'
            f'<ellipse cx="{x+90}" cy="{y+6}" rx="80" ry="38" fill="#fff" {S}/>{body}'
            f'<path d="M{x+150},{y-30} Q{x+300},{y-60} {x+430},{y-20} L{x+430},{y+120} L{x+140},{y+120} Q{x+120},{y+40} {x+150},{y-30} Z" fill="{st["top"][0]}" {S}/>'
            f'<path d="M{x+170},{y+20} q120,-30 250,0" stroke="#fff" stroke-width="5" opacity=".4" fill="none"/>'
            + "".join(f'<circle cx="{x+190+i*50}" cy="{y+60+(i%2)*18}" r="7" fill="#fff" opacity=".5"/>' for i in range(5)) +
            f'<rect x="{x}" y="{y+120}" width="430" height="40" rx="8" fill="url(#woodG)" {S}/></g>')


def bg_kids_room():
    stars = "".join(f'<path d="M{x},{y} l4,10 10,4 -10,4 -4,10 -4,-10 -10,-4 10,-4 Z" fill="#fff7c2" opacity="{R.uniform(.4,.9):.2f}"/>' for x, y in ((R.randint(20, 1060), R.randint(40, 700)) for _ in range(40)))
    return (f'<rect width="1080" height="1920" fill="#1a1838"/>{stars}'
            f'<rect x="700" y="380" width="300" height="360" rx="14" fill="#0b1030" {S}/><circle cx="900" cy="470" r="48" fill="#f6f1d8"/><circle cx="880" cy="456" r="10" fill="#e3dcc0"/><circle cx="912" cy="490" r="7" fill="#e3dcc0"/>'
            f'<path d="M700,420 L300,1500 L760,1500 L1000,720 Z" fill="url(#beam)"/>'
            f'<path d="M60,300 Q300,360 540,300 Q780,360 1020,300" stroke="#e9d9ff" stroke-width="3" fill="none"/>'
            + "".join(f'<path d="M{80+i*120},{316+ (12 if i%2 else 0)} l40,0 -20,46 Z" fill="{("#ff8fb1","#ffd166","#5fc7a8","#8fbaff")[i%4]}" {S}/>' for i in range(8)) +
            f'<rect y="1500" width="1080" height="420" fill="#251f3e"/>'
            + bed_with_kid(70, 1040, KIDS[0]) + bed_with_kid(600, 1100, KIDS[1]) + bed_with_kid(70, 1380, KIDS[2]) + bed_with_kid(600, 1440, KIDS[3]) +
            f'<circle cx="540" cy="1880" r="26" fill="#ffd166" opacity=".9" filter="url(#blur2)"/><circle cx="540" cy="1880" r="80" fill="#ffd166" opacity=".15"/>')


def bg_hallway():
    return (f'<rect width="1080" height="1920" fill="#14152a"/><rect x="200" y="300" width="680" height="1200" fill="#1b1d38"/>'
            f'<path d="M200,300 L0,0 M880,300 L1080,0 M200,1500 L0,1920 M880,1500 L1080,1920" stroke="#262848" stroke-width="6"/>'
            f'<rect x="420" y="560" width="240" height="940" fill="#0d0e1e" {S}/><rect x="530" y="560" width="22" height="940" fill="#ffd98a" opacity=".8"/><path d="M530,1500 L420,1920 L680,1920 L552,1500 Z" fill="#ffd98a" opacity=".22"/>'
            + "".join(f'<g transform="translate({x},{y}) rotate({r})"><rect width="110" height="140" fill="#c9a96e" {S}/><rect x="10" y="10" width="90" height="120" fill="#3a3560"/><circle cx="55" cy="60" r="22" fill="#c48466"/></g>' for x, y, r in ((40, 640, -4), (900, 600, 5), (60, 860, 3)))
            + f'<rect y="1500" width="1080" height="420" fill="#1e1b30"/>')


def bg_bathroom():
    tiles = "".join(f'<rect x="{x}" y="{y}" width="88" height="88" fill="{"#262b45" if ((x+y)//90)%2 else "#2c3250"}"/>' for x in range(0, 1080, 90) for y in range(0, 1500, 90))
    return (f'<rect width="1080" height="1920" fill="#20243c"/>{tiles}'
            f'<ellipse cx="780" cy="380" rx="420" ry="320" fill="url(#bulb)"/><circle cx="780" cy="380" r="24" fill="#fff6d6" {S}/>'
            f'<rect x="548" y="418" width="464" height="884" rx="34" fill="#8a8fb0" {S}/><rect x="560" y="430" width="440" height="860" rx="26" fill="#2a2850"/>'
            f'<rect x="530" y="1310" width="500" height="70" rx="16" fill="#e9eef8" {S}/><ellipse cx="780" cy="1330" rx="130" ry="22" fill="#b9c3d6"/>'
            f'<rect x="590" y="1240" width="70" height="80" rx="10" fill="#8fbaff" {S}/>'
            + "".join(f'<rect x="{598+i*12}" y="{1200-(i%2)*14}" width="8" height="70" rx="4" fill="{c}"/>' for i, c in enumerate(("#9b1c32", "#ffd166", "#5fc7a8", "#ff8fb1", "#8fbaff")))
            + f'<rect y="1500" width="1080" height="420" fill="#181b30"/>')


BG = {"apartment_night": bg_apartment, "kitchen_night": bg_kitchen_night, "kids_room": bg_kids_room, "hallway": bg_hallway, "bathroom": bg_bathroom}


# ================================================================ overlays
def hud(day, pct, handle="@getfitwithme", label=None):
    s = (f'<g font-family="Anton"><rect x="44" y="104" width="252" height="132" rx="20" fill="#0c0918" opacity=".86" stroke="#ffffff22" stroke-width="2"/>'
         f'<text x="170" y="148" text-anchor="middle" font-size="26" fill="#cfc4ff" letter-spacing="4">DAY</text>'
         f'<text x="170" y="216" text-anchor="middle" font-size="68" fill="#ffd84d">{day}<tspan font-size="32" fill="#cfc4ff">/30</tspan></text>'
         f'<rect x="316" y="104" width="720" height="132" rx="20" fill="#0c0918" opacity=".86" stroke="#ffffff22" stroke-width="2"/>'
         f'<text x="676" y="148" text-anchor="middle" font-size="26" fill="#cfc4ff" letter-spacing="4">GLOW-UP</text>'
         f'<rect x="346" y="166" width="660" height="48" rx="24" fill="#2a2240"/><rect x="346" y="166" width="{max(48, 660*pct/100):.0f}" height="48" rx="24" fill="url(#hudBar)"/>'
         f'<text x="676" y="206" text-anchor="middle" font-size="40" fill="#fff">{pct}%</text></g>'
         f'<text x="1016" y="292" text-anchor="end" font-family="Inter" font-weight="800" font-size="24" fill="#fff" opacity=".7">{e(handle)}</text>')
    if label:
        s += (f'<g><rect x="44" y="258" width="{70 + len(label)*27}" height="78" rx="18" fill="#ffd84d" stroke="#1a0d33" stroke-width="4"/>'
              f'<text x="76" y="316" font-family="Anton" font-size="50" fill="#1a0d33">{e(label)}</text></g>')
    return s


def caption(text, y=1420):
    """TikTok-style bold caption; words in *stars* are highlighted yellow."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len((cur + " " + w).replace("*", "")) > 18 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    out = []
    for i, ln in enumerate(lines):
        spans = "".join(f'<tspan fill="{"#ffd84d" if "*" in w else "#fff"}">{e(w.replace("*", ""))} </tspan>' for w in ln.split())
        out.append(f'<text x="540" y="{y + i*92}" text-anchor="middle" font-family="Anton" font-size="84" stroke="#000" stroke-width="14" paint-order="stroke" letter-spacing="1">{spans}</text>')
    return "".join(out)


def mood(dark=.5, storm=False):
    s = ""
    if storm: s += rain()
    s += f'<rect width="1080" height="1920" fill="#0a1030" opacity="{dark*.35:.2f}"/><rect width="1080" height="1920" fill="url(#vig)" opacity="{min(1, dark+.3):.2f}"/>'
    return s


def frame(bg, people="", day=1, pct=0, label=None, cap=None, dark=.5, storm=False, extra=""):
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{CHAR_DEFS}{SCENE_DEFS}'
            f'{BG[bg]() if bg in BG else bg}{people}{extra}{mood(dark, storm)}{hud(day, pct, label=label)}{caption(cap) if cap else ""}</svg>')


def place_mom(b, outfit, pose, face, prop=None, x=540, foot=1690, scale=1.18, phones=False):
    return f'<g transform="translate({x - 230*scale},{foot - 905*scale}) scale({scale})">{danielle(b, outfit, pose, face, prop, phones)}</g>'


def place_kid(i, mood_, x, foot, scale=1.3):
    st = KIDS[i]; sc = scale * st["h"]
    return f'<g transform="translate({x - 100*sc},{foot - 385*sc}) scale({sc})">{kid(st, mood_)}</g>'
