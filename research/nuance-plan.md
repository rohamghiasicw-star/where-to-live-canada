# Nuance dimensions - plan

Source: Doug's PDF, 2026-08-14, `research/doug-top20-alternative-reasons.pdf`
("Top 20 Alternative Reasons People Choose a City to Move To"), plus his texts
the same night and Roham's note: **"need more nuance type of searching, not just
stats type searching."**

## First, what Doug asked for structurally is already built

> "if we come up with 20 or more categories for people to pick from to come up
> with either 5 or 10 preferred categories (weighted)"

The app has **24 categories in the US, 26 in Canada**, you pick up to 5, and tap
order is the weight. That part exists. What he is actually pushing on is the
*kind* of category, not the count or the mechanism.

**Recommendation: keep the cap at 5, grow the menu to ~38.** At 10 picks the
10th counts a tenth of the first, which is noise pretending to be an opinion,
and it turns a 5-screen flow into a 10-screen one. The lever is a wider menu,
not a longer answer.

## The framing, because it decides what gets built

Nuance is not the opposite of measurable. Doug's list is *more* measurable than
the current one, not less. Dog parks, dark skies, ferries, farmers markets and
direct international flights are all countable. What makes them feel nuanced is
that they are **specific to how you would actually live**, where the generic
best-places list is cost of living, job growth and a crime index.

So: most of the 20 can be built without breaking the app's own rule that nothing
is invented. Four or five genuinely cannot, and those are named below rather
than faked.

## Tier 1 - the Overpass pipeline already does this, just more tags

`src/build_osm.py` and `src/us/build_osm.py` already run one area-scoped
OpenStreetMap query per place for pitches, worship and rinks. Eight of Doug's 20
are the same query with more tags. Cheapest real work on the list.

| Doug's reason | Tags |
| --- | --- |
| Pet infrastructure | `leisure=dog_park`, `amenity=veterinary` |
| Walkability / 15-minute city | `shop=supermarket|convenience`, `amenity=pharmacy|school|cafe` |
| Subculture alignment | `amenity=arts_centre|studio`, `tourism=gallery`, `leisure=hackerspace`, `craft=*`, `shop=music|books` |
| Local food sovereignty | `amenity=marketplace`, `shop=farm|greengrocer` |
| Continuing education | `amenity=library|college|university` |
| Healthcare niche access | `amenity=clinic|doctors|hospital`, `healthcare=*` |
| Public transit quirks | `amenity=bicycle_rental`, `route=ferry`, `railway=subway_entrance` |
| Volunteering ecosystems | `office=ngo|charity`, `amenity=social_facility|animal_shelter` |

## Tier 2 - real national datasets, one new pull each

Each needs its own fetch and join. Listed with the source I intend to use.
**None of these are verified yet** - verification is step one of the build, and
anything that turns out to be paywalled, stale or too coarse gets cut, not
guessed at.

| Doug's reason | Intended source | Coverage risk |
| --- | --- | --- |
| Dark sky | VIIRS nighttime lights annual composite, sampled at each place | Low, it is a global raster |
| Walkability, as a real index | EPA National Walkability Index (US), Can-ALE (CA) | Block-group, needs aggregating to place |
| Disaster resilience | FEMA National Risk Index (US) | **No Canadian equivalent** |
| Digital connectivity | FCC Broadband Data Collection (US), ISED/CRTC national broadband (CA) | Both exist, different shapes |
| Airport global connectivity | OpenFlights routes + the drive-time engine in `build_proximity.py` | Low |
| Multilingual / expat density | ACS language spoken at home, StatCan mother tongue | Low, same census pipeline as French |
| Noise pollution | BTS National Transportation Noise Map (US) | **No Canadian equivalent** |
| Micro-climate: humidity | Relative humidity already in NOAA and ECCC normals | Low |
| Dating market | Already have gender balance and never-married %. Reframe, no new data | None |

## Tier 3 - cannot be built honestly, and should be said out loud

No national dataset exists for these at 710 and 4,197 places. Any version would
be me writing a vibe and calling it data, which is the one thing the app
promises not to do.

- **Social pacing** (hyper-fast super city vs slow regional). Only a proxy from
  density and commute time, which is the stats layer wearing a costume.
- **Acoustic and visual aesthetics** (architectural style, landscape vibe).
- **Local governance style** (participatory budgeting, neighbourhood councils).
- **Allergy relief.** Pollen data is commercial and patchy.
- **Tax and incentive perks.** Real but tiny: roughly a few dozen North American
  towns run relocation-grant programs. Shippable only as a hand-sourced flag on
  those specific places, each with its own link. Not a national field.

The honest home for the Tier 3 material is the **resident-research field that
already exists in the schema** (`lived`, currently 71 of 710 Canadian places and
0 US). That is where "what living here is actually like" belongs, sourced and
attributed to residents, not computed.

## Build order

1. Verify every Tier 2 source resolves, is free, and is joinable at place level. Cut what does not.
2. Tier 1 - one Overpass pass per country, 8 new dimensions.
3. Tier 2 - the survivors, cheapest join first.
4. Wire into `Q_ALL` with `cc` gates so US-only and CA-only dimensions stay on their own country, the way religion already does.
5. Re-check the picker at ~38 tiles. That many needs group headers to stay scannable, and the guide's "up to five" card gets more important, not less.

