#!/usr/bin/env python3
"""Fully animated Episode 1 of "30 Days to Her" — characters move, camera moves, captions pop, voiceover + sound design.
    python3 getfitwithme/_build/animate.py [--preview]"""
import html, json, math, os, random, re, subprocess, sys, tempfile, wave
import numpy as np
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import character as C  # noqa: E402
import scenes as Sc  # noqa: E402

e = html.escape
FPS, W, H, SR = 30, 1080, 1920, 44100
OUT = os.path.join(os.path.dirname(HERE), "series", "episode-01")
VOICES = os.environ.get("PIPER_VOICES", "/tmp/claude-0/-home-user-DigiByDK-shop/d44cb649-a423-501e-9be8-c37ee2c8ad5e/scratchpad/tts")
NARRATOR = os.path.join(VOICES, "voice-en-us-lessac-medium", "en-us-lessac-medium.onnx")


# ================================================================ helpers
def ease(t): t = max(0., min(1., t)); return t * t * (3 - 2 * t)
def back(t): t = max(0., min(1., t)); c = 1.9; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def kf(t, keys):
    """Keyframes [(time, value), ...] with smoothstep easing. Values may be numbers or tuples."""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            u = ease((t - t0) / (t1 - t0 or 1))
            return tuple(a + (b - a) * u for a, b in zip(v0, v1)) if isinstance(v0, tuple) else v0 + (v1 - v0) * u
    return keys[-1][1]


def cam(s, x, y):
    return f"translate(540,960) scale({s:.4f}) translate({-x:.1f},{-y:.1f})"


def mom(t, b, outfit, pose, face, x, foot, scale=1.18, prop=None, blink=False, talk=0., head_drop=None, prop_rot=0, breathe=1., sob=0., phones=False):
    br = 1 + .012 * math.sin(t * 2.6) * breathe
    dx = sob * 3.2 * math.sin(t * 38) ; dy = sob * 2.5 * abs(math.sin(t * 19))
    body = C.danielle(b, outfit, pose, face, prop, phones, blink, talk, head_drop, prop_rot)
    return (f'<g transform="translate({x - 230*scale + dx:.1f},{foot - 905*scale + dy:.1f}) scale({scale})">'
            f'<g transform="translate(230,905) scale({2-br:.4f},{br:.4f}) translate(-230,-905)">{body}</g></g>')


def kid_at(i, mood, x, foot, scale=1.3, talk=0., blink=False, bob=0.):
    st = C.KIDS[i]; sc = scale * st["h"]
    return f'<g transform="translate({x - 100*sc:.1f},{foot - 385*sc - bob:.1f}) scale({sc:.4f})">{C.kid(st, mood, talk, blink)}</g>'


def blinking(t, period=3.7, offset=0.):
    return ((t + offset) % period) < .13


R = random.Random(11)
RAIN = [(R.randint(-60, 1140), R.randint(0, 1920), R.uniform(.5, 1), R.choice((2, 2, 3))) for _ in range(260)]


def rain(t, op=.4):
    out = []
    for x, y, a, w in RAIN:
        yy = (y + t * 1900 * (0.8 + a * .4)) % 2000 - 60
        xx = x - (yy * .25) % 1140
        out.append(f'<line x1="{xx:.0f}" y1="{yy:.0f}" x2="{xx-14:.0f}" y2="{yy+58:.0f}" stroke="#b9cfff" stroke-width="{w}" opacity="{op*a:.2f}"/>')
    return "".join(out)


def sparkles(t, pts, scale=1.):
    out = []
    for i, (x, y) in enumerate(pts):
        a = .5 + .5 * math.sin(t * 5 + i * 1.7)
        s = (10 + 10 * a) * scale
        out.append(f'<path d="M{x},{y-s} L{x+s*.25},{y-s*.25} L{x+s},{y} L{x+s*.25},{y+s*.25} L{x},{y+s} L{x-s*.25},{y+s*.25} L{x-s},{y} L{x-s*.25},{y-s*.25} Z" fill="#fff" opacity="{.35+.65*a:.2f}"/>')
    return "".join(out)


def tears(t, cx, eye_y, n=3):
    out = []
    for k in range(n):
        for s_ in (-1, 1):
            ph = ((t * .9 + k / n + (0.37 if s_ > 0 else 0)) % 1)
            y = eye_y + 30 + ph ** 1.6 * 200
            out.append(f'<ellipse cx="{cx + s_*44 + s_*ph*10:.1f}" cy="{y:.1f}" rx="6" ry="9" fill="#a8e1ff" stroke="#4aa3d8" stroke-width="2" opacity="{1-ph:.2f}"/>')
    return "".join(out)


