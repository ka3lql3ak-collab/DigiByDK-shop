#!/usr/bin/env python3
"""Episode 1 (extended, ~2:15) — morning secret, rejections, the collapse, the doctor, the walk home,
the blackout, the kids, the mirror, the choice and a cliffhanger. Everyone moves; narrator varies pace and pitch.
    python3 getfitwithme/_build/animate4.py [--preview SECONDS] ;  DRY=1 for a frame check"""
import json, math, os, re, subprocess, sys, tempfile, wave
import numpy as np
from scipy.signal import resample_poly, butter, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import character as C  # noqa: E402
import scenes as Sc  # noqa: E402
import rooms as Rm  # noqa: E402
from animate import ease, back, kf, cam, blinking, rain, tears, vignette, timed_words, Mix, kidify, noise, bandpass, lowpass, FPS, SR, e  # noqa: E402
from animate import sfx_thunder, sfx_impact, sfx_whoosh, sfx_heartbeat, sfx_rain, music_pad  # noqa: E402
from animate2 import darkness, sfx_click, sfx_crack, sfx_powerdown, sfx_sting  # noqa: E402
from animate3 import piper, env_of, hud, ecg, sfx_beep, MALE, FEMALE  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "series", "episode-01")
NARR = (MALE[0], 613)   # more expressive male speaker, natural pitch

LINES = {
    "hook": ("N", "The doctor gave her thirty days."),
    "morning": ("N", "But let's go back. Meet Danielle. Single mom of four. Every morning starts the same way. A pounding headache. Four hungry kids. And a secret... hidden in the kitchen cabinet."),
    "wine": ("TEEN", "Mom... is that wine?"),
    "juice": ("MOM", "It's juice, baby. Go get your shoes on."),
    "jobs": ("N", "She's been looking for work for months. Fourteen applications. Fourteen rejections. And the bills? They never stop coming."),
    "collapse": ("N", "Then, one Tuesday morning... right in front of her kids..."),
    "momscream": ("TEEN", "MOM!"),
    "doctor": ("N", "Two hours later, a doctor is holding her lab results. Severe liver damage. Her eyes are already turning yellow. If she doesn't stop drinking, and change her whole life in thirty days... she may not live to see her kids grow up."),
    "walk": ("N", "She walked home in the rain. She didn't call her sister. She didn't tell her kids. She told no one."),
    "drink": ("N", "And that night... what does she do? She drinks anyway."),
    "dark": ("N", "And then... the power gets cut off."),
    "scared": ("LS", "Mommy, I'm scared!"),
    "hungry": ("OS", "Mommy... I'm hungry."),
    "promise": ("TEEN", "You PROMISED you would stop! I found the bottles under your bed!"),
    "trying": ("MOM", "I'm trying, baby... I'm trying."),
    "die": ("BOY", "Mommy... are you gonna die?"),
    "know": ("N", "Nobody told him about the doctor. But kids... always know."),
    "hug": ("N", "She held him so tight... like he might disappear."),
    "mirror": ("N", "Gray hair. Yellow eyes. A woman she doesn't even recognize. And four babies who need her alive."),
    "whisper": ("MOM", "Thirty days. Okay... thirty days."),
    "title": ("N", "Thirty days. Four kids. No more lies."),
    "choice": ("N", "So... does she tell her kids the truth about the doctor? Or does she keep it a secret? Comment TELL... or SECRET."),
    "tease": ("N", "And tomorrow morning... somebody is knocking on her door."),
}
WHO = {"N": "NARRATOR", "LS": "LITTLE SISTER", "OS": "OLDER SISTER", "TEEN": "OLDEST SISTER", "MOM": "DANIELLE", "BOY": "LITTLE BROTHER"}
HL = {"THIRTY", "30", "DOCTOR", "LIVER", "YELLOW", "DRINKING", "DRINKS", "ANYWAY", "POWER", "SCARED", "HUNGRY", "PROMISED", "STOP", "TRYING", "SECRET", "WINE",
      "JUICE", "REJECTIONS", "COLLAPSED", "MOM", "DIE", "KNOW", "GRAY", "ALIVE", "LIES", "TRUTH", "TELL", "KIDS", "BOTTLES", "NO", "ONE", "KNOCKING", "DISAPPEAR"}


# ================================================================ voices
def clarity(a):
    sos = butter(2, [2200, 5500], btype="band", fs=SR, output="sos")
    a = a + .22 * sosfilt(sos, a)                          # presence, no muddy low end
    a = sosfilt(butter(2, 80, btype="high", fs=SR, output="sos"), a)
    a = np.tanh(a * 1.4) / np.tanh(1.4)
    return (a / (np.abs(a).max() + 1e-9) * .9).astype(np.float32)


def breath():
    n = noise(.32); t = np.arange(len(n)) / SR
    return (bandpass(n, 500, 3500) * np.sin(np.pi * t / .32) ** 2 * .05).astype(np.float32)


def narrate(text, tmp, key, rng):
    """Sentence by sentence with varied pace, pitch and pauses, plus soft breaths — less robotic."""
    parts = [p.strip() for p in re.findall(r"[^.?!]+(?:\.\.\.|[.?!])?", text) if p.strip()]
    out = []
    for i, p in enumerate(parts):
        a = piper(p, os.path.join(tmp, f"{key}_{i}.wav"), *NARR, length=float(rng.uniform(1.0, 1.12) + (.08 if p.endswith("...") else 0)),
                  silence=.15, noise=float(rng.uniform(.75, .9)), noise_w=float(rng.uniform(.85, 1.05)))
        f = float(rng.uniform(.975, 1.03))
        a = resample_poly(a, 1000, int(1000 * f))
        if i and rng.random() < .5: out.append(breath())
        out.append(a)
        out.append(np.zeros(int(SR * (rng.uniform(.28, .5) if p.endswith(("...", "?")) else rng.uniform(.14, .26))), dtype=np.float32))
    return clarity(np.concatenate(out))


