# Usability test — "Where to live in Canada"

Persona: 29-year-old remote software worker in Toronto, tech-savvy, impatient with jank, priced out of the city. Wants: affordable housing (big deal), a growing (not dying) place, some scene/diversity (not all-retiree), tolerable winter, near-ish a city.

URL: https://rohamghiasicw-star.github.io/where-to-live-canada/
Viewport: window set to 1280w (renders ~1470 CSS px inner). Desktop.

---

## 1. First impression (skeptic hat on)

- Loads instantly. Static GitHub Pages page, no spinner, no cookie banner, no email-wall. Good start.
- Does NOT read as AI-generic. Editorial/newsroom feel: giant bold "Where to live in Canada", a short manifesto ("Every best-places-to-list picks the weights for you. This one asks what you want."), and a live computed answer up top ("You should live in Woodstock, ON — It gets you the drive and the winter. You give up the sun.").
- Nice crafted touches: the answer writes a sentence about tradeoffs, names near-ties ("Nearly the same on your answers: St. Thomas, Salaberry-de-Valleyfield. What separates them is the sun."), and there's a "Send this to someone" share button. The URL hash encodes my exact answers (`#-5.2_20.1_...`), so state is shareable. That's a real product decision, not boilerplate.
- Right-hand meta column states provenance up front: 712 places, Census 2021, Climate 1981-2010, Smoke 2013-2024, Votes 2025. Reads like someone who cares about data honesty.
- Methodology footer is unusually candid: weighted power mean (so you can't fail your top priority and still win), Revelstoke's snow station is 43km away and 1,431m up a mountain so its 1,388cm is "alpine snowpack, not the town", Indian reserves deliberately excluded. This is craft, not a template.

Skeptic note: 16 sliders is a LOT to land on a first-time user. No onboarding beyond the numbered list. But the defaults are pre-filled and an answer is already showing, so it's explorable.

## 2. The task — crank Housing budget low + cost matters a lot

- State lives in the URL hash as `value.weight` pairs (weight 0=Skip,1=A little,2=Matters,3=A lot). Clean, shareable, and it updated instantly on every click. No lag.
- Set Housing budget weight to "A lot": one click, hash flipped `600.2`→`600.3` immediately. Snappy.
- Dragged the budget slider from $600k down: it landed on $425k (`425.3`). Slider is smooth, value/label update live while dragging. Precise landing is a little fiddly (a drag from x=90→66 jumped $600k→$425k, ~$175k in 24px) — fine-grained values need a careful hand, but the persona doesn't need pixel precision. No jank.
- Result: top answer changed from Woodstock ON to **Salaberry-de-Valleyfield, QC** — "It gets you the price and the size." Near-ties: Saint-Jérôme, Cornwall ("What separates them is the short commute"). The narrative sentence correctly re-wrote itself to talk about price/size. Nice.
- HONEST persona reaction: Salaberry is a 94%-French town, home value ~$291k. It's exactly what I typed (cheap + small city + mild-ish winter) but it's not where an anglo Toronto dev wants to land. The tool answers the literal question, not the unspoken one. That's fair, but it means I have to actually encode "diversity / younger / near a city" myself.

### WAIT-WHAT #1: the "clears your dealbreakers" count moved when I only changed a weight
- At budget = Matters/$600k the footer said "670 of 712 clear your dealbreakers." After budget = A lot/$425k it said "605 of 712." I never set an explicit dealbreaker.
- Best guess: with the power-mean, weighting budget "A lot" makes any place far above $425k catastrophically fail that one axis, so it drops below the "cleared" threshold. Confirmed later: Toronto and Vancouver show Fit = "—" (disqualified) because their home values ($1.13M / $1.73M) blow the $425k budget I weighted A lot. So "dealbreakers" = places that catastrophically fail a heavily-weighted axis. Defensible and matches the footer's "can't fail the thing you care most about and win anyway," but the word "dealbreakers" is confusing when the user never explicitly toggled one (only Wildfire smoke has a literal "Dealbreaker" button). Minor clarity flag.

## 3. The 21-column table

Columns: (rank) Place, Fit, Jan, Jul, Snow, Sun, Smoke, People, Drive, Home, Lean, Growth, Age, Short, Carfree, Unemp, Diverse, French, Mood, (provenance).

- Columns I weighted are tinted green; Skipped ones go gray. Nice, immediate visual mapping of "what's driving the ranking."
- **Sorting: NOT sortable.** Clicking a column header does nothing (I clicked "Home" — order unchanged). The only re-ranking lever is the weights on the left. Philosophically consistent (the Fit ranking is the product) but a data-savvy user who wants "sort by cheapest" or "sort by growth" can't. Friction for my persona.
- **Header tooltips are native `title` attributes**, not custom UI. That's why nothing showed in a screenshot on hover (native titles have a ~1s delay, don't render in captures, don't work on touch, aren't keyboard-accessible). They DO work for a real mouse user and the copy is good, but for a page this crafted it's the low-effort route. Full tooltip text (all accurate/clear):
  - Jan/Jul: avg Jan/Jul temp °C, ECCC normals 1981-2010
  - Snow: snow/yr cm · Sun: bright sunshine h/yr · Smoke: wildfire PM µg/m³, FireWork model
  - People: population (2021 Census) · Drive: minutes to nearest metro >300k, routed on real roads
  - Home: avg self-estimated home value 2021 · Lean: riding lean −100 left..+100 right, 2025
  - Growth: pop change 2016→2021 · Age: median age · Short: % commuting <15 min
  - Carfree: % transit/foot/bike · Unemp: unemployment % 2021 · Diverse: % immigrants · French: % French first language
  - Mood: resident sentiment −2..+2 from forums/news/blogs, only where researched
