# Viral research: what makes a result screen get screenshotted and forwarded

Companion to `flow.md`. That file established the result-screen *composition* (verdict, why, tradeoff, runner-up, provenance, all without a click) and established that **no living, well-designed exemplar exists in the "which city should you live in" genre** — Teleport is dead, Nomad List and Numbeo are anti-references. This file does not redo that. It answers the next question: **once the result is on screen, what makes it leave the screen.**

Verification key: **[V]** = I opened the URL and read the returned content. **[S]** = search-result summary only, weaker, flagged. **[U]** = could not verify.

---

## 1. The competitors, and why the whole genre is share-dead

### What I could open

| Product | URL | What the "result" is | Share mechanic |
|---|---|---|---|
| **AreaVibes** | https://www.areavibes.com/ [V] | A **Livability Score out of 100** attached to an address. Verbatim: *"The Livability Score is then calculated out of 100 for city, neighborhood or address."* Input is *"an address, neighborhood, zip code or city"* — it never asks you anything. Personalization is a sort: *"Sort the list of best places to live by crime, cost of living or schools based on what's most important to you."* | **None found** |
| **Livability** | https://livability.com/best-places/ [V] | An editorial hub of lists — *"Top 100 Best Places To Live"*, *"Best Places To Live by U.S. Region"*, *"Best Places To Live by State"*. No score on the hub. No personalization. | **None found** |
| **Citymatch** | https://www.citymatch.us/ [V] | A quiz → a gated **report**. Verbatim: *"Deciding where to move?"* / *"We Find Perfect Cities For You"* / *"TAKE THE QUIZ"* / *"GET YOUR FREE MATCH"* / *"Get your first match on us."* Free tier is one match; a paid tier exists. | **None found.** The result is the lead magnet. |
| **Novad** | https://novad.app/quiz [V] | 10 questions → **5-7 ranked cities**, each a card with a **match percentage** ("98%"), temperature, cost of living, internet speed, tags, one line of blurb. It positions itself explicitly against personality quizzes that give *"1 city, no explanation."* | **None found** |

### What refused to open, and why that is itself a finding

- **US News Best Places to Live** — https://realestate.usnews.com/places/rankings/best-places-to-live — **WebFetch timed out at 60s.** Not verified. [U]
- **Niche.com Best Places to Live** — https://www.niche.com/places-to-live/rankings/best-places-to-live/ — **HTTP 403 Forbidden.** Not verified. [U]

The two biggest brands in the category both refuse an ordinary HTTP fetch. I am not claiming that proves anything about their design. I am noting the shape: these are ad-and-affiliate businesses that monetise sessions on their own domain, and a business like that has no reason to build an artifact that works away from the page.

### Search-surfaced, not opened [S]

BuzzFeed's "Where Should I Live? Quiz" (https://www.buzzfeed.com/rossyoder/where-should-i-live-ai-quiz), ProProfs (https://www.proprofs.com/quiz-school/story.php?title=what-us-city-should-you-live-in, claimed 9M+ attempts), arealme (https://www.arealme.com/country/en/), CityVibeCheck (https://cityvibecheck.com/vibe-discover.html), LookyLoo (https://lookyloomove.com/quiz), whereshouldilive.co (https://www.whereshouldilive.co/). All [S] — search summary only, do not treat as verified.

### The blunt verdict: uniformly bad, and structurally so

The genre splits into exactly two business shapes, and **both are hostile to a result that travels.**

1. **The ranking hub** (US News, Niche, Livability, Money). There is no "your result" at all. The unit of content is an *article about a city*, so the only shareable object is a link to somebody else's editorial. Nothing on the page is about the reader.
2. **The lead-gen quiz** (Citymatch, LookyLoo, the SEO quiz farms). The quiz exists to capture an email. A result that spreads for free is directly against the model, so the result is thinned, gated, or delivered by mail.

**AreaVibes is the interesting near-miss and the clearest warning.** It has exactly the thing this app has — a score out of 100 on a place — and it is not shared, because a number attached to an address is a *lookup*, not a claim about a person. Novad is the second near-miss: 5-7 cities at 98%, 96%, 94% is a shortlist, and a shortlist is a leaderboard, which `design-refs.md` §1.6 already convicts (*"Ranking is a leaderboard, not an argument"*).

**Not one live product in this category that I could open has a share button, a share image, or any artifact designed to leave the page.** So `flow.md`'s finding extends: there is no well-designed exemplar in the genre *and* there is no exemplar with a share mechanic at all. Every pattern in §2 below is borrowed from outside the category, because there is nothing inside it to borrow.

---

## 2. The share artifact: link or image?