def say(key, tmp, rng):
    who, text = LINES[key]
    p = os.path.join(tmp, key + ".wav")
    if who == "N": return narrate(text, tmp, key, rng)
    if who == "MOM": a = piper(text, p, *FEMALE, length=1.25, silence=.55, noise=.85, noise_w=1.0)
    elif who == "TEEN": a = kidify(piper(text, p, *FEMALE, length=.92 if key != "momscream" else .8, silence=.25, noise=.85), 1.1) * 1.35
    elif who == "LS": a = kidify(piper(text, p, *FEMALE, length=1.0, silence=.2), 1.34)
    elif who == "OS": a = kidify(piper(text, p, *FEMALE, length=1.15, silence=.3), 1.24)
    else: a = kidify(piper(text, p, *FEMALE, length=1.25, silence=.5), 1.22)
    return clarity(a)


# ================================================================ living characters
def alive(pose, b, t, amp=1.0, ph=0.0, gesture=0.0):
    p = pose if isinstance(pose, dict) else C.pose_offsets(pose, b)
    out = {}
    for k, s in (("L", 1), ("R", -1)):
        (ex, ey), (hx, hy) = p[k]
        w = t * 1.7 + ph + (0 if k == "L" else 1.3)
        dx, dy = 5 * amp * math.sin(w), 4 * amp * math.cos(w * .8)
        if k == "R" and gesture > 0:  # talking hand
            g = gesture * (.6 + .4 * math.sin(t * 7 + ph))
            ex, ey, hx, hy = ex - 18 * g, ey - 30 * g, hx - 46 * g, hy - 70 * g
        out[k] = ((ex + dx * .5, ey + dy * .5), (hx + dx, hy + dy))
    return out


def mom(t, pose, face, x, foot, scale=1.15, prop=None, talk=0., sob=0., blink=None, head_drop=None, prop_rot=0, b=1, outfit="hoodie", amp=1., ph=0., fall=0.):
    p = alive(pose, b, t, amp, ph, gesture=min(1, talk * 1.6))
    head_rot = 3 * math.sin(t * 1.1 + ph) * amp + talk * 4 * math.sin(t * 8)
    if blink is None: blink = blinking(t, 3.1, ph) and talk < .05 and face not in ("crying",)
    br = 1 + .012 * math.sin(t * 2.6 + ph)
    dx = sob * 3.2 * math.sin(t * 38); dy = sob * 2.5 * abs(math.sin(t * 19))
    sway = 1.2 * math.sin(t * .9 + ph) * amp
    body = C.danielle(b, outfit, p, face, prop, False, blink, talk, head_drop, prop_rot, head_rot)
    rot = sway - 86 * fall
    return (f'<g transform="translate({x - 230*scale + dx:.1f},{foot - 905*scale + dy:.1f}) scale({scale})">'
            f'<g transform="rotate({rot:.2f} 230 905) translate(230,905) scale({2-br:.4f},{br:.4f}) translate(-230,-905)">{body}</g></g>')


def kid(i, mood, x, foot, scale=1.25, t=0., talk=0., arms=None, walk=0., amp=1.):
    st = C.KIDS[i]; s = scale * st["h"]
    if arms is None:
        a = 6 * math.sin(t * 2.1 + i) * amp
        arms = [((-12 + a * .4, 50), (-10 + a, 96 - a * .5)), ((-12 - a * .4, 50), (-10 - a, 96 + a * .5))]
        if talk > .05: arms[1] = ((-40, 10 - 20 * talk), (-60, -30 - 40 * talk))
    bob = 14 * abs(math.sin(t * 10)) * walk
    rot = 2 * math.sin(t * 1.4 + i * 1.7) * amp + 4 * math.sin(t * 10) * walk
    body = C.kid(st, mood, talk, blinking(t, 2.4, i * .7) and talk < .05, arms)
    return (f'<g transform="translate({x - 100*s:.1f},{foot - 385*s - bob:.1f}) scale({s:.4f})"><g transform="rotate({rot:.2f} 100 380)">{body}</g></g>')


def tears_at(t, x, foot, scale, head_drop=16):
    return f'<g transform="translate({x-230*scale:.0f},{foot-905*scale:.0f}) scale({scale})">{tears(t, 230, 176 + head_drop)}</g>'


# ================================================================ captions (clean, centered)
def groups_for(text, t0, dur, who):
    tw = timed_words(text, t0, dur)
    groups, cur = [], []
    for w in tw:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[.,!?…]$", w[0]) or sum(len(x[0]) for x in cur) > 14: groups.append((who, cur)); cur = []
    if cur: groups.append((who, cur))
    return groups


def captions(T, groups, y=1340):
    for who, g in groups:
        if g[0][1] - .03 <= T <= g[-1][2] + .1:
            spans = []
            for w, a, b_ in g:
                key = re.sub(r"\W", "", w).upper()
                col = "#ffd84d" if a <= T < b_ + .05 else ("#ff8fc4" if key in HL else "#ffffff")
                spans.append(f'<tspan fill="{col}">{e(w.upper())} </tspan>')
            pop = 1 + .06 * max(0, 1 - (T - g[0][1]) / .15)
            label = "" if who == "N" else (f'<g transform="translate(540,{y-112})"><rect x="-{len(WHO[who])*11+26}" y="-30" width="{len(WHO[who])*22+52}" height="42" rx="21" fill="#ff5fa8"/>'
                                            f'<text text-anchor="middle" y="1" font-family="Anton" font-size="28" fill="#fff" letter-spacing="2">{WHO[who]}</text></g>')
            return (label + f'<g transform="translate(540,{y}) scale({pop:.3f})"><text text-anchor="middle" font-family="Anton" font-size="86" '
                    f'stroke="#000" stroke-width="14" paint-order="stroke" stroke-linejoin="round" letter-spacing="1">{"".join(spans)}</text></g>')
    return ""