- **Abbreviations hard to guess WITHOUT the tooltip:** "Short" (=short-commute %), "Mood" (=sentiment, mostly ".." unresearched), "Carfree", "Lean", and "People" (just population, but sits beside a count so reads ambiguous). Everything else is guessable.
- **Compare 3 places** (my candidate shortlist across columns):
  - Airdrie AB: Jan −7.1 / Home $418k / Growth +20.3% / Age 36 / Diverse 17% / Carfree 5% / Drive 30m to Calgary
  - Halifax NS: Jan −4.1 / Home $404k / Growth +9.1% / Age 40 / Diverse 12% / Carfree 16% / Drive "here"
  - Québec QC: Jan −12.8 / Home $327k / Growth +3.3% / Age 43 / Diverse 9% / French 96% / Carfree 20%
  - Reads cleanly across the row; the green tint makes it easy to see which cells earned the rank. Airdrie wins on growth+youth, Halifax on being an actual city under budget with mild winter, Québec on price but brutal winter + French wall.

## 4. Detail panel (opened Salaberry + Windsor)

- Row click expands an inline panel: monthly temp bar chart (blue cold / orange warm), a Climate block (Snow, Precip, Sun, Days below −20, Wildfire smoke) with the **exact weather station used and how far off it is** ("From ORMSTOWN, 16.7km away, 4m elevation diff" / "From WINDSOR A, 2.2km, 0m"), and a "The place" block (People, Home avg, Rent+utilities, Median income, Unemployment, Nearest city, Riding, Lean). Plus a "What residents say" note.
- **LAYOUT BUG (repeatable):** at 1280/1512 width the panel's right-hand "The place" column is cut off past the viewport edge — I can see the labels (People, Home, Rent, Income, Riding, Lean) but the VALUES are off-screen right. To read them the user must horizontally scroll the very wide table. Happened for both Salaberry and Windsor. On a lead-in feature (the detail panel) this is a real miss on a standard laptop.
- Salaberry values (read via DOM): People 43k, Home $291k, Rent+utilities $730/mo, Median income $62k, Unemp .., Nearest Montreal 60min, Riding named in full, Lean "swing," Residents "Not researched... 28 of 129 places are done."

## 5. Numbers sanity-check (places I know)

RIGHT (real ECCC/Census data, strong confidence):
- Toronto Jan −3.7 / Jul 22.3 / Snow 122cm / Home $1.13M — accurate
- Vancouver Jan 4.1 / Jul 18.0 / Snow 38cm / Home $1.73M / Smoke 0.94 (>Toronto) — accurate
- Yellowknife Jan −25.6 · Winnipeg −16.4 · Saskatoon −15.4 · Calgary −7.1 w/ 2396h sun — all accurate
- Windsor: Jul 23.0 (warmest CA summer), Days below −20 = 1 (correct, southernmost city)
- Halifax Jan −4.1 / Home $404k — plausible
- Montréal Diverse 33% immigrants / French 63% / Carfree 41% — accurate

SUSPICIOUS / WRONG:
- **Tsawwassen BC "Growth +176.5%"** — jarring outlier (likely the Tsawwassen First Nation CSD's real post-2016 build-out, but it looks broken). Worse: its **Home value is ".." (missing)** yet it ranks #2 in my persona run. Because the app "drops missing values rather than guessing," a place missing the exact field I weighted "A lot" (budget) can't fail that test and floats up unfairly. Real scoring weakness.
- **"28 of 129" vs "71 of 712" researched** — the slider blurb + detail panel say "28 of 129 places are researched," the footer says "researched for 71 of 712 places." Two different counts for the same concept. Internal inconsistency in a product whose whole pitch is data honesty.
- **Unemployment reads high everywhere** — Toronto 13.9%, Niagara Falls 22.5%, Windsor 18.9%. That's the COVID-era May-2021 Census. Disclosed (tooltip says "2021"), but a casual user reads these as current and gets a wrong impression.
- **Halifax "catch" ER-closure claim dated exactly today (July 17, 2026)** — cites 13 specific NS EDs closed, names real facilities. Impressive texture IF accurate, but it's hyper-specific, unverifiable from the page, has no inline source link, and the date matching "today" is a skeptic red flag (real fresh data, or a template inserting today's date?).
- Vancouver Lean "+0" (neutral) — mildly surprising for a left-leaning city; defensible as vote-weighted across mixed ridings, not clearly wrong.

