---
name: Where U Belong
description: A hardiness zone map that floods a whole country in five printed bands, so the map is the answer rather than an illustration of it.
colors:
  ink: "#0B2A21"
  ink-2: "#123528"
  rule: "#21493B"
  rule-2: "#2E5C4A"
  stock: "#F4EBD4"
  stock-2: "#E7DABA"
  on-ink: "#F4EBD4"
  on-ink-2: "#AFC8B8"
  on-ink-3: "#86A492"
  on-stock: "#14231C"
  on-stock-2: "#48584C"
  on-stock-3: "#6B7A6F"
  fit-0: "#33507A"
  fit-1: "#3C7F8C"
  fit-2: "#6FA24A"
  fit-3: "#D9A21B"
  fit-4: "#D6461C"
  z5: "#D6461C"
  signal: "#E9B949"
  signal-2: "#C8971F"
  check: "#A78BFA"
  thin: "#86A492"
  warm: "#E9B949"
  cool: "#3C7F8C"
  sink: "#E7DABA"
typography:
  display:
    fontFamily: "Radio Canada, sans-serif"
    fontSize: "clamp(2.6rem, 12vw, 5.5rem)"
    fontWeight: 700
    lineHeight: 0.92
    letterSpacing: "-0.015em"
    fontVariation: "font-stretch: 75%"
  headline:
    fontFamily: "Radio Canada, sans-serif"
    fontSize: "clamp(2.6rem, 9vw, 5rem)"
    fontWeight: 700
    lineHeight: 0.92
    letterSpacing: "-0.015em"
    fontVariation: "font-stretch: 75%"
  title:
    fontFamily: "Radio Canada, sans-serif"
    fontSize: "clamp(1.9rem, 6.5vw, 2.9rem)"
    fontWeight: 700
    lineHeight: 0.92
    letterSpacing: "-0.015em"
    fontVariation: "font-stretch: 75%"
  subhead:
    fontFamily: "Radio Canada, sans-serif"
    fontSize: "1.3rem"
    fontWeight: 700
    lineHeight: 0.92
    letterSpacing: "-0.015em"
    fontVariation: "font-stretch: 75%"
  body:
    fontFamily: "Radio Canada, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
    fontFeature: "tabular-nums"
  body-small:
    fontFamily: "Radio Canada, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Radio Canada, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 700
    lineHeight: 1.45
    letterSpacing: "0.07em"
rounded:
  none: "0"
spacing:
  gut: "1.5rem"
  gut-narrow: "1.1rem"
  tile-gap: "7px"
  option-gap: "6px"
  chip-gap: "5px"
  maxw: "1500px"
  reading-max: "880px"
components:
  picker-tile:
    backgroundColor: "transparent"
    textColor: "{colors.on-ink-2}"
    typography: "{typography.body-small}"
    rounded: "{rounded.none}"
    padding: "0.6rem 0.8rem"
  picker-tile-selected:
    backgroundColor: "{colors.stock}"
    textColor: "{colors.on-stock}"
    rounded: "{rounded.none}"
    padding: "0.6rem 0.8rem"
  rank-badge:
    backgroundColor: "{colors.z5}"
    textColor: "#FFFFFF"
    rounded: "{rounded.none}"
    size: "1.5em"
  action-primary:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "1rem"
    height: "56px"
  action-primary-hover:
    backgroundColor: "{colors.signal-2}"
    textColor: "{colors.ink}"
  action-primary-disabled:
    backgroundColor: "{colors.rule}"
    textColor: "{colors.on-ink-3}"
  action-back:
    backgroundColor: "transparent"
    textColor: "{colors.on-ink-2}"
    typography: "{typography.body-small}"
    rounded: "{rounded.none}"
    padding: "1rem"
    height: "56px"
  question-panel:
    backgroundColor: "{colors.stock}"
    textColor: "{colors.on-stock}"
    rounded: "{rounded.none}"
    padding: "1.4rem 1.3rem 1.6rem"
  option:
    backgroundColor: "transparent"
    textColor: "{colors.on-stock-2}"
    typography: "{typography.body-small}"
    rounded: "{rounded.none}"
    padding: "0.85rem 0.95rem"
  option-selected:
    backgroundColor: "{colors.on-stock}"
    textColor: "{colors.stock}"
    rounded: "{rounded.none}"
    padding: "0.85rem 0.95rem"
  check-answer-panel:
    backgroundColor: "{colors.stock}"
    textColor: "{colors.on-stock}"
    rounded: "{rounded.none}"
    padding: "0.8rem 1.5rem"
  check-answer-change:
    backgroundColor: "transparent"
    textColor: "{colors.on-stock-2}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.45rem 0.65rem"
    height: "42px"
  view-switch-button:
    backgroundColor: "transparent"
    textColor: "{colors.on-ink-2}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.5rem 0.85rem"
    height: "42px"
  view-switch-button-active:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.ink}"
  search-input:
    backgroundColor: "{colors.ink-2}"
    textColor: "{colors.on-ink}"
    typography: "{typography.body-small}"
    rounded: "{rounded.none}"
    padding: "0.6rem 0.75rem"
  share-button:
    backgroundColor: "{colors.z5}"
    textColor: "#FFFFFF"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "0.85rem 1.2rem"
  place-row:
    backgroundColor: "transparent"
    textColor: "{colors.on-ink}"
    rounded: "{rounded.none}"
    padding: "0.95rem 1.5rem"
