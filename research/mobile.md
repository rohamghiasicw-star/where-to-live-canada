# Mobile rebuild research: "Where to live in Canada"

Concrete, sourced patterns for turning the desktop tool (left survey column, Canada map, 21-column comparison "plate") into something usable at 375px. Every pattern below says what it is, who does it well, and the honest tradeoff. Citations are inline URLs.

The tool as it stands today (from `app/app.js`, `app/index.html`):
- 17 dimensions, each with a value (range slider or option buttons) plus a 0-3 importance weight on the 1/3/9 scale.
- Answers are the shareable state, encoded in `location.hash` (`encodeState`/`decodeState`). This must survive any restructure.
- Three outputs: a text verdict ("you should live in X"), a canvas map of Canada shaded by fit, and the 21-column plate (rank, place, fit, then 17 dimension columns + a provenance dot). Tapping a place already expands a transposed detail block (`detailHTML`).

The single most useful framing from the research: this is not really a "table" tool, it is a **ranking + compare-a-few** tool. NN/g's comparison-table research says comparison tables only support real decision-making at **5 items or fewer**, and beyond that you must "add other mechanisms such as filters to help users narrow down the larger set of possibilities to 5 or fewer" (https://www.nngroup.com/articles/comparison-tables/). We have 712. So on mobile the 21x712 plate is not the product. The product is: an answer, a ranked list, a place detail, and the ability to pin a handful to compare. The full plate becomes a desktop-only "power view."

---

## 1. Many-input forms on mobile (sequencing 17 weighted questions)

**The core tension.** Two research streams point in slightly different directions and the resolution matters for this tool.

