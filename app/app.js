/* WHERE TO LIVE / CANADA
   DATA and MAPGEO are injected by build_app.py */

const $ = (s, r = document) => r.querySelector(s);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

/* ---------- survey definition ----------
   Each question yields a target + a weight. score(place) -> 0..1 or null
   when the place has no data for it. Null is excluded from the average
   rather than guessed at, and shown as reduced coverage. */

const M = ['J','F','M','A','M','J','J','A','S','O','N','D'];
const cv = (p, el, m = '13') => (p.climate && p.climate[el]) ? p.climate[el][m] : null;

// ideal-point: full marks at the target, decaying over `tol`
const near = (x, target, tol) => x == null ? null : clamp(1 - Math.abs(x - target) / tol, 0, 1);

const Q = [
  {
    id: 'winter', label: 'Winter', hint: 'Average January temperature you want to live in.',
    kind: 'range', min: -26, max: 6, step: 1, def: -5, w: 2,
    fmt: (v) => `${v > 0 ? '+' : ''}${v}°C`,
    ends: ['Deep freeze', 'No real winter'],
    score: (p, v) => near(cv(p, 'tmean', '1'), v, 16),
    val: (p) => cv(p, 'tmean', '1'), unit: '°C',
  },
  {
    id: 'summer', label: 'Summer', hint: 'Average July temperature you want.',
    kind: 'range', min: 12, max: 24, step: 1, def: 20, w: 1,
    fmt: (v) => `${v}°C`,
    ends: ['Cool', 'Hot'],
    score: (p, v) => near(cv(p, 'tmean', '7'), v, 7),
    val: (p) => cv(p, 'tmean', '7'), unit: '°C',
  },
  {
    id: 'snow', label: 'Snow', hint: 'How much shovelling can you live with?',
    kind: 'opts', def: 'some', w: 1,
    opts: [['none', 'As little as possible'], ['some', 'Some is fine'], ['lots', 'Bring it on']],
    score: (p, v) => {
      const s = cv(p, 'snow'); if (s == null) return null;
      if (v === 'none') return clamp(1 - s / 250, 0, 1);
      if (v === 'lots') return clamp(s / 400, 0, 1);
      return clamp(1 - Math.abs(s - 170) / 220, 0, 1);
    },
    val: (p) => cv(p, 'snow'), unit: 'cm/yr',
  },
  {
    id: 'sun', label: 'Sun', hint: 'Hours of bright sunshine per year.',
    kind: 'opts', def: 'yes', w: 1,
    opts: [['yes', 'I need sun'], ['meh', "Doesn't matter"]],
    score: (p, v) => {
      const s = cv(p, 'sun'); if (s == null || v === 'meh') return null;
      return clamp((s - 1500) / (2500 - 1500), 0, 1);
    },
    val: (p) => cv(p, 'sun'), unit: 'h/yr',
  },
  {
    id: 'smoke', label: 'Wildfire smoke', hint: 'Modelled wildfire contribution to fine particulate, 12-year average.',
    kind: 'opts', def: 'less', w: 2,
    opts: [['deal', 'Dealbreaker'], ['less', 'Prefer less'], ['meh', "Doesn't matter"]],
    score: (p, v) => {
      const s = p.smoke ? p.smoke.mean_ugm3 : null;
      if (s == null || v === 'meh') return null;
      return clamp(1 - s / 2.6, 0, 1);
    },
    hard: (p, v) => v === 'deal' && p.smoke && p.smoke.mean_ugm3 > 1.5,
    hardWhy: 'heavy wildfire smoke',
    val: (p) => p.smoke ? p.smoke.mean_ugm3 : null, unit: 'µg/m³',
  },
  {
    id: 'size', label: 'Size', hint: 'How big a place do you want?',
    kind: 'opts', def: 'small', w: 2,
    opts: [['village', 'Village'], ['town', 'Town'], ['small', 'Small city'], ['mid', 'Mid city'], ['big', 'Big city']],
    score: (p, v) => {
      if (p.pop == null) return null;
      const target = { village: 3.4, town: 4.1, small: 4.8, mid: 5.4, big: 6.2 }[v];
      return near(Math.log10(Math.max(p.pop, 300)), target, 1.5);
    },
    val: (p) => p.pop, unit: 'people',
  },
  {
    id: 'prox', label: 'Near a big city', hint: 'Drive to the nearest metro over half a million.',
    kind: 'opts', def: 'hour', w: 2,
    opts: [['in', 'In one'], ['hour', 'Within an hour'], ['half', 'Half a day is fine'], ['far', 'As far as possible']],
    score: (p, v) => {
      const d = p.prox ? p.prox.drive_min_to_big_city : null;
      if (d == null) return null;
      if (v === 'in') return near(d, 0, 70);
      if (v === 'hour') return near(d, 45, 110);
      if (v === 'half') return near(d, 180, 260);
      return clamp(d / 420, 0, 1);
    },
    val: (p) => p.prox ? p.prox.drive_min_to_big_city : null, unit: 'min',
  },
  {
    id: 'cost', label: 'Housing budget', hint: 'What you can pay for a home.',
    kind: 'range', min: 200, max: 1400, step: 25, def: 600, w: 2,
    fmt: (v) => `$${v}k`,
    ends: ['$200k', '$1.4M'],
    score: (p, v) => {
      const h = p.cost ? p.cost.home_price : null;
      if (h == null) return null;
      const b = v * 1000;
      if (h <= b) return clamp(0.6 + 0.4 * (1 - h / b), 0, 1); // under budget, cheaper is better
      return clamp(0.6 * (1 - (h - b) / b), 0, 0.6);           // over budget, falls away
    },
    hard: (p, v) => p.cost && p.cost.home_price != null && p.cost.home_price > v * 1000 * 1.6,
    hardWhy: 'far over budget',
    val: (p) => p.cost ? p.cost.home_price : null, unit: '$',
  },
  {
    id: 'politics', label: 'Politics', hint: 'Vote-weighted lean of the federal riding.',
    kind: 'opts', def: 'meh', w: 1,
    opts: [['left', 'Left'], ['centre', 'Centre'], ['right', 'Right'], ['meh', "Doesn't matter"]],
    score: (p, v) => {
      const l = p.politics ? p.politics.lean : null;
      if (l == null || v === 'meh') return null;
      const t = { left: -55, centre: 0, right: 55 }[v];
      return near(l, t, 95);
    },
    val: (p) => p.politics ? p.politics.lean : null, unit: 'lean',
  },
  {
    id: 'mood', label: 'What residents say', hint: 'Weight the places where people actually sound happy. Only covers the 28 places researched so far.',
    kind: 'opts', def: 'meh', w: 0,
    opts: [['yes', 'Count it'], ['meh', 'Ignore it']],
    score: (p, v) => {
      if (v === 'meh' || !p.lived || !p.lived.sentiment) return null;
      const vals = Object.values(p.lived.sentiment).filter((x) => x != null);
      if (!vals.length) return null;
      return clamp((vals.reduce((a, b) => a + b, 0) / vals.length + 2) / 4, 0, 1);
    },
  },
];

