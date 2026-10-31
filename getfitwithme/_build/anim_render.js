// Frame renderer: reads JSON lines on stdin (first line: defs + backgrounds, then one frame per line),
// renders each frame with Chromium and pipes JPEGs into ffmpeg.  node anim_render.js <out.mp4> <fps>
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const readline = require('readline');
(async () => {
  const [out, fps] = process.argv.slice(2);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', fps, '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
  let head = null, n = 0;
  for await (const line of rl) {
    if (!line.trim()) continue;
    const d = JSON.parse(line);
    if (!head) {
      head = d;
      await p.setContent(`<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@700;800&display=swap" rel="stylesheet">
        <style>body{margin:0;background:#000}svg{display:block}</style></head><body>
        <svg id="root" width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">${d.defs}
        <g id="cam"><g id="bg"></g><g id="fg"></g></g><g id="ui"></g></svg></body></html>`, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      await p.evaluate(bgs => { window.BGS = bgs; window.curBg = null; }, d.bgs);
      continue;
    }
    await p.evaluate(f => {
      if (f.bg !== window.curBg) { document.getElementById('bg').innerHTML = window.BGS[f.bg]; window.curBg = f.bg; }
      document.getElementById('cam').setAttribute('transform', f.cam || '');
      document.getElementById('fg').innerHTML = f.fg;
      document.getElementById('ui').innerHTML = f.ui;
    }, d);
    const buf = await p.screenshot({ type: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (++n % 150 === 0) process.stderr.write(`  ${n} frames\n`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