- **One-thing-per-page / conversational forms convert better, up to a limit.** GOV.UK's foundational pattern is one question per page: it "helps users understand what you're asking them to do, and focus on the specific question and its answer" and it "work[s] well on mobile devices" and is "better at handling things like errors, branches, loops and saving progress" (https://design-system.service.gov.uk/patterns/question-pages/, https://designnotes.blog.gov.uk/2015/07/03/one-thing-per-page/). Typeform-style single-question flows report completion around 47% vs a ~21% industry average, and multi-step forms are credited with large conversion lifts because each screen "isolates a single decision" (https://rowform.io/blog/single-question-vs-long-forms-the-data-on-why-single-question-forms-win/, https://www.fillout.com/blog/one-question-at-a-time-form).
- **But the effect reverses past ~12-14 questions, and reverses when the steps interact.** The same conversion data warns "a conversational form will usually start hurting conversion rates around the time you pass 12-14 questions, as users may feel the sequential approach becomes tedious." We have 17. And more decisively, NN/g on staged disclosure (wizards): it is "useful when you can divide a task into distinct steps that have little interaction" but "problematic when the steps are interdependent and users must alternate between them" (https://www.nngroup.com/articles/progressive-disclosure/).

**Why the wizard is the wrong default for THIS tool specifically.** The whole point of this tool is that the 17 dimensions trade off against each other and the user tunes them while watching the ranking move. That is the definition of "interdependent steps where users must alternate between them." A strict 17-screen wizard hides the result while the user is answering, which kills the feedback loop that makes the tool fun. So the winning pattern here is **grouped sections, not a 17-step wizard.**

- **Grouping / chunking (the recommended default).** NN/g's cognitive-load work: group related fields so users can "focus on one information category at a time" and it "minimizes context switching between unrelated topics," with "clear, descriptive headings" per section (https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/). The tool already has three natural groups in `Q[]`: **Climate** (winter, summer, snow, sun, smoke), **The place** (size, near-a-city, budget, politics), **Life there** (growth, age, commute, car, jobs, mix, French, mood). Ship those three as collapsible sections, most-important expanded first. Who does it well: GOV.UK allows grouping "a number of related questions on the same page" when research supports it, using a statement heading over the group (https://design-system.service.gov.uk/patterns/question-pages/). Tradeoff: a long-ish scroll, but far fewer taps than 17 screens and it keeps the result reachable.

- **Progressive disclosure of the tail.** Eight of the 17 dimensions ship with weight 0 (car, jobs, mix, french defaults, mood, etc. are "not fussed"/off). NN/g: show core first, defer advanced, which gives "30 to 50 percent faster initial task completion" while keeping the full set discoverable (https://www.nngroup.com/articles/progressive-disclosure/). Concretely: show Climate + The place expanded, collapse "Life there" behind a "More things that matter to you" toggle. Anyone who cares opens it; nobody is forced through 8 low-salience questions.

- **Sequencing rule.** GOV.UK "Continue" button is labelled "Continue" not "Next" and left-aligned "so users do not miss it" (https://design-system.service.gov.uk/patterns/question-pages/). If a stepper is used for the *first-run* only, keep step labels simple ("Question 3 of 9"), avoid heavy progress bars.

**Verdict for the tool:** three collapsible grouped sections on one scrollable "Answer" screen, with the low-weight "Life there" group collapsed by default. Optionally a lightweight first-run overlay that walks a newcomer through the first group, then drops them into the live tool. Do **not** build a strict 17-screen wizard: the steps are interdependent and there are more than 14 of them, both of which the research flags as wizard-failure conditions.

---

## 2. A 20-column comparison table on a 375px screen (the hard one)

Honest headline: **there is no pattern that shows 21 columns x 712 rows well on a phone, and the good design systems say don't try.** NN/g comparison-table research: on mobile "typically only 2 items fit at once," and if you "convert to tabs or lists... these formats weaken compensatory decision-making since users must memorize attributes" (https://www.nngroup.com/articles/comparison-tables/). So the job is to replace the plate with patterns that preserve the *decision*, not the *grid*.

Every real pattern, assessed:

**A. Horizontal scroll with a frozen first column + sticky header (the "keep the table" option).**
- Mechanics: `overflow-x:auto` on the wrapper, `position:sticky; left:0` on the place-name cell, `position:sticky; top:0` on the header row. This is exactly what uxpatterns.dev and NN/g describe (https://uxpatterns.dev/patterns/data-display/table, https://www.nngroup.com/articles/mobile-tables/).
- Does it actually work? Partially, and only with guardrails. NN/g endorses locking headers ("help users know what they are looking at") and locking the left column so users "see the necessary labels at all times." It hard-fails without them (their BestBuy example left users "disoriented when labels disappeared"), and it fails silently if there's no visible scroll affordance: "it must be apparent that there is more data beyond the horizontal fold" via arrows or a cut-off element (dots "are typically harder for users to notice"). Do **not** solve it by forcing rotation: "what you gain in column space, you lose in row space... an annoyance to users if you dictate how they must hold their phone."
- Verdict: acceptable only as a secondary "see the full grid" power view for people who pinned a few places. Useless as the primary browse surface for 712 rows and 21 columns. Honest answer to "is horizontal scroll fine?": it is *tolerable for a handful of pinned rows with sticky name + sticky header + a visible scroll cue*, and a *known failure* if you dump the whole plate into it.

**B. Card-per-row (each place becomes a stacked card). The recommended primary browse.**
- Mechanics: each row collapses to a card. The most-identifying field becomes the card title, actions/links go top-right, remaining fields stack underneath as label/value pairs (https://medium.com/design-bootcamp/designing-user-friendly-data-tables-for-mobile-devices-c470c82403ad). For this tool the card title is the place name + province, the hero value is the fit score, and instead of dumping all 17 values you surface the 2-3 that drove the score (the tool already computes `good`/`bad`/`parts` per place). CSS-only version: media query flips `table`/`tr`/`td` to `display:block` and uses `td::before{content:attr(data-label)}` for the labels (https://uxpatterns.dev/patterns/data-display/table).
- Tradeoff (stated plainly by the sources): "users cannot view as many records simultaneously above the page fold," so cards are weak for side-by-side comparison and strong for scanning one record at a time (https://medium.com/design-bootcamp/...). That is the right tradeoff here because browsing 712 is a scanning task, and comparison is handled separately (pattern F).
- Who does it well: every mobile CRM/list and, conceptually, the search-result rows in Zillow/Airbnb.

**C. Priority columns (show 2-3, expand for the rest).**
- Mechanics: render only the highest-signal columns, hide the rest behind a per-row expand (accordion) or a global column toggle (https://uxpatterns.dev/patterns/data-display/table). NN/g validates user-chosen columns: Dell lets users pick "product specifications of most interest to them via a menu" (https://www.nngroup.com/articles/mobile-tables/).
- For this tool the priority columns are dynamic and already known: the dimensions the user weighted highest. Show those as chips on each card; the rest live in the detail sheet.
- Tradeoff: hidden data needs an extra tap and users may miss a field; fine when the shown columns are the ones the user said they care about.

**D. Transpose (columns become rows) via a detail sheet. Already half-built.**
- Mechanics: for a single place, flip the 21 columns into 21 labelled rows in a scrollable sheet. The tool's `detailHTML` already does this (Climate block, The place block, What residents say block). NN/g: present a single record in a "nonmodal panel" that "still allow[s] users access to the table data" (https://www.nngroup.com/articles/data-tables/).
- Tradeoff: one place at a time, no cross-place comparison in this view. That is correct for "tell me everything about this one place."

**E. Accordion grouping of attributes.**
- NN/g cites Samsung grouping attributes by category so users "see an overview of the type of data that's available" and expand what they want (https://www.nngroup.com/articles/mobile-tables/). Maps cleanly onto the existing Climate / The place / Life there grouping inside the detail sheet.

**F. Compare tray / pin-to-compare (the real answer to "comparison on mobile").**
- Mechanics: a persistent "compare" affordance. User taps a star/checkbox on up to ~3-4 cards; a small bottom bar shows "Compare (3)"; tapping opens a focused view of just those places, transposed (attributes down the left, the 2-3 pinned places across the top), with a **highlight-differences** toggle. This directly follows NN/g comparison guidance: narrow to <=5 first, then compare, and "make disparities obvious" (Best Buy's "Highlight Differences" switch shows differences in yellow) (https://www.nngroup.com/articles/comparison-tables/). Best Buy, Apple (watch comparison), and Tesla are the cited exemplars.
- Tradeoff: an extra interaction model to build, but it is the only way to get honest comparison on a phone, and it is *better* UX than the desktop plate because it compares the few places the user actually cares about instead of 712.

**What does NOT work (be honest):**
- Dumping all 21 columns into a horizontal-scroll container as the main view. Known failure (NN/g: only ~2 columns visible, comparison collapses).
- Forcing landscape rotation (NN/g explicit anti-pattern).
- Tiny cells to cram more columns: violates touch-target minimums (section 5) and is unreadable.

**Recommended stack for this tool:** ranked **cards** (B) with dynamic **priority chips** (C) as the browse surface -> tap opens a **transposed detail sheet** (D + E) -> a **pin-to-compare tray** (F) for side-by-side -> keep the full **frozen-column horizontal table** (A) as a desktop-only / "full grid" opt-in.

---

## 3. Separate pages/routes vs one page with views (single self-contained HTML file)

Constraint: one HTML file, no framework, no router, hash already carries shareable state. So "separate pages" must be simulated.

**Keep two kinds of state strictly separate:**
- **Answer state** = the survey values + weights. This is what people share. Leave it exactly where it is: `location.hash` via `encodeState`/`decodeState`. Do not touch the sharing contract.
- **View state** = which mobile screen is showing (Answer / Map / List / a detail sheet). This is ephemeral UI, nobody shares "I was looking at the map tab." Drive it with a class/`data-view` attribute on a container and CSS, **not** the URL.

**Mechanics that fit a single file:**

- **CSS-only responsive disclosure (the backbone).** One DOM, two layouts. Desktop keeps survey + map + plate visible together. Below a breakpoint (~760px), a bottom tab bar toggles `data-view="answer|map|list"` on the root and CSS shows exactly one panel. This is the cleanest way to "be one page on desktop, separate screens on mobile" with zero routing. The desktop experience is untouched.
- **Bottom tab bar for the top-level screens.** NN/g: tab bars "are well suited for sites with relatively few navigation options," best with ~4-5 max, and placing them at the bottom follows iOS convention (https://www.nngroup.com/articles/mobile-navigation-patterns/). We have exactly three top-level screens (Answer, Map, List), which is ideal. Avoid a hamburger: NN/g and the reachability literature note hidden menus reduce discoverability and cost an extra tap, and bottom tabs "sit in the safest zone for one-handed use" (https://www.nngroup.com/articles/mobile-navigation-patterns/, https://uxplanet.org/one-handed-use-of-tab-bar-bottom-navigation-best-practices-for-reachability-73376377444b).
- **`history.pushState` only for the detail/compare sheet.** So the Android hardware back button and the iOS back-swipe close the sheet instead of leaving the page. On open: `history.pushState({sheet:id}, '')`; on `popstate`: close the sheet. Crucially, push a state object without changing the path or hash (`pushState(state, '', location.href)`) so the shareable hash is preserved byte-for-byte. This gives "route-like" back behavior with no router and no broken share links.
- **Do not use path-based routes** (`/map`, `/list`). A single static file served from `file://` or a plain host has no server-side routing; path routes would 404 on refresh and complicate sharing. Hash is already taken by answer state. `data-view` + `pushState`-for-sheets is the correct, boring solution.

Guidance summary: **bottom tabs beat hamburger for a 3-view tool** (discoverability + thumb reach); primary navigation should be visible, not hidden (https://www.nngroup.com/articles/mobile-navigation-patterns/).

---

## 4. Map + list + filters on mobile (what Zillow / Airbnb / Redfin actually do)

**The dominant pattern is one of two, and both are worth offering:**

**Pattern 1: Map with a draggable bottom sheet of results (Airbnb / Google Maps / Apple Maps).**
- Mechanics: full-bleed map fills the screen; a **non-modal** bottom sheet of results sits over it and drags between snap points (peek / half / full). Because it is non-modal, the map behind stays interactive. LogRocket describes exactly this: "Use a non-modal bottom sheet when the bottom sheet needs to be paired with the main document (think: mobile Google Maps when the 'place' bottom sheet is paired with the main document that shows its location on the map)" (https://blog.logrocket.com/ux-design/bottom-sheets-optimized-ux/). The sheet needs a visible **drag handle** (a horizontal grab bar) or "users might assume that it's not resizable." Apple's equivalent is a sheet with **detents** (medium/large) and a grabber (https://developer.apple.com/design/human-interface-guidelines/sheets).
- Snap-point caution: LogRocket warns against too-clever snapping ("there aren't any visual cues to communicate what's going to happen"). Use 2-3 clear detents (peek showing the top result, half, full-list), not continuous magnetism.
- Selecting a card highlights its pin and vice-versa (spatial sync). Google Maps' persistent sheet "cannot be fully dismissed" but drags up/down (https://mobbin.com/glossary/bottom-sheet).

**Pattern 2: Toggle between full map and full list (Zillow split-view lineage).**
- Mechanics: Zillow's mobile standard is "map on top and listings below... As users move the map, the list updates automatically," with "sticky filter bars... [so] users can adjust price or home type without leaving the map view" (https://raw.studio/blog/using-maps-as-the-core-ux-in-real-estate-platforms/). On smaller phones this often degrades to a **floating "List/Map" switch button** that flips between a full-screen map and a full-screen list.
- Selecting a listing highlights its pin; panning the map re-filters the list (no search button).

**Which for this tool:** the tool's map is a *result visualization* (dots shaded by fit), not a primary filter surface (filtering is the survey). So the cheapest correct move is **Pattern 2 with the bottom tab bar doing the toggle** (Map tab vs List tab), and let a tap on a map dot open the same detail sheet the list uses. If you want the premium feel later, upgrade the Map tab to **Pattern 1**: keep the map full-screen and float a draggable "Top matches" bottom sheet over it (peek = #1 result, drag up = ranked list), tapping a dot expands its card. Both reuse the existing `detailHTML` sheet, so it's one detail component shared across map and list.

Filters (the survey) should be reachable from map/list without losing place, e.g. a sticky "Adjust answers" button that jumps to the Answer tab, mirroring Zillow's "sticky filter bars" so users "adjust... without leaving the map view."

---

## 5. Bottom sheets, thumb reach, tap targets (the ergonomic rules)

**Minimum tap targets (cite these directly):**
- Apple HIG: **44x44 pt** minimum (~59px) (https://blog.logrocket.com/ux-design/all-accessible-touch-target-sizes/).
- Material Design: **48x48 dp** minimum (https://www.nngroup.com/articles/mobile-tables/ references 44x44px; Material's own figure is 48dp; https://m2.material.io/develop/web/supporting/touch-target).
- WCAG: **2.5.8 (AA) = 24px** minimum, **2.5.5 (AAA) = 44px**. Practical rule from the source: "Nothing clickable should be smaller than a square of 24px," but "aiming for 48px can't hurt and will be compliant with every design system" (https://blog.logrocket.com/ux-design/all-accessible-touch-target-sizes/).
- Spacing: keep clear space between targets so users don't hit the wrong one; LogRocket's bottom-sheet piece cites "44x48px touch targets with minimum 8px spacing" (https://blog.logrocket.com/ux-design/bottom-sheets-optimized-ux/).

**Direct implication for this tool:** the weight ticks and option buttons in the survey are small on desktop. On mobile every `.tick`, `.opt`, and slider thumb must be >=44px (target 48px) with >=8px gaps. The 1/3/9 weight control (three tiny boxes) is the biggest offender and needs enlarging or a segmented redesign.

**Thumb zone / reachability:**
- The bottom of the screen is the natural one-handed thumb zone; top corners are the hardest to reach on tall phones. Bottom navigation "sits in the safest zone for one-handed use" (https://uxplanet.org/one-handed-use-of-tab-bar-bottom-navigation-best-practices-for-reachability-73376377444b, https://www.nngroup.com/articles/mobile-navigation-patterns/).
- Therefore: **primary actions and navigation go to the bottom.** The tab bar (Answer/Map/List), the "Compare (n)" tray, the sheet's primary button, and the "Send this to someone" share action all belong at the bottom. Top of screen is for the title/verdict (read, not tapped).

**Bottom sheet mechanics to build:**
- Non-modal for map pairing (map stays live behind), modal (with a dimmed scrim) only for a focused single-place detail or the compare view. LogRocket: modal sheets render the page "inert with a translucent backdrop"; use them "for focused tasks requiring full user attention" (https://blog.logrocket.com/ux-design/bottom-sheets-optimized-ux/).
- Always show a **drag handle**; without it users don't know it resizes.
- Use 2-3 explicit **detents/snap points** (peek / half / full), not continuous snapping.
- Don't make the scrim dismiss-on-tap if there's unsaved intent; the source warns dismissible scrims "cause accidental closures and data loss." For a read-only detail sheet, tap-scrim-to-close is fine.
- Sheets are preferred over a whole new screen for "simple, low-density content"; for dense flows, prefer paged navigation (LogRocket notes some famous bottom sheets "switched to a more traditional paged navigation flow").

---

## Source list (opened and read)

1. NN/g, Mobile Navigation Patterns. https://www.nngroup.com/articles/mobile-navigation-patterns/
2. NN/g, Mobile Tables: Comparisons and Other Data Tables. https://www.nngroup.com/articles/mobile-tables/
3. NN/g, Comparison Tables for Products, Services, and Features. https://www.nngroup.com/articles/comparison-tables/
4. NN/g, Data Tables: Four Major User Tasks. https://www.nngroup.com/articles/data-tables/
5. NN/g, Progressive Disclosure (incl. staged disclosure / wizards). https://www.nngroup.com/articles/progressive-disclosure/
6. NN/g, Few Guesses, More Success: 4 Principles to Reduce Cognitive Load in Forms. https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/
7. GOV.UK Design System, Question pages. https://design-system.service.gov.uk/patterns/question-pages/
8. GOV.UK blog, One thing per page. https://designnotes.blog.gov.uk/2015/07/03/one-thing-per-page/
9. UX Patterns for Developers, Data Table pattern. https://uxpatterns.dev/patterns/data-display/table
10. Design Bootcamp (Medium), Designing user-friendly data tables for mobile. https://medium.com/design-bootcamp/designing-user-friendly-data-tables-for-mobile-devices-c470c82403ad
11. Raw.Studio, Using Maps as the Core UX in Real Estate Platforms (Zillow split view). https://raw.studio/blog/using-maps-as-the-core-ux-in-real-estate-platforms/
12. LogRocket, How to design bottom sheets for optimized UX. https://blog.logrocket.com/ux-design/bottom-sheets-optimized-ux/
13. LogRocket, All accessible touch target sizes. https://blog.logrocket.com/ux-design/all-accessible-touch-target-sizes/
14. UX Planet, One-handed use of tab bar / bottom navigation (reachability). https://uxplanet.org/one-handed-use-of-tab-bar-bottom-navigation-best-practices-for-reachability-73376377444b
15. Single-question vs long forms, the data (Typeform/conversion figures). https://rowform.io/blog/single-question-vs-long-forms-the-data-on-why-single-question-forms-win/
16. Fillout, One-question-at-a-time vs single-page forms. https://www.fillout.com/blog/one-question-at-a-time-form
17. Apple HIG, Sheets (detents/grabber; JS-rendered, general HIG guidance). https://developer.apple.com/design/human-interface-guidelines/sheets
18. Material Design, Touch target (48dp). https://m2.material.io/develop/web/supporting/touch-target
19. Mobbin, Bottom Sheet glossary (Google Maps persistent sheet). https://mobbin.com/glossary/bottom-sheet