/* how each dimension reads in the one-line verdict under a place name */
const SHORT = {
  winter: 'the winter', summer: 'the summer', snow: 'the snow', sun: 'the sunshine',
  smoke: 'clean air', size: 'the size', prox: 'the drive', cost: 'the price',
  politics: 'the politics', outdoors: 'the outdoors',
};
const listify = (a) => a.length < 2 ? (a[0] || '') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];

/* ---------- state ---------- */
const state = {};
const weights = {};
Q.forEach((q) => { state[q.id] = q.multi ? [q.def] : q.def; weights[q.id] = q.w; });
let selected = null;

/* ---------- scoring ---------- */
function scoreAll() {
  const out = DATA.map((p) => {
    let num = 0, den = 0, have = 0, want = 0;
    const parts = [];
    let excluded = null;
    for (const q of Q) {
      const w = weights[q.id];
      if (!w) continue;
      want++;
      if (q.hard && q.hard(p, state[q.id])) excluded = q.hardWhy;
      const s = q.score(p, state[q.id]);
      if (s == null) continue;
      have++;
      num += w * s; den += w;
      parts.push({ id: q.id, label: q.label, s, w, pull: w * (s - 0.5) });
    }
    const fit = den ? (num / den) * 100 : 0;
    parts.sort((a, b) => b.pull - a.pull);
    return {
      p, fit, parts, excluded,
      coverage: want ? have / want : 0,
      good: parts.filter((x) => x.s > 0.62).slice(0, 2),
      bad: parts.length ? parts[parts.length - 1] : null,
    };
  });
  out.sort((a, b) => (a.excluded ? 1 : 0) - (b.excluded ? 1 : 0) || b.fit - a.fit);
  return out;
}

