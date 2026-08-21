# What Doug is actually telling us

Read across all his messages, not just the latest one.

| When | What he sent |
| --- | --- |
| Jul 17 | "Your work is excellent... I will work in a document to make it sticky, personal and most importantly - viral" |
| Jul 17 | USA is the better opening country, more diverse weather |
| Jul 20 | `Where U Belong.docx` - rename, pick ~5 of ~20 and **rank** them |
| Aug 14 | Globe and Mail piece + "there are many articles like this, therefore the App had to be more personalized" + "20 or more categories... either 5 or 10 preferred categories (weighted)" |
| Aug 14 | PDF: 20 alternative reasons people choose a city |
| Tue | The list **again**, now 15 categories, plus a specific weighting scheme, plus a worked example |

**He has now sent the same core idea four times: categories, pick five, rank them,
weight them.** Nobody repeats themselves four times because they have new
information. They repeat themselves because they cannot see it landed.

## His 15 against what is already built

| Doug's category | In the app | As |
| --- | --- | --- |
| Weather - temperature | YES | Winter, Summer |
| Weather - rain / snow | YES | Rain, Snow |
| Weather - change of seasons | YES | Seasons |
| Population | YES | Size of place |
| Transit | YES | Rapid transit |
| Drivability / commute | YES | Short commute |
| Proximity to water | YES | Near water |
| Cost of living | YES | Housing budget |
| Political (red / blue / purple) | YES | Politics |
| Proximity to larger cities | YES | Near a city |
| Dating scene | **PARTLY** | three separate questions - Single people, Gender balance, Who lives there - never combined into one keyed to your age |
| **Outdoor activities** | **NO** | hiking, bicycling, skiing - nothing |
| **Culture and events** | **NO** | arts venues are in the OSM pull now, events are not |
| **Healthier lifestyle** | **NO** | nothing |
| **Inclusive vibe** | **NO** | he flags himself that it is hard, and he is right |

Eleven of his fifteen already exist. The app has **24 dimensions in the US and 26
in Canada**, which is more than the twenty he asked for.

## So the real message is one of two things, probably both

1. **He cannot see the list.** The picker is 24 tiles in three groups and on a
   phone that is well past one screen. His own screenshot from Aug 7 was taken
   mid-page. He may never have scrolled to "Life there".
2. **The four he keeps naming are the four that do not exist.** Outdoors,
   culture, health, inclusive. He is not repeating himself at random - he is
   repeating the gap.

## And the line he ended on is a different complaint entirely

> "If people put something down as 1st, the output needs to reflect this"

That is not about categories. That is about output, and it is **correct** -
see the measurement below.

## The weighting: he diagnosed it right and his fix would not have worked

Measured, not argued.

Rank **the short commute first** among five picks and the winner is Hillsboro OR,
which scores **41 out of 100** on it. The pick ranked first was the pick sacrificed,
and nothing on screen said so.

Share of total weight going to the first pick:

| Scheme | 1st | 2nd | 3rd | 4th | 5th |
| --- | --- | --- | --- | --- | --- |
| Current (5,4,3,2,1) | **33%** | 27% | 20% | 13% | 7% |
| Doug's (10,7,6,5,1) | **34%** | 24% | 21% | 17% | 3% |
| Exponential (16,8,4,2,1) | **52%** | 26% | 13% | 6% | 3% |

Doug's scheme moves the first pick from 33% to 34%. It is the same curve.

I built the exponential version and ran it: **the commute-first answer did not
move.** Hillsboro still won, still at 41%.

**The cause is not the weighting.** It is that a short commute and rapid transit
are anti-correlated in America. Small towns have the commute, big cities have the
trains, and almost nowhere has both. Isolating it:

```
commute alone            -> Hays KS          100%
commute + summer         -> Alpena MI         99%
commute + prox           -> McPherson KS      99%
commute + mix            -> Storm Lake IA    100%
commute + transit        -> Clayton MO        55%   <- the collapse
```

No weight curve fixes a request the country cannot satisfy. What the app owed him
was to **say so**, and it did not: the "nowhere is both X and Y" note existed but
was gated on the OVERALL fit being under 62. Hillsboro scores 79, because the
other four picks carry it. Now gated on the pick instead.

## What is left to do

The four missing categories are in deep research now, one agent each, same
standard as the last round: real download URL, real join key, measured coverage,
and a stated verdict including "cut it" where that is the honest answer.

---

# Verdict 1 of 4: Inclusive vibe - CUT

