# Typography: is your stack the reason it "looks way too AI"?

Research date: 2026-07-16. Companion to `ai-tells.md` (which this builds on and, in one place, corrects).

Current stack under review:
- **League Gothic** — condensed display
- **IBM Plex Sans** — body
- **IBM Plex Mono** — data/labels

Loaded as base64 woff2 data URIs via `fonts/faces.css` + `fonts/faces.json` (96K / 200K). Swapping faces is mechanically cheap.

---

## 0. The short answer

**Your fonts are very likely not what your critic reacted to.** Not one of the three appears on any AI-tell list I could find, and I looked hard, including the only systematic catalogue that exists (impeccable.style, 46 patterns).

**But you asked me to be honest, so:** there are two real findings that cut against a clean bill of health, and one of them is a genuine hole in your existing research.

1. **The ALL-CAPS letterspaced mono label is a confirmed, multi-source AI tell.** Not the font. The *pattern*. If you are using IBM Plex Mono for tracked-out uppercase eyebrows above headings, that is the single most-named typographic tell in the literature, and you're doing it. This is the thing to fix.
2. **IBM Plex is being actively prescribed to AI as the "Technical" aesthetic** by the most-copied frontend-design guidance in circulation, including Anthropic's own cookbook. It is not burned *yet*. It is on the exact runway that burned Inter. Your `ai-tells.md` §3.7 checked whether designers criticise Plex (they don't, correctly) but never checked what AI is being *told* to use. That's the leading indicator, and it's flashing.

**The deeper problem is not slop, it's fit.** You're building a Canadian geography/almanac/reference tool and typesetting it in a corporate technical UI stack. IBM Plex is a *fine* typeface that is wearing the wrong clothes for this job. It says "developer tooling," not "field guide." That mismatch reads as thoughtless, and thoughtless is what people mean when they say "AI."

---

## 1. Is IBM Plex an AI/LLM tell?

### The case for "no" (strong, and it's the majority of the evidence)

**impeccable.style/slop — the only systematic catalogue of AI-generated UI patterns (46 patterns, live detection overlay).** Pattern #15 is literally called "Overused font." It names:

> "Inter, Geist, Space Grotesk, and the newest reflex, Instrument Serif" — used "on so many sites they no longer feel distinctive."
> — https://impeccable.style/slop/

IBM Plex is **not named**. Neither is anything in the Plex family.

**Typewolf's most-popular-fonts data (drawn from 3,000+ sites):** the 2026 top 15 is Apercu, GT America, Futura, Founders Grotesk, Neue Haas Grotesk, Canela, Graphik, Proxima Nova, GT Walsheim, Avenir, Maison Neue, Circular, Brandon Grotesque, Ogg, Helvetica Neue. **IBM Plex does not appear.**
— https://www.typewolf.com/recommendations

**Typewolf's own IBM Plex Sans page** describes steady professional adoption, not saturation. Recommended alternatives: Adelle Sans, Akkurat.
— https://www.typewolf.com/ibm-plex-sans

**Other AI-tell inventories name Inter, not Plex:**
- prg.sh: "Inter, Roboto, or Arial (the 'safe' system fonts that appear in thousands of examples)" — https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website
- 925studios: "Inter is a fine typeface" but "is also the default font in nearly every AI design tool, component library, and website builder" — https://www.925studios.co/blog/ai-slop-web-design-guide
- Kyle Chayka's essay names large italic serifs and tracked-out subheadings, no sans — https://kylechayka.substack.com/p/the-generic-style-of-ai-web-design

