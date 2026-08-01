# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Someone on a phone, probably in or near a group chat, idly wondering where they
would actually fit. Not a relocation researcher. The confirmed primary job is
**getting a result worth sending to someone**, not planning a move. People weighing
a genuine relocation are a real secondary audience and the depth is there for them,
but they do not set the design priority.

The idea came from a conversation in a gym change room: someone liked Vancouver's
climate but found the city too big, liked Alberta but not the politics, liked
Halifax except the traffic, liked the town of Goderich but not its snowstorms and
the drive to London. That person is the user.

## Product Purpose

Pick up to five things that matter to you, rank them by the order you pick, answer
only those, and every city and town in the country re-sorts against your answer.
The output is a single place, named, with the reasoning laid out answer by answer.

Success is someone screenshotting the result into a chat.

## Positioning

Every "best places to live" list picks the weights for you. This one asks you, and
then shows its work.

Two things a neighbouring product could not truthfully copy:

1. **The ranking is the reader's, not the publisher's.** Nothing is a recommendation
   and there is no editorial top ten. The order you tap the tiles is the weighting.
2. **A real map on a real projection, drawn from the same geometry the ranking uses.**
   Statistics Canada Lambert for Canada, USGS Albers with Alaska and Hawaii insets
   for the US. Nobody else in this category has this to put on a share card.

Researched competitors (AreaVibes, Livability, Citymatch, Novad, US News, Niche)
have no share mechanic at all, structurally: ranking hubs monetise pageviews so
there is no "your result", and lead-gen quizzes monetise emails so a freely
travelling result fights the model.

## Operating Context

A phone, one thumb, maybe thirty seconds of patience, often arriving from a link
someone else sent. The shared artifact is an image dropped into a chat, not a link
preview. Desktop exists and matters less.

## Capabilities and Constraints

- Two self-contained pages: the USA (4,197 places) at the root, Canada (710) at
  `/canada/`. Fonts, data and map geometry are inlined, so either works offline or
  off a USB stick. Roughly 7 MB raw and 1.3 MB gzipped for the US.
- Static hosting on GitHub Pages. No server, no build step at request time.
- **The entire answer lives in the URL hash.** A hash fragment is never sent to a
  server (RFC 3986 §3.5), so per-result link previews are impossible as built. The
  share card exists because of this constraint, not despite it.
- 26 rankable dimensions in Canada, 24 in the US. French and census-sourced religion
  are Canada-only; the US census is barred by law from asking about religion
  (13 U.S.C. 221) and uses counted places of worship instead.
- Weighted power mean, not a plain average, so a place cannot fail the thing you
  care most about and win by being mediocre elsewhere.

## Brand Commitments

- **Name: "Where U Belong", emphasis on the U.** Doug's, and binding.
- Voice: short, plain, contractions, no em dashes. Never "flat-rate" marketing
  register. State the cost of a result, never only the upside.
- The user has volunteered no binding visual constraint. impeccable.style was shown
  as an install instruction, explicitly **not** as a visual reference.

## Evidence on Hand

Real, sourced, and in the repo. Nothing here is fabricated:

- Climate: Environment Canada normals 1981-2010; NOAA US normals 1991-2020.
- Wildfire smoke: ECCC FireWork Cumulative Effects (CA); Childs et al. 2022
  fire-attributed smoke PM2.5, 2006-2020 (US).
- Census: StatCan 2021 profile plus 2025 estimate; ACS 5-year.
- Politics: Elections Canada 2025 by riding; 2024 presidential by county.
- Water, drive times, OpenStreetMap amenity counts, pro sports and transit, each
  with sources recorded in `research/`.
- Resident research covers 71 of 710 Canadian places and none of the US ones.

Absences that must never be papered over: US religion demographics do not exist;
Alaska and Hawaii have no wildfire smoke figure; 301 US places have no snow record;
New England towns are absent from the US list because the Census files them as
minor civil divisions rather than places.

## Product Principles

1. **Never invent local detail.** Every number traces to a named source. A missing
   value reads `..` and is dropped from the score rather than guessed at.
2. **State the cost.** A result with no stated tradeoff is a horoscope.
3. **The reader's ranking wins.** No editorial thumb on the scale, ever.
4. **Surface the unconsidered.** Ranking thousands of places only earns its keep if
   the answer can be somewhere you have never heard of.
5. **Say what is missing, out loud, in the product.** Every known gap above is
   disclosed in the footer rather than quietly omitted.

## Accessibility & Inclusion

Mobile-first and thumb-reachable; controls clear 44px. Type must survive being read
at arm's length on a phone in daylight. Indian reserves and treaty lands are
deliberately excluded from the rankings: they are real communities but not places
someone can decide to move to, and ranking them as options would be both wrong and
disrespectful.