def vignette(dark):
    return f'<rect width="1080" height="1920" fill="#0a1030" opacity="{dark*.3:.2f}"/><rect width="1080" height="1920" fill="url(#vig)" opacity="{min(1, dark+.3):.2f}"/>'


# ================================================================ captions (CapCut style)
def timed_words(text, start, dur):
    words = text.split()
    weights = [len(re.sub(r"\W", "", w)) + 2 + (5 if re.search(r"[.,!?…]$", w) else 0) for w in words]
    tot = sum(weights); t = start; out = []
    for w, k in zip(words, weights):
        d = dur * k / tot; out.append((w, t, t + d)); t += d
    return out


def chunks(tw):
    out, cur = [], []
    for w in tw:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[.,!?…]$", w[0]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def caption_ui(T, all_chunks, y=1430, hl=("THIS", "HER", "DAY", "SUPERHERO", "CRYING", "EMPTY", "DRINKING", "YOU", "OVERWEIGHT", "DEPRESSED")):
    for ch in all_chunks:
        if ch[0][1] - .05 <= T <= ch[-1][2] + .15:
            spans = []
            for w, a, b_ in ch:
                active = a <= T < b_
                key = re.sub(r"\W", "", w).upper()
                col = "#ffd84d" if (active or key in hl) else "#ffffff"
                if active and key in hl: col = "#ff6fb5"
                spans.append(f'<tspan fill="{col}">{e(w.upper())} </tspan>')
            pop = 1 + .14 * max(0, 1 - (T - ch[0][1]) / .18)
            return (f'<g transform="translate(540,{y}) scale({pop:.3f})"><text x="0" y="0" text-anchor="middle" font-family="Anton" font-size="96" '
                    f'stroke="#000" stroke-width="16" paint-order="stroke" stroke-linejoin="round" letter-spacing="1">{"".join(spans)}</text></g>')
    return ""


# ================================================================ voice
def tts(text, path, length=1.12, silence=.35, speaker=None):
    args = [sys.executable, "-m", "piper", "-m", NARRATOR, "-f", path, "--length-scale", str(length), "--sentence-silence", str(silence)]
    if speaker is not None: args += ["-s", str(speaker)]
    subprocess.run(args, input=text.encode(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        sr = w.getframerate()
    a = resample_poly(a, SR, sr)
    nz = np.where(np.abs(a) > .02)[0]
    if len(nz): a = a[max(0, nz[0] - 800): nz[-1] + 2000]
    return a


def kidify(a, factor=1.2):
    """Pitch + speed up for a child voice."""
    return resample_poly(a, 100, int(100 * factor))


# ================================================================ sound design
def env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR))


class Mix:
    def __init__(s, dur): s.buf = np.zeros(int(dur * SR) + SR, dtype=np.float32)
    def add(s, t, a, g=1.):
        i = int(t * SR); j = min(len(s.buf), i + len(a))
        if j > i: s.buf[i:j] += a[:j - i] * g


rng = np.random.default_rng(3)


def noise(sec): return rng.standard_normal(int(sec * SR)).astype(np.float32)


def bandpass(a, lo, hi):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(4, [lo, hi], btype="band", fs=SR, output="sos"), a).astype(np.float32)


def lowpass(a, f):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(4, f, btype="low", fs=SR, output="sos"), a).astype(np.float32)


def sfx_thunder(): n = noise(3.5); return lowpass(n, 160) * env_exp(len(n), .9) * 2.2 + bandpass(n, 300, 2000) * env_exp(len(n), .12) * .4
def sfx_impact():
    t = np.arange(int(1.2 * SR)) / SR
    return (np.sin(2 * np.pi * (60 - 25 * t) * t) * np.exp(-t * 4) * .9 + lowpass(noise(1.2), 400) * np.exp(-t * 18) * .8).astype(np.float32)
def sfx_whoosh(sec=.6):
    n = noise(sec); t = np.arange(len(n)) / SR
    out = np.zeros_like(n)
    for k, f in enumerate(np.linspace(300, 4000, 8)):
        seg = slice(int(k * len(n) / 8), int((k + 1) * len(n) / 8))
        out[seg] = bandpass(n, f * .7, f * 1.3)[seg]
    return out * np.sin(np.pi * t / sec) * .7
