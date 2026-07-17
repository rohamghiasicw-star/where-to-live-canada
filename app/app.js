/* WHERE TO LIVE / CANADA. DATA and MAPGEO injected by src/build_app.py */

const $ = (s, r = document) => r.querySelector(s);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const M = ['J','F','M','A','M','J','J','A','S','O','N','D'];
const cv = (p, el, m = '13') => (p.climate && p.climate[el]) ? p.climate[el][m] : null;
const NA = '..';   // StatCan's published symbol for "not available", not an invented dash
const near = (x, t, tol) => x == null ? null : clamp(1 - Math.abs(x - t) / tol, 0, 1);

/* ---------- the dimensions ----------
   Each is one column of the plate, in a fixed order that never changes.
   `show` renders the value; a place with no data still gets its cell. */
const Q = [
  {
    id: 'winter', g: 'Climate', label: 'Winter', col: 'Jan', hint: 'The January you want to wake up in.',
    kind: 'range', min: -26, max: 6, step: 1, def: -5, w: 2,
    fmt: (v) => `${v > 0 ? '+' : ''}${v}°`, ends: ['Deep freeze', 'No winter'],
    score: (p, v) => near(cv(p, 'tmean', '1'), v, 16),
    show: (p) => { const x = cv(p, 'tmean', '1'); return x == null ? null : [x.toFixed(1), '°']; },
  },
  {
    id: 'summer', g: 'Climate', label: 'Summer', col: 'Jul', hint: 'And the July.',
    kind: 'range', min: 12, max: 24, step: 1, def: 20, w: 1,
    fmt: (v) => `${v}°`, ends: ['Cool', 'Hot'],
    score: (p, v) => near(cv(p, 'tmean', '7'), v, 7),
    show: (p) => { const x = cv(p, 'tmean', '7'); return x == null ? null : [x.toFixed(1), '°']; },
  },
  {
    id: 'snow', g: 'Climate', label: 'Snow', col: 'Snow', hint: 'How much shovelling.',
    kind: 'opts', def: 'some', w: 1,
    opts: [['none','As little as possible'],['some','Some is fine'],['lots','Bring it on']],
    score: (p, v) => {
      const s = cv(p, 'snow'); if (s == null) return null;
      if (v === 'none') return clamp(1 - s / 250, 0, 1);
      if (v === 'lots') return clamp(s / 400, 0, 1);
      return clamp(1 - Math.abs(s - 170) / 220, 0, 1);
    },
    show: (p) => { const x = cv(p, 'snow'); return x == null ? null : [Math.round(x), 'cm']; },
  },
  {
    id: 'sun', g: 'Climate', label: 'Sun', col: 'Sun', hint: 'Hours of it a year.',
    kind: 'opts', def: 'yes', w: 1, opts: [['yes','I need sun'],['meh','Not fussed']],
    score: (p, v) => { const s = cv(p, 'sun'); if (s == null || v === 'meh') return null;
      return clamp((s - 1500) / 1000, 0, 1); },
    show: (p) => { const x = cv(p, 'sun'); return x == null ? null : [Math.round(x), 'h']; },
  },
  {
    id: 'smoke', g: 'Climate', label: 'Wildfire smoke', col: 'Smoke',
    hint: 'Modelled smoke from fire only, 12-year average.',
    kind: 'opts', def: 'less', w: 2,
    opts: [['deal','Dealbreaker'],['less','Prefer less'],['meh','Not fussed']],
    score: (p, v) => { const s = p.smoke ? p.smoke.mean_ugm3 : null;
      if (s == null || v === 'meh') return null; return clamp(1 - s / 2.6, 0, 1); },
    hard: (p, v) => v === 'deal' && p.smoke && p.smoke.mean_ugm3 > 1.5,
    hardWhy: 'the smoke',
    show: (p) => p.smoke ? [p.smoke.mean_ugm3.toFixed(2), ''] : null,
  },
  {
    id: 'size', g: 'The place', label: 'Size', col: 'People', hint: 'How big a place.',
    kind: 'opts', def: 'small', w: 2,
    opts: [['village','Village'],['town','Town'],['small','Small city'],['mid','Mid city'],['big','Big city']],
    score: (p, v) => { if (p.pop == null) return null;
      const t = { village:3.4, town:4.1, small:4.8, mid:5.4, big:6.2 }[v];
      return near(Math.log10(Math.max(p.pop, 300)), t, 1.5); },
    show: (p) => p.pop == null ? null : [fmtNum(p.pop), ''],
  },
  {
    id: 'prox', g: 'The place', label: 'Near a city', col: 'Drive', hint: 'To the nearest metro over 300,000.',
    kind: 'opts', def: 'hour', w: 2,
    opts: [['in','In one'],['hour','Within an hour'],['half','Half a day is fine'],['far','As far as possible']],
    score: (p, v) => { const d = p.prox ? p.prox.drive_min_to_big_city : null; if (d == null) return null;
      if (v === 'in') return near(d, 0, 70);
      if (v === 'hour') return near(d, 45, 110);
      if (v === 'half') return near(d, 180, 260);
      return clamp(d / 420, 0, 1); },
    show: (p) => { const d = p.prox ? p.prox.drive_min_to_big_city : null;
      return d == null ? null : (d === 0 ? ['here', ''] : [Math.round(d), 'm']); },
  },
  {
    id: 'cost', g: 'The place', label: 'Housing budget', col: 'Home', hint: 'What you can pay.',
    kind: 'range', min: 200, max: 1400, step: 25, def: 600, w: 2,
    fmt: (v) => `$${v}k`, ends: ['$200k', '$1.4M'],
    score: (p, v) => { const h = p.cost ? p.cost.home_price : null; if (h == null) return null;
      const b = v * 1000;
      return h <= b ? clamp(0.6 + 0.4 * (1 - h / b), 0, 1) : clamp(0.6 * (1 - (h - b) / b), 0, 0.6); },
    hard: (p, v) => p.cost && p.cost.home_price != null && p.cost.home_price > v * 1000 * 1.6,
    hardWhy: 'the price',
    show: (p) => (p.cost && p.cost.home_price) ? [fmtNum(p.cost.home_price), ''] : null,
  },
  {
    id: 'politics', g: 'The place', label: 'Politics', col: 'Lean', hint: 'Vote-weighted lean of the federal riding, 2025.',
    kind: 'opts', def: 'meh', w: 1,
    opts: [['left','Left'],['centre','Centre'],['right','Right'],['meh','Not fussed']],
    score: (p, v) => { const l = p.politics ? p.politics.lean : null;
      if (l == null || v === 'meh') return null;
      return near(l, { left:-55, centre:0, right:55 }[v], 95); },
    show: (p) => p.politics && p.politics.lean != null
      ? [(p.politics.lean > 0 ? '+' : '') + p.politics.lean.toFixed(0), ''] : null,
  },
  /* --- what living there is actually like. all 2021 Census, all 129/129. --- */
  {
    id: 'growth', label: 'Growing or emptying', col: 'Growth', g: 'Life there',
    hint: 'Population change 2016 to 2021. Some of these towns are shrinking.',
    kind: 'opts', def: 'meh', w: 1,
    opts: [['grow','Somewhere on the way up'],['steady','Steady is fine'],['meh','Not fussed']],
    score: (p, v) => { const x = p.life ? p.life.pop_change : null;
      if (x == null || v === 'meh') return null;
      return v === 'grow' ? clamp((x + 5) / 20, 0, 1) : near(x, 3, 12); },
    show: (p) => p.life && p.life.pop_change != null
      ? [(p.life.pop_change > 0 ? '+' : '') + p.life.pop_change.toFixed(1), '%'] : null,
  },
  {
    id: 'age', label: 'Who lives there', col: 'Age', g: 'Life there',
    hint: 'Median age. Under 40 is a working town, over 55 is a retirement one.',
    kind: 'opts', def: 'meh', w: 1,
    opts: [['young','Younger crowd'],['mixed','A mix'],['older','Older and quieter'],['meh','Not fussed']],
    score: (p, v) => { const x = p.life ? p.life.median_age : null;
      if (x == null || v === 'meh') return null;
      return near(x, { young: 36, mixed: 43, older: 56 }[v], 14); },
    show: (p) => p.life && p.life.median_age != null ? [p.life.median_age.toFixed(0), ''] : null,
  },
  {
    id: 'commute', label: 'The commute', col: 'Short', g: 'Life there',
    hint: 'Share of workers who get there in under 15 minutes.',
    kind: 'opts', def: 'short', w: 1,
    opts: [['short','I want it short'],['meh','Not fussed']],
    score: (p, v) => { const x = p.life ? p.life.commute_short_pct : null;
      if (x == null || v === 'meh') return null; return clamp(x / 80, 0, 1); },
    show: (p) => p.life && p.life.commute_short_pct != null ? [p.life.commute_short_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'car', label: 'Life without a car', col: 'Carfree', g: 'Life there',
    hint: 'Share who get to work by transit, foot or bike.',
    kind: 'opts', def: 'meh', w: 0,
    opts: [['need','I want to manage without one'],['meh','I will drive']],
    score: (p, v) => { const x = p.life ? p.life.carfree_pct : null;
      if (x == null || v === 'meh') return null; return clamp(x / 40, 0, 1); },
    show: (p) => p.life && p.life.carfree_pct != null ? [p.life.carfree_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'jobs', label: 'The job market', col: 'Unemp', g: 'Life there',
    hint: 'Unemployment rate, 2021.',
    kind: 'opts', def: 'meh', w: 0,
    opts: [['need','I need to find work there'],['meh','I bring my own work']],
    score: (p, v) => { const x = p.cost ? p.cost.unemployment : (p.life ? p.life.unemployment : null);
      if (x == null || v === 'meh') return null; return clamp(1 - (x - 4) / 14, 0, 1); },
    show: (p) => { const x = p.life ? p.life.unemployment : null;
      return x == null ? null : [x.toFixed(1), '%']; },
  },
  {
    id: 'mix', label: 'Mix of people', col: 'Diverse', g: 'Life there',
    hint: 'Share of residents who are immigrants.',
    kind: 'opts', def: 'meh', w: 0,
    opts: [['yes','Somewhere mixed'],['meh','Not fussed']],
    score: (p, v) => { const x = p.life ? p.life.immigrants_pct : null;
      if (x == null || v === 'meh') return null; return clamp(x / 35, 0, 1); },
    show: (p) => p.life && p.life.immigrants_pct != null ? [p.life.immigrants_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'french', label: 'French', col: 'French', g: 'Life there',
    hint: 'Share whose first official language is French.',
    kind: 'opts', def: 'meh', w: 0,
    opts: [['yes','I want to live in French'],['some','Some is nice'],['meh','Not fussed']],
    score: (p, v) => { const x = p.life ? p.life.french_pct : null;
      if (x == null || v === 'meh') return null;
      return v === 'yes' ? clamp(x / 70, 0, 1) : near(x, 25, 45); },
    show: (p) => p.life && p.life.french_pct != null ? [p.life.french_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'mood', label: 'What residents say', col: 'Mood', g: 'Life there',
    hint: 'Only 28 of 129 places are researched, so this is off by default.',
    kind: 'opts', def: 'meh', w: 0, opts: [['yes','Count it'],['meh','Ignore it']],
    score: (p, v) => { if (v === 'meh' || !p.lived || !p.lived.sentiment) return null;
      const x = Object.values(p.lived.sentiment).filter((n) => n != null);
      if (!x.length) return null;
      return clamp((x.reduce((a,b)=>a+b,0) / x.length + 2) / 4, 0, 1); },
    show: (p) => { if (!p.lived || !p.lived.sentiment) return null;
      const x = Object.values(p.lived.sentiment).filter((n) => n != null);
      if (!x.length) return null;
      const m = x.reduce((a,b)=>a+b,0) / x.length;
      return [(m > 0 ? '+' : '') + m.toFixed(1), '']; },
  },
];


/* what each column of the plate actually is, in words, on hover and on the
   help strip. an abbreviation nobody can expand is not a label. */
const COLHELP = {
  winter:  ['Average January temperature', '°C', 'Environment Canada normals 1981-2010'],
  summer:  ['Average July temperature', '°C', 'Environment Canada normals 1981-2010'],
  snow:    ['Snow that falls in a year', 'cm', 'Environment Canada normals 1981-2010'],
  sun:     ['Hours of bright sunshine in a year', 'h', 'Environment Canada normals 1981-2010'],
  smoke:   ['Wildfire smoke in the air, 12-year average', 'µg/m³ of fine particulate',
            'ECCC FireWork, the model run with fires minus the run without'],
  size:    ['People who live there', '', '2021 Census'],
  prox:    ['Drive to the nearest city over 300,000', 'minutes', 'Routed on real roads'],
  cost:    ['What an average home is worth', '', '2021 Census, what owners estimated in 2021'],
  politics:['Political lean of the federal riding', '-100 left to +100 right',
            'Elections Canada, 2025 result, vote-weighted'],
  growth:  ['How much the population changed, 2016 to 2021', '%', '2021 Census'],
  age:     ['Median age. Under 40 is a working town, over 55 a retirement one', 'years', '2021 Census'],
  commute: ['Share of workers who get there in under 15 minutes', '%', '2021 Census'],
  car:     ['Share who get to work by transit, foot or bike', '%', '2021 Census'],
  jobs:    ['Unemployment rate', '%', '2021 Census'],
  mix:     ['Share of residents who are immigrants', '%', '2021 Census'],
  french:  ['Share whose first official language is French', '%', '2021 Census'],
  mood:    ['How residents sound about the place, -2 to +2', '', 'Forums, local news and blogs. Only where researched.'],
};

const SHORT = { winter:'the winter', summer:'the summer', snow:'the snow', sun:'the sun',
  smoke:'clean air', size:'the size', prox:'the drive', cost:'the price',
  politics:'the politics', mood:'the mood', growth:'the growth', age:'the crowd',
  commute:'the short commute', car:'getting around without a car', jobs:'the job market',
  mix:'the mix of people', french:'the French' };
const said = (q) => q.kind === 'range' ? q.fmt(state[q.id])
  : (q.opts.find((o) => o[0] === state[q.id]) || ['',''])[1];
const listify = (a) => a.length < 2 ? (a[0]||'') : a.slice(0,-1).join(', ') + ' and ' + a[a.length-1];
function fmtNum(n) {
  if (n == null) return NA;
  if (n >= 1e6) return (n/1e6).toFixed(2) + 'M';
  if (n >= 1e3) return (n/1e3).toFixed(n >= 1e4 ? 0 : 1) + 'k';
  return String(Math.round(n));
}

/* ---------- state, and the shareable link ---------- */
const state = {}, weights = {};
Q.forEach((q) => { state[q.id] = q.def; weights[q.id] = q.w; });
let selected = null;
let showAll = false;
const PLATE_N = 60;   // a plate shows the confusion set, not the whole book

const OPTKEY = '0123456789abcdefghij';
const encodeState = () => Q.map((q) => (q.kind === 'range' ? String(state[q.id])
  : OPTKEY[q.opts.findIndex((o) => o[0] === state[q.id])]) + '.' + weights[q.id]).join('_');
function decodeState(s) {
  const parts = (s || '').split('_');
  if (parts.length !== Q.length) return false;
  try {
    Q.forEach((q, i) => {
      const [val, w] = parts[i].split('.');
      if (q.kind === 'range') { const n = +val; if (!Number.isFinite(n)) throw 0;
        state[q.id] = clamp(n, q.min, q.max); }
      else { const o = q.opts[OPTKEY.indexOf(val)]; if (!o) throw 0; state[q.id] = o[0]; }
      weights[q.id] = clamp(+w || 0, 0, 3);
    });
    return true;
  } catch (e) { return false; }
}
const shared = location.hash.length > 2 && decodeState(location.hash.slice(1));

/* ---------- scoring ---------- */
function scoreAll() {
  const out = DATA.map((p) => {
    let num = 0, den = 0;
    const parts = [];
    let excluded = null;
    const cells = {};
    for (const q of Q) {
      const s = q.score(p, state[q.id]);
      cells[q.id] = s;
      const w = weights[q.id];
      if (!w) continue;
      if (q.hard && q.hard(p, state[q.id])) excluded = q.hardWhy;
      if (s == null) continue;
      num += w * s; den += w;
      parts.push({ id: q.id, s, w, pull: w * (s - 0.5) });
    }
    parts.sort((a, b) => b.pull - a.pull);
    return { p, fit: den ? (num/den)*100 : 0, parts, cells, excluded,
      good: parts.filter((x) => x.s > 0.62).slice(0, 2),
      bad: parts.length ? parts[parts.length-1] : null };
  });
  out.sort((a,b) => (a.excluded?1:0)-(b.excluded?1:0) || b.fit-a.fit);
  return out;
}

/* ---------- the confusion set ----------
   Golden's "similar species" paragraph. Find the places nearest this one on
   overall fit, then name the ONE dimension that actually separates them. That
   dimension gets the arrow. Point at what distinguishes, not at what is good. */
function confusion(r, ranked) {
  const live = ranked.filter((x) => !x.excluded);
  const i = live.indexOf(r);
  if (i < 0) return null;
  const near_ = live.slice(Math.max(0, i-2), i+3).filter((x) => x !== r && Math.abs(x.fit - r.fit) < 6);
  if (near_.length < 1) return null;
  let best = null;
  for (const q of Q) {
    if (!weights[q.id]) continue;
    const mine = r.cells[q.id];
    if (mine == null) continue;
    let spread = 0, n = 0;
    for (const o of near_) { const s = o.cells[q.id]; if (s == null) continue; spread += Math.abs(mine - s); n++; }
    if (!n) continue;
    const avg = spread / n;
    if (!best || avg > best.avg) best = { id: q.id, avg };
  }
  if (!best || best.avg < 0.12) return null;
  return { others: near_.map((x) => x.p.name), splitter: best.id };
}

/* ---------- map ---------- */
const cvs = $('#map'), ctx = cvs.getContext('2d');
let hot = -1, ranked = [], pts = [];
const RAMP = ['--fit-0','--fit-1','--fit-2','--fit-3','--fit-4'];
const rampOf = (f) => css(RAMP[clamp(Math.floor(f/100*RAMP.length), 0, RAMP.length-1)]);

function drawMap() {
  const W = Math.round(cvs.getBoundingClientRect().width) || 800;
  const H = Math.round(W * (MAPGEO.height/1000));
  const dpr = window.devicePixelRatio || 1;
  cvs.width = W*dpr; cvs.height = H*dpr; cvs.style.height = H+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,W,H);
  const k = W/1000;
  ctx.lineJoin = 'round';
  for (const rings of Object.values(MAPGEO.prov)) {
    for (const rg of rings) {
      ctx.beginPath();
      rg.forEach(([x,y],i) => i ? ctx.lineTo(x*k,y*k) : ctx.moveTo(x*k,y*k));
      ctx.closePath();
      ctx.fillStyle = css('--sink'); ctx.fill();
      ctx.strokeStyle = css('--rule-2'); ctx.lineWidth = 0.6; ctx.stroke();
    }
  }
  pts = [];
  for (const r of ranked.slice().reverse()) {
    const x = r.p.x*k, y = r.p.y*k;
    const rad = r.excluded ? 1.5 : 2 + (r.fit/100)**2 * 4;
    ctx.beginPath(); ctx.arc(x,y,rad,0,6.284);
    if (r.excluded) { ctx.fillStyle = css('--rule-2'); ctx.fill(); }
    else { ctx.fillStyle = rampOf(r.fit); ctx.fill();
      ctx.strokeStyle = css('--fit-ink'); ctx.lineWidth = 0.5; ctx.stroke(); }
    pts.push({ x, y, r: Math.max(rad,5), rec: r });
  }
  const top = ranked.filter((r)=>!r.excluded).slice(0,8);
  ctx.font = `600 ${Math.max(9, k*12)}px 'Radio Canada', sans-serif`;
  ctx.textBaseline = 'middle';
  const placed = [];
  const hits = (a) => placed.some((b) => a.x < b.x+b.w && a.x+a.w > b.x && a.y < b.y+b.h && a.y+a.h > b.y);
  for (const r of top) {
    const x = r.p.x*k, y = r.p.y*k, t = r.p.name;
    const w = ctx.measureText(t).width, h = 11;
    let spot = null;
    for (const [tx,ty] of [[x+7,y],[x-7-w,y],[x-w/2,y-h],[x-w/2,y+h]]) {
      if (tx < 2 || tx+w > W-2) continue;
      const box = { x:tx-2, y:ty-h/2-1, w:w+4, h:h+2 };
      if (!hits(box)) { spot = [tx,ty,box]; break; }
    }
    if (!spot) continue;
    placed.push(spot[2]);
    ctx.fillStyle = css('--paper'); ctx.globalAlpha = 0.85;
    ctx.fillRect(spot[2].x, spot[2].y, spot[2].w, spot[2].h); ctx.globalAlpha = 1;
    ctx.fillStyle = css('--ink'); ctx.fillText(t, spot[0], spot[1]);
  }
  if (hot >= 0) {
    const h = pts.find((q) => q.rec === ranked[hot]);
    if (h) { ctx.beginPath(); ctx.arc(h.x,h.y,8,0,6.284);
      ctx.strokeStyle = css('--ink'); ctx.lineWidth = 1.2; ctx.stroke(); }
  }
}

function ribbon(el, p) {
  const w = el.clientWidth || 300, h = 42, dpr = window.devicePixelRatio || 1;
  el.width = w*dpr; el.height = h*dpr;
  const c = el.getContext('2d'); c.setTransform(dpr,0,0,dpr,0,0); c.clearRect(0,0,w,h);
  const t = []; for (let m=1; m<=12; m++) t.push(cv(p,'tmean',String(m)));
  if (t.some((x) => x == null)) return;
  const lo = -30, hi = 26, bw = w/12, zero = h - ((0-lo)/(hi-lo))*h;
  c.strokeStyle = css('--rule-2'); c.lineWidth = 1;
  c.beginPath(); c.moveTo(0,zero); c.lineTo(w,zero); c.stroke();
  t.forEach((v,i) => {
    const y = h - ((v-lo)/(hi-lo))*h;
    c.fillStyle = v < 0 ? css('--cool') : css('--warm');   // opposed states, opposed temperature
    c.fillRect(i*bw+1.5, Math.min(y,zero), bw-3, Math.abs(zero-y));
  });
  c.font = `9px 'Radio Canada', sans-serif`; c.fillStyle = css('--ink-3');
  t.forEach((v,i) => c.fillText(M[i], i*bw+bw/2-3, h-1));
}

/* ---------- render ---------- */
function verdict() {
  const r = ranked.find((x) => !x.excluded);
  const host = $('#verdict');
  if (!r) { host.innerHTML = `<p class="empty">Nothing clears your dealbreakers. Loosen one.</p>`; return; }
  const p = r.p, L = p.lived || {};
  const reasons = r.good.map((g) => SHORT[g.id]);
  const against = r.bad && r.bad.s < 0.45 ? SHORT[r.bad.id] : null;
  const cf = confusion(r, ranked);
  const runners = ranked.filter((x)=>!x.excluded).slice(1,4);
  // a low top score means the answers contradict each other. name the two that fight.
  const live = ranked.filter((x) => !x.excluded).length;
  const cut = ranked.length - live;
  let conflict = null;
  if (r.fit < 62) {
    const worst = r.parts.filter((x) => x.s < 0.4).sort((a,b) => a.s - b.s).slice(0,2);
    const Qof = (id) => Q.find((q) => q.id === id);
    if (worst.length === 2) {
      const a = Qof(worst[0].id), b = Qof(worst[1].id);
      conflict = `Nowhere in Canada is both <b>${said(a).toLowerCase()}</b> (${a.label.toLowerCase()})
        and <b>${said(b).toLowerCase()}</b> (${b.label.toLowerCase()}). ${p.name} is the closest compromise.`;
    } else if (worst.length === 1) {
      const a = Qof(worst[0].id);
      conflict = `Nowhere that fits the rest of your answers is also <b>${said(a).toLowerCase()}</b>
        (${a.label.toLowerCase()}). That is the one giving way.`;
    }
  }
  const cutMsg = cut > ranked.length * 0.5
    ? `Your dealbreakers rule out ${cut} of ${ranked.length} places.` : null;
  host.innerHTML = `
    <p class="v-lead">${shared ? 'They should live in' : 'You should live in'}</p>
    <h2 class="v-name">${p.name}<span class="pv">${p.prov}</span></h2>
    <p class="v-line">${reasons.length ? `It gets you ${listify(reasons)}.` : 'It is the closest thing to what you asked for.'}
      ${against ? `<span class="cut">You give up ${against}.</span>` : ''}</p>
    ${conflict || cutMsg ? `<p class="v-warn">${[cutMsg, conflict].filter(Boolean).join(' ')}
      <b>${Math.round(r.fit)} out of 100</b> is the best fit available, so something has to give.</p>` : ''}
    ${cf ? `<p class="v-catch">Nearly the same on your answers: <b>${cf.others.join(', ')}</b>.
      What separates them is <b>${SHORT[cf.splitter]}</b>.</p>` : ''}
    ${L.honest_downside ? `<p class="v-catch"><b>The catch, from people who live there.</b> ${L.honest_downside}</p>` : ''}
    <div class="v-foot">
      <button class="v-share" id="share">Send this to someone</button>
      <span class="v-next">Then ${runners.map((x)=>x.p.name).join(', ')}</span>
    </div>`;
}

function cellHTML(q, r) {
  const v = q.show(r.p);
  if (!v) return `<span class="cell"><span class="na">${NA}</span></span>`;
  const s = r.cells[q.id];
  const tint = (s != null && weights[q.id]) ? `background:${rampOf(s*100)}` : '';
  return `<span class="cell" style="${tint}"><span class="v">${v[0]}</span><span class="u">${v[1]}</span></span>`;
}

function detailHTML(r) {
  const p = r.p, L = p.lived || {}, st = (p.stations_used||{}).tmean;
  const row = (k,v,u) => `<div class="drow"><span>${k}</span><b>${v}${u?`<span class="u"> ${u}</span>`:''}</b></div>`;
  const s = (el,m) => { const x = cv(p,el,m); return x == null ? NA : Math.round(x); };
  const quotes = (L.quotes||[]).slice(0,2).map((q) =>
    `<p class="quote">“${q.quote}”<cite><a href="${q.source_url}" target="_blank" rel="noopener">${
      new URL(q.source_url).hostname.replace('www.','')}</a></cite></p>`).join('');
  const sent = L.sentiment ? Object.entries(L.sentiment).map(([k,v]) => `<div class="sr">
      <span class="sk">${k}</span><span class="st"><i style="${v<0?`right:50%;width:${Math.abs(v)/2*50}%`
      :`left:50%;width:${v/2*50}%`};background:${v<0?css('--warm'):css('--cool')}"></i></span>
      <span class="sv">${v>0?'+':''}${v.toFixed(1)}</span></div>`).join('') : '';
  return `<div class="dwrap"><div class="dgrid">
    <div>
      <p class="dh">Climate</p>
      <canvas class="ribbon" data-rib></canvas>
      <div class="rib-k"><span>Mean monthly temperature</span><span>${s('tmean','1')}° to ${s('tmean','7')}°</span></div>
      ${row('Snow', s('snow'), 'cm/yr')}
      ${row('Precipitation', s('precip'), 'mm/yr')}
      ${row('Sun', s('sun'), 'h/yr')}
      ${row('Days below -20', s('days_lt_m20'), '')}
      ${row('Wildfire smoke', p.smoke ? p.smoke.mean_ugm3.toFixed(2) : NA, 'µg/m³')}
      <p class="prov-note">${st ? `From <em>${st.name}</em>, ${st.km}km away${
        st.delev != null ? `, ${st.delev}m difference in elevation` : ''}. ${
        st.code === 'COMPUTED' ? st.note + '.' : 'ECCC normals 1981-2010.'}`
        : 'No station close enough. These are blank, not estimated.'}</p>
    </div>
    <div>
      <p class="dh">The place</p>
      ${row('People', fmtNum(p.pop), '')}
      ${row('Home, average value', p.cost && p.cost.home_price ? '$'+fmtNum(p.cost.home_price) : NA, '')}
      ${row('Rent and utilities', p.cost && p.cost.rent_2br ? '$'+Math.round(p.cost.rent_2br) : NA, '/mo')}
      ${row('Median household income', p.cost && p.cost.median_hh_income ? '$'+fmtNum(p.cost.median_hh_income) : NA, '')}
      ${row('Unemployment', p.cost && p.cost.unemployment != null ? p.cost.unemployment : NA, '%')}
      ${row('Nearest city over 300k', p.prox ? p.prox.nearest_big_city : NA,
        p.prox && p.prox.drive_min_to_big_city != null ? `${Math.round(p.prox.drive_min_to_big_city)}min` : '')}
      ${row('Riding', p.politics ? p.politics.riding : NA, '')}
      ${row('Lean', p.politics ? p.politics.lean_label : NA, '')}
      <p class="prov-note">${p.csd ? `Census figures are for <em>${p.csd}</em>.` : ''} 2021 Census.
        Home value is what owners estimated in 2021, not a market price.</p>
    </div>
    <div>
      <p class="dh">What residents say</p>
      ${L.evidence_count ? `
        <div class="sent">${sent}</div>
        ${L.hated && L.hated.length ? `<p class="dh" style="margin-top:.7rem">They complain about</p>
          <ul class="pts">${L.hated.slice(0,2).map((x)=>`<li>${x}</li>`).join('')}</ul>` : ''}
        ${quotes ? `<p class="dh" style="margin-top:.7rem">In their words</p>${quotes}` : ''}
        <p class="prov-note"><em>Researched.</em> ${L.evidence_count} findings from ${L.source_count} pages.</p>`
        : `<p class="prov-note"><em>Not researched.</em> Nobody has read what residents say about
           ${p.name} yet, so this column is empty rather than guessed. 28 of 129 places are done.
           This place is scored on measured data only.</p>`}
    </div>
  </div></div>`;
}

/* The plate is 129 rows by 21 columns, so a full rebuild is ~70ms. That is fine
   for a click and terrible for a slider drag, which fires per pixel. Coalesce to
   one render per frame. */
let pending = false;
function render() {
  if (pending) return;
  // requestAnimationFrame never fires in a hidden tab, so a page opened in a
  // background tab would sit blank until focused. Coalesce only when visible.
  if (document.hidden) { draw(); return; }
  pending = true;
  requestAnimationFrame(() => { pending = false; draw(); });
}
function draw() {
  ranked = scoreAll();
  const live = ranked.filter((r) => !r.excluded);
  const shown = showAll ? ranked.length : Math.min(PLATE_N, ranked.length);
  $('#count').innerHTML = `${live.length} of ${DATA.length} clear your dealbreakers` +
    (ranked.length > PLATE_N ? ` &nbsp;<button class="showall" id="showall">${
      showAll ? 'show the top 60' : `show all ${ranked.length}`}</button>` : '');
  verdict();
  history.replaceState(null, '', '#' + encodeState());

  const cols = Q.filter((q) => q.col);
  $('#thead').innerHTML = `<tr><th></th><th class="l">Place</th><th>Fit</th>
    ${cols.map((q) => { const h = COLHELP[q.id] || [q.label,'',''];
      return `<th${weights[q.id] ? '' : ' style="opacity:.45"'} title="${h[0]}${h[1] ? ' ('+h[1]+')' : ''}. ${h[2]}">${q.col}</th>`; }).join('')}
    <th title="Provenance"></th></tr>`;

  $('#tbody').innerHTML = ranked.slice(0, shown).map((r, i) => {
    const p = r.p, key = p.name + p.prov, cf = !r.excluded ? confusion(r, ranked) : null;
    // width axis carries settlement size: a big city sets wide, a village narrow
    const wd = p.pop ? clamp(75 + (Math.log10(Math.max(p.pop,300)) - 2.5) / 4 * 25, 75, 100) : 88;
    return `<tr class="${r.excluded ? 'cut' : ''}">
      <td class="rank">${r.excluded ? '' : i+1}</td>
      <td class="pname" style="--w:${wd.toFixed(0)}%"><button data-i="${i}">${p.name}<span class="pv">${p.prov}</span></button></td>
      <td class="fit"><span class="b" style="background:${r.excluded ? css('--sink') : rampOf(r.fit)}">${
        r.excluded ? '—' : Math.round(r.fit)}</span></td>
      ${cols.map((q) => `<td class="${cf && cf.splitter === q.id ? 'split' : ''}">${cellHTML(q, r)}</td>`).join('')}
      <td class="prov"><i class="${p.lived ? 'full' : 'none'}" title="${
        p.lived ? 'Residents researched' : 'Not researched'}"></i></td>
    </tr>` + (selected === key ? `<tr class="detail"><td colspan="${cols.length + 4}">${detailHTML(r)}</td></tr>` : '');
  }).join('');

  const rib = $('[data-rib]');
  if (rib) { const r = ranked.find((x) => x.p.name + x.p.prov === selected); if (r) ribbon(rib, r.p); }
  drawMap();
}

/* ---------- survey ---------- */
function buildSurvey() {
  let lastG = null;
  $('#qs').innerHTML = Q.map((q) => {
    const head = q.g !== lastG ? `<p class="qgroup">${q.g}</p>` : '';
    lastG = q.g;
    const body = q.kind === 'range'
      ? `<div class="slider-row"><input type="range" id="r-${q.id}" min="${q.min}" max="${q.max}"
           step="${q.step}" value="${state[q.id]}" aria-label="${q.label}">
           <span class="readout" id="o-${q.id}">${q.fmt(state[q.id])}</span></div>
         <div class="scale-ends"><span>${q.ends[0]}</span><span>${q.ends[1]}</span></div>`
      : `<div class="opts">${q.opts.map(([v,l]) => `<button class="opt" data-q="${q.id}" data-v="${v}"
           aria-pressed="${state[q.id]===v}">${l}</button>`).join('')}</div>`;
    const WL = ['off', 'matters a little', 'matters', 'matters a lot'];
    return head + `<div class="q"><div class="q-top"><p class="q-label">${q.label}</p>
      <div class="weight" role="group" aria-label="How much ${q.label} matters">
        <span class="wlab" id="wl-${q.id}">${WL[weights[q.id]]}</span>
        ${[1,2,3].map((n) => `<button class="tick" data-w="${q.id}" data-n="${n}"
          title="${WL[n]}" aria-label="${q.label}, ${WL[n]}" aria-pressed="${weights[q.id]>=n}"></button>`).join('')}
      </div></div><p class="q-hint">${q.hint}</p>${body}</div>`;
  }).join('');
}
const WLAB = ['off', 'matters a little', 'matters', 'matters a lot'];
function syncTicks() {
  document.querySelectorAll('.tick').forEach((t) =>
    t.setAttribute('aria-pressed', weights[t.dataset.w] >= +t.dataset.n));
  Q.forEach((q) => { const l = $('#wl-' + q.id); if (l) l.textContent = WLAB[weights[q.id]]; });
}

$('#qs').addEventListener('input', (e) => {
  if (e.target.type !== 'range') return;
  const id = e.target.id.slice(2), q = Q.find((x) => x.id === id);
  state[id] = +e.target.value; $('#o-'+id).textContent = q.fmt(+e.target.value);
  render();
});
$('#qs').addEventListener('click', (e) => {
  const o = e.target.closest('.opt'), w = e.target.closest('.tick');
  if (o) {
    state[o.dataset.q] = o.dataset.v;
    o.closest('.opts').querySelectorAll('.opt').forEach((b) => b.setAttribute('aria-pressed', b === o));
    if (!weights[o.dataset.q]) { weights[o.dataset.q] = 1; syncTicks(); }
    render();
  }
  if (w) {
    const id = w.dataset.w, n = +w.dataset.n;
    weights[id] = weights[id] === n ? n-1 : n;
    syncTicks(); render();
  }
});
document.addEventListener('click', (e) => {
  if (!e.target.closest('#showall')) return;
  showAll = !showAll; render();
});
$('#tbody').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-i]'); if (!b) return;
  const r = ranked[+b.dataset.i], key = r.p.name + r.p.prov;
  selected = selected === key ? null : key; render();
});
$('#reset').addEventListener('click', () => {
  Q.forEach((q) => { state[q.id] = q.def; weights[q.id] = q.w; });
  selected = null; history.replaceState(null, '', location.pathname);
  buildSurvey(); render();
});
document.addEventListener('click', async (e) => {
  const b = e.target.closest('#share'); if (!b) return;
  const top = ranked.find((r) => !r.excluded);
  const text = top ? `Apparently I should live in ${top.p.name}, ${top.p.prov}.` : 'Where should I live in Canada?';
  try {
    if (navigator.share) { await navigator.share({ title: 'Where To Live / Canada', text, url: location.href }); return; }
    await navigator.clipboard.writeText(`${text} ${location.href}`);
    b.textContent = 'Copied, with your answers in it';
    setTimeout(() => { b.textContent = 'Send this to someone'; }, 2600);
  } catch (err) { b.textContent = location.href; }
});