---

# Design System: Where U Belong

## Overview

**Creative North Star: "The Hardiness Zone Map"**

A plant hardiness map floods an entire country in saturated bands to answer exactly
one question: what survives where. That is already this product's mechanism, so the
map stops illustrating the answer and becomes it. The whole visual world is built out
of that one idea. Ground is deep printed ink. Panels are sheets of uncoated warm stock
pasted onto the ink. Colour is not decoration, it is classification: five countable
zone bands own whole regions of the screen at once.

The surface is a printed sheet, not a dashboard. There are no gradients on any
surface, no rounded corners anywhere, no card grid, no illustration, and no imagery
of any kind. Rules and hard colour edges do the work that borders, shadows and
elevation do in a typical product UI. Density is high but ordered: full-bleed
horizontal rules, generous vertical rhythm, and one loud thing per screen.

This world was chosen against two specific alternatives, and both refusals are
load-bearing. The category default is a white sidebar of sliders over a pale
choropleth (MoveMap, Where Might I Live). Its predictable opposite is the cream-ground
editorial data essay, which is literally what this app used to be before this rebuild.
Both were rejected as the same rut: a quiet neutral field with data politely arranged
on top of it. Reaching for either is undoing the decision, not iterating on it.

**Key Characteristics:**

- Deep printed-green ink ground (`ink`), never a white or cream page.
- Warm uncoated stock (`stock`) used as pasted-on panels, never as the page.
- A five-band fit ramp, cold to hot, classed so every band is populated.
- Mustard (`signal`) as the single action colour, used sparingly.
- One typeface at two widths. The 75% width axis is the display face.
- Zero border-radius, zero gradients, hard printed edges everywhere.
- Thumb-first: a sticky action bar, 44px+ targets, one question per screen.

## Colors

A printed two-ink world (dark green ground, warm stock) with a five-step spot-colour
zone ramp laid over it and a single mustard signal for action.

### Primary