/* ---------- map ---------- */
const cvs = $('#map'), ctx = cvs.getContext('2d');
let hot = -1, ranked = [], pts = [];

function drawMap() {
  // measure the canvas itself, not the padded parent, or the projection squashes
  const W = Math.round(cvs.getBoundingClientRect().width) || 800;
  const H = Math.round(W * (MAPGEO.height / 1000));
  const dpr = window.devicePixelRatio || 1;
  cvs.width = W * dpr; cvs.height = H * dpr;
  cvs.style.height = H + 'px';
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, W, H);
  const k = W / 1000;

  // landmass
  ctx.lineJoin = 'round';
  for (const rings of Object.values(MAPGEO.prov)) {
    for (const r of rings) {
      ctx.beginPath();
      r.forEach(([x, y], i) => i ? ctx.lineTo(x * k, y * k) : ctx.moveTo(x * k, y * k));
      ctx.closePath();
      ctx.fillStyle = css('--land'); ctx.fill();
      ctx.strokeStyle = css('--land-edge'); ctx.lineWidth = 0.6; ctx.stroke();
    }
  }

  // places, worst first so the best sit on top
  const order = ranked.slice().reverse();
  const top = new Set(ranked.filter((r) => !r.excluded).slice(0, 10).map((r) => r.p.name + r.p.prov));
  pts = [];
  for (const r of order) {
    const x = r.p.x * k, y = r.p.y * k;
    const isTop = top.has(r.p.name + r.p.prov);
    const f = r.excluded ? 0 : r.fit / 100;
    const rad = r.excluded ? 1.6 : 1.8 + f * f * 4.4;
    ctx.beginPath(); ctx.arc(x, y, rad, 0, 6.284);
    if (isTop) { ctx.fillStyle = css('--survey'); ctx.fill(); }
    else {
      ctx.fillStyle = css('--sheet'); ctx.fill();
      ctx.strokeStyle = r.excluded ? css('--rule') : css('--contour');
      ctx.lineWidth = 0.9; ctx.stroke();
    }
    pts.push({ x, y, r: Math.max(rad, 5), rec: r });
  }

  // label the top ten, map-label style, skipping any that would collide
  const fs = Math.max(10, k * 15);
  ctx.font = `${fs}px ${css('--f-display')}`;
  ctx.textBaseline = 'middle';
  const placed = [];
  const hits = (a) => placed.some((b) =>
    a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y);
  ranked.filter((r) => !r.excluded).slice(0, 10).forEach((r) => {
    const x = r.p.x * k, y = r.p.y * k;
    const t = r.p.name.toUpperCase();
    const wpx = ctx.measureText(t).width, hpx = fs * 0.92;
    // try right, left, above, below until one lands clear
    const tries = [
      [x + 8, y], [x - 8 - wpx, y],
      [x - wpx / 2, y - hpx - 4], [x - wpx / 2, y + hpx + 4],
    ];
    let spot = null;
    for (const [tx, ty] of tries) {
      if (tx < 2 || tx + wpx > W - 2) continue;
      const box = { x: tx - 2, y: ty - hpx / 2 - 1, w: wpx + 4, h: hpx + 2 };
      if (!hits(box)) { spot = [tx, ty, box]; break; }
    }
    if (!spot) return;                      // crowded corner: leave it to the index
    placed.push(spot[2]);
    ctx.fillStyle = css('--sheet');
    ctx.globalAlpha = 0.85;
    ctx.fillRect(spot[2].x, spot[2].y, spot[2].w, spot[2].h);
    ctx.globalAlpha = 1;
    // leader line when the label had to move off the dot
    if (spot[1] !== y) {
      ctx.strokeStyle = css('--contour'); ctx.lineWidth = 0.5;
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, spot[1] + (spot[1] < y ? hpx / 2 : -hpx / 2)); ctx.stroke();
    }
    ctx.fillStyle = css('--ink');
    ctx.fillText(t, spot[0], spot[1]);
  });

  if (hot >= 0) {
    const h = pts.find((q) => q.rec === ranked[hot]);
    if (h) {
      ctx.beginPath(); ctx.arc(h.x, h.y, 9, 0, 6.284);
      ctx.strokeStyle = css('--survey'); ctx.lineWidth = 1.4; ctx.stroke();
    }
  }
}

