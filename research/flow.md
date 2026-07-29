# Flow research: rebuilding the tool as pick → answer → result

Brief: the current build shows a 23-tile picker, the answers, the verdict, a search box, a map, ranked cards **and** a 23-column table on one scrolling page. Owner's verdict: "too confusing." Target: step 1 pick (max 5), step 2 one question per screen, step 3 one big result, with map + table behind an "explore" view.

Scope note: this file is about **flow only**. Colour/type/palette live in `ai-tells.md`, `design-refs.md`, `type.md`. Mobile ergonomics (tap targets, bottom sheets, tab bars) live in `mobile.md` and are not re-litigated here — except where this restructure **contradicts** `mobile.md`, which it does in one important place (see §0).

Verification key: **[V]** = I opened the URL and read it. **[S]** = came from a search-result summary I could not open (403 / JS shell) — flagged, weaker. **[U]** = could not verify at all.

---

## 0. THE CONTRADICTION WITH EXISTING RESEARCH — read this first

`research/mobile.md` §1 ends with an explicit verdict:

> "Do **not** build a strict 17-screen wizard: the steps are interdependent and there are more than 14 of them, both of which the research flags as wizard-failure conditions."

**That verdict was correct for the tool it was written about, and it does not apply to the tool being built now.** Both of its failure conditions are removed by the new design, not argued away:

1. **"More than 14 questions."** The threshold `mobile.md` cites is the conversational-form ceiling at ~12-14 questions. The new flow caps the user at **5**. Five is not near the ceiling; it is a third of it. The 17-question objection dies with the 17 questions.
2. **"The steps are interdependent."** This one needs care, because it is the deeper objection. NN/g's staged-disclosure caution is that wizards are "problematic when the steps are interdependent and users must alternate between them" (https://www.nngroup.com/articles/progressive-disclosure/, cited in `mobile.md` [V via mobile.md]). In the 17-dimension build the interdependence was real: every dimension competed with every other for weight, so tuning meant alternating. **In the new build the interdependence is resolved once, in step 1, by the pick order.** You choose five things and rank them by choosing them. After that, each question is about one thing only and does not trade against its neighbours. The interdependent decision has been extracted out of the sequence and given its own screen.

So: **`mobile.md`'s anti-wizard verdict is superseded, on its own stated grounds.** What survives from `mobile.md` unchanged and should be carried forward: card-per-row browse, dynamic priority chips, transposed detail sheet, pin-to-compare, full grid as an opt-in power view, bottom tabs over hamburger, 44-48px targets, `data-view` for view state with the answer hash untouched. Nothing in this file overrides any of that.

One more inherited item that this restructure makes easier, from `design-refs.md` §2 on the NYT dialect quiz [V via design-refs]: "the map redraws after every single answer… No submit-and-reveal cliff; the result *tightens*." Keep that. A stepped flow does **not** have to mean a hidden result — see §5.

---

## 1. Stepped flows people finish: how many decisions before the first payoff

### The Political Compass — 6 pages, 8 propositions each, "Page 1 of 6" [V]
Opened `https://www.politicalcompass.org/test/en?page=1`. Structure, read off the page:
- **8 propositions per page**, not one.
- **6 pages total**, declared as a literal "**Page 1 of 6**" string at the top of the test section.
- Answer control: 4-point forced choice, **no neutral** — "Strongly disagree / Disagree / Agree / Strongly agree".
- Opening instruction copy, verbatim: *"Just a few propositions to start with, concerning — no less — how you see the country and the world."*
- URL: https://www.politicalcompass.org/test/en?page=1

Two things worth stealing. First, **the progress indicator is a sentence, not a bar** — "Page 1 of 6" is text, and it costs nothing, cannot mislead, and reads as editorial rather than as app chrome. Second, the **first screen is explicitly framed as small** ("just a few propositions to start with"). It sets the expectation that the ask is light before asking anything.

And a caution against over-reading "one question per screen": the most-forwarded political quiz on the internet puts **eight** on a page and is fine. The count per screen matters less than the *count of screens* and whether each screen is one **kind** of decision.