**Answer: an image. And for the things that spread hardest, an image the user makes themselves with a screenshot.**

### 2.1 The screenshot is the baseline mechanism, not the fallback

Monkeytype — a results screen with a devoted community that gets posted constantly — ships **no share affordance at all**. I opened https://monkeytype.com/about [V]: it describes result features (*"watch replay"*, *"tag pb"*, *"raw burst errors"*), and the only save is *"Sign in to save your result"* — which saves the *data*, not an image. There is no share button, no download, no image export mentioned anywhere.

That is the single most useful fact in this section. **A result screen that is composed well enough gets shared with zero share code.** A download button and a `navigator.share` call are optimisations on top of a screenshot, not preconditions for one. Which means: **spend the design budget on what the top of the result screen looks like at phone-screenshot crop, before spending any of it on a canvas renderer.**

Corollary that matters for this app: a phone screenshot captures **the visible viewport**, not the page. So the share artifact is not something you build — it is *whatever happens to be above the fold when the result lands*. That is a layout decision, and it is free.

### 2.2 Where a purpose-built image exists, it is story-shaped or card-shaped, and the numbers are documented

I could not verify Spotify Wrapped's or Strava's sharing mechanics directly — https://support.spotify.com/us/article/spotify-wrapped/ [V, fetched] contains **no** description of how a card is shared, what format it is, or whether it can be saved. **Flagging that as [U]: do not build on "Wrapped exports a 1080x1920 PNG" — I did not verify it.** Receiptify: the current host (https://receiptify.knowlet3211.dev/) failed DNS resolution; **not verified [U]**.

What I *can* verify is the destination format, which constrains anything designed to land there:

- **Instagram Stories** — Meta's own spec, https://developers.facebook.com/docs/instagram-platform/sharing-to-stories/ [V]: background images **minimum 720x1280**, *"Recommended aspect ratios: 9:16 or 9:18"*, JPG/PNG. The conventional render at that ratio is **1080x1920**.
- **Feed / rich-link card** — Meta, https://developers.facebook.com/docs/sharing/webmasters/images/ [V]: *"Use images that are at least 1200 x 630 pixels for the best display on high resolution devices."* *"The minimum allowed image dimension is 200 x 200 pixels."* *"Try to keep your images as close to 1.91:1 aspect ratio as possible to display the full image in Feed without any cropping."* *"The size of the image file must not exceed 8 MB."*
- **Independent corroboration of 1200x630** — Vercel's OG image library, https://vercel.com/docs/og-image-generation [V]: *"Recommended OG image size: 1200x630 pixels"*, and its `ImageResponse` examples all pass `{ width: 1200, height: 630 }`.
- **X / Twitter card dimensions — NOT VERIFIED.** https://developer.x.com/en/docs/x-for-websites/cards/overview/summary-card-with-large-image returned **HTTP 402 Payment Required**. Do not cite the familiar "2:1, 300x157 minimum" figures; I could not open the source. [U]

**So there are two real target shapes and they are incompatible: 1.91:1 landscape for a link preview, 9:16 portrait for a story or a phone screenshot.** You cannot serve both with one asset. See §6 for which one this app should pick.

### 2.3 How the artifact gets out — the three mechanisms, ranked by reliability

1. **Screenshot.** Works on every device, needs no code, and is what people already do. Free.
2. **Download anchor.** `canvas.toBlob()` → `URL.createObjectURL()` → `<a download>`. Verified mechanics in §5.
3. **`navigator.share({ files })`.** Real, but conditional — HTTPS only, must be triggered by a user gesture, and must be feature-detected with `canShare`. Verified in §5.

**What is on the shared image and in what hierarchy** is answered in the spec, §6. The short version, taken from what the competitors get wrong: **the score must not be the first thing.** AreaVibes leads with 88, Novad leads with 98%, and neither travels.

---

## 3. Why anyone would share "You belong in Chester, Pennsylvania"

`flow.md` §2 already covered NFX's eight motives and picked three (identity projection, validation, being helpful). This section does not redo that. It ranks the motives **against this specific sentence**, and adds one motive NFX's list does not name that is probably the biggest lever this product has.

Secondary support, flagged: the NYT Customer Insight Group / Latitude Research **"Psychology of Sharing"** study (2,500 medium-to-heavy sharers) is consistently reported as finding **68% share "to give people a better sense of who they are and what they care about"**, 94% consider whether the information will be useful to the recipient, and 78% share to maintain relationships. **[S] — the primary PDF is on Scribd and I did not open it; these figures came from a search summary over secondary write-ups.** Directionally identical to NFX, which flow.md verified, so nothing below rests on the numbers.

