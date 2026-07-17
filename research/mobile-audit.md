# Mobile audit — Where To Live / Canada

Live: https://rohamghiasicw-star.github.io/where-to-live-canada/
Audited from source (the deployed `index.html` is byte-identical to the local build: 1,568,749 bytes). CSS lives in `app/style.css`, JS in `app/app.js`, both inlined into the single root `index.html` by `src/build_app.py`. All values below were read out of the CSS/JS and re-confirmed against the live deployed file.

The whole app is one viewport-width column with **only two media queries**: `@media (max-width: 1000px)` and `@media (prefers-reduced-motion: reduce)`. There is **no phone breakpoint** — nothing is tuned below 1000px. So at 375px you get the 1000px "tablet stack" layout at desktop density.

---

## PART 1 — Concrete current failures at 375px

### A. Structure — the answer is buried under the whole survey
- `.field { grid-template-columns: 300px 1fr }` on desktop becomes `grid-template-columns: 1fr` at `@media (max-width:1000px)` (`style.css:335-337`). Good in principle, but it stacks the **17-question survey ABOVE the verdict + map + table**. On a phone you scroll through all 17 questions (each with a label, hint, weight control, and options) before you ever see your result.
- Same rule sets `.survey { position: static }` (`style.css:337`), dropping the sticky sidebar that desktop has (`.survey { position: sticky; top: 0 }`, `style.css:129`). Consequence: to change one weight and see the table re-rank you must scroll **up** to the survey, tap, then scroll **down** to the plate. Ping-pong on every adjustment. There is no tab / segmented control / bottom-sheet to switch between "what you want" and "the answer".
- **This is the single biggest mobile failure and it is layout, not a tap size.**

### B. Tap targets under 44×44 (Apple/WCAG minimum) — measured from CSS

| Control | Selector | CSS value | Rendered size | Verdict |
|---|---|---|---|---|
| Weight "tick" boxes (3 per question ×17 = 51 of them) | `.tick` (`style.css:149-152`) | `width:26px; height:22px` | **26×22px** | FAIL — ~25% of min area, and three sit 3px apart (`gap:3px`, `style.css:148`). This is the primary "how much it matters" control. |
| Option chips | `.opt` (`style.css:158-162`) | `padding:.55rem .75rem; font-size:.9375rem; line-height:1.15` | height ≈ **~37px**; short labels ("Left", "Village") are narrow | FAIL (<44). |
| Slider thumb | `input[type=range]::-webkit-slider-thumb` (`style.css:174-178`) | `width:12px; height:24px`; track `height:1px`; row `height:26px` (`style.css:170`) | **12px-wide thumb**, 26px hit strip | FAIL — precise drag on a 12px thumb over a 1px track is very hard on touch. |
| "Start over" | `.reset` (`style.css:184-187`) | `padding:.35rem .6rem; font-size:.8125rem` | height ≈ **~33px** | FAIL (<44). |
| "Send this to someone" | `.v-share` (`style.css:206-209`) | `padding:.45rem .8rem; font-size:.9375rem` | height ≈ **~39px** | FAIL (<44). |
| "show all 712" / "show top 60" | `.showall` (`style.css:355-358`) | `padding:0`, underlined 13px text link | glyph-height only | FAIL — tiny inline link. |
| Place name (opens the detail row) | `.pname button { all:unset }` (`style.css:257`) | `all:unset` strips padding; 15px text in a td with `.6rem` vertical padding | tap target ≈ text glyph ~15px tall | Marginal — relies on the row, the button itself is unpadded. |

### C. Column headers are hover-only — dead on touch
- `.plate-t thead th[title]` uses `cursor:help` + native `title=` tooltips (`style.css:386`; built in `app.js:528-529`). The intro literally instructs *"Hover any column heading to see what it means and where the number came from"* (`index.html` how-to step 3). **There is no hover on touch**, so on a phone the 17 abbreviated headers — `Jan, Jul, Snow, Sun, Smoke, People, Drive, Home, Lean, Growth, Age, Short, Carfree, Unemp, Diverse, French, Mood` — cannot be expanded at all. `Short` = "under-15-min commute" and `Diverse` = "% immigrants" are unguessable.

