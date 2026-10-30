// Renders PDF books with Chromium. node pdf.js <tmpdir> [--pass2] <slug...>
// Pass 1: <slug>-book1.html -> .pdf, plus <slug>-wb.html -> .pdf and field geometry (<slug>-wb.json).
// Pass 2: <slug>-book2.html (table of contents now has page numbers) -> .pdf with bookmarks.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const args = process.argv.slice(2), dir = args.shift(), pass2 = args[0] === '--pass2';
  if (pass2) args.shift();
  const b = await chromium.launch(), page = await b.newPage();
  const load = async f => { await page.goto('file://' + path.join(dir, f), { waitUntil: 'networkidle' }); await page.evaluate(() => document.fonts.ready) };
  for (const slug of args) {
    await load(`${slug}-book${pass2 ? 2 : 1}.html`);
    await page.pdf({ path: path.join(dir, `${slug}-book${pass2 ? 2 : 1}.pdf`), format: 'Letter', preferCSSPageSize: true, printBackground: true, outline: false, tagged: true });
    if (pass2) continue;
    await load(`${slug}-wb.html`);
    const fields = await page.evaluate(() => [...document.querySelectorAll('[data-f]')].map(el => {
      const pg = el.closest('.page'), pi = [...document.querySelectorAll('.page')].indexOf(pg), r = el.getBoundingClientRect(), pr = pg.getBoundingClientRect();
      return { p: pi, k: el.dataset.f, name: el.dataset.name, x: r.left - pr.left, y: r.top - pr.top, w: r.width, h: r.height };
    }));
    fs.writeFileSync(path.join(dir, `${slug}-wb.json`), JSON.stringify(fields));
    await page.pdf({ path: path.join(dir, `${slug}-wb.pdf`), format: 'Letter', preferCSSPageSize: true, printBackground: true });
  }
  await b.close();
})();