### The ranking, for this result

1. **Identity claim.** Highest by a distance. "You belong in Chester, PA" is a sentence *about the reader*, and the picks that produced it are five things they said mattered. Katz's line from `flow.md` — *"this is who I am, this is where I come from"* — applies directly, with one upgrade: the dialect quiz told you where you're *from*, this tells you where you *belong*. Aspiration is more postable than provenance.
2. **Surprise / disagreement-bait.** Second, and **specific to this product in a way that does not apply to a personality quiz.** "You belong in Chester, PA" is funny and arguable in a way "You are an INFJ" is not, because the reader has an opinion about Chester and no opinion about INFJ. The obscurity of the place is an *asset*: a result naming Austin or Portland is a horoscope, a result naming a town of 32,000 that the reader has never heard of is a claim someone will screenshot to argue with. **Design consequence: do not suppress unfamiliar winners, and do not add a "big cities only" comfort filter.** The weird answer is the viral answer.
3. **Comparison with friends.** Third, and it is the mechanic that turns one share into several: the value of posting your town is that someone replies with theirs. This is the one motive that **requires the link to work**, because the friend has to be able to re-run it as themselves. It is also the reason the app's URL-hash state is worth more than the image.
4. **Being helpful.** Fourth. Real — it is a genuinely useful tool and NFX names this motive [V via flow.md] — but it drives a *DM*, not a *post*, and DMs do not compound.
5. **Bragging.** Effectively unavailable. There is no scarcity, no rank, nothing earned, and "Chester" is not a flex. Do not design for it. Anything that tries to manufacture it (a rarity percentage, a "only 3% of people get this town") is a fabricated statistic and will read as such.

### What makes a result an identity statement rather than a lookup

Four things, all of which the current design either has or can get for free:

1. **It is a sentence in the second person, not a record.** "You belong in Chester, PA" vs "Chester, PA — 94". The first is a claim; the second is a database row. AreaVibes proves the database row does not travel.
2. **The evidence is the reader's own answers, in the reader's own order.** The five-row decomposition `flow.md` §5 specifies is not just an anti-horoscope device — it is what makes the screenshot *legible to a stranger*. A friend scrolling past sees the five things you care about, which is more of an identity disclosure than the town name is.
3. **It names a cost the reader accepts.** The tradeoff line ("what you would give up") is the most identity-loaded element on the screen, because choosing to accept a cost is a character statement in a way that receiving a score is not. This is already item 4 in flow.md's result order; it is also, per this research, the most *shareable* line on the page.
4. **It could have come out differently.** `design-refs.md` §4's test. A result that reads as computed-for-you rather than assigned-to-you is a claim you can own.

### Is 94/100 helpful or harmful?

**Harmful as the hero. Useful as a subordinate line. Do not put it on the share image at all.**

- Harmful because it invites leaderboard framing, and the two products in this category that lead with a number (AreaVibes 88, Novad 98%) [V] are exactly the two that nobody shares.
- Harmful because a big number over small labels is `impeccable.style`'s named **"Hero metric layout"** tell, already convicted in `ai-tells.md` and `flow.md` §6.4 [V via those files].
- Harmful on a *share image* specifically because it invites a rebuttal about method ("94 out of what?") instead of about the place, which is the wrong argument to start.
- Useful on the *result screen* as evidence directly beside the claim, set quieter than its own label, because it is the proof the thing computed something rather than picked something.

There is one honest exception: a score is worth showing when it is **low or middling**, because "your best match in the whole country is a 61" is a genuinely interesting, genuinely shareable admission. A score that is only ever flattering is decoration; a score that can embarrass the tool is data.

---

## 4. Rich link previews, and the hash-fragment wall

### 4.1 The specs, verified

- **The four required Open Graph properties** — https://ogp.me/ [V]: `og:title`, `og:type`, `og:image`, `og:url`. `og:image` is *required*, not optional. Structured sub-properties include `og:image:width`, `og:image:height`, `og:image:alt`.
- **Dimensions** — https://developers.facebook.com/docs/sharing/webmasters/images/ [V]: *"Use images that are at least 1200 x 630 pixels for the best display on high resolution devices."* Minimum *"200 x 200 pixels."* *"Try to keep your images as close to 1.91:1 aspect ratio as possible to display the full image in Feed without any cropping."* *"The size of the image file must not exceed 8 MB."*
- **Caching** — same page [V]: Facebook *"cache[s] all images referenced based on each image's URL"*, so to update one you must *"Use a new URL for the new image"*, and *"The crawler has to see an image at least once before it can be rendered."* Practical: version the filename, and expect the very first share of a new image to preview without it.
- **The 1 MB rule** — https://developers.facebook.com/docs/sharing/webmasters/web-crawlers/ [V]: *"Any Open Graph properties need to be listed before the first 1 MB of your website or app, or it will be cutoff."* Force a re-crawl *"either by passing the URL through the Sharing Debugger tool or by using the Sharing API."*
- **X / Twitter card dimensions — NOT VERIFIED.** https://developer.x.com/en/docs/x-for-websites/cards/overview/summary-card-with-large-image returned **HTTP 402 Payment Required**. [U]

