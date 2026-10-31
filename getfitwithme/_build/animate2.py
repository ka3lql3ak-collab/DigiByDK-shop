#!/usr/bin/env python3
"""Episode 1 v2 — no spoilers, real drama: power outage, kids in the dark, the cracked mirror.
    python3 getfitwithme/_build/animate2.py [--preview SECONDS]"""
import json, math, os, re, subprocess, sys, tempfile, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import character as C  # noqa: E402
import scenes as Sc  # noqa: E402
import rooms as Rm  # noqa: E402
from animate import (ease, back, kf, cam, mom, kid_at, blinking, rain, tears, vignette, timed_words, Mix, noise, bandpass, lowpass,  # noqa: E402
                     sfx_thunder, sfx_impact, sfx_whoosh, sfx_heartbeat, sfx_rain, music_pad, tts, kidify, FPS, SR, e)

OUT = os.path.join(os.path.dirname(HERE), "series", "episode-01")

LINES = {
    "hook": "Danielle has thirty days to change her life... before she loses everything.",
    "intro": "Single mom. Four kids. Overweight. Depressed. And at two a.m.... the bottle is the only thing that listens.",
    "dark": "Then... the lights go out.",
    "notice": "Final notice. Power shut off. Fourteen job rejections... and now, this.",
    "mommy1": "Mommy?!",
    "mommy2": "Mommy, where are you?!",
    "kids": "She runs to her babies in the dark. All four of them... scared... and looking right at her.",
    "boy": "Mommy... why you crying?",
    "bottle": "She looks at the bottle in her hand. Then... at her kids.",
    "mirror": "She hasn't looked in a mirror in months. And tonight... she doesn't even recognize the woman staring back.",
    "title": "Thirty days. Four kids. One choice.",
    "choice": "You decide what she does next. Comment one word. POUR IT OUT... or ONE MORE GLASS.",
}
HL = {"THIRTY", "30", "EVERYTHING", "DEPRESSED", "BOTTLE", "LIGHTS", "OUT", "FINAL", "NOTICE", "MOMMY", "SCARED", "CRYING", "KIDS", "MIRROR",
      "RECOGNIZE", "CHOICE", "YOU", "POUR", "GLASS", "FOUR", "OVERWEIGHT", "BABIES", "LOSES"}


# ================================================================ voice: make it warmer + more human
def humanize(a):
    sos1 = butter(2, [120, 380], btype="band", fs=SR, output="sos")
    sos2 = butter(2, [2500, 5000], btype="band", fs=SR, output="sos")
    a = a + .35 * sosfilt(sos1, a) + .2 * sosfilt(sos2, a)               # warmth + presence
    a = np.tanh(a * 1.6) / np.tanh(1.6)                                  # gentle compression
    n = int(.45 * SR); ir = np.random.default_rng(5).standard_normal(n) * np.exp(-np.arange(n) / (.09 * SR)); ir[0] = 12
    wet = fftconvolve(a, ir)[:len(a)]; wet /= np.abs(wet).max() + 1e-9
    a = a / (np.abs(a).max() + 1e-9) * .9 + wet * .09                    # small room
    return a.astype(np.float32)


def voice(text, path, length=1.18, silence=.5, kid=None):
    a = tts(text, path, length=length, silence=silence)
    if kid: a = kidify(a, kid)
    return humanize(a)


# ================================================================ UI: slim HUD + giant captions
def hud(day, pct):
    return (f'<g opacity=".92"><rect x="40" y="88" width="236" height="64" rx="32" fill="#0c0918" fill-opacity=".72" stroke="#ffffff30" stroke-width="2"/>'
            f'<text x="158" y="133" text-anchor="middle" font-family="Anton" font-size="38" fill="#fff" letter-spacing="2">DAY <tspan fill="#ffd84d">{day}</tspan><tspan fill="#cfc4ff" font-size="26">/30</tspan></text>'
            f'<rect x="296" y="88" width="744" height="64" rx="32" fill="#0c0918" fill-opacity=".72" stroke="#ffffff30" stroke-width="2"/>'
            f'<text x="330" y="132" font-family="Anton" font-size="28" fill="#cfc4ff" letter-spacing="3">GLOW-UP</text>'
            f'<rect x="478" y="106" width="470" height="28" rx="14" fill="#2a2240"/><rect x="478" y="106" width="{max(28, 470*pct/100):.0f}" height="28" rx="14" fill="url(#hudBar)"/>'
            f'<text x="1004" y="131" text-anchor="middle" font-family="Anton" font-size="30" fill="#fff">{pct}%</text></g>')


