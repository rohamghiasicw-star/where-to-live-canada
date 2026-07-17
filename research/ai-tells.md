# What makes a web design read as AI-generated — evidence inventory (July 2026)

Research method: Reddit mined directly via the JSON API (through a logged-in browser session — Reddit 403s datacenter IPs and blocks Anthropic's crawler entirely, so both `curl` from the sandbox and WebFetch are dead ends for reddit.com). Supplemented with designer blogs, one quantitative study, and one New Yorker piece.

**Verdict key**
- **REAL / LOUD** — designers name this unprompted, first, repeatedly.
- **REAL / QUIET** — documented by credible sources, but not what people shout about.
- **CONTESTED** — sources disagree, or it's a trend complaint rather than an AI complaint.
- **NOT SUPPORTED** — I searched for it and could not find designers complaining. Assumption, not tell.

---

## 0. The single most important finding

The loudest tells are **colour and layout**, not typography-as-such, and *by a wide margin* the loudest single tell is **the purple/blue gradient**. Everything else is downstream.

Top-voted comment in r/web_design's "Everything already looks and feels like it's Ai and it's depressing" thread — the first thing anyone says, +39:

> "you can tell if a website is vibe coded when there's blue/purple gradients everywhere in the frontend"
> — u/gatwell702, https://www.reddit.com/r/web_design/comments/1q73fox/

**The causal origin is documented and specific.** Tailwind UI shipped `bg-indigo-500` as the default button colour in ~2019-2020. LLMs trained on the resulting mountain of Tailwind tutorials. Adam Wathan (Tailwind's creator) posted a semi-apologetic tweet in August 2025 — 1M+ views — apologising "for making every button in Tailwind UI use `bg-indigo-500` five years ago, because now every AI-generated interface on earth is purple."
- https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p
- Named classes: `bg-indigo-500`, `text-indigo-600`, `from-indigo-500 to-purple-600`

This matters for your stack: **you are not using purple.** The single loudest tell does not apply to you. That is a genuine advantage, and it means the marginal tells below carry proportionally more weight.

---

## 1. The quantitative baseline (the only hard numbers that exist)

Adrian Krebs ran Playwright + deterministic DOM/computed-style checks over **1,590 Show HN submissions**. Not LLM vibes — actual CSS checks. Self-reported false-positive rate 5-10%.
- https://www.adriankrebs.ch/blog/design-slop/

Results:
| Tier | Definition | Share |
|---|---|---|
| Heavy slop | 4+ patterns | 22% (347) |
| Mild | 2-3 patterns | 32% (508) |
| Clean | 0-1 patterns | 46% (735) |

**Most common tells, measured:**
1. Permanent dark theme — **34%**
2. Gradient backgrounds — **27%**
3. Icon-card grids — **22%**

⚠️ **Source-integrity note:** `developersdigest.tech/blog/ai-design-slop-and-how-to-spot-it` presents "16 AI Design Slop Patterns" as its own reporting. It is the **same dataset, same 16 patterns, same 22/32/46 split** as Krebs. It is a repost. **Treat these as ONE source, not two.** Anyone citing both as corroboration is double-counting.

The 16 patterns (Krebs' list):
- **Fonts:** Inter everywhere (esp. centred hero); Space Grotesk / Instrument Serif / Geist combos; serif-italic on one accent word in an otherwise-Inter hero
- **Colour:** "VibeCode Purple"; perma-dark-mode w/ medium-grey body text + all-caps section labels; barely-passing WCAG AA contrast; gradients everywhere; large coloured glows/box-shadows
- **Layout:** centred hero in generic sans; badge directly above H1; coloured left/top borders on cards; identical icon-top feature cards; numbered 1-2-3 step sequences; stat banner rows; sidebar with emoji icons; all-caps headings
- **Frameworks flagged:** shadcn/ui, glassmorphism

Krebs on card borders — note the strength of this claim:
> "Colored left borders are almost as reliable a sign of AI-generated design as em-dashes for text."

---

## 2. COLOUR

### 2.1 Purple/blue/indigo gradient — **REAL / LOUD. The #1 tell.**
See §0. Named first, by everyone, in every source. Measured at 27% of Show HN pages.

**Contrarian view worth knowing** (r/web_design, "Is AI design becoming desirable?"):
> "AI learns on popular designs. So naturally, the output it makes mirrors the popular design trends. The common AI design (purple gradients, cards, drop shadows, round corners) are not inherently bad, just overused, and they were already being overused before the AI."
> — u/hdd113, https://www.reddit.com/r/web_design/comments/1sk7k6r/

And a genuinely useful inversion — purple is now a *deliberate* signal for AI products:
> "We have a purple / blue gradient on our site and it was built by hand haha but in our case it's to subconsciously signal that we're an AI product. Kinda how the sparkle has become affiliated with AI too."
> — u/ZacheryBMimbs, https://www.reddit.com/r/web_design/comments/1q73fox/

(The ✨ sparkle emoji as an AI signifier is a real, separate tell.)

### 2.2 Warm cream / beige + terracotta / rusty orange — **REAL / LOUD, and rising fast. This is "the Claude look".**
This is the most important finding for anyone building in 2026, and it is **specifically documented by Kyle Chayka in The New Yorker** ("The A.I.-Design Aesthetic That's Taking Over the Internet", June 2026).

Chayka's inventory of the emergent Claude Design aesthetic:
> "beige- and cream-colored backgrounds, rusty orange-hued accents"
> — large serif typefaces, **italicised**
> — subheadings that are **"tracked out"** (extra letter-spacing)
> — "an inexplicable prevalence of ticker-like text bars, as if the website were a cable-news show"
> — "dashboard elements with multiple rounded rectangular outlines, sometimes with a neon glow underneath"

Sources:
- https://kylechayka.substack.com/p/the-generic-style-of-ai-web-design
- The New Yorker: https://www.newyorker.com/culture/infinite-scroll/the-ai-design-aesthetic-thats-taking-over-the-internet
- New Yorker's own framing: "Anthropic's new A.I. tool is creating instant design clichés" — https://x.com/NewYorker/status/2070280959677895042

Chayka's mechanism, verbatim:
> when users don't actively resist the model's output, "they get the generic output, the lowest common acceptable denominator of aesthetics and taste."

Independently corroborated by the 46-pattern slop list:
> **Cream surfaces** — "Warm cream or beige page background has become the default 'tasteful' AI surface"
> — https://impeccable.style/slop/

And by designer Nick Simson, who names the palette he's actively avoiding: **warm terracotta, serif typefaces, sand-coloured backgrounds** — https://www.nicksimson.com/posts/2026-the-vibes-are-off.html

**Your `#F4F1EA` + terracotta instinct is correct and it is now arguably a WORSE tell than purple**, because purple reads as "cheap AI" while cream/terracotta reads as "tasteful AI" — which is exactly the costume more sophisticated builders now reach for. It is the default output of the most design-forward AI tool on the market.

### 2.3 Near-black + single vermilion/acid accent — **NOT SUPPORTED as a named tell.**
I searched specifically for this. **No designer discourse names "near-black + one saturated accent" as an AI tell.** It does not appear in Krebs' 16, the impeccable 46, 925studios' list, Chayka, or Built In.

**But** — two adjacent things ARE tells, and your stack sits between them:
- **Perma-dark-mode is the #1 *measured* tell at 34%** (Krebs). Not dark + orange specifically. Just: the page is dark by default and never had a light mode.
- **Dark + coloured glow** is named: "Dark backgrounds with colored box-shadow glows are the default 'cool' look" (impeccable.style).

So: **dark is a tell. Orange is not. Dark + orange + *glow* would be.** Dark + orange + flat, no glow, no gradient — is not a documented tell.

### 2.4 Dark-mode-technical + `#FF5722` orange — **NOT SUPPORTED. You are likely imagining this one.**
Direct answer to your question: **no.** I searched for it explicitly. 925studios' AI-slop tells piece — a dedicated inventory — **does not mention orange accents at all.** Neither does Krebs, nor Built In. The AI-orange that IS documented is Chayka's **rusty/terracotta orange on cream** (§2.2), which is a *warm editorial* orange, not a *technical* `#FF5722` orange.

Caveat worth holding: absence of complaint in July 2026 is not proof of safety — it may simply be early. But as of now, this is not a thing designers complain about.

### 2.5 Olive / army green + cream — **NOT SUPPORTED.**
Searched. Returns only SEO palette-generator spam (huehive, media.io), **zero designer discourse**. The fact that the query surfaces AI-palette-generator sites rather than critique is itself the finding: it's a generic "earthy" palette, not a recognised AI signature. Closest real tell is the **cream/beige background** (§2.2), which olive+cream would trigger — the olive is incidental, the cream is the problem.

### 2.6 Other colour tells — **REAL / QUIET**
- **Cyan-on-dark** — "Purple/violet gradients and cyan-on-dark are the most recognizable tells" (impeccable.style)
- **Gradient text on headlines** — flagged by dev.to and impeccable ("violates scannability")
- **Barely-passing contrast** — "Generated dark themes routinely ship body text that fails WCAG AA" (Krebs). This is a *forensic* tell: run a contrast checker; AI dark themes fail.
- **Large coloured glows / box-shadows** (Krebs; impeccable "dark mode glow")

---

## 3. TYPE

### 3.1 Inter — **REAL / LOUD. The #1 type tell.**
> "Inter is the #1 indicator of AI-generated slop, with Roboto, Arial, and Space Grotesk following close behind."
> — https://aiskill.market/blog/banning-inter-the-font-tell

> "Inter becoming the Helvetica of the LLM era." — Krebs

Crucially, everyone is careful to say the typeface is *good*: "The goal is not to avoid Inter because it is bad — it is an excellent typeface — but to make a deliberate choice rather than accepting the default." The tell is **ubiquity**, not quality. "When every generated page uses the same face, that face stops signaling craft and starts signaling 'generated'."

### 3.2 Space Grotesk — **REAL / LOUD, and specifically damning.**
> "Space Grotesk serves as the model's idea of an 'edgy default' — when an agent wants to look more designed, it reaches for Space Grotesk, and it has become its own cliché."
> — aiskill.market

This is the sharpest single observation in the whole corpus: Space Grotesk is what the model picks *when it is trying not to look generic*. Reaching for it is the tell that you asked the model to be interesting.

### 3.3 The named AI font set — **REAL / LOUD**
Consistently, across independent sources: **Inter, Space Grotesk, Instrument Serif, Geist** (+ Roboto, Arial).
- Krebs: "Space Grotesk, Instrument Serif, and Geist"
- impeccable.style "Overused fonts": "Inter, Geist, Space Grotesk, Instrument Serif"

Geist = Vercel's typeface. Instrument Serif = the italic-serif-accent face.

### 3.4 Serif italic accent word in the hero — **REAL / LOUD**
Krebs: "Serif italic for one accent word in an otherwise-Inter hero."
impeccable: "**Italic serif hero** — Oversized italic serif as the primary hero headline."
Chayka: "large italicized serif type."

Three independent sources. This is one of the most reliable tells in existence. The construction "Build *better* software" with one word in Instrument Serif italic is a signature.

### 3.5 ALL-CAPS letterspaced eyebrow label above the headline — **REAL / LOUD. Your instinct is right.**
Directly named, verbatim:
> "**Eyebrow labels** — Tiny uppercase letter-spaced label sitting immediately above an oversized hero headline"
> — https://impeccable.style/slop/

Corroborated three ways:
- Krebs: "perma dark mode with medium-grey body text and **all-caps section labels**"; separately "**Badge right above the hero H1**"; separately "All-caps headings"
- Chayka: "**tracked-out subheadings**" (tracked-out = letterspaced)

**This is a confirmed, multi-source tell.** The eyebrow + tracking + caps combo is one of the most reliably AI constructions there is.

### 3.6 "Condensed uppercase headline + letterspaced mono caption" as a combo — **NOT SUPPORTED as a named combo.**
Honest answer: **I could not find this specific pairing named anywhere.** Neither half is attested as a *condensed*-type tell:
- **No source names condensed display faces** (League Gothic, Oswald, Anton, Archivo) as AI tells. Not in Krebs, impeccable, 925studios, aiskill, or Chayka. AI reaches for *neo-grotesques* (Inter/Geist) and *editorial serifs* (Instrument), not condensed.
- **But the second half of your combo is a tell.** "Letterspaced caption" = eyebrow label (§3.5) = confirmed. And mono-for-UI-labels is §4.

So: the *condensed uppercase headline* is clean. The *letterspaced caption* under it is the liability.

### 3.7 IBM Plex Sans / Mono — **NOT SUPPORTED. Direct answer: no, it is not an AI tell.**
Searched explicitly for IBM Plex and JetBrains Mono as overused/cliché. **Zero designer criticism found.** No AI-tell list names IBM Plex. The AI mono default, where one exists, is Geist Mono / the shadcn stack.

The only mild negative sentiment found anywhere: one designer noting they'd used IBM Plex Mono since 2018 and always felt "a bit of an IBM shill for doing so" — https://dx13.co.uk/articles/2023/02/17/monospaced/ — which is a corporate-association gripe from 2023, not an AI tell.

**IBM Plex is currently a safe, differentiating choice.** It is arguably *anti*-slop precisely because the models don't reach for it.

### 3.8 One typeface for everything — **REAL / QUIET**
impeccable.style: "**Single font** — Using one typeface for headings, body, labels, buttons." A real tell of no typographic decision having been made.

---

## 4. MONO / THE "FAKE TECHNICAL" AESTHETIC

This is the most nuanced section and where your question is sharpest. **The answer is genuinely split.**

### 4.1 Monospace-everything — **CONTESTED. Not currently an AI tell. It's a legit 2026 trend AND a cliché risk.**
- **Not on any AI-tell list.** Mono does not appear in Krebs' 16, impeccable's 46, or 925studios' inventory. 925studios explicitly does **not** mention monospace.
- **It's a deliberate, respected 2026 trend.** Tubik Studio's 2026 trends piece names "a return to monospaced or mono-inspired type to align visual rhythm with data logic," describing "raw, schematic, brutally clear layouts" and "bringing wireframe logic into final UIs." Their framing: "This isn't 'ugly on purpose.' It's function-forward design." — https://blog.tubikstudio.com/ui-design-trends-2026/
- **Named as an aesthetic with a name:** "Technical Mono / Code Brutalism" — monospaced typography, command-line simplicity, high-contrast layouts, ASCII art, wireframe diagrams, green-on-black. — https://aigoodies.beehiiv.com/p/aesthetics-2026

⚠️ **Verification note:** a search snippet attributed the line *"overuse turns it into parody"* and *"thin lines pointing at elements, small labels that look informational even when they're decorative"* to this beehiiv piece. **I fetched it and those lines are NOT in it.** The snippet conflated sources. I could not locate a primary source for that phrasing. **Do not cite it.** (Flagging because it's the single most quotable line for your §4 thesis and it appears to be a search-engine hallucination.)

### 4.2 The "credibility costume" critique — **REAL, but the critique is of AI generally, not the technical aesthetic specifically.**
The strongest version of your "dresses up as a data instrument to seem credible" thesis is Built In's "new skeuomorphism" argument — and it indicts *all* AI design, not the technical look:
> "It is the average of all design that has ever been fed into a model, rendered with enough technical competence to clear every review"
> "AI points at nothing in particular and says, **'This is professional.'**"
> Where skeuomorphism had "conviction" (misplaced as it was), AI design has **"no position."**
> Interfaces that "looked like no one made them."
> "There's just a faint sense that nobody thought about the users specifically, which is correct"
> — https://builtin.com/articles/ai-design-slop-era

### 4.2b The best answer to your telemetry question — and it's from Reddit, not a blog
A solo founder posted an AI-rebuilt analytics dashboard asking *"how do I make it not look like AI made it?"* (r/vibecoding). The most substantive reply reframes the whole question, and it is the sharpest thing I found anywhere on the technical-instrument aesthetic:

> "It does **not scream AI** to me as much as it reads like a **default dashboard kit**: same dark surface everywhere, **KPI cards with equal weight**, and a line chart as the main proof even though a Pomodoro app is really about behavior change. I would make it feel more intentional by changing the hierarchy around the user's question: 1. Make the top row answer 'did I have a good focus week?' instead of only showing raw metrics. 2. Group metrics into behavior stages... 3. **Use one primary accent only** for progress toward the weekly goal. Let everything else be quieter. 4. Replace generic labels/icons with domain-specific [ones]"
> — u/devlimelabs, https://www.reddit.com/r/vibecoding/comments/1unm64x/

And, plainly:
> "I would say it screams AI per se, just more basic, **like all the dashboard templates**."
> — u/mirepup, same thread

**This is the answer to your question 4.** The tell is not "it looks technical." The tell is **KPI cards with equal weight** — an instrument panel where nothing is prioritised, because no one decided what matters. A real instrument has a *primary reading*. Slop has four identical stat tiles. Note this bites your `.lm` **4-up stat strip** directly: four equal-weight metrics in a row is *both* Krebs' "stat banner rows" tell *and* the equal-weight-KPI tell.

The prescription — "use one primary accent only, let everything else be quieter" — is also the single most actionable fix in the entire corpus.

**Bottom line on §4:** the technical/telemetry aesthetic is **not** yet an AI tell. It is a real trend practiced deliberately by good designers. Your risk is not "technical = AI"; it's §6 — technical-as-costume, where the instrument panel displays nothing and every reading is the same size.

### 4.3 Grid-line backgrounds — **CONTESTED / trend tell, not AI tell.**
The "Vercel aesthetic" blueprint grid is real and named — Vercel's redesign popularised the subtle grid pattern; Stripe, Tailwind, Linear followed. — https://www.setproduct.com/blog/complete-guide-to-blueprint-grid-design

But it's absent from every AI-tell list. It reads as **"2023 dev-tool trend-follower"**, not "AI made this."

### 4.4 The "Linear look" — **REAL / LOUD, but it is a TREND complaint, NOT an AI complaint. Important distinction.**
Daryl Ginn's "The Linear effect" predates the AI-slop discourse and **never mentions AI**. Three traits:
1. "Dark, your website has to be dark"
2. Subtle blurred gradient overlays, especially "behind product visuals"
3. "Animated glowing artefacts" — "bonus points if they're interactive"

The killer line:
> "Squint and look at the images above, can you tell they are 4 different websites? I'm not sure I can."
> — https://rectangle.substack.com/p/the-linear-effect

Even Linear's own co-founder tweeted: "Thinking @linear should go from dark to light mode in 2023."
Aggregator of the clones: **linears.art**.

> "Open any new SaaS product launched in the last two years, and there is a 50/50 chance it looks like Linear" — https://www.925studios.co/blog/linear-design-breakdown-saas-ui-2026

**Why this matters to you:** the Linear look is criticised as derivative *by humans copying humans*. AI then trained on it. So dark + glow + gradient now reads as **both** trend-chasing **and** AI. The overlap is dark-mode + glow — which is why §2.3's verdict is "dark is the tell, orange isn't."

---

## 5. LAYOUT / COMPONENTS

Ranked by strength of evidence.

| Pattern | Verdict | Evidence |
|---|---|---|
| **Three icon-top feature cards in a row** | **REAL / LOUD** | Krebs measured **22%** ("icon-card grids"). 925studios calls it the signature layout: *"a row of three feature cards, rounded corners, soft shadow, thin-line icon at the top of each."* impeccable: *"A small rounded-square icon container above a heading is the universal AI feature-card template."* |
| **Coloured left/top accent rail on cards** | **REAL / LOUD** | Krebs: *"almost as reliable a sign of AI-generated design as em-dashes for text."* impeccable: *"Side-tab accent — Thick colored border on one side of a card. The most recognizable tell of AI-generated UIs."* **Two independent sources both call this the most reliable tell.** |
| **Perma-dark mode** | **REAL / LOUD** | Krebs' **#1 measured tell, 34%** |
| **Badge/pill directly above the H1** | **REAL / LOUD** | Krebs: "Badge right above the hero H1" |
| **Centred hero, generic sans** | **REAL / LOUD** | Krebs |
| **Glassmorphism** | **REAL** | Krebs flags it; impeccable: *"Blur effects, glass cards, and glow borders used as decoration"* |
| **Extreme rounding (`rounded-2xl`/`3xl`)** | **REAL** | impeccable: *"24px and up"* border-radius on small elements. Eidos: *"rounded corners stacked around more rounded corners, pillow buttons"* |
| **Gradient orbs / blobs** | **REAL** | Built In: *"Gradient blobs (soft, orbital, vaguely optimistic)"*; Eidos: *"blobs and abstract backgrounds"* |
| **Numbered 1-2-3 / 01-02-03 steps** | **REAL** | Krebs "numbered step sequences"; impeccable "01 / 02 / 03 section labels"; Built In "three-step onboarding flows with progress dots" |
| **Stat banner row (4-up metrics)** | **REAL** | Krebs: "stat banner rows" |
| **1px hairline + wide diffuse shadow** | **REAL / QUIET** | impeccable: *"Hairline + shadow combo — 1px hairline paired with a wide, diffuse shadow"* |
| **Nested cards** | **REAL / QUIET** | impeccable: *"Cards inside cards create visual noise and excessive depth"* |
| **Monotonous spacing** | **REAL / QUIET** | impeccable: *"The same spacing value used everywhere"* — a strong forensic tell: no spacing *scale* was decided |
| **Sidebar with emoji icons** | **REAL** | Krebs |
| **Everything lifts on hover** | **REAL — Reddit-only find** | *"and everything transforms upward a few pixels just a little on hover. Not just buttons either, whole box-shadowed sections"* — u/tonyciccarone, https://www.reddit.com/r/web_design/comments/1q73fox/ — **not in any blog list.** |
| **Bento grids** | **NOT SUPPORTED** | Searched; appears on no AI-tell list. Apple/trend signifier, not AI. |
| **Grid-line backgrounds** | **CONTESTED** | §4.3 — trend tell, not AI tell |
| **Donut chart top-right of dashboard** | **REAL / QUIET** | Built In |

**Broken links as a tell** — a forensic non-visual one worth noting:
> "Many AI sites I've seen have broken links. Just visited a AI software company where the lead magnet doesn't work.... kinda hard to trust an AI company who doesn't check the slop it produces."
> — https://www.reddit.com/r/web_design/comments/1q73fox/

---

## 6. THE META-TELL: "concept as costume"

Your framing has no single agreed name, but the **argument is well-established** and Built In states it best. There is no evidence for a term "concept as costume" in circulation — but the idea is everywhere:

- **Built In:** AI design is "the average of all design that has ever been fed into a model, rendered with enough technical competence to clear every review." It has "no position." "AI points at nothing in particular and says, 'This is professional.'" Named tells are all *competent*: gradient blobs, three-step onboarding, empty states with friendly illustrations, donut charts, card layouts, clean nav. "All technically sound. All interchangeable."
- **Chayka:** the model "locks onto a pattern that works" then "reproduces that infinitely" — so the *theme* varies while the *structure* doesn't.
- **Eidos Design** (The Slop Rebellion): AI "excels at the average"; the fix is "designing like there's an author," work with "conviction baked back into it." Treat AI output "like a junior designer's first draft, critiquing it and cutting what's generic while keeping the one weird thing it got right by accident." — https://eidosdesign.substack.com/p/eidos-design-volume-xxxii-ai-made
- **Michal Malewicz's "Slopless" manifesto** — an organised anti-sameness movement. "No quarrel with AI itself"; the ask is that designers "stop letting the tools make the decisions." — https://slopless.design/

**Reddit's version of the meta-tell** — the most damning practical test anyone proposed:
> "Ask your Ai to build 3 different landing [pages]..." [they come out the same]
> — u/cartiermartyr, https://www.reddit.com/r/web_design/comments/1sb2pia/

and

> "I visited Lovable and Framer today.. I swear they're just pushing the same sampled design works"
> — u/cartiermartyr, same thread

**The operational test this implies:** if you can swap your palette for another brand's and the design still works perfectly — it has no concept, it has a costume. A real concept breaks when you restyle it.

---

## 7. COPY TELLS

| Tell | Source |
|---|---|
| **Em-dash overuse** — "More than a couple of em-dashes in body copy is an AI cadence tell" | impeccable.style |
| **Buzzwords:** *streamline, empower, supercharge, world-class, enterprise-grade* | impeccable.style |
| **Weightless imperative headline pairs:** *"Build faster. Ship smarter."* | 925studios |
| **Aphoristic cadence** — short rebuttal statements ("It's not X. It's Y.") | impeccable.style |
| **"Theater framing"** — dismissing things as "performative" | impeccable.style |
| **Gradient text on the headline** | dev.to / impeccable |

(Your house style already bans em dashes — that's the single biggest copy tell, already handled.)

---

## 7b. THE TELL THAT BEATS ALL OTHERS FOR A NON-DESIGNER AUDIENCE: THE IMAGERY

Worth flagging because it outranks everything above for a general audience. The single biggest "looks AI generated" roast thread I found (**254 comments, +1082**, r/graphic_design, "latest issue of tradie looks AI generated") is **not about layout at all**. Every top comment is about the *photograph*.

Nobody mentioned fonts, colour, or grids. They mentioned the fake photo — and then, tellingly, someone identified its actual provenance:
> "That specific image is AI-generated stock image from 2023. They did look for it, they didn't generate it themselves."
> — u/MsMaggieMcGill (+363), https://www.reddit.com/r/graphic_design/comments/1dsqjqg/
> "Because it's faster and easier than finding stock of laughing construction guys. And cheaper probably."
> — u/funkyfreshpants (+237), same thread

**Implication:** for a trades/service business, a single fake or generic-stock hero photo will out you as AI faster than any typographic choice — to *customers*, not just designers. Real photos of real crews are the highest-leverage anti-AI move available, and it costs nothing but sourcing discipline.

---

## 8. WHAT ACTUALLY FIXES IT (upvoted, concrete)

- **Feed it a design system as context — that's the whole game.** The top answer in r/webdev's "Do AI-generated UIs actually maintain design consistency?":
  > "AI is great at generating a single screen that looks good. It's terrible at remembering what it decided three screens ago... always feed it a design system as context — your **spacing scale, type ramp, color tokens, component library**. Without constraints it'll make every page look like a different app. What works for me: define the system first (even a minimal one), then use AI within [it]."
  > — u/Strong_Check1412, https://www.reddit.com/r/webdev/comments/1rour0f/

  Corroborated in the same thread: consistency "breaks once you start scaling beyond a few screens... The main reason is that the model does not truly understand the design system behind the product unless you explicitly provide it. If spacing tokens, typography scale, component rules, and color variables are clearly defined in the prompt or design context, AI can follow them reasonably [well]" — u/Academic_Flamingo302
- **One primary accent, everything else quieter.** Fix hierarchy around the user's actual question, not around raw metrics. — u/devlimelabs (§4.2b)
- **Don't accept the default; make one committed decision.** The consensus across aiskill.market and Eidos: the problem is never quality, always *defaults*. "A skill that bans the defaults before code generation and forces a committed choice overwrites the model's taste up front."
- **Treat AI output as a junior's first draft** — critique it, cut the generic, "keep the one weird thing it got right by accident." (Eidos)
- **The 3-landing-page test** — generate three; if they're the same, the tool decided, not you. (u/cartiermartyr)
- **Check your links.** Broken links + dead lead magnets are a trust-killing tell that costs nothing to fix.
- **Run a contrast checker.** AI dark themes routinely fail WCAG AA (Krebs) — passing contrast is a cheap, forensic differentiator.
- **Counter-aesthetic (the designers' answer):** friction, texture, glitch, nostalgia, "intentional mistakes, hand-drawn marks, texture overlays, rough edges, imperfect line work." (Eidos / Lindsay Marsh)

---

## 9. THE DO-NOT LIST

Ordered by evidence strength. Each is a thing to check a design against.

1. **DO NOT use a purple/blue/indigo gradient.** The #1 tell, universally. Origin: Tailwind `bg-indigo-500`. — dev.to indigo-500; r/web_design 1q73fox (+39 top comment)
2. **DO NOT put a coloured accent rail on the left/top edge of cards.** Two independent sources call it *the most recognisable* tell. "Almost as reliable as em-dashes for text." — Krebs; impeccable.style
3. **DO NOT default to permanent dark mode.** The #1 *measured* tell at 34% of 1,590 pages. — Krebs
4. **DO NOT ship a row of three icon-top feature cards.** 22% measured. The universal AI feature-card template. — Krebs; 925studios; impeccable.style
5. **DO NOT use Inter, Space Grotesk, Geist, or Instrument Serif.** Especially not Space Grotesk — it's the model's "edgy default," i.e. the tell that you asked it to look designed. — aiskill.market; Krebs; impeccable.style
6. **DO NOT italicise one serif accent word in a sans hero.** Three independent sources. — Krebs; impeccable.style; Chayka
7. **DO NOT use a warm cream/beige background with terracotta/rusty-orange accents.** This is "the Claude look," documented in The New Yorker. Now the *tasteful* slop. — Chayka; impeccable.style; Simson
8. **DO NOT put a tiny letterspaced ALL-CAPS eyebrow above an oversized headline.** Explicitly named. — impeccable.style; Krebs; Chayka ("tracked-out subheadings")
9. **DO NOT put a badge/pill directly above the H1.** — Krebs
10. **DO NOT combine a dark background with coloured box-shadow glows.** The default "cool" look; also the Linear-clone tell. — impeccable.style; Ginn
11. **DO NOT use one typeface for headings, body, labels and buttons.** Signals no typographic decision was made. — impeccable.style
12. **DO NOT use a single spacing value everywhere.** Signals no scale was designed. — impeccable.style
13. **DO NOT round everything to 24px+, or nest cards in cards.** — impeccable.style; Eidos
14. **DO NOT animate a hover-lift on every box.** Reddit-observed, absent from blog lists — so it's an *unguarded* tell. — u/tonyciccarone
15. **DO NOT ship failing contrast.** AI dark themes "routinely ship body text that fails WCAG AA." — Krebs
16. **DO NOT use em dashes, or "streamline/empower/supercharge/world-class/enterprise-grade", or "Build faster. Ship smarter."** — impeccable.style; 925studios
17. **DO NOT use ✨ as an AI signifier** (unless you *want* to signal AI). — u/ZacheryBMimbs
18. **DO NOT ship broken links.** — r/web_design 1q73fox
19. **DO NOT give every stat/KPI card equal weight.** An instrument panel with no primary reading is the "default dashboard kit" tell. Applies directly to a 4-up stat strip. — u/devlimelabs; Krebs ("stat banner rows")
20. **DO NOT use AI or generic stock photography.** The loudest tell to a *non-designer* audience by a mile — the biggest roast thread found was 254 comments about one fake photo, zero about layout. — r/graphic_design 1dsqjqg

### Cleared — searched for, NOT found to be tells
- **Near-black + single vermilion/acid accent** — not named anywhere. *Dark* is the tell; the accent hue isn't.
- **`#0A0A0A` + `#FF5722` technical dark+orange** — **not a cliché.** 925studios' dedicated tell-list doesn't mention orange at all. The documented AI orange is *rusty terracotta on cream*, a different animal.
- **Olive/army green + cream** — no designer discourse. Only the *cream* half is a liability.
- **IBM Plex Sans / Mono** — no criticism found. Currently safe and differentiating; models don't reach for it.
- **Condensed display faces** (League Gothic, Oswald, Anton, Archivo) — named on no AI-tell list. AI reaches for neo-grotesques and editorial serifs, not condensed.
- **Monospace for UI labels** — not on any AI-tell list; a deliberate, respected 2026 trend (Tubik). Cliché risk ≠ AI tell.
- **Bento grids** — on no AI-tell list.
- **Grid-line backgrounds** — "Vercel aesthetic," a 2023 trend tell, not an AI tell.
- **The technical/telemetry aesthetic itself** — not an AI tell. Practiced deliberately by good designers. Your risk is §6, not §4.

---

## 10. THE 10 SHARPEST SPECIFICS

1. **The purple is Tailwind's fault, specifically `bg-indigo-500`,** and Adam Wathan apologised for it in Aug 2025 to 1M+ views. The tell has a documented cause, a class name, and a date.
2. **"Colored left borders are almost as reliable a sign of AI-generated design as em-dashes for text."** (Krebs) — two independent sources rank the card accent rail as *the* most recognisable tell, above colour.
3. **Space Grotesk is what the model picks when you ask it not to be generic.** "The model's idea of an 'edgy default'... it has become its own cliché." Reaching for it is the tell that you tried.
4. **34% / 27% / 22%** — perma-dark, gradient backgrounds, icon-card grids, measured by Playwright over 1,590 Show HN pages. The only hard numbers in the discourse.
5. **The New Yorker documented "the Claude look" in June 2026:** beige/cream + rusty orange + big italic serif + tracked-out subheads + cable-news ticker bars + rounded-rect dashboards with neon glow underneath. Your cream+terracotta hypothesis is not just right — it's *the* 2026 tell.
6. **"AI points at nothing in particular and says, 'This is professional.'"** (Built In) — the meta-tell in one line. Every AI tell is *competent*. That's the point. It clears review and says nothing.
7. **Your dark+orange+mono stack is NOT a documented tell** — I looked hard. Dark is (34%). Glow is. Orange, mono, condensed, IBM Plex, bento and grid-backgrounds are not. Don't fix what isn't broken; fix the *dark-by-default* and any *glow*.
8. **"Everything transforms upward a few pixels on hover. Not just buttons either, whole box-shadowed sections."** — a real tell that appears on **zero** blog lists. Reddit sees things the think-pieces miss.
9. **"KPI cards with equal weight"** is the real telemetry tell — not the technical look itself. A dashboard where nothing is primary reads as a "default dashboard kit." The fix, verbatim: *"use one primary accent only... let everything else be quieter."* Your 4-up stat strip is the exposed surface.
10. **The restyle test:** if swapping your palette for another brand's leaves the design working perfectly, you have a costume, not a concept. Corollary of "ask your AI to build 3 different landing pages" — they come out identical.
11. **To customers, the photo is the tell, not the type.** The biggest roast thread in the corpus (254 comments) never mentions layout. It's all about one fake construction-worker stock image. For a movers site this outranks every item above.
12. **The double-counting trap:** the "16 patterns" list circulating as two sources (developersdigest + Adrian Krebs) is **one** study. Most 2026 "AI slop" listicles are reposts of Krebs, impeccable.style, or Chayka. There are ~4 primary sources in this entire discourse; everything else is downstream.

---

## Source list

**Primary / load-bearing**
- Adrian Krebs, "Scoring Show HN submissions for AI design patterns" — https://www.adriankrebs.ch/blog/design-slop/ *(the only quantitative study)*
- Kyle Chayka, "The generic style of AI web design" — https://kylechayka.substack.com/p/the-generic-style-of-ai-web-design
- Kyle Chayka, The New Yorker, "The A.I.-Design Aesthetic That's Taking Over the Internet" (June 2026) — https://www.newyorker.com/culture/infinite-scroll/the-ai-design-aesthetic-thats-taking-over-the-internet
- "Slop" (46 patterns, 8 categories) — https://impeccable.style/slop/
- Built In, "The New Skeuomorphism: How AI Makes Bad Design Look Good Enough" — https://builtin.com/articles/ai-design-slop-era
- "Banning Inter: Why Font Defaults Are the Slop Tell" — https://aiskill.market/blog/banning-inter-the-font-tell
- dev.to / Alan West, "Why Every AI-Built Website Looks the Same (Blame Tailwind's Indigo-500)" — https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p

**Reddit (verbatim, mined via JSON API)**
- r/web_design — "Everything already looks and feels like it's Ai and it's depressing" — https://www.reddit.com/r/web_design/comments/1q73fox/ *(the purple gradient tell, +39 top comment; hover-lift; broken links; the hand-built-purple contrarian)*
- r/web_design — "...it's gotten worse *rant*" — https://www.reddit.com/r/web_design/comments/1sb2pia/ *(the 3-landing-page test; Lovable/Framer "same sampled design works")*
- r/web_design — "Is AI design becoming desirable?" — https://www.reddit.com/r/web_design/comments/1sk7k6r/ *(the "overused before AI" contrarian)*
- r/vibecoding — "how do I make it not look like AI made it?" — https://www.reddit.com/r/vibecoding/comments/1unm64x/ *(the best telemetry/dashboard critique found anywhere)*
- r/webdev — "Do AI-generated UIs actually maintain design consistency?" — https://www.reddit.com/r/webdev/comments/1rour0f/ *(the design-system-as-context fix)*
- r/graphic_design — "latest issue of tradie looks AI generated" — https://www.reddit.com/r/graphic_design/comments/1dsqjqg/ *(254 comments, all about the imagery, none about layout)*

**Reddit coverage caveat:** searched ~180 queries across r/web_design, r/graphic_design, r/UI_Design, r/userexperience, r/webdev, r/Frontend, r/design_critiques, r/SideProject, r/vibecoding, r/typography, r/SaaS, r/Entrepreneur, r/roastmystartup, r/ChatGPTCoding. **The design subs have far less specific AI-tell discourse than expected** — mostly rants ("everything looks like AI and it's depressing") rather than itemised lists. The itemised taxonomies live in blogs; Reddit supplies the *ranking* (purple first, always), the *contrarians*, and a few tells the blogs miss (hover-lift, equal-weight KPIs, broken links, imagery). Both were needed.

**Trend / counter-aesthetic**
- Daryl Ginn, "The Linear effect" — https://rectangle.substack.com/p/the-linear-effect
- 925studios, "AI Slop Fonts and Gradients" — https://www.925studios.co/blog/ai-slop-design-tells
- 925studios, "Linear Design Breakdown" — https://www.925studios.co/blog/linear-design-breakdown-saas-ui-2026
- Eidos Design, "The Slop Rebellion" — https://eidosdesign.substack.com/p/eidos-design-volume-xxxii-ai-made
- Michal Malewicz, "Slopless" manifesto — https://slopless.design/
- Tubik Studio, "What's Next: 7 UI Design Trends of 2026" — https://blog.tubikstudio.com/ui-design-trends-2026/
- Setproduct, "Vercel aesthetic: Blueprint Grid design" — https://www.setproduct.com/blog/complete-guide-to-blueprint-grid-design
- Nick Simson, "The vibes are off." — https://www.nicksimson.com/posts/2026-the-vibes-are-off.html
- "Aesthetics in the AI era" — https://aigoodies.beehiiv.com/p/aesthetics-2026

**Repost — do not cite as independent**
- developersdigest.tech "16 Patterns" — https://www.developersdigest.tech/blog/ai-design-slop-and-how-to-spot-it *(= Krebs)*
</content>
</invoke>
