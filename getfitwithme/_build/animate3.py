#!/usr/bin/env python3
"""Episode 1 v3 — the doctor's 30 days, the kids' confrontation, male narrator, clean captions.
    python3 getfitwithme/_build/animate3.py [--preview SECONDS]"""
import json, math, os, re, subprocess, sys, tempfile, wave
import numpy as np
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import character as C  # noqa: E402
import scenes as Sc  # noqa: E402
import rooms as Rm  # noqa: E402
from animate import ease, back, kf, cam, mom, kid_at, blinking, rain, tears, vignette, timed_words, Mix, kidify, FPS, SR, e  # noqa: E402
from animate import sfx_thunder, sfx_impact, sfx_whoosh, sfx_heartbeat, sfx_rain, music_pad  # noqa: E402
from animate2 import humanize, darkness, sfx_click, sfx_crack, sfx_powerdown, sfx_sting  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "series", "episode-01")
VOICES = "/tmp/claude-0/-home-user-DigiByDK-shop/d44cb649-a423-501e-9be8-c37ee2c8ad5e/scratchpad/tts"
MALE = (os.path.join(VOICES, "voice-en-us-libritts-high", "en-us-libritts-high.onnx"), 523)
FEMALE = (os.path.join(VOICES, "voice-en-us-lessac-medium", "en-us-lessac-medium.onnx"), None)

# (key, speaker, text)
LINES = {
    "hook": ("N", "The doctor gave her thirty days."),
    "doctor": ("N", "Severe liver damage. Her eyes are already turning yellow. If she doesn't stop drinking... and change her whole life in thirty days... she may not live to see her kids grow up."),
    "drink": ("N", "So that night... what does she do? She drinks anyway."),
    "dark": ("N", "And then... the power gets cut off."),
    "scared": ("LS", "Mommy, I'm scared!"),
    "hungry": ("OS", "Mommy... I'm hungry."),
    "promise": ("TEEN", "You PROMISED you would stop!"),
    "trying": ("MOM", "I'm trying, baby... I'm trying."),
    "die": ("BOY", "Mommy... are you gonna die?"),
    "know": ("N", "Nobody told him about the doctor. But kids... always know."),
    "mirror": ("N", "Gray hair. Yellow eyes. A woman she doesn't even recognize. And four babies who need her alive."),
    "title": ("N", "Thirty days. Four kids. No more lies."),
    "choice": ("N", "So... does she tell her kids the truth about the doctor? Or does she keep it a secret? Comment TELL... or SECRET."),
}
WHO = {"N": "NARRATOR", "LS": "LITTLE SISTER", "OS": "OLDER SISTER", "TEEN": "OLDEST SISTER", "MOM": "DANIELLE", "BOY": "LITTLE BROTHER"}
HL = {"THIRTY", "30", "DOCTOR", "LIVER", "YELLOW", "DRINKING", "DRINKS", "ANYWAY", "POWER", "SCARED", "HUNGRY", "PROMISED", "STOP", "TRYING",
      "DIE", "KNOW", "GRAY", "ALIVE", "LIES", "TRUTH", "SECRET", "TELL", "KIDS"}