def stamp(text, t, t0, x, y, rot):
    if t < t0: return ""
    s = 2.2 - 1.2 * back((t - t0) / .22)
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s:.3f})"><rect x="-230" y="-70" width="460" height="120" rx="10" fill="none" stroke="#e23b3b" stroke-width="12"/>'
            f'<text text-anchor="middle" y="28" font-family="Anton" font-size="96" fill="#e23b3b" letter-spacing="6">{text}</text></g>')


def sfx_knock():
    out = np.zeros(int(1.6 * SR), dtype=np.float32)
    for k, tt in enumerate((0, .32, .64)):
        n = int(.12 * SR); t = np.arange(n) / SR
        hit = (lowpass(noise(.12), 260) * np.exp(-t * 40) * 2.4 + np.sin(2 * np.pi * 90 * t) * np.exp(-t * 30)).astype(np.float32)
        i = int(tt * SR); out[i:i + n] += hit
    return out


def sfx_thud():
    t = np.arange(int(.5 * SR)) / SR
    return (np.sin(2 * np.pi * 70 * t) * np.exp(-t * 12) + lowpass(noise(.5), 300) * np.exp(-t * 20)).astype(np.float32)


# ================================================================ build
def build(preview=None):
    tmp = tempfile.mkdtemp()
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(8)
    V = {k: say(k, tmp, rng) for k in LINES}
    vd = {k: len(a) / SR for k, a in V.items()}
    EV = {k: env_of(V[k]) for k in LINES if LINES[k][0] != "N"}
    S_ = [
        ("hook", vd["hook"] + 2.6, [("hook", 1.2)]),
        ("morning", vd["morning"] + vd["wine"] + vd["juice"] + 2.4, [("morning", .4), ("wine", vd["morning"] + .9), ("juice", vd["morning"] + vd["wine"] + 1.4)]),
        ("jobs", vd["jobs"] + 1.0, [("jobs", .4)]),
        ("collapse", vd["collapse"] + vd["momscream"] + 3.2, [("collapse", .3), ("momscream", vd["collapse"] + 1.4)]),
        ("doctor", vd["doctor"] + 1.2, [("doctor", .5)]),
        ("walk", vd["walk"] + 1.2, [("walk", .5)]),
        ("drink", vd["drink"] + vd["dark"] + 3.0, [("drink", .4), ("dark", vd["drink"] + 1.0)]),
        ("kids", vd["scared"] + vd["hungry"] + 2.4, [("scared", .8), ("hungry", .8 + vd["scared"] + .5)]),
        ("fight", vd["promise"] + vd["trying"] + 2.4, [("promise", .5), ("trying", .5 + vd["promise"] + .7)]),
        ("boy", vd["die"] + vd["know"] + vd["hug"] + 3.4, [("die", .6), ("know", .6 + vd["die"] + 1.0), ("hug", .6 + vd["die"] + vd["know"] + 1.6)]),
        ("mirror", vd["mirror"] + vd["whisper"] + 2.6, [("mirror", .4), ("whisper", vd["mirror"] + 1.4)]),
        ("title", max(4.0, vd["title"] + 1.0), [("title", .45)]),
        ("choice", vd["choice"] + 1.4, [("choice", .5)]),
        ("tease", vd["tease"] + 3.0, [("tease", 1.4)]),
    ]
    starts, t = {}, 0.
    for name, d, _ in S_: starts[name] = t; t += d
    total = t
    cue = {key: starts[name] + off for name, d, cues in S_ for key, off in cue_list} if False else {key: starts[name] + off for name, d, cl in S_ for key, off in cl}
    groups = []
    for name, d, cl in S_:
        if name == "title": continue
        for key, off in cl: groups += groups_for(LINES[key][1], starts[name] + off, vd[key], LINES[key][0])

    def talk(key, T):
        if key not in EV: return 0.
        i = int((T - cue[key]) * FPS)
        return float(EV[key][i]) if 0 <= i < len(EV[key]) else 0.

    # ---------------- sound
    M, MV = Mix(total), Mix(total)
    for key, s in cue.items(): MV.add(s, V[key], 1.0)
    for k in range(int(starts["morning"] / .85) + 1): M.add(.2 + k * .85, sfx_beep(), .8)
    M.add(starts["morning"] - .4, sfx_sting(), .9)
    M.add(starts["morning"], music_pad(starts["collapse"] - starts["morning"], (130.8, 164.8, 196), .025), 1)
    M.add(cue["wine"] - .2, sfx_sting(), .6)
    for k in range(3): M.add(starts["jobs"] + vd["jobs"] * (.32 + k * .14), sfx_thud(), 1.2)
    for k in range(int((starts["doctor"] - starts["collapse"]) / .7)): M.add(starts["collapse"] + k * .7, sfx_heartbeat(), .9 + k * .05)
    M.add(starts["collapse"] + vd["collapse"] + .9, sfx_thud(), 1.6); M.add(starts["collapse"] + vd["collapse"] + .9, sfx_impact(), .8)
    M.add(starts["doctor"] - .4, sfx_sting(), 1.0)
    for k in range(int(vd["doctor"] / .7) + 2): M.add(starts["doctor"] + k * .7, sfx_beep(), .22)
    M.add(starts["walk"], sfx_rain(starts["kids"] - starts["walk"] + 4), 1.)
    M.add(starts["walk"] + 2.0, sfx_thunder(), .6); M.add(starts["drink"] + 1.2, sfx_thunder(), .7)
    M.add(starts["doctor"], music_pad(starts["title"] - starts["doctor"], (110, 130.8, 164.8), .03), 1)
    dk = starts["drink"] + vd["drink"] + .8
    M.add(dk, sfx_powerdown(), 1.2); M.add(dk + .1, sfx_thunder(), .9); M.add(dk + 1.6, sfx_click(), 1.)
    M.add(starts["fight"], sfx_sting(), .7)
    for k in range(int(vd["die"] / .8) + 3): M.add(starts["boy"] + .2 + k * .8, sfx_heartbeat(), 1.0)
    for s in ("jobs", "doctor", "walk", "drink", "kids", "boy", "mirror", "title", "choice"): M.add(starts[s] - .3, sfx_whoosh(), .45)
    M.add(starts["mirror"] + vd["mirror"] * .8, sfx_crack(), 1.3); M.add(starts["mirror"] + vd["mirror"] * .8, sfx_impact(), .7)
    for k in range(3): M.add(starts["title"] + .45 + k * 1.0, sfx_impact(), .9)
    M.add(starts["title"], music_pad(starts["tease"] - starts["title"], (110, 138.6, 164.8, 220), .045), 1)
    M.add(starts["tease"] + .3, sfx_knock(), 1.6); M.add(starts["tease"] + vd["tease"] + 1.5, sfx_knock(), 1.8); M.add(total - 1.2, sfx_sting(), 1.)

    def write(a, path):
        a = a[:int(total * SR)]; a = a / max(1, np.abs(a).max() / .95)
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())
    wav, wav_nv = os.path.join(tmp, "mix.wav"), os.path.join(tmp, "nv.wav")
    write(M.buf * .7 + MV.buf, wav); write(M.buf * .6, wav_nv)

    def frame(T):
        for name, d, _ in S_:
            if T < starts[name] + d: break
        t = T - starts[name]
        f = {"cam": "", "bg": "black"}
        fade_in = max(0, 1 - t / .3) if name not in ("hook", "kids", "doctor") else 0
        fade_out = max(0, 1 - (d - t) / .25) if name not in ("hook", "drink", "title", "choice", "collapse", "tease") else 0
        fg, ui = "", hud(1, 0)
        if name == "hook":
            fg = f'<rect x="140" y="760" width="800" height="260" rx="20" fill="#06120c" stroke="#1b2430" stroke-width="10"/>' + ecg(t, 170, 900, 740, 90)
            for k, (w, col, y, t0) in enumerate((("THE DOCTOR", "#ffffff", 560, 1.2), ("GAVE HER", "#ffffff", 690, 1.7), ("30 DAYS.", "#ffd84d", 1260, 2.3))):
                if t >= t0:
                    s = 2.0 - 1.0 * back((t - t0) / .3)
                    fg += f'<g transform="translate(540,{y}) scale({s:.3f})"><text text-anchor="middle" font-family="Anton" font-size="{190 if k == 2 else 130}" fill="{col}" stroke="#000" stroke-width="14" paint-order="stroke">{w}</text></g>'
            ui = ""; f["nocap"] = True
        elif name == "morning":
            f["bg"] = "kitchen_day"
            tw, tj = cue["wine"] - starts["morning"], cue["juice"] - starts["morning"]
            head = {"L": C.pose_offsets("idle", 1)["L"], "R": ((-24, 90), (40, -70))}
            pose = head if t < tw - .3 else "idle"
            fg = ""
            if t < tw - .6:  # kids running around the kitchen
                for i, (x0, sp, foot) in enumerate(((100, 140, 1700), (900, -120, 1720), (300, 90, 1740), (700, -150, 1760))):
                    xx = x0 + sp * t
                    xx = (xx % 1300) - 110
                    fg += kid(i, "happy", xx, foot, 1.15, t, walk=1)
            else:
                fg += kid(0, "sad" if t < tj else "sad", 860, 1660, 1.3, t, talk=talk("wine", T),
                          arms=[((-12, 50), (-10, 96)), ((-60, -6), (-110, -30))] if t < tj else None)
                fg += kid(3, "happy", 160, 1760, 1.15, t)
            fg += mom(t, pose, "tired" if t < tw else ("shocked" if t < tj else "smirk"), 520, 1720, 1.18, talk=talk("juice", T), head_drop=8)
            if t >= tw - .4:  # she slams the cabinet shut
                u = ease((t - (tw - .4)) / .25)
                fg += f'<path d="M{1030 - 140*u:.0f},316 L1060,330 L1060,610 L{1030 - 140*u:.0f},604 Z" fill="#7a45dc" stroke="#2a161c" stroke-width="3"/>'
            if t < tw - .3:
                z, cx_, cy_ = kf(t, [(0, 1.05), (tw * .45, 1.15), (tw * .75, 1.7), (tw - .4, 1.7)]), kf(t, [(0, 540), (tw * .75, 960)]), kf(t, [(0, 1100), (tw * .75, 520)])
            elif t < tj: z, cx_, cy_ = 1.45, 760, 1150
            else: z, cx_, cy_ = kf(t, [(tj, 1.6), (d, 1.4)]), 520, kf(t, [(tj, 900), (d, 1000)])
            f["cam"] = cam(z, cx_, cy_)
        elif name == "jobs":
            f["bg"] = "kitchen_day"
            fg = mom(t, "hold", "sad" if t < d * .6 else "crying", 520, 1720, 1.18, prop="letter", sob=.4 if t > d * .6 else 0)
            for k, (x, y, r) in enumerate(((540, 640, -10), (520, 860, 7), (560, 1080, -5))):
                ui_t0 = vd["jobs"] * (.32 + k * .14) + .4
                fg += stamp("REJECTED", t, ui_t0, x, y, r)
            f["cam"] = cam(kf(t, [(0, 1.0), (d, 1.15)]), 540, kf(t, [(0, 1000), (d, 900)]))
        elif name == "collapse":
            f["bg"] = "kitchen_day"
            tf = vd["collapse"] + .3
            fall = ease((t - tf) / .6) if t > tf else 0
            dizzy = min(1, t / tf)
            fg = mom(t, "idle", "tired" if fall < .2 else "sad", 520, 1720, 1.18, amp=1 + 3 * dizzy, blink=fall > .3, head_drop=16, fall=fall)
            ts = cue["momscream"] - starts["collapse"]
            if t > ts - .5:
                run = ease((t - (ts - .5)) / .8)
                fg += kid(0, "sad", 1150 - 420 * run, 1700, 1.35, t, talk=talk("momscream", T), walk=1 - run)
                fg += kid(3, "sad", -120 + 300 * run, 1760, 1.2, t, walk=1 - run)
            wob = 6 * dizzy * (1 - fall)
            f["cam"] = cam(kf(t, [(0, 1.1), (tf, 1.35), (tf + .6, 1.05), (d, 1.2)]), 520 + wob * math.sin(t * 3), kf(t, [(0, 1050), (tf, 900), (tf + .6, 1300)])) + f" rotate({wob*math.sin(t*2):.2f} 540 960)"
            ui += f'<rect width="1080" height="1920" fill="#fff" opacity="{max(0, 1 - abs(t - tf - .6)/.12)*.7:.2f}"/>'
            if t > d - .8: ui += f'<rect width="1080" height="1920" fill="#000" opacity="{ease((t-(d-.8))/.6):.2f}"/>'
        elif name == "doctor":
            f["bg"] = "doctor"
            sh = 2.5 * math.sin(t * 29)
            base = C.pose_offsets("hold", 1); p = {"L": base["L"], "R": (base["R"][0], (base["R"][1][0] + sh, base["R"][1][1] + sh * .6))}
            crying = t > d * .62
            fg = mom(t, p, "crying" if crying else ("shocked" if t > d * .3 else "sad"), 420, 1740, 1.15, prop="labs", sob=.5 if crying else 0, amp=.4)
            fg += ecg(t, 840, 500, 170, 40)
            if crying: fg += tears_at(t, 420, 1740, 1.15)
            hx, hy_ = 420 + 66 * 1.15, 1740 - 513 * 1.15; eyes_y = 1740 - (905 - 186) * 1.15
            f["cam"] = cam(kf(t, [(0, 1.2), (d * .12, 2.0), (d * .3, 2.0), (d * .38, 2.5), (d * .58, 2.6), (d * .72, 1.3), (d, 1.15)]),
                           kf(t, [(0, 520), (d * .12, hx), (d * .3, hx), (d * .38, 420), (d * .72, 470)]), kf(t, [(0, 900), (d * .12, hy_), (d * .3, hy_), (d * .38, eyes_y), (d * .58, eyes_y), (d * .72, 1150)]))
            if t < .5: ui += f'<rect width="1080" height="1920" fill="#fff" opacity="{1 - t/.5:.2f}"/>'
            fg += vignette(.2)
        elif name == "walk":
            f["bg"] = "street"
            mx = -120 + (d and (1260 * t / d))
            bob = 10 * abs(math.sin(t * 5.5))
            fg = f'<g transform="translate(0,{-bob:.1f})">{mom(t, "hold", "crying", mx, 1660, 1.0, prop="labs", sob=.5)}</g>' + tears_at(t, mx, 1660 - bob, 1.0)
            fg += f'<g transform="translate({mx:.0f},1700) scale(1,-.35)" opacity=".18">{mom(t, "hold", "crying", 0, 0, 1.0)}</g>'
            fg += rain(t, .45) + vignette(.4)
            f["cam"] = cam(1.35, mx, 1250)
        elif name == "drink":
            f["bg"] = "apartment"
            tdk = vd["drink"] + .8
            base = C.pose_offsets("slump", 1); drink = {"L": base["L"], "R": ((-50, 60), (-10, -24))}
            u = kf(t, [(0, 0), (vd["drink"] * .55, 0), (vd["drink"] * .72, 1), (tdk - .3, 1), (tdk, 0)])
            lights = 1 if t < tdk else (0 if t > tdk + .5 or (t - tdk) % .16 < .08 else 1)
            on_light = t > tdk + 1.6
            if on_light: fg = mom(t, "phone", "shocked", 540, 1700, prop="phone")
            else: fg = mom(t, C.lerp_pose(base, drink, u), "tired" if u > .5 else "sad", 540, 1700, prop="wine", prop_rot=-58 * u, head_drop=16 - 18 * u, amp=.6)
            ph = (t % 1.3) / 1.3
            fg += f'<ellipse cx="770" cy="{110 + ph*1390:.0f}" rx="7" ry="12" fill="#9fc4ff" opacity="{.9 if ph < .97 else 0}"/>'
            fg += f'<g transform="translate(905,1500)"><path d="M-60,0 h120 l-14,90 h-92 Z" fill="#8a94b0" stroke="#2a161c" stroke-width="4"/><ellipse rx="60" ry="14" fill="#5a6a90" stroke="#2a161c" stroke-width="4"/></g>'
            if lights: fg += f'<rect x="56" y="896" width="268" height="158" fill="#fff" opacity="{(.35 + .25*math.sin(t*23)*math.sin(t*7))*.4:.2f}"/>'
            fg += rain(t, .32) + vignette(.4) + darkness(.94 * (1 - lights), [(610, 860, 430 + 25 * math.sin(t * 9))] if on_light else [])
            f["cam"] = cam(kf(t, [(0, 1.05), (vd["drink"] * .55, 1.1), (vd["drink"] * .72, 1.5), (tdk, 1.5), (tdk + .4, 1.15), (d, 1.3)]), kf(t, [(0, 540), (vd["drink"] * .72, 580)]),
                           kf(t, [(0, 1100), (vd["drink"] * .72, 760), (tdk, 760), (tdk + .4, 1000), (d, 920)]))
            if tdk < t < tdk + .6: f["cam"] += f" translate({10*math.sin(t*70):.1f},0)"
        elif name in ("kids", "fight", "boy"):
            f["bg"] = "kids_dark"
            KP = [(560, 1650), (700, 1660), (840, 1670), (980, 1700)]
            parts = []
            for i, (kx, foot) in enumerate(KP):
                mood, tk, arms, sc, walk_ = "sad", 0., None, 1.25, 0.
                if name == "kids": tk = talk("scared", T) if i == 2 else (talk("hungry", T) if i == 1 else 0)
                if name == "fight" and i == 0:
                    st_ = ease(t / .5); kx += 0 * st_; sc += .25 * st_; mood, tk = "mad", talk("promise", T)
                    arms = [((-60, -6), (-114, -16 + 8 * math.sin(t * 9))), ((-12, 50), (-10, 96))]
                if name == "boy" and i == 3:
                    tk = talk("die", T)
                    th = cue["hug"] - starts["boy"] - 1.0
                    step = ease(t / .6); kx -= 240 * step; sc += .3 * step
                    if t > th: hu = ease((t - th) / .8); kx -= 260 * hu; foot += 20 * hu
                parts.append(kid(i, mood, kx, foot, sc, t, tk, arms, walk_))
                if mood == "sad" and name != "fight":
                    s_ = sc * C.KIDS[i]["h"]
                    for k in range(2):
                        ph = (t * .8 + k * .5 + i * .3) % 1
                        parts.append(f'<ellipse cx="{kx - 24*s_/1.25:.0f}" cy="{foot - 385*s_ + (110 + ph*90)*s_:.0f}" rx="5" ry="8" fill="#a8e1ff" opacity="{1-ph:.2f}"/>')
            kids_fg = "".join(parts)
            if name == "kids":
                walk = ease(t / 1.4); mx = -180 + 440 * walk; bob = 12 * abs(math.sin(t * 9)) * (1 if t < 1.4 else 0)
                fg = kids_fg + f'<g transform="translate(0,{-bob:.1f})">{mom(t, "phone", "shocked", mx, 1720, 1.15, prop="phone")}</g>'
                fg += darkness(.82, [(kf(t, [(0, 600), (d, 770)]), 1360, 440), (560, 520, 320), (mx + 60, 860, 260)])
                f["cam"] = cam(kf(t, [(0, 1.0), (d, 1.15)]), kf(t, [(0, 540), (d, 640)]), kf(t, [(0, 1200), (d, 1250)]))
            elif name == "fight":
                tt = .5 + vd["promise"] + .7; cry = t > tt
                fg = mom(t, "slump" if not cry else "face", "crying" if cry else "shocked", 260, 1720, 1.15, talk=talk("trying", T), sob=1 if cry else 0) + kids_fg
                if cry: fg += tears_at(t, 260, 1720, 1.15, 16)
                fg += darkness(.76, [(620, 1250, 480), (300, 900, 340), (560, 520, 300)])
                z, cx_, cy_ = (kf(t, [(0, 1.25), (.6, 1.6)]), kf(t, [(0, 560), (.6, 520)]), 1260) if t < tt else (kf(t, [(tt, 1.6), (d, 1.8)]), 280, kf(t, [(tt, 950), (d, 900)]))
                f["cam"] = cam(z, cx_, cy_)
                if t < .6: f["cam"] += f" translate({8*math.sin(t*60):.1f},0)"
            else:
                th = cue["hug"] - starts["boy"] - 1.0
                hu = ease((t - th) / .8) if t > th else 0
                hugp = {"L": ((-36, 84), (64, 150)), "R": ((-36, 84), (64, 150))}
                fg = kids_fg + mom(t, C.lerp_pose(C.pose_offsets("slump", 1), hugp, hu), "crying", 260, 1720, 1.15, sob=.8 * (1 - .5 * hu), amp=.5)
                fg += tears_at(t, 260, 1720, 1.15, 16)
                if hu > .05:  # her hands on his back
                    for hx_ in (260 - 70 * 1.15 + 40, 260 + 70 * 1.15 - 40):
                        fg += f'<circle cx="{hx_:.0f}" cy="{1720 - (905 - 468)*1.15:.0f}" r="{20*hu:.0f}" fill="#c48466" stroke="#2a161c" stroke-width="4"/>'
                fg += darkness(.78, [(kf(t, [(0, 760), (th + .8, 300)]), 1300, 440), (300, 900, 340)])
                tk_ = .6 + vd["die"] + 1.0
                if t < tk_ - .3: z, cx_, cy_ = kf(t, [(0, 1.3), (.8, 1.9)]), 740, 1340
                elif t < th: z, cx_, cy_ = kf(t, [(tk_ - .3, 1.8), (th, 1.6)]), kf(t, [(tk_ - .3, 300), (th, 320)]), 950
                else: z, cx_, cy_ = kf(t, [(th, 1.4), (d, 1.25)]), 300, kf(t, [(th, 1150), (d, 1200)])
                f["cam"] = cam(z, cx_, cy_)
        elif name == "mirror":
            f["bg"] = "bathroom"
            tc = vd["mirror"] * .8 + .4
            crack_u = ease((t - tc) / .5)
            refl = (f'<g clip-path="url(#mc4)" opacity=".6"><g transform="translate(1560,0) scale(-1,1)">{mom(t, "idle", "sad", 780, 1330, .86, talk=talk("whisper", T))}</g>'
                    f'<rect x="560" y="410" width="440" height="880" fill="#6d32d4" opacity=".14"/></g>')
            crack = ""
            if crack_u > 0:
                paths = ["M760,700 L700,560 L640,520", "M760,700 L860,600 L960,560", "M760,700 L720,880 L600,1000", "M760,700 L880,860 L990,1020",
                         "M760,700 L780,500 L760,420", "M760,700 L640,720 L560,700", "M760,700 L900,720 L1000,760"]
                crack = "".join(f'<path d="{p}" stroke="#fff" stroke-width="5" fill="none" stroke-dasharray="600" stroke-dashoffset="{600*(1-crack_u):.0f}" opacity=".9"/>' for p in paths)
            flick = .85 + .15 * math.sin(t * 17) * math.sin(t * 5.3)
            fg = (f'<defs><clipPath id="mc4"><rect x="560" y="410" width="440" height="880" rx="26"/></clipPath></defs>{refl}{crack}'
                  f'<g transform="translate(560,1300)"><rect x="-22" y="-60" width="44" height="64" rx="6" fill="#f4ecd8" stroke="#2a161c" stroke-width="3"/>'
                  f'<path d="M0,-60 q{-6+4*math.sin(t*9):.1f},-20 0,-40 q{6+4*math.sin(t*7):.1f},20 0,40 Z" fill="#ffcf4a"/><circle cx="0" cy="-80" r="{240*flick:.0f}" fill="url(#candleG)" opacity=".9"/></g>')
            fg += mom(t, "idle", "determined" if t > cue["whisper"] - starts["mirror"] else ("shocked" if crack_u > .2 else "sad"), 290, 1740, 1.12, talk=talk("whisper", T), amp=.6)
            fg += f'<rect width="1080" height="1920" fill="#0a0820" opacity="{.5 - .2*flick:.2f}"/>' + vignette(.35)
            fg += f'<rect width="1080" height="1920" fill="#fff" opacity="{max(0, 1 - abs(t - tc)/.12)*.6:.2f}"/>'
            eyes = 1740 - (905 - 186) * 1.12
            tw_ = cue["whisper"] - starts["mirror"]
            f["cam"] = cam(kf(t, [(0, 1.1), (vd["mirror"] * .3, 2.2), (vd["mirror"] * .55, 2.2), (tc, 1.4), (tw_, 1.5), (tw_ + 1, 2.1), (d, 2.2)]),
                           kf(t, [(0, 520), (vd["mirror"] * .3, 290), (vd["mirror"] * .55, 290), (tc, 700), (tw_, 600), (tw_ + 1, 300)]),
                           kf(t, [(0, 1100), (vd["mirror"] * .3, eyes - 60), (vd["mirror"] * .55, eyes - 60), (tc, 780), (tw_, 900), (tw_ + 1, eyes - 40)]))
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
        elif name == "choice":
            sl = back(t / .55)
            hugp = {"L": ((-36, 84), (64, 150)), "R": ((-36, 84), (64, 150))}
            hide = {"L": C.pose_offsets("idle", 1)["L"], "R": ((-10, 96), (60, 150))}
            uL = kf(t, [(0, 0), (d * .3, 0), (d * .45, 1)]); uR = kf(t, [(0, 0), (d * .5, 0), (d * .65, 1)])
            left = (f'<g transform="translate({-540*(1-sl):.1f},0)"><rect width="540" height="1920" fill="#123a4f"/><rect width="540" height="1920" fill="url(#vig)" opacity=".55"/>'
                    f'<g transform="translate(270,600) scale({1 + .05*math.sin(t*5):.3f})"><text text-anchor="middle" font-family="Anton" font-size="150" fill="#7fe0ff" stroke="#000" stroke-width="12" paint-order="stroke">TELL</text>'
                    f'<text text-anchor="middle" y="70" font-family="Anton" font-size="40" fill="#fff" stroke="#000" stroke-width="6" paint-order="stroke">the kids the truth</text></g>'
                    + mom(t, C.lerp_pose(C.pose_offsets("idle", 1), hugp, uL), "crying", 270, 1720, .78, sob=.3, amp=.6)
                    + kid(3, "sad", 270, 1760, 1.0, t)
                    + "".join(f'<circle cx="{270 + s_*36:.0f}" cy="{1720 - (905-468)*.78:.0f}" r="{14*uL:.0f}" fill="#c48466" stroke="#2a161c" stroke-width="3"/>' for s_ in (-1, 1)) + '</g>')
            right = (f'<g transform="translate({540*(1-sl):.1f},0)"><rect x="540" width="540" height="1920" fill="#4a0f24"/><rect x="540" width="540" height="1920" fill="url(#vig)" opacity=".55"/>'
                     f'<g transform="translate(810,600) scale({1 + .05*math.sin(t*5+1.5):.3f})"><text text-anchor="middle" font-family="Anton" font-size="150" fill="#ff6f9f" stroke="#000" stroke-width="12" paint-order="stroke">SECRET</text>'
                     f'<text text-anchor="middle" y="70" font-family="Anton" font-size="40" fill="#fff" stroke="#000" stroke-width="6" paint-order="stroke">hide the doctor\'s news</text></g>'
                     + mom(t, C.lerp_pose(C.pose_offsets("hold", 1), hide, uR), "smirk" if uR > .5 else "sad", 810, 1720, .82, prop="labs", amp=.6) + '</g>')
            pulse = 1 + .07 * math.sin(t * 7)
            fg = left + right + f'<rect x="532" y="420" width="16" height="{1320*sl:.0f}" fill="#ffd84d"/>'
            ui = hud(1, 0) + f'<g transform="translate(540,340) scale({pulse:.3f})"><text text-anchor="middle" font-family="Anton" font-size="78" fill="#ffd84d" stroke="#000" stroke-width="12" paint-order="stroke" letter-spacing="3">COMMENT ONE WORD</text></g>'
        else:  # tease: knocking at the door
            f["bg"] = "black"
            under = .5 + .5 * math.sin(t * 2)
            sh = max(0, 1 - abs(t - .3) / .2) + max(0, 1 - abs(t - .62) / .2) + max(0, 1 - abs(t - .94) / .2)
            fg = (f'<rect x="300" y="420" width="480" height="1140" rx="8" fill="#1a1426" stroke="#2a2440" stroke-width="12"/><circle cx="720" cy="1000" r="16" fill="#c9a96e"/>'
                  f'<rect x="300" y="1556" width="480" height="10" fill="#ffe6a8" opacity="{.6+.4*under:.2f}"/><path d="M300,1566 L180,1920 L900,1920 L780,1566 Z" fill="#ffe6a8" opacity=".12"/>'
                  f'<rect x="440" y="1556" width="70" height="10" fill="#000"/><rect x="560" y="1556" width="70" height="10" fill="#000"/>')
            f["cam"] = cam(1.0 + .05 * t, 540, 1100) + f" translate({10*sh*math.sin(t*80):.1f},0)"
            if t > d - 1.8:
                a = ease((t - (d - 1.8)) / .4)
                ui += (f'<rect width="1080" height="1920" fill="#000" opacity="{.6*a:.2f}"/><g opacity="{a:.2f}"><text x="540" y="860" text-anchor="middle" font-family="Anton" font-size="96" fill="#fff" stroke="#000" stroke-width="12" paint-order="stroke">WHO\'S AT THE DOOR?</text>'
                       f'<text x="540" y="1000" text-anchor="middle" font-family="Anton" font-size="84" fill="#ffd84d" stroke="#000" stroke-width="12" paint-order="stroke">EPISODE 2 DEPENDS ON YOU</text></g>')
                f["nocap"] = True
        if not f.get("nocap"): ui += captions(T, groups)
        fo = max(fade_in, fade_out)
        if fo: ui += f'<rect width="1080" height="1920" fill="#000" opacity="{fo:.2f}"/>'
        f["fg"] = fg; f["ui"] = ui
        return f

    empty = Rm.kids_room(lights_on=False)
    for x, k1, k2, q1, q2 in ((20, 0, 2, "quilt1", "quilt3"), (590, 1, 3, "quilt2", "quilt4")):
        empty = empty.replace(Rm.bunk_bed(x, C.KIDS[k1], C.KIDS[k2], q1, q2), Rm.bunk_bed(x, None, None, q1, q2))
    bgs = {"black": '<rect width="1080" height="1920" fill="#07050f"/>', "doctor": Rm.doctor_office(), "apartment": Rm.apartment(), "kitchen_day": Rm.kitchen_day(),
           "street": Rm.street_rain(), "kids_dark": empty, "bathroom": Rm.bathroom_candle()}
    if os.environ.get("DRY"):
        for i in range(0, int(total * FPS), 5): frame(i / FPS)
        print("dry ok", round(total, 1), {k: round(v, 1) for k, v in starts.items()}); return
    if os.environ.get("STILLS"):  # render chosen moments as PNGs for review
        times = [float(x) for x in os.environ["STILLS"].split(",")]
        js = os.path.join(tmp, "s.js")
        open(js, "w").write("""const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.setContent('<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@700;800&display=swap" rel="stylesheet"><style>body{margin:0}svg{display:block}</style></head><body><svg id="r" width="1080" height="1920" viewBox="0 0 1080 1920">'+d.defs+'<g id="cam"><g id="bg"></g><g id="fg"></g></g><g id="ui"></g></svg></body></html>',{waitUntil:'networkidle'});
for (const fr of d.frames){await p.evaluate(([f,bgs])=>{document.getElementById('bg').innerHTML=bgs[f.bg];document.getElementById('cam').setAttribute('transform',f.cam||'');document.getElementById('fg').innerHTML=f.fg;document.getElementById('ui').innerHTML=f.ui;},[fr,d.bgs]);await p.screenshot({path:fr.path,clip:{x:0,y:0,width:1080,height:1920}});}
await b.close()})();""")
        frames_ = []
        for k, tt in enumerate(times):
            fr = frame(tt); fr["path"] = os.path.join(os.environ.get("STILL_DIR", tmp), f"still_{k:02d}.png"); frames_.append(fr)
        jf = os.path.join(tmp, "s.json"); json.dump({"defs": C.DEFS + Sc.SCENE_DEFS + Rm.ROOM_DEFS, "bgs": bgs, "frames": frames_}, open(jf, "w"))
        subprocess.run(["node", js, jf], check=True)
        print("stills", {k: round(v, 1) for k, v in starts.items()}); return
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
        lines = ["EPISODE 1 · DAY 1  (30 Days to Her)", "Narrator: natural, warm, storyteller. Kids: real and raw. Let the silences breathe.", ""]
        for key, s in sorted(cue.items(), key=lambda kv: kv[1]):
            lines.append(f"[{int(s)//60}:{int(s)%60:02d}] {WHO[LINES[key][0]]}: {LINES[key][1]}")
        lines += ["", "POST CAPTION:", "The doctor gave her 30 days 💔 Single mom of 4. She collapsed in front of her kids. Liver failing. Lights cut off. Her son asked if she's gonna die. Should she TELL the kids the truth or keep it a SECRET? 👇🏽 #30DaysToHer #storytime #fyp #momlife",
                  "", "PIN THIS COMMENT: Most comments wins. Episode 2 drops at 100 comments 💜"]
        open(os.path.join(OUT, "Episode-1-SCRIPT.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    pv = float(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else None
    build(pv)