def caption_groups(text, t0, dur):
    tw = timed_words(text, t0, dur)
    groups, cur = [], []
    for w in tw:
        cur.append(w)
        long_ = len(re.sub(r"\W", "", w[0])) > 7
        if len(cur) == 2 or long_ or re.search(r"[.,!?…]$", w[0]): groups.append(cur); cur = []
    if cur: groups.append(cur)
    return groups


def captions(T, groups, y=1260):
    for g in groups:
        if g[0][1] - .03 <= T <= g[-1][2] + .08:
            lines = []
            for w, a, b_ in g:
                key = re.sub(r"\W", "", w).upper()
                active = a <= T < b_ + .05
                col = "#ffd84d" if key in HL else "#ffffff"
                if active and key in HL: col = "#ff5fa8"
                lines.append((w.upper(), col, active, a))
            size = 150 if sum(len(l[0]) for l in lines) <= 9 else 118
            out = []
            gap = size * 1.08
            yy = y - (len(lines) - 1) * gap / 2
            for i, (w, col, active, a) in enumerate(lines):
                pop = 1 + .22 * max(0, 1 - (T - a) / .16)
                rot = -3 if i % 2 else 2
                out.append(f'<g transform="translate(540,{yy + i*gap:.0f}) scale({pop:.3f}) rotate({rot})"><text text-anchor="middle" font-family="Anton" font-size="{size}" fill="{col}" '
                           f'stroke="#000" stroke-width="20" paint-order="stroke" stroke-linejoin="round" style="filter:drop-shadow(0 8px 0 rgba(0,0,0,.45))">{e(w)}</text></g>')
            return "".join(out)
    return ""


def darkness(op, holes):
    """Dark overlay with soft light holes [(x, y, r)]."""
    if op <= 0: return ""
    cs = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#holeG)"/>' for x, y, r in holes)
    return (f'<defs><radialGradient id="holeG"><stop offset="0" stop-color="#000"/><stop offset=".55" stop-color="#000" stop-opacity=".85"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            f'<mask id="darkM"><rect width="1080" height="1920" fill="#fff"/>{cs}</mask></defs>'
            f'<rect width="1080" height="1920" fill="#02030a" opacity="{op:.2f}" mask="url(#darkM)"/>')


def sfx_click():
    t = np.arange(int(.08 * SR)) / SR
    return (bandpass(noise(.08), 1500, 6000) * np.exp(-t * 80)).astype(np.float32) * 1.5


def sfx_crack():
    n = noise(1.2); t = np.arange(len(n)) / SR
    pops = np.zeros_like(n)
    for k in range(9): i = int((.05 + k * .09) * SR); pops[i:i + 400] += np.hanning(400) * (1 - k / 10)
    return (bandpass(n, 2000, 9000) * pops * 3 + bandpass(n, 300, 2000) * np.exp(-t * 8) * .4).astype(np.float32)


def sfx_powerdown():
    t = np.arange(int(1.4 * SR)) / SR
    f = 120 * np.exp(-t * 2.2) + 30
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.5) * .6 + lowpass(noise(1.4), 200) * np.exp(-t * 3) * .4).astype(np.float32)


def sfx_sting():
    t = np.arange(int(2.5 * SR)) / SR
    return (sum(np.sin(2 * np.pi * f * t) for f in (73.4, 77.8, 146.8)) * np.exp(-t * 1.2) * .25 + lowpass(noise(2.5), 120) * np.exp(-t * 2) * .5).astype(np.float32)