def piper(text, path, model, speaker, length=1.12, silence=.5, noise=.7, noise_w=.85):
    args = [sys.executable, "-m", "piper", "-m", model, "-f", path, "--length-scale", str(length), "--sentence-silence", str(silence),
            "--noise-scale", str(noise), "--noise-w-scale", str(noise_w)]
    if speaker is not None: args += ["-s", str(speaker)]
    subprocess.run(args, input=text.encode(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768; sr = w.getframerate()
    a = resample_poly(a, SR, sr)
    nz = np.where(np.abs(a) > .02)[0]
    return a[max(0, nz[0] - 800): nz[-1] + 2400] if len(nz) else a


def say(key, tmp):
    who, text = LINES[key]
    p = os.path.join(tmp, key + ".wav")
    if who == "N":
        a = piper(text, p, *MALE, length=1.16, silence=.55, noise=.68, noise_w=.8)
        a = resample_poly(a, 100, 94)  # a touch deeper
    elif who == "MOM": a = piper(text, p, *FEMALE, length=1.3, silence=.6, noise=.8, noise_w=1.0)
    elif who == "TEEN": a = kidify(piper(text, p, *FEMALE, length=.95, silence=.2, noise=.8), 1.1) * 1.3
    elif who == "LS": a = kidify(piper(text, p, *FEMALE, length=1.0, silence=.2), 1.34)
    elif who == "OS": a = kidify(piper(text, p, *FEMALE, length=1.15, silence=.3), 1.24)
    else: a = kidify(piper(text, p, *FEMALE, length=1.25, silence=.5), 1.22)
    return humanize(a)


def env_of(a):
    v = np.array([np.sqrt(np.mean(a[int(i * SR / FPS):int((i + 1) * SR / FPS)] ** 2) + 1e-9) for i in range(int(len(a) / SR * FPS) + 1)])
    return np.clip(v / (v.max() + 1e-9) * 1.4, 0, 1)


# ================================================================ UI
def hud(day, pct):
    return (f'<g opacity=".92"><rect x="40" y="88" width="236" height="64" rx="32" fill="#0c0918" fill-opacity=".72" stroke="#ffffff30" stroke-width="2"/>'
            f'<text x="158" y="133" text-anchor="middle" font-family="Anton" font-size="38" fill="#fff" letter-spacing="2">DAY <tspan fill="#ffd84d">{day}</tspan><tspan fill="#cfc4ff" font-size="26">/30</tspan></text>'
            f'<rect x="296" y="88" width="744" height="64" rx="32" fill="#0c0918" fill-opacity=".72" stroke="#ffffff30" stroke-width="2"/>'
            f'<text x="330" y="132" font-family="Anton" font-size="28" fill="#cfc4ff" letter-spacing="3">GLOW-UP</text>'
            f'<rect x="478" y="106" width="470" height="28" rx="14" fill="#2a2240"/><rect x="478" y="106" width="{max(28, 470*pct/100):.0f}" height="28" rx="14" fill="url(#hudBar)"/>'
            f'<text x="1004" y="131" text-anchor="middle" font-family="Anton" font-size="30" fill="#fff">{pct}%</text></g>')


def caption_groups(text, t0, dur, who):
    tw = timed_words(text, t0, dur)
    groups, cur = [], []
    for w in tw:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[.,!?…]$", w[0]) or sum(len(x[0]) for x in cur) > 14: groups.append((who, cur)); cur = []
    if cur: groups.append((who, cur))
    return groups


def captions(T, groups, y=1340):
    """Clean, centered, straight captions: one line, gentle pop, active word highlighted."""
    for who, g in groups:
        if g[0][1] - .03 <= T <= g[-1][2] + .1:
            spans = []
            for w, a, b_ in g:
                key = re.sub(r"\W", "", w).upper()
                active = a <= T < b_ + .05
                col = "#ffd84d" if active else ("#ff8fc4" if key in HL else "#ffffff")
                spans.append(f'<tspan fill="{col}">{e(w.upper())} </tspan>')
            pop = 1 + .06 * max(0, 1 - (T - g[0][1]) / .15)
            label = "" if who == "N" else (f'<g transform="translate(540,{y-112})"><rect x="-{len(WHO[who])*11+26}" y="-30" width="{len(WHO[who])*22+52}" height="42" rx="21" fill="#ff5fa8"/>'
                                            f'<text text-anchor="middle" y="1" font-family="Anton" font-size="28" fill="#fff" letter-spacing="2">{WHO[who]}</text></g>')
            return (label + f'<g transform="translate(540,{y}) scale({pop:.3f})"><text text-anchor="middle" font-family="Anton" font-size="86" '
                    f'stroke="#000" stroke-width="14" paint-order="stroke" stroke-linejoin="round" letter-spacing="1">{"".join(spans)}</text></g>')
    return ""


def ecg(t, x0, y0, w, h):
    pts = []
    for i in range(80):
        x = x0 + i * w / 79
        ph = ((i / 79) * 3 - t * 1.4) % 1
        y = y0 + (-h * .9 if .48 < ph < .5 else (h * .5 if .5 < ph < .53 else (-h * .2 if .44 < ph < .46 else 0)))
        pts.append(f"{x:.1f},{y:.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="#5fe39a" stroke-width="4"/><circle cx="{x0+w:.0f}" cy="{y0}" r="5" fill="#5fe39a"/>'


def sfx_beep():
    t = np.arange(int(.18 * SR)) / SR
    return (np.sin(2 * np.pi * 1000 * t) * np.minimum(1, (0.18 - t) * 40) * .35).astype(np.float32)


# ================================================================ build
def build(preview=None):
    tmp = tempfile.mkdtemp()
    os.makedirs(OUT, exist_ok=True)
    V = {k: say(k, tmp) for k in LINES}
    vd = {k: len(a) / SR for k, a in V.items()}
    EV = {k: env_of(V[k]) for k in ("scared", "hungry", "promise", "trying", "die")}
    shots = [
        ("hook", vd["hook"] + 2.6, [("hook", 1.2)]),
        ("doctor", vd["doctor"] + 1.2, [("doctor", .5)]),
        ("drink", vd["drink"] + vd["dark"] + 3.0, [("drink", .4), ("dark", vd["drink"] + 1.0)]),
        ("kids", vd["scared"] + vd["hungry"] + 2.2, [("scared", .6), ("hungry", .6 + vd["scared"] + .5)]),
        ("fight", vd["promise"] + vd["trying"] + 2.2, [("promise", .4), ("trying", .4 + vd["promise"] + .7)]),
        ("boy", vd["die"] + vd["know"] + 2.4, [("die", .5), ("know", .5 + vd["die"] + 1.0)]),
        ("mirror", vd["mirror"] + 2.0, [("mirror", .4)]),
        ("title", max(4.0, vd["title"] + 1.0), [("title", .45)]),
        ("choice", vd["choice"] + 2.8, [("choice", .5)]),
    ]
    starts, t = {}, 0.
    for name, d, _ in shots: starts[name] = t; t += d
    total = t
    cue_t = {key: starts[name] + off for name, d, cues in shots for key, off in cues}
    groups = []
    for name, d, cues in shots:
        if name in ("title",): continue
        for key, off in cues: groups += caption_groups(LINES[key][1], starts[name] + off, vd[key], LINES[key][0])

    def talk(key, T):
        i = int((T - cue_t[key]) * FPS)
        return float(EV[key][i]) if 0 <= i < len(EV[key]) else 0.

    # ---------------- sound
    M, MV = Mix(total), Mix(total)
    for key, s in cue_t.items(): MV.add(s, V[key], 1.0)
    for k in range(int(starts["doctor"] / .85) + 1): M.add(.2 + k * .85, sfx_beep(), .8)
    M.add(starts["doctor"] - .4, sfx_sting(), 1.0)
    for k in range(int(vd["doctor"] / .7) + 2): M.add(starts["doctor"] + k * .7, sfx_beep(), .25)
    M.add(starts["drink"], sfx_rain(starts["kids"] - starts["drink"] + 4), 1.)
    M.add(starts["drink"] + 1.2, sfx_thunder(), .7)
    M.add(starts["drink"], music_pad(starts["title"] - starts["drink"], (110, 130.8, 164.8), .03), 1)
    dk = starts["drink"] + vd["drink"] + .8
    M.add(dk, sfx_powerdown(), 1.2); M.add(dk + .1, sfx_thunder(), .9); M.add(dk + 1.6, sfx_click(), 1.)
    M.add(starts["fight"], sfx_sting(), .7)
    for k in range(int(vd["die"] / .8) + 3): M.add(starts["boy"] + .2 + k * .8, sfx_heartbeat(), 1.0)
    for s in ("drink", "kids", "boy", "mirror", "title", "choice"): M.add(starts[s] - .3, sfx_whoosh(), .45)
    M.add(starts["mirror"] + vd["mirror"] * .8, sfx_crack(), 1.3); M.add(starts["mirror"] + vd["mirror"] * .8, sfx_impact(), .7)
    for k in range(3): M.add(starts["title"] + .45 + k * 1.0, sfx_impact(), .9)
    M.add(starts["title"], music_pad(total - starts["title"], (110, 138.6, 164.8, 220), .045), 1)

    def write(a, path):
        a = a[:int(total * SR)]; a = a / max(1, np.abs(a).max() / .95)
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())
    wav, wav_nv = os.path.join(tmp, "mix.wav"), os.path.join(tmp, "nv.wav")
    write(M.buf * .7 + MV.buf, wav); write(M.buf * .6, wav_nv)

    KIDPOS = [(650, 1640), (770, 1650), (890, 1660), (990, 1690)]

    def frame(T):
        for name, d, _ in shots:
            if T < starts[name] + d: break
        t = T - starts[name]
        f = {"cam": "", "bg": "black"}
        fade_in = max(0, 1 - t / .3) if name not in ("hook", "kids") else 0
        fade_out = max(0, 1 - (d - t) / .25) if name not in ("hook", "drink", "title", "choice") else 0
        fg, ui = "", hud(1, 0)
        if name == "hook":
            fg = f'<rect x="140" y="760" width="800" height="260" rx="20" fill="#06120c" stroke="#1b2430" stroke-width="10"/>' + ecg(t, 170, 900, 740, 90)
            for k, (w, col, y, t0) in enumerate((("THE DOCTOR", "#ffffff", 560, 1.2), ("GAVE HER", "#ffffff", 690, 1.7), ("30 DAYS.", "#ffd84d", 1260, 2.3))):
                if t >= t0:
                    s = 2.0 - 1.0 * back((t - t0) / .3)
                    fg += f'<g transform="translate(540,{y}) scale({s:.3f})"><text text-anchor="middle" font-family="Anton" font-size="{190 if k == 2 else 130}" fill="{col}" stroke="#000" stroke-width="14" paint-order="stroke">{w}</text></g>'
            ui = ""; f["nocap"] = True
        elif name == "doctor":
            f["bg"] = "doctor"
            sh = 2.5 * math.sin(t * 29)
            p = C.pose_offsets("hold", 1); p = {"L": p["L"], "R": (p["R"][0], (p["R"][1][0] + sh, p["R"][1][1] + sh * .6))}
            crying = t > d * .62
            fg = mom(t, 1, "hoodie", p, "crying" if crying else ("shocked" if t > d * .25 else "sad"), 420, 1740, 1.15, prop="labs", sob=.5 if crying else 0, blink=(not crying) and blinking(t, 2.8))
            fg += ecg(t, 840, 500, 170, 40)
            if crying: fg += f'<g transform="translate({420-230*1.15:.0f},{1740-905*1.15:.0f}) scale(1.15)">{tears(t, 230, 186)}</g>'
            hx, hy_ = 420 + 66 * 1.15, 1740 - 513 * 1.15
            eyes_y = 1740 - (905 - 186) * 1.15
            z = kf(t, [(0, 2.0), (d * .22, 2.0), (d * .3, 2.4), (d * .55, 2.6), (d * .7, 1.3), (d, 1.15)])
            cx_ = kf(t, [(0, hx), (d * .22, hx), (d * .3, 420), (d * .7, 470)]); cy_ = kf(t, [(0, hy_), (d * .22, hy_), (d * .3, eyes_y), (d * .55, eyes_y), (d * .7, 1150)])
            f["cam"] = cam(z, cx_, cy_)
            fg += vignette(.2)
        elif name == "drink":
            f["bg"] = "apartment"
            tdk = vd["drink"] + .8
            base = C.pose_offsets("slump", 1); drink = {"L": base["L"], "R": ((-30, 70), (40, -40))}
            u = kf(t, [(0, 0), (vd["drink"] * .55, 0), (vd["drink"] * .75, 1), (tdk - .3, 1), (tdk, 0)])
            lights = 1 if t < tdk else (0 if t > tdk + .5 or (t - tdk) % .16 < .08 else 1)
            on_light = t > tdk + 1.6
            if on_light: fg = mom(t, 1, "hoodie", "phone", "shocked", 540, 1700, prop="phone")
            else: fg = mom(t, 1, "hoodie", C.lerp_pose(base, drink, u), "tired" if u > .5 else "sad", 540, 1700, prop="wine", prop_rot=-110 * u,
                           head_drop=16 - 20 * u, blink=blinking(t, 2.6))
            ph = (t % 1.3) / 1.3
            fg += f'<ellipse cx="770" cy="{110 + ph*1390:.0f}" rx="7" ry="12" fill="#9fc4ff" opacity="{.9 if ph < .97 else 0}"/>'
            fg += f'<g transform="translate(905,1500)"><path d="M-60,0 h120 l-14,90 h-92 Z" fill="#8a94b0" stroke="#2a161c" stroke-width="4"/><ellipse rx="60" ry="14" fill="#5a6a90" stroke="#2a161c" stroke-width="4"/></g>'
            if lights: fg += f'<rect x="56" y="896" width="268" height="158" fill="#fff" opacity="{(.35 + .25*math.sin(t*23)*math.sin(t*7))*.4:.2f}"/>'
            fg += rain(t, .32) + vignette(.4)
            fg += darkness(.94 * (1 - lights), [(610, 860, 430 + 25 * math.sin(t * 9))] if on_light else [])
            f["cam"] = cam(kf(t, [(0, 1.05), (vd["drink"] * .6, 1.1), (vd["drink"] * .8, 1.45), (tdk, 1.45), (tdk + .4, 1.15), (d, 1.3)]), 540,
                           kf(t, [(0, 1100), (vd["drink"] * .8, 780), (tdk, 780), (tdk + .4, 1000), (d, 920)]))
            if tdk < t < tdk + .6: f["cam"] += f" translate({10*math.sin(t*70):.1f},0)"
        elif name in ("kids", "fight", "boy"):
            f["bg"] = "kids_dark"
            kids_fg = ""
            for i, (kx, foot) in enumerate(KIDPOS):
                mood, tk, arms, sc = "sad", 0., None, 1.25
                if name == "kids":
                    tk = talk("scared", T) if i == 2 else (talk("hungry", T) if i == 1 else 0)
                if name == "fight" and i == 0:
                    step = ease(t / .5); kx -= 260 * step; foot += 40 * step; sc += .25 * step
                    mood, tk = "mad", talk("promise", T)
                    arms = [((-60, -6), (-114, -16)), ((-12, 50), (-10, 96))]
                if name == "boy" and i == 3:
                    step = ease(t / .6); kx -= 260 * step; foot += 40 * step; sc += .35 * step
                    tk = talk("die", T)
                shiver = 2 * math.sin(t * 30 + i)
                st = C.KIDS[i]; s_ = sc * st["h"]
                kids_fg += f'<g transform="translate({kx - 100*s_ + shiver:.1f},{foot - 385*s_:.1f}) scale({s_:.4f})">{C.kid(st, mood, tk, blinking(t, 2.4, i*.7) and tk < .05, arms)}</g>'
                if mood == "sad" and name != "fight":
                    for k in range(2):
                        ph = (t * .8 + k * .5 + i * .3) % 1
                        kids_fg += f'<ellipse cx="{kx - 30*s_/1.25 + shiver:.0f}" cy="{foot - 385*s_ + (110 + ph*90)*s_:.0f}" rx="5" ry="8" fill="#a8e1ff" opacity="{1-ph:.2f}"/>'
            if name == "kids":
                walk = ease(t / 1.6); mx = -180 + 400 * walk; bob = 12 * abs(math.sin(t * 9)) * (1 if t < 1.6 else 0)
                fg = kids_fg + f'<g transform="translate(0,{-bob:.1f})">{mom(t, 1, "hoodie", "phone", "shocked", mx, 1720, 1.15, prop="phone")}</g>'
                fg += darkness(.84, [(kf(t, [(0, 600), (d, 820)]), 1360, 430), (560, 520, 320), (mx + 60, 860, 240)])
                f["cam"] = cam(kf(t, [(0, 1.05), (d, 1.3)]), kf(t, [(0, 560), (d, 800)]), kf(t, [(0, 1250), (d, 1300)]))
            elif name == "fight":
                tt = .4 + vd["promise"] + .7
                cry = t > tt
                fg = kids_fg + mom(t, 1, "hoodie", "slump" if not cry else "face", "crying" if cry else "shocked", 240, 1720, 1.15, talk=talk("trying", T) if cry else 0, sob=1 if cry else 0)
                if cry: fg += f'<g transform="translate({240-230*1.15:.0f},{1720-905*1.15:.0f}) scale(1.15)">{tears(t, 230, 202)}</g>'
                fg += darkness(.78, [(600, 1250, 460), (300, 900, 330), (560, 520, 300)])
                if t < tt: z, cx_, cy_ = kf(t, [(0, 1.3), (.6, 1.75)]), kf(t, [(0, 600), (.6, 520)]), 1300
                else: z, cx_, cy_ = kf(t, [(tt, 1.6), (d, 1.8)]), 260, kf(t, [(tt, 950), (d, 900)])
                f["cam"] = cam(z, cx_, cy_)
                if t < .6: f["cam"] += f" translate({8*math.sin(t*60):.1f},0)"
            else:
                tk_ = .5 + vd["die"] + 1.0
                fg = kids_fg + mom(t, 1, "hoodie", "slump", "crying", 240, 1720, 1.15, sob=.8)
                fg += f'<g transform="translate({240-230*1.15:.0f},{1720-905*1.15:.0f}) scale(1.15)">{tears(t, 230, 192)}</g>'
                fg += darkness(.8, [(760, 1300, 420), (300, 900, 330)])
                if t < tk_ - .3: z, cx_, cy_ = kf(t, [(0, 1.4), (.8, 2.0)]), 740, 1340
                else: z, cx_, cy_ = kf(t, [(tk_ - .3, 1.8), (d, 1.4)]), kf(t, [(tk_ - .3, 300), (d, 420)]), kf(t, [(tk_ - .3, 900), (d, 1050)])
                f["cam"] = cam(z, cx_, cy_)
        elif name == "mirror":
            f["bg"] = "bathroom"
            crack_u = ease((t - vd["mirror"] * .8 - .4) / .5)
            refl = (f'<g clip-path="url(#mc3)" opacity=".6"><g transform="translate(1560,0) scale(-1,1)">{mom(t, 1, "hoodie", "idle", "sad", 780, 1330, .86, blink=blinking(t, 2.6))}</g>'
                    f'<rect x="560" y="410" width="440" height="880" fill="#6d32d4" opacity=".14"/></g>')
            crack = ""
            if crack_u > 0:
                paths = ["M760,700 L700,560 L640,520", "M760,700 L860,600 L960,560", "M760,700 L720,880 L600,1000", "M760,700 L880,860 L990,1020",
                         "M760,700 L780,500 L760,420", "M760,700 L640,720 L560,700", "M760,700 L900,720 L1000,760"]
                crack = "".join(f'<path d="{p}" stroke="#fff" stroke-width="5" fill="none" stroke-dasharray="600" stroke-dashoffset="{600*(1-crack_u):.0f}" opacity=".9"/>' for p in paths)
            flick = .85 + .15 * math.sin(t * 17) * math.sin(t * 5.3)
            fg = (f'<defs><clipPath id="mc3"><rect x="560" y="410" width="440" height="880" rx="26"/></clipPath></defs>{refl}{crack}'
                  f'<g transform="translate(560,1300)"><rect x="-22" y="-60" width="44" height="64" rx="6" fill="#f4ecd8" stroke="#2a161c" stroke-width="3"/>'
                  f'<path d="M0,-60 q{-6+4*math.sin(t*9):.1f},-20 0,-40 q{6+4*math.sin(t*7):.1f},20 0,40 Z" fill="#ffcf4a"/><circle cx="0" cy="-80" r="{240*flick:.0f}" fill="url(#candleG)" opacity=".9"/></g>')
            fg += mom(t, 1, "hoodie", "idle", "shocked" if crack_u > .2 else "sad", 290, 1740, 1.12, blink=blinking(t, 2.6))
            fg += f'<rect width="1080" height="1920" fill="#0a0820" opacity="{.5 - .2*flick:.2f}"/>' + vignette(.35)
            fg += f'<rect width="1080" height="1920" fill="#fff" opacity="{max(0, 1 - abs(t - vd["mirror"]*.8 - .4)/.12)*.6:.2f}"/>'
            eyes = 1740 - (905 - 186) * 1.12
            f["cam"] = cam(kf(t, [(0, 1.1), (vd["mirror"] * .3, 2.2), (vd["mirror"] * .55, 2.2), (vd["mirror"] * .75, 1.4), (d, 1.55)]),
                           kf(t, [(0, 520), (vd["mirror"] * .3, 290), (vd["mirror"] * .55, 290), (vd["mirror"] * .75, 700)]), kf(t, [(0, 1100), (vd["mirror"] * .3, eyes - 60), (vd["mirror"] * .55, eyes - 60), (vd["mirror"] * .75, 780)]))
            if 0 < crack_u < 1: f["cam"] += f" translate({10*math.sin(t*70):.1f},{8*math.cos(t*60):.1f})"
        elif name == "title":
            fg = '<rect width="1080" height="1920" fill="#2a1260" opacity=".35"/>'
            for k, (w, col) in enumerate((("30 DAYS.", "#ffd84d"), ("4 KIDS.", "#ff8fb1"), ("NO MORE LIES.", "#b98cff"))):
                t0 = .45 + k * 1.0
                if t >= t0:
                    s = 2.4 - 1.4 * back((t - t0) / .32)
                    fg += f'<g transform="translate(540,{720 + k*270}) scale({s:.3f})"><text text-anchor="middle" y="60" font-family="Anton" font-size="{200 if k < 2 else 150}" fill="{col}" stroke="#000" stroke-width="16" paint-order="stroke">{w}</text></g>'
            sh = sum(max(0, 1 - (t - (.45 + k)) / .25) for k in range(3) if t >= .45 + k)
            f["cam"] = f"translate({12*sh*math.sin(t*70):.1f},{10*sh*math.cos(t*60):.1f})"
            f["nocap"] = True
        else:  # choice: TELL vs SECRET
            sl = back(t / .55)
            hug = {"L": ((-60, 40), (-104, 10)), "R": ((-60, 40), (-104, 10))}
            hide = {"L": C.pose_offsets("idle", 1)["L"], "R": ((-10, 96), (60, 150))}
            uL = kf(t, [(0, 0), (d * .4, 0), (d * .55, 1)]); uR = kf(t, [(0, 0), (d * .6, 0), (d * .75, 1)])
            left = (f'<g transform="translate({-540*(1-sl):.1f},0)"><rect width="540" height="1920" fill="#123a4f"/><rect width="540" height="1920" fill="url(#vig)" opacity=".55"/>'
                    f'<g transform="translate(270,600) scale({1 + .05*math.sin(t*5):.3f})"><text text-anchor="middle" font-family="Anton" font-size="150" fill="#7fe0ff" stroke="#000" stroke-width="12" paint-order="stroke"><tspan x="0" y="0">TELL</tspan></text>'
                    f'<text text-anchor="middle" y="70" font-family="Anton" font-size="40" fill="#fff" stroke="#000" stroke-width="6" paint-order="stroke">the kids the truth</text></g>'
                    + mom(t, 1, "hoodie", C.lerp_pose(C.pose_offsets("idle", 1), hug, uL), "crying", 230, 1720, .78, sob=.4)
                    + kid_at(3, "sad", 420, 1730, 1.05) + '</g>')
            right = (f'<g transform="translate({540*(1-sl):.1f},0)"><rect x="540" width="540" height="1920" fill="#4a0f24"/><rect x="540" width="540" height="1920" fill="url(#vig)" opacity=".55"/>'
                     f'<g transform="translate(810,600) scale({1 + .05*math.sin(t*5+1.5):.3f})"><text text-anchor="middle" font-family="Anton" font-size="150" fill="#ff6f9f" stroke="#000" stroke-width="12" paint-order="stroke">SECRET</text>'
                     f'<text text-anchor="middle" y="70" font-family="Anton" font-size="40" fill="#fff" stroke="#000" stroke-width="6" paint-order="stroke">hide the doctor\'s news</text></g>'
                     + mom(t, 1, "hoodie", C.lerp_pose(C.pose_offsets("hold", 1), hide, uR), "smirk" if uR > .5 else "sad", 810, 1720, .82, prop="labs") + '</g>')
            pulse = 1 + .07 * math.sin(t * 7)
            fg = left + right + f'<rect x="532" y="420" width="16" height="{1320*sl:.0f}" fill="#ffd84d"/>'
            ui = hud(1, 0) + f'<g transform="translate(540,340) scale({pulse:.3f})"><text text-anchor="middle" font-family="Anton" font-size="78" fill="#ffd84d" stroke="#000" stroke-width="12" paint-order="stroke" letter-spacing="3">COMMENT ONE WORD</text></g>'
            if t > d - 1.7:
                a = ease((t - (d - 1.7)) / .4)
                ui += (f'<rect width="1080" height="1920" fill="#000" opacity="{.72*a:.2f}"/><g opacity="{a:.2f}"><text x="540" y="900" text-anchor="middle" font-family="Anton" font-size="96" fill="#fff" stroke="#000" stroke-width="12" paint-order="stroke">EPISODE 2</text>'
                       f'<text x="540" y="1030" text-anchor="middle" font-family="Anton" font-size="96" fill="#ffd84d" stroke="#000" stroke-width="12" paint-order="stroke">DEPENDS ON YOU</text></g>')
                f["nocap"] = True
        if not f.get("nocap"): ui += captions(T, groups)
        fo = max(fade_in, fade_out)
        if fo: ui += f'<rect width="1080" height="1920" fill="#000" opacity="{fo:.2f}"/>'
        f["fg"] = fg; f["ui"] = ui
        return f

    empty_beds = Rm.kids_room(lights_on=False)
    for x, k1, k2, q1, q2 in ((20, 0, 2, "quilt1", "quilt3"), (590, 1, 3, "quilt2", "quilt4")):
        empty_beds = empty_beds.replace(Rm.bunk_bed(x, C.KIDS[k1], C.KIDS[k2], q1, q2), Rm.bunk_bed(x, None, None, q1, q2))
    bgs = {"black": '<rect width="1080" height="1920" fill="#07050f"/>', "doctor": Rm.doctor_office(), "apartment": Rm.apartment(),
           "kids_dark": empty_beds, "bathroom": Rm.bathroom_candle()}
    if os.environ.get("DRY"):
        for i in range(0, int(total * FPS), 5): frame(i / FPS)
        print("dry ok", round(total, 1), {k: round(v, 1) for k, v in starts.items()}); return
    nframes = int((preview or total) * FPS)
    silent = os.path.join(tmp, "video.mp4")
    proc = subprocess.Popen(["node", os.path.join(HERE, "anim_render.js"), silent, str(FPS)], stdin=subprocess.PIPE)
    proc.stdin.write((json.dumps({"defs": C.DEFS + Sc.SCENE_DEFS + Rm.ROOM_DEFS, "bgs": bgs}) + "\n").encode())
    for i in range(nframes): proc.stdin.write((json.dumps(frame(i / FPS)) + "\n").encode())
    proc.stdin.close(); proc.wait()
    tag = "-preview" if preview else ""
    outs = [(wav, f"Episode-1-Day-1{tag}.mp4")] + ([] if preview else [(wav_nv, "Episode-1-Day-1-NO-VOICE.mp4")])
    for w_, name in outs:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", w_, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", os.path.join(OUT, name)], check=True)
    print("done", f"{nframes/FPS:.1f}s", {k: round(v, 1) for k, v in starts.items()}, flush=True)
    if not preview:
        lines = ["EPISODE 1 · DAY 1  (30 Days to Her)", "Narrator: deep, slow, serious. Kids: real and raw. Let the silences breathe.", ""]
        for key, s in sorted(cue_t.items(), key=lambda kv: kv[1]):
            lines.append(f"[{int(s)//60}:{int(s)%60:02d}] {WHO[LINES[key][0]]}: {LINES[key][1]}")
        lines += ["", "POST CAPTION:", "The doctor gave her 30 days 💔 Single mom of 4. Liver failing. Lights cut off. Her 6-year-old asked if she's gonna die. Should she TELL the kids the truth or keep it a SECRET? 👇🏽 #30DaysToHer #storytime #fyp #momlife",
                  "", "PIN THIS COMMENT: Most comments wins. Episode 2 drops at 100 comments 💜"]
        open(os.path.join(OUT, "Episode-1-SCRIPT.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    pv = float(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else None
    build(pv)
