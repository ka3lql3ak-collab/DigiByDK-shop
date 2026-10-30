// Renders each cover in covers.html to a 1080x1080 PNG: node covers.js <covers.html> <outdir> <slug...>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [src, out, ...slugs] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
  await p.goto('file://' + path.resolve(src));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  for (const s of slugs) await (await p.$('#c-' + s + ' .cover')).screenshot({ path: path.join(out, s + '.png') });
  await b.close();
})();