/* ---------- climate ribbon ---------- */
function ribbon(el, p) {
  const w = el.clientWidth || 300, h = 46, dpr = window.devicePixelRatio || 1;
  el.width = w * dpr; el.height = h * dpr;
  const c = el.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0);
  c.clearRect(0, 0, w, h);
  const t = [], lo = -30, hi = 26;
  for (let m = 1; m <= 12; m++) t.push(cv(p, 'tmean', String(m)));
  if (t.some((x) => x == null)) return;
  const bw = w / 12;
  const zero = h - ((0 - lo) / (hi - lo)) * h;
  c.strokeStyle = css('--rule'); c.lineWidth = 1;
  c.beginPath(); c.moveTo(0, zero); c.lineTo(w, zero); c.stroke();
  t.forEach((v, i) => {
    const y = h - ((v - lo) / (hi - lo)) * h;
    c.fillStyle = v < 0 ? css('--water') : css('--contour');
    c.fillRect(i * bw + 1.5, Math.min(y, zero), bw - 3, Math.abs(zero - y));
  });
  c.font = `9px ${css('--f-mono')}`; c.fillStyle = css('--ink-3');
  t.forEach((v, i) => c.fillText(M[i], i * bw + bw / 2 - 3, h - 1));
}

/* ---------- render ---------- */
function fmtNum(n) {
  if (n == null) return '—';
  if (n >= 1e6) return (n / 1e6).toFixed(2) + 'M';
  if (n >= 1e3) return (n / 1e3).toFixed(n >= 1e4 ? 0 : 1) + 'k';
  return String(Math.round(n));
}

/* resident sentiment: diverging from a centre line, because the sign is the point */
function sentBar(L) {
  if (!L || !L.sentiment) return '';
  const keys = Object.keys(L.sentiment);
  if (!keys.length) return '';
  const rows = keys.map((k) => {
    const v = L.sentiment[k];                      // -2..+2
    const w = Math.abs(v) / 2 * 50;                // half-width percent
    const neg = v < 0;
    return `<div class="sr">
      <span class="sk">${k}</span>
      <span class="st">
        <i style="${neg ? `right:50%;width:${w}%` : `left:50%;width:${w}%`};background:${
          neg ? 'var(--survey)' : 'var(--relief)'}"></i>
      </span>
      <span class="sv">${v > 0 ? '+' : ''}${v.toFixed(1)}</span>
    </div>`;
  }).join('');
  return `<p class="dh" style="margin-top:.8rem">How residents feel, by topic</p>
    <div class="sent">${rows}</div>
    <div class="ribbon-key"><span>complain</span><span>praise</span></div>`;
}

