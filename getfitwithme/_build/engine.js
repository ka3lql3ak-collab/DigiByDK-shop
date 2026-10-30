// Get Fit With Me product engine — renders the P object into an interactive app.
const KEY = 'gfwm_' + P.slug;
let S = {};
try { S = JSON.parse(localStorage.getItem(KEY)) || {} } catch (e) {}
S.d = S.d || {}; S.v = S.v || {}; S.pr = S.pr || [];
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)) } catch (e) {} };
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const HYPE = ['THAT\'S MY GIRL 🔥', 'Strong AND cute 💅🏽', 'Booty gains loading… 🍑', 'Another one! 💪🏽', 'You showed UP 👑', 'Main character energy ✨', 'The gym is YOURS 😤', 'Proud of you, baddie 💜'];
const hype = () => HYPE[Math.random() * HYPE.length | 0];

// ---------- completion keys for progress
function keys(sec) {
  if (sec.type === 'program') return sec.weeks.flatMap((w, wi) => w.days.map((_, di) => `${sec.id}:${wi}:${di}`));
  if (sec.type === 'challenge') return sec.days.map((_, i) => `${sec.id}:${i}`);
  if (sec.type === 'checklist') return sec.groups.flatMap((g, gi) => g.items.map((_, ii) => `${sec.id}:${gi}:${ii}`));
  return [];
}
const ALL = P.sections.flatMap(keys);
function pct(list) { return list.length ? Math.round(100 * list.filter(k => S.d[k]).length / list.length) : 0 }
function updRing() {
  const p = pct(ALL), r = $('#ring');
  if (!r) return;
  r.style.setProperty('--p', p);
  $('#ringn').textContent = p + '%';
}