Doug wrote "tougher to pull this data". He was right, and the evidence is worse
than he guessed. Full notes in `research/src-inclusive.md`.

| Source | What killed it |
| --- | --- |
| **HRC Municipal Equality Index** | Real and current, but **PDF only** - no CSV, no API. The join was actually run: **449 of 4,226 places match, 10.6%**. And that is the ceiling, not a starting point: HRC states the 506-city list "has been the number of cities rated since 2016". No open licence, copyright HRC. |
| **Movement Advancement Project** | State level by design, in their own words. Their one municipal list excludes "municipalities in states with statewide protections", so a missing city means two opposite things - verified LA, SF, Seattle, Boston, NYC, Chicago all absent. |
| **FBI hate crime** | Geography is the law-enforcement agency, not a place. Measured from the real file: among 2,114 reporting city agencies, **52.1% reported exactly one incident all year, median 1**. The FBI's own methodology says it "does not apply offense estimation procedures to account for missing data". The ORI-to-place crosswalk is 2012 and login-walled. |
| **Canada** | Finest geography StatCan publishes is the **CMA**. Built the real CSD-to-CMA correspondence for all 712 places: 35.8% sit in a published CMA, 44.1% are outside any CMA or CA entirely, and the ones that match share only 41 values - **Montreal CMA alone would hand 77 different CSDs the identical number.** Zero of 712 places would get a value measured at their own geography. |

**The trap to name out loud:** the tempting substitute is share of same-sex
households, or a diversity index. Do not. That tells a reader a place is
inclusive because of who already lives there, which is a different claim and not
one the data supports.

The only honest version is a **badge, not a score**: "Rated 100/100 on HRC's 2025
Municipal Equality Index, which scores city laws and policies on LGBTQ+
inclusion", shown on the ~449 rated places, with no value and no penalty
anywhere else - and only with HRC's permission, since there is no open licence.

Every real measure here scores the **government**, not the place, and all three
sources say so themselves.

---

# Verdict 2: Healthier lifestyle - SHIPPED (US)

CDC PLACES physical inactivity, place level, 4,188 of 4,197. San Diego 19.8%,
Kansas City MO 29.7%, KS 35.3% - Doug's own test, working. One named measure,
not a health score, on CDC's own instruction. PA and KY are absent from the 2025
release entirely (both failed the BRFSS minimum) and are backfilled from 2024.
Modelled estimates, said so in the hint. Canada floors at health region: 712/712
join but 711 places share only 106 values, so six BC mountain towns read
identically. Deferred, not shipped.

# Verdict 3: Skiing - SHIPPED (both countries)

OpenSkiMap, nightly from OSM, operating downhill areas with at least one lift:
**526 US, 236 Canada**. Straight-line km, said so in the hint. Ski alone returns
Lebanon NH at 0 km; ski plus an active place returns Steamboat Springs.

Hiking and bicycling are NOT shipped, and for a measured reason. The USGS
national trail layer's coverage is state-dependent - **Vermont 8,495 miles
against Rhode Island 32.5**, a 260x gap that is about who mapped it, not who has
trails. Ranking on it would put Rhode Island towns last for a fake reason. For
bicycling, no US agency publishes lane mileage at all: not FHWA, not BTS, not
Census, all three checked. The honest proxy is ACS bike-commute share, which is
already sitting in `places.json` unused.

# Two defects this round found in our OWN work

**1. `craft=*` was polluting the arts count.** Measured across the Canadian pull,
the tag in North America is electrician, builder, hvac, plumber, roofer, floorer,
insulation. A plumber is not an arts scene, and counting one puts
population-correlated noise into the single dimension meant not to be
population. Now an explicit maker allowlist. No refetch needed - the data was
already pulled, only the classification changed.

**2. The 15 km radius breaks down around dense cities.** Measured from our own
file:

| Place | arts within 15 km |
| --- | --- |
| **Hoboken NJ** (pop 60k) | **1,540** |
| Jersey City NJ | 1,539 |
| **New York NY** | **1,538** |
| Union City NJ | 1,475 |

Hoboken outscores New York City because a 15 km disc from its centroid swallows
Manhattan. For the five reachability dimensions this is fine and intended - "is
there a vet I can drive to" is a question about what you can reach, and the file
says so. For **arts it is wrong**, because "is this an arts town" is a question
about the place, not its neighbours.

**So arts is the one OSM dimension not shipping yet.** The fix is per-capita on
the exclusive column, which independent work found is genuinely uncorrelated with
population (spearman -0.107, against 0.925 for raw counts). The other five ship
on the radius column as designed.