### 4.2 A live finding in this repo, and it is the cheapest fix in this document

Byte offsets measured in `/Users/rohamghiasi/Desktop/Mover Files/livable/index.html` (7,380,323 bytes):

| Tag | First byte offset |
|---|---|
| `<title` | 23 |
| `name="description"` | 128 |
| `og:title` | 526 |
| `twitter:card` | 746 |
| **`og:image`** | **not present anywhere in the file** |

Two consequences:

1. **There is no `og:image`.** Per ogp.me it is one of the four required properties [V], and per Meta *"The crawler has to see an image at least once before it can be rendered"* [V]. Every link shared into iMessage, WhatsApp, Slack, Discord, X or Facebook today renders as a bare text row. One PNG and one meta tag fixes it.
2. **The meta block is safe today but structurally fragile.** The tags sit in the first 750 bytes, well inside Meta's 1 MB cutoff — but the file is 7.38 MB. If a build change ever emits the embedded dataset above the meta block, previews die silently with no error anywhere.

(Read-only measurement. Nothing under `app/`, `src/` or any data file was touched.)

### 4.3 Why per-result OG images are impossible as currently built

Not hard — **impossible**, and the reason is a protocol fact.

**RFC 3986 §3.5** — https://www.rfc-editor.org/rfc/rfc3986 [V], verbatim: the fragment identifier *"is not used in the scheme-specific processing of a URI; instead, the fragment identifier is separated from the rest of the URI prior to a dereference, and thus the identifying information within the fragment itself is dereferenced solely by the user agent, regardless of the URI scheme."*

The server never receives the hash. A crawler requesting `https://…/where-to-live-canada/#picks=smoke,cost,water` receives exactly the same bytes as a crawler requesting the bare URL. There is no mechanism by which a hash-stated result can vary an OG tag.

**And GitHub Pages has no request-time code.** https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages [V]: *"GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files straight from a repository on GitHub, optionally runs the files through a build process, and publishes a website."* (Honest note: that page did **not** contain an explicit "no server-side code" statement; the absence of a runtime is implied by "static site hosting service", not quoted. [I])

For contrast, the mainstream solution requires exactly the runtime a static host does not have. Vercel's OG library — https://vercel.com/docs/og-image-generation [V] — generates images *"using Vercel Functions"*, i.e. a function invoked per request, at *"Recommended OG image size: 1200x630 pixels"*. That is the shape of the thing that is unavailable here.

### 4.4 The options, honestly priced

| Option | What it takes | What it buys | Verdict |
|---|---|---|---|
| **A. One generic OG image** | One PNG, one meta tag | Every share gets a real preview card instead of a grey box. Nothing personalised. | **Do this now.** It is the honest answer for v1 and it is the fix for §4.2. |
| **B. Per-city static stubs, per-city images** | Build step emitting ~4,907 HTML files (4,197 US + 710 CA) at real paths like `/r/us/chester-pa/`, each with its own `og:title` and its own generated PNG, each hydrating into the app | Preview shows the town name *and* a town-specific image | Highest cost. Still cannot encode the reader's picks — those are combinatorial and un-prerenderable. |
| **C. Per-city stubs, one shared image** | Same ~4,907 tiny HTML files, but all pointing at a single `og:image` | Preview headline reads *"You belong in Chester, Pennsylvania"* | **The one worth pricing after A.** ~80% of the effect for ~1% of B's cost, because the *title* is the text a recipient actually reads before tapping. |
| **D. A serverless function elsewhere** | A second host | Full dynamism | Rejected. Adds a server to a static app to solve a preview. |

**Is a single well-designed generic OG image the honest answer? Yes — for now.** It is the only option that requires no change to how state is stored, and it removes a real, currently-live failure. Option C is the upgrade path and it does require moving the shared winner out of the hash and into the path.

**What other static quiz sites do about this: I could not verify a single documented case.** I found no source describing how a static, hash-state quiz handles per-result OG images. Flagged as [U] rather than guessed.

---

## 5. Canvas share-card mechanics

Every claim here is from a spec page I opened.

### 5.1 Sizing