function detailHTML(r) {
  const p = r.p, L = p.lived || {}, st = p.stations_used || {};
  const s = (el, m) => cv(p, el, m);
  const row = (k, v, u) => `<div class="stat"><span>${k}</span><b>${v}${u ? `<span class="u"> ${u}</span>` : ''}</b></div>`;
  const na = '—';
  const tstn = st.tmean;
  const prov = tstn
    ? `Climate from <span class="wname">${tstn.name}</span>, ${tstn.km}km away${tstn.delev != null ? `, ${tstn.delev}m elevation difference` : ''}. ${tstn.code === 'COMPUTED' ? tstn.note + '.' : 'Environment Canada normals 1981-2010.'}`
    : 'No climate station close enough to this place.';

  const quotes = (L.quotes || []).slice(0, 2).map((q) =>
    `<blockquote class="quote">“${q.quote}”<cite><a href="${q.source_url}" target="_blank" rel="noopener">${new URL(q.source_url).hostname.replace('www.', '')}</a></cite></blockquote>`).join('');

  return `<div class="detail-grid">
    <div>
      <p class="dh">Climate</p>
      <canvas class="ribbon" data-rib></canvas>
      <div class="ribbon-key"><span>Mean monthly temperature</span><span>${s('tmean','1') ?? na}° to ${s('tmean','7') ?? na}°</span></div>
      ${row('Snow', s('snow') != null ? Math.round(s('snow')) : na, 'cm/yr')}
      ${row('Rain and melt', s('precip') != null ? Math.round(s('precip')) : na, 'mm/yr')}
      ${row('Sun', s('sun') != null ? Math.round(s('sun')) : na, 'h/yr')}
      ${row('Days below -20', s('days_lt_m20') != null ? Math.round(s('days_lt_m20')) : na, '')}
      ${row('Days above 30', s('days_gt30') != null ? Math.round(s('days_gt30')) : na, '')}
      ${row('Wildfire smoke', p.smoke ? p.smoke.mean_ugm3.toFixed(2) : na, 'µg/m³')}
      <p class="prov-note">${prov}</p>
    </div>
    <div>
      <p class="dh">The place</p>
      ${row('People', fmtNum(p.pop), '')}
      ${row('Home price', p.cost && p.cost.home_price ? '$' + fmtNum(p.cost.home_price) : na, '')}
      ${row('Rent, 2 bed', p.cost && p.cost.rent_2br ? '$' + Math.round(p.cost.rent_2br) : na, '/mo')}
      ${row('Median income', p.cost && p.cost.median_hh_income ? '$' + fmtNum(p.cost.median_hh_income) : na, '')}
      ${row('Nearest big city', p.prox && p.prox.nearest_big_city ? p.prox.nearest_big_city : na,
            p.prox && p.prox.drive_min_to_big_city != null ? `${Math.round(p.prox.drive_min_to_big_city)}min` : '')}
      ${row('Politics', p.politics && p.politics.lean_label ? p.politics.lean_label : na, '')}
      ${sentBar(L)}
      ${L.honest_downside ? `<p class="dh" style="margin-top:.8rem">The catch</p><p style="font-size:.82rem;margin:.2rem 0 .5rem">${L.honest_downside}</p>` : ''}
      ${L.loved && L.loved.length ? `<p class="dh" style="margin-top:.7rem">Residents like</p><ul class="pts">${L.loved.slice(0,3).map((x)=>`<li>${x}</li>`).join('')}</ul>` : ''}
      ${L.hated && L.hated.length ? `<p class="dh" style="margin-top:.6rem">Residents complain about</p><ul class="pts neg">${L.hated.slice(0,3).map((x)=>`<li>${x}</li>`).join('')}</ul>` : ''}
      ${quotes ? `<p class="dh" style="margin-top:.7rem">In their words</p>${quotes}` : ''}
      ${L.evidence_count ? `<p class="prov-note">${L.evidence_count} sourced findings from ${L.source_count} pages residents wrote or local outlets published. Confidence ${L.confidence}.</p>`
        : `<p class="prov-note">No resident research for this place yet. The survey scores it on measured data only.</p>`}
    </div>
  </div>`;
}