## Open question for Roham

Tier 1 alone takes the menu from 24 to 32 and costs one Overpass run per country.
Tier 2 is the bigger spend and where the Canada gaps bite. Worth doing both, or
ship Tier 1 first and see whether Doug's point lands?

---

# VERDICTS after source verification (2026-08-18)

Five agents opened and downloaded from the real endpoints. Full notes in
`research/src-*.md`. Nothing below is from memory.

## SHIPPING - confirmed real, confirmed joinable

| Dimension | Source | Join | Coverage |
| --- | --- | --- | --- |
| 6 OSM dimensions (dog, arts, local food, learning, health, volunteering) | Overpass | 15 km radius of the place point | pull running |
| Language spoken at home | ACS **C16001** (US) / StatCan 98-401-X2021005 (CA) | place GEOID / CSD | **4,226/4,226 and 712/712** |
| Broadband | FCC BDC "Summary by Geography Type - Census Place" | **7-digit GEOID direct** | 305/305 sampled, 0 missing |
| Natural hazard risk | FEMA National Risk Index county CSV (US) | `STCOFIPS` via `place_county.json` | 3,231 counties |
| Earthquake risk (CA) | NRCan Seismic PSRA | **`csduid` direct** | 5,162 rows |

Two traps recorded so they are not rediscovered later:

- **FCC: never use `technology = "Any Technology"`.** It counts Starlink, so it
  reads ~1.000 everywhere and separates nothing. Use `Any Terrestrial` + `Fiber`.
- **ACS: the table is C16001, not B16001.** B16001 has *zero* place-level rows;
  it stops at PUMA. And the Summary File flips the column name: `C16001_E003`
  where the API says `C16001_003E`.

### Also confirmed usable, second wave

| Dimension | Source | Join | Note |
| --- | --- | --- | --- |
| Dark sky | VIIRS VNL V2 via **Zenodo 10.5281/zenodo.17294744**, CC-BY-4.0 | sample raster at lat/lon | one global file covers both countries |
| Walkability (US) | EPA National Walkability Index, `NatWalkInd` | block group -> place | **use the 2010 Block Assignment Files**, 2020 silently drops 13% of Providence |
| Walkability (CA) | **StatCan Proximity Measures Database**, OGL | `CSDUID` already a column | ten indices, compose your own |

Three traps recorded:

- **EOG's own VIIRS download went paid on 1 June 2026.** Every path under
  `eogdata.mines.edu/nighttime_light/` now 302s to a login. The Zenodo mirror is
  the same VNL V2 data - its embedded TIFF tag names the original EOG file - and
  needs no account. Values are rescaled 0-2000, not raw radiance.
- **Can-ALE ships with no licence at all.** GitHub reports `license: null` and
  there is no LICENSE file, so it is default copyright with no grant of
  redistribution. It joins at 100% and is tempting. Do not use it in a public
  app. StatCan's Proximity Measures Database is the licensed answer and needs no
  crosswalk at all.
- **EPA's published walkability CSV writes the GEOID in scientific notation**
  (`4.8113E+11`). Rebuild it from `STATEFP+COUNTYFP+TRACTCE+BLKGRPCE`.

## CUT - and the reason, so nobody re-proposes them

| Dropped | Why |
| --- | --- |
| **Transportation noise** | Canada has no national noise data and never will: TP 1247E says contours are the airport operator's property and "Transport Canada does not retain copies". Full catalogue sweeps of Toronto, Ottawa, Mississauga, Vancouver, Edmonton, Halifax, Surrey, Ontario GeoHub and the BC Data Catalogue returned **zero**. Canada-wide coverage is ~1.3% and mostly unlabelled airport zoning polygons. The US product exists but is a 1.6 GB Esri mosaic raster GDAL could not open, and BTS itself says it "should not be used to evaluate noise levels in individual locations". |
| **Humidity / micro-climate** | Half of all places sit 25 km+ from a humidity station (US median 24.9 km, CA 20.8 km, against a 4.1 km baseline for temperature). NOAA publishes dew point but no RH; ECCC publishes RH but no dew point. Deriving RH from normal-T and normal-Td is not the normal RH, and the bias is unpublished. Two countries, opposite derivations, mismatched time bases. |
| **Airport connectivity** | OpenFlights routes have been frozen since **June 2014** - the file still lists AirTran and US Airways. BTS T-100 works for the US but only covers US-touching segments, so Canadian transatlantic service is invisible. StatCan gives movement *volume*, not destinations. The two countries cannot be put on one scale. |
| **IRS / CRA non-profits** | Both files are real, but neither carries a place code, so it means geocoding ~902k US orgs and point-in-polygon against TIGER. Naive city matching gets 64% and fails *systematically on large cities*. The OSM `volunteer_orgs` count already answers the same question at no join cost. |

## Known gap this turned up, not part of this task

The Canadian climate normals **1991-2020 are published** and the app is still on
**1981-2010**. Worth its own pass.

## Overpass note for whoever runs this next

A regex alternation - `["amenity"~"^(library|college|university)$"]` - cannot use
the tag index and makes Overpass scan every amenity in the area. Measured on
Newfoundland: the regex form returns 504, the identical tags as separate exact
matches return in 13 seconds. Every tag line in `TAG_BATCHES` is an exact match
for that reason, and the batches exist to keep each request inside the endpoint's
time budget.