const tip = $('#tip');
cvs.addEventListener('mousemove', (e) => {
  const b = cvs.getBoundingClientRect(), mx = e.clientX-b.left, my = e.clientY-b.top;
  let best = null, bd = 1e9;
  for (const q of pts) { const d = Math.hypot(q.x-mx, q.y-my); if (d < q.r+3 && d < bd) { bd = d; best = q; } }
  if (best) {
    const r = best.rec; hot = ranked.indexOf(r);
    tip.innerHTML = `<b>${r.p.name}</b>${r.excluded ? 'ruled out on '+r.excluded
      : 'fit '+Math.round(r.fit)+', rank '+(hot+1)}`;
    tip.style.left = clamp(mx+12, 0, b.width-240)+'px'; tip.style.top = (my+12)+'px';
    tip.classList.add('on'); cvs.style.cursor = 'pointer';
  } else { hot = -1; tip.classList.remove('on'); cvs.style.cursor = 'default'; }
  drawMap();
});
cvs.addEventListener('mouseleave', () => { hot = -1; tip.classList.remove('on'); drawMap(); });
cvs.addEventListener('click', () => {
  if (hot < 0) return;
  const r = ranked[hot], key = r.p.name + r.p.prov;
  selected = selected === key ? null : key; render();
  const el = $(`button[data-i="${ranked.indexOf(r)}"]`);
  if (el) el.scrollIntoView({ block: 'center', behavior: 'smooth' });
});

let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(render, 120); });

if (shared) $('#lede').innerHTML = `Someone sent you their answers, so this is <b>their</b> result.
  Change anything on the left and it becomes yours.`;

buildSurvey();
draw();          // first paint is synchronous: never depend on a frame that may not come