Also relevant to the owner's complaint: Political Compass' own guidance on the questions is *"Your responses should not be overthought. Some of them are intentionally vague. Their purpose is to trigger reactions in the mind, measuring feelings and prejudices rather than detailed opinions on policy."* (https://www.politicalcompass.org/test [V]). That is permission to write the questions loose and fast. A tool that ranks 710 towns on Environment Canada normals will be tempted to write precise, hedged questions. Precise questions are slow questions.

### The NYT dialect quiz — the reduction *is* the design [V]
Knight Lab's interview with Josh Katz (https://knightlab.northwestern.edu/2014/01/20/behind-the-dialect-map-interactive-how-an-intern-created-the-new-york-times-most-popular-piece-of-content-in-2013/ [V]):
- Katz started from the **122-question Harvard Dialect Survey**, added ~20 of his own for "more than 140 questions," then cut nearly all of them for the published quiz.
- The cut rule was **discriminative power, not coverage**. Verbatim: *"Pancakes or flapjacks? Everyone says pancakes, Katz said. So that question and about 120 others were thrown out."*
- Why it landed, in his words: *"Dialect is all about people's sense of identity — 'this is who I am, this is where I come from.'"* And the unplanned payoff: *"For a lot of people the quiz will show them where their parents grew up."*
- It became the NYT's most popular content of 2013. Knight Lab's closing note on why: *"At the end of the day it's fun."*
- ⚠️ The Knight Lab piece does **not** state the final question count and does **not** say whether the map updated live. The "25 questions" figure and the live-redraw behaviour are attested elsewhere (`design-refs.md` §2 records the live redraw as [V] from reading the interactive itself; the 25 figure appears in secondary write-ups such as https://languagelog.ldc.upenn.edu/nll/?p=9252 [S]). Treat "25" as secondary-sourced.

**The transferable rule: cut every question that everyone answers the same way.** For this app that is a live and specific test. A question where 700 of 710 towns score identically is a pancakes question — it costs the user a screen and moves the ranking by nothing. Any of the 23 dimensions whose distribution across the 710 is nearly flat should be *ineligible for the picker*, not merely deprioritised. This is a data check somebody can actually run, and it is the single highest-leverage cut available: it shortens the flow without removing any real choice.

**And Katz's identity line is the frame for the whole app.** "This is who I am, this is where I come from" is why a dialect quiz outperformed every news story that year. A tool that says *where you should live* has the same engine available and should be written in the second person throughout, about the reader, not about the dataset. `design-refs.md` §2 already flags this ("Opening line is a question about **you**, not about the dataset") — the stepped flow is what makes it structurally true rather than a headline.

### Progress indicators and abandonment — the numbers, and how much to trust them
Search surfaced a consistent set of figures, but the sourcing is weak and I am flagging it hard:
- "A B2B company added 'Step X of 4' to their lead form, and completion rate increased from **32% to 41%**"; "Forms with conditional logic and conversational (one-question-per-screen) modes see **15-25% higher completion**"; "multi-page forms with one question per step convert **86% higher** than single-step"; "multi-step forms outperformed equivalent single-page forms by **296%** on average… lifts as high as **412%**"; and, usefully, "**per-step completion rates typically improve as users advance** — step four of a five-step form shows higher completion than step one, because the finish line is visible."
- These came from a search summary over https://heyflow.com/blog/reduce-form-abandonment-progress-indicators/, https://formflux.io/blog/form-completion-rates-guide, https://www.amraandelma.com/multi-step-form-abandonment-stats/, https://ivyforms.com/blog/multi-step-forms-single-step-forms/ **[S]**.
- ⚠️ **heyflow.com returned HTTP 403 to WebFetch — I did not open it.** Every one of these sites sells form software, the "296%"/"412%" figures have no named study, and this is exactly the genre of marketing-blog stat that circulates without a primary source. **Do not put any of these numbers in the product or in a pitch.** The only claim here I would build on is the *directional* one that is also independently attested by GOV.UK and NN/g in `mobile.md`: fewer decisions per screen, more screens, is fine — and the drop-off is front-loaded, so the first screen carries almost all the abandonment risk.

**What that means concretely: the first screen is the only screen with a real abandonment problem.** If step 4 of 5 completes better than step 1 because the finish line is visible, then the design effort belongs almost entirely on the landing screen and on making the total ask legible immediately. Everything after screen 1 is downhill.

---

## 2. The result screen: earned and screenshot-worthy, not horoscope-generic

### What actually drives sharing — the named drivers [V]
NFX's inventory of sharing motives (https://www.nfx.com/post/why-people-share [V]) names eight. Three are directly available to this app and five are not, which is a useful filter:

- **Identity projection** — verbatim: *"Sharing an outraged Yelp review or political Facebook post helps us define what we stand against, and by implication what we stand for."* This is the primary engine. A result that says "you are a Kootenay person" is an identity claim the reader can post; a result that says "Nelson BC scored 84.3" is not.
- **Validation** — verbatim, and it is specifically about this genre: *"People shared their results because they wanted to be validated and boost their self-esteem,"* noted as applying to personality assessments.
- **Being helpful** — *"We are compelled to share things that we find useful because we want to be perceived as helpful and nurturing to our tribes."* This is the second engine and the one most people building quizzes forget. A Canadian moving-decision tool has genuine utility; a shareable result that a friend can *use* (not just admire) gets forwarded for a different reason than a personality label does.
- Not available / not worth chasing: Status (nothing scarce here), Safety, Order, Novelty, Voyeurism.

**Design consequence: build for two share motives at once.** The screenshot wants an identity claim. The forward-to-a-friend wants a usable answer. Those are different objects and it is worth shipping both — the top of the result is the identity claim, the bottom is the useful part, and the link carries the state so a friend lands on *your* answer and can immediately re-answer as themselves.

### The academic caution — and it is aimed squarely at this design [V]
Peer-reviewed, *International Journal of Communication*, "Online Quizzes as Viral, Consumption-Based Identities" (https://ijoc.org/index.php/ijoc/article/view/5265 [V]). Abstract, verbatim: identity in these quizzes *"is often circumscribed around digestible, consumption-based 'results.'"* The paper's charge is that BuzzFeed-style quizzes reduce identity to something *digestible* and then monetise it.

Read as a design warning rather than a critique of capitalism, it is the sharpest statement of the failure mode the owner is worried about: **a result becomes generic exactly at the moment it becomes digestible.** So the digestibility has to be paid for. The way the good ones pay for it is by attaching the *evidence* to the label. See below.

### How 16Personalities composes a result [V]
Opened a type page (https://www.16personalities.com/infj-personality [V]). Top-to-bottom order, read off the page:
1. **The code** (INFJ) — the thing you screenshot.
2. **The nickname** ("Advocate") — the identity noun. The code alone is not shareable; the noun is.
3. **A one-sentence tagline**: *"Advocates are quiet visionaries, often serving as inspiring and tireless idealists."*
4. **The four axes spelled out in words** — Introverted, Intuitive, Feeling, Judging. This is the *why*: the label is decomposed back into the four decisions that produced it.
5. **A pull quote** (Goethe) early on the page.
6. Then long-form sections in this order: **Introduction → Strengths & Weaknesses → Romantic Relationships → Friendships → Parenthood → Career Paths → Workplace Habits → Conclusion → Premium Career Suite.**
- ⚠️ I could **not** verify famous-person examples or a rarity percentage on that page; the search summary claimed both ("The Architect" for INTJ, exemplars) [S] but the type page I opened did not show them. The rarity percentage appears on the personal results page, which requires taking the test — **unverified**.
- ⚠️ I could not open `16personalities.com/free-personality-test` (JS shell, WebFetch returned only nav and footer). **The claim "one question per screen with a percentage bar" is something I did not verify.** Do not cite me on 16Personalities' test mechanics.

**The transferable structure is items 1-4, in that order: label → noun → one sentence → the decomposition.** Note that the decomposition comes *fourth*, immediately, on the same screen. The result does not say "trust me"; within one screen it shows the four inputs that made it. That is what stops it reading as a horoscope. `design-refs.md` §2 already found the same move in the dialect quiz ("It shows *your most distinctive answer for each city* — per-item evidence, so you can reject the verdict on the merits").

### The GOV.UK "check answers" pattern — the honest version of the same move [V]
https://design-system.service.gov.uk/patterns/check-answers/ [V]. Verbatim: *"Check answers pages help to increase users' confidence as they can clearly see that they have completed all the sections and that their data has been captured."* Mechanics worth copying exactly:
- Answers are a **summary list** (definition list: label + the user's own answer), grouped into labelled sections.
- **A "Change" link sits next to each row**, and returning to a question must **pre-populate** what they entered. Verbatim: *"The answers pages should look the same way they did when the user last used them"* and users *"should not need to go through the rest of the transaction again."*
- Unanswered optional questions render as **"Not provided"** — missing is printed as missing, which is the same commitment `design-refs.md` §4 draws out of the almanac/provisional-sheet convention.
- Two-thirds column width on desktop, to keep line length readable and keep the action links reachable for screen-magnifier users.

**This is the answer to "where do the user's five answers live on the result screen."** Not in a collapsed panel and not back on the previous step: as a five-row summary list with per-row Change links, directly under the verdict. It doubles as the *why* (these are the five things you said mattered, in your order) and as the edit affordance (change one thing, watch the answer move). It is confidence-building and re-engagement in one component, and it is a boring government pattern rather than a designed-feeling flourish, which is exactly why it will not read as generated.

---

## 3. Progressive disclosure to a data table — including the evidence AGAINST it

### The strongest finding in this whole file, and it cuts against the plan [V]
Datawrapper's own design doctrine (https://www.datawrapper.de/academy/our-explanatory-approach [V]) is built on refusing hidden depth. Verbatim: **"If the content is hidden, readers won't see it."** They quote NYT graphics editor **Archie Tse**: **"If you make a tooltip or rollover, assume no one will ever see it."** Their stated goal is that *"everything important is visible right away, at first glance at the chart,"* and they deliberately **do not offer drop-down menus or tabs** because *"Large portions of your readership may miss huge parts of the dataset entirely."*

Tse's full three rules, from his Malofiej 2016 talk "Why We Are Doing Fewer Interactives" — reported by Nieman Lab (https://www.niemanlab.org/2016/03/at-the-malofiej-infographics-world-summit-the-best-form-of-storytelling-is-often-static/) and Dominikus Baur's write-up (https://medium.com/@dominikus/the-end-of-interactive-visualizations-52c585dcafcb), slides at https://github.com/archietse/malofiej-2016 **[S — I read the search summary and the reporting, not the slides themselves]**:
1. If you make the reader **click or do anything other than scroll**, something spectacular has to happen.
2. If you make a **tooltip or a rollover**, assume that no one will ever see it.
3. If the content is **important for the reader to see, don't hide it.**
His diagnosis: *"Readers just want to scroll."*

**How to hold both truths.** The owner is right that 23 columns on the front page is confusing, and Tse is right that hidden content is unseen content. The reconciliation is that these two statements are about **different content**:
- The **verdict, the why, and the runner-up** are Tse's rule 3 content. They must be on the result screen with no click. Not in a tooltip. Not behind "show details".
- The **23-column table** is not content the general reader needs; it is *proof of work* for the sceptic. It has a small, self-selecting audience that will hunt for it. Tse's rule 1 applies and is satisfiable: clicking through to a full national data table **is** the spectacular thing.
- The tooltip rule is the one to obey literally: **do not put any load-bearing explanation in a hover.** `mobile-audit.md` already found this failing in the live build ("Column headers are hover-only — dead on touch"). Tse and the audit agree.

### How a serious data publisher actually does the front-door-to-raw-numbers walk [V]
Our World in Data grapher page, opened (https://ourworldindata.org/grapher/life-expectancy [V]). The exact labels a reader gets:
- **"Download full data"** (all entities and time points, ZIP) and **"Download displayed data"** (only what is currently selected on screen).
- A **Data API** with CSV and JSON URLs.
- A **"Data sources"** section naming each upstream dataset (Human Mortality Database, UN WPP, Zijdeman et al., Riley).
- A **"How to cite"** section with full and abbreviated citation forms.
- **"Show more" / "Show less"** toggles on the descriptive text.
- ⚠️ I could **not** confirm from the fetched text that the Chart / Map / Table tabs render as tabs — they are client-side. Treat "OWID has a Table tab" as **[U]**. What I *can* attest is the download/source/citation layer above.

**Two things to steal.** First, the **"displayed data" vs "full data" split** — the honest version of an escape hatch: the curious reader gets the exact numbers behind *the thing they were just looking at*, not a firehose. For this app that maps precisely onto "download the five columns you picked, for all 710" vs "download everything." Second, **provenance is a peer of the data, not a footnote** — a named section with the upstream datasets and a citation block. `design-refs.md` §2 already flagged this as the one thing worth stealing from OWID ("every chart is one click from its provenance"). It holds up.

### Disclosure widgets, done plainly [V-ish]
Datawrapper's own mechanism for optional depth is `<details>`/`<summary>` (https://academy.datawrapper.de/article/353-how-to-add-disclosure-widget [S — surfaced in search, not opened]). Note the tension with the house rule already locked in `CLAUDE.md` for the movers site (FAQ `<details>` must ship `open` because collapsed content does not help ranking and cannot be clicked by a crawler or an LLM). **That rule was written for SEO pages and does not automatically transfer to a client-side tool** — but the underlying instinct (collapsed = unseen) is the same instinct Tse and Datawrapper are expressing. Default-open where the content matters; collapse only genuinely optional depth.

---

## 4. Structural AI-slop tells (layout and chrome, not colour)

`ai-tells.md` covers colour, type and the card/hero tells thoroughly. This section adds only what is **structural and specific to a stepped flow**, since that is the new surface being built.

### Named, verbatim, from the inventory [V]
Re-opened https://impeccable.style/slop/ [V] and pulled only the structural entries:
- **"Tiny numbered section labels"** — *"Tiny numbers repeated beside headings imitate editorial structure without adding it."* **This is the exact indictment of "Step 1 / Step 2 / Step 3" chrome.** The tell is not that a flow has steps; it is that the step numbers are printed as decoration in a place where they add no information.
- **"Hero eyebrow / pill chip"** — *"A tiny uppercase letter-spaced label sitting immediately above an oversized hero headline, or the same shape rendered as a pill chip."*
- **"Hero metric layout"** — *"Big number, small label, three supporting stats, gradient accent."* Directly relevant: a result screen whose top is one big score plus three little stats is the named pattern.
- **"Identical card grids"** — *"Same-sized cards with icon + heading + text repeated endlessly."*
- **"Icon tile stacked above heading"** — *"A small rounded-square icon container above a heading is the universal AI feature-card template."*
- **"Nested cards"** — *"Cards inside cards create visual noise and excessive depth."*
- **"Heading crowded against the previous block"** — *"A heading sits closer to the previous block than its own content."* A pure spacing tell; worth a pass over the step screens.
- **"One column stretches the first viewport"** — *"One opening column runs far past its neighbor, leaving dead space."*
- **"Cards flush against the scroller edge"** — *"Scroller cards lose one edge because the panel has no matching inset."*

Corroborating from `ai-tells.md` (already verified there, not re-fetched): Krebs measured *"numbered step sequences"* among his 16 patterns, and Built In names *"three-step onboarding flows with progress dots"* as a signature AI-competent construction. Two independent sources put step chrome and progress dots on the list.

### The structural default, stated plainly [S]
From a search over dev.to and Publishd write-ups on fixing the AI-built look (https://dev.to/alanwest/how-to-fix-the-ai-generated-look-in-your-frontend-1ahh, https://publishd.app/blog/make-ai-built-site-not-look-ai) **[S — search summary; I did not open these two]**: *"AI-generated UI often looks similar because the model reaches for the safest visual structure: centered hero, stacked sections, cards, generic spacing, and predictable grids"*, and the features section is *"a 3-column grid of cards with a tiny icon, heading, and 2 lines of text — the most copy-pasted layout on the internet right now."* Flagged as [S]; the same claims are already [V] in `ai-tells.md` via Krebs and 925studios, so nothing load-bearing rests on these two URLs.

### The specific items the brief asked about, honestly graded
| Pattern asked about | Verdict | Evidence |
|---|---|---|
| **"Step 1 / 2 / 3" chrome** | **Named tell** | impeccable "Tiny numbered section labels" [V]; Krebs "numbered step sequences"; Built In "three-step onboarding flows" (both via `ai-tells.md`) |
| **Progress dots / rings** | **Named for dots. Rings unverified.** | Built In names "progress dots" (via `ai-tells.md`). I searched for **progress rings** specifically and **found no designer discourse naming them** — treat as [U], not cleared, just unattested |
| **Hero + three feature cards** | **Named tell, measured** | Krebs 22% icon-card grids; impeccable "Identical card grids" + "Icon tile stacked above heading" [V] |
| **Centred everything** | **Named tell** | Krebs "centred hero in generic sans"; "the safest visual structure: centered hero, stacked sections" [S] |
| **Gradient CTAs** | **Named tell** | Krebs measured gradient backgrounds at 27%; "gradient accent" is part of impeccable's "Hero metric layout" [V] |
| **Pill buttons** | **Partly.** The *pill chip label* is named; the pill *button* is not | impeccable names the "pill chip" as an eyebrow-label shape [V]. I found **no source naming rounded/pill buttons as an AI tell** on their own — extreme rounding (24px+) is named, buttons specifically are not. [U] |
| **Emoji bullets** | **Named, in a specific form** | Krebs names "sidebar with emoji icons"; `design-refs.md` counted **417** emoji flags and an emoji nav strip on nomads.com as its cleanest "no decision was made" diagnostic [V via design-refs] |

**The honest summary: step numbers, progress dots, three-card rows, centred heroes and gradient CTAs are all attested. Progress rings and pill buttons are not attested — I looked and did not find them.** Avoid them if you like, but do not claim research backing.

### One more piece of concrete step guidance [V]
Setproduct's multi-step UI guide (https://www.setproduct.com/blog/steps-ui-design [V]):
- **"Most effective flows use between 3 and 6 steps. Too few can overwhelm users with dense forms, while too many may feel exhausting."** A 1-to-5 question flow sits inside that band; the current one-page build sits at the "dense form" end it warns about.
- Step count should reflect **logical grouping, not technical requirements**.
- Labels: **"natural language, not internal terms"**; it names *"cryptic labels like 'General' or 'Misc.'"* as an anti-pattern. Never icons alone: *"always include a label."*
- Back/edit: **"Letting users revisit and update previous steps improves trust and reduces drop-off."** But *"Don't allow going forward to a step that hasn't passed validation unless you're intentionally supporting non-linear flows."*
- The anti-pattern that names the current build's likely failure mode if this is done badly, verbatim: **"fake Steps UI, where all the fields are dumped into one giant form with a pretty stepper on top."** A stepper bolted onto the existing scrolling page would be exactly this. The steps have to be real screens.

---

## 5. THE RECOMMENDED FLOW FOR THIS APP

Design rule running through all of it: **one screen answers one question, and every mark on the screen could have come out different.** The second half is the test `design-refs.md` §4 derived from the topographic-sheet work ("could its value have come out different? If no, it's costume"). It is what keeps a stepped flow from turning into "Step 1/2/3" chrome — a step number that is *the reader's own rank* is data; a step number printed because flows have step numbers is decoration.

### Screen 1 — the pick, and literally nothing else

**On screen:**
1. The name of the thing.
2. **One sentence in the second person** that states the whole ask and its size: *"Pick up to five things that matter to you, most important first. Then answer five questions."* (Political Compass' *"just a few propositions to start with"* move — declare that the ask is small *before* asking. This screen carries nearly all the abandonment risk, per §1.)
3. **The tiles.** Not 23 loose tiles — the 23 grouped under 3 or 4 plain nouns (Weather / Money / People / The place), so the eye parses four things rather than twenty-three. Setproduct: labels in natural language, never icon-only.
4. **A number appears on a tile the moment it is picked** — 1, 2, 3, 4, 5. The pick order *is* the weighting, so the number is the reader's data. Unpicked tiles carry no number. Tapping a picked tile removes it and the numbers behind it close up.
5. **One button, bottom, left-aligned, labelled with the count**: "Answer these 3" → "Answer these 5". Dead until there is at least one pick. GOV.UK's rule is that the forward button says "Continue" and is left-aligned "so users do not miss it" (via `mobile.md` [V]); here the count is worth more than the word, because it makes the remaining ask legible on the screen where people quit.

**Not on screen 1:** no verdict, no map, no ranked cards, no table, no search box, no importance sliders, no "how it works", no sample result, no three explainer cards, no stat strip.

**Trigger to step 2:** the button only. **Do not auto-advance on the fifth pick** — a screen that jumps out from under the reader on the tap they did not know was terminal is the single cheapest way to make a flow feel confusing. The reader must be able to pick five, look at the order, and reorder before committing.

**Prerequisite data job — run this before building the picker.** Katz threw out ~120 of 140 questions on discriminative power ("everyone says pancakes"). Compute the spread of each of the 23 dimensions across the 710 places and **make the flat ones ineligible for the picker**. A dimension where nearly every town scores the same costs a screen and moves the ranking by nothing. This is the cheapest available reduction and it removes no real choice.

### Step 2 — one question per screen, N screens where N is what they picked

- **One question, one viewport, no scrolling at 375px.** If a question needs scrolling it is written too long.
- **Progress is a sentence, not a bar**: `2 of 5 · snow`. Political Compass ships literal "Page 1 of 6" text [V], and it is immune to both the "numbered step label" tell and the "progress dots" tell. No bar, no dots, no ring, no percentage.
- **Answer controls: discrete options wherever possible, and auto-advance on tap** for those. Political Compass forces a 4-point choice with **no neutral** [V] — forcing a side is what makes the result mean something. A visible **Back** on every screen (Setproduct: revisiting previous steps "improves trust and reduces drop-off"). Sliders, if any survive, need an explicit Continue because a drag is not a commitment.
- **Write the questions loose.** Political Compass' own instruction is that responses *"should not be overthought"* and some propositions are *"intentionally vague"* on purpose [V]. A tool built on ECCC normals will be tempted into precise, hedged questions. Precise questions are slow questions and slow questions are where people leave.
- **From question 2 onward, one small line at the bottom: `Leading so far: Nelson, BC`.** This is the dialect quiz's redraw-after-every-answer, kept (`design-refs.md` §2 [V]), and it directly answers the objection `mobile.md` raised against wizards — the result is never fully hidden, so the feedback loop survives the stepping. It also satisfies Tse's rule 3 without putting the whole verdict on screen early. Keep it one line and unstyled; it is a hint, not the payoff.

### Exact tap count, landing to first result

| Run | Taps | Breakdown |
|---|---|---|
| Minimum (1 thing) | **3** | 1 pick + 1 button + 1 answer |
| Typical (3 things) | **7** | 3 picks + 1 button + 3 answers |
| Maximum (5 things) | **11** | 5 picks + 1 button + 5 answers |

No scroll required to reach the result on any run. The last answer *lands on* the result screen — there is no separate submit tap and no "calculating" screen. Compare with the current build: 23 tiles each with a 0-3 weight control, plus a scroll past verdict, search, map and cards before the table — an unbounded interaction count with no defined completion point. **That unboundedness is what "too confusing" actually means, and a defined 3-to-11-tap path is the fix.**

### Step 3 — the result screen, top to bottom

Composed to be *earned* (the why is on the same screen as the claim) and *screenshottable* (the top 40% is a self-contained identity claim). Order matters and this order is the deliverable:

1. **The verdict as a sentence, second person, place name set largest on the page.** *"You should live in **Nelson, British Columbia.**"* Then, small: population, region. **The score is not the hero.** A big number with three small stats under it is impeccable.style's named "Hero metric layout" tell [V] — and Klim's practice, per `design-refs.md` §6, is to set the number *lighter* than its label. The place name is the identity claim; the number is evidence.
2. **One sentence of why, naming their number-one pick.** *"Because you put wildfire smoke first, and Nelson sits in the cleanest tenth of the country for it."* One dimension, the one they ranked first. This is the 16Personalities move of putting the nickname and one-line tagline immediately under the code [V].
3. **The five-row summary — the earned-ness, and the whole anti-horoscope mechanism.** Built exactly as GOV.UK's check-answers list [V]: one row per picked thing, **in the reader's own order**, each row showing *the thing · what you said · how this place scores* · **Change**. Returning from a Change link must land on that question with the answer pre-populated and come straight back — GOV.UK: *"users should not need to go through the rest of the transaction again."* This one component does four jobs: it is the why, it is the decomposition (16P's four spelled-out axes), it is the edit affordance, and it is the re-engagement loop. Unanswered things print as **"Not provided"**, per the same pattern — which is also the almanac commitment already made in `design-refs.md` §4 ("missing is printed as missing").
4. **The tradeoff, named, unhedged, in the same type size as the why.** *"What you would give up: it is eight hours to an international airport."* Precedent, all three already verified in `design-refs.md`: the dialect quiz's `Show least similar` invert, The Pudding admitting inside the piece that its own method was bad with elephants, and USGS declaring a whole **provisional edition** product tier when the data is thin. A result with no stated cost is the horoscope; a result that volunteers its cost is a recommendation. This is the single highest-value item on the screen and it must not be collapsed.
5. **Exactly one runner-up, with the one-line difference.** *"Runner-up: Rossland, BC — same air, colder winter."* One, not ten. A top-ten list is a leaderboard (`design-refs.md` §1.6: "Ranking is a leaderboard, not an argument"); one runner-up with a stated difference is an argument you can disagree with.
6. **The provenance line.** ECCC normals 1981-2010 · FireWork 2013-2024 · Census 2021 · Elections Canada 2025. The epoch stamp, per `design-refs.md` §4 — state it next to the claim, not in a footer.
7. **Two actions, bottom, in the thumb zone** (`mobile.md` §5): **"Send this to someone"** (copies the existing `location.hash` state link, untouched) and **"Explore all 710"**. Nothing else.

**Not on the result screen:** the map, the table, the search box, a share-image generator, a top-10 grid, a score gauge or ring, three cards.

**Two share objects, one screen.** Per NFX [V], the screenshot is driven by *identity projection* and *validation* — items 1-3. The forwarded link is driven by *being helpful* — items 4-7 plus the state-carrying URL, so a friend lands on your answer and can immediately re-answer as themselves. Both are already served by the order above; no separate "share card" is needed.

### Where the map and the table live

One **Explore** view, one tap from the result. Nothing in it is required to understand the answer.

- **Entry:** the "Explore all 710" button. Also the only route to the search box — search is a jump-to-a-place tool for someone who already has a place in mind, not a front door.
- **Inside:** bottom tabs **List / Map** (`mobile.md` §3-4 pattern 2, bottom tabs over hamburger). List = ranked cards showing **only the columns the reader picked** as chips, not all 23 (`mobile.md` §2 pattern C, dynamic priority columns). Tap a card → transposed detail sheet (`mobile.md` §2 pattern D, already half-built as `detailHTML`). Map = the shaded dots; tapping a dot opens the same sheet.
- **The 23-column table sits one level deeper still**, as an explicit opt-in at the end of the List, desktop-only, with frozen name column and sticky header (`mobile.md` §2 pattern A — which that file rates as a *known failure* as a primary surface and *tolerable* as a power view). This is Tse's rule 1 honoured: the click leads somewhere spectacular rather than to a merely-hidden version of the same thing.
- **Escape hatches, OWID's split** [V]: **"Download displayed data"** = the reader's five columns for all 710. **"Download full data"** = all 23. Plus a named **data sources** block and a **how to cite** line. This is the sceptic's route to the raw numbers and it costs one static file each.
- **What must NOT move behind Explore:** the verdict, the why rows, the tradeoff, the runner-up, the provenance. Datawrapper, verbatim: *"If the content is hidden, readers won't see it."* Tse: *"If the content is important for the reader to see, don't hide it."* The whole justification for hiding the table is that the table is **not** that content — and that justification collapses the moment any part of the argument gets moved in with it.

---

## 6. DO NOT DO — structural patterns that would read as generic

Each with the reason and the source. Colour and typeface do-nots are in `ai-tells.md` §9 and are not repeated.

1. **Do not print "Step 1 / Step 2 / Step 3" as chrome.** impeccable.style names *"Tiny numbered section labels — Tiny numbers repeated beside headings imitate editorial structure without adding it"* [V]; Krebs measured "numbered step sequences"; Built In names "three-step onboarding flows with progress dots" (both via `ai-tells.md`). Use `2 of 5 · snow` as a plain sentence instead.
2. **Do not ship a progress bar, dot row, or ring.** Same sources for dots. Political Compass ships "Page 1 of 6" as text and is one of the most-completed quizzes on the internet [V]. (Honest note: **progress rings specifically are unattested** — I searched and found no designer discourse naming them. Avoiding them is a taste call, not a research finding.)
3. **Do not bolt a stepper on top of the existing scrolling page.** Setproduct's named anti-pattern, verbatim: *"fake Steps UI, where all the fields are dumped into one giant form with a pretty stepper on top."* [V]
4. **Do not make the score the hero of the result.** impeccable's *"Hero metric layout — Big number, small label, three supporting stats, gradient accent"* [V]. The place name is the hero; the number is set quieter than its own label (`design-refs.md` §6, Klim practice [V]).
5. **Do not put three cards in a row anywhere** — not as "how it works", not as the top three matches. Krebs measured icon-card grids at 22%; impeccable: *"Identical card grids"* and *"Icon tile stacked above heading — the universal AI feature-card template"* [V].
6. **Do not centre the flow screens.** "Centred hero in generic sans" is one of Krebs' 16 (via `ai-tells.md`), and the safest-structure default is described as *"centered hero, stacked sections, cards, generic spacing, predictable grids"* [S]. Left-align the question, the options and the button — GOV.UK left-aligns the forward button specifically "so users do not miss it" (via `mobile.md`).
7. **Do not use an eyebrow label or pill chip above any headline** — including a "YOUR RESULT" or "STEP 2 OF 5" tag. impeccable: *"a tiny uppercase letter-spaced label sitting immediately above an oversized hero headline, or the same shape rendered as a pill chip"* [V].
8. **Do not use emoji as the labels on the 23 tiles.** `design-refs.md` counted 417 emoji flags and an emoji nav strip on nomads.com and rated system-fonts-plus-emoji its cleanest "no decision was made" diagnostic [V via design-refs]; Krebs names "sidebar with emoji icons".
9. **Do not use a gradient on the primary button.** Krebs measured gradient backgrounds at 27%; "gradient accent" is baked into impeccable's hero-metric pattern [V]. One accent, flat.
10. **Do not put any load-bearing explanation in a tooltip or a hover.** Tse: *"If you make a tooltip or a rollover, assume that no one will ever see it."* `mobile-audit.md` already found the live build's column headers are hover-only and therefore dead on touch.
11. **Do not auto-advance off the picker on the fifth pick,** and do not auto-advance a slider. A screen that leaves on an unexpected tap is the cheapest possible way to feel confusing.
12. **Do not show a top-ten grid as the result.** `design-refs.md` §1.6: *"Ranking is a leaderboard, not an argument."* One winner, one runner-up, one stated difference.
13. **Do not add a "calculating your result" interstitial, animation, or confetti.** Nothing is being computed that takes time; a fake wait is the purest form of chrome that could not have come out different.
14. **Do not generate a share image.** The result screen's top 40% *is* the share image if items 1-3 fit a phone screenshot. A separate generated card is a second thing to design badly.
15. **Do not hide the tradeoff, the runner-up, or the why behind a disclosure.** Datawrapper: *"If the content is hidden, readers won't see it."* [V]
16. **Do not put the search box on the landing screen.** It is the Nomad-List failure `design-refs.md` §1.6 documents — handing the reader 173 controls and asking them to become their own analyst. The tool's premise is that it asks *you* the questions.

---

## 7. Contradictions and honest gaps

**Contradicts `mobile.md` §1 (deliberately, on its own grounds):** that file's "do not build a wizard" verdict rested on 17 questions and interdependent steps. A 5-pick flow has neither. Details in §0. Everything else in `mobile.md` stands.

**Tension with the plan itself, worth holding:** Datawrapper and Archie Tse are on record that hidden content is unseen content, and the plan hides a table. §3 resolves this by splitting the content — argument stays visible, proof-of-work goes behind one click — but the resolution only holds if nothing from the argument migrates into Explore. That is the failure mode to watch during the build.

**Tension with `CLAUDE.md`'s ledger item 6** (every `<details>` ships `open`, because collapsed content "gets indexed but doesn't help ranking"): that rule was written for the movers SEO pages and does not automatically transfer to a client-side tool with no SEO stake. Noted rather than resolved — but the underlying instinct is identical to Tse's, so default-open is the safer read.

**Could not verify:**
- **16Personalities' test mechanics.** Their test page is a JS shell; WebFetch returned only nav and footer. I did not verify one-question-per-screen, the progress percentage, or the answer scale. Nothing in §5 depends on it.
- **16Personalities' rarity percentage and famous-person exemplars.** Claimed in a search summary [S]; the type page I opened showed neither.
- **The dialect quiz's final question count (25) and whether the map redrew live** — Knight Lab states neither. The redraw is [V] in `design-refs.md` from reading the interactive; "25" is secondary [S].
- **Every multi-step conversion statistic** (32%→41%, 86%, 296%, 412%, 15-25%). heyflow.com returned **HTTP 403**; all of these come from form-vendor marketing blogs with no named study. **Do not use these numbers anywhere.** Only the directional claim survives, and it is independently supported by GOV.UK and NN/g via `mobile.md`.
- **OWID's Chart / Map / Table tabs.** Client-side rendered; I confirmed only the Download / Data sources / How to cite layer.
- **Progress rings and pill buttons as AI tells.** Searched, found nothing. Unattested, not cleared.
- **The "which city should you live in" genre.** I opened none that are alive and well-designed. `design-refs.md` already established why: **Teleport, the only serious prior art, is dead** (DNS parks, zero content). The genre's living examples are Nomad List and Numbeo, both already documented there as anti-references. So there is no exemplar to copy in this category — the flow above is assembled from quizzes and news graphics instead, which is the honest position.

---

## Source list (opened and read, this file only)

1. Political Compass, test page 1 — https://www.politicalcompass.org/test/en?page=1 [V]
2. Political Compass, test intro — https://www.politicalcompass.org/test [V]
3. Knight Lab, "Behind the dialect map interactive" (Josh Katz interview) — https://knightlab.northwestern.edu/2014/01/20/behind-the-dialect-map-interactive-how-an-intern-created-the-new-york-times-most-popular-piece-of-content-in-2013/ [V]
4. GOV.UK Design System, "Check answers" pattern — https://design-system.service.gov.uk/patterns/check-answers/ [V]
5. Datawrapper Academy, "Our explanatory approach" (incl. the Archie Tse quote) — https://www.datawrapper.de/academy/our-explanatory-approach [V]
6. Our World in Data grapher, life expectancy — https://ourworldindata.org/grapher/life-expectancy [V]
7. 16Personalities, INFJ type page — https://www.16personalities.com/infj-personality [V]
8. NFX, "Why People Share: The Psychology Behind Going Viral" — https://www.nfx.com/post/why-people-share [V]
9. *International Journal of Communication*, "Online Quizzes as Viral, Consumption-Based Identities" — https://ijoc.org/index.php/ijoc/article/view/5265 [V]
10. impeccable.style, "Slop" (structural patterns only) — https://impeccable.style/slop/ [V]
11. Setproduct, "Steps UI design" — https://www.setproduct.com/blog/steps-ui-design [V]

**Opened and failed:** https://www.16personalities.com/free-personality-test (JS shell) · https://heyflow.com/blog/reduce-form-abandonment-progress-indicators/ (HTTP 403) · https://design-system.service.gov.uk/patterns/task-list-pages/ (archived, content removed; renamed to "Complete multiple tasks")

**Search-summary only, not opened [S]:** niemanlab.org Malofiej 2016 report · medium.com/@dominikus on the death of interactive visualisations · github.com/archietse/malofiej-2016 slides · formflux.io · amraandelma.com · ivyforms.com · dev.to "How to fix the AI-generated look" · publishd.app · languagelog.ldc.upenn.edu · academy.datawrapper.de disclosure-widget article
