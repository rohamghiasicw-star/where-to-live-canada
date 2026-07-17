# Mobile prototype — key decisions

Working prototype at `proto/mobile.html`. Single self-contained file, vanilla HTML/CSS/JS,
no frameworks, no network requests. Opens straight off disk. Three screens switched by a
fixed bottom tab bar (Answer / Map / List). Built to be judged on real content: the 30-place
`data/proto_slice.json` is inlined and scored with the **same model as the desktop app** —
weighted power mean, weights 1 / 3 / 9, p = 0.5, hard dealbreakers for smoke and price.

Scope note: the slice carries 10 fields, so the survey scores the **8 dimensions the data
supports** (winter, summer, snow, wildfire smoke, size, near-a-big-city, housing budget,
politics) plus the `lived` provenance flag. The remaining 9 dimensions of the real app
(sun, growth, age, commute, carfree, jobs, diversity, French, resident mood) have no numbers
in the slice, so they are left out rather than faked — the layout pattern scales to all 17.
Type is a system sans stand-in for Radio Canada; everything else is the real ink/paper/teal.

---

## 1. Survey: sectioned scroll, not a stepper

**Chose a grouped, sticky-sectioned scroll** (Climate / The place), not a one-question-per-screen
stepper.

Reasoning: this is a *tuning* tool, not a signup form. The value is in nudging a weight, seeing
the answer move, nudging another — a loop the user runs many times and out of order. A stepper
optimizes for "answer each once, in sequence, then see a result," which is the wrong loop: it
hides the running effect behind Next/Back and makes it slow to jump back to the one question you
want to retune. The desktop app is also a single scroll, so this keeps the mental model.

To keep a 17-question scroll from feeling like a wall: sticky group headers, one question per
card, the current answer echoed on the right of each question label, and — most importantly — a
**running "your top pick so far"** pinned to the top of the screen. That pinned result is what a
stepper's final screen would have given you, except it's always visible, so the survey never
feels like data entry with a delayed payoff. (Verified: setting Winter to "A lot" flips the
pinned pick from Longueuil 74 to Halifax 79 live.)

## 2. Importance control: a four-stop labelled segmented control

The desktop app uses three 26px squares (below the 44px tap minimum, and their meaning —
1/3/9 weighting — is invisible). Replaced with a full-width segmented control:

**Skip · A little · Matters · A lot** → weights 0 / 1 / 2 / 3.

- Every stop is a real labelled button, ~85px wide × 46px tall — comfortably past 44px.
- The words carry the meaning, so there's nothing to decode and no hover-only tooltip.
- "Skip" is an explicit, discoverable off state (the desktop "click again to turn off" is not
  discoverable on touch). Choosing an answer chip auto-promotes Skip → A little, so you can't
  set a preference that silently doesn't count.
- Selecting Skip dims the answer control for that question, so "this one is off" reads at a glance.
- The active stop is the only filled (ink) element in the row, so weight is legible without color,
  leaving the teal ramp free to mean "fit" everywhere else.

## 3. Bottom-sheet snap mechanics

Two sheets: the **map results sheet** (peek / half / full) and the **detail sheet** (open /
drag-to-dismiss). Both use Pointer Events, so one code path handles touch and mouse.

Snap points are computed from the live map-area height, as `translateY` offsets:
`peek` shows the handle + header + one row (~132px), `half` ~50%, `full` ~90% (leaving a strip
of map above). On release the sheet snaps to the nearest of the three.

The one subtlety that makes it feel right: **the pointer is only captured once a drag crosses a
~6px threshold.** A plain tap on a card inside the sheet is never swallowed — it falls straight
through to open that place's detail. Dragging the handle always moves the sheet; dragging the
*list* only moves the sheet when it's not full, or when it's full and already scrolled to the top
and you're pulling down — otherwise the list scrolls natively. The detail sheet uses the same
threshold trick so its close button and content stay tappable, and a drag down past ~28% of its
height dismisses it. All snap transitions are gated behind `prefers-reduced-motion`.

## 4. The table → card + detail sheet

The desktop plate is ~21 columns; on a phone that's an unreadable horizontal scroll. The answer
is **not a smaller table** but a two-level disclosure:

- **List screen** = a stacked card per place: rank, name + province, fit score (teal chip), a
  provenance dot if residents were researched, and only the **3–4 stats that actually moved this
  place's ranking** — chosen per card by weight × distance-from-neutral, so a place near the top
  on price shows its price, not a fixed column set. No two cards necessarily show the same stats,
  which is the point: show why *this* place ranks, not a uniform grid.
- **Detail sheet** = tap any card (on the List *or* on the Map results sheet, *or* a dot on the
  map) to open a full-height sheet with everything: a **"Why it ranks"** breakdown (every active
  dimension, your ask vs this place's value, and a teal sub-score bar) followed by the complete
  record and the provenance/sources note. Ruled-out places are parked below the ranking and open
  with a dealbreaker banner.

So the 21 columns become: 3–4 relevant numbers on the card for scanning, and the full record one
tap away — never a horizontal scroll.

---

## Requirements check

- Tap targets ≥44px (chips 44, segments 46, tabs 60, close 44). Inputs render ≥16px (no iOS zoom).
- Fixed bottom tab bar, thumb-reachable, clear active state (ink label + top rule).
- Bottom sheets drag and snap with real touch + mouse (Pointer Events); tested peek→full and back.
- No horizontal overflow at 375px; `overflow-x:hidden` on root, card stats wrap.
- `prefers-reduced-motion` disables all transitions/animations.
- Everything inline; no external fonts, scripts, or images. The map is a hand-drawn stylized
  Canada on canvas with dots projected from real lat/lng — geometry is approximate by design,
  the interaction is what's being judged.

## Viewing

Open `proto/mobile.html` directly in a browser, or serve the folder
(`python3 -m http.server`) and load it at 375px width / mobile emulation.