function render() {
  ranked = scoreAll();
  const live = ranked.filter((r) => !r.excluded);
  const cut = ranked.filter((r) => r.excluded);
  $('#count').textContent = `${live.length} of ${DATA.length} places`;

  const list = $('#index');
  list.innerHTML = ranked.map((r, i) => {
    const p = r.p;
    const why = r.excluded
      ? `<span class="against">Ruled out on ${r.excluded}</span>`
      : [
          r.good.length ? `Gets you ${listify(r.good.map((g) => SHORT[g.id] || g.label.toLowerCase()))}` : '',
          r.bad && r.bad.s < 0.4 ? `<span class="against">but not ${SHORT[r.bad.id] || r.bad.label.toLowerCase()}</span>` : '',
        ].filter(Boolean).join('<span class="sep">·</span>');
    const key = p.name + p.prov;
    return `<li><button class="row ${selected === key ? 'lit' : ''}" data-i="${i}">
      <span class="rank">${r.excluded ? '—' : i + 1}</span>
      <span>
        <span class="rname">${p.name}<span class="pv">${p.prov}</span></span>
        <span class="rwhy">${why || 'no strong signal either way'}</span>
      </span>
      <span class="fit"><span class="fitnum">${r.excluded ? '—' : Math.round(r.fit)}</span>
        <span class="fitbar"><i style="width:${r.excluded ? 0 : Math.round(r.fit)}%"></i></span></span>
    </button>${selected === key ? `<div class="detail">${detailHTML(r)}</div>` : ''}</li>`;
  }).join('');

  list.querySelectorAll('[data-rib]').forEach((el) => {
    const r = ranked.find((x) => x.p.name + x.p.prov === selected);
    if (r) ribbon(el, r.p);
  });
  drawMap();
}

/* ---------- survey UI ---------- */
function buildSurvey() {
  const host = $('#qs');
  host.innerHTML = Q.map((q) => {
    let body;
    if (q.kind === 'range') {
      body = `<div class="slider-row">
          <input type="range" id="r-${q.id}" min="${q.min}" max="${q.max}" step="${q.step}" value="${q.def}"
                 aria-label="${q.label}">
          <span class="readout" id="o-${q.id}">${q.fmt(q.def)}</span>
        </div>
        <div class="scale-ends"><span>${q.ends[0]}</span><span>${q.ends[1]}</span></div>`;
    } else {
      body = `<div class="opts">${q.opts.map(([v, l]) =>
        `<button class="opt" data-q="${q.id}" data-v="${v}" aria-pressed="${
          q.multi ? state[q.id].includes(v) : state[q.id] === v}">${l}</button>`).join('')}</div>`;
    }
    return `<div class="q">
      <div class="q-top">
        <p class="q-label">${q.label}</p>
        <div class="weight" role="group" aria-label="${q.label} importance">
          <span class="weight-lab">matters</span>
          ${[1, 2, 3].map((n) => `<button class="tick" data-w="${q.id}" data-n="${n}"
              aria-label="${q.label} importance ${n} of 3" aria-pressed="${weights[q.id] >= n}"></button>`).join('')}
        </div>
      </div>
      <p class="q-hint">${q.hint}</p>
      ${body}
    </div>`;
  }).join('');

  host.addEventListener('input', (e) => {
    const t = e.target;
    if (t.type === 'range') {
      const id = t.id.slice(2), q = Q.find((x) => x.id === id);
      state[id] = +t.value;
      $('#o-' + id).textContent = q.fmt(+t.value);
      render();
    }
  });
  host.addEventListener('click', (e) => {
    const o = e.target.closest('.opt'), w = e.target.closest('.tick');
    if (o) {
      const q = Q.find((x) => x.id === o.dataset.q);
      if (q.multi) {
        let cur = state[q.id].filter((v) => v !== 'any');
        const v = o.dataset.v;
        if (v === 'any') cur = ['any'];
        else cur = cur.includes(v) ? cur.filter((x) => x !== v) : [...cur, v];
        state[q.id] = cur.length ? cur : ['any'];
        o.closest('.opts').querySelectorAll('.opt').forEach((b) =>
          b.setAttribute('aria-pressed', state[q.id].includes(b.dataset.v)));
      } else {
        state[q.id] = o.dataset.v;
        o.closest('.opts').querySelectorAll('.opt').forEach((b) =>
          b.setAttribute('aria-pressed', b === o));
      }
      if (!weights[q.id]) { weights[q.id] = 1; syncTicks(); }
      render();
    }
    if (w) {
      const id = w.dataset.w, n = +w.dataset.n;
      weights[id] = weights[id] === n ? n - 1 : n;
      syncTicks(); render();
    }
  });
}
function syncTicks() {
  document.querySelectorAll('.tick').forEach((t) =>
    t.setAttribute('aria-pressed', weights[t.dataset.w] >= +t.dataset.n));
}