**Do not use `devicePixelRatio` for an exported share image.** MDN's high-DPI recipe — https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio [V] — is for a canvas *displayed on screen*: set `canvas.style.width` in CSS pixels, set `canvas.width` to `Math.floor(size * window.devicePixelRatio)`, then `ctx.scale(scale, scale)` to normalise the coordinate system.

That is the right pattern **only if you show the card in the page**. For an export, the file must be identical on every device, so the export canvas is a fixed pixel size (§6: 1080 x 1350) and there is no `devicePixelRatio` in the maths at all. If you also want an on-screen preview, render once at export size offscreen and display it with a CSS width — the browser downscales it and it stays sharp on retina for free.

### 5.2 Fonts, and the failure that is completely silent

- `document.fonts.ready` — https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/ready [V] — returns a Promise that *"will only resolve once"* the document *"has completed loading fonts"*, *"layout operations are completed"*, and *"no further font loads are needed."*
- **The trap:** `fonts.ready` only guarantees fonts the *document layout* needed. A weight or size drawn only onto the canvas may never have been requested by the DOM, so `fonts.ready` resolves and `ctx.fillText` still renders in a fallback face. Canvas throws no error and logs no warning for a missing font. You find out when someone posts a card set in Helvetica.
- **Fix:** `await document.fonts.load('700 120px "Radio Canada"')` for **each exact weight/size string you will draw**, then `await document.fonts.ready`, then draw.

### 5.3 Getting the bitmap out

`HTMLCanvasElement.toBlob()` — https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob [V]:
- Signature `toBlob(callback)` / `toBlob(callback, type)` / `toBlob(callback, type, quality)`. **Asynchronous, callback-based** — wrap it in a Promise.
- *"Default type is `image/png`"*; if an unsupported type is passed, *"`image/png` is used instead"*. `quality` applies *"only for lossy compression formats"*.
- The callback argument may be `null` *"if the image cannot be created for any reason"* — handle it.
- **`SecurityError`** is thrown *"if the canvas's bitmap is not origin-clean"*, i.e. if anything drawn onto it came from another origin. Inline every asset.
- Encoded resolution metadata is **96dpi**.

### 5.4 `navigator.share` with files

From https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share [V] and https://web.dev/articles/web-share [V]:

- `shareData` accepts `url`, `text`, `title`, `files`. *"All properties are optional but at least one known data property must be specified."* `title` *"may be ignored by the target."*
- **Feature-detect with `canShare`, not `share`.** web.dev, verbatim: *"Notice that the sample handles feature detection by testing for `navigator.canShare()` rather than for `navigator.share()`."* The canonical guard:
  ```js
  if (navigator.canShare && navigator.canShare({ files: filesArray })) { … }
  ```
- **Transient activation is mandatory.** MDN: *"It must be triggered off a UI event like a button click and cannot be launched at arbitrary points by a script."* web.dev: *"It must be invoked in response to a user action such as a click"* and *"It can only be used on a site that is accessed via HTTPS."*
- File types: *"Certain types of audio, image, pdf, video, and text files can be shared."* PNG is fine.
- Exceptions: `NotAllowedError` (policy blocked, no transient activation, or file share blocked), `TypeError` (bad data, or *"Files are specified but the implementation does not support file sharing"*), `AbortError` (*"user canceled the share operation or no share targets available"*), `DataError`.
- In a third-party iframe you need `allow="web-share"`.

**iOS Safari:** https://caniuse.com/web-share [V] shows Web Share supported in Safari on iOS from **12.2** onward and in desktop Safari from **12.1**. **caniuse's table does not break out Level 2 / `files` support, so I could not verify from it whether iOS Safari accepts a `files` array. [U]** Treat file sharing as unknown on any given device and gate it on `canShare({files})` at runtime.

### 5.5 What commonly breaks

1. **The `await` eats the user gesture.** `navigator.share` needs transient activation. If the click handler awaits font loading and `toBlob` before calling `share`, activation can lapse and you get `NotAllowedError`. **Render the blob before the button is pressed; the handler should do nothing but call `share`.**
2. **Silent font fallback.** §5.2. No error, no warning.
3. **Tainted canvas → `SecurityError` on `toBlob`.** Any cross-origin bitmap without CORS.
4. **`AbortError` on cancel is normal.** Catch it and do nothing — never surface an error when someone dismisses a share sheet.
5. **`AbortError` also fires when there are no share targets** — indistinguishable from a cancel. This alone means the download anchor must always exist.
6. **Blob URL leaks.** `URL.revokeObjectURL(url)` after the download fires.
7. **The filename is user-visible** in the share sheet and in Photos. `you-belong-in-chester-pa.png`, not `canvas.png`.
8. **Canvas has no line breaking.** `fillText` will not wrap. Place names in this dataset range from "Ajax, ON" to things like "Saint-Louis-du-Ha! Ha!, QC" — you must measure with `ctx.measureText` and step the display size down until it fits, or the longest names run off the card. With 4,907 possible winners this is not an edge case; it is the most predictable production failure on the list.
9. **`toBlob(null)`.** Handle the null-blob case.

