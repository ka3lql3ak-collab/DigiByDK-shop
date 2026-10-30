// Get Fit With Me — interactive product engine. Renders window.P into the app.
const KEY = 'gfwm2_' + P.slug;
let S = {};
try { S = JSON.parse(localStorage.getItem(KEY)) || {} } catch (e) {}
for (const k of ['d', 'v', 'q', 'read']) S[k] = S[k] || {};
for (const k of ['pr', 'm']) S[k] = S[k] || [];
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)) } catch (e) {} };
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const num = v => { const n = parseFloat(v); return isFinite(n) ? n : null };
const e1rm = (w, r) => r <= 1 ? w : w * (1 + r / 30);
const fmt = n => Math.round(n).toLocaleString();
const sec = id => P.sections.find(s => s.id === id);

// ---------------------------------------------------------------- theme
function applyTheme() { const t = S.v.theme || 'auto'; if (t === 'auto') document.documentElement.removeAttribute('data-theme'); else document.documentElement.dataset.theme = t }
applyTheme();

// ---------------------------------------------------------------- progress keys
function keys(s) {
  if (s.type === 'program') return s.weeks.flatMap((w, wi) => w.days.map((_, di) => `${s.id}:${wi}:${di}`));
  if (s.type === 'challenge') return s.days.map((_, i) => `${s.id}:${i}`);
  if (s.type === 'checklist') return s.groups.flatMap((g, gi) => g.items.map((_, ii) => `${s.id}:${gi}:${ii}`));
  if (s.type === 'guide') return P.guide.map((_, i) => `read:${i}`);
  return [];
}
const isDone = k => k.startsWith('read:') ? !!S.read[k.slice(5)] : !!S.d[k];
const ALL = P.sections.flatMap(keys);
const pct = list => list.length ? Math.round(100 * list.filter(isDone).length / list.length) : 0;
const bar = (list, label = 'complete') => `<div class="meter"><div class="meter-top"><span>${pct(list)}% ${label}</span><span>${list.filter(isDone).length} / ${list.length}</span></div><div class="track"><i style="width:${pct(list)}%"></i></div></div>`;

// ---------------------------------------------------------------- program helpers
function setKey(sid, wi, di, ei, si) { return `${sid}:${wi}:${di}:${ei}:${si}` }
function lastTime(s, wi, di, ei) {
  for (let w = wi - 1; w >= 0; w--) {
    const ex = s.weeks[w].days[di].ex[ei], out = [];
    for (let si = 0; si < ex.s; si++) { const k = setKey(s.id, w, di, ei, si), wt = S.v[k + ':w'], r = S.v[k + ':r']; if (wt || r) out.push(`${wt || '—'}×${r || '—'}`) }
    if (out.length) return { week: s.weeks[w].name, txt: out.join(' · '), ws: Array.from({ length: ex.s }, (_, si) => S.v[setKey(s.id, w, di, ei, si) + ':w'] || '') };
  }
  return null;
}
function history() { // {exercise: [{x: label, i: weekIndex, v: e1rm, w, r}]}
  const H = {};
  P.sections.filter(s => s.type === 'program').forEach(s => s.weeks.forEach((wk, wi) => wk.days.forEach((d, di) => d.ex.forEach((ex, ei) => {
    for (let si = 0; si < ex.s; si++) {
      const k = setKey(s.id, wi, di, ei, si), w = num(S.v[k + ':w']), r = num(S.v[k + ':r']);
      if (w && r) { const v = e1rm(w, r), a = H[ex.n] = H[ex.n] || {}; if (!a[wi] || v > a[wi].v) a[wi] = { x: wk.name.replace('Week ', 'W'), i: wi, v, w, r } }
    }
  }))));
  for (const n in H) H[n] = Object.values(H[n]).sort((a, b) => a.i - b.i);
  return H;
}