// ---------- section renderers
const R = {
  intro: s => `<div class="card glow">${s.html}<p class="sig">— Danielle 💜</p></div>`,

  program(s) {
    const wi = +(S.v[s.id + ':wk'] || 0), wk = s.weeks[wi];
    const chips = s.weeks.length > 1 ? `<div class="chips">${s.weeks.map((w, i) => {
      const done = w.days.every((_, di) => S.d[`${s.id}:${i}:${di}`]);
      return `<button class="chip ${i == wi ? 'on' : ''} ${done ? 'done' : ''}" data-wk="${s.id}:${i}">${done ? '✓ ' : ''}${esc(w.name)}</button>`
    }).join('')}</div>` : '';
    return `${bar(keys(s))}${chips}
    <div class="phase"><span class="tag">${esc(wk.phase)}</span>${esc(wk.note)}</div>
    ${wk.days.map((d, di) => {
      const k = `${s.id}:${wi}:${di}`, done = S.d[k];
      return `<div class="card day ${done ? 'complete' : ''}">
        <div class="dayhead"><div><h3>${esc(d.name)}</h3><p class="muted">${esc(d.focus)}</p></div>${done ? '<span class="stamp">CRUSHED IT</span>' : ''}</div>
        ${d.ex.map((e, ei) => {
          const ek = `${k}:${ei}`;
          return `<div class="ex">
            <div class="exhead"><b>${esc(e.n)}</b><span class="pill">${e.s} × ${esc(e.r)}</span><span class="pill ghost">⏱ ${esc(e.rest)}</span></div>
            <div class="exrow"><div class="sets">${Array.from({ length: e.s }, (_, si) =>
              `<button class="set ${S.d[ek + ':' + si] ? 'on' : ''}" data-set="${ek}:${si}" data-rest="${esc(e.rest)}" aria-label="Set ${si + 1}">${S.d[ek + ':' + si] ? '✓' : si + 1}</button>`).join('')}</div>
            <label class="wt">lbs <input inputmode="decimal" data-v="${ek}:w" value="${esc(S.v[ek + ':w'] || '')}" placeholder="—"></label></div>
            ${e.tip ? `<details><summary>Form tip</summary><p>${esc(e.tip)}</p></details>` : ''}
          </div>`
        }).join('')}
        <button class="btn big ${done ? 'ghost' : ''}" data-day="${k}">${done ? '↺ Undo' : 'WORKOUT COMPLETE 🔥'}</button>
      </div>`
    }).join('')}`;
  },

  challenge(s) {
    const sel = +(S.v[s.id + ':sel'] || 0), d = s.days[sel];
    let streak = 0; while (streak < s.days.length && S.d[`${s.id}:${streak}`]) streak++;
    const done = s.days.filter((_, i) => S.d[`${s.id}:${i}`]).length;
    return `${bar(keys(s))}
    <div class="stats"><div><b>${done}</b><span>days done</span></div><div><b>🔥 ${streak}</b><span>day streak</span></div><div><b>${30 - done}</b><span>to go</span></div></div>
    <div class="grid30">${s.days.map((x, i) => `<button class="dbtn ${i == sel ? 'sel' : ''} ${S.d[s.id + ':' + i] ? 'on' : ''}" data-sel="${s.id}:${i}">${S.d[s.id + ':' + i] ? '✓' : i + 1}</button>`).join('')}</div>
    <div class="card day ${S.d[s.id + ':' + sel] ? 'complete' : ''}">
      <div class="dayhead"><div><p class="eyebrow">DAY ${sel + 1}</p><h3>${esc(d.t)}</h3></div>${S.d[s.id + ':' + sel] ? '<span class="stamp">DONE</span>' : ''}</div>
      ${d.rounds ? `<p class="muted">Do <b>${d.rounds} rounds</b> of the circuit. Rest 60s between rounds.</p>` : ''}
      <ul class="moves">${d.ex.map(e => `<li><span>${esc(e.n)}</span><b>${esc(e.r)}</b></li>`).join('')}</ul>
      <h4>Today's non-negotiables</h4>
      ${s.tasks.map((t, ti) => check(`${s.id}:${sel}:t${ti}`, t, `data-task="${s.id}:${sel}"`)).join('')}
      <h4>Mindset</h4><p class="prompt">“${esc(d.prompt)}”</p>
      <textarea data-v="${s.id}:${sel}:j" placeholder="Write it out, babe…">${esc(S.v[s.id + ':' + sel + ':j'] || '')}</textarea>
    </div>`;
  },

  checklist: s => bar(keys(s)) + s.groups.map((g, gi) => `<div class="card"><h3>${esc(g.title)}</h3>${g.items.map((it, ii) => check(`${s.id}:${gi}:${ii}`, it, 'data-cl')).join('')}</div>`).join(''),

  accordion: s => `<div class="card">${s.items.map(it => `<details class="acc"><summary>${esc(it.q)}</summary><p>${esc(it.a)}</p></details>`).join('')}</div>`,

  cards: s => `<div class="tiles">${s.items.map(c => `<div class="tile"><div class="ti">${c.i}</div><h4>${esc(c.t)}</h4><p>${esc(c.d)}</p></div>`).join('')}</div>`,

  journal: s => s.prompts.map((p, i) => `<div class="card"><p class="prompt">“${esc(p)}”</p><textarea data-v="${s.id}:${i}" placeholder="Start writing…">${esc(S.v[s.id + ':' + i] || '')}</textarea></div>`).join(''),

  macro(s) {
    const v = k => esc(S.v['m:' + k] || '');
    const opt = (k, list, def) => list.map(([val, lab]) => `<option value="${val}" ${(S.v['m:' + k] || def) == val ? 'selected' : ''}>${lab}</option>`).join('');
    return `<div class="card glow"><h3>Calculate your macros 🧮</h3>
      <div class="form">
        <label>Weight (lbs)<input inputmode="decimal" data-m="w" value="${v('w')}" placeholder="150"></label>
        <label>Height (ft)<input inputmode="numeric" data-m="ft" value="${v('ft')}" placeholder="5"></label>
        <label>Height (in)<input inputmode="numeric" data-m="in" value="${v('in')}" placeholder="5"></label>
        <label>Age<input inputmode="numeric" data-m="age" value="${v('age')}" placeholder="27"></label>
        <label>Sex<select data-m="sex">${opt('sex', [['f', 'Female'], ['m', 'Male']], 'f')}</select></label>
        <label>Activity<select data-m="act">${opt('act', [['1.375', 'Lift 2–3x/week'], ['1.55', 'Lift 4–5x/week'], ['1.725', 'Daily training / active job']], '1.55')}</select></label>
        <label class="full">Goal<select data-m="goal">${opt('goal', [['-400', '🔥 Lose fat (snatched era)'], ['0', '⚖️ Maintain & tone (recomp)'], ['250', '🍑 Build muscle (booty gains)']], '0')}</select></label>
      </div>
      <div id="macroOut"></div>
      <p class="fine">Uses the Mifflin-St Jeor equation. Re-check every 4 weeks or every 5 lbs of change. Not medical advice.</p></div>`;
  },

  meals(s) {
    const di = +(S.v[s.id + ':day'] || 0), d = s.days[di];
    const tot = d.meals.reduce((a, m) => a + m[2], 0);
    return `<div class="chips">${s.days.map((x, i) => `<button class="chip ${i == di ? 'on' : ''}" data-meal="${s.id}:${i}">${x.name}</button>`).join('')}</div>
      <div class="card"><div class="dayhead"><h3>${d.name} · ~${tot}g protein</h3></div>
      ${d.meals.map(m => `<div class="meal"><span class="eyebrow">${m[0]}</span><p>${esc(m[1])}</p><span class="pill">${m[2]}g protein</span></div>`).join('')}
      <p class="fine">Adjust portions (rice, oats, potatoes, oil) up or down to hit your calories from the macro calculator.</p></div>`;
  },

  pr(s) {
    const best = {};
    S.pr.forEach(r => { if (r.sec === s.id) { const e = s.metric ? r.w : r.w * (1 + r.r / 30); if (!best[r.l] || (s.metric ? false : e > best[r.l].e)) best[r.l] = { ...r, e } } });
    const rows = S.pr.map((r, i) => ({ ...r, i })).filter(r => r.sec === s.id).reverse();
    return `<div class="card glow"><h3>${s.metric ? 'Log a measurement 📏' : 'Log a new PR 👑'}</h3>
      <div class="form">
        <label class="full">${s.metric ? 'What' : 'Lift'}<select id="prl-${s.id}">${s.lifts.map(l => `<option>${esc(l)}</option>`).join('')}</select></label>
        <label>${s.metric ? 'Value' : 'Weight (lbs)'}<input id="prw-${s.id}" inputmode="decimal" placeholder="${s.metric ? '28' : '75'}"></label>
        ${s.metric ? '' : `<label>Reps<input id="prr-${s.id}" inputmode="numeric" placeholder="5"></label>`}
      </div>
      <button class="btn big" data-addpr="${s.id}" data-metric="${s.metric ? 1 : 0}">${s.metric ? 'SAVE IT 📏' : 'ADD TO THE WALL 👑'}</button></div>
      ${s.metric ? '' : `<div class="tiles">${s.lifts.map(l => `<div class="tile ${best[l] ? 'gold' : ''}"><div class="ti">${best[l] ? '👑' : '🔒'}</div><h4>${esc(l)}</h4><p>${best[l] ? `<b class="big">${best[l].w} lbs × ${best[l].r}</b><br>est. 1-rep max ≈ ${Math.round(best[l].e)} lbs` : 'No PR yet'}</p></div>`).join('')}</div>`}
      <div class="card"><h3>History</h3>${rows.length ? rows.map(r => `<div class="hist"><span>${esc(r.date)}</span><b>${esc(r.l)}</b><span>${r.w}${s.metric ? '' : ' lbs × ' + r.r}</span><button class="x" data-delpr="${r.i}" aria-label="Delete">✕</button></div>`).join('') : '<p class="muted">Nothing yet. Go make history, baddie.</p>'}</div>`;
  },

  upsell: () => `<div class="card glow center"><p class="script">you did that</p><h3>Ready for your next level?</h3>
    <p>Every Get Fit With Me program is built to work together. Keep the momentum going 💜</p>
    <div class="ups">${OTHERS.filter(o => o.slug !== P.slug).map(o => `<a class="up" href="index.html#${o.slug}"><span>${o.emoji}</span><b>${esc(o.short)}</b><em>${esc(o.price)}</em></a>`).join('')}</div>
    <a class="btn big" href="index.html">VISIT THE STORE 🛍️</a>
    <p class="muted">Tag me on Instagram & TikTok with <b>#GetFitWithMe</b> so I can hype you up!</p></div>`,
};