**Root cause of the Inter problem, for context:** Adam Wathan (Tailwind's creator) publicly apologised in Aug 2025 for making every Tailwind UI button `bg-indigo-500`, because it became the median of the training data. The AI "isn't designing, it's averaging." Plex was never a framework default, so it never entered that averaging loop.

**Verdict on the lagging indicator: IBM Plex is not an AI tell. Your `ai-tells.md` §3.7 is correct on the evidence it examined.**

### The case for "not so fast" (new — this is what §3.7 missed)

§3.7 asked: *do designers criticise IBM Plex?* Answer: no. But that's the lagging indicator. The question that predicts the next Inter is: **what is AI being instructed to reach for?**

**Anthropic's own Claude Cookbook, "Prompting for frontend aesthetics"** — a widely-copied document — gives this exact list:

> **Impact choices:**
> - Code aesthetic: JetBrains Mono, Fira Code, Space Grotesk
> - Editorial: Playfair Display, Crimson Pro, Fraunces
> - Startup: Clash Display, Satoshi, Cabinet Grotesk
> - **Technical: IBM Plex family, Source Sans 3**
> - Distinctive: Bricolage Grotesque, Obviously, Newsreader
>
> **Never use:** Inter, Roboto, Open Sans, Lato, default system fonts
>
> — https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics

Read that carefully. **"IBM Plex family" IS the officially-recommended escape hatch from Inter, filed under exactly the register you are using it in: "Technical."** Every developer who follows this guidance to avoid slop lands on Plex.

This is not an isolated doc:
- **aitmpl.com "Premium Web Design" skill** (a distributed Claude Code skill) recommends **IBM Plex Sans** in its sans-display list and **IBM Plex Mono** in its monospace-accent list, for "editorial quality labels, categories, dates." — https://www.aitmpl.com/component/skills/creative-design/premium-web-design
- **xAI's DESIGN.md** (VoltAgent's awesome-design-md collection) names **IBM Plex Mono** as a documented alternate for the mono role. — https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/x.ai/DESIGN.md