// ---------------------------------------------------------------- renderers
const R = {
  guide(s) {
    const ch = S.v.ch;
    if (ch == null) {
      const qd = S.v.gq || '';
      const list = P.guide.map((c, i) => ({ c, i })).filter(({ c }) => !qd || (c.t + ' ' + c.text).toLowerCase().includes(qd.toLowerCase()));
      return `${bar(keys(s), 'read')}
      <div class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="gsearch" placeholder="Search ${P.guide.length} chapters…" value="${esc(qd)}" aria-label="Search the guide"></div>
      <ol class="toc">${list.map(({ c, i }) => {
        let snip = '';
        if (qd) { const t = c.text, p = t.toLowerCase().indexOf(qd.toLowerCase()); if (p > -1) snip = `<span class="snip">…${esc(t.slice(Math.max(0, p - 50), p))}<mark>${esc(t.substr(p, qd.length))}</mark>${esc(t.slice(p + qd.length, p + 90))}…</span>` }
        return `<li><button class="toc-row ${S.read[i] ? 'is-read' : ''}" data-ch="${i}"><span class="toc-n">${String(i + 1).padStart(2, '0')}</span><span class="toc-t">${esc(c.t)}${snip}</span><span class="toc-m">${S.read[i] ? '<svg viewBox="0 0 24 24" class="ic ok"><path d="m5 12 5 5L20 7"/></svg>' : c.min + ' min'}</span></button></li>`
      }).join('') || '<p class="muted">No chapters match that search.</p>'}</ol>`;
    }
    const c = P.guide[ch], n = P.guide.length;
    return `<div class="reader">
      <div class="reader-bar"><button class="link" data-ch="toc">← All chapters</button><span>Chapter ${+ch + 1} of ${n} · ${c.min} min read</span></div>
      <article class="prose"><h2>${esc(c.t)}</h2>${c.html}</article>
      <div class="reader-foot">
        ${ch > 0 ? `<button class="btn ghost" data-ch="${ch - 1}">← Previous</button>` : '<span></span>'}
        ${ch < n - 1 ? `<button class="btn primary" data-readnext="${ch}">Mark as read · Next →</button>` : `<button class="btn primary" data-readnext="${ch}">${S.read[ch] ? 'Finished ✓' : 'Mark as read · Finish'}</button>`}
      </div></div>`;
  },

  program(s) {
    const wi = Math.min(+(S.v[s.id + ':wk'] || 0), s.weeks.length - 1), wk = s.weeks[wi];
    const firstOpen = wk.days.findIndex((_, di) => !S.d[`${s.id}:${wi}:${di}`]);
    return `${bar(keys(s), 'of workouts complete')}
    ${s.weeks.length > 1 ? `<div class="seg" role="tablist">${s.weeks.map((w, i) => {
      const done = w.days.every((_, di) => S.d[`${s.id}:${i}:${di}`]);
      return `<button class="${i == wi ? 'on' : ''} ${done ? 'done' : ''}" data-wk="${s.id}:${i}">${esc(w.name.replace('Week ', 'Wk '))}${done ? ' ✓' : ''}</button>`
    }).join('')}</div>` : ''}
    <div class="phase"><div><span class="eyebrow">${esc(wk.name)} · ${esc(wk.phase)} phase</span><p>${esc(wk.note)}</p></div></div>
    ${wk.days.map((d, di) => {
      const k = `${s.id}:${wi}:${di}`, done = S.d[k], openK = 'open:' + k;
      const open = S.v[openK] ?? (di === firstOpen);
      const sets = d.ex.reduce((a, e) => a + e.s, 0), doneSets = d.ex.reduce((a, e, ei) => a + Array.from({ length: e.s }, (_, si) => S.d[setKey(s.id, wi, di, ei, si)]).filter(Boolean).length, 0);
      return `<section class="day ${done ? 'complete' : ''} ${open ? 'open' : ''}">
        <button class="day-head" data-toggle="${openK}" aria-expanded="${!!open}">
          <span class="day-status">${done ? '<svg viewBox="0 0 24 24" class="ic"><path d="m5 12 5 5L20 7"/></svg>' : di + 1}</span>
          <span class="day-title"><b>${esc(d.name)}</b><small>${esc(d.focus)}</small></span>
          <span class="day-count">${doneSets}/${sets} sets</span>
          <svg viewBox="0 0 24 24" class="ic chev"><path d="m6 9 6 6 6-6"/></svg>
        </button>
        ${open ? `<div class="day-body">
          ${d.ex.map((e, ei) => {
            const lt = lastTime(s, wi, di, ei);
            return `<div class="ex">
              <div class="ex-head"><button class="ex-name" data-lib="${esc(e.n)}">${esc(e.n)} <svg viewBox="0 0 24 24" class="ic sm"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg></button>
                <div class="ex-meta"><span>${e.s} × ${esc(e.r)}</span><span>RIR ${esc(e.rir)}</span><span>Rest ${esc(e.rest)}</span></div></div>
              ${lt ? `<p class="last">Last time (${esc(lt.week)}): <b>${esc(lt.txt)}</b></p>` : ''}
              <div class="sets"><div class="set-h"><span>Set</span><span>lb</span><span>Reps</span><span></span></div>
              ${Array.from({ length: e.s }, (_, si) => {
                const sk = setKey(s.id, wi, di, ei, si), on = S.d[sk];
                const ph = lt ? (lt.ws[si] || lt.ws.find(Boolean) || '') : '';
                return `<div class="set ${on ? 'on' : ''}"><span class="set-n">${si + 1}</span>
                  <input inputmode="decimal" data-v="${sk}:w" value="${esc(S.v[sk + ':w'] || '')}" placeholder="${esc(ph)}" aria-label="Set ${si + 1} weight">
                  <input inputmode="numeric" data-v="${sk}:r" value="${esc(S.v[sk + ':r'] || '')}" placeholder="${esc(String(e.r).split(/[–\s]/)[0])}" aria-label="Set ${si + 1} reps">
                  <button class="tick" data-set="${sk}" data-rest="${esc(e.rest)}" aria-label="Complete set ${si + 1}"><svg viewBox="0 0 24 24" class="ic"><path d="m5 12 5 5L20 7"/></svg></button></div>`
              }).join('')}</div></div>`
          }).join('')}
          <label class="notes"><span>Session notes</span><textarea data-v="${k}:notes" placeholder="How did it feel? Anything to change next time?">${esc(S.v[k + ':notes'] || '')}</textarea></label>
          <button class="btn ${done ? 'ghost' : 'primary'} wide" data-day="${k}">${done ? 'Mark as not complete' : 'Complete workout'}</button>
        </div>` : ''}
      </section>`
    }).join('')}`;
  },

  challenge(s) {
    const sel = Math.min(+(S.v[s.id + ':sel'] || 0), s.days.length - 1), d = s.days[sel], dk = `${s.id}:${sel}`;
    let streak = 0; while (streak < s.days.length && S.d[`${s.id}:${streak}`]) streak++;
    const done = s.days.filter((_, i) => S.d[`${s.id}:${i}`]).length;
    return `<div class="stats"><div><b>${done}</b><span>Days complete</span></div><div><b>${streak}</b><span>Day streak</span></div><div><b>${s.days.length - done}</b><span>Days to go</span></div></div>
    <div class="cal">${s.days.map((x, i) => `<button class="${i == sel ? 'sel' : ''} ${S.d[s.id + ':' + i] ? 'on' : ''}" data-sel="${s.id}:${i}" aria-label="Day ${i + 1}">${i + 1}</button>`).join('')}</div>
    <section class="card ${S.d[dk] ? 'complete' : ''}">
      <div class="card-head"><div><span class="eyebrow">Day ${sel + 1} · Week ${Math.floor(sel / 7) + 1}</span><h3>${esc(d.t)}</h3></div>${S.d[dk] ? '<span class="badge">Complete</span>' : ''}</div>
      ${d.rounds ? `<p class="muted">Complete <b>${d.rounds} rounds</b> of the circuit below. Rest 60 seconds between rounds.</p>` : ''}
      <ul class="moves">${d.ex.map(e => `<li><span>${esc(e.n)}</span><b>${esc(e.r)}</b></li>`).join('')}</ul>
      ${d.rounds ? `<div class="rounds">${Array.from({ length: d.rounds }, (_, r) => `<button class="${S.d[dk + ':r' + r] ? 'on' : ''}" data-flag="${dk}:r${r}">Round ${r + 1}</button>`).join('')}</div>` : ''}
      <h4>Daily non-negotiables</h4>
      ${s.tasks.map((t, ti) => check(`${dk}:t${ti}`, t, `data-task="${dk}"`)).join('')}
      <h4>Mindset prompt</h4><blockquote class="prompt">${esc(d.prompt)}</blockquote>
      <textarea data-v="${dk}:j" placeholder="Write your reflection…">${esc(S.v[dk + ':j'] || '')}</textarea>
      <div class="row-between">${sel > 0 ? `<button class="btn ghost" data-sel="${s.id}:${sel - 1}">← Day ${sel}</button>` : '<span></span>'}${sel < s.days.length - 1 ? `<button class="btn ghost" data-sel="${s.id}:${sel + 1}">Day ${sel + 2} →</button>` : ''}</div>
    </section>`;
  },

  progress(s) {
    const H = history(), lifts = (s.lifts || []).filter(Boolean);
    let html = '';
    if (lifts.length) {
      const cur = S.v.chartLift && lifts.includes(S.v.chartLift) ? S.v.chartLift : lifts[0];
      const pts = H[cur] || [];
      html += `<section class="card"><div class="card-head"><div><span class="eyebrow">Strength trend</span><h3>Estimated 1-rep max</h3></div>
        <select data-sv="chartLift" aria-label="Choose exercise">${lifts.map(l => `<option ${l === cur ? 'selected' : ''}>${esc(l)}</option>`).join('')}</select></div>
        ${pts.length ? chart(pts.map(p => ({ x: p.x, y: p.v, t: `${p.w} lb × ${p.r}` }))) : `<div class="empty">Log weights and reps for <b>${esc(cur)}</b> in the Program tab and your trend appears here.</div>`}
        ${pts.length > 1 ? `<p class="muted">Change since ${esc(pts[0].x)}: <b class="up">${pts.at(-1).v >= pts[0].v ? '+' : ''}${fmt(pts.at(-1).v - pts[0].v)} lb (${Math.round(100 * (pts.at(-1).v / pts[0].v - 1))}%)</b></p>` : ''}</section>`;
      const best = {};
      lifts.forEach(l => (H[l] || []).forEach(p => { if (!best[l] || p.v > best[l].v) best[l] = { ...p, src: 'Program' } }));
      S.pr.forEach(p => { const v = e1rm(p.w, p.r); if (!best[p.l] || v > best[p.l].v) best[p.l] = { v, w: p.w, r: p.r, src: p.date } });
      html += `<section class="card"><div class="card-head"><div><span class="eyebrow">Personal records</span><h3>PR Wall</h3></div></div>
        <div class="pr-grid">${lifts.map(l => `<div class="pr ${best[l] ? 'has' : ''}"><span>${esc(l)}</span>${best[l] ? `<b>${best[l].w} lb × ${best[l].r}</b><small>e1RM ${fmt(best[l].v)} lb</small>` : '<small>No record yet</small>'}</div>`).join('')}</div>
        <details class="add"><summary>Log a PR manually</summary><div class="form3">
          <select id="prl">${lifts.map(l => `<option>${esc(l)}</option>`).join('')}</select><input id="prw" inputmode="decimal" placeholder="Weight (lb)"><input id="prr" inputmode="numeric" placeholder="Reps">
          <button class="btn primary" data-addpr>Save PR</button></div></details></section>`;
    }
    if (s.measure) {
      const M = ['Weight', 'Waist', 'Hips', 'Glutes', 'Thigh', 'Arm'], cur = S.v.mMetric || 'Weight';
      const pts = S.m.filter(e => num(e[cur]) != null).map(e => ({ x: e.date.slice(0, 5), y: num(e[cur]), t: e.date }));
      html += `<section class="card"><div class="card-head"><div><span class="eyebrow">Body measurements</span><h3>Check-ins</h3></div>
        <select data-sv="mMetric" aria-label="Choose measurement">${M.map(m => `<option ${m === cur ? 'selected' : ''}>${m}</option>`).join('')}</select></div>
        ${pts.length ? chart(pts, cur === 'Weight' ? 'lb' : 'in') : '<div class="empty">Add your first check-in below. Measure every 2 weeks, same time of day.</div>'}
        <div class="form-grid">${M.map(m => `<label>${m} <small>${m === 'Weight' ? 'lb' : 'in'}</small><input inputmode="decimal" id="m-${m}"></label>`).join('')}</div>
        <button class="btn primary wide" data-addm>Save check-in</button>
        ${S.m.length ? `<div class="table-wrap"><table class="tbl"><thead><tr><th>Date</th>${M.map(m => `<th>${m}</th>`).join('')}<th></th></tr></thead><tbody>
          ${S.m.map((e, i) => `<tr><td>${esc(e.date)}</td>${M.map(m => `<td>${esc(e[m] || '—')}</td>`).join('')}<td><button class="x" data-delm="${i}" aria-label="Delete">×</button></td></tr>`).reverse().join('')}</tbody></table></div>` : ''}
      </section>`;
    }
    return html;
  },

  library() {
    const q = (S.v.lq || '').toLowerCase(), cat = S.v.lcat || 'All';
    const names = Object.keys(P.lib), cats = ['All', ...new Set(names.map(n => P.lib[n].cat))];
    const list = names.filter(n => (cat === 'All' || P.lib[n].cat === cat) && (!q || (n + ' ' + P.lib[n].m).toLowerCase().includes(q)));
    return `<div class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="lsearch" placeholder="Search ${names.length} exercises or muscles…" value="${esc(S.v.lq || '')}" aria-label="Search exercises"></div>
      <div class="chips">${cats.map(c => `<button class="${c === cat ? 'on' : ''}" data-lcat="${c}">${c}</button>`).join('')}</div>
      <div class="lib">${list.map(n => `<button class="lib-card" data-lib="${esc(n)}"><span class="eyebrow">${esc(P.lib[n].cat)}</span><b>${esc(n)}</b><small>${esc(P.lib[n].m)}</small></button>`).join('') || '<p class="muted">No exercises match.</p>'}</div>`;
  },

  tools() {
    return `<section class="card"><div class="card-head"><div><span class="eyebrow">Calculator</span><h3>Estimated 1-Rep Max</h3></div></div>
      <p class="muted">Enter a recent hard set. Uses the Epley formula: weight × (1 + reps ÷ 30).</p>
      <div class="form-grid two"><label>Weight (lb)<input inputmode="decimal" data-tool="ow" value="${esc(S.v['t:ow'] || '')}"></label><label>Reps<input inputmode="numeric" data-tool="or" value="${esc(S.v['t:or'] || '')}"></label></div>
      <div id="oneOut"></div></section>
      <section class="card"><div class="card-head"><div><span class="eyebrow">Calculator</span><h3>Warm-Up Sets</h3></div></div>
      <p class="muted">Enter your first working weight to get ramp-up sets.</p>
      <div class="form-grid two"><label>Working weight (lb)<input inputmode="decimal" data-tool="ww" value="${esc(S.v['t:ww'] || '')}"></label>
        <label>Equipment<select data-tool="wt">${[['bb', 'Barbell (45 lb bar)'], ['db', 'Dumbbells / machine']].map(([v, l]) => `<option value="${v}" ${(S.v['t:wt'] || 'bb') === v ? 'selected' : ''}>${l}</option>`).join('')}</select></label></div>
      <div id="warmOut"></div></section>
      <section class="card"><div class="card-head"><div><span class="eyebrow">Calculator</span><h3>Barbell Plate Loader</h3></div></div>
      <div class="form-grid two"><label>Target weight (lb)<input inputmode="decimal" data-tool="pw" value="${esc(S.v['t:pw'] || '')}"></label>
        <label>Bar<select data-tool="pb">${[['45', 'Standard 45 lb'], ['35', "Women's 35 lb"]].map(([v, l]) => `<option value="${v}" ${(S.v['t:pb'] || '45') === v ? 'selected' : ''}>${l}</option>`).join('')}</select></label></div>
      <div id="plateOut"></div></section>
      <section class="card"><div class="card-head"><div><span class="eyebrow">Reference</span><h3>RIR Effort Scale</h3></div></div>
      <table class="tbl"><thead><tr><th>RIR</th><th>Feels like</th></tr></thead><tbody>
      <tr><td>4+</td><td>Easy: warm-up territory</td></tr><tr><td>3</td><td>Challenging, bar speed still fast</td></tr><tr><td>2</td><td>Hard, reps start slowing</td></tr><tr><td>1</td><td>Very hard, one rep left</td></tr><tr><td>0</td><td>Failure: isolation & machines only</td></tr></tbody></table></section>`;
  },

  macro() {
    const v = k => esc(S.v['m:' + k] || '');
    const opt = (k, list, def) => list.map(([val, lab]) => `<option value="${val}" ${(S.v['m:' + k] || def) == val ? 'selected' : ''}>${lab}</option>`).join('');
    return `<section class="card"><div class="card-head"><div><span class="eyebrow">Personal calculator</span><h3>Calories & Macros</h3></div></div>
      <div class="form-grid">
        <label>Weight (lb)<input inputmode="decimal" data-m="w" value="${v('w')}" placeholder="150"></label>
        <label>Height (ft)<input inputmode="numeric" data-m="ft" value="${v('ft')}" placeholder="5"></label>
        <label>Height (in)<input inputmode="numeric" data-m="in" value="${v('in')}" placeholder="5"></label>
        <label>Age<input inputmode="numeric" data-m="age" value="${v('age')}" placeholder="28"></label>
        <label>Sex<select data-m="sex">${opt('sex', [['f', 'Female'], ['m', 'Male']], 'f')}</select></label>
        <label>Activity<select data-m="act">${opt('act', [['1.375', 'Lift 2–3×/week'], ['1.55', 'Lift 4–5×/week'], ['1.725', 'Very active']], '1.55')}</select></label>
        <label class="full">Goal<select data-m="goal">${opt('goal', [['-400', 'Lose fat (−400 kcal)'], ['0', 'Maintain / recomp'], ['250', 'Build muscle (+250 kcal)']], '0')}</select></label>
      </div><div id="macroOut"></div>
      <p class="fine">Mifflin-St Jeor equation × activity factor. Protein 0.8 g/lb (0.7 g/lb above 200 lb), fat 27% of calories, carbs make up the rest. Re-check after 2 weeks using Chapter 4 of the guide. Not medical advice.</p></section>`;
  },

  meals(s) {
    const di = +(S.v[s.id + ':day'] || 0), d = s.days[di], tot = d.meals.reduce((a, m) => a + m[2], 0);
    return `<div class="seg">${s.days.map((x, i) => `<button class="${i == di ? 'on' : ''}" data-meal="${s.id}:${i}">${x.name.slice(0, 3)}</button>`).join('')}</div>
      <section class="card"><div class="card-head"><div><span class="eyebrow">Day ${di + 1} of 7</span><h3>${esc(d.name)}</h3></div><span class="badge">~${tot} g protein</span></div>
      ${d.meals.map(m => { const rec = P.recipes && P.recipes.findIndex(r => r.n === m[1]); return `<div class="meal"><span class="eyebrow">${esc(m[0])}</span>
        <div class="meal-row"><p>${esc(m[1])}</p><span class="pill">${m[2]} g protein</span></div>${rec > -1 ? `<button class="link" data-recipe="${rec}">View recipe →</button>` : ''}</div>` }).join('')}
      <p class="fine">Adjust portions of carbs and fats (rice, oats, potatoes, oil) to land on your calories from My Macros. Protein amounts are approximate.</p></section>`;
  },

  recipes(s) {
    const f = S.v.rf || 'All', types = ['All', ...new Set(s.items.map(r => r.t))];
    return `<div class="chips">${types.map(t => `<button class="${t === f ? 'on' : ''}" data-rf="${t}">${t}</button>`).join('')}</div>
      <div class="lib">${s.items.map((r, i) => ({ r, i })).filter(({ r }) => f === 'All' || r.t === f).map(({ r, i }) => `<button class="lib-card" data-recipe="${i}"><span class="eyebrow">${esc(r.t)} · ${esc(r.time)}</span><b>${esc(r.n)}</b>
        <span class="macros-mini"><span>${r.m[0]} kcal</span><span>P ${r.m[1]}g</span><span>C ${r.m[2]}g</span><span>F ${r.m[3]}g</span></span></button>`).join('')}</div>`;
  },

  checklist: s => bar(keys(s)) + s.groups.map((g, gi) => `<section class="card"><div class="card-head"><h3>${esc(g.title)}</h3><span class="muted">${g.items.filter((_, ii) => S.d[`${s.id}:${gi}:${ii}`]).length}/${g.items.length}</span></div>${g.items.map((it, ii) => check(`${s.id}:${gi}:${ii}`, it, 'data-cl')).join('')}</section>`).join(''),

  accordion: s => `<section class="card">${s.items.map(it => `<details class="acc"><summary>${esc(it.q)}<svg viewBox="0 0 24 24" class="ic chev"><path d="m6 9 6 6 6-6"/></svg></summary><p>${esc(it.a)}</p></details>`).join('')}</section>`,

  journal: s => s.prompts.map((p, i) => `<section class="card"><span class="eyebrow">Prompt ${i + 1}</span><blockquote class="prompt">${esc(p)}</blockquote><textarea data-v="${s.id}:${i}" placeholder="Start writing…">${esc(S.v[s.id + ':' + i] || '')}</textarea></section>`).join(''),

  upsell: () => `<section class="card hero-card"><span class="eyebrow">Keep going</span><h3>Your next program</h3>
    <p class="muted">Every Get Fit With Me program is designed to work together.</p>
    <div class="ups">${P.others.filter(o => o.slug !== P.slug).map(o => `<${P.stan ? `a href="${esc(P.stan)}" target="_blank" rel="noopener"` : 'div'} class="up"><span><b>${esc(o.short)}</b><small>${esc(o.sub)}</small></span><em>${esc(o.price)}</em></${P.stan ? 'a' : 'div'}>`).join('')}</div>
    ${P.stan ? `<a class="btn primary wide" href="${esc(P.stan)}" target="_blank" rel="noopener">Visit my store</a>` : '<p class="muted center">Find them all in my store. The link is in my Instagram bio.</p>'}
    <p class="fine center">Share your progress with <b>#GetFitWithMe</b>. I love seeing it.</p></section>`,
};