---

## 6. The spec: this app's share card

### Dimensions

**1080 x 1350 px, 4:5 portrait.** Exported at exactly that size, device-independent.

Why this and not the alternatives:
- The baseline share mechanism is a **phone screenshot** (§2.1), which is portrait. A portrait card matches what people already make.
- **1200 x 630 (1.91:1)** is a *link-preview* format [V, Meta] — correct for `og:image`, dead as a screenshot artifact.
- **1080 x 1920 (9:16)** is the story format [V, Meta: min 720x1280, *"9:16 or 9:18"*] — it survives a story and gets destroyed in a feed.
- 4:5 is the tallest ratio that posts uncropped to a feed and still centre-crops acceptably into a story. It also gives the vertical room the five-row decomposition needs, which the landscape format does not.

**These are two different assets.** `og:image` is 1200 x 630 and generic (§4). The share card is 1080 x 1350 and personal. Do not try to make one file do both.

### Layout, top to bottom

Ground: the app's existing cool off-white paper. Ink: the app's near-black. One warm accent, used **once**. No gradient, no shadow, no dark variant, no rounded container, no card-inside-a-card.

Margin **90px** on all sides → a 900px live column. Everything left-aligned. Nothing centred.

1. **Hairline rule, then the tool name**, set at body size in the body weight, left. ~28px. That is the entire branding. No logo, no lockup, no eyebrow label, no pill.
2. **The verdict, as one sentence in two sizes.**
   - `You belong in` — 44px, regular.
   - **`Chester, Pennsylvania`** — ~120px, the largest element on the card, allowed to wrap to two lines, auto-fitted down per §5.5 item 8. This is the only thing that must be legible at thumbnail size.
   - Underneath, quiet: population and county/region, 26px. Only facts the app already holds — invent nothing.
3. **The five-row decomposition — the reason the card is portrait.** One row per pick, **in the reader's own pick order**, carrying the reader's own rank number. Three columns, hairline rule between rows, 30px:
   ```
   1   wildfire smoke     you said: as little as possible     cleanest 8% in the US
   2   housing cost       you said: under $1,400              $1,180 median
   3   near water         you said: yes                       Delaware River, 1 km
   ```
   Unanswered picks print `not provided`, per the GOV.UK check-answers pattern already adopted in `flow.md` §5.
   This block is what makes the card readable to a stranger scrolling past. It is a portrait of the reader, not of the town — which is precisely the identity mechanism §3 ranks first.
4. **The tradeoff, one line, unhedged**, 32px, with air above it. *"What you'd give up: it's eight hours to an international airport."* Per §3 this is the most identity-loaded line on the card, and it inoculates the post against the obvious first reply.
5. **The runner-up, one line**, 26px. *"Runner-up: Coatesville, PA. Same everything, cheaper."*
6. **Foot**, 24px, quietest ink: the data epochs and the bare domain, one line.

**Type: four sizes only** — 120 / 44 / 30 / 24, plus 26 if the runner-up needs its own step. `design-refs.md` §0 Bug 3 convicts the app's current 20 sizes; the Pudding ships 5 and Low-Tech 6. Radio Canada throughout, **two weights maximum**.

### What to cut

- **The score.** §3. It belongs on the result screen, quieter than its own label; it does not belong on the card.
- **The map.** 4,197 dots at 1080px is a smudge.
- **Any photograph of the town.** There is no verified photo for 4,907 places, and a generic skyline is the loudest AI tell there is to a non-designer audience (`ai-tells.md` §7b: a 254-comment roast thread about one stock photo, zero comments about layout).
- Logo lockup, QR code, watermark, app-store badge, "Take the quiz" button.
- Any percentage, ring, gauge, bar, or progress element.
- Emoji.
- Gradients, glows, accent rails on a card edge, nested cards, rounded 24px+ corners — all named in `ai-tells.md` §9.

### The share text

The `text` field of `navigator.share`, and the string behind the copy button:

```
You belong in Chester, Pennsylvania.
https://rohamghiasicw-star.github.io/where-to-live-canada/#…
```

Nothing else. It is the same sentence as the card, so the post reads as one statement rather than a caption plus an ad. No hashtag, no emoji, no exclamation mark, no "I got", no percentage, no "take the quiz".