/* ---------- events ---------- */
$('#index').addEventListener('click', (e) => {
  const b = e.target.closest('.row'); if (!b) return;
  const r = ranked[+b.dataset.i], key = r.p.name + r.p.prov;
  selected = selected === key ? null : key;
  render();
});

const tip = $('#tip');
cvs.addEventListener('mousemove', (e) => {
  const b = cvs.getBoundingClientRect();
  const mx = e.clientX - b.left, my = e.clientY - b.top;
  let best = null, bd = 1e9;
  for (const q of pts) {
    const d = Math.hypot(q.x - mx, q.y - my);
    if (d < q.r + 3 && d < bd) { bd = d; best = q; }
  }
  if (best) {
    const r = best.rec;
    hot = ranked.indexOf(r);
    tip.innerHTML = `<b>${r.p.name}</b><span class="m">${r.p.prov} · ${
      r.excluded ? 'ruled out: ' + r.excluded : 'fit ' + Math.round(r.fit) + ' · rank ' + (ranked.indexOf(r) + 1)}</span>`;
    tip.style.left = clamp(mx + 12, 0, b.width - 240) + 'px';
    tip.style.top = (my + 12) + 'px';
    tip.classList.add('on');
    cvs.style.cursor = 'pointer';
  } else { hot = -1; tip.classList.remove('on'); cvs.style.cursor = 'crosshair'; }
  drawMap();
});
cvs.addEventListener('mouseleave', () => { hot = -1; tip.classList.remove('on'); drawMap(); });
cvs.addEventListener('click', () => {
  if (hot < 0) return;
  const r = ranked[hot], key = r.p.name + r.p.prov;
  selected = selected === key ? null : key;
  render();
  const el = $(`.row[data-i="${ranked.indexOf(r)}"]`);
  if (el) el.scrollIntoView({ block: 'center', behavior: 'smooth' });
});

$('#reset').addEventListener('click', () => {
  Q.forEach((q) => { state[q.id] = q.multi ? [q.def] : q.def; weights[q.id] = q.w; });
  selected = null;
  buildSurvey(); render();
});

const root = document.documentElement;
$('#theme').addEventListener('click', () => {
  const cur = root.dataset.theme ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  root.dataset.theme = cur === 'dark' ? 'light' : 'dark';
  render();
});

let rt;
addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(render, 120); });

buildSurvey();
render();