### D. The table — 21 columns, horizontal scroll, no frozen name column
- Column count: rank + Place + Fit + **17 data columns** + provenance = **21 columns** (confirmed: `Q.filter(q=>q.col)` = 17; `app.js:526-530`; comment at `app.js:504` says "21 columns"). Default view renders **60 rows** (`PLATE_N = 60`, `app.js:231`), expandable to all 712.
- Width: cells are `.cell { padding:.6rem .5rem }` with `white-space:nowrap` (`style.css:233-236, 242`), `Fit` col `width:3.2rem`, table `font-size:.8125rem` (13px). 17 data columns at ~40-55px each + name + fit + rank + prov ≈ **~840-950px of table** on a 327px-usable screen (375px − 48px gutters).
- Behaviour: `.plate-scroll { overflow-x:auto }` (`style.css:223`) → the table **scrolls horizontally**. It is contained, so the page body itself does not scroll sideways (good). But:
  - **No frozen first column.** Neither `.rank` nor `.pname` has `position:sticky; left:0`. `thead th` is `position:sticky; top:0` (vertical only, `style.css:226-228`). So as soon as you scroll right to read Smoke/Home/Lean, **the place-name column scrolls off-screen** and you lose which row is which. This makes the "read across a row" and "compare down a column" purpose of the table unusable on a phone.
  - 13px tabular cells are legible but small; the header row is 13px too.

### E. Map — height is fine, interactivity is not
- `canvas#map { width:100% }` with no CSS height (`style.css:315`); JS sets `H = round(W × MAPGEO.height/1000)` and `MAPGEO.height = 662.5` (`app.js:326`), i.e. height = width × 0.6625. At ~327px canvas width the map is ~**217px tall** — a sensible third of the viewport, **not** a failure.
- But every map interaction is bound to **mouse events only**: `cvs.addEventListener('mousemove'…)` sets the hover target and tooltip, `'mouseleave'` clears it, and `'click'` early-returns `if (hot < 0)` (`app.js:628-648`). There are **no `touch`/`pointer` handlers**, and touch devices have no hover. Result: on a phone the **tooltip never shows and tap-to-select a dot is unreliable/dead**. The dot labels also shrink to the 9px floor (`Math.max(9, k*12)`, k≈0.33 → clamped to 9px, `app.js:352`) and most of the top-8 labels get dropped by the collision test.

### F. Spacing / density never adapts
- `--gut: 1.5rem` (24px) is used as the horizontal pad on every section and never reduced (`style.css:64`). On 375px that's **48px (13%)** of the screen gone to gutters, tightening the already-overflowing table.
- Section text is mostly `--t-xs` = 13px (headnote, hints, footer, table). Readable but dense on a phone.

### G. Sticky elements — minor, no hard overlap
- `.qgroup` survey section labels are `position:sticky; top:0; z-index:1` (`style.css:346-351`) and `thead th` is `sticky; top:0; z-index:2`. They live in different scroll regions so they don't collide destructively. There is **no `position:fixed` element anywhere**, so no fixed-bar overlap on a short viewport. (No sticky tap-to-call bar either — correct, this is a data tool, not a lead-gen page.)

### H. iOS zoom-on-focus — checked, NOT triggered (the one thing that's fine)
- iOS only zooms when a focused **text/number/email/tel/url/password/textarea/select** has `font-size < 16px`. This app has **none of those** — the only inputs are `<input type="range">` sliders (`app.js:559`) and `<button>`s. Range and button do not trigger focus-zoom. Body is 17px (`--t-m`). So there is **no zoom bug**. (Still worth bumping the 13px table/hint text for readability, but it is not a zoom trigger.)

---

## PART 2 — How comparable tools solve this on a phone

### Teleport Cities (the closest philosophical twin — now dead, this is its exact model)
A preference-weighting quiz identical in spirit to this tool: pick the life-quality aspects that matter, enter budget, get a **ranked list of cities each with a single composite Match Score**, visualised as a horizontal bar whose coloured segments show how much each category contributed. Tap a city → detail view; tap the score bar → the match **broken down by every preference you chose**. It never showed a 20-column matrix on a phone — it showed one match bar per city and drilled down. This is the model to copy.

### Zillow / Realtor.ca (the map+list pattern)
On mobile they do **not** show map and list at once. A **map/list toggle**, plus a **bottom sheet** that peeks up over the map with the result cards; drag it up to fill the screen, drag down to see the map; tap a pin → a single card slides in. NN/g's bottom-sheet guidance backs this exactly: bottom sheets are made for "displaying location details while allowing users to pan the underlying map," support drag-to-expand, a visible close button, and back-button dismiss.

### Niche.com place pages
Compresses ~a dozen dimensions into **letter-grade badges** (A+ … D−). Rankings are a vertical **list of place cards** (grade + one-line why), tap → a detail page with graded category sections. The grade badge does the heavy lifting a numeric column can't on a small screen.

### Nomad List / nomads.com
Vertical scroll of **city cards** (photo + a few score badges), a **filter/sort sheet** ("sort by internet / cost / weather"), favourites, and an integrated map. The key move: you compare on **one chosen metric at a time** by re-sorting, not by reading 20 columns.

