# Breaker / QA report — "Where to live in Canada"

URL tested: https://rohamghiasicw-star.github.io/where-to-live-canada/
Widths: phone 375x812 / 390x844, desktop 1280x900, landscape-phone 820x400.
Date: 2026-07-17.

## Headline
The app is genuinely hard to break. Zero console errors or warnings across the whole
session. No crash, no `NaN`, no `undefined`, no `[object Object]`, no broken quote links.
The scoring engine, share links, back button, tab switching and map all behave correctly.
Everything below is either a cosmetic/copy nit or an edge case — nothing is a functional break.

IMPORTANT CONTEXT: this URL serves a **STAGING build** — a red "STAGING · work in progress,
may be rough · the stable version is here →" banner, a `[STAGING] …` document title, and it
**redeployed live while I was testing** (the app script grew 38,758 → 39,365 bytes mid-session).
That churn reset in-memory state a couple of times. I separated those harness/redeploy artifacts
from real bugs (see bottom).

---

## Bugs, worst first

### 1. (LOW-MED) Methodology copy contradicts the app's own data — Revelstoke snow
- The "About the data / Climate" text states: *"Revelstoke's nearest published station is 43km
  away and 1,431m up a mountain, reporting 1,388cm of snow. That is the alpine snowpack, not the town."*
- The actual data: Revelstoke snow = **424.6 cm**, station **"REVELSTOKE A", 4.2 km away, 14 m
  elevation difference** (`stations_used.tmean`). The mountain station is no longer used.
- Nothing in the entire 712-place dataset reports anywhere near 1,388 cm — the max is Valemount BC
  at 532 cm.
- Repro: open the site → scroll to the About text (mentions "1,388cm") → then open Revelstoke's
  detail sheet, which reads "From REVELSTOKE A, 4.2km away, 14m difference in elevation… Snow 374/424cm".
- Expected: the worked example matches the data. Saw: the example describes a 43km/1,431m/1,388cm
  station that the app no longer uses and that contradicts Revelstoke's own row. Stale example.

### 2. (LOW-MED) Lloydminster appears twice; one map dot is unreachable
- "Lloydminster (Part)" is in the list **twice**: once SK (pop 11,843, home $283k) and once AB
  (pop 19,739, home $344k). Same for "Flin Flon (Part)".
- Their map dots sit **0.22 px apart** (coords x 254.1/253.5, y 378.4/378.3). A tap always resolves
  to the **AB** entry — the **SK Lloydminster dot can never be selected on the map**.
- Repro (map): tap the Lloydminster dot on the prairies → always opens Lloydminster AB. There is no
  tap location that opens the SK one.
- Also user-facing: the raw census suffix "(Part)" reads like a glitch, and seeing the same town
  name twice with different numbers is confusing.
- Expected: one clean "Lloydminster" (or clearly distinguished halves) reachable on the map.
  Saw: duplicate rows + an unreachable overlapping dot + raw "(Part)" label.

### 3. (LOW) Detail-sheet provenance leaks raw StatCan census type codes
- Every place's detail sheet fine-print shows the census type code: "Goderich, **Town (T)**",
  "St. John's, **City (CY)**", "…**Village (V)**". Counts across the data: T ×272, CY ×142, V ×135,
  VL ×48, DM ×26, TV ×21, C ×10, MU ×6, HAM ×4, MD ×4, plus others.
- Repro: open any place's detail sheet → read the grey "Census figures are for X, Town (T). 2021
  Census…" line.
- Good news: primary place **names are clean** — 0 codes leak into the ranked list, cards, or verdict.
  Only the grey provenance line shows it. Cosmetic.

### 4. (LOW) 135 riding names render with double hyphens
- Federal ridings show "--" where the real name uses an em-dash, e.g. "Huron--Bruce",
  "Cape Breton--Canso--Antigonish", "Sydney--Glace Bay", "Terra Nova--The Peninsulas". 135 ridings affected.
- Repro: open any place detail sheet → "Riding" row.
- Reads like a typo. (Note: consistent with a deliberate no-em-dash house style, but "--" looks unfinished.)

### 5. (LOW) "Someone sent you their answers" banner never clears after you edit
- Open a shared link → banner: *"Someone sent you their answers, so this is **their** result.
  Change anything on the left and it becomes yours."* After you change an answer, the result is now
  yours, but the banner **still says "their result."**
- Repro: open a share link, change the Winter slider → verdict/ranking update, banner unchanged.
- The banner is set once at load and never reset. Mildly self-contradictory.

### 6. (LOW, edge) Share button's clipboard-failure fallback dumps the raw URL as its label
- When `navigator.clipboard.writeText` is blocked (permission denied / non-secure context / some
  in-app browsers), the `catch` sets the button text to `location.href`, so "Send this to someone"
  becomes a long unreadable URL string with no "copy failed" explanation.