function check(k, label, attr) { return `<div class="check ${S.d[k] ? 'done' : ''}" data-chk="${k}" ${attr} role="checkbox" aria-checked="${!!S.d[k]}" tabindex="0"><span class="box"><svg viewBox="0 0 24 24" class="ic"><path d="m5 12 5 5L20 7"/></svg></span><span>${esc(label)}</span></div>` }

function chart(pts, unit = 'lb') {
  const W = 640, H = 240, pl = 48, pr = 16, pt = 16, pb = 32;
  const ys = pts.map(p => p.y), lo = Math.min(...ys), hi = Math.max(...ys), pad = (hi - lo) * .15 || Math.max(5, hi * .05);
  const y0 = lo - pad, y1 = hi + pad, X = i => pl + (pts.length === 1 ? (W - pl - pr) / 2 : i * (W - pl - pr) / (pts.length - 1)), Y = v => pt + (1 - (v - y0) / (y1 - y0)) * (H - pt - pb);
  const ticks = [0, .5, 1].map(t => y0 + t * (y1 - y0));
  const line = pts.map((p, i) => `${i ? 'L' : 'M'}${X(i).toFixed(1)},${Y(p.y).toFixed(1)}`).join('');
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Progress chart">
    ${ticks.map(t => `<line x1="${pl}" x2="${W - pr}" y1="${Y(t)}" y2="${Y(t)}" class="grid"/><text x="${pl - 8}" y="${Y(t) + 4}" text-anchor="end">${fmt(t)}</text>`).join('')}
    <path d="${line} L${X(pts.length - 1)},${H - pb} L${X(0)},${H - pb}Z" class="area"/><path d="${line}" class="line"/>
    ${pts.map((p, i) => `<g><circle cx="${X(i)}" cy="${Y(p.y)}" r="5"/><title>${esc(p.t)}: ${fmt(p.y)} ${unit}</title><text x="${X(i)}" y="${H - 10}" text-anchor="middle">${esc(p.x)}</text></g>`).join('')}
  </svg>`;
}

// ---------------------------------------------------------------- layout
function render(keepScroll) {
  const cur = sec(S.v.tab) || P.sections[0];
  $$('#nav button').forEach(b => { b.classList.toggle('on', b.dataset.tab === cur.id); b.setAttribute('aria-current', b.dataset.tab === cur.id ? 'page' : 'false') });
  const y = scrollY;
  $('#main').innerHTML = `<div class="sec-head"><h2>${esc(cur.label)}</h2></div>` + R[cur.type](cur);
  if (cur.type === 'macro') calcMacros();
  if (cur.type === 'tools') calcTools();
  if (cur.type === 'guide' && S.v.ch != null) restoreQuizzes();
  const p = pct(ALL); $('#overall').style.width = p + '%'; $('#overallN').textContent = p + '%';
  if (keepScroll) scrollTo(0, y);
}

// ---------------------------------------------------------------- calculators
function calcMacros() {
  const g = k => num(S.v['m:' + k]), out = $('#macroOut');
  const w = g('w'), ft = g('ft'), inch = g('in') || 0, age = g('age');
  const sex = S.v['m:sex'] || 'f', act = num(S.v['m:act'] || 1.55), goal = num(S.v['m:goal'] || 0);
  if (!(w > 60 && ft > 3 && age > 12)) { out.innerHTML = '<div class="empty">Enter your stats to see your personal targets.</div>'; return }
  const kg = w * .4536, cm = (ft * 12 + inch) * 2.54, bmr = 10 * kg + 6.25 * cm - 5 * age + (sex === 'm' ? 5 : -161);
  const tdee = bmr * act; let cal = Math.max(Math.round((tdee + goal) / 10) * 10, sex === 'm' ? 1500 : 1200);
  const pro = Math.round(w * (w > 200 ? .7 : .8)), fat = Math.round(cal * .27 / 9), carb = Math.max(50, Math.round((cal - pro * 4 - fat * 9) / 4));
  const P4 = pro * 4, C4 = carb * 4, F9 = fat * 9, T = P4 + C4 + F9;
  out.innerHTML = `<div class="kpis"><div class="kpi big"><span>Daily calories</span><b>${fmt(cal)}</b><small>Maintenance ≈ ${fmt(tdee)} kcal</small></div>
    <div class="kpi"><span>Protein</span><b>${pro} g</b><small>${Math.round(100 * P4 / T)}% of calories</small></div>
    <div class="kpi"><span>Carbs</span><b>${carb} g</b><small>${Math.round(100 * C4 / T)}%</small></div>
    <div class="kpi"><span>Fat</span><b>${fat} g</b><small>${Math.round(100 * F9 / T)}%</small></div>
    <div class="kpi"><span>Water</span><b>${Math.round(w / 2)} oz</b><small>+12–24 oz per training hour</small></div></div>
    <div class="split"><i style="width:${100 * P4 / T}%" class="p"></i><i style="width:${100 * C4 / T}%" class="c"></i><i style="width:${100 * F9 / T}%" class="f"></i></div>
    <p class="muted">Across 4 meals: about <b>${Math.round(pro / 4)} g protein</b>, <b>${Math.round(carb / 4)} g carbs</b> and <b>${Math.round(fat / 4)} g fat</b> per meal.</p>`;
}
function calcTools() {
  const t = k => num(S.v['t:' + k]);
  const ow = t('ow'), or = t('or'), o = $('#oneOut');
  if (ow && or) {
    const m = e1rm(ow, or);
    o.innerHTML = `<div class="kpis"><div class="kpi big"><span>Estimated 1RM</span><b>${fmt(m)} lb</b></div></div>
      <table class="tbl"><thead><tr><th>Target reps</th><th>~% of 1RM</th><th>Weight</th></tr></thead><tbody>${[[1, 100], [3, 93], [5, 87], [8, 80], [10, 75], [12, 70], [15, 65]].map(([r, p]) => `<tr><td>${r}</td><td>${p}%</td><td>${fmt(m * p / 100)} lb</td></tr>`).join('')}</tbody></table>`;
  } else o.innerHTML = '';
  const ww = t('ww'), wt = S.v['t:wt'] || 'bb', w = $('#warmOut');
  if (ww) {
    const step = wt === 'bb' ? 5 : 2.5, rnd = x => Math.max(wt === 'bb' ? 45 : step, Math.round(x / step) * step);
    const plan = [[wt === 'bb' ? 45 : rnd(ww * .4), 10], [rnd(ww * .6), 6], [rnd(ww * .8), 3]]; if (ww >= 135 || (wt === 'db' && ww >= 40)) plan.push([rnd(ww * .9), 1]);
    w.innerHTML = `<table class="tbl"><thead><tr><th>Set</th><th>Weight</th><th>Reps</th></tr></thead><tbody>${plan.map((p, i) => `<tr><td>Warm-up ${i + 1}</td><td>${p[0]} lb</td><td>${p[1]}</td></tr>`).join('')}<tr class="hl"><td>Working sets</td><td>${ww} lb</td><td>As programmed</td></tr></tbody></table>`;
  } else w.innerHTML = '';
  const pw = t('pw'), pb = num(S.v['t:pb'] || 45), pe = $('#plateOut');
  if (pw && pw >= pb) {
    let side = (pw - pb) / 2; const plates = [];
    for (const p of [45, 35, 25, 10, 5, 2.5]) while (side >= p - 1e-9) { plates.push(p); side -= p }
    pe.innerHTML = `<p>Each side: ${plates.length ? plates.map(p => `<span class="plate p${String(p).replace('.', '_')}">${p}</span>`).join('') : '<b>bar only</b>'}</p>${side > .01 ? `<p class="fine">Closest loadable: ${pw - side * 2} lb</p>` : ''}`;
  } else pe.innerHTML = pw ? `<p class="fine">Target must be at least the bar weight (${pb} lb).</p>` : '';
}

// ---------------------------------------------------------------- quizzes
function restoreQuizzes() { $$('.quiz').forEach(q => { const a = S.q[q.dataset.qid]; if (a != null) markQuiz(q, a) }) }
function markQuiz(q, a) {
  const ans = +q.dataset.ans;
  $$('.opt', q).forEach((b, i) => { b.disabled = true; b.classList.toggle('right', i === ans); b.classList.toggle('wrong', i === a && a !== ans) });
  const ex = $('.qexp', q); ex.hidden = false; ex.innerHTML = `<b>${a === ans ? 'Correct.' : 'Not quite.'}</b> ${esc(q.dataset.exp)}`;
}

// ---------------------------------------------------------------- sheet (dialog)
function sheet(html) { const d = $('#sheet'); $('#sheetBody').innerHTML = html; d.showModal(); $('#sheetBody').scrollTop = 0 }
function libSheet(n) {
  const x = P.lib[n]; if (!x) return;
  const li = a => a.map(t => `<li>${esc(t)}</li>`).join('');
  sheet(`<span class="eyebrow">${esc(x.cat)} · ${esc(x.eq)}</span><h2>${esc(n)}</h2><p class="muted"><b>Muscles:</b> ${esc(x.m)}</p>
    <h4>Setup</h4><ol>${li(x.setup)}</ol><h4>Execution</h4><ol>${li(x.do)}</ol>
    <h4>Coaching cues</h4><ul class="cues">${li(x.cues)}</ul><h4>Common mistakes</h4><ul class="mist">${li(x.mist)}</ul>
    <div class="vars"><div><span class="eyebrow">Easier</span><p>${esc(x.easier)}</p></div><div><span class="eyebrow">Harder</span><p>${esc(x.harder)}</p></div><div><span class="eyebrow">Swaps</span><p>${esc(x.swap)}</p></div></div>`);
}
function recipeSheet(i) {
  const r = P.recipes[i];
  sheet(`<span class="eyebrow">${esc(r.t)} · ${esc(r.time)}</span><h2>${esc(r.n)}</h2>
    <div class="kpis four"><div class="kpi"><span>Calories</span><b>${r.m[0]}</b></div><div class="kpi"><span>Protein</span><b>${r.m[1]} g</b></div><div class="kpi"><span>Carbs</span><b>${r.m[2]} g</b></div><div class="kpi"><span>Fat</span><b>${r.m[3]} g</b></div></div>
    <h4>Ingredients</h4>${r.ing.map((g, j) => check(`rec:${i}:${j}`, g, 'data-sheetchk')).join('')}
    <h4>Method</h4><ol>${r.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol><p class="fine">Macros are approximate per serving and vary by brand.</p>`);
}
function settingsSheet() {
  const t = S.v.theme || 'auto';
  sheet(`<h2>Settings</h2>
    <h4>Appearance</h4><div class="seg">${[['auto', 'System'], ['light', 'Light'], ['dark', 'Dark']].map(([v, l]) => `<button class="${t === v ? 'on' : ''}" data-theme="${v}">${l}</button>`).join('')}</div>
    <h4>PDF book</h4><p class="muted">The printable book with fillable logs and worksheets.</p><a class="btn primary wide" href="${P.pdf}" download>Download PDF</a>
    <h4>Backup</h4><p class="muted">Your progress is saved on this device. Export a backup to move it to another phone or browser.</p>
    <div class="row-between"><button class="btn ghost" data-export>Export backup</button><label class="btn ghost">Import backup<input type="file" accept="application/json" id="importFile" hidden></label></div>
    <h4>Reset</h4><button class="btn danger wide" data-reset>Erase all progress</button>`);
}

// ---------------------------------------------------------------- events
document.addEventListener('click', ev => {
  const t = ev.target.closest('button,[data-chk],a[data-x]'); if (!t) return;
  const d = t.dataset;
  if (d.tab) { S.v.tab = d.tab; if (d.tab === 'guide') S.v.ch = null; save(); render(); scrollTo({ top: 0 }); return }
  if (d.ch != null) { S.v.ch = d.ch === 'toc' ? null : +d.ch; save(); render(); scrollTo({ top: $('#main').offsetTop - 70 }); return }
  if (d.readnext != null) {
    const i = +d.readnext; S.read[i] = true;
    if (i < P.guide.length - 1) S.v.ch = i + 1; else { S.v.ch = null; toast('Guide complete. Well done.') }
    save(); render(); scrollTo({ top: $('#main').offsetTop - 70 }); return;
  }
  if (t.classList.contains('opt')) { const q = t.closest('.quiz'), a = +d.i; S.q[q.dataset.qid] = a; save(); markQuiz(q, a); return }
  if (d.toggle) { const cur = t.getAttribute('aria-expanded') === 'true'; S.v[d.toggle] = !cur; save(); render(true); return }
  if (d.wk) { const [id, i] = d.wk.split(':'); S.v[id + ':wk'] = +i; save(); render(true); return }
  if (d.sel) { const [id, i] = d.sel.split(':'); S.v[id + ':sel'] = +i; save(); render(true); return }
  if (d.meal) { const [id, i] = d.meal.split(':'); S.v[id + ':day'] = +i; save(); render(true); return }
  if (d.lcat) { S.v.lcat = d.lcat; save(); render(true); return }
  if (d.rf) { S.v.rf = d.rf; save(); render(true); return }
  if (d.lib) { libSheet(d.lib); return }
  if (d.recipe != null) { recipeSheet(+d.recipe); return }
  if (d.flag) { S.d[d.flag] = !S.d[d.flag]; save(); t.classList.toggle('on', S.d[d.flag]); return }
  if (d.set) {
    const row = t.closest('.set'), wIn = row.querySelector('[data-v$=":w"]'), rIn = row.querySelector('[data-v$=":r"]');
    S.d[d.set] = !S.d[d.set];
    if (S.d[d.set]) { // fill from placeholders so a tap logs the set
      if (!wIn.value && wIn.placeholder) { wIn.value = wIn.placeholder; S.v[wIn.dataset.v] = wIn.value }
      if (!rIn.value && /^\d+$/.test(rIn.placeholder)) { rIn.value = rIn.placeholder; S.v[rIn.dataset.v] = rIn.value }
    }
    save(); row.classList.toggle('on', S.d[d.set]);
    const cnt = t.closest('.day').querySelector('.day-count'), all = $$('.set', t.closest('.day'));
    cnt.textContent = `${all.filter(s => s.classList.contains('on')).length}/${all.length} sets`;
    if (S.d[d.set]) { tone(880, .08); const s2 = parseRest(d.rest); if (s2) startTimer(s2) }
    return;
  }
  if (d.day) {
    S.d[d.day] = !S.d[d.day];
    if (S.d[d.day]) {
      S.v['open:' + d.day] = false;
      const [sid, wi, di] = d.day.split(':'), s = sec(sid), day = s.weeks[wi].days[di];
      let sets = 0, vol = 0;
      day.ex.forEach((e, ei) => { for (let si = 0; si < e.s; si++) { const k = setKey(sid, wi, di, ei, si), w = num(S.v[k + ':w']), r = num(S.v[k + ':r']); if (S.d[k]) sets++; if (w && r) vol += w * r } });
      chime(); toast(`${day.name.split('·')[0].trim()} complete · ${sets} sets${vol ? ` · ${fmt(vol)} lb total volume` : ''}`);
    }
    save(); render(true); return;
  }
  if (d.chk) {
    if (d.sheetchk != null) { S.d[d.chk] = !S.d[d.chk]; save(); t.classList.toggle('done', S.d[d.chk]); return }
    S.d[d.chk] = !S.d[d.chk];
    if (d.task) {
      const [id, i] = d.task.split(':'), s = sec(id), was = S.d[d.task];
      S.d[d.task] = s.tasks.every((_, ti) => S.d[`${id}:${i}:t${ti}`]);
      if (S.d[d.task] && !was) { chime(); toast(`Day ${+i + 1} complete`) }
    }
    save(); render(true); return;
  }
  if (d.addpr != null) {
    const w = num($('#prw').value), r = num($('#prr').value) || 1;
    if (!w) { toast('Enter a weight first'); return }
    S.pr.push({ l: $('#prl').value, w, r, date: new Date().toLocaleDateString() }); save(); render(true); chime(); toast('PR saved'); return;
  }
  if (d.addm != null) {
    const e = { date: new Date().toLocaleDateString() }; let any = false;
    ['Weight', 'Waist', 'Hips', 'Glutes', 'Thigh', 'Arm'].forEach(m => { const v = $('#m-' + m).value.trim(); if (v) { e[m] = v; any = true } });
    if (!any) { toast('Enter at least one measurement'); return }
    S.m.push(e); save(); render(true); toast('Check-in saved'); return;
  }
  if (d.delm != null) { if (confirm('Delete this check-in?')) { S.m.splice(+d.delm, 1); save(); render(true) } return }
  if (d.theme) { S.v.theme = d.theme; save(); applyTheme(); $$('[data-theme]', $('#sheet')).forEach(b => b.classList.toggle('on', b.dataset.theme === d.theme)); return }
  if (d.export != null) {
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify(S)], { type: 'application/json' }));
    a.download = `${P.slug}-backup-${new Date().toISOString().slice(0, 10)}.json`; a.click(); return;
  }
  if (d.reset != null) { if (confirm('Erase all progress for this program? This cannot be undone.')) { S = { d: {}, v: {}, q: {}, read: {}, pr: [], m: [] }; save(); $('#sheet').close(); applyTheme(); render() } return }
  if (t.id === 'settingsBtn' || t.id === 'settingsBtn2') { settingsSheet(); return }
  if (t.id === 'sheetClose') { $('#sheet').close(); return }
});
document.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.dataset && e.target.dataset.chk) { e.preventDefault(); e.target.click() } });
document.addEventListener('input', e => {
  const d = e.target.dataset;
  if (d.v) { S.v[d.v] = e.target.value; save() }
  if (d.m) { S.v['m:' + d.m] = e.target.value; save(); calcMacros() }
  if (d.tool) { S.v['t:' + d.tool] = e.target.value; save(); calcTools() }
  if (e.target.id === 'gsearch' || e.target.id === 'lsearch') {
    S.v[e.target.id === 'gsearch' ? 'gq' : 'lq'] = e.target.value; save();
    const pos = e.target.selectionStart, id = e.target.id; render(true); const n = $('#' + id); n.focus(); n.setSelectionRange(pos, pos);
  }
});
document.addEventListener('change', e => {
  const d = e.target.dataset;
  if (d.m) { S.v['m:' + d.m] = e.target.value; save(); calcMacros() }
  if (d.tool) { S.v['t:' + d.tool] = e.target.value; save(); calcTools() }
  if (d.sv) { S.v[d.sv] = e.target.value; save(); render(true) }
  if (e.target.id === 'importFile' && e.target.files[0]) {
    e.target.files[0].text().then(txt => { try { const o = JSON.parse(txt); if (!o.d || !o.v) throw 0; S = o; save(); applyTheme(); $('#sheet').close(); render(); toast('Backup restored') } catch (_) { toast('That file is not a valid backup') } });
  }
});
$('#sheet').addEventListener('click', e => { if (e.target.id === 'sheet') $('#sheet').close() });

// ---------------------------------------------------------------- rest timer
let tEnd = 0, tInt = 0, tTotal = 0;
function parseRest(r) { const m = /([\d.]+)\s*(min|s)/.exec(r || ''); return m ? Math.round(parseFloat(m[1]) * (m[2] === 'min' ? 60 : 1)) : 0 }
function startTimer(s) { clearInterval(tInt); tTotal = s; tEnd = Date.now() + s * 1000; $('#timer').classList.add('open', 'run'); tick(); tInt = setInterval(tick, 250) }
function tick() {
  const left = Math.max(0, (tEnd - Date.now()) / 1000), L = Math.ceil(left);
  $('#tnum').textContent = Math.floor(L / 60) + ':' + String(L % 60).padStart(2, '0');
  $('#tring').style.strokeDashoffset = 283 * (1 - left / (tTotal || 1));
  if (!L) { clearInterval(tInt); $('#timer').classList.remove('run'); $('#tnum').textContent = 'Go'; [0, .25, .5].forEach(w => tone(988, .16, w, 'square', .06)); try { navigator.vibrate && navigator.vibrate([200, 100, 200]) } catch (_) {} }
}
if ($('#tfab')) {
  $('#tfab').onclick = () => $('#timer').classList.toggle('open');
  $('#timer').addEventListener('click', e => {
    const b = e.target.closest('[data-t]'); if (!b) return;
    if (b.dataset.t === 'stop') { clearInterval(tInt); $('#timer').classList.remove('run'); $('#tnum').textContent = '0:00'; $('#tring').style.strokeDashoffset = 0 }
    else if (b.dataset.t === '+15') { if (tEnd > Date.now()) { tEnd += 15000; tTotal += 15 } else startTimer(15) }
    else if (b.dataset.t === 'hide') $('#timer').classList.remove('open');
    else startTimer(+b.dataset.t);
  });
}

// ---------------------------------------------------------------- sound + toast
let AC;
function tone(f, d, when = 0, type = 'sine', vol = .12) {
  try {
    AC = AC || new (window.AudioContext || window.webkitAudioContext)();
    const o = AC.createOscillator(), g = AC.createGain(), t0 = AC.currentTime + when;
    o.type = type; o.frequency.value = f; g.gain.setValueAtTime(vol, t0); g.gain.exponentialRampToValueAtTime(.001, t0 + d);
    o.connect(g).connect(AC.destination); o.start(t0); o.stop(t0 + d);
  } catch (e) {}
}
const chime = () => [523, 659, 784].forEach((f, i) => tone(f, .3, i * .09, 'triangle', .08));
function toast(m) { const t = $('#toast'); t.textContent = m; t.classList.add('show'); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 2800) }

render();