def sfx_rewind(sec=1.2):
    t = np.arange(int(sec * SR)) / SR
    f = 1800 * np.exp(-t * 1.4) + 200 + 80 * np.sin(2 * np.pi * 18 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return ((np.sign(np.sin(ph)) * .25 + bandpass(noise(sec), 1500, 6000) * .4) * np.minimum(1, t * 8) * np.minimum(1, (sec - t) * 6)).astype(np.float32)
def sfx_heartbeat():
    t = np.arange(int(.35 * SR)) / SR
    th = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 18)
    out = np.zeros(int(.9 * SR), dtype=np.float32); out[:len(th)] += th; out[int(.22 * SR):int(.22 * SR) + len(th)] += th * .7
    return out
def sfx_rain(sec): n = noise(sec); return bandpass(n, 900, 7000) * .09 + lowpass(n, 300) * .04
def music_pad(sec, notes=(110, 130.8, 164.8), gain=.05):
    t = np.arange(int(sec * SR)) / SR
    sig = sum(np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t) for f in notes)
    return (sig * (1 + .25 * np.sin(2 * np.pi * .3 * t)) * gain).astype(np.float32)
def sfx_sparkle():
    t = np.arange(int(1.2 * SR)) / SR
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-(t - d).clip(0) * 6) * (t > d) for f, d in ((1760, 0), (2217, .08), (2637, .16), (3520, .24))).astype(np.float32) * .12


# ================================================================ backgrounds (static per shot)
def bg_stage():
    return ('<rect width="1080" height="1920" fill="#0b0618"/><rect y="1420" width="1080" height="500" fill="#1c1030"/>'
            '<ellipse cx="540" cy="1520" rx="460" ry="80" fill="#6d32d4" opacity=".35"/>'
            + "".join(f'<rect x="{x}" y="0" width="70" height="1420" fill="#2a1250" opacity=".55"/>' for x in (0, 70, 940, 1010))
            + '<text x="540" y="420" text-anchor="middle" font-family="Anton" font-size="120" fill="#6d32d4" opacity=".35" letter-spacing="14">DAY 30</text>')


def bg_black(): return '<rect width="1080" height="1920" fill="#07050f"/>'


# ================================================================ the episode
LINES = {
    "open": "In thirty days... she'll look like THIS.",
    "intro": "But on day one... this is Danielle. Single mom of four. Overweight. Depressed. And drinking every night... just to make it to tomorrow.",
    "kitchen": "The lights are getting cut off. The fridge is empty. Fourteen job rejections... and counting.",
    "kids": "Down the hall, four babies are sleeping. They still think their mommy is a superhero.",
    "hall": "Then... her little boy wakes up.",
    "boy": "Mommy... why you crying?",
    "mirror": "She walks to the mirror. She hasn't looked at herself in months. And for one second... she saw HER.",
    "title": "Thirty days. Four kids. One chance.",
    "choice": "And YOU control every move she makes. Comment one word. POUR IT OUT... or ONE MORE GLASS.",
}