### Numbeo (quality of life)
Old-school wide interactive tables that **overflow horizontally on a phone** (the same weakness this tool has). Its one good mobile-friendly piece is the **2-city side-by-side comparison** (`comparison.jsp`): pick two places, see every metric stacked in two columns — two columns fit on 375px where 21 never will.

### MoneySense — Canada's Best Places to Live (the direct Canadian analog)
Two artifacts: (1) a 400+ city ranking that on phones is a **left/right horizontal-scroll table with tap-to-sort arrows** — i.e. Numbeo's weak pattern again; and (2) a **"Create your own ranking"** tool that lets you weight the criteria and collapses the result to a **ranked list** — which is the part that actually works small.

### US News Best Places to Live
250 metros as a **ranked card list** (score + blurb), tap → detail page with category-score breakdown, plus a limited compare feature. Cards + drill-down, not a live matrix.

**The pattern every one of them converges on for phones:** a **ranked list / cards** carrying one headline score, **drill-down** to a per-place breakdown, and comparison done **one metric at a time (re-sort)** or **two places head-to-head** — never a wide always-on matrix.

---

## PART 3 — The table problem, concretely

712 places × 18 stats (Fit, Jan, Jul, snow, sun, smoke, population, drive, home price, lean, growth, age, commute, carfree, unemployment, diversity, French, resident-mood) cannot be a scroll-both-ways grid on a phone. Nobody reads a 21st column on a 375px screen.

**Single best mechanic: a ranked list of place cards, each showing Fit + the 2–3 stats that actually decided this place for THIS user, tapping a card opens a bottom-sheet with the full breakdown.**

Why this and not a squished/scroll table:
1. **The app already computes exactly the "which stats matter" data.** `scoreAll()` produces per place `good` (top 2 dimensions it scores well on), `bad` (its worst), and `confusion()` returns the ONE dimension that separates it from its near-neighbours (`app.js:268-316`). The verdict already writes sentences like *"It gets you the winter and the size. You give up the price."* So each card can show **Fit score + "gets you X and Y" + "you give up Z"** with zero new data — it surfaces the 3 relevant columns per place instead of forcing the user to find them among 17.
2. **The detail sheet already exists.** `detailHTML(r)` (`app.js:449-502`) renders the full climate ribbon, place stats, and resident sentiment for one place. Reused as-is, tap-a-card → **bottom sheet** (Zillow/Realtor.ca pattern, drag-to-expand, close button) is the whole "read across a row" job, done vertically where there's infinite height.
3. **Cross-place comparison ("which of these is coldest / cheapest") → a one-metric sort/compare chip row.** A horizontal chip row of the 17 dimensions; tap one and the list re-sorts by it and each card shows a **mini bar for that single metric**. This delivers the desktop "compare down a column" affordance one column at a time — the Nomad List sort model. The map (which already colour-encodes Fit spatially) stays as the country-wide overview.
4. **Head-to-head → an optional pick-2 compare** (Numbeo `comparison.jsp`): select two places, show all 18 stats in two columns. Two columns fit; twenty-one don't.

**Real apps that do this well:** **Teleport** (ranked match-score list + tap-to-see the per-preference breakdown — nearly this exact tool), **Zillow / Realtor.ca** (the bottom-sheet-over-map mechanic), and **Niche** (one compressed headline score per card, drill-down for the rest).

Keep the full 21-column plate as a **desktop-only** view (it's genuinely good there — Sibley's matrix). On phones, swap it for the card list; the underlying `ranked` array feeds both.

---

### Sources
- NN/g, Bottom Sheets: Definition and UX Guidelines — https://www.nngroup.com/articles/bottom-sheet/
- Teleport match score — https://teleport.org/blog/2015/04/match-score/ ; Smithsonian writeup — https://www.smithsonianmag.com/innovation/where-should-you-live-app-will-tell-you-180962588/
- Zillow map/list critique — https://harpreetvishnoi.medium.com/product-critique-zillow-mobile-app-1dd0a1c26fb9 ; Map UI list+details — https://mapuipatterns.com/list-details/
- Niche methodology / place page — https://www.niche.com/places-to-live/rankings/methodology/ ; https://www.niche.com/places-to-live/new-york-city-new-york-ny/
- Nomad List / nomads.com — https://nomads.com/map ; https://nomads.com/explore
- Numbeo QoL comparison — https://www.numbeo.com/quality-of-life/comparison.jsp ; rankings — https://www.numbeo.com/quality-of-life/rankings.jsp
- MoneySense Best Places (create your own ranking) — https://www.moneysense.ca/canadas-best-places-to-live-2018-create-your-own-ranking/
- US News Best Places to Live — https://realestate.usnews.com/places/rankings/best-places-to-live