# ================================================================ build
def build(preview=None):
    tmp = tempfile.mkdtemp()
    os.makedirs(OUT, exist_ok=True)
    V = {}
    for k, v in LINES.items():
        if k == "boy": V[k] = voice(v, os.path.join(tmp, k + ".wav"), 1.3, .6, kid=1.22)
        elif k == "mommy1": V[k] = voice(v, os.path.join(tmp, k + ".wav"), 1.0, .2, kid=1.34)
        elif k == "mommy2": V[k] = voice(v, os.path.join(tmp, k + ".wav"), .95, .2, kid=1.28)
        else: V[k] = voice(v, os.path.join(tmp, k + ".wav"))
    vd = {k: len(a) / SR for k, a in V.items()}
    shots = [
        ("hook", vd["hook"] + 1.6, [("hook", .9)]),
        ("intro", vd["intro"] + 1.0, [("intro", .4)]),
        ("dark", vd["dark"] + 2.4, [("dark", .2)]),
        ("notice", vd["notice"] + .8, [("notice", .4)]),
        ("mommy", 2.6, [("mommy1", .2), ("mommy2", 1.0)]),
        ("kids", vd["kids"] + vd["boy"] + 2.0, [("kids", .3), ("boy", vd["kids"] + 1.0)]),
        ("bottle", vd["bottle"] + 1.4, [("bottle", .4)]),
        ("mirror", vd["mirror"] + 2.0, [("mirror", .4)]),
        ("title", max(4.0, vd["title"] + 1.0), [("title", .45)]),
        ("choice", vd["choice"] + 2.6, [("choice", .5)]),
    ]
    starts, t = {}, 0.
    for name, d, _ in shots: starts[name] = t; t += d
    total = t
    groups = []
    for name, d, cues in shots:
        for key, off in cues:
            if key not in ("mommy1", "mommy2"): groups += caption_groups(LINES[key], starts[name] + off, vd[key])
    boy_env = np.array([np.sqrt(np.mean(V["boy"][int(i * SR / FPS):int((i + 1) * SR / FPS)] ** 2) + 1e-9) for i in range(int(vd["boy"] * FPS) + 1)])
    boy_env = np.clip(boy_env / (boy_env.max() + 1e-9) * 1.4, 0, 1)
    boy_t0 = starts["kids"] + vd["kids"] + 1.0

    # ---------------- sound
    M, MV = Mix(total), Mix(total)
    for name, d, cues in shots:
        for key, off in cues: MV.add(starts[name] + off, V[key], 1.0)
    for k in range(int(starts["intro"] / .95) + 1): M.add(.1 + k * .95, sfx_heartbeat(), 1.0)
    for lt in (.5, 1.6, 2.3): M.add(lt, sfx_thunder(), .8)
    M.add(starts["intro"] - .3, sfx_sting(), 1.0)
    M.add(starts["intro"], sfx_rain(starts["mommy"] - starts["intro"]), 1.)
    M.add(starts["intro"] + 2.0, sfx_thunder(), .7)
    M.add(starts["intro"], music_pad(starts["title"] - starts["intro"], (110, 130.8, 164.8), .03), 1)
    M.add(starts["dark"] + .9, sfx_powerdown(), 1.2); M.add(starts["dark"] + 1.0, sfx_thunder(), .9); M.add(starts["dark"] + 1.9, sfx_click(), 1.)
    M.add(starts["mommy"], sfx_sting(), .8)
    for s in ("notice", "kids", "bottle", "mirror", "title", "choice"): M.add(starts[s] - .3, sfx_whoosh(), .5)
    for k in range(int(vd["bottle"] / .8) + 2): M.add(starts["bottle"] + .2 + k * .8, sfx_heartbeat(), 1.0)
    M.add(starts["mirror"] + vd["mirror"] * .78, sfx_crack(), 1.3)
    M.add(starts["mirror"] + vd["mirror"] * .78, sfx_impact(), .7)
    for k in range(3): M.add(starts["title"] + .45 + k * 1.0, sfx_impact(), .9)
    M.add(starts["title"], music_pad(total - starts["title"], (110, 138.6, 164.8, 220), .045), 1)
    M.add(starts["choice"], sfx_impact(), .6)

    def write(a, path):
        a = a[:int(total * SR)]; a = a / max(1, np.abs(a).max() / .95)
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())
    wav, wav_nv = os.path.join(tmp, "mix.wav"), os.path.join(tmp, "nv.wav")
    write(M.buf * .75 + MV.buf, wav); write(M.buf * .6, wav_nv)

    # ---------------- frames
    MOM_K = dict(b=1, outfit="hoodie")

    def frame(T):
        for name, d, _ in shots:
            if T < starts[name] + d: break
        t = T - starts[name]
        f = {"cam": "", "bg": "black"}
        fade_in = max(0, 1 - t / .3) if name not in ("hook", "mommy", "dark") else 0
        fade_out = max(0, 1 - (d - t) / .25) if name not in ("hook", "dark", "title", "choice") else 0
        fg, ui = "", hud(1, 0)
        if name == "hook":
            flash = sum(max(0, 1 - abs(t - lt) / .12) for lt in (.5, 1.6, 2.3))
            f["bg"] = "apartment"
            fg = mom(t, 1, "hoodie", "slump", "crying", 540, 1700, prop="wine", sob=1) + rain(t, .5)
            fg += f'<rect width="1080" height="1920" fill="#000" opacity="{max(0, 1 - flash*1.4):.2f}"/><rect width="1080" height="1920" fill="#dfe6ff" opacity="{flash*.35:.2f}"/>'
            for k, (w, col, y, t0) in enumerate((("30 DAYS", "#ffd84d", 760, d - 2.4), ("TO CHANGE", "#ffffff", 930, d - 1.8), ("HER LIFE.", "#ff5fa8", 1070, d - 1.4))):
                if t >= t0:
                    s = 2.2 - 1.2 * back((t - t0) / .3)
                    fg += f'<g transform="translate(540,{y}) scale({s:.3f})"><text text-anchor="middle" font-family="Anton" font-size="170" fill="{col}" stroke="#000" stroke-width="16" paint-order="stroke">{w}</text></g>'
            sh = flash * 14
            f["cam"] = f"translate({sh*math.sin(t*80):.1f},{sh*math.cos(t*70):.1f})"
            ui = ""
            f["nocap"] = True
        elif name == "intro":
            f["bg"] = "apartment"
            base = C.pose_offsets("slump", 1); drink = {"L": base["L"], "R": ((-30, 70), (40, -40))}
            u = kf(t, [(0, 0), (d * .55, 0), (d * .68, 1), (d * .85, 1), (d * .95, 0)])
            crying = t < d * .5 or t > d * .9
            fg = mom(t, 1, "hoodie", C.lerp_pose(base, drink, u), "crying" if crying else "tired", 540, 1700, prop="wine", prop_rot=-110 * u,
                     head_drop=kf(t, [(0, 16), (d * .65, -4), (d * .85, -4), (d * .95, 16)]), sob=.9 if crying else 0, blink=(not crying) and blinking(t, 2.6))
            if crying: fg += f'<g transform="translate({540-230*1.18:.0f},{1700-905*1.18:.0f}) scale(1.18)">{tears(t, 230, 186)}</g>'
            ph = (t % 1.3) / 1.3
            fg += f'<ellipse cx="770" cy="{110 + ph*1390:.0f}" rx="7" ry="12" fill="#9fc4ff" opacity="{.9 if ph < .97 else 0}"/>'
            fg += f'<g transform="translate(905,1500)"><path d="M-60,0 h120 l-14,90 h-92 Z" fill="#8a94b0" stroke="#2a161c" stroke-width="4"/><ellipse cx="0" cy="0" rx="60" ry="14" fill="#5a6a90" stroke="#2a161c" stroke-width="4"/>'
            if ph > .97 or ph < .15: fg += f'<ellipse cx="0" cy="0" rx="{20 + 120*((ph+.03)%1):.0f}" ry="{5 + 20*((ph+.03)%1):.0f}" fill="none" stroke="#cfe0ff" stroke-width="3" opacity=".7"/>'
            fg += '</g>'
            tv = .35 + .25 * math.sin(t * 23) * math.sin(t * 7)
            fg += f'<rect x="56" y="896" width="268" height="158" fill="#fff" opacity="{tv*.4:.2f}"/><ellipse cx="190" cy="980" rx="320" ry="260" fill="#9fb4ff" opacity="{tv*.12:.2f}"/>'
            flash = max(0, 1 - abs(t - 2.0) / .15)
            fg += rain(t, .35) + f'<rect width="1080" height="1920" fill="#dfe6ff" opacity="{flash*.5:.2f}"/>' + vignette(.45)
            f["cam"] = cam(kf(t, [(0, 1.0), (d * .5, 1.1), (d * .66, 1.45), (d * .86, 1.45), (d, 1.15)]), 540, kf(t, [(0, 1100), (d * .5, 1050), (d * .66, 780), (d * .86, 780), (d, 1000)]))
            ui = hud(1, 0)
        elif name == "dark":
            f["bg"] = "apartment"
            fl = [(0.9, 1.0), (1.05, 0), (1.15, 1), (1.25, .2), (1.35, 1)]
            dk = 0
            for tt, v in fl:
                if t >= tt: dk = v
            on_light = t >= 1.9
            pose = C.pose_offsets("phone", 1) if on_light else C.pose_offsets("slump", 1)
            fg = mom(t, 1, "hoodie", pose, "shocked" if t > 1.0 else "crying", 540, 1700, prop="phone" if on_light else "wine", blink=False)
            fg += rain(t, .3)
            holes = [(610, 860, 420 + 30 * math.sin(t * 9))] if on_light else []
            fg += darkness(.94 * dk, holes)
            if on_light: fg += f'<path d="M600,880 L180,1920 L1080,1920 Z" fill="#fff6d0" opacity=".12"/>'
            f["cam"] = cam(kf(t, [(0, 1.05), (1.0, 1.05), (1.4, 1.25), (d, 1.35)]), 560, kf(t, [(0, 1050), (d, 900)]))
            if t > 1.0: f["cam"] += f" translate({8*math.sin(t*60)*max(0, 1-(t-1.0)/.5):.1f},0)"
            ui = hud(1, 0)
        elif name == "notice":
            f["bg"] = "kitchen"
            shake = 3 * math.sin(t * 31)
            p = C.pose_offsets("hold", 1); p = {"L": p["L"], "R": (p["R"][0], (p["R"][1][0] + shake, p["R"][1][1] + shake * .6))}
            fg = mom(t, 1, "hoodie", p, "crying" if t > d * .5 else "shocked", 380, 1720, prop="letter", sob=.5 if t > d * .5 else 0)
            fg += darkness(.9, [(kf(t, [(0, 470), (d, 430)]), kf(t, [(0, 1110), (d, 900)]), 360)])
            f["cam"] = cam(kf(t, [(0, 2.0), (d * .45, 1.8), (d, 1.25)]), kf(t, [(0, 470), (d, 450)]), kf(t, [(0, 1110), (d, 1000)]))
            if t < 2.0:  # stamp the notice text on screen
                ui += ""
        elif name == "mommy":
            f["bg"] = "black"
            sh = 18 * max(0, 1 - t / .5) + 10 * max(0, 1 - abs(t - 1.0) / .4)
            for k, (w, y0, t0, col) in enumerate((("MOMMY?!", 860, .2, "#ffffff"), ("MOMMY, WHERE", 1080, 1.0, "#ff5fa8"), ("ARE YOU?!", 1230, 1.0, "#ff5fa8"))):
                if t >= t0:
                    s = 1.9 - .9 * back((t - t0) / .25)
                    fg += f'<g transform="translate({540 + sh*math.sin(t*70+k):.1f},{y0}) scale({s:.3f})"><text text-anchor="middle" font-family="Anton" font-size="{170 if k == 0 else 120}" fill="{col}" stroke="#000" stroke-width="14" paint-order="stroke">{w}</text></g>'
            sx = 540 + 420 * math.sin(t * 2.4)
            fg = f'<ellipse cx="{sx:.0f}" cy="{1500 + 120*math.cos(t*1.7):.0f}" rx="260" ry="200" fill="#fff6d0" opacity=".10"/>' + fg
            ui = hud(1, 0)
        elif name == "kids":
            f["bg"] = "kids_dark"
            tb = vd["kids"] + 1.0
            walk = ease(t / 2.2)
            mx = -180 + 420 * walk
            bob = 12 * abs(math.sin(t * 9)) * (1 if t < 2.2 else 0)
            bi = int((T - boy_t0) * FPS); talk = float(boy_env[bi]) if 0 <= bi < len(boy_env) else 0.
            step = ease((t - (tb - .9)) / .7)
            kids_fg = ""
            for i, (kx, foot, scale) in enumerate(((640, 1640, 1.25), (760, 1650, 1.25), (880, 1660, 1.25), (980, 1690, 1.25))):
                if i == 3:
                    kx -= 220 * step; foot += 40 * step; scale += .35 * step
                shiver = 2 * math.sin(t * 30 + i)
                kids_fg += kid_at(i, "sad", kx + shiver, foot, scale, talk=talk if i == 3 else (.25 if t < tb else 0), blink=blinking(t, 2.4, i * .7))
            fg = kids_fg + f'<g transform="translate(0,{-bob:.1f})">{mom(t, 1, "hoodie", "phone", "crying", mx, 1720, 1.15, prop="phone", sob=.6)}</g>'
            beam_x = mx + 70
            fg += f'<path d="M{beam_x:.0f},900 L{820 + 60*math.sin(t*1.3):.0f},1250 L1080,1920 L{beam_x+140:.0f},1920 Z" fill="#fff6d0" opacity=".08"/>'
            fg += darkness(.82, [(kf(t, [(0, 600), (tb, 820), (d, 760)]), 1350, 420), (560, 520, 330), (mx + 60, 860, 250)])
            if t < tb - .2: z, cx_, cy_ = kf(t, [(0, 1.0), (tb - .2, 1.15)]), kf(t, [(0, 640), (tb - .2, 720)]), 1250
            elif t < tb + vd["boy"] + .3: z, cx_, cy_ = 1.85, 760 - 10, 1380
            else: z, cx_, cy_ = kf(t, [(tb + vd["boy"] + .3, 1.5), (d, 1.2)]), kf(t, [(tb + vd["boy"] + .3, 300), (d, 500)]), 1100
            f["cam"] = cam(z, cx_, cy_)
        elif name == "bottle":
            f["bg"] = "kids_dark"
            kids_fg = "".join(kid_at(i, "sad", kx, foot, 1.25 + (.35 if i == 3 else 0), blink=blinking(t, 2.4, i)) for i, (kx, foot) in enumerate(((640, 1640), (760, 1650), (880, 1660), (760, 1730))))
            fg = kids_fg + mom(t, 1, "hoodie", "hold", "sad", 240, 1720, 1.15, prop="wine", blink=blinking(t, 3))
            fg += darkness(.8, [(330, 1080, 300), (760, 1380, 380)])
            u = ease((t - d * .5) / .6)
            f["cam"] = cam(kf(t, [(0, 2.1), (d * .45, 2.2), (d * .62, 1.6), (d, 1.5)]), 330 + 430 * u, 1100 + 250 * u)
        elif name == "mirror":
            f["bg"] = "bathroom"
            crack_u = ease((t - vd["mirror"] * .78 - .4) / .5)
            refl = (f'<g clip-path="url(#mirrorClip2)" opacity=".55"><g transform="translate(1560,0) scale(-1,1)">{mom(t, 1, "hoodie", "idle", "sad", 780, 1330, .86, blink=blinking(t, 2.6))}</g>'
                    f'<rect x="560" y="410" width="440" height="880" fill="#6d32d4" opacity=".18"/></g>')
            crack = ""
            if crack_u > 0:
                paths = ["M760,700 L700,560 L640,520", "M760,700 L860,600 L960,560", "M760,700 L720,880 L600,1000", "M760,700 L880,860 L990,1020",
                         "M760,700 L780,500 L760,420", "M760,700 L640,720 L560,700", "M760,700 L900,720 L1000,760"]
                crack = "".join(f'<path d="{p}" stroke="#fff" stroke-width="5" fill="none" stroke-dasharray="600" stroke-dashoffset="{600*(1-crack_u):.0f}" opacity=".9"/>'
                                f'<path d="{p}" stroke="#2a161c" stroke-width="2" fill="none" stroke-dasharray="600" stroke-dashoffset="{600*(1-crack_u):.0f}"/>' for p in paths)
                crack += f'<circle cx="760" cy="700" r="{22*crack_u:.0f}" fill="#fff" opacity=".7"/>'
            flick = .85 + .15 * math.sin(t * 17) * math.sin(t * 5.3)
            fg = (f'<defs><clipPath id="mirrorClip2"><rect x="560" y="410" width="440" height="880" rx="26"/></clipPath></defs>{refl}{crack}'
                  f'<g transform="translate(560,1300)"><rect x="-22" y="-60" width="44" height="64" rx="6" fill="#f4ecd8" stroke="#2a161c" stroke-width="3"/>'
                  f'<path d="M0,-60 q{-6+4*math.sin(t*9):.1f},-20 0,-40 q{6+4*math.sin(t*7):.1f},20 0,40 Z" fill="#ffcf4a"/><circle cx="0" cy="-80" r="{240*flick:.0f}" fill="url(#candleG)" opacity=".9"/></g>')
            fg += mom(t, 1, "hoodie", "idle", "shocked" if crack_u > .2 else "sad", 290, 1740, 1.12, blink=blinking(t, 2.6))
            fg += f'<rect width="1080" height="1920" fill="#0a0820" opacity="{.55 - .2*flick:.2f}"/>' + vignette(.4)
            fg += f'<rect width="1080" height="1920" fill="#fff" opacity="{max(0, 1 - abs(t - vd["mirror"]*.78 - .4)/.12)*.6:.2f}"/>'
            z = kf(t, [(0, 1.05), (vd["mirror"] * .7, 1.2), (vd["mirror"] * .8, 1.55), (d, 1.6)])
            f["cam"] = cam(z, kf(t, [(0, 520), (vd["mirror"] * .8, 760)]), kf(t, [(0, 1100), (vd["mirror"] * .8, 760)]))
            if crack_u > 0 and crack_u < 1: f["cam"] += f" translate({10*math.sin(t*70):.1f},{8*math.cos(t*60):.1f})"
        elif name == "title":
            fg = '<rect width="1080" height="1920" fill="#2a1260" opacity=".35"/>'
            for k, (w, col) in enumerate((("30 DAYS.", "#ffd84d"), ("4 KIDS.", "#ff8fb1"), ("1 CHOICE.", "#b98cff"))):
                t0 = .45 + k * 1.0
                if t >= t0:
                    s = 2.4 - 1.4 * back((t - t0) / .32)
                    fg += f'<g transform="translate(540,{720 + k*270}) scale({s:.3f})"><text text-anchor="middle" y="60" font-family="Anton" font-size="200" fill="{col}" stroke="#000" stroke-width="16" paint-order="stroke">{w}</text></g>'
            sh = sum(max(0, 1 - (t - (.45 + k)) / .25) for k in range(3) if t >= .45 + k)
            f["cam"] = f"translate({12*sh*math.sin(t*70):.1f},{10*sh*math.cos(t*60):.1f})"
            f["nocap"] = True
        else:  # choice
            sl = back(t / .55)
            uL = kf(t, [(0, 0), (d * .45, 0), (d * .62, 1)]); uR = kf(t, [(0, 0), (d * .66, 0), (d * .84, 1)])
            raiseR = {"L": C.pose_offsets("hold", 1)["L"], "R": ((-30, 70), (40, -40))}
            left = (f'<g transform="translate({-540*(1-sl):.1f},0)"><rect width="540" height="1920" fill="#123a4f"/><rect width="540" height="1920" fill="url(#vig)" opacity=".6"/>'
                    f'<g transform="translate(270,600) scale({1 + .05*math.sin(t*5):.3f})"><text text-anchor="middle" font-family="Anton" font-size="128" fill="#7fe0ff" stroke="#000" stroke-width="12" paint-order="stroke"><tspan x="0" y="0">POUR</tspan><tspan x="0" y="124">IT OUT</tspan></text></g>'
                    + mom(t, 1, "hoodie", "hold", "determined", 270, 1720, .82, prop="wine", prop_rot=-150 * uL, blink=blinking(t, 2.4)) + '</g>')
            if uL > .3: left += "".join(f'<ellipse cx="{292 + k*5:.0f}" cy="{1190 + ((t*2.2 + k*.17) % 1)*500:.0f}" rx="7" ry="12" fill="#8a1530" opacity=".85"/>' for k in range(6))
            right = (f'<g transform="translate({540*(1-sl):.1f},0)"><rect x="540" width="540" height="1920" fill="#4a0f24"/><rect x="540" width="540" height="1920" fill="url(#vig)" opacity=".6"/>'
                     f'<g transform="translate(810,600) scale({1 + .05*math.sin(t*5+1.5):.3f})"><text text-anchor="middle" font-family="Anton" font-size="128" fill="#ff6f9f" stroke="#000" stroke-width="12" paint-order="stroke"><tspan x="0" y="0">ONE MORE</tspan><tspan x="0" y="124">GLASS</tspan></text></g>'
                     + mom(t, 1, "hoodie", C.lerp_pose(C.pose_offsets("hold", 1), raiseR, uR), "sad", 810, 1720, .82, prop="glass", blink=blinking(t, 2.9, 1)) + '</g>')
            pulse = 1 + .08 * math.sin(t * 7)
            fg = left + right + f'<rect x="532" y="500" width="16" height="{1240*sl:.0f}" fill="#ffd84d"/>'
            ui = (hud(1, 0) + f'<g transform="translate(540,400) scale({pulse:.3f})"><text text-anchor="middle" font-family="Anton" font-size="84" fill="#ffd84d" stroke="#000" stroke-width="12" paint-order="stroke" letter-spacing="3">COMMENT ONE WORD</text></g>')
            if t > d - 1.6:
                a = ease((t - (d - 1.6)) / .4)
                ui += (f'<rect width="1080" height="1920" fill="#000" opacity="{.7*a:.2f}"/><g opacity="{a:.2f}"><text x="540" y="900" text-anchor="middle" font-family="Anton" font-size="96" fill="#fff" stroke="#000" stroke-width="12" paint-order="stroke">EPISODE 2</text>'
                       f'<text x="540" y="1030" text-anchor="middle" font-family="Anton" font-size="96" fill="#ffd84d" stroke="#000" stroke-width="12" paint-order="stroke">DEPENDS ON YOU</text></g>')
            f["nocap_after"] = d - 1.6
        if not f.get("nocap") and not (f.get("nocap_after") and t > f["nocap_after"]): ui += captions(T, groups)
        fo = max(fade_in, fade_out)
        if fo: ui += f'<rect width="1080" height="1920" fill="#000" opacity="{fo:.2f}"/>'
        f["fg"] = fg; f["ui"] = ui
        return f

    bgs = {"black": '<rect width="1080" height="1920" fill="#07050f"/>', "apartment": Rm.apartment(), "kitchen": Rm.kitchen_dark(),
           "kids_dark": Rm.kids_room(lights_on=False).replace(Rm.bunk_bed(20, C.KIDS[0], C.KIDS[2], "quilt1", "quilt3"), Rm.bunk_bed(20, None, None, "quilt1", "quilt3"))
                                                     .replace(Rm.bunk_bed(590, C.KIDS[1], C.KIDS[3], "quilt2", "quilt4"), Rm.bunk_bed(590, None, None, "quilt2", "quilt4")),
           "bathroom": Rm.bathroom_candle()}
    nframes = int((preview or total) * FPS)
    silent = os.path.join(tmp, "video.mp4")
    proc = subprocess.Popen(["node", os.path.join(HERE, "anim_render.js"), silent, str(FPS)], stdin=subprocess.PIPE)
    proc.stdin.write((json.dumps({"defs": C.DEFS + Sc.SCENE_DEFS + Rm.ROOM_DEFS, "bgs": bgs}) + "\n").encode())
    for i in range(nframes): proc.stdin.write((json.dumps(frame(i / FPS)) + "\n").encode())
    proc.stdin.close(); proc.wait()
    tag = "" if not preview else "-preview"
    outs = [(wav, f"Episode-1-Day-1{tag}.mp4")] + ([] if preview else [(wav_nv, "Episode-1-Day-1-NO-VOICE.mp4")])
    for w_, name in outs:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", w_, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", os.path.join(OUT, name)], check=True)
    print("done", f"{nframes/FPS:.1f}s", {k: round(v, 2) for k, v in starts.items()})
    if not preview:
        lines = ["EPISODE 1 · DAY 1  (30 Days to Her)", "Read slow. Whisper the quiet lines. Let the pauses breathe.", ""]
        for name, d, cues in shots:
            for key, off in cues:
                s = starts[name] + off
                who = "KIDS (shouting)" if key.startswith("mommy") else ("LITTLE BROTHER" if key == "boy" else "NARRATOR")
                lines.append(f"[{int(s)//60}:{int(s)%60:02d}] {who}: {LINES[key]}")
        lines += ["", "POST CAPTION:", "Day 1. Single mom of 4. The lights just went out 💔 30 days to change her life, and YOU decide every move. Comment POUR IT OUT or ONE MORE GLASS 👇🏽 #30DaysToHer #fyp #storytime #momlife",
                  "", "PIN THIS COMMENT: Most comments wins. Episode 2 drops at 100 comments 💜"]
        open(os.path.join(OUT, "Episode-1-SCRIPT.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    pv = None
    if "--preview" in sys.argv: pv = float(sys.argv[sys.argv.index("--preview") + 1])
    build(pv)