- Repro here: click "Send this to someone" in the automation context → button label becomes
  `https://…/#6.3_20.1_1.1_…` (the whole hash).
- On normal HTTPS mobile/desktop this path usually succeeds (or uses the native share sheet), so it's
  an edge case, not the common path. Still, the fallback is ugly and unguided.

### 7. (LOW, defensible) 760px breakpoint puts landscape phones / small tablets on the desktop mega-table
- Breakpoint is `max-width:760px`. At 761–1023px (landscape phone, small tablet) the app switches to
  the desktop **21-column plate** (table scrollWidth ≈ 1,351px on an 820px screen → horizontal scroll).
- Repro: rotate a phone to landscape (e.g. iPhone → 844px wide) → clean cards flip to a wide scrolling
  21-column table.
- The document itself doesn't overflow horizontally (the table scrolls inside its own container), and
  the stated design intent is "table only helps at desktop," so this is defensible — but a landscape
  rotation is a jarring layout change and the table is cramped at ~820px.

---

## What held up well (tried hard to break, couldn't)

- **Everything Skip (nothing matters):** graceful. Verdict reads "You should live in Carbonear NL.
  It is the closest thing to what you asked for." Every fit = 0, ranked by data order. No crash, no NaN.
- **Exactly one thing "a lot" drives the whole ranking:** Winter-only at warm (+6) → Greater Victoria
  BC (Jan +5.7°); at cold (−26) → Dawson YT / Churchill / Yellowknife / Iqaluit. Correct.
- **Contradictions are explained, never nonsense:**
  - Big city + $200k budget → excludes Toronto/Vancouver/Montréal/Calgary/Ottawa on "**the price**"
    (378 of 712 cut), offers the largest affordable cities (Trois-Rivières, fit only **40**), and the
    verdict spells it out: *"Nowhere that fits the rest of your answers is also big city (size). That is
    the one giving way. 40 out of 100 is the best fit available, so something has to give."*
  - Dealbreaker wildfire smoke → rules out the entire BC interior on "**the smoke**" (Kamloops 2.82,
    Kelowna 2.40, Penticton 2.54 µg/m³; 58 cut). Correctly labelled.
  - "As far from a city as possible" + "short commute a lot" → not actually contradictory; returns
    remote towns that also have short commutes (fit 100). Sensible.
  - Even both hard filters stacked (dealbreaker smoke + $200k) leaves 317 survivors, so the empty
    state is practically unreachable — but it's still handled ("Nothing clears your dealbreakers. Loosen one.").
- **Share / result loop:** copying the link and opening it fresh restores the **exact** answers and
  result (winter +6/A-lot, politics Left/A-lot → Victoria BC) and shows the "Someone sent you their
  answers" banner. Changing one answer updates the hash so a re-share carries the new state.
- **Back button + detail sheet (mobile):** opening a place sheet pushes one history entry and locks
  scroll; the browser **Back button closes the sheet**, keeps you on the app, unlocks scroll, and
  preserves the shareable hash. Clean (the sheet is a full modal, so answers can't drift behind it).
- **Rapid Answer/List/Map switching:** 9 fast switches — map canvas stays correct (716x474, 712 pts,
  ~103k painted pixels), never blank, never stuck, no misrender.
- **Map dots:** tapping a dot opens the correct place (audited top dots: Winnipeg→Winnipeg,
  Iqaluit→Iqaluit, etc.), tapping empty ocean opens nothing, no dot/place mismatch (except the
  Lloydminster overlap in bug #2).
- **Resize desktop↔mobile:** desktop builds the 21-col/60-row plate and hides the tab bar; mobile
  builds cards and shows the tab bar; no document-level horizontal overflow at 1280. Switch logic is
  sound (matchMedia + resize listeners).
- **Data sanity:** all 211 resident quotes have valid `source_url`s (no `new URL()` throw, no broken
  quote link); no NaN fields; only "extreme" home price is West Vancouver $3.13M (legit). NA renders
  as ".." (e.g. "Unemployment .. %"), never NaN. Detail sheets show station provenance correctly.
- **Console:** zero logs, zero errors, zero warnings the entire session.

---

## Harness / staging artifacts (NOT app bugs — ruled out)
- Phantom slider/weight changes early on were my own mis-fired clicks (the screenshot coordinate space
  is 375x812; an out-of-bounds y and a couple of mis-mapped taps nudged sliders). The app correctly
  honored each click.
- State resets mid-test were the **staging site redeploying** (script 38,758→39,365 bytes) + reload
  form-restoration, not app logic.
- `resize_window` in this harness doesn't dispatch a real `resize`/matchMedia `change` event, so the
  DOM looked stale until I called `render()` manually — on real hardware those events fire and the
  layout rebuilds. `decodeState` round-trips perfectly and is not buggy.
