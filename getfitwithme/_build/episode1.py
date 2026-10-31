#!/usr/bin/env python3
"""Episode 1 of "30 Days to Her": renders frames (captioned + clean) and the videos.
    python3 getfitwithme/_build/episode1.py"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "series", "episode-01")
sys.path.insert(0, HERE)
import scenes as Sc  # noqa: E402
import character as C  # noqa: E402

# (seconds, voiceover, caption)
SCRIPT = [
    (5.0, "Day one. Two a.m. It's raining. And she's on her third bottle this week.", "2 A.M. *Third* bottle this week."),
    (4.6, "The lights are about to be cut off. The fridge is almost empty. And she's out of answers.", "*SHUT-OFF* notice. Fridge almost *empty.*"),
    (5.0, "Down the hall, four babies are sleeping. They have no idea their mommy is falling apart.", "Four babies asleep. They don't know *mommy* is falling apart."),
    (4.6, "Then her little boy wakes up, holding his teddy bear. Mommy... why you crying?", '"Mommy... why you *crying?*"'),
    (5.4, "She walks to the mirror. She hasn't looked in months. And for one second... she sees her. The woman she could become.", "For one second... she saw *HER.*"),
    (6.4, "She has thirty days to change her life. For her kids. For herself. And you decide every move. Comment one word: POUR IT OUT... or ONE MORE GLASS.", None),
]


def frames(captions=True):
    cap = lambda i: SCRIPT[i][2] if captions else None
    F = [
        Sc.frame("apartment_night", Sc.place_mom(1, "hoodie", "slump", "crying", "wine", x=540, foot=1700), label="DAY 1", cap=cap(0), dark=.55, storm=True),
        Sc.frame("kitchen_night", Sc.place_mom(1, "hoodie", "hold", "shocked", "letter", x=380, foot=1720), cap=cap(1), dark=.45),
        Sc.frame("kids_room", "", cap=cap(2), dark=.4),
        Sc.frame("hallway", Sc.place_mom(1, "hoodie", "slump", "crying", x=390, foot=1720) + Sc.place_kid(3, "sad", 800, 1740, 1.9) + Sc.teddy(890, 1690, .75), cap=cap(3), dark=.45),
    ]
    mirror = (f'<g clip-path="url(#mirrorClip)"><rect x="560" y="430" width="440" height="860" fill="url(#mirrorGlow)"/>'
              f'<g opacity=".85" filter="url(#mirrorFx)">{Sc.place_mom(0, "bra", "flex", "smirk", x=780, foot=1330, scale=.86)}</g>'
              + "".join(f'<path d="M{x},{y} l5,14 14,5 -14,5 -5,14 -5,-14 -14,-5 14,-5 Z" fill="#fff" opacity=".85"/>' for x, y in ((620, 520), (950, 600), (640, 900), (980, 1000), (720, 470)))
              + '<path d="M580,450 L700,450 L580,640 Z" fill="#fff" opacity=".12"/></g>')
    F.append(Sc.frame("bathroom", Sc.place_mom(1, "hoodie", "idle", "sad", x=300, foot=1740, scale=1.12), extra=mirror, cap=cap(4), dark=.35))

    def half(x0, col, glow, lines, sub, pose, face, prop):
        t = "".join(f'<text x="{x0+270}" y="{560+i*118}" text-anchor="middle" font-family="Anton" font-size="120" fill="{col}" stroke="#000" stroke-width="10" paint-order="stroke">{l}</text>' for i, l in enumerate(lines))
        return (f'<rect x="{x0}" width="540" height="1920" fill="{glow}"/><rect x="{x0}" width="540" height="1920" fill="url(#vig)" opacity=".6"/>{t}'
                f'<text x="{x0+270}" y="{520 + len(lines)*118}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="32" fill="#fff">{sub}</text>'
                + Sc.place_mom(1, "hoodie", pose, face, prop, x=x0 + 270, foot=1720, scale=.82))
    F.append(f'<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{C.DEFS}{Sc.SCENE_DEFS}'
             + half(0, "#7fe0ff", "#123a4f", ["POUR", "IT OUT"], "Start Day 1 for real", "hold", "determined", "wine")
             + half(540, "#ff6f9f", "#4a0f24", ["ONE MORE", "GLASS"], "I'll start tomorrow...", "hold", "sad", "glass")
             + '<rect x="532" y="360" width="16" height="1400" fill="#ffd84d"/>'
             + '<text x="540" y="420" text-anchor="middle" font-family="Anton" font-size="70" fill="#ffd84d" stroke="#000" stroke-width="10" paint-order="stroke" letter-spacing="4">COMMENT ONE WORD</text>'
             + '<text x="540" y="1830" text-anchor="middle" font-family="Anton" font-size="62" fill="#fff" stroke="#000" stroke-width="10" paint-order="stroke">WHAT SHOULD SHE DO?</text>'
             + Sc.hud(1, 0) + '</svg>')
    return F


RENDER_JS = """const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const head='<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@700;800&display=swap" rel="stylesheet"><style>body{margin:0}svg{display:block}</style></head><body>';
for (const [path,svg] of jobs){await p.setContent(head+svg+'</body></html>',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.screenshot({path,clip:{x:0,y:0,width:1080,height:1920}});}
await b.close()})();"""


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def video(pngs, out, tmp):
    fps, fade = 30, .6
    clips = []
    moves = [("1.0+0.0009*on", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),            # slow push in
             ("1.12-0.0007*on", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),           # pull out
             ("1.08", "(iw-iw/zoom)*on/{n}", "ih/2-(ih/zoom/2)"),                   # pan right
             ("1.0+0.0011*on", "iw/2-(iw/zoom/2)", "ih*0.42-(ih/zoom/2)"),         # push toward faces
             ("1.0+0.0013*on", "iw*0.62-(iw/zoom/2)", "ih*0.45-(ih/zoom/2)"),      # push into the mirror
             ("1.04+0.0004*on", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)")]
    for i, (png, (sec, _, _)) in enumerate(zip(pngs, SCRIPT)):
        n = int((sec + fade) * fps)
        z, x, y = moves[i % len(moves)]
        c = os.path.join(tmp, f"clip{i}.mp4")
        ff("-loop", "1", "-i", png, "-vf",
           f"scale=2160:3840,zoompan=z='{z}':x='{x.format(n=n)}':y='{y}':d={n}:s=1080x1920:fps={fps},format=yuv420p",
           "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", c)
        clips.append((c, sec + fade))
    # crossfade chain
    inputs, filt, last, t = [], [], "0:v", 0
    for c, _ in clips: inputs += ["-i", c]
    for i in range(1, len(clips)):
        t += clips[i - 1][1] - fade
        filt.append(f"[{last}][{i}:v]xfade=transition={'fadeblack' if i in (2, 4, 5) else 'fade'}:duration={fade}:offset={t:.2f}[v{i}]")
        last = f"v{i}"
    total = sum(d for _, d in clips) - fade * (len(clips) - 1)
    # rain + thunder bed, then a soft swell on the choice
    audio = (f"anoisesrc=color=pink:amplitude=0.35:duration={total:.2f},highpass=f=900,lowpass=f=7000,volume=0.35[rain];"
             f"anoisesrc=color=brown:amplitude=0.9:duration={total:.2f},lowpass=f=120,volume='if(between(t,0.3,2.2),1.6*exp(-(t-0.3)),0.05)':eval=frame[thunder];"
             f"sine=f=110:duration={total:.2f},volume='0.06*min(1,max(0,(t-{total-7:.2f})/4))':eval=frame[pad1];"
             f"sine=f=164.8:duration={total:.2f},volume='0.045*min(1,max(0,(t-{total-7:.2f})/4))':eval=frame[pad2];"
             f"[rain][thunder][pad1][pad2]amix=inputs=4:normalize=0,afade=t=out:st={total-1.2:.2f}:d=1.2[a]")
    ff(*inputs, "-filter_complex", ";".join(filt) + ";" + audio, "-map", f"[{last}]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{total:.2f}", out)
    print(out, f"{total:.1f}s")


def main():
    tmp = tempfile.mkdtemp()
    os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "frames-clean"), exist_ok=True)
    jobs, cap_png, clean_png = [], [], []
    for i, (a, b) in enumerate(zip(frames(True), frames(False))):
        pa, pb = os.path.join(OUT, "frames", f"{i+1:02d}.png"), os.path.join(OUT, "frames-clean", f"{i+1:02d}.png")
        jobs += [[pa, a], [pb, b]]; cap_png.append(pa); clean_png.append(pb)
    js = os.path.join(tmp, "r.js"); open(js, "w").write(RENDER_JS)
    jf = os.path.join(tmp, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", js, jf], check=True)
    video(cap_png, os.path.join(OUT, "Episode-1-Day-1-READY-TO-POST.mp4"), tmp)
    video(clean_png, os.path.join(OUT, "Episode-1-Day-1-CLEAN-for-voiceover.mp4"), tmp)
    t, lines = 0.0, ["EPISODE 1 · DAY 1 · ROCK BOTTOM", "30 Days to Her", "", "VOICEOVER SCRIPT (read slow, emotional, let it breathe)", ""]
    for i, (sec, vo, _) in enumerate(SCRIPT):
        lines.append(f"[{int(t)//60}:{int(t)%60:02d}] Scene {i+1}: {vo}"); t += sec
    lines += ["", "POST CAPTION:", "Day 1. Single mom of 4. Rock bottom. 30 days to change my life, and YOU decide every move 💔 "
              "Comment POUR IT OUT or ONE MORE GLASS 👇🏽 #30DaysToHer #fyp #momlife #transformation",
              "", "PIN THIS COMMENT: Most comments wins. Episode 2 drops when we hit 100 comments 💜"]
    open(os.path.join(OUT, "Episode-1-SCRIPT.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