**Do not ship:** `I'm a 94% match for Chester, PA! 🏙️ Take the quiz:` — the score invites an argument about method instead of about the place (§3), the emoji is a named tell, and "take the quiz" makes the sharer sound like an affiliate.

For the **link-preview** surface, which is a different job: if per-city stubs get built (§4 option C), `og:title` = `You belong in Chester, Pennsylvania`. Until then, a fixed `og:title` that is **a question about the reader**, not a boast about the tool — the dialect quiz's opening move, already noted in `design-refs.md` §2.

---

## 7. Viral levers ranked by impact / effort

1. **Ship an `og:image` at all.** There isn't one (§4.2). Every link shared today previews as a grey text row. Cost: one PNG plus one meta tag. Benefit: every share, on every platform, forever. **Best ratio in this document, not close.**
2. **Design the result screen's first viewport to be the share artifact.** Free. Requires only that `flow.md`'s result items 1-3 fit above the fold at 375px with no scroll. §2.1 (Monkeytype) is the evidence that this alone is enough.
3. **One-sentence share text behind the existing "Send this to someone" button.** Tiny. Stops the sharer writing weaker copy than yours.
4. **Decide not to suppress obscure winners.** Zero effort — it is a decision to *not build* a "major cities only" comfort filter. Possibly the largest single lever on share rate (§3, motive 2: an unfamiliar town is arguable; Austin is a horoscope).
5. **Per-city OG title stubs sharing one image** (§4 option C). Medium: a build step emitting ~4,907 small HTML files at real paths. The title is the only text a recipient reads before deciding to tap.
6. **The 1080x1350 canvas card with a download button.** Real effort (font preloading, text measurement, fitting). Do it after 1-4, and ideally only once 2 has shown people are screenshotting.
7. **`navigator.share({files})` layered on top of the download button.** Small increment once 6 exists. Never a replacement for it (§5.5 item 5).
8. **Per-city OG images.** ~4,907 generated PNGs. High cost, and it still cannot encode the reader's picks. Probably never worth it.

---

## 8. Do not do

1. Do not put the score on the share card.
2. Do not build the canvas card before confirming a plain screenshot of the result screen already looks right.
3. Do not make `navigator.share` the only exit. `AbortError` fires both on user-cancel and on no-share-targets and the two are indistinguishable [V, MDN] — the download anchor must always exist.
4. Do not do async work inside the share click handler; transient activation expires and you get `NotAllowedError` [V, MDN]. Pre-render the blob.
5. Do not draw without `await document.fonts.load()` for each exact weight/size string. Canvas font fallback is completely silent [V, MDN].
6. Do not draw any cross-origin bitmap onto the export canvas — `toBlob` throws `SecurityError` on a non-origin-clean canvas [V, MDN].
7. Do not put a stock photo, a skyline, or an AI-generated image of the town on the card.
8. Do not add a QR code, logo lockup, watermark, or app-store badge.
9. Do not write share copy containing "I got", a percentage, a hashtag, an emoji, or an exclamation mark.
10. Do not attempt to pre-render OG images that encode the reader's picks. The picks are combinatorial; only the winner is enumerable.
11. Do not let a build change move the meta block below the embedded dataset. Meta cuts off after 1 MB [V] and the file is 7.38 MB.
12. Do not use 1200x630 as the screenshot artifact. It is a link-preview format only.
13. Do not add a share-to-unlock gate, an email wall, or a "see your full results" step. That is the Citymatch model [V] and it is exactly why nobody shares Citymatch.
14. Do not invent a rarity statistic ("only 2% get Chester") unless it is computed from real session data.
15. Do not add confetti, a share counter, or a "142 people got this town today" ticker. Chayka names ticker-style bars specifically as a Claude-look tell (`ai-tells.md` §2.2).
16. Do not build a "compare with a friend" feature before the plain link works. Motive 3 in §3 is already served by the URL hash for free.
17. Do not centre the card's contents, and do not put a letterspaced all-caps label above the town name — both named in `ai-tells.md` §9 and `flow.md` §6.

---

## 9. Contradictions with existing research, called out

