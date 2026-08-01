/* WHERE TO LIVE / CANADA. DATA and MAPGEO injected by src/build_app.py */

const $ = (s, r = document) => r.querySelector(s);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const M = ['J','F','M','A','M','J','J','A','S','O','N','D'];
const cv = (p, el, m = '13') => (p.climate && p.climate[el]) ? p.climate[el][m] : null;
const NA = '..';   // StatCan's published symbol for "not available", not an invented dash
const near = (x, t, tol) => x == null ? null : clamp(1 - Math.abs(x - t) / tol, 0, 1);
/* how far the year swings, July mean minus January mean. Doug's "seasonality
   1-5": Ottawa lands at 31 degrees of swing, Victoria at 10. */
const swingOf = (p) => { const a = cv(p, 'tmean', '7'), b = cv(p, 'tmean', '1');
  return (a == null || b == null) ? null : a - b; };
const LIVED_N = DATA.filter((p) => p.lived).length;   // researched places, live count

/* ---------- the dimensions ----------
   Each is one column of the plate, in a fixed order that never changes.
   `show` renders the value; a place with no data still gets its cell. */
const Q_ALL = [
  {
    id: 'winter', g: 'Climate', label: 'Winter', col: 'Jan', hint: 'The January you want to wake up in.',
    kind: 'range', min: -26, max: 6, step: 1, nudge: 2, def: -5, w: 2,
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
    id: 'swing', g: 'Climate', label: 'Seasons', col: 'Swing',
    hint: 'The gap between January and July. Ottawa swings 31°, Victoria 10°.',
    kind: 'opts', def: 'big', w: 1,
    opts: [['big','Four real seasons'],['mid','Some change'],['mild','Much the same all year']],
    score: (p, v) => { const s = swingOf(p); if (s == null) return null;
      return near(s, { big: 34, mid: 24, mild: 11 }[v], 15); },
    show: (p) => { const s = swingOf(p); return s == null ? null : [s.toFixed(0), '°']; },
  },
  {
    id: 'rain', g: 'Climate', label: 'Rain', col: 'Rain', hint: 'Total precipitation in a year.',
    kind: 'opts', def: 'dry', w: 0,
    opts: [['dry','Keep it dry'],['mid','In between'],['wet','I like the rain']],
    score: (p, v) => { const r = cv(p, 'precip'); if (r == null) return null;
      if (v === 'dry') return clamp(1 - (r - 300) / 900, 0, 1);
      if (v === 'wet') return clamp((r - 400) / 900, 0, 1);
      return near(r, 800, 500); },
    show: (p) => { const r = cv(p, 'precip'); return r == null ? null : [Math.round(r), 'mm']; },
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
    kind: 'opts', def: 'yes', w: 1,
    opts: [['yes','I need sun'],['grey','Grey suits me fine']],
    score: (p, v) => { const s = cv(p, 'sun'); if (s == null) return null;
      return v === 'grey' ? clamp(1 - (s - 1500) / 1000, 0, 1) : clamp((s - 1500) / 1000, 0, 1); },
    show: (p) => { const x = cv(p, 'sun'); return x == null ? null : [Math.round(x), 'h']; },
  },
  {
    id: 'smoke', g: 'Climate', label: 'Wildfire smoke', col: 'Smoke',
    hint: 'Modelled smoke from fire only, 12-year average.',
    kind: 'opts', def: 'less', w: 2,
    opts: [['deal','Dealbreaker'],['less','Prefer less']],
    score: (p, v) => { const s = p.smoke ? p.smoke.mean_ugm3 : null;
      if (s == null) return null; return clamp(1 - s / 2.6, 0, 1); },
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
      if (d == null) return null;
      if (d === 0) return ['here', ''];
      if (d < 150) return [Math.round(d), 'm'];       // minutes, while that still reads
      return [(d / 60).toFixed(d < 600 ? 1 : 0), 'h'];
    },
  },
  {
    id: 'water', g: 'The place', label: 'Near water', col: 'Water',
    hint: 'Distance to the ocean or a big lake, measured to the shoreline.',
    kind: 'opts', def: 'any', w: 0,
    opts: [['ocean','On the ocean'],['lake','On a lake'],['any','Either will do']],
    score: (p, v) => { const W = p.water; if (!W) return null;
      const km = v === 'ocean' ? W.km_to_ocean : v === 'lake' ? W.km_to_lake : W.km_to_water;
      if (km == null) return null;
      return clamp(1 - km / 25, 0, 1); },   // on the shore is 1, a 25km drive is 0
    show: (p) => { const W = p.water; if (!W || W.km_to_water == null) return null;
      return [W.km_to_water < 1 ? '0' : Math.round(W.km_to_water), 'km']; },
  },
  {
    id: 'pitches', g: 'The place', label: 'Soccer pitches', col: 'Pitch',
    hint: 'Pitches within a 15km drive, counted off OpenStreetMap.',
    kind: 'flag', def: 1, w: 0, want: 'Somewhere I can actually get a game',
    score: (p) => { const n = p.osm ? p.osm.soccer_pitches : null;
      if (n == null) return null;
      return clamp(Math.sqrt(n / 50), 0, 1); },   // 50 within a drive is plenty
    show: (p) => p.osm && p.osm.soccer_pitches != null ? [p.osm.soccer_pitches, ''] : null,
  },
  {
    id: 'sports', g: 'The place', label: 'Pro sports', col: 'Pro',
    hint: 'A top-tier team that actually plays there. NHL, CFL, MLS, MLB, NBA, WNBA, PWHL, CPL.',
    kind: 'flag', def: 1, w: 0, want: 'A pro team to go and watch',
    // absence is verified, not missing, so it scores zero rather than dropping out
    score: (p) => { const c = p.civic;
      if (!c || !c.has_pro_team) return 0;
      return clamp(0.6 + (c.pro_league_count || 1) / 8 * 0.4, 0, 1); },
    show: (p) => (p.civic && p.civic.pro_league_count)
      ? [p.civic.pro_league_count, ''] : ['0', ''],
  },
  {
    id: 'transit', g: 'The place', label: 'Rapid transit', col: 'Rail',
    hint: 'A subway, light rail or commuter train serving the place.',
    kind: 'flag', def: 1, w: 0, want: 'Rail I can actually use',
    score: (p) => { const c = p.civic;
      if (!c || !c.rapid_transit) return 0;
      return { subway: 1, 'light rail': 0.9, 'commuter rail': 0.5 }[c.transit_type] || 0.5; },
    show: (p) => { const c = p.civic;
      if (!c || !c.rapid_transit) return ['no', ''];
      return [{ subway: 'metro', 'light rail': 'LRT', 'commuter rail': 'GO' }[c.transit_type] || 'yes', '']; },
  },
  {
    id: 'cost', g: 'The place', label: 'Housing budget', col: 'Home', hint: 'What you can pay.',
    kind: 'range', min: 200, max: 1400, step: 25, nudge: 100, def: 600, w: 2,
    fmt: (v) => `$${v}k`, ends: ['$200k', '$1.4M'],
    score: (p, v) => { const h = p.cost ? p.cost.home_price : null; if (h == null) return null;
      const b = v * 1000;
      return h <= b ? clamp(0.6 + 0.4 * (1 - h / b), 0, 1) : clamp(0.6 * (1 - (h - b) / b), 0, 0.6); },
    hard: (p, v) => p.cost && p.cost.home_price != null && p.cost.home_price > v * 1000 * 1.6,
    hardWhy: 'the price',
    show: (p) => (p.cost && p.cost.home_price) ? [fmtNum(p.cost.home_price), ''] : null,
  },
  {
    id: 'politics', g: 'The place', label: 'Politics', col: 'Lean', hint: `Vote-weighted lean of the ${CFG.sources.politics_unit}, ${CFG.vote_year}.`,
    kind: 'opts', def: 'centre', w: 0,
    opts: [['left','Left'],['centre','Centre'],['right','Right']],
    score: (p, v) => { const l = p.politics ? p.politics.lean : null;
      if (l == null) return null;
      const P = CFG.politics;                  // calibrated per country at build time
      // Left and Right are one-sided: overshooting the target is not a miss.
      // Symmetric targets scored Washington DC at zero on "Left" for being the
      // most left-leaning place in the country, which is plainly the wrong answer.
      if (v === 'left')  return l <= P.left  ? 1 : clamp(1 - (l - P.left) / P.tol, 0, 1);
      if (v === 'right') return l >= P.right ? 1 : clamp(1 - (P.right - l) / P.tol, 0, 1);
      return near(l, P.centre, P.tol); },
    show: (p) => p.politics && p.politics.lean != null
      ? [(p.politics.lean > 0 ? '+' : '') + p.politics.lean.toFixed(0), ''] : null,
  },
  /* --- what living there is actually like. all 2021 Census, all 129/129. --- */
  {
    id: 'growth', label: 'Growing or emptying', col: 'Growth', g: 'Life there',
    hint: 'Population change 2016 to 2021. Some of these towns are shrinking.',
    kind: 'opts', def: 'grow', w: 0,
    opts: [['grow','On the way up'],['steady','Steady suits me']],
    score: (p, v) => { const x = p.life ? p.life.pop_change : null;
      if (x == null) return null;
      const G = CFG.growth;
      return v === 'grow' ? clamp((x + G.offset) / G.span, 0, 1) : near(x, G.steady, G.tol); },
    show: (p) => p.life && p.life.pop_change != null
      ? [(p.life.pop_change > 0 ? '+' : '') + p.life.pop_change.toFixed(1), '%'] : null,
  },
  {
    id: 'age', label: 'Who lives there', col: 'Age', g: 'Life there',
    hint: 'Median age. Under 40 is a working town, over 55 is a retirement one.',
    kind: 'opts', def: 'mixed', w: 0,
    opts: [['young','Younger crowd'],['mixed','A mix'],['older','Older and quieter']],
    score: (p, v) => { const x = p.life ? p.life.median_age : null;
      if (x == null) return null;
      return near(x, { young: 36, mixed: 43, older: 56 }[v], 14); },
    show: (p) => p.life && p.life.median_age != null ? [p.life.median_age.toFixed(0), ''] : null,
  },
  {
    id: 'commute', label: 'The commute', col: 'Short', g: 'Life there',
    hint: 'Share of workers who get there in under 15 minutes.',
    kind: 'flag', def: 1, w: 0, want: 'A short commute',
    score: (p) => { const x = p.life ? p.life.commute_short_pct : null;
      if (x == null) return null; return clamp(x / 80, 0, 1); },
    show: (p) => p.life && p.life.commute_short_pct != null ? [p.life.commute_short_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'car', label: 'Life without a car', col: 'Carfree', g: 'Life there',
    hint: 'Share who get to work by transit, foot or bike.',
    kind: 'flag', def: 1, w: 0, want: 'To manage without a car',
    score: (p) => { const x = p.life ? p.life.carfree_pct : null;
      if (x == null) return null; return clamp(x / 40, 0, 1); },
    show: (p) => p.life && p.life.carfree_pct != null ? [p.life.carfree_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'jobs', label: 'The job market', col: 'Unemp', g: 'Life there',
    hint: 'Unemployment rate, 2021.',
    kind: 'flag', def: 1, w: 0, want: 'To find work there',
    score: (p) => { const x = p.life ? p.life.unemployment : null;
      if (x == null) return null; return clamp(1 - (x - 4) / 14, 0, 1); },
    show: (p) => { const x = p.life ? p.life.unemployment : null;
      return x == null ? null : [x.toFixed(1), '%']; },
  },
  {
    id: 'mix', label: 'Mix of people', col: 'Diverse', g: 'Life there',
    hint: 'Share of residents who are immigrants.',
    kind: 'flag', def: 1, w: 0, want: 'A mixed, diverse place',
    score: (p) => { const x = p.life ? p.life.immigrants_pct : null;
      if (x == null) return null; return clamp(x / 35, 0, 1); },
    show: (p) => p.life && p.life.immigrants_pct != null ? [p.life.immigrants_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'french', cc: ['CA'], label: 'French', col: 'French', g: 'Life there',
    hint: 'Share whose first official language is French.',
    kind: 'opts', def: 'yes', w: 0,
    opts: [['yes','I want to live in French'],['some','Some is nice']],
    score: (p, v) => { const x = p.life ? p.life.french_pct : null;
      if (x == null) return null;
      return v === 'yes' ? clamp(x / 70, 0, 1) : near(x, 25, 45); },
    show: (p) => p.life && p.life.french_pct != null ? [p.life.french_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'kids', label: 'Kids around', col: 'Kids', g: 'Life there',
    hint: 'Share of the population under 15. The median place is 16%.',
    kind: 'opts', def: 'many', w: 0,
    opts: [['many','Lots of young families'],['few','Not many children']],
    score: (p, v) => { const x = p.demo ? p.demo.children_pct : null;
      if (x == null) return null;
      return v === 'many' ? clamp((x - 8) / 14, 0, 1) : clamp(1 - (x - 8) / 14, 0, 1); },
    show: (p) => p.demo && p.demo.children_pct != null ? [p.demo.children_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'single', label: 'Single people', col: 'Single', g: 'Life there',
    hint: 'Share of adults who have never married. The median place is 26%.',
    kind: 'opts', def: 'single', w: 0,
    opts: [['single','A lot of single people'],['settled','Mostly settled couples']],
    score: (p, v) => { const x = p.demo ? p.demo.never_married_pct : null;
      if (x == null) return null;
      return v === 'single' ? clamp((x - 15) / 25, 0, 1) : clamp(1 - (x - 15) / 25, 0, 1); },
    show: (p) => p.demo && p.demo.never_married_pct != null
      ? [p.demo.never_married_pct.toFixed(0), '%'] : null,
  },
  {
    id: 'gender', label: 'Gender balance', col: 'M/100F', g: 'Life there',
    hint: 'Men per 100 women. Resource towns run high, retirement towns low.',
    kind: 'opts', def: 'even', w: 0,
    opts: [['women','More women than men'],['even','About even'],['men','More men than women']],
    score: (p, v) => { const x = p.demo ? p.demo.males_per_100_females : null;
      if (x == null) return null;
      return near(x, { women: 88, even: 100, men: 112 }[v], 16); },
    show: (p) => p.demo && p.demo.males_per_100_females != null
      ? [p.demo.males_per_100_females.toFixed(0), ''] : null,
  },
  {
    id: 'faith', cc: ['CA'], label: 'Faith community', col: 'Faith', g: 'Life there',
    hint: 'Somewhere your own community is actually present.',
    kind: 'opts', def: 'none', w: 0,
    opts: [['christian','Christian'],['muslim','Muslim'],['jewish','Jewish'],['sikh','Sikh'],
           ['hindu','Hindu'],['buddhist','Buddhist'],['none','Somewhere secular']],
    score: (p, v) => {
      const d = p.demo; if (!d) return null;
      const x = d[v === 'none' ? 'no_religion_pct' : v + '_pct'];
      if (x == null) return null;
      // a community is "present" well below a majority: 10% of a city is a lot of
      // people and plenty of institutions, so the curve saturates early.
      return v === 'none' || v === 'christian' ? clamp(x / 70, 0, 1) : clamp(x / 10, 0, 1);
    },
    show: (p) => { const d = p.demo; if (!d) return null;
      const v = state.faith, x = d[v === 'none' ? 'no_religion_pct' : v + '_pct'];
      return x == null ? null : [x.toFixed(x < 10 ? 1 : 0), '%']; },
  },
  {
    /* The US census is barred by law from asking about religion, so where the
       Canadian question measures the share of people, this one counts the actual
       buildings you could drive to. Different measurement, said so in the hint.
       Saturation is per religion because the base rates are nothing alike: a town
       with 8 synagogues is a real Jewish community, 8 churches is a small town. */
    id: 'worship', cc: ['US'], label: 'Faith community', col: 'Faith', g: 'Life there',
    hint: 'Places of worship of your faith within a 15km drive, counted from OpenStreetMap.',
    kind: 'opts', def: 'christian', w: 0,
    opts: [['christian','Christian'],['muslim','Muslim'],['jewish','Jewish'],
           ['sikh','Sikh'],['hindu','Hindu'],['buddhist','Buddhist']],
    score: (p, v) => {
      const o = p.osm; if (!o) return null;
      // Saturation per religion, set so the question GRADES rather than just
      // passes. At 6 synagogues everything from a single shul to Brooklyn tied at
      // a perfect score, which answers "is there a community" but cannot tell a
      // reader where the community is largest.
      const F = { christian: ['churches', 250], muslim: ['mosques', 14],
                  jewish: ['synagogues', 18], sikh: ['gurdwaras', 4],
                  hindu: ['temples_hindu', 7], buddhist: ['temples_buddhist', 7] }[v];
      const n = o[F[0]];
      if (n == null) return null;
      return clamp(Math.sqrt(n / F[1]), 0, 1);
    },
    show: (p) => { const o = p.osm; if (!o) return null;
      const f = { christian:'churches', muslim:'mosques', jewish:'synagogues',
                  sikh:'gurdwaras', hindu:'temples_hindu', buddhist:'temples_buddhist' }[state.worship];
      return o[f] == null ? null : [o[f], ''];
    },
  },
  {
    id: 'mood', label: 'What residents say', col: 'Mood', g: 'Life there',
    hint: `Only ${LIVED_N} of ${DATA.length} places are researched.`,
    kind: 'flag', def: 1, w: 0, want: 'Somewhere residents speak well of',
    noPick: true,   // shown as a column, not offered as something to rank on
    score: (p) => { if (!p.lived || !p.lived.sentiment) return null;
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


/* a question tagged with `cc` exists only in those countries: French is a
   Canadian question, and the US census does not ask about religion at all. */
const Q = Q_ALL.filter((q) => !q.cc || q.cc.includes(CFG.cc));

/* what each column of the plate actually is, in words, on hover and on the
   help strip. an abbreviation nobody can expand is not a label. */
const COLHELP = {
  winter:  ['Average January temperature', '°C', CFG.sources.climate],
  summer:  ['Average July temperature', '°C', CFG.sources.climate],
  swing:   ['How far the year swings, July mean minus January mean', '°C', CFG.sources.climate],
  rain:    ['Total precipitation in a year', 'mm', CFG.sources.climate],
  snow:    ['Snow that falls in a year', 'cm', CFG.sources.climate],
  sun:     ['Hours of bright sunshine in a year', 'h', CFG.sources.climate],
  smoke:   ['Wildfire smoke in the air, 12-year average', 'µg/m³ of fine particulate',
            CFG.sources.smoke],
  size:    ['People who live there', '', CFG.sources.pop],
  prox:    ['Drive to the nearest city over 300,000', 'minutes', 'Routed on real roads'],
  cost:    ['What an average home is worth', '', '2021 Census, what owners estimated in 2021'],
  politics:[`Political lean of the ${CFG.sources.politics_unit}`, '-100 left to +100 right', CFG.sources.politics],
  growth:  ['How much the population changed, 2016 to 2021', '%', CFG.sources.census],
  age:     ['Median age. Under 40 is a working town, over 55 a retirement one', 'years', CFG.sources.census],
  commute: ['Share of workers who get there in under 15 minutes', '%', CFG.sources.census],
  car:     ['Share who get to work by transit, foot or bike', '%', CFG.sources.census],
  jobs:    ['Unemployment rate', '%', CFG.sources.census],
  mix:     ['Share of residents who are immigrants', '%', CFG.sources.census],
  french:  ['Share whose first official language is French', '%', CFG.sources.census],
  water:   ['Distance to the ocean or a big lake', 'km', 'Natural Earth shoreline geometry'],
  pitches: ['Soccer pitches within a 15km drive', '', 'OpenStreetMap'],
  sports:  ['Top-tier pro leagues playing there', '', 'League and team sources, verified 2026'],
  transit: ['Rapid transit serving the place', '', 'Transit authority and line sources, verified 2026'],
  kids:    ['Share of the population under 15', '%', CFG.sources.census],
  single:  ['Share of adults who have never married', '%', CFG.sources.census],
  gender:  ['Men per 100 women', '', CFG.sources.census],
  faith:   ['Share of residents in the community you picked', '%', CFG.sources.religion],
  worship: ['Places of worship of the faith you picked, within a 15km drive', '', 'OpenStreetMap'],
  mood:    ['How residents sound about the place, -2 to +2', '', 'Forums, local news and blogs. Only where researched.'],
};

const SHORT = { winter:'the winter', summer:'the summer', snow:'the snow', sun:'the sun',
  swing:'the seasons', rain:'the rain',
  smoke:'clean air', size:'the size', prox:'the drive', cost:'the price',
  politics:'the politics', mood:'the mood', growth:'the growth', age:'the crowd',
  commute:'the short commute', car:'getting around without a car', jobs:'the job market',
  mix:'the mix of people', french:'the French', kids:'the young families',
  single:'the single crowd', gender:'the gender balance', faith:'your community',
  water:'the water', pitches:'the soccer', sports:'the pro team', transit:'the train',
  worship:'your faith community' };
const said = (q) => q.kind === 'range' ? q.fmt(state[q.id])
  : q.kind === 'flag' ? q.want.toLowerCase()
  : (q.opts.find((o) => o[0] === state[q.id]) || ['',''])[1];
/* short name for the picker tile. the survey label is a sentence heading;
   a tile needs two or three words that read at a glance. */
const PICKLABEL = { winter:'Winter', summer:'Summer', swing:'Seasons', rain:'Rain',
  snow:'Snow', sun:'Sun', smoke:'Clean air', size:'Size of place', prox:'Near a city',
  cost:'Housing cost', politics:'Politics', growth:'Growing', age:'Who lives there',
  commute:'Short commute', car:'Life without a car', jobs:'Jobs', mix:'Diverse',
  french:'French', mood:'What locals say', kids:'Kids around', single:'Single people',
  gender:'Gender balance', faith:'Faith community', worship:'Faith community',
  water:'Near water',
  pitches:'Soccer pitches', sports:'Pro sports', transit:'Rapid transit' };
const listify = (a) => a.length < 2 ? (a[0]||'') : a.slice(0,-1).join(', ') + ' and ' + a[a.length-1];
function fmtNum(n) {
  if (n == null) return NA;
  if (n >= 1e6) return (n/1e6).toFixed(2) + 'M';
  if (n >= 1e3) return (n/1e3).toFixed(n >= 1e4 ? 0 : 1) + 'k';
  return String(Math.round(n));
}

/* ---------- state, and the shareable link ----------
   You PICK up to five things that matter and RANK them by the order you pick.
   Everything you did not pick is not scored at all.

   This replaced an importance dial on all nineteen dimensions. That dial was
   unreadable ("how much does winter matter" nineteen times), and worse, it let
   seventeen lukewarm answers outvote the one thing someone actually cared
   about. Five ranked picks say the same thing in a fifth of the taps. */
const MAX_PICKS = 5;
const state = {};
let picks = [];
Q.forEach((q) => { state[q.id] = q.def; });
let selected = null;
let showAll = false;
const PLATE_N = 60;   // a plate shows the confusion set, not the whole book

let query = '';   // the "find a place" filter. keeps each place's true rank.
/* the link carries the picks in rank order, each as questionIndex.value */
const encodeState = () => picks.map((id) => {
  const q = Q.find((x) => x.id === id);
  const v = q.kind === 'range' ? String(state[id])
          : q.kind === 'flag' ? '0'
          : String(q.opts.findIndex((o) => o[0] === state[id]));
  return Q.indexOf(q) + '.' + v;
}).join('_');
function decodeState(s) {
  const parts = (s || '').split('_').filter(Boolean);
  if (!parts.length || parts.length > MAX_PICKS) return false;
  const next = [];
  try {
    for (const part of parts) {
      const [qi, val] = part.split('.');
      const q = Q[+qi];
      if (!q || next.includes(q.id)) throw 0;
      if (q.kind === 'range') {
        const n = +val; if (!Number.isFinite(n)) throw 0;
        state[q.id] = clamp(n, q.min, q.max);
      } else if (q.kind === 'opts') {
        const o = q.opts[+val]; if (!o) throw 0; state[q.id] = o[0];
      }
      next.push(q.id);
    }
    picks = next;
    return true;
  } catch (e) { return false; }
}
let shared = location.hash.length > 2 && decodeState(location.hash.slice(1));
function ownIt() {   // the moment they change anything, the result is theirs, not the sender's
  if (!shared) return;
  shared = false;
  const l = $('#lede'); if (l && ORIG_LEDE) l.innerHTML = ORIG_LEDE;
}

/* ---------- scoring ----------
   1. Weight comes from your ranking. With n picks, your first counts n and your
      last counts 1, so a full five reads 5-4-3-2-1. It is stated on the page in
      those words, because a weighting nobody can explain is a black box.

   2. The fit is a weighted power mean with p<1, not a plain average. A plain
      average is fully compensatory: a place can fail the one thing you care
      most about and still win by being mediocre on everything else. p=0.5
      makes a bad score on a heavy dimension bite instead of averaging out.  */
const P_MEAN = 0.5;
const wOf = (id) => { const i = picks.indexOf(id); return i < 0 ? 0 : picks.length - i; };

function scoreAll() {
  const out = DATA.map((p) => {
    let num = 0, den = 0;
    const parts = [];
    let excluded = null;
    const cells = {};
    let wantW = 0;               // total weight the user asked for
    for (const q of Q) {
      const s = q.score(p, state[q.id]);
      cells[q.id] = s;
      const w = wOf(q.id);
      if (!w) continue;
      if (q.hard && q.hard(p, state[q.id])) excluded = q.hardWhy;
      wantW += w;
      if (s == null) continue;   // missing data
      num += w * Math.pow(s, P_MEAN); den += w;
      parts.push({ id: q.id, s, w, pull: w * (s - 0.5) });
    }
    // coverage: a place missing a dimension you weighted heavily used to get a
    // free pass (dropped from the average) and could float to the top on the
    // criterion it lacked. Dock the fit by how much of your weighted preference
    // it actually has data for, so missing your #1 priority hurts.
    const coverage = wantW ? den / wantW : 1;
    const raw = den ? Math.pow(num / den, 1 / P_MEAN) * 100 : 0;
    const missing = Q.filter((q) => wOf(q.id) && cells[q.id] == null && q.col);
    parts.sort((a, b) => b.pull - a.pull);
    return { p, fit: raw * (0.55 + 0.45 * coverage), parts, cells, excluded, coverage, missing,
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
    if (!wOf(q.id)) continue;
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

/* ---------- the map ----------
   A hardiness map does not scatter dots, it floods the country in bands.
   So every square of the sheet takes the zone colour of the nearest ranked
   place: 4,197 points become a continuous field at finer resolution than
   the county choropleths this category ships. Drawn into a small ImageData
   and scaled up with smoothing OFF, so the band edges stay hard and printed
   rather than blurring into a gradient. */
let _fieldCache = { key: null, canvas: null };
let ZONE_BREAKS = null;      // the quantile cuts, so the legend can state them

function zoneField(W, H, k) {
  // cache on the ranking, so panning or a tooltip never recomputes it
  const key = W + 'x' + H + ':' + ranked.length + ':' + picks.join(',') +
              ':' + Q.map((q) => state[q.id]).join(',');
  if (_fieldCache.key === key) return _fieldCache.canvas;

  const SC = 4;                                  // one field cell per 4 device px
  const fw = Math.max(1, Math.ceil(W / SC)), fh = Math.max(1, Math.ceil(H / SC));
  const off = document.createElement('canvas');
  off.width = fw; off.height = fh;
  const octx = off.getContext('2d');
  const img = octx.createImageData(fw, fh);
  const d = img.data;

  // bucket the places so each cell searches a handful, not all 4,197
  const BK = 48;
  const bw = Math.ceil(W / BK) + 1, bh = Math.ceil(H / BK) + 1;
  const buckets = new Array(bw * bh);
  const live = ranked.filter((r) => !r.excluded);
  for (const r of live) {
    const bx = Math.min(bw - 1, Math.max(0, (r.p.x * k / BK) | 0));
    const by = Math.min(bh - 1, Math.max(0, (r.p.y * k / BK) | 0));
    (buckets[by * bw + bx] || (buckets[by * bw + bx] = [])).push(r);
  }
  // Class the bands by QUANTILE, not by raw score. Fits cluster in the middle, so
   // splitting 0-100 into five equal slices painted almost everything one green and
   // the map said "everywhere is fine". A printed zone map classes so every band is
   // actually populated; this does the same, and the legend states the breaks.
  const fits = live.map((r) => r.fit).sort((p, q) => p - q);
  const brk = [0.2, 0.4, 0.6, 0.8].map((f) => fits[Math.floor(f * (fits.length - 1))] || 0);
  ZONE_BREAKS = brk;
  const bandOf = (f) => f < brk[0] ? 0 : f < brk[1] ? 1 : f < brk[2] ? 2 : f < brk[3] ? 3 : 4;
  const rgb = RAMP.map((n) => {
    const c = css(n).trim();
    return [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)];
  });

  for (let fy = 0; fy < fh; fy++) {
    const py = fy * SC + SC / 2;
    const by0 = (py / BK) | 0;
    for (let fx = 0; fx < fw; fx++) {
      const px = fx * SC + SC / 2;
      const bx0 = (px / BK) | 0;
      let best = null, bd = Infinity;
      // widen the ring until something is found; empty country is far from anywhere
      for (let ring = 0; ring <= 6 && !best; ring++) {
        for (let by = by0 - ring; by <= by0 + ring; by++) {
          if (by < 0 || by >= bh) continue;
          for (let bx = bx0 - ring; bx <= bx0 + ring; bx++) {
            if (bx < 0 || bx >= bw) continue;
            if (ring && Math.abs(by - by0) !== ring && Math.abs(bx - bx0) !== ring) continue;
            const cell = buckets[by * bw + bx];
            if (!cell) continue;
            for (const r of cell) {
              const dx = r.p.x * k - px, dy = r.p.y * k - py;
              const dd = dx * dx + dy * dy;
              if (dd < bd) { bd = dd; best = r; }
            }
          }
        }
        if (best && ring > 0) break;
      }
      const o = (fy * fw + fx) * 4;
      if (!best) { d[o + 3] = 0; continue; }
      const c = rgb[bandOf(best.fit)];
      d[o] = c[0]; d[o + 1] = c[1]; d[o + 2] = c[2]; d[o + 3] = 255;
    }
  }
  octx.putImageData(img, 0, 0);
  _fieldCache = { key, canvas: off };
  return off;
}

function drawMap() {
  const W = Math.round(cvs.getBoundingClientRect().width) || 800;
  const H = Math.round(W * (MAPGEO.height/1000));
  const dpr = window.devicePixelRatio || 1;
  cvs.width = W*dpr; cvs.height = H*dpr; cvs.style.height = H+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,W,H);
  const k = W/1000;
  ctx.lineJoin = 'round';

  // 1. clip to the country, so the field stops at the coastline
  ctx.save();
  ctx.beginPath();
  for (const rings of Object.values(MAPGEO.prov)) {
    for (const rg of rings) {
      rg.forEach(([x,y],i) => i ? ctx.lineTo(x*k,y*k) : ctx.moveTo(x*k,y*k));
      ctx.closePath();
    }
  }
  ctx.clip();

  // 2. flood it with zone bands
  const field = zoneField(W, H, k);
  ctx.imageSmoothingEnabled = false;             // hard printed edges, not a gradient
  ctx.drawImage(field, 0, 0, W, H);
  ctx.imageSmoothingEnabled = true;
  ctx.restore();

  // 3. state and province lines, cut back into the flood in the ground ink
  ctx.strokeStyle = css('--ink');
  ctx.lineWidth = 1;
  ctx.globalAlpha = 0.5;
  for (const rings of Object.values(MAPGEO.prov)) {
    for (const rg of rings) {
      ctx.beginPath();
      rg.forEach(([x,y],i) => i ? ctx.lineTo(x*k,y*k) : ctx.moveTo(x*k,y*k));
      ctx.closePath(); ctx.stroke();
    }
  }
  ctx.globalAlpha = 1;

  // 4. only the top matches get a mark. The field already says where is good.
  const small = MOBILE.matches;
  const NTOP = small ? 5 : 10;
  const topRecs = ranked.filter((r) => !r.excluded).slice(0, NTOP);
  pts = [];
  for (const r of ranked) pts.push({ x: r.p.x*k, y: r.p.y*k, r: small ? 7 : 6, rec: r });
  for (const r of topRecs.slice().reverse()) {
    const x = r.p.x*k, y = r.p.y*k;
    ctx.beginPath(); ctx.arc(x, y, small ? 5 : 6, 0, 6.284);
    ctx.fillStyle = css('--stock'); ctx.fill();
    ctx.strokeStyle = css('--ink'); ctx.lineWidth = 2.5; ctx.stroke();
  }

  const top = topRecs;
  ctx.font = `700 ${Math.max(11, k*13)}px 'Radio Canada', sans-serif`;
  ctx.textBaseline = 'middle';
  const placed = [];
  const hits = (a) => placed.some((b) => a.x < b.x+b.w && a.x+a.w > b.x && a.y < b.y+b.h && a.y+a.h > b.y);
  for (const r of top) {
    const x = r.p.x*k, y = r.p.y*k, t = r.p.name;
    const w = ctx.measureText(t).width, h = 13;
    let put = null;
    for (const [dx, dy] of [[10, 0], [-10 - w, 0], [0, -15], [0, 15], [10, -15], [-10 - w, 15]]) {
      const box = { x: x + dx, y: y + dy - h / 2, w, h };
      if (box.x < 3 || box.x + w > W - 3 || box.y < 3 || box.y + h > H - 3) continue;
      if (hits(box)) continue;
      put = box; break;
    }
    if (!put) continue;
    placed.push(put);
    // a label on a flooded map needs its own stock behind it or it is unreadable
    ctx.fillStyle = css('--stock');
    ctx.fillRect(put.x - 4, put.y - 2, w + 8, h + 5);
    ctx.fillStyle = css('--on-stock');
    ctx.fillText(t, put.x, put.y + h / 2 + 1);
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
  c.font = `9px 'Radio Canada', sans-serif`; c.fillStyle = css('--on-ink-3');
  t.forEach((v,i) => c.fillText(M[i], i*bw+bw/2-3, h-1));
}

/* ---------- the share card ----------
   A quiz result spreads as an IMAGE, not a link: people screenshot it into a group
   chat. A link cannot carry a rich preview here either, because the whole answer
   lives in the URL hash and a hash fragment is never sent to a server, so GitHub
   Pages can never render a per-result preview image. So the app draws the card
   itself and hands over a real file.

   The map is the point. Any quiz can print a name in big type; almost none can show
   you WHERE on a real projection, drawn from the same geometry as the app. That is
   the bit that makes the screenshot unmistakably this and not a personality test. */
const CARD_W = 1080, CARD_H = 1350;   // 4:5, the tallest a feed will show uncropped

async function drawCard() {
  const r = ranked.find((x) => !x.excluded);
  if (!r) return null;
  const p = r.p;
  try { await document.fonts.ready; } catch (e) {}   // never draw in a fallback face

  const c = document.createElement('canvas');
  c.width = CARD_W; c.height = CARD_H;
  const x = c.getContext('2d');
  const INK = css('--ink'), STOCK = css('--stock'), SIGNAL = css('--signal');
  const ONSTOCK = css('--on-stock'), ONSTOCK2 = css('--on-stock-2'), ONSTOCK3 = css('--on-stock-3');
  const ONINK2 = css('--on-ink-2'), ONINK3 = css('--on-ink-3');

  x.fillStyle = INK; x.fillRect(0, 0, CARD_W, CARD_H);
  const M = 72;
  x.fillStyle = SIGNAL; x.fillRect(0, 0, CARD_W, 14);

  x.textBaseline = 'alphabetic';
  x.fillStyle = SIGNAL;
  x.font = "700 26px 'Radio Canada', sans-serif";
  x.fillText('WHERE U BELONG', M, 116);

  x.fillStyle = ONINK2;
  x.font = "400 40px 'Radio Canada', sans-serif";
  x.fillText(shared ? 'They belong in' : 'You belong in', M, 200);

  // The name shrinks to fit rather than clipping, and the budget has to reserve the
  // province code AND the score plate. Budgeting for the plate alone let "Cape
  // Breton" push its NS straight under the 88.
  // No score on the card. A fit number invites an argument about the method
  // instead of about the place, and the card's job is a claim about YOU, not a
  // scorecard. The score stays on the result screen where the reasoning is.
  x.font = "400 38px 'Radio Canada', sans-serif";
  const pvW = x.measureText(p.prov).width;
  const maxW = CARD_W - M * 2 - pvW - 24;
  const NAME = p.name.toUpperCase();
  let size = 132;
  do { x.font = `700 ${size}px 'Radio Canada', sans-serif`; x.canvas.style.fontStretch = '75%'; size -= 4; }
  while (x.measureText(NAME).width > maxW && size > 40);
  x.fillStyle = STOCK;
  x.fillText(NAME, M, 322);
  const nameW = x.measureText(NAME).width;
  x.fillStyle = ONINK3;
  x.font = "400 38px 'Radio Canada', sans-serif";
  x.fillText(p.prov, M + nameW + 18, 322);

  // The map, from the same geometry the app draws. Height is CAPPED and the width
  // follows, because the two countries have very different aspect ratios: the US
  // sheet is wide and Canada's is nearly square, and a fixed width let the US map
  // run long enough to push the rows under the footer.
  const FOOT = 150, ROWS_TOP_GAP = 74;
  const mapY = 372, MAP_MAX_H = 430;
  const k = Math.min((CARD_W - M * 2) / 1000, MAP_MAX_H / MAPGEO.height);
  const mapW = 1000 * k, mapH = MAPGEO.height * k;
  const mapX = (CARD_W - mapW) / 2;               // centred, whatever the country
  x.save();
  // CLIP to the map box. The Canadian sheet is fitted to the inhabited band on
  // purpose, so the arctic islands run to y = -184 and bleed off the top edge the
  // way they do on a real map series. The app's canvas clips that; without the same
  // clip here the arctic painted straight over the province code in the headline.
  x.beginPath(); x.rect(mapX, mapY, mapW, mapH); x.clip();
  x.translate(mapX, mapY); x.lineJoin = 'round';
  for (const rings of Object.values(MAPGEO.prov)) {
    for (const rg of rings) {
      x.beginPath();
      rg.forEach(([px, py], i) => i ? x.lineTo(px * k, py * k) : x.moveTo(px * k, py * k));
      x.closePath();
      x.fillStyle = css('--ink-2'); x.fill();
    }
  }
  // the same zone flood the app draws, so the card is the map not a legend of it
  const fieldC = zoneField(Math.round(mapW), Math.round(mapH), k);
  x.imageSmoothingEnabled = false;
  x.drawImage(fieldC, 0, 0, mapW, mapH);
  x.imageSmoothingEnabled = true;
  x.strokeStyle = INK; x.lineWidth = 1.4; x.globalAlpha = 0.55;
  for (const rings of Object.values(MAPGEO.prov)) {
    for (const rg of rings) {
      x.beginPath();
      rg.forEach(([px, py], i) => i ? x.lineTo(px * k, py * k) : x.moveTo(px * k, py * k));
      x.closePath(); x.stroke();
    }
  }
  x.globalAlpha = 1;
  x.beginPath(); x.arc(p.x * k, p.y * k, 17, 0, 6.284);
  x.fillStyle = STOCK; x.fill();
  x.strokeStyle = INK; x.lineWidth = 5; x.stroke();
  x.restore();

  // what you asked for, and what it actually is there. Spacing is computed from
  // what is left rather than assumed, so five picks cannot run into the footer.
  const n = Math.min(picks.length, 5);
  let y = mapY + mapH + ROWS_TOP_GAP;
  x.fillStyle = SIGNAL;
  x.font = "700 26px 'Radio Canada', sans-serif";
  x.fillText('WHAT YOU ASKED FOR', M, y);
  y += 20;
  const step = n ? Math.min(62, (CARD_H - FOOT - y) / n) : 0;
  for (let i = 0; i < n; i++) {
    const q = Q.find((z) => z.id === picks[i]), v = q.show(p);
    y += step;
    x.fillStyle = css('--z5'); x.fillRect(M, y - 30, 34, 34);
    x.fillStyle = '#fff'; x.font = "700 22px 'Radio Canada', sans-serif";
    x.fillText(String(i + 1), M + 11, y - 6);
    x.fillStyle = STOCK; x.font = "700 34px 'Radio Canada', sans-serif";
    x.fillText(q.label, M + 52, y);
    if (v) {
      x.fillStyle = ONINK2; x.font = "400 34px 'Radio Canada', sans-serif";
      const t = v[0] + v[1];
      x.fillText(t, CARD_W - M - x.measureText(t).width, y);
    }
    x.strokeStyle = css('--rule'); x.lineWidth = 1;
    x.beginPath(); x.moveTo(M, y + 20); x.lineTo(CARD_W - M, y + 20); x.stroke();
  }

  // The tradeoff, never collapsed. A result with no stated cost is a horoscope.
  const giveUp = r.bad && r.bad.s < 0.45 ? SHORT[r.bad.id] : null;
  if (giveUp) {
    x.fillStyle = SIGNAL;
    x.font = "400 30px 'Radio Canada', sans-serif";
    x.fillText(`What you give up: ${giveUp}.`, M, CARD_H - 136);
  }
  x.fillStyle = ONINK3;
  x.font = "400 28px 'Radio Canada', sans-serif";
  x.fillText(`${DATA.length.toLocaleString()} places in ${CFG.country}, ranked on real data`, M, CARD_H - 92);
  x.fillStyle = ONINK2;
  x.font = "700 28px 'Radio Canada', sans-serif";
  x.fillText(SHARE_HOST, M, CARD_H - 48);
  return c;
}
const SHARE_HOST = location.host + location.pathname.replace(/index\.html$/, '');

async function shareCard() {
  const c = await drawCard(); if (!c) return;
  const top = ranked.find((r) => !r.excluded);
  const text = `Apparently I belong in ${top.p.name}, ${top.p.prov}. Where do you belong?`;
  const blob = await new Promise((res) => c.toBlob(res, 'image/png'));
  const file = new File([blob], 'where-u-belong.png', { type: 'image/png' });
  // Web Share with a file is the good path on a phone. Everything else downloads.
  if (navigator.canShare && navigator.canShare({ files: [file] })) {
    try { await navigator.share({ files: [file], text, title: 'Where U Belong' }); return; }
    catch (e) { if (e && e.name === 'AbortError') return; }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'where-u-belong.png'; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
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
      conflict = `Nowhere in ${CFG.country} is both <b>${said(a).toLowerCase()}</b> (${a.label.toLowerCase()})
        and <b>${said(b).toLowerCase()}</b> (${b.label.toLowerCase()}). ${p.name} is the closest compromise.`;
    } else if (worst.length === 1) {
      const a = Qof(worst[0].id);
      conflict = `Nowhere that fits the rest of your answers is also <b>${said(a).toLowerCase()}</b>
        (${a.label.toLowerCase()}). That is the one giving way.`;
    }
  }
  /* The point of ranking 710 places rather than the famous 30 is that the answer
     can be somewhere you have never heard of. Find the best-scoring small place
     that is not already in the top three, and say so out loud. */
  const wild = ranked.find((x) => !x.excluded && x !== r
    && ranked.filter((y) => !y.excluded).indexOf(x) > 2
    && (x.p.pop || 0) < 30000 && x.fit > r.fit - 12);

  const cutMsg = cut > ranked.length * 0.5
    ? `Your dealbreakers rule out ${cut} of ${ranked.length} places.` : null;

  /* Your five answers, each with what this place actually scored on it, and a link
     back to change it. This is the GOV.UK check-answers pattern: it is the "why",
     the decomposition and the edit affordance in one boring, legible component.
     It is deliberately NOT hidden behind a click - the whole argument for the
     result screen is that the reasoning arrives without being asked for. */
  const rows = picks.map((id, i) => {
    const q = Q.find((x) => x.id === id);
    const sc = r.cells[id], val = q.show(p);
    const bar = sc == null ? '' :
      `<span class="ca-bar"><i style="width:${Math.round(sc*100)}%;background:${rampOf(sc*100)}"></i></span>`;
    return `<div class="ca-row">
      <span class="ca-k"><span class="q-rank">${i + 1}</span>${q.label}</span>
      <span class="ca-v">${said(q)}</span>
      <span class="ca-got">${val ? `${p.name} is <b>${val[0]}${val[1]}</b>` :
        `<span class="na">not recorded here</span>`}${bar}</span>
      <button class="ca-ch" data-goq="${i}">Change</button>
    </div>`;
  }).join('');

  host.innerHTML = `
    <div class="v-hero">
      <p class="v-lead">${shared ? 'They belong in' : 'You belong in'}</p>
      <h2 class="v-name">${p.name}<span class="pv">${p.prov}</span></h2>
      <p class="v-line">${reasons.length ? `It gets you ${listify(reasons)}.` : 'It is the closest thing to what you asked for.'}
        ${against ? `<span class="cut">You give up ${against}.</span>` : ''}</p>
      <p class="v-score">Fit <b>${Math.round(r.fit)}</b> out of 100${
        r.coverage < 0.999 ? `, on the ${Math.round(r.coverage*100)}% of your answers it has data for` : ''}</p>
    </div>

    <div class="checkans">
      <p class="ca-head">Why, answer by answer</p>
      ${rows}
    </div>

    ${conflict || cutMsg ? `<p class="v-warn">${[cutMsg, conflict].filter(Boolean).join(' ')}</p>` : ''}
    ${cf ? `<p class="v-catch">Nearly the same on your answers: <b>${cf.others.join(', ')}</b>.
      What separates them is <b>${SHORT[cf.splitter]}</b>.</p>` : ''}
    ${L.honest_downside ? `<p class="v-catch"><b>The catch, from people who live there.</b> ${L.honest_downside}</p>` : ''}
    ${wild ? `<p class="v-wild"><b>One you were probably not thinking of.</b>
      <span class="v-wn">${wild.p.name}<span class="pv">${wild.p.prov}</span></span>
      population ${fmtNum(wild.p.pop)}, and it scores ${Math.round(wild.fit)} on the same answers.</p>` : ''}

    ${runners.length ? `<p class="v-next">Then <b>${runners.map((x)=>x.p.name).join('</b>, <b>')}</b>.</p>` : ''}
    <div class="v-foot">
      <button class="v-share" id="sharecard">Save the picture</button>
      <button class="v-again" id="share">Send the link</button>
      <button class="v-again" id="vagain">Start over</button>
    </div>
    <p class="v-prov">${CFG.prov_line} Nothing here is a recommendation, and where a number
      is missing it is dropped rather than guessed at.</p>`;
}

function cellHTML(q, r) {
  const v = q.show(r.p);
  if (!v) return `<span class="cell"><span class="na">${NA}</span></span>`;
  const s = r.cells[q.id];
  const tint = (s != null && wOf(q.id)) ? `background:${rampOf(s*100)}` : '';
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
      ${row(p.pop_year === 2025 ? 'People (2025 estimate)' : 'People', fmtNum(p.pop), '')}
      ${row('Home, average value', p.cost && p.cost.home_price ? '$'+fmtNum(p.cost.home_price) : NA, '')}
      ${row('Rent and utilities', p.cost && p.cost.rent_2br ? '$'+Math.round(p.cost.rent_2br) : NA, '/mo')}
      ${row('Median household income', p.cost && p.cost.median_hh_income ? '$'+fmtNum(p.cost.median_hh_income) : NA, '')}
      ${row('Unemployment', p.cost && p.cost.unemployment != null ? p.cost.unemployment : NA, '%')}
      ${row('Nearest city over 300k', p.prox ? p.prox.nearest_big_city : NA,
        p.prox && p.prox.drive_min_to_big_city != null ? `${Math.round(p.prox.drive_min_to_big_city)}min` : '')}
      ${row(CFG.riding_label, p.politics ? p.politics.riding : NA, '')}
      ${row('Lean', p.politics ? p.politics.lean_label : NA, '')}
      <p class="prov-note">${p.csd ? `Census figures are for <em>${p.csd}</em>.` : ''} ${CFG.detail_note}</p>
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
           ${p.name} yet, so this column is empty rather than guessed. ${LIVED_N} of ${DATA.length} places are done.
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
// which places to list, each carrying its TRUE rank in the full ranking. When
// searching, show every name match (not just the top slice) so "Goderich" is
// findable at rank 334 without scrolling.
function displayList() {
  if (query) {
    const q = query.toLowerCase();
    return ranked.map((r, i) => ({ r, rank: i })).filter((x) => x.r.p.name.toLowerCase().includes(q));
  }
  const shown = showAll ? ranked.length : Math.min(PLATE_N, ranked.length);
  return ranked.slice(0, shown).map((r, i) => ({ r, rank: i }));
}

function draw() {
  ranked = scoreAll();
  history.replaceState(null, '', picks.length ? '#' + encodeState() : location.pathname);
  // only the screen on show gets built. The table is 710 rows by 27 columns and
  // there is no reason to pay for it while someone is still picking.
  if (screen === 'result') { verdict(); return; }
  if (screen !== 'explore') return;
  drawExplore();
}

function drawExplore() {
  const live = ranked.filter((r) => !r.excluded);
  const list = displayList();
  $('.plate').dataset.view = exView;
  $('#total').textContent = DATA.length;
  $('#count').innerHTML = query
    ? `${list.length} match${list.length === 1 ? '' : 'es'} for “${query}”` +
      ` &nbsp;<button class="showall" id="clearsearch">clear</button>`
    : `${live.length} of ${DATA.length} clear your dealbreakers` +
      (ranked.length > PLATE_N ? ` &nbsp;<button class="showall" id="showall">${
        showAll ? 'show the top 60' : `show all ${ranked.length}`}</button>` : '');
  if (exView === 'list') { drawCards(); return; }
  if (exView === 'map')  { drawMap(); return; }
  drawTable();
}

function drawTable() {
  const list = displayList();
  const cols = Q.filter((q) => q.col);
  $('#thead').innerHTML = `<tr><th></th><th class="l">Place</th><th>Fit</th>
    ${cols.map((q) => { const h = COLHELP[q.id] || [q.label,'',''];
      return `<th${wOf(q.id) ? '' : ' style="opacity:.45"'} title="${h[0]}${h[1] ? ' ('+h[1]+')' : ''}. ${h[2]}">${q.col}</th>`; }).join('')}
    <th title="Provenance"></th></tr>`;

  $('#tbody').innerHTML = list.map(({ r, rank }) => {
    const p = r.p, key = p.name + p.prov, cf = !r.excluded ? confusion(r, ranked) : null;
    // width axis carries settlement size: a big city sets wide, a village narrow
    const wd = p.pop ? clamp(75 + (Math.log10(Math.max(p.pop,300)) - 2.5) / 4 * 25, 75, 100) : 88;
    return `<tr class="${r.excluded ? 'cut' : ''}">
      <td class="rank">${r.excluded ? '' : rank+1}</td>
      <td class="pname" style="--w:${wd.toFixed(0)}%"><button data-i="${rank}">${p.name}<span class="pv">${p.prov}</span></button></td>
      <td class="fit"><span class="b" style="background:${r.excluded ? css('--sink') : rampOf(r.fit)}">${
        r.excluded ? '—' : Math.round(r.fit)}</span></td>
      ${cols.map((q) => `<td class="${cf && cf.splitter === q.id ? 'split' : ''}">${cellHTML(q, r)}</td>`).join('')}
      <td class="prov"><i class="${p.lived ? 'full' : 'none'}" title="${
        p.lived ? 'Residents researched' : 'Not researched'}"></i></td>
    </tr>` + (selected === key ? `<tr class="detail"><td colspan="${cols.length + 4}">${detailHTML(r)}</td></tr>` : '');
  }).join('');

  const rib = $('[data-rib]');
  if (rib) { const r = ranked.find((x) => x.p.name + x.p.prov === selected); if (r) ribbon(rib, r.p); }
}

/* ---------- mobile: ranked cards + detail sheet ----------
   Each card is a place with the 2-3 stats that decided it, per the mobile
   research: a comparison table only helps at <=5 items, so 712 places on a
   phone are a ranked list, not a grid. Tapping opens the full record in a sheet. */
const MOBILE = matchMedia('(max-width: 760px)');

function drawCards() {
  const list = displayList();
  const live = ranked.filter((r) => !r.excluded).length;
  const head = `<li class="cards-head">` + (query
    ? `${list.length} match${list.length === 1 ? '' : 'es'} for “${query}” · <button class="showall" id="clearsearch">clear</button>`
    : `${live} of ${DATA.length} clear your dealbreakers` +
      (ranked.length > 80 ? ` · <button class="showall" id="showall">${showAll ? 'top 80' : 'show all'}</button>` : '')) + `</li>`;
  $('#cards').innerHTML = head + (list.length ? list.map(({ r, rank }) => {
    const p = r.p;
    // the 2-3 dimensions the user weighted most, with this place's actual value
    const chips = r.parts.slice(0, 3).map((pt) => {
      const q = Q.find((x) => x.id === pt.id); const v = q.show(p);
      return v ? `<span class="chip">${q.col} <b>${v[0]}${v[1]}</b></span>` : '';
    }).filter(Boolean).join('');
    const why = r.excluded
      ? `<span class="cut">Ruled out on ${r.excluded}</span>`
      : (r.good.length ? `Gets you ${listify(r.good.map((g) => SHORT[g.id]))}` : 'the closest to what you asked');
    return `<li><button class="pcard ${r.excluded ? 'excl' : ''}" data-i="${rank}">
      <span class="pr">${r.excluded ? '—' : rank + 1}</span>
      <span class="pn">${p.name}<span class="pv">${p.prov}</span></span>
      <span class="pf" style="background:${r.excluded ? 'var(--sink)' : rampOf(r.fit)}">${r.excluded ? '—' : Math.round(r.fit)}</span>
      <span class="pwhy">${why}</span>
      <span class="chips">${chips}</span>
    </button></li>`;
  }).join('') : `<li class="cards-head" style="color:var(--ink-3)">No place named “${query}”. Try part of the name.</li>`);
}

function openSheet(r) {
  $('#sheetBody').innerHTML = `<div class="sheet-name">${r.p.name}<span class="pv">${r.p.prov}</span></div>` + detailHTML(r);
  const sh = $('#sheet'); sh.hidden = false;
  const rib = sh.querySelector('[data-rib]'); if (rib) ribbon(rib, r.p);
  if (!history.state || !history.state.sheet)
    history.pushState({ sheet: true }, '', location.href);   // back-button closes it, hash stays put
  document.body.style.overflow = 'hidden';
}
function closeSheet(pop) {
  const sh = $('#sheet'); if (sh.hidden) return;
  sh.hidden = true; document.body.style.overflow = '';
  if (!pop && history.state && history.state.sheet) history.back();
}
$('#sheetClose').addEventListener('click', () => closeSheet());
$('#sheetScrim').addEventListener('click', () => closeSheet());
addEventListener('popstate', () => closeSheet(true));

$('#cards').addEventListener('click', (e) => {
  const b = e.target.closest('.pcard'); if (!b) return;
  openSheet(ranked[+b.dataset.i]);
});

/* ---------- screens ----------
   One thing at a time. Everything used to be on a single scroll: the picker, the
   answers, the verdict, a search box, a map, cards and a 27-column table. That is
   what made it unreadable. Now: pick, answer one question at a time, get a result,
   and the field guide waits behind one button for anyone who wants the numbers. */
const root = $('#sheetRoot');
let screen = 'pick';        // pick | ask | result | explore
let askIdx = 0;
let exView = 'list';        // list | map | table

function goTo(s) {
  screen = s;
  root.dataset.screen = s;
  if (s === 'ask') {
    if (!picks.length) { screen = 'pick'; root.dataset.screen = 'pick'; }
    else askIdx = clamp(askIdx, 0, picks.length - 1);
  }
  if (screen === 'pick') buildPicker();
  if (screen === 'ask') buildAsk();
  actionbar();
  render();
  scrollTo(0, 0);
}

function actionbar() {
  const bar = $('#actionbar'), n = picks.length;
  if (screen === 'pick') {
    bar.innerHTML = `<button class="ab-main" id="abGo"${n ? '' : ' disabled'}>${
      n ? `Answer ${n} question${n > 1 ? 's' : ''}` : 'Pick at least one thing'}</button>`;
  } else if (screen === 'ask') {
    bar.innerHTML = `<button class="ab-back" id="abBack">Back</button>
      <button class="ab-main" id="abGo">${
        askIdx >= n - 1 ? 'Where do I belong?' : 'Next'}</button>`;
  } else if (screen === 'result') {
    bar.innerHTML = `<button class="ab-back" id="abEdit">Change answers</button>
      <button class="ab-main" id="abExplore">See all ${DATA.length}</button>`;
  } else {
    // on the field guide the way back to your answer is the primary move, not editing
    bar.innerHTML = `<button class="ab-back" id="abEdit">Change answers</button>
      <button class="ab-main" id="abResult">Back to my result</button>`;
  }
}

$('#actionbar').addEventListener('click', (e) => {
  const b = e.target.closest('button'); if (!b || b.disabled) return;
  if (b.id === 'abGo' && screen === 'pick') { askIdx = 0; goTo('ask'); return; }
  if (b.id === 'abGo' && screen === 'ask') {
    if (askIdx >= picks.length - 1) goTo('result');
    else { askIdx++; buildAsk(); actionbar(); scrollTo(0, 0); }
    return;
  }
  if (b.id === 'abBack') {
    if (askIdx > 0) { askIdx--; buildAsk(); actionbar(); scrollTo(0, 0); }
    else goTo('pick');
    return;
  }
  if (b.id === 'abEdit') goTo('pick');
  if (b.id === 'abExplore') goTo('explore');
  if (b.id === 'abResult') goTo('result');
});

// the three ways to read the same ranking
$('#vswitch').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-view]'); if (!b) return;
  exView = b.dataset.view;
  $('#vswitch').querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', x === b));
  render();
});

// re-render when crossing the desktop/mobile boundary so the right structure builds
MOBILE.addEventListener('change', () => { selected = null; render(); });

/* ---------- survey ----------
   Two parts. The picker is every dimension as a tile; tapping one adds it to
   your ranking and stamps it with its number. Below it, only the things you
   picked ask you anything. Pick nothing and you are asked nothing. */
const PICKABLE = Q.filter((q) => !q.noPick);
function buildPicker() {
  const qt = $('#qtotal'); if (qt) qt.textContent = PICKABLE.length;   // never let the copy go stale
  let lastG = null;
  const host = $('#picker');
  host.innerHTML = PICKABLE.map((q) => {
    const head = q.g !== lastG ? `<p class="pk-g">${q.g}</p>` : '';
    lastG = q.g;
    const i = picks.indexOf(q.id);
    return head + `<button class="pk${i >= 0 ? ' on' : ''}" type="button" data-pick="${q.id}"
      aria-pressed="${i >= 0}" aria-label="${PICKLABEL[q.id] || q.label}${i >= 0 ? `, ranked ${i+1}` : ''}"
      >${i >= 0 ? `<span class="pk-n">${i + 1}</span>` : ''}${PICKLABEL[q.id] || q.label}</button>`;
  }).join('');
  host.classList.toggle('full', picks.length >= MAX_PICKS);
  const n = picks.length;
  $('#pkcount').innerHTML = n === 0
    ? `Tap up to ${MAX_PICKS}. The order you tap is the order they count.`
    : n >= MAX_PICKS
      ? `That is your ${MAX_PICKS}. Tap one again to swap it out.`
      : `<b>${n} of ${MAX_PICKS}</b> picked. ${n === 1 ? 'Pick another, or stop here.' : 'Keep going, or stop here.'}`;
}

/* the control for one question. Shared by the solo ask screen. */
function controlHTML(q) {
  if (q.kind === 'range') return `<div class="slider-row">
      <button class="step" type="button" data-step="${q.id}" data-dir="-1" aria-label="Lower ${q.label}">&minus;</button>
      <input type="range" id="r-${q.id}" min="${q.min}" max="${q.max}"
        step="${q.step}" value="${state[q.id]}" aria-label="${q.label}">
      <button class="step" type="button" data-step="${q.id}" data-dir="1" aria-label="Raise ${q.label}">+</button>
      <span class="readout" id="o-${q.id}">${q.fmt(state[q.id])}</span></div>
    <div class="scale-ends"><span>${q.ends[0]}</span><span>${q.ends[1]}</span></div>`;
  if (q.kind === 'flag') return `<p class="q-flag">${q.want}.</p>
    <p class="q-flagnote">Nothing to set here. You picked it, so it counts.</p>`;
  return `<div class="opts opts-big">${q.opts.map(([v,l]) => `<button class="opt" data-q="${q.id}" data-v="${v}"
      aria-pressed="${state[q.id]===v}">${l}</button>`).join('')}</div>`;
}

/* one question, filling the screen, in rank order. */
function buildAsk() {
  const id = picks[askIdx]; if (!id) return;
  const q = Q.find((x) => x.id === id);
  const nth = ['your top priority','your second priority','your third priority',
               'your fourth priority','your fifth priority'][askIdx] || 'a priority';
  $('#askProg').textContent = `Question ${askIdx + 1} of ${picks.length}`;
  $('#askTitle').textContent = q.label;
  $('#qs').innerHTML = `<div class="q q-solo">
      <p class="q-rankline"><span class="q-rank">${askIdx + 1}</span>This is ${nth}</p>
      <p class="q-hint">${q.hint}</p>
      ${controlHTML(q)}
    </div>`;
  $('#askdots').innerHTML = picks.map((_, i) =>
    `<span class="dot${i === askIdx ? ' on' : i < askIdx ? ' done' : ''}"></span>`).join('');
}

$('#picker').addEventListener('click', (e) => {
  const b = e.target.closest('.pk'); if (!b) return;
  const id = b.dataset.pick, i = picks.indexOf(id);
  if (i >= 0) picks.splice(i, 1);                       // tap again to drop, the rest renumber
  else if (picks.length >= MAX_PICKS) return;           // full: the tiles are visibly dimmed
  else picks.push(id);
  ownIt(); buildPicker(); actionbar(); render();
});
$('#qs').addEventListener('input', (e) => {
  if (e.target.type !== 'range') return;
  const id = e.target.id.slice(2), q = Q.find((x) => x.id === id);
  state[id] = +e.target.value; $('#o-'+id).textContent = q.fmt(+e.target.value);
  ownIt(); render();
});
$('#qs').addEventListener('click', (e) => {
  // the +/- steppers: sliders were drag-only, which a touch user (or anyone on a
  // phone) could not operate. these let you tap to set the value.
  const st = e.target.closest('.step');
  if (st) {
    const id = st.dataset.step, q = Q.find((x) => x.id === id);
    state[id] = clamp(state[id] + (+st.dataset.dir) * (q.nudge || q.step), q.min, q.max);
    ownIt();
    const inp = $('#r-' + id), out = $('#o-' + id);
    if (inp) inp.value = state[id];
    if (out) out.textContent = q.fmt(state[id]);
    render();
    return;
  }
  const o = e.target.closest('.opt');
  if (o) {
    ownIt();
    state[o.dataset.q] = o.dataset.v;
    o.closest('.opts').querySelectorAll('.opt').forEach((b) => b.setAttribute('aria-pressed', b === o));
    render();
  }
});
document.addEventListener('click', (e) => {
  const ch = e.target.closest('.ca-ch');
  if (ch) { askIdx = +ch.dataset.goq; goTo('ask'); return; }
  if (e.target.closest('#sharecard')) { shareCard(); return; }
  if (e.target.closest('#vagain')) { startOver(); return; }
  if (e.target.closest('#showall')) { showAll = !showAll; render(); return; }
  if (e.target.closest('#clearsearch')) { query = ''; const s = $('#search'); if (s) s.value = ''; render(); }
});

// "find a place" search. On a phone, jump to the List so results are visible.
$('#search').addEventListener('input', (e) => {
  query = e.target.value.trim();
  if (query && exView !== 'list') {   // a search you cannot see the results of is a dead end
    exView = 'list';
    $('#vswitch').querySelectorAll('button').forEach((x) =>
      x.setAttribute('aria-pressed', x.dataset.view === 'list'));
  }
  render();
});
$('#tbody').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-i]'); if (!b) return;
  const r = ranked[+b.dataset.i], key = r.p.name + r.p.prov;
  selected = selected === key ? null : key; render();
});
function startOver() {
  Q.forEach((q) => { state[q.id] = q.def; });
  picks = []; askIdx = 0; selected = null; query = '';
  history.replaceState(null, '', location.pathname);
  goTo('pick');
}
document.addEventListener('click', async (e) => {
  const b = e.target.closest('#share'); if (!b) return;
  const top = ranked.find((r) => !r.excluded);
  const mine = picks.length
    ? ` I ranked ${listify(picks.slice(0, 3).map((id) => SHORT[id]))} and got ${Math.round(top.fit)} out of 100.`
    : '';
  const text = top
    ? `Apparently I belong in ${top.p.name}, ${top.p.prov}.${mine} Where do you belong?`
    : 'Where do you belong in Canada?';
  try {
    if (navigator.share) { await navigator.share({ title: 'Where U Belong', text, url: location.href }); return; }
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

// touch: tap the nearest dot to a finger and open its record. The map was
// mouse-only, so a phone could not read or select a place.
function pickAt(clientX, clientY, slop) {
  const b = cvs.getBoundingClientRect(), mx = clientX - b.left, my = clientY - b.top;
  let best = null, bd = 1e9;
  for (const q of pts) { const d = Math.hypot(q.x - mx, q.y - my); if (d < q.r + slop && d < bd) { bd = d; best = q; } }
  return best;
}
cvs.addEventListener('touchend', (e) => {
  const t = e.changedTouches && e.changedTouches[0]; if (!t) return;
  const hit = pickAt(t.clientX, t.clientY, 14);   // fat-finger slop
  if (hit) { e.preventDefault(); openSheet(hit.rec); }
}, { passive: false });

cvs.addEventListener('click', () => {
  if (hot < 0) return;
  const r = ranked[hot];
  if (MOBILE.matches) { openSheet(r); return; }
  const key = r.p.name + r.p.prov;
  selected = selected === key ? null : key; render();
  const el = $(`button[data-i="${ranked.indexOf(r)}"]`);
  if (el) el.scrollIntoView({ block: 'center', behavior: 'smooth' });
});

let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(render, 120); });

const ORIG_LEDE = ($('#lede') || {}).innerHTML;   // captured before the shared override, restored on edit
if (shared) $('#lede').innerHTML = `Someone sent you their answers, so this is <b>their</b> result.
  Change anything and it becomes yours.`;

/* a shared link lands straight on the sender's result, which is the whole point
   of sharing one. Everyone else starts at the picker. */
buildPicker();
if (shared && picks.length) { screen = 'result'; root.dataset.screen = 'result'; }
actionbar();
draw();          // first paint is synchronous: never depend on a frame that may not come
