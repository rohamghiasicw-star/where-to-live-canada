# Design references: data tools that don't look like dashboards

Research for **Where To Live / Canada**. Question behind it: what does web design look like when it unmistakably reads as human-designed, and how does that apply to a tool made of numbers?

**Method.** ~60 real pages opened. `WebFetch` converts pages to markdown and strips CSS, so every hex and typeface below was pulled by `curl`-ing the live site and its linked stylesheets, or by reading the foundry's own package source. Tabular-figure claims were verified by downloading font binaries and reading their GSUB feature tables with `fontTools`. Nothing here is from memory.

- **[V]** = read out of live CSS / package source / font binary, by me or a research agent
- **[V-me]** = I independently re-verified it myself
- **[I]** = inferred, reasoning shown
- **[U]** = unverified, flagged rather than guessed

Corrections made to agent output during verification are noted inline. Two subagent claims were wrong and are corrected below rather than passed through.

---

## 0. The verdict on what's already built

The tool already runs a National Topographic System sheet metaphor: `.collar`, `.plate`, `.legend`, `.sheet`, sections named *The survey / The field / The index*, and a palette the CSS header says is taken from real NTS sheets. **That instinct is right and most of this research supports it.** The idiom is not the problem. Four concrete execution bugs are.

### Bug 1 — the palette has semantic collisions [V-me]

Map inks and score colours occupy the same hues. Measured RGB euclidean distance, light theme:

| Map ink | Score colour | Distance | Verdict |
|---|---|---|---|
| `--survey #B33A1E` | `--bad #A33A22` | **16.5** | effectively the same red, two unrelated jobs |
| `--relief #6E7D52` | `--ok #4F7A3C` | **38.1** | collision |
| `--contour #8A5A33` | `--warn #A8761C` | **47.0** | collision |
| `--contour #8A5A33` | `--bad #A33A22` | **44.0** | collision |

Anything under ~60 reads as the same colour. So "this place scores badly" is painted in the same red as a survey mark, and "good fit" in the same green as terrain.

Tom Patterson (shadedrelief.com) [V] names exactly this failure: readers *"often mistakenly interpret hypsometric tints as natural vegetation or land cover."* Map colour carries semantic load whether or not you intend it. Right now the map's vocabulary and the score's vocabulary are fighting.

**Fix:** the map gets earth inks. The score gets a hue that appears nowhere on the map. They must not be neighbours.

### Bug 1b — the palette can *label* but not *encode* [V]

The deepest issue, and it isn't any single hex. **Nine flat named colours and no ramp.**

A survey sheet's defining colour move is an **ordered sequence where colour carries a quantity** — the hypsometric ramp — plus a small set of categorical inks around it. The build has borrowed the **categorical half** (the inks: contour, water, relief, survey) and **skipped the quantitative half** entirely.

129 cities are ranked on a score. That's a quantity. **There is no ramp for it.**

This is the deepest costume tell in the palette — deeper than any individual value — because it means the palette currently *cannot encode anything, only label*. The one thing a topographic sheet is famous for, colour carrying magnitude, is the one thing missing.

### Bug 1c — the greens are the wrong green, and the black is green [V-me]

**Every real cartographic lowland green is a teal. `--relief` is an olive.** Verified against Patterson & Jenny's cross-blended hypsometric tints (*Cartographic Perspectives* 69, doi:10.14714/CP69.20), measured channel by channel:

| Colour | RGB | B − R |
|---|---|---|
| Patterson warm_humid 0m `#72A48D` | (114,164,141) | **+27** |
| Patterson warm_humid 200m `#86B89F` | (134,184,159) | **+25** |
| Patterson cold_humid 0m `#789F98` | (120,159,152) | **+32** |
| Patterson cold_humid 200m `#91B1AB` | (145,177,171) | **+26** |
| **`--relief #6E7D52`** | **(110,125,82)** | **−28 ← opposite direction** |

Every Patterson green is blue-shifted by +25 to +32. `--relief` is yellow-shifted by −28. This isn't arbitrary: per Imhof via Patterson & Jenny, hypsometric sequences imitate **aerial perspective** — atmosphere between eye and ground scatters blue *in*. The tradition's greens are teal because they're **physically modelled**, not picked. An olive green is army surplus and 1970s field manuals — it reads *military map*, which is a costume genre. `#6E7D52` is the most costume-coded value in the palette.

**And a token named `relief` that is green reproduces the exact error Patterson wrote the paper to fix.** Their thesis: green misleads because readers read it as vegetation ("people misread elevation colors as climate or vegetation information" — their canonical case is dark-green lowlands implying lush vegetation in the Persian Gulf). Both national systems agree categorically: **green = woodland, scrub, orchards, vineyards** (USGS *and* NRCan) [V]. In this idiom green means *plants*. It has never meant elevation.

**In a tool that ranks places partly on climate, a green will be read as "verdant / temperate / pleasant."** That's a live misreading, in the actual subject matter, of precisely the type the literature documents.

**The uniform cast [V-me]:** 6 of 9 tokens are green-dominant — `paper`, `sheet`, `ink`, `rule`, `land`, `relief`. **`--ink #14180F` is (20,24,15): G > R. The black is green.** Real cartographic palettes are *not* uniformly cast — Patterson's arid lowland `#A0988D` is a warm grey, his polar `#95A9C4` a cold blue, his summit `#F5F5F5` neutral. **The hues diverge because they mean different things.** A single hue rotation applied across an entire palette is a photo filter — the visual equivalent of the paper-texture overlay, applied *over* the system rather than derived *from* it.

Related [V-me]: `paper #E7E9E1`, `sheet #F2F3EE` and `land #DCE0D2` are within ~20 RGB units of each other — three indistinguishable sage greys. *(Agent said four including `rule`; `rule` measures 63.8 from `paper` and is adequately separated. Using my number.)* If three of nine swatches can't be told apart in a legend, the legend can't do its job — which is the whole contract.

**Verified Patterson values, if a ramp gets built** (from tidyterra `data-raw`, encoding Patterson & Jenny 2011). Shared highland ramp — all three non-polar palettes converge above 1000m, and *the convergence is itself the design*:
```
#D4C9B4 (1000m) → #D4B8A3 (2000) → #D4C1B3 (3000) → #D4CFCC (4000)
→ #DCDCDC (5000) → #EBEBED (6000) → #F5F5F5 (7000)
```
Lowlands by environment:

| Elev | arid | warm_humid | cold_humid | polar |
|---|---|---|---|---|
| 0m | `#A0988D` | `#72A48D` | `#789F98` | `#95A9C4` |
| 50 | `#AAA096` | `#78AC95` | `#82A59F` | `#A4B4CB` |
| 200 | `#B4AA9E` | `#86B89F` | `#91B1AB` | `#ABC0D5` |
| 600 | `#CABEAE` | `#A9C0A6` | `#B4C0B4` | `#B9C9E0` |

> **Correction caught in research:** the raw file renders arid/600m as `#CABEBE`, but its own RGB triple (202,190,174) → **`#CABEAE`**, which tidyterra's docs independently confirm. Use `#CABEAE`. Flagged because it's exactly the kind of error that propagates silently.

**Steal the structure, not the values** (his encode elevation, not fitness): monotone lightness, converging to near-neutral `#F5F5F5` at the top.

**What's right and should stay:** `contour #8A5A33` (brown = hypsography ✓ — but **line-only**; at (138,90,51) it's far darker/more saturated than any Patterson terrain value, so as an area fill it reads chocolate). `water #2F6B87` (blue = hydrography ✓). `ink` (black = cultural ✓ — de-green it). `survey #B33A1E` — correct by convention, but see Bug 1: red will be read as *hazard* on a page shipping wildfire smoke.

### Bug 2 — `tabular-nums` is a no-op [V-me]

Verified against the actual bundled binaries in `fonts/faces.css`, decoded from base64 and inspected with `fontTools`:

| Bundled font | GSUB/GPOS features | `tnum`? |
|---|---|---|
| IBM Plex Sans 400 | `ccmp, dnom, frac, kern, liga, mark, numr` | **no** |
| IBM Plex Mono 400 | `ccmp, dnom, frac, mark, numr` | **no** |
| IBM Plex Mono 500 | `ccmp, dnom, frac, mark, numr` | **no** |
| League Gothic 400 | `ccmp, kern, liga, locl, mark, mkmk` | **no** |

`font-variant-numeric: tabular-nums` appears 3× in `style.css` and does nothing. It currently *works by accident* because those selectors use Plex Mono, which is fixed-width by construction. Apply it to Plex Sans and it silently fails.

Cause is likely `src/get_fonts.py`: it pulls the `latin` subset from Google Fonts, and the subsets are stripped (270–280 glyphs). Either re-subset from source with `--layout-features+=tnum`, or pick a face with verified `tnum` (list in §4).

**League Gothic has no numeric features at all and 237 glyphs.** For a display face carrying big numbers, that's worth knowing.

### Bug 3 — the type scale is accreted, not designed [V-me]

**20 distinct font sizes**, including *seven* crammed between 0.72 and 0.82rem: `0.72, 0.74, 0.76, 0.78, 0.79, 0.80, 0.82`. Those are not perceptually distinguishable. Nobody chose them; they accumulated.

Compare, all verified from live CSS:

| Site | Type sizes | Weights |
|---|---|---|
| **The Pudding** [V-me] | **5** (`giant/large/medium/small/xsmall`, all `clamp()`) | **3** — 100/400/900, *no 500/600* |
| **Low-Tech Magazine** [V-me] | **6** (0.7 / 0.85 / 1 / 1.4 / 2 / 2.5rem) | system mono only |
| **Washington Post** [U, write-up] | 1 face, **2 weights**, for every chart | 2 |
| **Colophon Foundry** [V] | fluid `clamp()`, body floor **20px** | **1 weight, whole site** |
| **Where To Live / Canada** | **20** | 400/500 |

This single metric is the most reliable template tell in the entire research set.

### Bug 4 — synthetic bold [V-me]

Only **IBM Plex Sans 400** is bundled. But `.v-catch b` sets `font-weight: 500` and inherits the body font (it declares no `font-family`). Plex Sans 500 doesn't exist in the bundle, so the browser fakes it by smearing the 400 outlines. `.q-label` at `font-size: 0.9rem; font-weight: 500` has the same problem.

`.v-facts b` and `.stat b` are fine — they're `--f-mono`, and Plex Mono 500 *is* bundled.

Synthetic bold is a thing no typographer ships on purpose.

---

## 1. The six strongest references

### 1. Financial Times — `#FFF1E5` and a palette named after things
**URL:** ft.com · palette source: `unpkg.com/@financial-times/o-colors@6.7.1/src/scss/_palette.scss`
**What it is:** a global financial paper whose entire digital product sits on newsprint pink.