function bar(list) { const p = pct(list); return `<div class="bar"><i style="width:${p}%"></i><span>${p}% complete</span></div>` }
function check(k, label, attr) { return `<div class="check ${S.d[k] ? 'done' : ''}" data-chk="${k}" ${attr} role="checkbox" aria-checked="${!!S.d[k]}" tabindex="0"><span class="box">${S.d[k] ? '✓' : ''}</span><span>${esc(label)}</span></div>` }

// ---------- layout
function renderNav() {
  const cur = S.v.tab || P.sections[0].id;
  $('#nav').innerHTML = P.sections.map(s => `<button class="tab ${s.id === cur ? 'on' : ''}" data-tab="${s.id}"><span>${s.icon}</span>${esc(s.label)}</button>`).join('');
}
function render() {
  const cur = P.sections.find(s => s.id === (S.v.tab || P.sections[0].id)) || P.sections[0];
  $('#main').innerHTML = `<h2 class="sectitle">${cur.icon} ${esc(cur.label)}</h2>` + R[cur.type](cur);
  if (cur.type === 'macro') calcMacros();
  renderNav(); updRing();
}

function calcMacros() {
  const g = k => parseFloat(S.v['m:' + k]), out = $('#macroOut');
  const w = g('w'), ft = g('ft'), inch = g('in') || 0, age = g('age');
  const sex = S.v['m:sex'] || 'f', act = parseFloat(S.v['m:act'] || 1.55), goal = parseFloat(S.v['m:goal'] || 0);
  if (!(w > 60 && ft > 3 && age > 12)) { out.innerHTML = '<p class="muted center">Fill in your stats to see your numbers ✨</p>'; return }
  const kg = w * 0.4536, cm = (ft * 12 + inch) * 2.54;
  const bmr = 10 * kg + 6.25 * cm - 5 * age + (sex === 'm' ? 5 : -161);
  let cal = Math.round((bmr * act + goal) / 10) * 10;
  cal = Math.max(cal, sex === 'm' ? 1500 : 1200);
  const pro = Math.round(w * (w > 200 ? 0.7 : 0.8)), fat = Math.round(cal * 0.27 / 9);
  const carb = Math.max(50, Math.round((cal - pro * 4 - fat * 9) / 4)), water = Math.round(w / 2);
  out.innerHTML = `<div class="macros">
    <div class="mac cal"><b>${cal.toLocaleString()}</b><span>calories</span></div>
    <div class="mac"><b>${pro}g</b><span>protein</span></div>
    <div class="mac"><b>${carb}g</b><span>carbs</span></div>
    <div class="mac"><b>${fat}g</b><span>fat</span></div>
    <div class="mac"><b>${water} oz</b><span>water</span></div></div>
    <p class="center">That's about <b>${Math.round(pro / 4)}g protein per meal</b> across 4 meals 🍗</p>`;
}