- **Printed Green Ink** (`ink`, #0B2A21): the ground of everything. `html`, `body`,
  the sheet, the map background, the mobile detail sheet. Never a lighter page colour.
- **Ink Panel** (`ink-2`, #123528): the one step up from the ground, for sub-surfaces
  that must read as part of the ground and not as pasted stock. Table header rows, the
  search field, row hover, the country switcher, the warning block, the action bar.
- **Signal Mustard** (`signal`, #E9B949): the single action colour. The 3px rule under
  the header, the 3px rule over the action bar, the primary button, the active
  view-switch tab, the step number over a question, footer section headings, the
  "what you give up" line, and the `U` in the wordmark. Nothing else may claim it.
- **Signal Mustard Deep** (`signal-2`, #C8971F): the hover state of the primary button
  and nothing else.

### Secondary

- **Uncoated Stock** (`stock`, #F4EBD4): the pasted panel. It is not a background, it
  is a physical sheet dropped onto the ink. Used for the one-question panel, the
  check-answers block, the selected picker tile, the wildcard note, the map tooltip,
  and the label plates behind place names on the flooded map. It always arrives as a
  hard-edged rectangle carrying its own dark text colour.
- **Stock Shadow** (`stock-2`, #E7DABA): the rule colour and the empty-bar track
  *inside* a stock panel, plus the stepper hover fill. Never used on the ink ground.

### Tertiary

The fit ramp. Five printed spot inks, cold to hot, read as hardiness zones.

- **Zone 1, Cold Indigo** (`fit-0`, #33507A): worst fifth of the live ranking.
- **Zone 2, Teal** (`fit-1`, #3C7F8C): second fifth. Also `cool`, the sub-zero half of
  the climate ribbon and the negative half of a resident-sentiment bar.
- **Zone 3, Moss** (`fit-2`, #6FA24A): the middle fifth.
- **Zone 4, Gold** (`fit-3`, #D9A21B): the fourth fifth.
- **Zone 5, Hot Red** (`fit-4` and `z5`, #D6461C): the best fifth. As `z5` this same red
  is also the app's counting colour: the rank number stamped on a picked tile, the
  number badge on a question, the slider thumb, the fit score in the verdict, the
  focus ring inside a stock panel, and the "Save the picture" button.

The footer legend shows the ramp with two swatches only, `fit-4` for "Fits you" and
`fit-1` for "Does not". It reads the ramp's cold end as teal rather than as the actual
coldest band, indigo. If a third swatch is ever added, start it at `fit-0`.

### Neutral

- **Rule** (`rule`, #21493B): the standard hairline on the ink ground. Row dividers,
  table cell borders, the footer top border, the back-button divider.
- **Rule Bright** (`rule-2`, #2E5C4A): the visible edge of an interactive but
  unselected control on the ink ground. Unselected picker tiles, the search field
  border, the view switch frame, the ask-progress dots.
- **On Ink** (`on-ink`, #F4EBD4): primary text on the ground. Identical value to `stock`,
  because it is the same ink hitting the same paper.
- **On Ink Muted** (`on-ink-2`, #AFC8B8): secondary text, the lede, explanatory copy.
- **On Ink Faint** (`on-ink-3`, #86A492): tertiary text, notes, rank numbers, units,
  provenance lines, placeholders. Also `thin`, the hatch colour for "not researched".
- **On Stock** (`on-stock`, #14231C): primary text inside a stock panel.
- **On Stock Muted** (`on-stock-2`, #48584C): secondary text inside a stock panel.
- **On Stock Faint** (`on-stock-3`, #6B7A6F): tertiary text and the default control
  border inside a stock panel.
- **Researched Violet** (`check`, #A78BFA): the only colour in the system outside the
  green/warm/zone families. It marks one thing, that residents were actually
  researched for a place, in the legend and in the table's provenance column. Its
  foreignness is the point: it is a data-provenance mark, not part of the ranking.
- **Sink** (`sink`, #E7DABA) and **Warm** (`warm`, #E9B949): JS-only aliases. `sink`
  is the flat grey-cream plate behind an excluded place's score. `warm` is the
  above-zero half of the climate ribbon and the positive half of a sentiment bar.

### Named Rules

**The Ink Is The Page Rule.** The ground is `ink`, always. Warm stock arrives only as
a discrete pasted panel with hard edges and its own `on-stock-*` text ramp. A stock
panel that bleeds to the full width of the page and carries the whole screen is a
cream editorial essay wearing a costume, and that is the rejected world.

**The One Signal Rule.** Mustard is the action colour and only the action colour.
Two mustard things competing on a screen means one of them is not an action.

**The Live Ramp Is `--fit-*` Rule.** The CSS defines the zone ramp twice: `--z1`
through `--z5`, and `--fit-0` through `--fit-4`, pairwise identical in value. Only the
`--fit-*` names are live. `app.js` reads them by literal string
(`RAMP = ['--fit-0','--fit-1','--fit-2','--fit-3','--fit-4']`) through
`getComputedStyle`, so the map field, the table fit plate, the mobile score chip and
the check-answers bars are all driven by `--fit-*`. `--z1` through `--z4` are
referenced by nothing at all; `--z5` survives only as the UI counting red described
above. **Editing `--z1..--z4` changes nothing.** Change `--fit-0..--fit-4` to move the
ramp, and keep `--z5` in step with `--fit-4` by hand.

**The Quantile Rule.** See Components, The Zone Field. Bands are cut by quantile of the
live fit distribution, not by raw score. A palette change must preserve five clearly
countable steps, because the map's claim is that you can count the zones.

## Typography

**Display Font:** Radio Canada at `font-stretch: 75%` (variable width axis)
**Body Font:** Radio Canada at normal width (with `ui-sans-serif, system-ui, sans-serif`)
**Label/Mono Font:** none. Radio Canada with `font-variant-numeric: tabular-nums`
carries every number in the product.

**Character:** One family doing two jobs. Radio Canada is a variable font with a width
axis from 75% to 100% and a weight axis from 300 to 700, so pushing the width to 75% at
weight 700 produces a fat condensed sans that reads as seed-rack or nursery-tag
lettering. That is the display voice, and it costs zero extra bytes. The body voice is
the same face at normal width, which keeps the page unmistakably one printed object.

### Hierarchy

- **Display** (700, `clamp(2.6rem, 12vw, 5.5rem)`, 0.92, 75% width, uppercase): the
  answer. The place name on the verdict screen, and nothing else at this size.
- **Headline** (700, `clamp(2.6rem, 9vw, 5rem)`, 0.92, 75% width, uppercase): the
  wordmark only. `Where U Belong`, with the `U` in mustard, italic markup neutralised
  to normal so the emphasis is colour rather than slant.
- **Title** (700, `clamp(1.9rem, 6.5vw, 2.9rem)`, 0.92, 75% width, uppercase): the
  step head on every screen. "What matters to you?", the question label.
- **Subhead** (700, 1.3rem, 75% width, uppercase): a place name in a list row, the
  wildcard place name, the "All 4,197" plate heading. 2rem in the mobile detail sheet.
- **Body** (400, 1.0625rem / `--t-m`, 1.5): default. Explanatory copy, question hints,
  answer values. Capped at 60ch to 66ch depending on the block.
- **Body Small** (400, 0.9375rem / `--t-s`, 1.5): the lede, secondary lines, option
  labels, search field.
- **Label** (700, 0.8125rem / `--t-xs`, +0.07em, uppercase): picker group headings,
  the "Question 3 of 5" progress line, "Why, answer by answer", footer section
  headings, view-switch tabs, chips, notes, the whole footer body.

### Named Rules

**The One Face Rule.** The display voice is a width axis, not a second family. Never
add a condensed or slab display font to get a bigger headline. The page ships as a
single self-contained file with the font inlined as base64, so a second family is real
weight on every load.

**The Uppercase Display Rule.** Everything in the display voice is uppercase with
`letter-spacing: -0.015em` and `line-height: 0.92`. Tight, stacked, and set in caps is
what makes it read as printed signage rather than as a big paragraph.

**The Tabular Rule.** `font-variant-numeric: tabular-nums` is set on `body` and is
never turned off. Every ranking, score, temperature and count in this product is meant
to be scanned in a column.

## Layout

**Sheet.** One column, `max-width: 1500px`, centred, `min-height: 100vh`, flex column
so the footer sits at the bottom. The gutter is a single token, `--gut`, at 1.5rem on
desktop and 1.1rem below 761px. Almost every horizontal padding value in the system is
`var(--gut)`, which is why rules line up across unrelated blocks.

**Screens, not scroll.** The app is a four-state machine driven by one attribute,
`data-screen` on `#sheetRoot`: `pick`, `ask`, `result`, `explore`. Each `.scr` section
is `display: none` until its state is active. This is not routing sugar, it is the
core layout decision: the product used to be a single scroll carrying the picker, the
answers, the verdict, a search box, a map, cards and a 27-column table at once, and
that is what made it unreadable. The lede and the headnote are also hidden on every
screen except `pick`, and the footer only appears on `explore`.

**Reading width.** Above 761px the `pick`, `ask` and `result` screens clamp to 880px
even though the sheet is 1500px. Only `explore`, which carries the map and the wide
table, uses the full sheet.

**Header.** A two-column grid (content, headnote) with `align-items: end`, closed by a
3px mustard bottom border. Below 761px it collapses to one column and both the lede and
the headnote are hidden outright.

**Action bar.** `position: sticky; bottom: 0`, `z-index: 30`, with a 3px mustard top
border and `padding-bottom: env(safe-area-inset-bottom)`. Buttons are `min-height: 56px`.
On mobile the primary button stretches full width; above 761px the bar left-aligns and
the primary clamps to `min-width: 320px` with the back button at 160px.

**Rhythm.** Blocks are separated by 1px `rule` hairlines and by padding, never by
margin collapse or by cards. Section padding is consistently
`1rem-1.6rem var(--gut)`. Tile gaps are 7px, option gaps 6px, chip gaps 5px: tight,
because these are racks of labels, not a card grid.

**Footer.** A `repeat(auto-fit, minmax(260px, 1fr))` grid of source notes at 1.5rem gap,
each block capped at 62ch, preceded by a wrapping legend. It exists to state what the
data does not cover, so it is dense body copy at label size rather than a nav.

### Responsive

Two breakpoints and one motion query. There is no tablet tier.

- **`max-width: 760px`** is the mobile world. `--gut` drops to 1.1rem. The headnote and
  lede disappear. Picker tiles, options and the search field step up from `--t-s` to
  `--t-m` and picker tiles take a `min-height: 46px`, so touch targets grow while
  desktop stays compact. The 27-column table (`.plate-scroll`) is removed from the DOM
  flow entirely, not scrolled, because a comparison table stops helping past about five
  items. Place detail moves from an inline expanded table row into a bottom sheet
  overlay. Footer bottom padding grows to 4rem to clear the sticky bar.
- **`min-width: 761px`** is the desktop world: reading-width clamp, left-aligned action
  bar with fixed button widths.
- **`prefers-reduced-motion: reduce`** kills every transition and animation globally
  with `* { transition: none !important; animation: none !important; }`.

`matchMedia('(max-width: 760px)')` is also read in JS and is a structural switch, not
only a style one: it decides list-versus-table rendering, how many map labels are
drawn (5 on mobile, 10 on desktop), hit-target radius, and whether a click opens the
sheet or expands a row. A `change` listener re-renders on the boundary crossing.

## Elevation & Depth

This is a printed system, so depth is **paste, not lift**. There is no elevation scale
and no ambient shadow language. Surfaces sit flat on the ink ground and are separated
by colour and by hairline rules.

Shadows appear in exactly four places, and all four carry the same idea: a sheet of
warm stock physically lying on top of the ink. They are short, dark, tight and never
soft-glowing.

### Shadow Vocabulary

- **Pasted tile** (`box-shadow: 0 2px 4px rgba(0,0,0,0.4)`): a selected picker tile,
  the moment it flips from an outlined chip to a stock sheet.
- **Pasted panel** (`box-shadow: 0 3px 8px rgba(0,0,0,0.35)`): the one-question panel
  and the wildcard note. The two large stock rectangles.
- **Floating label** (`box-shadow: 0 2px 6px rgba(0,0,0,0.5)`): the map tooltip, which
  genuinely floats over the flooded field and needs the extra separation.

### Named Rules

**The Paste Rule.** A shadow in this system means "this is stock on top of ink". If a
surface is not `stock`-coloured, it gets no shadow. Ink-coloured sub-surfaces
(`ink-2`) separate by value alone.

**The No Lift Rule.** Nothing rises on hover. Hover changes colour or border, never
`transform`, never shadow depth. The only motion in the entire system is the mobile
sheet sliding up (`0.28s cubic-bezier(0.16, 1, 0.3, 1)`) and the map tooltip fading
(`0.12s`).

## Shapes

**Zero radius, everywhere.** `border-radius: 0` is written explicitly on every control
in the stylesheet: picker tiles, action buttons, options, steppers, the range thumb,
the change button, the search field, the share button. It is stated rather than left to
the default so that no future control quietly inherits a rounded look. Even the range
slider thumb is a hard 20x34px rectangle.

**Rules over borders.** Structure is carried by 1px hairlines (`rule` on ink,
`stock-2` inside stock) and by two 3px mustard rules that bracket the whole app: one
under the header, one over the action bar. A 1px `rule-2` outline is what makes a
control look interactive; filling it is what makes it look chosen.

**Plates and stamps.** Small rectangles of solid colour are the recurring silhouette:
the rank badge (a 1.5em square of `z5` with white tabular numerals), the fit score
plate in the table and on a mobile row, the fit bar in check-answers, the legend
swatches, the provenance dot (an 8px square, hatched with a `repeating-linear-gradient`
when a place has not been researched). Circles appear only on the map, where a dot is a
place.

**Focus.** `outline: 2px solid` with `outline-offset: 2px`, always. The colour switches
with the surface: `signal` on ink, `z5` inside a stock panel, `stock` inset by -4px on
the action bar.

## Components

### Picker Tiles

The seed rack. Every rankable dimension is a tile in a wrapping flex row, grouped by
category with uppercase `pk-g` headings. Character: a rack of labels, not a form.

- **Shape:** hard rectangle (0 radius), `1px solid rule-2`, transparent fill.
- **Unselected:** `on-ink-2` text on the ink ground. Hover brightens the border to
  `signal` and the text to `on-ink`.
- **Selected:** the tile flips to a pasted `stock` sheet with `on-stock` text, its own
  border colour, and the pasted-tile shadow. A `z5` rank badge is prepended showing the
  pick order. The state change is a material change, not a tint.
- **Full:** at five picks the container gets `.full` and every unselected tile drops to
  `opacity: 0.4` with `cursor: default` and a neutralised hover. The limit is shown, not
  enforced by an error.
- **Behavior:** tapping a selected tile removes it and the rest renumber. `aria-pressed`
  and an `aria-label` carrying the rank are maintained on every tile.

### Action Bar

The primary action, pinned to the thumb. It is the only persistent control in the app
and its content is rebuilt per screen.

- **Shape:** full-bleed sticky bar, 3px `signal` top rule, `ink-2` fill, safe-area
  padding.
- **Primary (`ab-main`):** mustard fill, ink text, 700 weight, `min-height: 56px`.
  Hover goes to `signal-2`. Disabled goes to a `rule` fill with `on-ink-3` text, and
  the label itself states the blocker ("Pick at least one thing").
- **Back (`ab-back`):** transparent, `on-ink-2`, separated by a 1px `rule` right border.
  Secondary is a colour absence, never an outlined pill.
- **Labels are the state.** The button says "Answer 3 questions", "Where do I belong?",
  "See all 4,197", "Back to my result". It never says "Next" when it can say what
  happens next.

### The One-Question Screen

Character: one thing on screen, on its own sheet of paper.

- A pasted `stock` panel (`q-solo`) carries the entire question: a `z5` rank stamp and
  the "This is your top priority" line, the hint, and the control.
- Controls inside the panel use the `on-stock-*` ramp, so the panel is a complete
  little world with its own text hierarchy and its own focus colour (`z5`).
- **Options** are full-width stacked buttons (`opts-big`). Selected inverts to a solid
  `on-stock` fill with `stock` text.
- **Sliders** ship with `-` and `+` stepper buttons at 48x48px on either side, because
  a drag-only slider is unusable with a thumb. The track is a 3px `on-stock-3` line and
  the thumb is a hard `z5` rectangle. A live readout sits to the right and the scale
  ends are labelled below.
- **Progress** is a row of 30x4px dots below the panel: `rule-2` upcoming,
  `on-ink-3` done, `signal` current.

### Check-Answers Result Rows

The signature component of the result screen, and a deliberate borrowing of the GOV.UK
check-answers pattern. It is the "why", the score decomposition and the edit affordance
in one boring legible block.

- The whole block is a pasted `stock` panel spanning the sheet.
- Each row is a two-column grid (content, change button) separated by a 1px `stock-2`
  top rule, in pick order.
- The row carries four things: the rank badge plus the dimension name, what you asked
  for, what this place actually is, and a 56x8px bar whose fill width is the sub-score
  and whose fill colour comes from the same `--fit-*` ramp as the map.
- A "Change" button on the right jumps straight back to that question by index.
- **It is never collapsed behind a click.** The entire argument of the result screen is
  that the reasoning arrives without being asked for.

### Explore View Switch

Three ways to read one ranking, as a single hard-edged segmented control.

- **Shape:** a `1px rule-2` frame with 1px internal dividers. No radius, no gap.
- **Inactive:** transparent, `on-ink-2`, uppercase label type, 42px min height.
- **Active:** solid `signal` fill with `ink` text. `aria-pressed` is the source of
  truth and is mirrored in CSS.
- The switch flips `data-view` on `.plate`, and CSS shows exactly one of the map, the
  ranked list and the table. Searching force-switches to the list, because a search
  whose results you cannot see is a dead end.

### The Zone Field (signature)

The map is not a scatter of dots on a basemap. It is the answer, drawn as a flooded
hardiness sheet.

- **Tessellation.** Every cell of the sheet takes the zone colour of the nearest ranked
  place, so 4,197 points become a continuous field at a finer resolution than the county
  choropleths this category ships. Places are bucketed on a 48px grid and the search
  widens ring by ring, so a cell tests a handful of candidates rather than all of them.
- **Resolution and edges.** The field is rendered into an `ImageData` at one cell per
  four device pixels, then drawn up to full size with `imageSmoothingEnabled = false`.
  Turning smoothing off is the whole visual point: the band edges stay hard and printed
  instead of blurring into a gradient.
- **Quantile banding.** Bands are classed by **quantile of the live fit distribution**
  (cuts at the 20th, 40th, 60th and 80th percentiles), not by raw 0-100 score. Splitting
  the raw range into five equal slices painted almost everything one green and the map
  said "everywhere is fine". A printed zone map classes so that every band is actually
  populated, and this does the same. The cuts are kept in `ZONE_BREAKS` so the legend
  can state them.
- **Clipping.** The country outline is used as a canvas clip path before the flood is
  drawn, so colour stops dead at the coastline. Province and state lines are then
  stroked back into the flood in the ground ink at `globalAlpha: 0.5`, cut into the
  colour rather than drawn over it.
- **Caching.** The field is cached against a key of size, ranking length, picks and
  every answer value, so hovering, panning or opening a tooltip never recomputes it.
- **Marks.** Only the top matches get a dot (5 on mobile, 10 on desktop): a `stock` disc
  with a 2.5px `ink` stroke. Labels are placed by trying six offsets and skipping any
  that collide or leave the frame, each on its own `stock` plate, because text on a
  flooded field is otherwise unreadable.
- **Input.** Mouse hover drives a `stock` tooltip; touch uses a separate 14px
  fat-finger slop radius and opens the detail sheet directly.

### The Share Card (signature)

A quiz result spreads as an image, not a link. The entire answer lives in the URL hash,
a hash fragment is never sent to a server, so a per-result link preview is structurally
impossible on static hosting. The card exists because of that constraint.

- **Canvas: 1080 x 1350** (4:5), the tallest a feed will show uncropped. 72px margins.
- **Composition, top to bottom:** a 14px `signal` bar across the very top; the wordmark
  in `signal` at 26px; "You belong in" (or "They belong in" for a received link) in
  `on-ink-2` at 40px; the place name in `stock` in the display face, auto-shrinking from
  132px down to a 40px floor so it never clips, with the province code set beside it in
  `on-ink-3` at 38px and reserved out of the width budget; the map; a `signal`
  "WHAT YOU ASKED FOR" label; up to five answer rows, each a `z5` numbered stamp, the
  dimension in `stock`, the value right-aligned in `on-ink-2`, closed by a 1px `rule`;
  the "What you give up" line in `signal`; the place count; and the host in `on-ink-2`.
- **The map is the point.** It is drawn from the same `MAPGEO` geometry and the same
  `zoneField()` as the app, so the card is the map and not a legend of it. Height is
  capped at 430px and width follows, because the US sheet is wide and Canada's is nearly
  square. The map box is clipped exactly as the app clips it, because the Canadian sheet
  is deliberately fitted to the inhabited band and the arctic islands run off the top
  edge the way they do on a real map series.
- **Row spacing is computed from the remaining space**, not assumed, so five picks
  cannot run into the footer.
- **No score on the card.** A fit number invites an argument about the method instead of
  about the place. The score stays on the result screen where the reasoning is.
- `await document.fonts.ready` runs before any drawing, so the card is never rendered in
  a fallback face.
- Web Share with a file is the good path; everything else downloads a PNG.

Separately, `src/build_og.py` renders a static 1200x630 `og-us.png` / `og-canada.png` in
the same palette for the page-level link preview. That is a build-time artifact and does
not carry a result.

### Ranked Place Rows (mobile) and the Plate (desktop)

- **Row (`pcard`):** a three-column baseline grid of rank, name, fit plate, with the
  reason and the weighted-dimension chips wrapping underneath. Transparent at rest,
  `ink-2` on hover or press, closed by a 1px `rule`. Despite the class name it is a
  ruled row, not a card: no radius, no shadow, no panel fill.
- **Fit plate:** a solid rectangle of the row's ramp colour with white 700 numerals.
  An excluded place gets a flat `rule` plate and an em-dash, so "ruled out" reads as a
  different kind of thing rather than as a low score.
- **Plate (`plate-t`):** a dense collapsed table at label size, sticky `ink-2` header,
  right-aligned numeric cells, per-cell ramp tinting on weighted columns only, unweighted
  columns dimmed to 45%. The one dimension that separates a place from its near
  neighbours gets a `signal` inset outline.
- **Missing data reads `..`**, StatCan's published symbol for not available, in
  `on-ink-3`. Never a dash, never a zero, never an estimate.

### Detail Sheet (mobile)

A bottom sheet overlay: a 72% opacity ink scrim, an `ink` card pinned to the bottom with
a 3px `signal` top border, `max-height: 92vh`, sliding up over 0.28s. It pushes a history
entry so the hardware back button closes it without disturbing the hash, and it locks
body scroll while open.

## Do's and Don'ts

### Do:

- **Do** keep `ink` (#0B2A21) as the page ground on every screen and every new surface.
- **Do** introduce a new light surface as a pasted `stock` panel with hard edges, the
  paste shadow, and the full `on-stock` / `on-stock-2` / `on-stock-3` text ramp.
- **Do** drive any fit-coloured element from `--fit-0` through `--fit-4`, and keep `z5`
  equal to `fit-4` if you retune the ramp.
- **Do** class any new banded visualization by quantile of the live distribution, so
  every band stays populated and countable.
- **Do** write `border-radius: 0` explicitly on any new control.
- **Do** reach for the width axis (`font-stretch: 75%`, weight 700, uppercase) when you
  need a display voice, and never for a second font family.
- **Do** keep touch targets at 42px minimum and 56px on the primary action, and give
  every slider a pair of `-` / `+` steppers.
- **Do** state the cost. A result surface must show what you give up alongside what you
  get, uncollapsed.
- **Do** keep everything inlineable. Fonts, data and map geometry ship inside one
  self-contained HTML file per country, so no new asset may require a network request.
- **Do** use `..` for a missing value.

### Don't:

- **Don't** build a white or pale sidebar of sliders over a light choropleth. That is
  the category default (MoveMap, Where Might I Live) and it is explicitly refused.
- **Don't** retreat to a cream-ground editorial data essay. That is this app's own
  previous design and it was rejected as the same rut as the first refusal.
- **Don't** add gradients to any surface. The only `linear-gradient` in the system is a
  2px hatch pattern standing in for "not researched".
- **Don't** add rounded corners, card grids, elevation scales, hover lift, or imagery.
- **Don't** spend mustard on anything that is not an action.
- **Don't** turn on `imageSmoothingEnabled` for the zone field. Soft band edges destroy
  the printed-map claim.
- **Don't** edit `--z1` through `--z4` expecting the map to change. They are dead
  aliases; `app.js` reads `--fit-*` by name.
- **Don't** collapse the reasoning behind a disclosure. The check-answers rows, the
  tradeoff line and the provenance notes are visible by default on purpose.
- **Don't** put a fit score on the share card.
- **Don't** add a second font family, an icon font, or any remote asset.
- **Don't** rely on a per-result link preview. The answer lives in the URL hash, which
  never reaches a server, which is exactly why the share card exists.