- **`flow.md` §6.14: "Do not generate a share image."** Partially contradicted. Its priority is right and I keep it: the top of the result screen is the primary share artifact and must be designed first (§7 item 2). But its stated grounds — *"a separate generated card is a second thing to design badly"* — argue for **sequencing**, not prohibition. Position: canvas card is item 6 of 8, contingent on item 2 shipping first. If forced to pick one forever, flow.md wins.
- **`flow.md` §5 item 7 assumes the link surface is handled** because *"the link carries the state."* It carries the state for a human, not for a crawler. The hash never reaches the server (RFC 3986 §3.5 [V]) and there is currently **no `og:image` at all** (§4.2), so a link pasted into any chat app previews as a bare grey row. That gap is not addressed anywhere in flow.md and it is the cheapest fix in this document.
- **`flow.md` §2's "no separate share card is needed"** rests on the assumption that both share motives are served by one screen. That holds for the screenshot and the DM. It does **not** hold for the link preview, which is a third surface with its own asset and its own dimensions.
- **No contradiction with `ai-tells.md`.** The card spec clears every item on its do-not list: no hero metric, no eyebrow, no gradient, no dark mode, no accent rail, no three-card row, no emoji, no stock photo, four type sizes, two weights.
- **One live tension:** a share card is *structurally* a hero-metric layout unless the hero is a proper noun. The spec resolves it by making the largest element the place name. The moment a score migrates onto the card, the tell returns.

### Could not verify — stated plainly

- **US News Best Places to Live** — WebFetch timed out at 60s. **Niche.com** — HTTP 403. Neither was assessed.
- **Spotify Wrapped and Strava share mechanics and dimensions.** The Spotify support page I opened contains nothing about sharing. Do not cite "Wrapped exports 1080x1920" from this file.
- **Receiptify.** DNS failure on the current host; not opened.
- **X / Twitter card dimensions.** HTTP 402 Payment Required.
- **Whether iOS Safari supports `navigator.share` with `files`.** caniuse shows Web Share from iOS 12.2 but does not break out Level 2.
- **Whether Meta's crawler executes JavaScript.** Its crawler doc says nothing about it. The "before the first 1 MB" phrasing implies source-reading, but that is inference [I], not a quote.
- **What any specific static quiz site does about per-result OG images.** No documented case found. §4.4 is reasoned from the specs, not copied from a precedent.
- **NYT "Psychology of Sharing" figures** (68% / 94% / 78%) — [S], secondary write-ups only; the primary is a Scribd PDF I did not open.
- **GitHub Pages "no server-side code."** Implied by *"static site hosting service"*; no explicit statement on the page I opened. [I]

---

## Source list (opened and read, this file only)

1. AreaVibes — https://www.areavibes.com/ [V]
2. Livability, Best Places — https://livability.com/best-places/ [V]
3. Citymatch — https://www.citymatch.us/ [V]
4. Novad quiz — https://novad.app/quiz [V]
5. Monkeytype, About — https://monkeytype.com/about [V]
6. Open Graph protocol — https://ogp.me/ [V]
7. Meta, Sharing image specs — https://developers.facebook.com/docs/sharing/webmasters/images/ [V]
8. Meta, Web crawlers (1 MB cutoff, user agents, cache) — https://developers.facebook.com/docs/sharing/webmasters/web-crawlers/ [V]
9. Meta, Sharing to Instagram Stories (9:16, min 720x1280) — https://developers.facebook.com/docs/instagram-platform/sharing-to-stories/ [V]
10. Vercel, OG image generation (1200x630, requires functions) — https://vercel.com/docs/og-image-generation [V]
11. RFC 3986 §3.5, Fragment — https://www.rfc-editor.org/rfc/rfc3986 [V]
12. GitHub Docs, About GitHub Pages — https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages [V]
13. MDN, `HTMLCanvasElement.toBlob()` — https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob [V]
14. MDN, `Navigator.share()` — https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share [V]
15. MDN, `FontFaceSet.ready` — https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/ready [V]
16. MDN, `Window.devicePixelRatio` (retina canvas recipe) — https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio [V]
17. web.dev, Web Share API (files, `canShare`, HTTPS, user activation) — https://web.dev/articles/web-share [V]
18. caniuse, Web Share API — https://caniuse.com/web-share [V]
19. Spotify Support, Wrapped (fetched; contained nothing on sharing) — https://support.spotify.com/us/article/spotify-wrapped/ [V, negative result]

**Opened and failed:** https://realestate.usnews.com/places/rankings/best-places-to-live (60s timeout) · https://www.niche.com/places-to-live/rankings/best-places-to-live/ (HTTP 403) · https://developer.x.com/en/docs/x-for-websites/cards/overview/summary-card-with-large-image (HTTP 402) · https://receiptify.knowlet3211.dev/ (DNS failure)

**Search-summary only, not opened [S]:** buzzfeed.com "Where Should I Live? Quiz" · proprofs.com · arealme.com · cityvibecheck.com · lookyloomove.com · whereshouldilive.co · the NYT/Latitude "Psychology of Sharing" figures via contently.com, foundationinc.co and other secondary write-ups