// ---------- events
document.addEventListener('click', e => {
  const t = e.target.closest('button,[data-chk]'); if (!t) return;
  const d = t.dataset;
  if (d.tab) { S.v.tab = d.tab; save(); render(); scrollTo({ top: $('#nav').offsetTop - 8, behavior: 'smooth' }); return }
  if (d.wk) { const [id, i] = d.wk.split(':'); S.v[id + ':wk'] = +i; save(); render(); return }
  if (d.sel) { const [id, i] = d.sel.split(':'); S.v[id + ':sel'] = +i; save(); render(); return }
  if (d.meal) { const [id, i] = d.meal.split(':'); S.v[id + ':day'] = +i; save(); render(); return }
  if (d.set) {
    S.d[d.set] = !S.d[d.set]; save(); t.classList.toggle('on', S.d[d.set]);
    t.textContent = S.d[d.set] ? '✓' : (+d.set.split(':').pop() + 1);
    if (S.d[d.set]) { blip(); const sec = parseRest(d.rest); if (sec) startTimer(sec) }
    return;
  }
  if (d.day) {
    S.d[d.day] = !S.d[d.day]; save(); render();
    if (S.d[d.day]) { confetti(); toast(hype()); chime() }
    return;
  }
  if (d.chk) {
    S.d[d.chk] = !S.d[d.chk]; save();
    if (d.task) {
      const [id, i] = d.task.split(':'), sec = P.sections.find(s => s.id === id);
      const all = sec.tasks.every((_, ti) => S.d[`${id}:${i}:t${ti}`]), was = S.d[d.task];
      S.d[d.task] = all; save(); render();
      if (all && !was) { confetti(); chime(); toast(`DAY ${+i + 1} DONE ${hype()}`) }
      return;
    }
    render(); if (S.d[d.chk]) blip();
    if (d.cl !== undefined) {
      const id = d.chk.split(':')[0], sec = P.sections.find(s => s.id === id);
      if (keys(sec).every(k => S.d[k]) && S.d[d.chk]) { confetti(); toast('ALL DONE ✨ ' + hype()) }
    }
    return;
  }
  if (d.addpr) {
    const id = d.addpr, w = parseFloat($('#prw-' + id).value), r = d.metric === '1' ? 0 : parseInt($('#prr-' + id).value || '1');
    if (!(w > 0)) { toast('Add a number first, babe 😉'); return }
    S.pr.push({ sec: id, l: $('#prl-' + id).value, w, r, date: new Date().toLocaleDateString() }); save(); render();
    confetti(); chime(); toast(d.metric === '1' ? 'Logged 📏 progress is progress!' : 'NEW PR 👑 ' + hype());
    return;
  }
  if (d.delpr !== undefined) { if (confirm('Delete this entry?')) { S.pr.splice(+d.delpr, 1); save(); render() } return }
});
document.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.dataset.chk) { e.preventDefault(); e.target.click() } });
document.addEventListener('input', e => {
  const d = e.target.dataset;
  if (d.v) { S.v[d.v] = e.target.value; save() }
  if (d.m) { S.v['m:' + d.m] = e.target.value; save(); calcMacros() }
});
document.addEventListener('change', e => { const d = e.target.dataset; if (d.m) { S.v['m:' + d.m] = e.target.value; save(); calcMacros() } });