**Palette [V-me, from FT's own package]:**
```
paper   #FFF1E5    ft-pink #FCD0B1    ft-grey #333333   slate   #262A33
claret  #990F3D    oxford  #0F5499    teal    #0D7680   wheat   #F2DFCE
mandarin #FF8833   jade    #00994D    velvet  #593380   wasabi  #96CC28
candy   #FF7FAA    lemon   #FFEC1A    crimson #CC0000   matisse #355778
mint    #C0EFD8    sky     #CCE6FF    light-blue #00A0DD
graphics-dark-blue #006F9B
```
**Type [V]:** MetricWeb (Klim) for UI; Financier for editorial [U, write-up-sourced].

**Why it's human:**
1. **The substrate is not white.** `--o-colors-page-background: #FFF1E5`. A newspaper decided its *screen* should be the colour of its *paper*. FT graphics are identifiable from a thumbnail with the logo cropped off.
2. **The colours are named after things** — `claret`, `wasabi`, `velvet`, `mandarin`, `matisse`, `wheat`, `jade`. Not `primary-500`. **This is the clearest human/machine tell found anywhere in this research.** `primary-500` permits any value; `wasabi` doesn't. A team that argues about whether a green is wasabi or jade will not ship a generic dashboard.
3. **`graphics-dark-blue #006F9B` is a separate token from `oxford #0F5499`** [V-me]. The graphics desk got its own blue because the brand blue didn't survive charts. That's an institution respecting a craft constraint — and it's the single most relevant detail here, because it's the answer to "how do I have a brand palette AND readable data?"

**Contrast [V-me]:** ink on paper 15.72:1. claret 7.62:1 (AAA). oxford 6.90:1 (AA).

**Steal:** the layer separation. Brand ground and data encoding are **different layers with different tokens**, and FT proves you can have a wildly distinctive substrate *and* rigorous data by refusing to make one colour do both jobs. Also: rename the palette after real Canadian things — `cedar`, `chinook`, `smoke`, `saskatoon`, `tarmac`, `slate`. The names will drive the design.

---

### 2. Whole Earth Index — the proof of convincing vs costume
**URL:** wholeearth.info · archive of Whole Earth publications 1968–2002.

**Palette [V]:** `--background: #000`, `--text: #fff`, secondary `#9CA3AF`.
**Type [V]:** `Whole Earth Modern`, `Whole Earth Mono`, `MLMRomanUnsl10`. File names: `WEMLMRoman8-Regular.woff2`, `WEMLMMono10-Regular.woff2`.
**[I], strongly supported:** `WE` + `LMRoman8`/`LMMono10` = **Latin Modern** (Knuth/Computer Modern TeX lineage), rebranded. The load-bearing detail is the **optical sizes** — Roman **8**, Mono **10** — size-specific cuts rather than one scaled master. That's a metal-type constraint, reproduced on purpose.

**Why it matters more than anything else here:** the most faithful archive of the most famous paper catalogue in counterculture history **has a pure black background**. No newsprint beige. No paper grain. No page curl. The scans carry the paper; the chrome gets out of the way.

It borrows the *access structure* — numbered sections ①–⑥, dense enumeration, tools-first ordering — and the *typesetting logic* (optical sizes). It refuses every surface cue.

**Steal:** this is the licence to stop decorating the survey sheet and start obeying it.

---

### 3. NYT "You Draw It" — the mechanic
**URL:** nytimes.com/interactive/2015/05/28/upshot/you-draw-it-how-family-income-affects-childrens-college-chances.html

**Type [V]:** `nyt-franklin`, the whole interactive in one face.
**Palette [V]:**
```
#9E4B6C  your line, your label, submit button, best-fit stroke
#AAAAAA  the actual truth
#FFFFCC  instruction callout (legal-pad yellow)
#F2E277 @ 5%  the region you haven't drawn yet
#DEDEDE  tooltip border
```

**Why it's human — three moves, all in the CSS:**
1. **Your guess is the hero colour; reality is grey.** `.g-your-label { color: #9E4B6C }` vs `.g-real-label { color: #AAA }`. The colour isn't encoding a *category*, it's encoding *whose it is*. It makes being wrong feel like a discovery rather than a scolding.
2. **Your line is fat and round-capped** — `stroke-width: 7px; stroke-linecap: round` vs the truth's `3px`. Your line is more than double the data's weight. No chart library defaults to that.
3. **The callout is built from CSS borders** — `#FFFFCC` with a border-triangle arrow. A hand-drawn speech bubble made of `border-width: 20px`.

**The mechanic:** *"We'd like you to draw your guess… before the data loads."* You must commit to a belief before it will show you anything. The result lands as **correction**, which is memorable, instead of **information**, which isn't.

**Steal — the biggest single idea for this tool.** Before revealing the ranking: *"Where do you think Kelowna lands on cost?"* They drag. Their guess renders at 7px in the accent; reality snaps in at 3px grey. Converts a leaderboard into an experience for the price of one SVG line.

---

### 4. The Pudding — personality as tokens
**URL:** pudding.cool

**Type [V-me]:** four families, all licensed, zero system fonts — **Atlas Grotesk** + **Atlas Typewriter** (Commercial Type), **Tiempos Text** (Klim), **Gooper SemiCondensed** (Ohno Type Co).
**Palette [V-me]:** `--color-blue #4717F6`, `--color-electric-green #3AE660` (also `--color-focus`), `--color-purple #A239CA`, `--color-red #FF533D`, `--color-yellow #E5E338`, 11-step grey ramp.

**Why it's human [all V-me]:**
1. **Imperfection is a token.** `--left-tilt: -2deg; --right-tilt: 2deg; --left-tilt-double: -4deg; --right-tilt-double: 4deg` — consumed by **12 rules**. *(Agent said 16; I measured 12. Using mine.)* They didn't sprinkle randomness, they built a system for wonkiness. **Random reads as broken; systematic imperfection reads as hand-made.**
2. **5 sizes, 3 weights** — 100/400/900, no 500/600 mush. `--border-radius: 3px`, not 12.
3. **`--font-form: var(--mono)`** — every input, filter and button is typewriter.
4. **Every story tile carries its own `--story-bg`** — the homepage is a quilt of ~223 unrelated colours, not one brand hue.

**On their menu piece** (pudding.cool/2026/06/menu-story/) [V], the best single detail in this research — the byline:
```css
border-top:    1px solid rgba(252,252,252,.32);
border-right:  1px solid rgba(252,252,252,.32);
border-left:   1px solid #dddbd5;
border-bottom: 1px solid #e5dec8;
filter: drop-shadow(0px -1px 6px rgba(0,0,0,.05));
transform: rotate(-.2deg);
```
**Four different border colours, one per side**, an *upward* shadow, and a `-0.2deg` tilt — below conscious perception. Someone simulated a slip of aged paper lying on a table. No template and no default produces per-side border colours.

That piece also **overrides its own sans slot with EB Garamond**, so the page has no sans-serif at all. Discipline everywhere + one indefensible choice = voice.

**Steal:** a `--tilt` token on city cards. Per-city `--city-bg`. Mono for every control. 5 sizes / 3 weights. 3px radius. And their process doc is explicit that they prescribe **no house visual rules** — each piece is designed to its argument. The absence of a style guide is the point.

---

### 5. Low-Tech Magazine (solar) — the data *is* the design constraint
**URL:** solar.lowtechmagazine.com · solar-powered site that shows its own live battery and weather.

**Palette [V-me]:**
```
--color-bg    #FFF5D1   (warm paper yellow)
--color-primary black
--color-high  #D11305
--color-low   #162DAB
--color-obs   #006951
--color-sky   #F0F8FF
--color-sub   rgb(130 130 130)
```
**Type [V-me]:** `--monospace: monospace`. The entire site runs the system mono stack. **Zero webfonts, by principle.**

**Why it's human:** the colours are named `--color-high` / `--color-low` / `--color-obs` — **semantic to the data, not to the brand**. Images are hand-dithered to save bytes, and the dithering becomes the house style. A persistent battery meter says "this is a real instrument." Type scale is a blunt 6-step ramp.

**Steal:** name palette vars after what the data *means*. Warm paper `#FFF5D1` over white. A persistent data-freshness meter in the collar — the "this is a live instrument" tell, and you have the material for it (ECCC normals 1981-2010, FireWork 2013-2024, StatCan 2021, Elections Canada 2025).

---

### 6. Nomads.com / Numbeo — the anti-reference, with receipts
**URLs:** nomads.com (formerly nomadlist.com), numbeo.com/quality-of-life/rankings.jsp

This is the closest prior art to what's being built, and it's a warning. Counted from the DOM [V]:

| Tell | Evidence |
|---|---|
| Everything at once | **560** × `class="choice"`, **173** filters, 34 filter-group labels — all rendered simultaneously |
| Attribute explosion | `Humidity January`…`Humidity December`, `Air quality (now)` vs `(annual avg)` |
| Opaque composite | "Nomad score" — one number, no shown weighting |
| **No typographic decision** | `font-family: -apple-system, SF UI Text, Helvetica Neue, Helvetica, Arial, sans-serif` [V-me] |
| Emoji as design system | **417** × `emoji_flag`; nav is `🌍 🌗 ❤️ 🚑 💬 🎒 📸 🗓 💸 🌤 🔌 🌴 💥 📊 🧪 📜 🕸 🏆` |

**The tells, generalized:**
1. **No question is ever asked.** You get 173 filters and are told to become your own analyst. Preference elicitation is offloaded onto the user as labour.
2. **The composite has no visible arithmetic.**
3. **Ranking is a leaderboard, not an argument** — nothing falsifiable, nothing memorable.
4. **System fonts + emoji = no decision was made.** The cleanest single diagnostic.
5. **All metrics weigh the same visually.** A dashboard flattens; an editor ranks.
6. **You cannot disagree with it.**

**Worth knowing:** **Teleport** (teleport.org) — preference-based city matching, genuinely the closest prior art — is **dead**. DNS resolves to a parking IP, zero content. Acquired by MOVE Guides, merged into Topia. *The best-designed competitor in this exact space no longer exists.*

---

## 2. Q1 — What genuinely well-designed data tools and quizzes do differently

Beyond You Draw It and the Pudding above:

**NYT Dialect Quiz** (nytimes.com/interactive/2014/upshot/dialect-quiz-map.html) [V] — NYT's most-viewed content ever. Type: `nyt-franklin`/`nyt-imperial`/`nyt-cheltenham`. Heat scale is ColorBrewer **RdYlBu-11**: `#313695 #4575B4 #74ADD1 #ABD9E9 #FFFFBF #FEE090 #FDAE61 #F46D43 #D73027 #A50026`.
- 25 questions, **one at a time**.
- **The map redraws after every single answer** — a persistent `"Your last answer"` label sits beside `Least similar`/`Most similar`. No submit-and-reveal cliff; the result *tightens*.
- **Uncertainty in one plain sentence:** the colours are the probability a random person there would answer a random question the way you did. No confidence-interval theatre.
- **It lets you argue:** `Show least similar` inverts the entire result. It shows *your most distinctive answer for each city* — per-item evidence, so you can reject the verdict on the merits.
- Opening line is a question about **you**, not about the dataset.

**GOV.UK Design System** (design-system.service.gov.uk) [V] — Type: `GDS Transport`, **two weights only**. Palette: `#0B0C0C` text (near-black, not `#000`), `#FFDD00` focus yellow, `#1D70B8` link, `#0F7A52` green, `#CA3535` red.
- **One question per page.** The canonical GDS rule.

**Our World in Data** (ourworldindata.org) [V] — honest verdict: **closer to the anti-reference**. Lato + navy (`#1D3D63` ×228, `#002147`) is institutional default. Its credibility is rigour, not voice. **What to steal isn't the look — it's that every chart is one click from its provenance** ("Sources", "Learn more about this data").

**Datawrapper** (datawrapper.de) [V] — Roboto + Roboto Mono. But `#FFF8F2` warm off-white page. Competent, not distinctive.

### The synthesis

| | Dashboard | Designed tool |
|---|---|---|
| Pacing | 173 filters at once | one question at a time |
| Reveal | submit → cliff | redraws after every answer |
| Stance | hands you data | makes you commit first |
| Voice | none | admits its own failures in-product |
| Uncertainty | error bars or nothing | one plain sentence |
| Disagreement | impossible | `Show least similar` + per-item evidence |
| Type | `-apple-system` | someone bought a typeface |

The voice point deserves emphasis. The Pudding's wine piece [V] contains the line that ChatGPT was particularly bad with elephants — **admitting method error inside the tool**. That buys more trust than any methodology footnote. This tool already has the raw material for exactly that move, and it's currently buried in the README: the smoke-data reversal (ECCC's "days with smoke or haze" correlates *negatively* with real smoke, Pearson −0.22), Revelstoke's station being 1,431m too high, Kenora geocoding to Kenora District, StatCan shipping latin-1 so `Montréal` silently becomes `montral`. **Those stories are the personality. They belong in the interface, not the repo.**

---

## 3. Q2 — Where personality comes from when the content is numbers

Ranked by leverage, from reading the CSS of every site above. **Illustration is last.**

**1. Refuse the default substrate.** Nearly free, highest impact. **Not one respected piece opened in this research used `#FFFFFF` as its page background:**

| Site | Background [V] |
|---|---|
| FT | `#FFF1E5` |
| Pudding menu story | `#FFFEF5` |
| Low-Tech Magazine | `#FFF5D1` |
| Future Fonts | `#EDEDEA` (109 uses) |
| Beckmans | `#EDEDED` — and `--white` is *redefined* as `#EDEDED` |
| Are.na | `#F5F1F0` |
| COLLINS | `#F8F8F7` [single-source, see §6] |
| Anthropic | `#F0EEE6` |

And never pure black. Dinamo `#242423` (39 uses). Pudding's similes piece: `--color-adjusted-black: #1A1D21` on `--color-adjusted-white: #E6E6E7`. Displaay ships *tinted* blacks — `#002323` teal-black, `#410042` aubergine-black. GOV.UK `#0B0C0C`.

*Current state: `--sheet: #F2F3EE` and `--ink: #14180F` already pass this test. This one's done.*

**2. Naming.** FT: `claret`, `wasabi`, `velvet`, `matisse`. Low-Tech: `--color-high`, `--color-low`, `--color-obs`. HFBK: `--fontColorDeselected`. COLLINS: `--color-brian-orange` — **named after a person**, a token that could not survive a design-system committee. Templates name colours `primary`. **Personality is upstream of pixels; it lives in the vocabulary.**

*Current state: `--contour`, `--water`, `--relief`, `--survey`, `--land-edge` already do this. Also done — which is why the collisions in §0 are worth fixing rather than abandoning.*

**3. Systematized imperfection.** Pudding's tilt tokens across 12 rules; the `-0.2deg` byline. Systematic, not sprinkled.

**4. Emotional colour assignment, not categorical.** You Draw It: your line `#9E4B6C`, the truth `#AAA`. Ask of every colour: *what does this make the reader feel about themselves?*

**5. Type restraint, then one violation.** Pudding: 5 sizes / 3 weights, then sets its sans slot to EB Garamond. WaPo: one face, two weights, every chart. Colophon: **one weight, whole site** — hierarchy from size and colour alone. Discipline alone = template. Discipline + one indefensible choice = voice.

**6. Material simulation.** Per-side border colours. Happy map's `--crosshatch: rgba(40,60,70,.1)`. NYT's `text-shadow: 1px 1px 0 black`. Making pixels behave like paper and ink.

**7. Weight as emotion.** 7px round-cap for your guess vs 3px for truth.

**Motion is last.** Pudding's motion is `transition: transform .25s` on a tilt. That's it.

**Two structural principles**, from Lena Groeger / Amanda Cox at Source (source.opennews.org/articles/design-principles-news-apps-graphics/) [V]:
- **The annotation layer** (Cox): put text *as close as possible to the relevant part* of the visual, never in a separate list. Annotations sit **on** the mark, not in a legend.
- **Scale** (Groeger): always show both the **far** (where this sits nationally) and the **near** (what your street feels like in August). That's a direct spec for a city page.

---

## 4. Q3 — Print reference: convincing vs costume

### The examples

| Work | URL | Print form borrowed | Constraint it *kept* |
|---|---|---|---|
| **Whole Earth Index** | wholeearth.info | catalogue index | optical sizes per point size; numbered sections ①–⑥ — on a `#000` background |
| **Feltron Annual Reports** | feltron.com (HTTP only; HTTPS fails) | the corporate annual report | a year is a **closed accounting period**, so the data must be *complete*, with prior-year comparatives |
| **Dear Data** | dear-data.com | correspondence postcard | one postcard = one week = a hard cap on data; hand-drawn legend on every reverse |
| **Are.na** | are.na | library card catalogue | an item is **filed, not fed** — no algorithmic sort, no feed |
| **Cooper Hewitt** | collection.cooperhewitt.org | museum accession catalogue | persistent ID + fixed field set; ships a real `print.css` |
| **Robin Sloan** | robinsloan.com | book typography | Filosofia (Licko's Bodoni revival, Emigre) — a *book* face on a screen, zero paper imagery |

**Feltron detail [V-me]:** the 2013 report was set entirely in **Input** (David Jonathan Ross) — a family designed *for code and data*. Felton wanted, in his words, a "bureaucratic document" rather than a "sexy typographic exercise," and something monospace-ish he could still get texture from. **⚠️ Licensing:** Input is free *only for private use in code editors*. A public web app needs a paid licence ($40–200+ tier).
The 2005 report was **Garage Gothic** (Frere-Jones) — a condensed gothic, the same family of forms as League Gothic. 2014: 7 offset colours incl. fluorescent + metallic, foil-stamped cover.

**The Dear Data finding is the most instructive [V]:** the dear-data.com website is a **stock Squarespace theme** (proxima-nova, europa, brandon-grotesque). So is Giorgia Lupi's own site. **The most celebrated print-native data work of the last 15 years sits on a template** — because the print quality lives entirely in the artifact, not the chrome. The postal constraint *is* the design system.

### What separates convincing from costume

The hypothesis ("structure vs surface") gets the right answer by the wrong mechanism, and the wrong mechanism will cost you. Two refinements from the evidence.

**First, the base rule holds:**

> **Convincing work borrows a print form's *constraints* — the parts that were annoying — and keeps them even though digital has abolished them. Costume borrows the parts that were pleasant side effects of those constraints.**

Whole Earth Index — an archive of a *paper catalogue* — has a **`#000` background** and pays to serve optical-size-specific cuts. It kept the hard part and threw away the signifier. The costume version has `#F4ECD8`, a paper-grain PNG, and Georgia.

**⚠️ Correction — "texture = costume" is false.** Stamen **Watercolor** (stamen.com/watercolor-process-3dd5135861fe/) [V] is the most ornamental map style of the modern era — literal paper, literal pigment — and it's respected by exactly the cartographers who'd sneer at a compass rose. Because the texture isn't an overlay: it's **computed from the geometry**. Masks are cut from rendered OSM data, water subtracted, Gaussian blur + Perlin noise produce a "fuzzier, wobblier outline," and edge darkening is derived by differencing a blurred mask against the original — mimicking how watercolour deposits more pigment at the edges as it dries. The dark rim around a lake is dark **because that lake's actual polygon is there.** The process is entirely deterministic: same data, same paper.

So state the rule correctly:

> **A graphical move is convincing when it is a function of the data, and costume when it is a layer over the data.**

A tiled paper-texture PNG is costume — identical whether you have 129 cities or zero. A grain whose density varies with how much evidence backs a row is not costume at all; **it's a legend entry.**

**Second, the sharpest single test** — and it's hiding in the collar. A **compass rose** on a north-up page declares an orientation that never varies: information content zero. A **magnetic declination diagram** looks like its cousin but is pure data. From the USGS margins spec [V]: it gives the direction to magnetic north *"at the date given, in this case 1994,"* because *"the magnetic pole, and thus the magnetic declination, change over time."* An angle, measured at a point, stamped with an epoch, **because it decays.** Same visual family. One is a badge; the other is a measurement with a shelf life.

> **The test for every mark on the page: could its value have come out different? If no, it's costume.**

Kenneth Field's third principle is the guillotine [V]: *"It's not what you put in that makes a great map but what you take out."*

**Third — honesty sometimes means *less* precision.** Daniel Huffman argues for **"salutary ambiguity"** [V]: when a thing has no crisp edge, an approximately-placed label is the *truthful* rendering and a polygon is the lie. He names "false precision through polygons" as the failure mode. Directly relevant to 101 places with no resident research.

**The remaining test:**
1. **Does it hurt?** A borrowed constraint that costs nothing is decoration. Felton's completeness obligation costs. Dear Data's card size costs. Paper texture costs nothing.
2. **Would the form's original practitioner recognize the *logic*, or only the *look*?** A catalogue editor would recognize Are.na's filing model. They'd learn nothing from a page-curl.

**Applied to the NTS sheet.** The survey sheet's real logic is **the information contract**: every mark is declared in the legend, the collar states provenance and revision date, the scale is shown honestly, symbols are consistent, and *the sheet does not omit a town for being boring*. That is the opposite of Nomad List's 173 optional filters — and this tool already has the material for the whole contract:

| Collar convention | The data already there |
|---|---|
| Sheet ID + revision date | ECCC normals **1981-2010**; FireWork **2013-2024**; StatCan **2021**; Elections Canada **April 2025** |
| Projection statement | **EPSG:3347**, Statistics Canada Lambert — already the real projection |
| Scale bar / accuracy | station distance + elevation offset **per place** (Revelstoke 4km vs Mount Fidelity's 43km/1,431m) |
| Reliability diagram | **28 of 129** places have resident research; 9 use computed normals with year counts |
| Legend | every mark declared — which is exactly what the §0 palette collisions currently violate |

An almanac's logic is a **fixed field set**: every town gets the same entries in the same order, *including the unflattering ones*, and the almanac never drops a town. Missing is printed as missing — which `README` already commits to ("Missing is not the same as mediocre"). **That's the structural borrow. It's already half-built. Finish it in the collar and stop there — no paper texture, no compass rose.**

### The finding that matters most: the sheet spends an ink plate on *epistemic status*

From the USGS symbol sheet, read directly [V]:

> Black — cultural features. Blue — hydrographic. Brown — hypsographic (contours). Green — woodland cover, scrub, orchards, vineyards. Red — important roads and the public land survey system.
> **Purple — features added from aerial photographs during map revision. The changes are not field checked.**

Five colours name *what a thing is*. **The sixth names how much you should trust it.** And NRCan independently reserves purple on Canadian NTS sheets for updates overlaid on original detail [V]. Two national agencies, no coordination, both spent one of six scarce ink plates — plates that cost real money per sheet — on **provenance**.

It goes further. USGS declares an entire **product tier** when the data is thin [V]: *provisional edition* maps "reflect a provisional rather than a finished appearance," and carry **fewer names and labels** than standard sheets. **The sheet looks less finished because it knows less.** It doesn't paper over the gap; it renders it.

And swisstopo — the most admired cartography on earth — leads with error, not beauty [V]: accuracy of "0.1 to 0.3 millimetres" of map space (2.5–7.5 m at 1:25,000), with control-point analysis confirming mean deviations of ~4.1 m. **The best map in the world publishes its own measured residual.**

**This is the answer to 28/129.** There is currently no visual class distinguishing a place with resident research from one without — they render identically. The idiom being borrowed solved this exact problem a century ago, with a colour. Note the polarity: purple marks the *better-informed* areas while flagging them unverified; the 28 are better-informed *and* verified. Either polarity works. What matters is that **the sheet never renders a researched place and an unresearched place the same way.**

And a place with no resident research and a 43km station is a **provisional sheet**: ship it, mark it provisional, show fewer labels on it. The reduced label count *is* the honesty signal, and it costs no apology copy.

### The collar conventions worth stealing, ranked

The USGS margins spec says the collar *"identifies and explains the map… corresponds somewhat to the table of contents and introduction of a book — it tells briefly how the map was made… what organizations are responsible."* The `.collar` / `.plate` split **is** the neatline. The nouns are right. The question is whether they do work.

**1. The credit legend — steal this first, verbatim in structure.** It isn't a flat source list. It separates **who published** / **who furnished the geodetic control** / **by what method** / **a separate credit note for hydrological information** / **explanatory notes**.

| Collar convention | The instance already in hand |
|---|---|
| Mapping agency | Where To Live / Canada |
| Agency furnishing control | ECCC (climate), StatCan 2021, Elections Canada 2025 |
| Method of compilation | FireWork RAQDPS-FW reanalysis 2013-2024; OSRM on OSM roads |
| **Credit note for hydrological info** | **the resident-quote corpus** — a *different kind* of evidence, credited separately, exactly as hydrography is |
| Explanatory notes | the honesty statements |

That fourth row is the gift: the credit legend already contains the precedent for "one of my data classes is qualitatively different and gets its own credit line." **Resident quotes are the hydrology.**

**2. The epoch stamp.** Declination is given "at the date given" *because it drifts*. Climate normals from **1981-2010** are, in 2026, a 16-year-old reference frame for a quantity known to be moving. State the epoch next to the value, always — not in a footnote. The sheet doesn't hide that its north is stale; it tells you which north, and when.

**3. The datum offset — for the 43km weather stations.** The best find in the research, and almost too on-the-nose [V]:

> North American Datum of 1927 (NAD27)… Note that NAD83 is also indicated on this map by **dashed crosses that are slightly offset** from each corner… **On some maps, the dashed crosses are absent, but the amount of offset is given in the text.**

When a topo sheet has two competing reference frames, it **draws both and shows the gap**. It does not silently pick one. **A weather station is not the city — it's a different reference frame for the same place.** The convention says render the offset: a tick at the city, a tick at the station, the distance stated. Revelstoke's own airport station at 4km vs Mount Fidelity at 43km/1,431m is exactly this. The source grants permission to draw it *or* state it in text — but not to omit it.

**4. Adjoining sheet names.** Real sheets name the neighbouring quadrangles in the collar. The most natural possible fit for a ranked-places tool, and it's a *real* collar element, not an invention.

**5. The contour interval statement.** The interval adapts to local relief — small in flat areas, larger in mountains, with *supplementary contours at less than the regular interval* where needed — **and the adaptation is declared in the margin**, positioned under the scale bar. If scores are binned, state the interval.

**6. Sheet name + reference code.** Every character of a real sheet code is a fact (lat, long, index, product type, scale). A place-ID scheme where each character means something is convincing; a decorative sheet number is costume.

**Do NOT take:** the north arrow (north-up; orientation isn't a variable). **The scale bar** — unless "distance" can be defined in score-space. Note the asymmetry: the scale bar is *mandatory* on a real sheet and *meaningless* here. That's the proof you must select on information content, not genre completeness.

---

## 5. Q4 — Palettes: the AI defaults, and real alternatives

### The anti-reference, with exact hexes [V-me, from Tailwind source]

```
indigo-500 #6366F1   violet-500 #8B5CF6   purple-500 #A855F7
indigo-600 #4F46E5   violet-600 #7C3AED   blue-500   #3B82F6
slate-500  #64748B   slate-900  #0F172A   gray-900   #111827
```
The "AI startup gradient" is almost always `#6366F1 → #8B5CF6` on `#0F172A`.
Bootstrap `$blue: #0D6EFD`. Material blue-500 `#2196F3`.

**Why they read as machine-chosen** — not because they're ugly, because they're *unchosen*:
1. **Zero-effort path.** `#6366F1` is what you get by typing `indigo-500`. It carries no decision, so it signals none.
2. **Perceptually uniform ramps have no accidents.** Real brand palettes have a weird one — slightly too dark or too green because someone *liked* it. Uniformity is the fingerprint.
3. **Hue clustering.** Every default lands in 220–280°. Even the "neutral" is blue: slate-900 `#0F172A` is measurably blue-tinted.
4. **Blue is the semantic null.** It means "software." It says nothing about climate, cost, or Canada.

The escape isn't "avoid monochrome + one accent" — Klim and Pentagram ship exactly that. It's *which* accent, and whether the neutral is **warm**.

### Real alternatives, all shipping, all verified

**A. FT Paper** — §1. The best of the set and it isn't close, because it solved this exact problem.

**B. Institutional monochrome + hot red** [V]
```
Klim:      #FFFFFF / #000000 / ramp #E2E2E2 #C6C6C6 #8D8D8D #717171 #383838 #1C1C1C
           accent --tertiaryColorRef: #E4001C   (one chromatic token in :root)
Pentagram: #1A1A1A / #E3E4E5 / #E61428
Order:     #141414 / #787878 / #FF3D00 / #FFC52F
```
Order's restraint, counted [V-me]: `#787878` ×25, `#141414` ×6, **`#FF3D00` ×4**. One accent, four uses. That's why it means something when it appears.
Contrast: Klim red 4.87:1 (AA); Order `#FF3D00` **3.55:1 — large/UI only, never body text**.

**C. Cartographic / ColorBrewer** (Cynthia Brewer, via `d3-scale-chromatic`) [V]
```
BrBG   #8C510A #D8B365 #F6E8C3 #C7EAE5 #5AB4AC #01665E
PuOr   #5E3C99 #B2ABD2 #F7F7F7 #FDB863 #E66101
YlOrBr #FFFFD4 #FED98E #FE9929 #D95F0E #993404
RdBu   #CA0020 #F4A582 #F7F7F7 #92C5DE #0571B0
```
The only family purpose-built for encoding, colourblind-safe by construction, and it reads as *atlas* — which is exactly what this tool is.

**D. Paul Tol categorical** [V, verified live in two separate Pudding pieces]
```
#4477AA #66CCEE #228833 #CCBB44 #EE6677 #AA3377 #BBBBBB
```
Colourblind-safe and doesn't read as Tailwind.

**E. Acid / hyper-digital** [V] — Grilli `#30FF00` on greys; Dinamo `#F8F135`/`#00C500`; Pudding `#4717F6`/`#3AE660`.
**Hard constraint:** `#30FF00` on `#242423` is 11.42:1 (AAA); on white it's **1.36:1 — catastrophic**. Acid is non-negotiably dark-ground. Rules it out for a light tool.

**F. Oxblood / warm archive** [V] — cosmos.so: `#F9F7F3` / `#A0213E` oxblood / `#BC361B` / `#9C6030` umber / `#EBB042` amber.
Oxblood 7.06:1 (AAA), burnt red 5.33:1 (AA), but `#EBB042` is **1.81:1 — fill only**.

### The rule the contrast math produced

**Every warm/earthy palette tested has an accent that fails as text:** `#D97757` 2.69:1, `#EBB042` 1.81:1, `#F58220` 2.59:1, `#FF3D00` 3.55:1. These palettes are **ground and fill, not ink.** Keep ink near-black and warm and the whole family passes AAA. Ignore it and you get a beautiful illegible tool.

### Data encoding for this specific tool

**Sequential (cost):** **YlOrBr** `#FFFFD4 → #993404`. It's the same hue family as an earth/paper ground, which is how brand and encoding become *one* decision instead of two fighting ones.

**Diverging (politics) — and the trap.** Red/blue is loaded, and **in Canada it's loaded backwards from the US**: Liberal is *red*, Conservative is *blue*. A US-trained reader inverts the entire map.

Verified party brand hexes [V]:

| Party | Hex | Source |
|---|---|---|
| Liberal | `#D71920` | liberal.ca |
| Conservative | `#142F52` navy, `#E81D2D` accent | conservative.ca |
| NDP | `#F58220` (+ `#FDB913`, `#40474F`) | ndp.ca/branding |
| Green | `#20A242`, `#1A402E` | greenparty.ca |
| Bloc | **[U] — not verified** | site returned only WordPress Gutenberg defaults |

> **Correction made during research:** `liberal.ca` and `blocquebecois.org` return `#0693E3`, `#00D084`, `#FF6900`, `#FCB900` — the **WordPress Gutenberg default editor palette**, not brand colours. Discarded. This is why Bloc has no verified hex.

**Recommendation:** use party colours **only** for categorical party identity (a "who won here" chip). For the user-facing political-*fit* axis, do **not** use red/blue at all — use **PuOr** (`#5E3C99 ↔ #E66101`) or **BrBG** (`#8C510A ↔ #01665E`). Diverging, colourblind-safe, no Canadian party freight. It also dodges the fact that left/right isn't a clean axis in a five-party system — Bloc and Green don't sit on it at all, which the README already concedes ("The political axis is a judgement call, not a measurement").

**⚠️ NDP orange `#F58220` is 2.59:1 on white — fails.** On dark `#141413` it's 7.11:1. Needs a darker variant or an outline on a light ground.

**Hazard (wildfire smoke) — honour the convention.** Canada's official **AQHI**, extracted from Environment Canada's own stylesheet (`weather.gc.ca/205/css/airquality/airquality.css`, classes `.bgValue1`–`.bgValueP`) [V]:

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | +10 |
|---|---|---|---|---|---|---|---|---|---|---|
| `#00CCFF` | `#0099CC` | `#006699` | `#FFFF00` | `#FFCC00` | `#FF9933` | `#FF6666` | `#FF0000` | `#CC0000` | `#990000` | `#660000` |

US EPA AQI, per AirNow [V]: `#00E400` `#FFFF00` `#FF7E00` `#FF0000` `#8F3F97` `#7E0023`.

> **Correction made during research:** a search summary gave EPA purple as `#990040` and maroon as `#4C0000`. Both wrong — the published RGB (153,0,76 / 76,0,38) converts to `#99004C` / `#4C0026`, and the authoritative AirNow doc lists *different values again*. Used AirNow's.

**Use AQHI, not EPA — this is a Canadian tool.** This is the one place to spend zero creativity. Users are BC residents who have stared at these exact swatches during real smoke events; the convention is pre-loaded muscle memory, and breaking it to match a brand is a safety regression dressed as design. **Quarantine it:** hazard becomes the *only* place saturated red appears on the page — which makes it read as an alarm precisely because nothing competes.

*This also resolves §0 Bug 1: if AQHI red is the only red, `--survey #B33A1E` and `--bad #A33A22` cannot both stay.*

---

## 6. Typefaces: what's shipping, with binary-verified tabular figures

Every `tnum` below confirmed by downloading the binary and reading its GSUB FeatureList — not from marketing copy.

### Free / open source

| Family | Foundry | tnum | Verified numeric features |
|---|---|---|---|
| **Saans** | Displaay | **YES** | `tnum, zero, pnum, frac, ordn` |
| **Instrument Sans** | Instrument (OFL) | **YES** | `tnum, pnum, ordn` + 12 stylistic sets |
| **Source Serif 4** | Adobe (OFL) | **YES** | `tnum, pnum, lnum, onum, zero, frac, ordn` + ss01/ss02 — 21 features, most complete free serif tested |
| **Literata** | (OFL) | **YES** | `tnum, pnum, lnum, onum, zero, frac, ordn`, variable `opsz/wght` |
| **Spectral** | Production Type (OFL) | **YES** | `tnum, pnum, lnum, onum, zero, frac, ordn` |
| **Newsreader** | Production Type (OFL) | **YES** | `tnum, pnum, ordn`, variable `opsz/wght` |
| **Bricolage Grotesque** | Atelier Triay (OFL) | **YES** | `tnum, pnum, lnum, onum, frac, ordn` |
| **Public Sans** | USWDS (OFL) | **YES** | `tnum, pnum, lnum, onum, frac, ordn` |
| **Space Grotesk** | Karsten (OFL) | **YES** | `tnum, pnum, lnum, onum, zero, frac, ordn` |
| **Geist Sans** | Vercel (OFL) | **YES** | 26 features — but now near-ubiquitous in dev tooling |

**Free — verified NO tnum, do not use for number columns:** **IBM Plex Sans** (has `zero, lnum, onum` in the full release, **no tnum**), **Instrument Serif** (`ordn` only), **Fraunces** (*no numeric features at all*, surprising given its reputation), **Libre Franklin** (`frac, ordn`).

> **⚠️ Correction:** search claimed *Switzer* (Fontshare) "does not prioritize tabular figures." **Unverifiable** — Fontshare's API returns empty and the product page is a 686-byte JS shell. Treat Switzer's tnum as **[U]**; test the binary before shipping it in a number column.
>
> **On monos:** Söhne Mono, Monument Grotesk Mono, Geist Mono, JetBrains Mono and Space Mono all lack `tnum` — **correctly**. Monospace is already tabular by construction; the feature would be a no-op. *(This is why the current build's `tabular-nums` on Plex Mono works despite the feature being absent.)*

### Paid

| Family | Foundry | tnum | Notes |
|---|---|---|---|
| **Söhne** | Klim | **YES** | `tnum, zero, frac, ordn, sups`. 692 glyphs/style, 11,072 total, **8,190 kern pairs/style**, manual VTT hinting, **slashed zero**. Ships Söhne Mono + Söhne Ikon |
| **Martina Plantijn** | Klim | **YES** | tabular *and* oldstyle figures — tables and prose from one family |
| **CF Basis** | Colophon | **YES** | `tnum, zero, pnum, lnum, onum, frac, ordn, subs, sups` — most complete figure set tested |
| **Tiempos Text** | Klim | **YES** [V-me] | Tabular + Lining + Old-style. **The quiet house serif of serious data journalism — shipped by both Bloomberg and The Pudding** |
| **Monument Grotesk** | Dinamo | **YES** | three widths incl. a genuine **Semi Mono** |
| **Unica77** | Lineto | **YES** | Haas Unica revival |
| **PP Neue Montreal** | Pangram Pangram | **YES** | variable |

### The gap in the current stack

Display (League Gothic) + sans (Plex) + mono (Plex Mono) — **but no serif.** The recurring pattern across every cluster is **grotesk/mono for the data, serif for the name and the argument**:

| Site | Data face | Argument face |
|---|---|---|
| The Pudding | Atlas Grotesk / Atlas Typewriter | **Tiempos Text** |
| Bloomberg | Neue Haas Grotesk | **Tiempos** |
| Wolff Olins | ABC Monument Grotesk | **Untitled Serif** (Klim) |
| Collection | Good Direction Sans | **Doves Type** |
| Elisa Breyer Archive | — | **Paragon** |

This tool has a human voice in it — *"what residents say"*, 28 places of real quotes with links — and nowhere to put it. **The serif is the missing epistemology:** measured numbers in mono, human testimony in serif. The type system encodes the difference between what was *measured* and what was *said*. That's a distinction the README already makes in prose and the design currently doesn't make at all.

### Pairings that signal a person [V, Typewolf]

- **Signifier + Switzer** — *Every*, Typewolf SOTD 2025-09-28. One expensive characterful serif + one free neutral grot. The serif carries the personality; the sans does the work.
- **Tobias + ABC Diatype + ABC Diatype Mono** — *Speakeasy*, 2025-12-08. **The three-role system**: display serif / UI sans / mono, where the mono is a real sibling, not a random Courier. **This is the pattern to copy.**
- **Arizona Flare + Dia** — *TR Studio*, 2025-09-27. Nobody arrives at a flared serif by default.
- **Editorial Old + Neue Montreal** — *Elena Scott*, 2025-12-09.

**The underlying rule:** every human-signalling pairing is either **sibling contrast** (cuts from one superfamily designed to differ) or **deliberate mismatch** (an old/weird/flared serif against a plain grot). Template pairings are one family at two weights, or two families that don't know each other. **The tell is that a person can say why the second face exists.**

### What cartographers actually select on — and what it says about League Gothic

Daniel Huffman's survey of working cartographers [V] is unambiguous, and it isn't about beauty. **Frutiger** wins (it was airport signage — "designed for readability at very small sizes," "good contrast on busy backgrounds," a "wide range of weights and styles"). **Univers** is praised for "lots of family members." Sans-serif dominates 6:2. The aesthetic criterion is restraint: a face should be *"bland enough not to call attention to itself."*

**The selection criterion is family size — because the family members are what encode the hierarchy.** A cartographer picks a face by counting how many distinctions it can make.

By that rule:

- **IBM Plex Sans/Mono is a genuinely defensible cartographic choice.** Large family, many weights, true italics, a mono companion. It satisfies Huffman's criterion on the merits. *(The bundling is the problem, not the face — see §0 Bugs 2 and 4.)*
- **League Gothic is the problem.** One weight, 237 glyphs, no numeric features [V-me, from the binary]. By the cartographers' own selection rule **it cannot encode anything — it has no family members to distinguish with. It can only shout.** Confine it to the collar: sheet title, sheet number. **It must never label data.** The moment League Gothic sets a city name, the type has stopped carrying information and started performing "map."

Note this arrives at the same verdict as the binary inspection in §0, by a completely independent route.

### Two type conventions worth stealing outright

**Italic = computed, not published.** Cartographers set hydrography in italic — a type style as a **declared class marker, applied without exception, and explained in the legend**. There's a class here that needs exactly that: the **9 places whose normals are computed from raw observations rather than published**. Set them in italic. Declare it: *"Italic = computed, not published."* One line in the legend, and it discharges an honesty debt the way the idiom intends. A structural steal, not a visual one.

**Imhof's sixth requirement is a direct instruction for the index.** Imhof: *"Names should not be evenly dispersed over the map, nor should names be densely clustered."* **An evenly-spaced list of 129 rows is precisely what Imhof says a map must not look like.** If clustering carries meaning — a rank cliff, a tie, the gap between the top 12 and the rest — the spacing should show it. **Uniform row height is a decision to discard information already in hand.** Cheapest convincing move available: let vertical rhythm encode the score distribution, and the list stops being a table wearing a map costume and starts being a plate.

Also documented, and therefore not a liberty: **type size and weight are legitimate ordinal variables** on a map — rank can drive them. And a label's colour should match its symbol's hue but run *darker* for legibility. If rows are tinted by score, the row's text should be the same hue, darker. That's how the sheet keeps association without losing legibility.

---

## 7. Techniques worth stealing, ranked by leverage

1. **`cqi` container-query units for card headlines** [V, Pangram Pangram]: `--heading-size-desktop: 12cqi / 10cqi / 4cqi`. Type sizes to its *container*, not the window. A city card in a 3-up grid and the same card in a detail view size correctly with **zero breakpoint code**. Highest leverage single line in this research for a card-based ranking UI.
2. **Tabular figures set *lighter* than the label** [V, Klim `.iuKILN`]: `font-feature-settings:'tnum'; color: var(--foregroundColorMix4)` — the number is mid-grey, four steps down the ramp. **Dashboards scream numbers in bold black; foundries whisper them and let the label lead.**
3. **Hairline rules, no boxes** [V, Dinamo: 9× `border-bottom:1px solid` and essentially nothing else]. Rules = document. Cards = dashboard.
4. **"What this actually means" under every metric** [V, Commercial Type]: their EULA — the densest, most-skipped document a foundry publishes — has a plain-language gloss after **every** clause. A wildfire-smoke score of 2.82 µg/m³ means nothing on its own. This is the highest-value idea for a tool whose whole problem is that numbers don't explain themselves.
5. **`--fontColorDeselected: #DDD`** [V-me, HFBK on `--backgroundColor: #EEE`]: a first-class token for **filtered-out state**. Ruled-out cities shouldn't vanish — they should **dim in place**, so you see what your preference cost you. The most directly relevant token found for a preference-ranking UI.
6. **`ch`-sized grid columns** [V-me, Beckmans]: `grid-template-columns: 1fr calc(55ch + …)` — columns locked to the reading measure, not pixels. Plus `repeat(72, minmax(0,1fr))` — a 72-column spreadsheet-grade grid (RISD independently ships `repeat(42,…)`). **12 columns is the template tell.**
7. **Em-grid off a fluid root** [V, Dinamo]: `body { font-size: calc(.06443px + 2.83565vw) }` with all layout in em. One number changes density everywhere — a free compact/comfortable toggle for a ranking table.
8. **The customizer as the product** [V, Dinamo Font Customizer]. **A preference-ranking tool *is* a customizer.** Make the fiddling the delight, not a settings drawer.
9. **Re-assert `kern` and `liga` in every feature class** [V, Grilli]: `font-feature-settings` is **not additive** — setting `ss01` alone silently kills your ligatures. Free correctness.
10. **Density switch** [V, Schema Magazine]: same records, two densities, one click. Exactly the gap between "compare 40 cities" and "read one city."
11. **Real fallbacks, chosen** [V, Ohno]: `"Covik Sans", Verdana` — Verdana because it's wide and warm and actually approximates Covik's metrics. Nobody templating picks Verdana on purpose.
12. **Re-theme per record** [V, Klim]: two colour references + a mixed ramp, restained per typeface. One engine, thirty moods. Could restain per *city*.

---

## 8. The shortlist

**Fix first (all bugs, all verified against the live build):**
1. **Build the score ramp** — §0 Bug 1b. The palette can currently label but not encode; the one thing a topo sheet is famous for is the one thing missing. Highest payoff on the list.
2. **Resolve the palette collisions** — §0 Bug 1. AQHI red becomes the only red on the page, which forces `--survey`/`--bad` apart.
3. **De-green the cast** — §0 Bug 1c. Neutralise `--ink` (the black is currently green). Re-hue or rename `--relief`: if it stays green it means *vegetation*, and that's a live misreading in a tool that ranks on climate. Separate `paper`/`sheet`/`land` (three indistinguishable sage greys).
4. **Fix or replace the fonts** — `tabular-nums` is a no-op; `.v-catch b` and `.q-label` render synthetic bold.
5. **Cut 20 type sizes to 5–6.** Kill the seven between 0.72 and 0.82rem.

**Then add:**
6. **The credit legend** — §4. Five sources, a documented structure (agency / control / method / separate note / explanatory notes) that fits them exactly, and **resident quotes as the hydrology**: a different kind of evidence, credited separately. Highest-value, lowest-risk addition.
7. **The purple slot** — a declared visual class for the 28/129. Two national agencies each spent a scarce ink plate on provenance. Right now a researched place and an unresearched place render identically.
8. **A serif for resident quotes.** Measured = mono, said = serif. Newsreader or Source Serif 4 (free, tnum verified), or Tiempos if there's budget.
9. **Italic = computed, not published** — one legend line, discharges the 9-places debt.
10. **Demote League Gothic to the collar.** One weight can't encode; it must never label data.
11. **Guess-before-reveal** on at least one dimension.
12. **The honesty stories into the collar** — the smoke-data reversal, Revelstoke's station, `Montréal → montral`. That's the voice, and it's sitting in the README.
13. **The datum offset** — draw the city tick and the station tick and state the gap, or state it in text. Never silently pick one.
14. **`--fontColorDeselected`** so ruled-out places dim in place.
15. **Non-uniform row rhythm** — Imhof #6. Even spacing discards the distribution you already have.

**Leave alone:** the warm substrate, the semantic colour names, the NTS idiom, the `.collar`/`.plate`/`.legend` nouns (they're the right nouns and the neatline split is a real convention), EPSG:3347, and "missing is not the same as mediocre." Those are already right.

**Never add:** paper texture, a compass rose, a fold shadow, deckled edges, aged-paper cream. *(Real sheets print on white — the beige is what fifty years in an archive does to a map, not a decision anyone made.)* And no scale bar unless "distance" can be defined in score-space.

**The test to run on every mark before it ships: could this have come out different?** Declination diagram — yes, it was 11° east in 1994 and something else now. Compass rose — no. That's the whole distinction, and it's why the sheet being imitated has survived a century of copying without the copies ever quite convincing.

---

## 9. Honest gaps

- **COLLINS** (`#F8F8F7` / `#140700` / `--color-brian-orange`) — agent-reported from inline props; my curl got 40 bytes (JS-gated). **Single-source.**
- **Washington Post** — every route 403/DNS-failed. ITC Franklin Pro + Postoni is **write-up-sourced only**. No hexes claimed.
- **Bloc Québécois** brand hex — site exposed only WordPress defaults. Unresolved.
- **Switzer** tnum — Fontshare API empty, page is a JS shell. Test the binary before use.
- **Feltron** — `feltron.com` is **HTTP-only**; HTTPS fails outright. The canonical data-as-print-object reference is now served without TLS.
- **Pantone 2026 Cloud Dancer 11-4201** `#F0EEE9` — TCX has no official hex; that's a third-party conversion. Trend direction verified, exact value isn't.
- **Corrected subagent claims:** (a) Beckmans "zero box-shadows" — **false**, 16 uses + a `--box-shadow` token; its `grep -c` counted lines and the CSS is minified. (b) Pudding tilt "16 rules" — I measured **12**. (c) Reuters ships **Knowledge**, not Source Sans Pro as Datawrapper's widely-cited survey says — the survey is out of date. (d) "four near-identical sage greys" — it's **three** (`paper`/`sheet`/`land`); `rule` measures 63.8 from `paper` and is adequately separated. (e) My own "texture = costume" rule was **wrong** — corrected in §4 via Stamen Watercolor. Treat secondhand font lists with suspicion; read the CSS.
- **Topographic sources dead/blocked:** `pubs.usgs.gov/gip/…topomapsymbols.pdf` (403); an Esri proceedings PDF for OS's eight principles (301 → dead index; substituted OS's own symbology docs + Kenneth Field); `wustl.pressbooks.pub` marginalia chapter (403); `codex99.com` (expired certificate). Patterson's `hypso.html` gives rationale but **publishes no hexes** — the values in §0 came from the tidyterra `data-raw` encoding of the CP69 paper.

### Primary sources for the survey-sheet section

| Source | What it is |
|---|---|
| [USGS *Topographic Map Symbols*](https://www.uky.edu/KGS/gis/USGSTopoSymbols.pdf) | the printed symbol sheet — the six-colour system incl. purple |
| [USGS *Topographic Map Margins*](https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/mapmargin.pdf) | element-by-element collar spec — credit legend, declination epoch, datum offset |
| [NRCan — NTS Maps](https://natural-resources.canada.ca/maps-tools-publications/maps/topographic-maps/national-topographic-system-maps) | Canada's national sheet spec — confirms purple independently |
| [swisstopo — National Map](https://www.swisstopo.admin.ch/en/national-map) | publishes its own measured error budget |
| [Patterson & Jenny, *Cross-blended Hypsometric Tints*, CP69](https://cartographicperspectives.org/index.php/journal/article/download/cp69-patterson-jenny/html?inline=1) | why green lowlands mislead; Imhof's aerial perspective |
| [tidyterra `data-raw`](https://raw.githubusercontent.com/dieghernan/tidyterra/main/data-raw/cross_blended_hypsometric_tints_db.R) | Patterson's palettes as data — all 41 hexes |
| [Stamen — Watercolor Process](https://stamen.com/watercolor-process-3dd5135861fe/) | the ornament is computed from the data |
| [OS — Symbology guide](https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/symbology) | six graphic variables; figure-ground |
| [Kenneth Field — Principles of cartographic design](http://cartonerd.blogspot.com/2015/10/principles-of-cartographic-design.html) | "Simplicity from Sacrifice" |
| [Huffman — Musings on Approximate Labels](https://somethingaboutmaps.wordpress.com/2020/10/20/musings-on-approximate-labels/) | "salutary ambiguity" |
| [Huffman — Cartographers' Preferred Typefaces](https://somethingaboutmaps.wordpress.com/2018/02/12/cartographers-preferred-typefaces/) | family size is the selection criterion |
| [Typography (cartography)](https://en.wikipedia.org/wiki/Typography_(cartography)) | Imhof's six requirements; italic hydrography |
- **Not verified:** Pentagram/IBM/WalkNYC palettes (not published); Base Design palette (hashed Next.js chunks); Beckmans' typeface (deliberately obfuscated as `pathToType.woff2`); sharptype.co (HTTP 429).
- **Dead:** Teleport (parking IP). **Blocked:** Merlin Bird ID, Atlas Obscura, Present & Correct (403) — no claims made.