## 6. "Matters a lot" dominance + contradiction test

- **Does "A lot" dominate? Yes.** Budget A lot at $425k disqualified Toronto/Vancouver (Fit "—") and flipped the entire top of the list to sub-$450k towns. The "A lot = 9× A little" power-mean claim holds up in behavior.
- **Contradiction (Big city + $425k, both A lot):** handled gracefully, NOT garbage. Winner = Halifax (Fit 68, $404k real city under budget), then Edmonton/Calgary/Québec/Winnipeg. Top Fit dropped 80→68, a subtle "nothing's perfect" signal. It does NOT explicitly say "these two conflict" — it just picks the best compromise and names what you give up ("You give up the short commute"). An ideal UX might call out the tension outright, but this is honest and sensible.

## 7. State / sharing / performance

- State encoded in URL hash as value.weight pairs. Only 3 sliders (Winter/Summer/Budget); everything else is button-groups.
- **Share works on fresh load:** opening a shared link reframes copy to "Someone sent you their answers... Change anything and it becomes yours" and header to "They should live in [place]." Thoughtful.
- Quirk: the app reads the hash only on initial load; it does NOT respond to in-session `hashchange`. Fine for real users (share always opens fresh) but worth knowing.
- Performance: buttons and slider update the answer/table/map instantly, no lag, even on 712 rows. Smooth.

## 8. Gaps for the remote-worker persona specifically

- **No internet / broadband column.** For the exact audience this tool attracts (remote workers deciding where to move), missing connectivity data is a real gap.
- The winners it hands a young remote dev (Salaberry 94% French; Airdrie car-dependent Calgary exurb, Carfree 5%) satisfy the numbers I entered but not the unspoken "somewhere with a scene." The tool answers literally; it can't capture vibe. Fair, but the persona would leave slightly unsatisfied.

## VERDICT

Top 5 problems (ranked):
1. Detail-panel right column ("The place": Home/Rent/Income/Riding/Lean values) is cut off past the viewport at normal laptop width (1280–1512). Repeatable on every place. The cost data — arguably the #1 thing a mover wants — is the part that gets clipped.
2. Missing-data places game the ranking: Tsawwassen ranks #2 in my persona run with a blank Home value while budget was my top "A lot" weight, because missing values are dropped rather than penalized. Combined with its +176.5% growth outlier, it looks broken and erodes trust.
3. Internal inconsistency in the "residents researched" count: "28 of 129" (sidebar + detail) vs "71 of 712" (footer). Bad look for a data-integrity product.
4. Table isn't sortable by column, and header tooltips are native `title` only (slow, no touch, no keyboard) — both limit the "read the table for why / hover any heading" promise the intro makes.
5. Unemployment is COVID-era 2021 Census (Toronto 13.9%, Niagara 22.5%) shown without an inline "this is 2021, it was a weird year" nudge; and no internet/broadband column for the remote-worker audience.

2 things I liked:
1. The honesty and craft: exact weather station + distance/elevation per place, Revelstoke alpine-snow caveat, reserves excluded on purpose, weighted power mean so you can't fail your top priority and still win, and a live narrative answer that rewrites itself ("It gets you the price and the size. You give up the sun."). This is not template output.
2. The whole interaction model: instant re-ranking with zero lag on 712 rows, shareable URL state that reframes to "someone sent you their answers," near-tie callouts ("what separates them is the sun"), and a genuinely smart handling of a contradictory profile (Halifax as cheapest real city, Fit capped at 68).

Numbers that looked WRONG/suspicious (this mattered most):
- Tsawwassen +176.5% growth AND ranked #2 with a MISSING home value — biggest red flag.
- "28 of 129" vs "71 of 712" researched — contradictory.
- Halifax "catch": 13 ER closures dated exactly today (2026-07-17), hyper-specific, no source link, unverifiable.
- Unemployment inflated by 2021-COVID vintage across the board.
- (Everything I could actually check — Toronto/Vancouver/Yellowknife/Winnipeg/Windsor/Calgary climate + home values — was accurate. The real data is legit; the suspicious stuff is edge/outlier/derived.)

Human-crafted or AI-generic? Emphatically human-crafted. The voice, the data caveats, the self-aware "it is a way to argue with a list," the per-place narrative, and the deliberate design choices (power mean, station provenance, reserves excluded) are the opposite of generic. The rough edges are craft-project rough edges (a cut-off panel, native tooltips, a count typo), not AI-slop rough edges.