// ---------- rest timer
let tEnd = 0, tInt = 0;
function parseRest(r) { const m = /([\d.]+)\s*(min|s)/.exec(r || ''); return m ? Math.round(parseFloat(m[1]) * (m[2] === 'min' ? 60 : 1)) : 0 }
function startTimer(sec) {
  clearInterval(tInt); tEnd = Date.now() + sec * 1000; $('#timer').classList.add('open', 'run'); tick(); tInt = setInterval(tick, 250);
}
function tick() {
  const left = Math.max(0, Math.ceil((tEnd - Date.now()) / 1000));
  $('#tnum').textContent = Math.floor(left / 60) + ':' + String(left % 60).padStart(2, '0');
  if (!left) { clearInterval(tInt); $('#timer').classList.remove('run'); $('#tnum').textContent = 'GO! 💪🏽'; alarm(); try { navigator.vibrate && navigator.vibrate([200, 100, 200]) } catch (e) {} toast('Rest over — get back under that weight 😤') }
}
$('#tfab').onclick = () => $('#timer').classList.toggle('open');
$('#timer').addEventListener('click', e => {
  const b = e.target.closest('[data-t]'); if (!b) return;
  if (b.dataset.t === 'stop') { clearInterval(tInt); $('#timer').classList.remove('run'); $('#tnum').textContent = '0:00' }
  else if (b.dataset.t === '+15') { if (tEnd > Date.now()) tEnd += 15000; else startTimer(15) }
  else startTimer(+b.dataset.t);
});

// ---------- sound + confetti
let AC;
function tone(f, d, when = 0, type = 'sine', vol = .15) {
  try {
    AC = AC || new (window.AudioContext || window.webkitAudioContext)();
    const o = AC.createOscillator(), g = AC.createGain(), t = AC.currentTime + when;
    o.type = type; o.frequency.value = f; g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(.001, t + d);
    o.connect(g).connect(AC.destination); o.start(t); o.stop(t + d);
  } catch (e) {}
}
const blip = () => tone(880, .12);
const chime = () => [523, 659, 784, 1047].forEach((f, i) => tone(f, .35, i * .1, 'triangle'));
const alarm = () => [0, .25, .5].forEach(w => tone(988, .18, w, 'square', .08));
function confetti(n = 160) {
  const c = $('#confetti'), x = c.getContext('2d'); c.width = innerWidth; c.height = innerHeight;
  const C = [P.c1, P.c2, '#ffd36e', '#ffffff', '#b0173d'];
  const ps = Array.from({ length: n }, () => ({ x: c.width / 2 + (Math.random() - .5) * 200, y: c.height * .55, vx: (Math.random() - .5) * 14, vy: -8 - Math.random() * 12, r: Math.random() * 6, c: C[Math.random() * C.length | 0], s: 6 + Math.random() * 8 }));
  let f = 0;
  (function loop() {
    x.clearRect(0, 0, c.width, c.height);
    ps.forEach(p => { p.x += p.vx; p.y += p.vy; p.vy += .35; p.vx *= .99; p.r += .15; x.save(); x.translate(p.x, p.y); x.rotate(p.r); x.fillStyle = p.c; x.fillRect(-p.s / 2, -p.s / 4, p.s, p.s / 2); x.restore() });
    if (++f < 200) requestAnimationFrame(loop); else x.clearRect(0, 0, c.width, c.height);
  })();
}
function toast(m) { const t = $('#toast'); t.textContent = m; t.classList.add('show'); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 2400) }

$('#reset').onclick = () => { if (confirm('Erase ALL your progress in this program? This cannot be undone.')) { S = { d: {}, v: {}, pr: [] }; save(); render() } };
render();