Note the pincer: the Cookbook says "never use Inter" and "use IBM Plex for technical." Space Grotesk got burned the same way — it was the *recommended alternative* to Inter two years ago, and impeccable.style now lists it as a top-4 tell. Bricolage Grotesque is repeating the cycle right now (Google Fonts popularity rank #48 and climbing; it appears in the Cookbook's "Distinctive" list).

**Honest verdict on Plex:** Not a tell today. Nobody's critic in July 2026 is looking at Plex and thinking "AI." But it is the single most-prescribed anti-Inter move in AI design guidance, aimed squarely at the "technical" aesthetic, which is the aesthetic you've built. Treat it as a face with a 12-to-18-month shelf life in this specific register. **It is not urgent. It is also not the differentiator you think it is.**

The real knock on Plex here isn't slop — it's **fit**. Plex is IBM's corporate UI face, the Carbon Design System default, engineered for enterprise software. It is genuinely well-made (Mike Abbink + Bold Monday, 100+ languages, real italics). It is also, for an almanac, *costume*: it performs "technical" rather than being editorial.

---

## 2. Is League Gothic / condensed uppercase display an AI tell?

**No. This is the cleanest part of your stack, and I found zero evidence against it.**

- **impeccable.style's 46 patterns do not include condensed display type.** Not League Gothic, not Oswald, not Anton, not Archivo Black, not Bebas Neue. The typography section (patterns 8–17) covers flat hierarchy, icon tiles, *italic serif* display, eyebrows, kickers, oversized headlines, crushed tracking, overused fonts (Inter/Geist/Space Grotesk), single-font pages, and all-caps body. Condensed is absent.
- **AI reaches for neo-grotesques and editorial serifs, not condensed.** That's the consistent pattern across every source. The AI hero is an *oversized italic serif*, per impeccable #10 and Chayka. Condensed display is a human choice.
- **League Gothic is not on Typewolf's top-15.** — https://www.typewolf.com/recommendations
- **It has real pedigree:** based on Alternate Gothic (Morris Fuller Benton, 1903), released by The League of Moveable Type. — https://www.typewolf.com/league-gothic

**The one caveat is within the condensed category, and it isn't about AI — it's about cheapness.** Bebas Neue is the burned one: "arguably the most widely used free condensed font in the world," the "Netflix font," which "screams confidence but has zero versatility — it's a sledgehammer, not a screwdriver." — https://madegooddesigns.com/best-condensed-fonts/

League Gothic is the *least* saturated of the free condensed group and has the best historical grounding. **Keep it, or change it for character reasons, not slop reasons.** Your `ai-tells.md` §3.6 already reached this and it holds up.

---

## 3. Is monospace-for-UI-labels a tell?

**This is your actual problem. Yes — emphatically, multi-source, named verbatim. And it is the one thing in your stack that all the evidence converges on.**

To be precise about what's guilty: **the font is innocent, the pattern is guilty.** Nobody flags "using a mono." Everybody flags **the tiny tracked-out ALL-CAPS label**.

**impeccable.style names it twice in the 46:**

> **#11 "Hero eyebrow / pill chip"** — "A tiny uppercase letter-spaced label sitting immediately above an oversized hero headline," or rendered as a pill chip. Called **"the default AI SaaS hero."**

> **#12 "Repeated section kicker labels"** — "Repeating tiny uppercase tracked labels above section headings turns a brand page into **AI editorial scaffolding**."

Three more of the 46 compound it if you're doing them:

> **#17 "All-caps body text"** — long uppercase passages, since "we recognize words by shape" (ascenders/descenders), which caps destroy.
> **#46 "Wide letter spacing on body text"** — tracking above 0.05em.
> **#27 "Numbered section markers"** — "01 / 02 / 03" as section labels.

— all https://impeccable.style/slop/

**Corroborated independently:**
- **Kyle Chayka (New Yorker staff writer), on the generic AI style:** "Subheadings are often **'tracked out**,' in design parlance, with spaces between letters." — https://kylechayka.substack.com/p/the-generic-style-of-ai-web-design
- **aiskill.market:** monospace-everything "looks like a hackathon project, not a product"; the tiny uppercase letterspaced label above an oversized hero is "the default AI SaaS hero." — https://aiskill.market/blog/typography-systems-for-ai-uis
- **xAI's own DESIGN.md specs it as house style:** "Geist Mono uppercase tracked for labels," carrying "captions and eyebrows at 1.2–1.4px positive letter-spacing." — https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/x.ai/DESIGN.md

That last one is the smoking gun for *why* it's a tell: it's a documented house style at a frontier AI lab, published to a scraped repo of design specs, which then gets replicated by every model trained on it.

**Note the tension your `ai-tells.md` §4.1 flagged and it's worth preserving:** monospace as a *typographic trend* is genuinely live and legitimate. Typewolf's 2026 trend read says "monospace fonts have broken free from their utilitarian origins and become a genuine design trend in branding, editorial design, and packaging." So mono isn't poison. **The specific eyebrow/kicker construction is.**

### What to do instead (concrete)

Keep a mono. Kill the eyebrow.

- **Delete hero eyebrows entirely.** If the label carries no information the headline doesn't, it's decoration. Almanacs don't have eyebrows.
- **If you need a section marker, set it in the body face**, sentence case, at body size, as a real line of text — not tracked caps floating above a heading.
- **Restrict mono to things that are actually tabular:** coordinates, elevations, populations, dates, census figures, source lines. That's *earned* mono, and on a geography tool you have genuinely tabular data — this is the rare project where mono is honest rather than costume.
- **Kill positive tracking on anything that isn't a short uppercase run.** If you keep any caps label, tracking stays ≤0.05em (impeccable #46).
- **Never `01 / 02 / 03`.**

---

## 4. Alternatives — 12 named faces you can download and self-host

All verified: names, licenses, download URLs, and whether woff2 ships in-repo. Sizes noted where relevant, since you're base64-ing into a data URI (base64 inflates ~1.33x).

### Tier 1 — the strong recommendations for this project

**1. Radio Canada + Radio Canada Big** ⭐ *the find*
- Coppers and Brasses (Montréal) — Charles Daoud, Alexandre Saumier Demers, Jacques Le Bailly. Big by Étienne Aubert Bonn.
- Humanist/institutional grotesque, **variable**: `wght` 300–700, `wdth` 75–100.
- **Commissioned for CBC/Radio-Canada, Canada's public broadcaster.** Literally institutional Canadian type, built for a national bilingual reference/news service. Extended in 2023 to cover the **Unified Canadian Aboriginal Syllabics** Unicode block — for a Canadian geography tool that is a real, substantive advantage, not a nice-to-have. Won Communication Arts Typography 2018. The `wdth 75` axis gives you condensed for tight map labels and table headers *from the same family*.
- **SIL OFL 1.1.** Self-host, subset, modify — all fine.
- https://fonts.google.com/specimen/Radio+Canada · https://fonts.google.com/specimen/Radio+Canada+Big · repo: https://github.com/cbcrc/radiocanadafonts
- Google Fonts popularity #329 / #729 — genuinely underused.

**2. Fraunces**
- Undercase Type (Phaedra Charles + Flavia Zimbardi). Serif, variable.
- Old-style serif with deliberate wobble and warmth, explicitly built *against* neutrality. Verified axes: `opsz` 9–144, `wght` 100–900, **`SOFT` 0–100** (crisp→rounded terminals), **`WONK` 0/1** (binary toggle swapping in the wonky alternates: the singular leg of the `g`, swashy `y` and `f`). The opsz range plus WONK is what makes it feel hand-set rather than webby.
- **SIL OFL 1.1.** ⚠️ Caveat: it's in the Claude Cookbook's "Editorial" list, so it carries mild prescription risk — but its axis space lets you make it yours in a way a static face can't.
- https://github.com/undercasetype/Fraunces (richest; **110 .woff2 in `fonts/webfonts/`**) · https://fonts.google.com/specimen/Fraunces

**3. Literata**
- TypeTogether. Serif, variable: `opsz` 7–72, `wght` 200–900.
- Commissioned as the **Google Play Books** reading face — engineered for exactly your use case: long-form reference reading on screen. Sturdy, slightly condensed, warm without folksiness. Reads "publishing house," not "website." The safest workhorse text serif here.
- **SIL OFL 1.1.** https://fonts.google.com/specimen/Literata · Popularity #212.

**4. Newsreader**
- Production Type. Serif, variable: `opsz` **6**–72, `wght` 200–800.
- Built for on-screen news reading. The `opsz` low end of 6pt is the widest here — it holds together at genuinely small sizes (footnotes, source lines, table cells) where Playfair-class faces shatter. Warm, open, slightly quirky terminals.
- **SIL OFL 1.1.** https://fonts.google.com/specimen/Newsreader · Popularity #148.

**5. Recursive**
- Arrow Type (Stephen Nixon). Variable sans/mono hybrid.
- **The most useful axis set for a data-heavy reference tool.** Verified: **`MONO` 0–1** (proportional sans → true monospace on a slider), **`CASL` 0–1** (Casual: linear/neutral → warm and brushy), `CRSV` 0–1, `slnt` -15–0, `wght` 300–1000. One file gives you body sans, warm editorial voice, *and* a metrically-related tabular mono for coordinates. `CASL` is literally a warmth dial.
- **SIL OFL 1.1.** https://fonts.google.com/specimen/Recursive · Popularity #703 — wildly underused for what it does.

**6. Young Serif**
- Bastien Sozeau (noirblancrouge). Display serif, variable `wght`.
- Chunky, slab-ish, generous old-style display serif with real presence. Reads like a **national park sign or a field-guide cover**. Listed on both Uncut and Google Fonts — quality signal without mass adoption.
- **SIL OFL 1.1** (verified OFL.txt). **11 .woff2 in `fonts/webfonts/`** incl. variable `Young-Serif[wght].woff2`.
- https://github.com/noirblancrouge/YoungSerif · https://fonts.google.com/specimen/Young+Serif · Popularity #637.

### Tier 2 — characterful, all OFL, all woff2-ready

**7. Karrik** — Velvetyne
- Jean-Baptiste Morizot + Lucas Le Bihan. Vernacular grotesque.
- Built from "uneven garage letterings, nameless fonts of obscure and discontinued foundries" — deliberate weight disadjustments, no optical corrections, uneven widths. Reads cleanly at body size, keeps its strangeness at display. `SS01` unlocks a chaotic alternate uppercase referencing garage lettering. **Its stated theme is phantom and ghost towns** — for a Canadian geography tool full of tiny place names and abandoned settlements that's almost too on the nose. The exact anti-Inter.
- **SIL OFL 1.1.** **woff2 in `fonts/Web/WOFF2/`** (Regular 30.4 KB).
- https://velvetyne.fr/fonts/karrik/ · https://gitlab.com/phantomfoundry/karrik_fonts/-/archive/master/karrik_fonts-master.zip

**8. Compagnon** — Velvetyne
- Duhé, Pradine, Papon, Lozano, Riollier, 2018. Typewriter-derived.
- Drawn from Typewriter Database specimens, merging typewriter eras into one family. **Five weights** (Light→Bold), unusually deep for a typewriter face. **Field-notes / survey-record mood — ideal for a field guide, and a far better "data" face than Plex Mono for this project** because it's honest rather than technical-costume.
- **SIL OFL 1.1.** **woff2 included** (~18–36 KB/weight).
- https://gitlab.com/velvetyne/compagnon/-/archive/master/compagnon-master.zip

**9. Sligoil** — Velvetyne
- Ariel Martín Pérez, 2022 (updated 2025). Monospace.
- Large inktraps, drawn for the game *Unknown Number*; references Matthew Carter, Irish whiskey distillery signage, and MIT Space Cadet keyboards. 784 glyphs, Vietnamese support. **Ships a variable font** (`SligoilVF.woff2`, 51 KB).
- **SIL OFL 1.1.** https://gitlab.com/velvetyne/sligoil/-/archive/main/sligoil-main.zip

**10. Fanwood** — The League of Moveable Type
- Barry Schwartz. Serif. Revival of Vojtěch Preissig's work.
- **Ships separate `Text` optical variants** (Regular, Italic, Text, Text Italic) — rare in libre type, and exactly the body/display split you want from one family. 449 glyphs, 15 OT features, covers `°` natively.
- **SIL OFL 1.1.** ⚠️ **No woff2** — 2010-vintage repo ships otf/ttf/woff. One `fonttools` pass fixes it.
- https://github.com/theleagueof/fanwood/archive/master.zip

**11. Sorts Mill Goudy** — The League of Moveable Type
- Barry Schwartz. Goudy Oldstyle revival. 425 glyphs, **small caps, oldstyle + lining figures, fractions**. This is *the* reference-book face — small caps and oldstyle figures are what make an almanac index look typeset rather than rendered.
- **SIL OFL 1.1.** ⚠️ **No woff2** — conversion needed.
- https://github.com/theleagueof/sorts-mill-goudy/archive/master.zip

**12. Martian Mono** — Evil Martians
- Roman Shamin. Monospace, variable: **`wdth` 75–112.5**, `wght` 100–800.
- For coordinates and tabular data. The `wdth` axis is the differentiator — condense to 75 to fit lat/long pairs into narrow map callouts without dropping size. Engineered and legible **without the JetBrains/Geist Mono startup-terminal association**.
- **SIL OFL 1.1.** https://fonts.google.com/specimen/Martian+Mono · Popularity #806.

### Bonus, for the Canadian angle

**Latitude + Equateur** — Velvetyne, revived from the **Ange Degheest** archive (Eugénie Bidaut, Oriane Charvieux, Mandy Elbé et al.). Beyond the obvious gift of the names for a geography tool, these are archive revivals of a mid-century woman type designer's lost work rediscovered at the Rennes School of Fine Arts — real provenance for a reference project. Regular only, so display/accent, not body. **OFL 1.1.** https://velvetyne.fr/fonts/degheest/

---

## 5. Faces to avoid, and why

**Ruled out on slop grounds** (named tells): Inter, Geist, **Geist Mono**, Space Grotesk, Instrument Serif, **Instrument Sans** (same designers as Instrument Serif — same project, same association), Roboto, Open Sans, Lato, Arial/system defaults.

**Ruled out on prescription risk** (in the Cookbook/skill lists, burning now): Playfair Display, Clash Display, Satoshi, Cabinet Grotesk, Switzer, General Sans, **Bricolage Grotesque** (GF popularity #48 and climbing — it has real character but reads as "2024 tasteful default"; it's where Space Grotesk was two years ago).

**Ruled out on cheapness**: Montserrat and Poppins — "decent" but "associated with free templates and budget projects due to extreme overuse" (https://madegooddesigns.com/popular-fonts/). Bebas Neue.

**Ruled out on register**: **Public Sans** — it's the US federal government face, institutional but *deliberately* neutral, which is the opposite of the warmth you asked for.

### ⚠️ Fontshare: a licensing landmine — read this before you use it

You asked me to investigate Fontshare specifically. **Its aesthetics are good and its license is a genuine problem for you.** The ITF Free Font License text (bundled as `License/FFL.txt`, identical to the web version) is **self-contradictory**:

- **Clause 01 grants** use "in any media (including Print, **Web**, Mobile, Digital, Apps, ePub, Broadcasting and OEM)," commercial, worldwide, unlimited.
- **Clause 02 forbids**: "You are **not allowed to transmit the Font Software over the Internet in font serving or for font replacement** by means of technologies such as but not limited to EOT, Cufon, sIFR or similar technologies that may be developed in the future without the prior written consent of the Licensor."
- **Yet the ZIP ships** `Fonts/WEB/fonts/*.woff2` + a README titled **"Installing Webfonts"** telling you to put it on your website.
- **No modification**: "You may not modify, edit, adapt, translate, reverse engineer, decompile... in whole or in part, without the prior written consent." **This forbids subsetting.**
- Fontshare labels these **"Closed Source"** on the font page itself.

The only web route the EULA explicitly blesses is the **Fontshare CDN API** — which means a third-party CDN dependency, and **that kills your data-URI self-hosting approach outright.**

For a reference tool you'll maintain for years, **go OFL**. Every Tier 1/2 face above is OFL 1.1. (If you ever do want them: **Zodiak** is the best pure almanac serif I found — Century-model, "thick slab-like serifs bracketed onto their stems," nineteenth-century even-width caps; and **Bespoke Serif/Slab/Sans** is the most complete superfamily. Both are worth knowing about. Neither is worth the license mess.)

Also worth correcting: **Khand, Familjen Grotesk, Crimson Pro, Public Sans, Literata and Space Grotesk on Fontshare are mirrored OFL Google Fonts**, not ITF originals — they carry `license_type: sil_ofl`.

**Uncut.wtf note:** it's a *catalogue*, not a host — every entry links out to its own foundry, so **licenses vary per font and must be checked at source**. It also carries Geist and Instrument Serif/Sans, so it is not a safe-harbour from the AI look.

---

## 6. What does an actual almanac/atlas use?

You asked for the institutional/governmental reference point. Here's what's real:

- **National Geographic** uses a **proprietary in-house system** designed by **Charles E. Riddiford** in the 1930s under chief cartographer Albert H. Bumstead, still in use digitally today. "Every feature is associated with a specific typeface, and colour and typographic weight (from light to bold) further add to this distinction." — https://www.nationalgeographic.com/maps/article/national-geographics-cartogaphic-typefaces · https://www.smithsonianmag.com/arts-culture/the-secret-to-national-geographics-maps-is-an-80-year-old-font-22205390/

  **The transferable lesson isn't the font — it's the system.** Nat Geo encodes *meaning* in type: feature class → typeface, magnitude → weight, category → colour. That is the single most almanac-authentic move available to you, and it's free. A geography tool where a river, a city, and a provincial boundary are typographically distinguishable is doing something no AI default does, because it requires knowing your data.

- **Government of Canada / Canada.ca**: design standard specifies **Lato** for headings, **Noto Sans** for body. Both chosen for language coverage. — https://design.canada.ca/styles/typography.html
- **Federal Identity Program**: the official typeface is **Helvetica** (incl. Neue/Now). — https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/typography-design-standard-fip.html
- **The Canada wordmark** is a **modified Baskerville**, with the original's thin strokes thickened. — https://fontsinuse.com/uses/38191/canada-wordmark

Note that Canadian federal typography is *deliberately neutral* (Helvetica, Lato, Noto) — it is not the warmth you're after, and Lato is on the Cookbook's "never use" list anyway. **Radio Canada is the better read on "institutional Canadian":** it's the only Canadian public-institution face that is simultaneously OFL, characterful, bilingual by design, and Indigenous-syllabics-capable.

**On the serif question specifically:** be aware there's now an active backlash. WIRED, June 2026 — "AI Has Come for Serif Fonts" — reports designers calling AI-adjacent serif branding **"tasteslop."** Designer Keya Vadgama coined "the serif renaissance," arguing AI-native companies reach for serifs because "AI is inherently cold and without opinion," and notes **Claude, Runway, Perplexity and Manus** all default to serifs. Critics online call the result "generic" and "very ugly." — https://www.wired.com/story/ai-has-come-for-serif-fonts/

**So: a serif is not automatically the escape from the AI look. In 2026 an unearned serif is itself becoming the AI look.** The defence is that yours is *earned* — an almanac has an actual, historical, non-decorative reason to be set in a book serif. That reason has to be visible in how you use it (oldstyle figures, small caps, real optical sizes, footnotes), not just asserted by picking one.

---

## 7. Three pairings I'd actually recommend

### Pairing A — "The Canadian institution" ⭐ my pick
- **Display:** Radio Canada Big
- **Body:** Radio Canada (`wght 400`), condensing to `wdth 75` for map labels and table headers
- **Data/tabular:** Martian Mono (`wdth 75–85` for coordinate pairs)
- **Optional editorial accent:** Young Serif for section openers only

**Why:** a Canadian geography and reference tool typeset in the Canadian public broadcaster's own institutional typeface, by a Montréal foundry, with Indigenous syllabics support — that is a *defensible idea*, not a font choice. It's the answer to "why this type?" that no AI would produce, because it requires knowing what the project is. All OFL, all self-hostable, one variable family covers display+body+condensed, so your data-URI payload likely *shrinks*. Warm, legible, zero startup smell. Popularity #329 — nobody's burned it.

**Risk:** it's a grotesque, so the "warmth" is institutional-warm, not bookish-warm. If you want the almanac feel, add Young Serif or go to Pairing B.

### Pairing B — "The field guide"
- **Display:** Young Serif
- **Body:** Literata (`opsz` responsive) or Newsreader if you need sub-8pt
- **UI/labels:** Radio Canada (`wdth 75` where tight)
- **Data:** Compagnon (typewriter, survey-record texture) or Recursive at `MONO 1`

**Why:** this is the register you actually asked for — warmth, editorial character, national-park-sign display over a genuine reading serif. Literata is engineered for long-form on-screen reading, which is literally your use case. Compagnon over Plex Mono for data is the key swap: it says "field notes," not "IBM Carbon." All OFL, all woff2 in-repo except none — no conversion needed.

**Risk:** the serif-backlash exposure from §6. Mitigate by earning it: oldstyle figures inline, real optical sizing, small caps in the index.

### Pairing C — "The vernacular almanac" (highest character, highest risk)
- **Display:** Sorts Mill Goudy (small caps + oldstyle figures) or ChunkFive for broadside headlines
- **Body:** Fanwood Text (built-in optical variants) or Petrona
- **UI/labels:** Karrik (`SS01` off for labels, on for accents)
- **Data:** Sligoil (variable, 51 KB)

**Why:** this is the one that could not possibly be mistaken for AI. Goudy small caps and oldstyle figures are 1911 reference-book typography, and Karrik's ghost-town vernacular is thematically perfect for Canadian place names. Nothing in this pairing appears in any AI guidance anywhere.

**Risk:** real work. Sorts Mill Goudy and Fanwood are 2010–2011 League repos that **ship otf/ttf/woff but no woff2** — you need a `fonttools`/`ttf2woff2` conversion step. And Goudy at small sizes on screen needs care. This is the connoisseur option; take it only if you'll actually tune it.

---

## 8. If you only do three things

1. **Kill the tracked-out ALL-CAPS mono eyebrow.** This is the only item here with unanimous multi-source evidence against it (impeccable #11, #12, #46; Chayka; aiskill; xAI's own spec). It is almost certainly what your critic's eye caught. Everything else in this document is optional.
2. **Swap IBM Plex → Radio Canada.** Not because Plex is burned — it isn't — but because it's the prescribed "Technical" AI default in Anthropic's own cookbook, and more importantly because it's the wrong costume for an almanac. Radio Canada is better-fitting, better-storied, equally free, and actually Canadian.
3. **Steal Nat Geo's system, not their font.** Encode meaning in type: feature class → face, magnitude → weight, category → colour. That's the thing an AI can't fake, because it requires knowing your data.

**Keep League Gothic** unless you want to change it for taste. It's clean.

---

## Source list

Primary evidence:
- https://impeccable.style/slop/ — the 46-pattern catalogue (patterns #8–17 typography, #11/#12 eyebrows, #15 overused fonts, #27, #46)
- https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics — "Technical: IBM Plex family, Source Sans 3"; "Never use: Inter, Roboto, Open Sans, Lato"
- https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/x.ai/DESIGN.md — "Geist Mono uppercase tracked for labels"; IBM Plex Mono as alternate
- https://www.aitmpl.com/component/skills/creative-design/premium-web-design — IBM Plex Sans + IBM Plex Mono in recommended lists
- https://kylechayka.substack.com/p/the-generic-style-of-ai-web-design — "tracked-out" subheadings, cream/beige, italic serifs
- https://www.wired.com/story/ai-has-come-for-serif-fonts/ — "tasteslop," the serif renaissance, Vadgama
- https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website — Inter/Roboto/Arial; Wathan's indigo-500 apology; "averaging, not designing"
- https://www.925studios.co/blog/ai-slop-web-design-guide — Inter as the AI-tool default
- https://aiskill.market/blog/typography-systems-for-ai-uis — "default AI SaaS hero"; monospace-everything

Usage/trend data:
- https://www.typewolf.com/recommendations — 2026 top 15 (no Plex, no League Gothic)
- https://www.typewolf.com/top-10-favorite-fonts — underused list
- https://www.typewolf.com/ibm-plex-sans · https://www.typewolf.com/league-gothic · https://www.typewolf.com/bebas-neue
- https://madegooddesigns.com/popular-fonts/ — Montserrat/Poppins overuse
- https://madegooddesigns.com/best-condensed-fonts/ — Bebas Neue "sledgehammer"

Foundries/faces:
- https://velvetyne.fr/ · https://uncut.wtf/ · https://www.fontshare.com/ · https://www.theleagueofmoveabletype.com/ · https://www.collletttivo.it/
- https://github.com/cbcrc/radiocanadafonts · https://www.coppersandbrasses.com/custom-work/radio-canada/ · https://cbc.radio-canada.ca/en/fonts-radio-canada
- https://github.com/undercasetype/Fraunces · https://github.com/noirblancrouge/YoungSerif
- https://fonts.google.com/specimen/{Radio+Canada, Radio+Canada+Big, Fraunces, Literata, Newsreader, Recursive, Young+Serif, Martian+Mono, Petrona}

Canadian/cartographic reference:
- https://design.canada.ca/styles/typography.html — Lato + Noto Sans
- https://www.canada.ca/en/treasury-board-secretariat/services/government-communications/design-standard/typography-design-standard-fip.html — Helvetica
- https://fontsinuse.com/uses/38191/canada-wordmark — modified Baskerville
- https://www.nationalgeographic.com/maps/article/national-geographics-cartogaphic-typefaces — Riddiford system
- https://www.smithsonianmag.com/arts-culture/the-secret-to-national-geographics-maps-is-an-80-year-old-font-22205390/
