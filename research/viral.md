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