def build(preview=False):
    tmp = tempfile.mkdtemp()
    os.makedirs(OUT, exist_ok=True)
    V = {k: tts(v, os.path.join(tmp, k + ".wav")) for k, v in LINES.items()}
    V["boy"] = kidify(tts(LINES["boy"], os.path.join(tmp, "boy.wav"), length=1.25, silence=.5), 1.22)
    vd = {k: len(a) / SR for k, a in V.items()}
    # shot list: (name, duration, voice cues [(key, offset)])
    shots = [
        ("open", max(3.8, vd["open"] + .9), [("open", .35)]),
        ("rewind", 1.3, []),
        ("intro", vd["intro"] + 1.4, [("intro", .5)]),
        ("kitchen", vd["kitchen"] + 1.0, [("kitchen", .4)]),
        ("kids", vd["kids"] + 1.0, [("kids", .4)]),
        ("hall", vd["hall"] + vd["boy"] + 2.6, [("hall", .3), ("boy", vd["hall"] + 1.5)]),
        ("mirror", vd["mirror"] + 1.6, [("mirror", .4)]),
        ("title", max(4.2, vd["title"] + 1.2), [("title", .5)]),
        ("choice", vd["choice"] + 2.2, [("choice", .6)]),
    ]
    starts, t = {}, 0.
    for name, d, _ in shots: starts[name] = t; t += d
    total = t
    # captions
    caps = []
    for name, d, cues in shots:
        for key, off in cues:
            caps += chunks(timed_words(LINES[key], starts[name] + off, vd[key]))
    # boy mouth from audio energy
    boy_env = np.array([np.sqrt(np.mean(V["boy"][int(i * SR / FPS):int((i + 1) * SR / FPS)] ** 2) + 1e-9) for i in range(int(vd["boy"] * FPS) + 1)])
    boy_env = np.clip(boy_env / (boy_env.max() + 1e-9) * 1.4, 0, 1)
    boy_t0 = starts["hall"] + vd["hall"] + 1.5

    # ---------------- audio mix
    M = Mix(total)
    for name, d, cues in shots:
        for key, off in cues: M.add(starts[name] + off, V[key], 1.0)
    M.add(0, music_pad(starts["rewind"], (220, 277.2, 329.6), .035))
    M.add(.95, sfx_impact(), .9); M.add(.9, sfx_sparkle(), 1)
    M.add(starts["rewind"], sfx_rewind(1.3), .9)
    rs, re_ = starts["intro"], starts["kids"]
    M.add(rs, sfx_rain(re_ - rs) * np.minimum(1, np.arange(int((re_ - rs) * SR)) / SR / .5).astype(np.float32), 1.)
    for lt in (rs + .9, rs + 6.2): M.add(lt, sfx_thunder(), .9)
    M.add(starts["intro"], music_pad(total - starts["intro"], (110, 130.8, 164.8), .03), 1)
    for s in ("intro", "kitchen", "kids", "hall", "mirror", "title", "choice"): M.add(starts[s] - .3, sfx_whoosh(), .6)
    for k in range(int(vd["mirror"] / .9) + 2): M.add(starts["mirror"] + .3 + k * .9, sfx_heartbeat(), .8)
    M.add(starts["mirror"] + vd["mirror"] * .72, sfx_sparkle(), 1.3)
    for k in range(3): M.add(starts["title"] + .45 + k * 1.05, sfx_impact(), .8)
    M.add(starts["choice"], sfx_impact(), .6)
    a = M.buf[:int(total * SR)]
    a = a / max(1, np.abs(a).max() / .95)
    wav = os.path.join(tmp, "mix.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())

    # ---------------- frames
    def frame(T):
        for name, d, _ in shots:
            if T < starts[name] + d: break
        t = T - starts[name]
        f = {"shot": name}
        fade_in = max(0, 1 - t / .35); fade_out = max(0, 1 - (d - t) / .3) if name not in ("open", "rewind") else 0
        ui = ""
        if name == "open":
            p = C.lerp_pose(C.pose_offsets("hip", 0), C.pose_offsets("flex", 0), (t - .45) / .5)
            z = kf(t, [(0, 1.0), (.9, 1.04), (1.05, 1.22), (3.8, 1.3)])
            beams = "".join(f'<path d="M{540 + 420*math.sin(t*1.3 + k*2.1):.0f},0 L{540 + 140*math.sin(t*1.3 + k*2.1) - 160:.0f},1500 L{540 + 140*math.sin(t*1.3 + k*2.1) + 160:.0f},1500 Z" fill="#c9a8ff" opacity=".13"/>' for k in range(3))
            fg = beams + mom(t, 0, "bra", p, "smirk" if t > .9 else "determined", 540, 1600, 1.2, blink=blinking(t, 2.9))
            fg += sparkles(t, [(250, 700), (840, 640), (200, 1100), (880, 1000), (540, 520), (300, 1400), (800, 1350)], 1.4 if t > .9 else .6)
            fg += f'<rect width="1080" height="1920" fill="#fff" opacity="{max(0, 1 - abs(t - 1.0) / .12) * .8:.2f}"/>'
            f["cam"] = cam(z, 540, 1050)
            ui = Sc.hud(30, 100, label=None) + f'<text x="540" y="380" text-anchor="middle" font-family="Anton" font-size="62" fill="#fff" opacity="{ease((t-.2)/.4):.2f}" stroke="#000" stroke-width="8" paint-order="stroke">FLASH FORWARD &gt;&gt;</text>'
            f["bg"] = "stage"
        elif name == "rewind":
            u = t / d
            day = max(1, round(30 - 29 * u)); pct = max(0, round(100 * (1 - u)))
            shift = int(40 * math.sin(t * 60))
            fg = (f'<g transform="translate({shift},0)" opacity=".85">{mom(0, 0, "bra", "flex", "smirk", 540, 1600, 1.2)}</g>'
                  f'<g transform="translate({-shift*2},0)" opacity=".5" style="mix-blend-mode:screen">{mom(0, 0, "bra", "flex", "smirk", 540, 1600, 1.2)}</g>'
                  + "".join(f'<rect y="{(k*137 + t*2400) % 1920:.0f}" width="1080" height="{R.randint(6, 26)}" fill="#fff" opacity=".18"/>' for k in range(14))
                  + '<rect width="1080" height="1920" fill="#6d32d4" opacity=".25"/>')
            f["cam"] = cam(1.1 + .1 * math.sin(t * 40), 540, 1000)
            ui = Sc.hud(day, pct) + ('<g opacity="%.2f"><text x="540" y="980" text-anchor="middle" font-family="Anton" font-size="170" fill="#fff" stroke="#000" stroke-width="14" paint-order="stroke">REWIND</text><path d="M300,780 l-90,50 90,50 Z M400,780 l-90,50 90,50 Z M680,780 l90,50 -90,50 Z" fill="#fff" stroke="#000" stroke-width="6" opacity="0"/><path d="M470,760 l-110,70 110,70 Z M600,760 l-110,70 110,70 Z" fill="#ffd84d" stroke="#000" stroke-width="8"/></g>' % (.6 + .4 * math.sin(t * 25)))
            f["bg"] = "black"
        elif name == "intro":
            # drink: raise bottle to mouth 3.0–5.2s, then sob
            base = C.pose_offsets("slump", 1)
            drink = {"L": base["L"], "R": ((-30, 70), (40, -40))}
            u = kf(t, [(0, 0), (2.8, 0), (3.5, 1), (5.0, 1), (5.7, 0)])
            p = C.lerp_pose(base, drink, u)
            crying = t > 5.8
            fg = mom(t, 1, "hoodie", p, "crying" if crying else ("sad" if u < .5 else "tired"), 540, 1700, prop="wine",
                     blink=(not crying) and blinking(t, 3.1), head_drop=kf(t, [(0, 16), (3.3, -4), (5.0, -4), (5.7, 16)]), prop_rot=-110 * u, sob=1 if crying else 0)
            if crying: fg += f'<g transform="translate({540-230*1.18:.0f},{1700-905*1.18:.0f}) scale(1.18)">{tears(t, 230, 186)}</g>'
            flash = max(0, 1 - abs(t - .9) / .15) + max(0, 1 - abs(t - 6.2) / .15) * .8
            fg += rain(t) + f'<rect width="1080" height="1920" fill="#dfe6ff" opacity="{flash*.55:.2f}"/>' + vignette(.5)
            z = kf(t, [(0, 1.0), (2.8, 1.08), (3.6, 1.38), (5.2, 1.38), (5.9, 1.12), (d, 1.18)])
            f["cam"] = cam(z, 540, kf(t, [(0, 1100), (2.8, 1050), (3.6, 760), (5.2, 760), (5.9, 1000)]))
            ui = Sc.hud(1, 0, label="DAY 1" if t > .3 else None)
            f["bg"] = "apartment"
        elif name == "kitchen":
            shake = 3 * math.sin(t * 31)
            p = C.pose_offsets("hold", 1); p = {"L": p["L"], "R": (p["R"][0], (p["R"][1][0] + shake, p["R"][1][1] + shake * .6))}
            crying = t > d * .55
            fg = mom(t, 1, "hoodie", p, "crying" if crying else "shocked", 380, 1720, prop="letter", blink=(not crying) and blinking(t, 2.7), sob=.6 if crying else 0)
            if crying: fg += f'<g transform="translate({380-230*1.18:.0f},{1720-905*1.18:.0f}) scale(1.18)">{tears(t, 230, 176)}</g>'
            ang = (t * 360 / 3) % 360
            fg += f'<line x1="720" y1="420" x2="{720 + 48*math.sin(math.radians(ang)):.1f}" y2="{420 - 48*math.cos(math.radians(ang)):.1f}" stroke="#e23b3b" stroke-width="3"/>'
            fl = .5 + .5 * (math.sin(t * 13) * math.sin(t * 7.3) > -.6)
            fg += f'<path d="M800,600 L0,1500 L0,1920 L800,1500 Z" fill="url(#fridgeBeam)" opacity="{fl*.6:.2f}"/>' + vignette(.42)
            f["cam"] = cam(kf(t, [(0, 1.9), (1.4, 1.9), (2.6, 1.05), (d, 1.1)]), kf(t, [(0, 520), (1.4, 520), (2.6, 540)]), kf(t, [(0, 1190), (1.4, 1190), (2.6, 1050)]))
            ui = Sc.hud(1, 0)
            f["bg"] = "kitchen"
        elif name == "kids":
            beds = [(70, 1040, 0), (600, 1100, 1), (70, 1380, 2), (600, 1440, 3)]
            fg = ""
            for k, (bx, by, i) in enumerate(beds):
                s = 1 + .025 * math.sin(t * 2.2 + k)
                fg += f'<g transform="translate({bx+280},{by+60}) scale(1,{s:.3f}) translate({-bx-280},{-by-60})">{Sc.bed_with_kid(bx, by, C.KIDS[i])}</g>'
                for z_ in range(2):
                    ph = (t * .45 + z_ * .5 + k * .23) % 1
                    fg += f'<text x="{bx+120 + ph*60:.0f}" y="{by-40 - ph*150:.0f}" font-family="Anton" font-size="{30+ph*20:.0f}" fill="#d9ccff" opacity="{(1-ph)*.9:.2f}">Z</text>'
            fg += sparkles(t, [(140, 220), (380, 140), (620, 260), (980, 180), (260, 560), (520, 430)], .8)
            fg += f'<circle cx="540" cy="1880" r="{90+12*math.sin(t*3):.0f}" fill="#ffd166" opacity=".16"/>' + vignette(.35)
            f["cam"] = cam(kf(t, [(0, 1.25), (d, 1.08)]), kf(t, [(0, 340), (d, 740)]), kf(t, [(0, 1150), (d, 1200)]))
            ui = Sc.hud(1, 0)
            f["bg"] = "kids"
        elif name == "hall":
            tb = vd["hall"] + 1.5
            walk = ease(t / 1.8)
            bx = 1180 - 380 * walk
            bob = 14 * abs(math.sin(t * 9)) * (1 if t < 1.8 else 0)
            bi = int((T - boy_t0) * FPS)
            talk = float(boy_env[bi]) if 0 <= bi < len(boy_env) else 0.
            after = t > tb + vd["boy"] + .1
            base = C.pose_offsets("slump", 1)
            wipe = {"L": base["L"], "R": ((-24, 96), (40, -40))}
            hug = {"L": ((-60, 40), (-104, 10)), "R": ((-60, 40), (-104, 10))}
            u_w = kf(t, [(0, 0), (tb - .6, 0), (tb, 1), (tb + vd["boy"], 1), (tb + vd["boy"] + .3, 0)])
            u_h = kf(t, [(0, 0), (tb + vd["boy"] + .2, 0), (tb + vd["boy"] + .8, 1)])
            p = C.lerp_pose(C.lerp_pose(base, wipe, u_w), hug, u_h)
            fg = mom(t, 1, "hoodie", p, "crying" if not after else "sad", 390, 1720, sob=0 if after else .8, head_drop=16 - 16 * u_h)
            if not after: fg += f'<g transform="translate({390-230*1.18:.0f},{1720-905*1.18:.0f}) scale(1.18)">{tears(t, 230, 186)}</g>'
            fg += kid_at(3, "sad", bx, 1740, 1.9, talk=talk, blink=blinking(t, 2.3, .5), bob=bob) + Sc.teddy(bx + 90, 1690 - bob, .75) + vignette(.4)
            if t < tb - .2: z, cx_, cy_ = kf(t, [(0, 1.05), (tb - .2, 1.15)]), 600, 1250
            elif t < tb + vd["boy"] + .2: z, cx_, cy_ = 1.75, bx - 10, 1420
            else: z, cx_, cy_ = kf(t, [(tb + vd["boy"] + .2, 1.55), (d, 1.25)]), 430, kf(t, [(tb + vd["boy"] + .2, 1000), (d, 1150)])
            f["cam"] = cam(z, cx_, cy_)
            ui = Sc.hud(1, 0)
            f["bg"] = "hall"
        elif name == "mirror":
            walk = ease(t / 1.6)
            mx = 120 + 180 * walk
            bob = 10 * abs(math.sin(t * 8)) * (1 if t < 1.6 else 0)
            reveal = ease((t - vd["mirror"] * .66) / .6)
            face = "shocked" if reveal > .3 else "sad"
            fg = f'<g clip-path="url(#mirrorClip)"><rect x="560" y="430" width="440" height="860" fill="url(#mirrorGlow)" opacity="{.15+.85*reveal:.2f}"/>'
            fg += f'<g opacity="{.12 + .78*reveal:.2f}" filter="url(#mirrorFx)">{mom(t, 0 if reveal > .05 else 1, "bra" if reveal > .05 else "hoodie", "flex" if reveal > .05 else "idle", "smirk" if reveal > .05 else "sad", 780, 1330, .86)}</g>'
            fg += sparkles(t, [(620, 520), (950, 600), (640, 900), (980, 1000), (720, 470), (860, 760)], reveal) + '<path d="M580,450 L700,450 L580,640 Z" fill="#fff" opacity=".12"/></g>'
            fg += f'<g transform="translate(0,{-bob:.1f})">{mom(t, 1, "hoodie", "idle", face, mx, 1740, 1.12, blink=blinking(t, 2.6))}</g>' + vignette(.32)
            fg += f'<rect width="1080" height="1920" fill="#b98cff" opacity="{max(0, 1 - abs(t - vd["mirror"]*.66 - .3)/.25)*.35:.2f}"/>'
            f["cam"] = cam(kf(t, [(0, 1.05), (vd["mirror"] * .6, 1.12), (vd["mirror"] * .75, 1.45), (d, 1.55)]), kf(t, [(0, 540), (vd["mirror"] * .6, 560), (vd["mirror"] * .75, 760)]), kf(t, [(0, 1100), (vd["mirror"] * .75, 900)]))
            ui = Sc.hud(1, 0)
            f["bg"] = "bathroom"
        elif name == "title":
            words = [("30 DAYS.", "#ffd84d"), ("4 KIDS.", "#ff8fb1"), ("1 CHANCE.", "#b98cff")]
            fg = f'<rect width="1080" height="1920" fill="url(#mirrorGlow)" opacity=".35"/>'
            for k, (w, col) in enumerate(words):
                t0 = .45 + k * 1.05
                if t >= t0:
                    s = 2.4 - 1.4 * back((t - t0) / .35)
                    fg += f'<g transform="translate(540,{700 + k*260}) scale({s:.3f})"><text text-anchor="middle" y="60" font-family="Anton" font-size="190" fill="{col}" stroke="#000" stroke-width="16" paint-order="stroke">{w}</text></g>'
            sh = sum(max(0, 1 - (t - (.45 + k * 1.05)) / .25) for k in range(3) if t >= .45 + k * 1.05)
            f["cam"] = f"translate({12*sh*math.sin(t*70):.1f},{10*sh*math.cos(t*60):.1f})"
            ui = Sc.hud(1, 0)
            f["bg"] = "black"
            f["nocap"] = True
        else:  # choice
            sl = back(t / .55)
            pourL = C.pose_offsets("hold", 1); raiseR = {"L": C.pose_offsets("hold", 1)["L"], "R": ((-30, 70), (40, -40))}
            uL = kf(t, [(0, 0), (d * .45, 0), (d * .65, 1)]); uR = kf(t, [(0, 0), (d * .7, 0), (d * .88, 1)])
            left = (f'<g transform="translate({-540*(1-sl):.1f},0)"><rect width="540" height="1920" fill="#123a4f"/><rect width="540" height="1920" fill="url(#vig)" opacity=".6"/>'
                    f'<g transform="translate(270,{620}) scale({1 + .05*math.sin(t*5):.3f})"><text text-anchor="middle" font-family="Anton" font-size="122" fill="#7fe0ff" stroke="#000" stroke-width="12" paint-order="stroke"><tspan x="0" y="0">POUR</tspan><tspan x="0" y="120">IT OUT</tspan></text></g>'
                    f'<text x="270" y="830" text-anchor="middle" font-family="Inter" font-weight="800" font-size="32" fill="#fff">Start Day 1 for real</text>'
                    + mom(t, 1, "hoodie", pourL, "determined", 270, 1720, .82, prop="wine", prop_rot=-150 * uL, blink=blinking(t, 2.4)) + '</g>')
            right = (f'<g transform="translate({540*(1-sl):.1f},0)"><rect x="540" width="540" height="1920" fill="#4a0f24"/><rect x="540" width="540" height="1920" fill="url(#vig)" opacity=".6"/>'
                     f'<g transform="translate(810,{620}) scale({1 + .05*math.sin(t*5+1.5):.3f})"><text text-anchor="middle" font-family="Anton" font-size="122" fill="#ff6f9f" stroke="#000" stroke-width="12" paint-order="stroke"><tspan x="0" y="0">ONE MORE</tspan><tspan x="0" y="120">GLASS</tspan></text></g>'
                     f'<text x="810" y="830" text-anchor="middle" font-family="Inter" font-weight="800" font-size="32" fill="#fff">I\'ll start tomorrow...</text>'
                     + mom(t, 1, "hoodie", C.lerp_pose(C.pose_offsets("hold", 1), raiseR, uR), "sad", 810, 1720, .82, prop="glass", blink=blinking(t, 2.9, 1)) + '</g>')
            if uL > .3:
                left += "".join(f'<ellipse cx="{300 + k*6:.0f}" cy="{1180 + ((t*2.2 + k*.17) % 1)*520:.0f}" rx="7" ry="12" fill="#8a1530" opacity=".85"/>' for k in range(6))
            pulse = 1 + .08 * math.sin(t * 7)
            fg = left + right + f'<rect x="532" y="360" width="16" height="{1400*sl:.0f}" fill="#ffd84d"/>'
            ui = (Sc.hud(1, 0) + f'<g transform="translate(540,440) scale({pulse:.3f})"><text text-anchor="middle" font-family="Anton" font-size="74" fill="#ffd84d" stroke="#000" stroke-width="12" paint-order="stroke" letter-spacing="4">COMMENT ONE WORD</text></g>'
                  f'<path d="M540,{1760 + 16*math.sin(t*8):.0f} l-40,-50 h80 Z" fill="#ffd84d" stroke="#000" stroke-width="6"/>')
            f["cam"] = ""
            f["bg"] = "black"
        if not f.get("nocap"): ui += caption_ui(T, caps)
        if fade_in or fade_out: ui += f'<rect width="1080" height="1920" fill="#000" opacity="{max(fade_in, fade_out):.2f}"/>'
        f["fg"] = fg; f["ui"] = ui
        return f

    bgs = {"stage": bg_stage(), "black": bg_black(), "apartment": Sc.bg_apartment(), "kitchen": Sc.bg_kitchen_night(),
           "kids": '<rect width="1080" height="1920" fill="#1a1838"/>' + Sc.bg_kids_room().split('<rect y="1500"')[0] + '<rect y="1500" width="1080" height="420" fill="#251f3e"/>',
           "hall": Sc.bg_hallway(), "bathroom": Sc.bg_bathroom()}
    nframes = int(total * FPS) if not preview else int(min(total, 6) * FPS)
    silent = os.path.join(tmp, "video.mp4")
    js = os.path.join(HERE, "anim_render.js")
    proc = subprocess.Popen(["node", js, silent, str(FPS)], stdin=subprocess.PIPE)
    head = {"defs": C.DEFS + Sc.SCENE_DEFS, "bgs": bgs}
    proc.stdin.write((json.dumps(head) + "\n").encode())
    for i in range(nframes):
        proc.stdin.write((json.dumps(frame(i / FPS)) + "\n").encode())
    proc.stdin.close(); proc.wait()
    out = os.path.join(OUT, "Episode-1-Day-1-ANIMATED.mp4" if not preview else "preview.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, f"{nframes/FPS:.1f}s", {k: round(v, 2) for k, v in starts.items()})
    # script
    lines = ["EPISODE 1 · DAY 1 · ROCK BOTTOM  (30 Days to Her)", ""]
    for name, d, cues in shots:
        for key, off in cues:
            s = starts[name] + off
            lines.append(f"[{int(s)//60}:{int(s)%60:02d}] {'LITTLE BROTHER' if key == 'boy' else 'NARRATOR'}: {LINES[key]}")
    lines += ["", "POST CAPTION:", "Day 1. Single mom of 4. Rock bottom. In 30 days she'll be unrecognizable, and YOU decide every move 💔 Comment POUR IT OUT or ONE MORE GLASS 👇🏽 #30DaysToHer #fyp #momlife #transformation #storytime",
              "", "PIN THIS COMMENT: Most comments wins. Episode 2 drops at 100 comments 💜"]
    open(os.path.join(OUT, "Episode-1-SCRIPT.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    build("--preview" in sys.argv)
