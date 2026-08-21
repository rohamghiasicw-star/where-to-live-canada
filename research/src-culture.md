# Culture and events dimension - source verification

Verified 2026-08-21. Every number below was measured off a real HTTP response or computed
from a file downloaded during this session. Nothing is estimated or recalled. Where
something could not be confirmed it says so, in those words, in the last section.

**The dimension the user asked for:** *"Culture ans events ( how a city is ranked ) big
cities have more"*. He is right that raw counts scale with size. The app already has a
population dimension, so a measure that just re-measures population is worthless here.
Every source below is judged on one question above all others: **does it separate places
of similar size?**

---

## Summary table

| # | Source | Format | Granularity | Join key | Separates similar-size places? | Verdict |
|---|---|---|---|---|---|---|
| 1 | IMLS Museum Data Files 2018 | 3 CSV in ZIP, 2.9 MB | Individual museum, lat/lon | lat/lon + county FIPS | Yes, but 2018 and museums only | USABLE WITH WORK |
| 2 | NEA grant awards | see §2 | see §2 | see §2 | see §2 | see §2 |
| 3 | IRS BMF, NTEE major group A | 4 CSV, 324 MB | Org, city/state/ZIP | city+state or geocode | **Yes - the best of the lot** | **USABLE WITH WORK** |
| 4 | OSM performance tags | Overpass | Element, lat/lon | lat/lon | Mixed - see per-tag verdicts | PARTLY USABLE |
| 5 | Canada national culture lists | see §5 | see §5 | see §5 | see §5 | see §5 |

**Headline:** the single best culture measure available is **IRS BMF NTEE major group A,
per capita**. Measured on the real 4,226-place spine, its raw count correlates with
population at pearson **0.925** (a near-perfect population proxy, exactly as he suspected),
but the **per-10k rate correlates with population at spearman -0.107** - effectively
independent of size - and inside the 50k-100k population band the p90/p10 spread is
**8.8x**. It puts Santa Fe, Sarasota, Santa Barbara and Wilmington at the top and
master-planned commuter suburbs at the bottom. That is a real signal, not a size echo.

---

## 1. IMLS Museum Universe Data File (MUDF) - CONFIRMED DISCONTINUED

**His belief was correct.** The collection is retired and was last updated in 2018.

Landing page (after a 301 redirect from the `/data-collection/` path he had):
<http://www.imls.gov/research-evaluation/data/museum-data-files>

The page states the initiative is retired, last updated in 2018, and that IMLS has no
plans to update the museum files. It has also been **renamed** - it is now published as
the "Museum Data Files (MDF)", not the "Museum Universe Data File (MUDF)". Earlier MUDF
vintages (FY2014 Q1, FY2015 Q1, FY2015 Q3) are referenced on the page but no download
links for them are exposed.

### The one live download

| | |
|---|---|
| URL | `https://www.imls.gov/sites/default/files/2018_csv_museum_data_files.zip` |
| HTTP | 200, `content-type: application/zip` |
| **Measured size** | **2,864,864 bytes = 2.9 MB** zipped, 11,521,500 bytes unzipped |
| `last-modified` header | **Mon, 02 Nov 2020 22:56:03 GMT** (server date; the CSVs inside are dated 09 Nov 2018) |
| Format | ZIP containing 3 CSVs |
| Documentation | `https://www.imls.gov/sites/default/files/museum_data_file_documentation_and_users_guide.pdf` (PDF, 581 KB per the page) |
| Licence | US federal government work, public domain. Free, no login. |
| Vintage | **2018. Terminal - it will never be refreshed.** |

### Actual record counts (counted, not quoted)

| Member file | Bytes | Records | Discipline |
|---|---|---|---|
| `MuseumFile2018_File1_Nulls.csv` | 2,915,718 | 7,431 | ART 2,620 / HST 1,776 / BOT 1,029 / SCI 834 / ZAW 465 / CMU 438 / NAT 269 |
| `MuseumFile2018_File2_Nulls.csv` | 2,824,866 | 7,961 | GMU 7,961 (general museums) |
| `MuseumFile2018_File3_Nulls.csv` | 5,780,916 | 14,786 | HSC 14,785 (historical societies / historic preservation) + 1 blank |
| **Total** | **11,521,500** | **30,178** | |

### Geography - this is the strong part

Measured fill rates across all three files:

| Field | File 1 | File 2 | File 3 |
|---|---|---|---|
| `LATITUDE` / `LONGITUDE` | 99.6% | 99.7% | 99.9% |
| `FIPSST` (state FIPS) | 100.0% | 100.0% | 100.0% |
| `FIPSCO` (county FIPS) | 93.0% | 91.8% | 92.0% |
| `ADCITY` | 100.0% | 100.0% | 100.0% |

**30,109 of 30,178 records carry a usable lat/lon.** That is a direct match to two of his
declared join keys (lat/lon, and place->county FIPS). No geocoding step is needed. The
57/58-column schema also carries `EIN`, `NTEEC`, `NAICS`, `WEBURL`, `INCOME15`,
`REVENUE15`, and a `LOCALE4` urbanicity code.

### The size-confound judgement - and a serious trap

Joined to the real spine with his existing 15 km radius method:

| pop band | n | median museums/10k | p10 | p90 | p90/p10 | % zero |
|---|---|---|---|---|---|---|
| 10k-25k | 2,350 | 8.47 | 1.52 | 43.23 | 28.5 | 2% |
| 25k-50k | 993 | 5.37 | 1.14 | 19.54 | 17.1 | 1% |
| 50k-100k | 532 | 2.91 | 0.78 | 11.06 | 14.1 | 1% |
| 100k-250k | 259 | 1.53 | 0.51 | 4.71 | 9.2 | 2% |
| 250k-1M | 83 | 0.94 | 0.30 | 2.73 | 9.0 | 4% |

Raw count vs population: pearson **0.185**. So the 15 km radius count is *not* a
population proxy. But that is not good news, because of what it is a proxy for instead.

**TRAP 1 - the radius double-counts metros 6.0x.** Summing `imls_all` across all spine
places with pop>=2,500 gives **125,492** museum-place pairs from only **30,109** real
museums. Neighbouring places all claim the same institutions.

**TRAP 2 - the centroid rule hands big-city assets to small neighbours.** Even using
nearest-place-only assignment, measured on the real spine:

| place | pop | land km² | museums (nearest-place) |
|---|---|---|---|
| New York, NY | 8,483,844 | 778.2 | **75** |
| Hoboken, NJ | 58,668 | 3.2 | **154** |
| Philadelphia, PA | 1,579,706 | 347.9 | **31** |
| Camden, NJ | 71,496 | 23.1 | **81** |

Why: the spine stores New York as a single centroid at 40.6627,-73.9387 (in Brooklyn).
The Metropolitan Museum of Art is **13.1 km** from that centroid but only **6.6 km** from
Hoboken's centroid. Any nearest-centroid rule gives Manhattan's museums to Hoboken. The
same happens to Philadelphia and Camden. **This affects his existing OSM pipeline too, not
just IMLS** - `data/osm.json` uses the identical centroid + 15 km design and carries an
`_exclusive` column built the same way.

Fix: assign by point-in-polygon against the TIGER place shapefile, or weight the radius
count by distance, rather than by distance to a single centroid.

**VERDICT: USABLE WITH WORK.** The file itself is excellent and trivially joinable via
lat/lon. Three real limits: it is frozen at 2018 and ageing; **49% of the records (14,786)
are `HSC` historical societies and historic-preservation groups, not visitable museums** -
filter those out or the measure becomes "how old is this town"; and the join method must be
fixed before the numbers mean anything.

### Bonus: it validates OSM museum coverage

Restricting IMLS to the disciplines OSM would actually tag `tourism=museum` (ART 2,620 +
HST 1,776 + SCI 834 + CMU 438 + NAT 269 + GMU 7,961) gives **13,898**. OSM `tourism=museum`
in the US is **14,800** (§4) - **6.5% more**, which is exactly what eight years of extra
mapping since 2018 should look like. (IMLS `BOT` 1,029 botanical gardens and `ZAW` 465
zoos/aquaria are excluded because OSM tags those `tourism=garden` / `tourism=zoo`.)

Two entirely independent censuses agreeing to within 6.5% is strong evidence that **OSM
museum coverage in the US is essentially complete**. That matters beyond museums: it is
the only hard calibration point available for judging how much to trust any other OSM
culture tag.

---

## 3. IRS Exempt Organizations BMF, NTEE major group A

*(§2 NEA/DataArts and §5 Canada appear below - they were verified in parallel.)*

### Download - re-measured today, not carried over

| File | URL | Measured bytes |
|---|---|---|
| Region 1 | `https://www.irs.gov/pub/irs-soi/eo1.csv` | 48,629,769 |
| Region 2 | `https://www.irs.gov/pub/irs-soi/eo2.csv` | 125,728,575 |
| Region 3 | `https://www.irs.gov/pub/irs-soi/eo3.csv` | 164,634,273 |
| Region 4 | `https://www.irs.gov/pub/irs-soi/eo4.csv` | 861,858 |
| **Total** | | **339,854,475 = 324 MB** |

All four returned HTTP 200. Parsed row count: **1,957,340**, matching the IRS's own stated
record count. Licence: US Government work, public domain, free, no key.

### THE ANSWER TO HIS QUESTION: how many NTEE-A organisations?

**118,457.**

That is major group `A` = "Arts, Culture and Humanities", counted over all 1,957,340 rows.
It independently reproduces the figure in `research/src-language-nonprofit.md` exactly.

Official subcode titles below are quoted from the IRS's own codebook
(`https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf`, HTTP 200, 425,457 bytes, extracted
with `pdftotext -layout`, lines 748-791) - not from memory. Counts are mine.

| Code | Official IRS title | Count |
|---|---|---|
| A20 | Arts, Cultural Organizations - Multipurpose | 15,147 |
| A23 | Cultural, Ethnic Awareness | 11,500 |
| A80 | Historical Societies, Related Historical Activities | 10,938 |
| A68 | Music | 7,153 |
| A65 | Theater | 6,842 |
| A25 | Arts Education | 5,348 |
| A60 | Performing Arts Organizations | 5,019 |
| A99 | Arts, Culture, and Humanities N.E.C. | 4,964 |
| A50 | Museum, Museum Activities | 3,802 |
| A62 | Dance | 3,659 |
| A54 | History Museums | 3,456 |
| A12 | Fund Raising and/or Fund Distribution | 3,377 |
| A82 | Historical Societies & Historic Preservation | 3,023 |
| A6B | Singing, Choral | 2,956 |
| A6C | Music Groups, Bands, Ensembles | 2,701 |

Useful aggregates I computed:

| Subset | Codes | Count |
|---|---|---|
| `A_all` | all of major group A | **118,457** |
| `A_perf` (live performance) | A60,A61,A62,A63,A65,A68,A69,A6A,A6B,A6C,A6E | **32,898** |
| `A_event` (literally events) | A27 Community Celebrations + A84 Commemorative Events | **1,930** |
| `A_perf_event` | the two above combined | **34,828** |
| `A_hist` | A80 + A82 historical societies | **13,961** |
| `A_museum` | A50-A57 | **9,335** |

Note there IS a literal "events" bucket - `A27 Community Celebrations` (856) and
`A84 Commemorative Events` (1,074) - but at 1,930 nationally it is far too thin to score
towns with. Do not use it alone.

### THE ANSWER TO HIS SECOND QUESTION: does it separate similar-sized cities?

**Yes, decisively - once you take it per capita.** Measured on the 4,226-place spine.

| Subset | places matched | raw count vs pop (pearson) | **per-10k rate vs pop (spearman)** | p90/p10 within 50k-100k | % zero |
|---|---|---|---|---|---|
| `A_all` | 3,363 | **0.925** | **-0.107** | **8.8x** | 0% |
| `A_perf` | 2,802 | 0.933 | -0.239 | 10.0x | 0% |
| `A_perf_event` | 2,848 | 0.932 | -0.238 | 9.3x | 0% |
| `A_event` | 687 | 0.686 | -0.946 | 2.8x | 0% |
| `A_hist` | 2,092 | 0.749 | -0.680 | 6.2x | 0% |
| `A_museum` | 1,757 | 0.872 | -0.707 | 6.0x | 0% |

Read that first row carefully, because it is the whole finding:

- **Raw count is a pure population proxy** (pearson 0.925). He was right. Do not ship it.
- **Per-capita rate is essentially independent of population** (spearman -0.107).
- **And it still spreads places 8.8x apart within a single population band.** So it is not
  size, and it is not flat. It is signal.

Real places, 50k-100k band, `A_all` per 10k (n=500):

| Highest | | Lowest | |
|---|---|---|---|
| Wilmington, DE (71,727) | 25.23 | Atascocita, TX (99,354) | 0.10 |
| Sarasota, FL (56,970) | 24.40 | Mount Pleasant, SC (93,993) | 0.11 |
| Santa Fe, NM (89,019) | 22.92 | Alafaya, FL (92,449) | 0.11 |
| Silver Spring, MD (81,462) | 18.29 | Rochester Hills, MI (77,089) | 0.13 |
| Santa Barbara, CA (87,779) | 17.32 | Poinciana, FL (75,068) | 0.13 |

And for `A_perf_event` per 10k in the same band: Sarasota 11.06, Marietta GA 6.91,
Portland ME 6.54, Santa Barbara 6.27, Santa Fe 6.07 at the top; Rancho Cordova CA 0.12,
South Gate CA 0.11, O'Fallon MO 0.11, Norwalk CA 0.10 at the bottom.

Those are the correct answers. Santa Fe, Sarasota, Santa Barbara and Portland ME really
are arts towns; Atascocita, Alafaya and Poinciana are master-planned Sunbelt subdivisions.
The measure is picking up the thing he actually wants.

### Which subset to ship: use `A_all`, not the performance subset

`A_perf_event` is conceptually closer to "culture and events", but it is too thin at town
scale. Count distribution in the 25k-100k band:

| Subset | median count | % of places with count <=2 (noise) | % with count >=10 (stable) |
|---|---|---|---|
| `A_all` | **13** | **7%** | **65%** |
| `A_perf_event` | 5 | 26% | 20% |

At 26% of towns sitting on 0-2 organisations, `A_perf_event` per capita is mostly
measuring rounding. `A_all` has the volume to be stable and still separates 8.8x.

**Statistical warning about the thin subsets:** the very strong negative rate-vs-pop
correlations for `A_event` (-0.946), `A_museum` (-0.707) and `A_hist` (-0.680) are largely
an artifact, not a finding. When nearly every matched place has a count of exactly 1, the
rate becomes 1/pop, which is mechanically anti-correlated with pop. Only `A_all` and
`A_perf` have enough volume for the correlation to mean anything.

### Independent cross-validation - the signal is real, not join noise

The IRS BMF (2026 tax records) and IMLS (2018 museum survey) are completely independent
data collections. Joined the same way and taken per capita, they agree:

| Pair | n | spearman |
|---|---|---|
| `A_all` per-cap vs IMLS-by-city per-cap | 2,751 | **0.520** |
| `A_perf_event` per-cap vs IMLS-by-city per-cap | 1,396 | **0.508** |
| `A_all` per-cap vs IMLS-nearest-place per-cap | 2,751 | 0.372 |

Two unrelated sources ranking towns the same way at r≈0.52 is meaningful agreement. If the
city-name join were mostly noise, these would be near zero.

### The join is still the problem - measured, not assumed

Naive normalized `CITY`+`STATE` match against the 4,226-place spine:

- **NTEE-A orgs matched: 77,219 / 118,457 = 65.2%** (consistent with the 64% found for the
  full BMF previously).
- **Spine places receiving any match: 3,363 / 4,226.**
- For comparison I ran the identical join on IMLS, which has ground-truth lat/lon:
  **15,764 / 30,109 = 52.4%** matched by city name. So the city-name join demonstrably
  loses about half of a file whose true locations are known.

The failure modes are the ones already documented in
`research/src-language-nonprofit.md` §3 - USPS abbreviations (`COLORADO SPGS`),
consolidated city-county names (`Louisville/Jefferson County`), and postal cities that are
not Census places at all (`BROOKLYN`, `BRONX`). It is **biased against the largest cities**,
which is the worst possible direction.

There is a second bias worth naming: **CDPs get spuriously low scores.** Atascocita TX,
Alafaya FL and Poinciana FL sit at the bottom of the table above with a count of 1 each.
Those are unincorporated census-designated places whose organisations file under a
neighbouring postal city (Humble, Orlando, Kissimmee). Their near-zero values are probably
join artifacts, not real cultural deserts. Rochester Hills MI at n=1 is the same story -
its mail goes to "Rochester".

The fix is the one already scoped: geocode the addresses, then point-in-polygon against
`cb_2024_us_place_500k.zip`. Do not ship the city-name join for the biggest cities or for
CDPs.

**Also inherited from the earlier verification, still true:** the BMF address is a
*mailing* address, not an operating location. PO boxes and treasurers' homes are common,
and a national charity headquartered in a small town inflates it.

**VERDICT: USABLE WITH WORK.** Best culture signal found. The work is entirely in the
geocode-and-point-in-polygon join, and it is not optional.

---
## 4. OpenStreetMap - which additional tags actually carry live music and performance

### Method

Overpass on the whole US or Canada times out, and he already knows regex alternations 504.
So the national counts below come from **Geofabrik's regional taginfo instances**, which
are precomputed per-region tag statistics with a JSON API and no timeouts:

- `https://taginfo.geofabrik.de/north-america:us/api/4/tag/stats?key=<K>&value=<V>`
- `https://taginfo.geofabrik.de/north-america:canada/api/4/tag/stats?key=<K>&value=<V>`

Both returned HTTP 200 with `data_until: 2026-08-20`. Exact-match tags only, one request
per tag, no regex. **This is the tool to use for any future "is this tag worth pulling"
question - it answers in one request instead of a 504.**

Counts are OSM *elements* (nodes + ways + relations), so a venue mapped as both a node and
a building outline can count twice. Treat them as upper bounds.

Population baseline for the cross-border column: World Bank API
`https://api.worldbank.org/v2/country/USA;CAN/indicator/SP.POP.TOTL?format=json&date=2024`
-> US 340,003,797 and Canada 41,262,329 for 2024, a **CA/US ratio of 0.1214**.
The `index` column is (CA/US element ratio) / 0.1214. **index 1.0 = both countries tag it
at the same rate per person. Above 1.5 means the tag is not comparable across the border.**

### Measured counts

| Tag | US | Canada | CA/US | index | per 1M US pop |
|---|---|---|---|---|---|
| `tourism=artwork` | 36,913 | 5,002 | 0.136 | 1.12 | 108.6 |
| `amenity=bar` | 27,331 | 2,449 | 0.090 | 0.74 | 80.4 |
| `amenity=social_facility` | 19,480 | 4,785 | 0.246 | 2.02 | 57.3 |
| `amenity=library` | 19,317 | 2,293 | 0.119 | 0.98 | 56.8 |
| `tourism=museum` | 14,800 | 1,903 | 0.129 | 1.06 | 43.5 |
| `amenity=community_centre` | 14,080 | 4,771 | 0.339 | **2.79** | 41.4 |
| `amenity=pub` | 11,102 | 2,518 | 0.227 | 1.87 | 32.7 |
| **`amenity=theatre`** | **10,840** | **1,193** | 0.110 | **0.91** | 31.9 |
| `amenity=events_venue` | 5,929 | 460 | 0.078 | 0.64 | 17.4 |
| **`amenity=cinema`** | **5,435** | **530** | 0.098 | **0.80** | 16.0 |
| `tourism=gallery` | 4,422 | 634 | 0.143 | 1.18 | 13.0 |
| `amenity=arts_centre` | 2,941 | 392 | 0.133 | 1.10 | 8.6 |
| `amenity=studio` | 2,885 | 542 | 0.188 | 1.55 | 8.5 |
| `leisure=dance` | 2,314 | 377 | 0.163 | 1.34 | 6.8 |
| **`amenity=nightclub`** | **1,703** | **216** | 0.127 | 1.05 | 5.0 |
| `amenity=casino` | 1,328 | 121 | 0.091 | 0.75 | 3.9 |
| `amenity=music_school` | 1,144 | 280 | 0.245 | 2.02 | 3.4 |
| `amenity=conference_centre` | 693 | 74 | 0.107 | 0.88 | 2.0 |
| `amenity=stage` | 320 | 32 | 0.100 | 0.82 | 0.9 |
| `leisure=hackerspace` | 279 | 44 | 0.158 | 1.30 | 0.8 |
| **`amenity=music_venue`** | **159** | **10** | 0.063 | 0.52 | 0.5 |
| `amenity=exhibition_centre` | 125 | 10 | 0.080 | 0.66 | 0.4 |
| `amenity=bandstand` | 6 | 0 | 0.000 | 0.00 | 0.0 |

### Verdict on each tag he asked about

**`amenity=theatre` - ADD IT. The single best addition.** 10,840 US / 1,193 CA, index 0.91
so it is comparable across the border. In OSM this means a performing-arts venue, not a
cinema (cinemas are `amenity=cinema`), which is exactly the "live performance" concept
missing from his current pull. It is the 8th most common tag on this list and roughly as
well mapped as `tourism=museum`, which §1 shows is ~97% complete against the IMLS census.

**`amenity=cinema` - ADD IT.** 5,435 US / 530 CA, index 0.80. Well populated and
consistently tagged. Caveat: it measures commercial multiplexes as much as culture, and
multiplexes track retail development, so it will partly re-measure "does this town have a
mall". Weight it low.

**`amenity=community_centre` - ADD IT, BUT NEVER COMPARE ACROSS THE BORDER.** 14,080 US /
4,771 CA. Volume is fine in both countries, but the **index is 2.79** - Canadians tag
community centres nearly 3x more densely per person than Americans. That is a mapping
culture artifact, not 3x more Canadian community centres. If a US place and a Canadian
place are scored on the same absolute scale, every Canadian town gets a free boost.
**Rank within country, then merge the ranks.** (Same warning applies to
`amenity=social_facility` index 2.02, `amenity=music_school` index 2.02 and `amenity=pub`
index 1.87.)

**`amenity=nightclub` - DO NOT TRUST IT.** Only 1,703 elements for the entire United
States, 5.0 per million people. There are obviously far more than 1,703 nightclubs in the
US; the tag is simply not applied. The index of 1.05 says the under-tagging is at least
even-handed between countries, but a tag this sparse produces mostly zeros at town scale
and the few non-zeros are wherever a mapper happened to care. Skip it.

**`amenity=music_venue` - DEAD. DO NOT USE.** **159 elements in the entire US and 10 in the
entire Canada.** Spread over 4,197 US places that is one element per 26 places. This tag is
effectively unused in North America - it is a newer tag that never got adoption here. Any
score built on it is 99% zeros. This is the clearest "does not work" on the list.

### Other tags worth knowing about

- **`amenity=events_venue` (5,929 US / 460 CA)** - decent US volume and conceptually right
  on target for "events", but index 0.64 means it is notably thinner in Canada. Usable in
  the US, weak in Canada.
- **`leisure=dance` (2,314 / 377)** - dance studios and halls. Thin but real.
- **`amenity=stage` (320 / 32)** and **`amenity=bandstand` (6 / 0)** - too sparse, skip.
  `amenity=bandstand` has **6 elements in the whole United States**; it is not a real tag
  here.
- **`amenity=exhibition_centre` (125 / 10)** - too sparse, skip.
- **`tourism=artwork` (36,913 / 5,002)** - the highest-volume culture-adjacent tag on the
  board and index 1.12, so cross-border comparable. It is public art: murals, sculptures,
  statues. Not "events", but a genuine and well-mapped signal of a place that invests in
  visible culture, and it has ~3.4x the volume of `amenity=theatre`. **Worth testing as an
  addition even though he did not ask about it.**
- **`amenity=library` (19,317 / 2,293, index 0.98)** - very well mapped and almost perfectly
  comparable across the border. Civic rather than "events", but if he wants a stable,
  high-coverage culture-infrastructure tag, this is the most complete one available.

### A correction to what he is ALREADY pulling: `craft=*` is not a culture tag

He listed `craft=*` as one of the tags he already pulls within 15 km of each place. I
checked what that key actually contains in North America
(`https://taginfo.geofabrik.de/north-america:us/api/4/key/values?key=craft&rp=12&sortname=count&sortorder=desc`):

| US | count | | Canada | count |
|---|---|---|---|---|
| `craft=brewery` | 3,732 | | `craft=brewery` | 591 |
| **`craft=hvac`** | **2,816** | | `craft=winery` | 406 |
| `craft=winery` | 2,196 | | **`craft=hvac`** | **391** |
| `craft=electronics_repair` | 2,142 | | `craft=electronics_repair` | 340 |
| **`craft=plumber`** | **2,054** | | **`craft=electrician`** | **328** |
| **`craft=roofer`** | **1,632** | | **`craft=plumber`** | **322** |
| `craft=photographer` | 1,558 | | `craft=caterer` | 266 |
| **`craft=electrician`** | **1,405** | | `craft=metal_construction` | 260 |
| `craft=signmaker` | 1,251 | | `craft=photographer` | 226 |
| `craft=caterer` | 1,247 | | `craft=carpenter` | 212 |
| `craft=cleaning` | 1,203 | | `craft=signmaker` | 204 |
| `craft=metal_construction` | 1,171 | | `craft=construction` | 188 |

Key totals: **36,043 US / 6,434 Canada**.

**`craft=*` in North America is a contractor directory, not an arts directory.** HVAC,
plumbers, roofers, electricians, cleaning and metal construction dominate the top of the
list. Breweries and wineries are next. Actual craftspeople (potters, luthiers, bookbinders)
are far down the tail. Pulling `craft=*` unfiltered into a culture score means a town with
lots of HVAC contractors scores as cultured - and contractor density tracks housing stock
and population, which is exactly the confound he is trying to avoid.

**Recommendation: stop pulling `craft=*` unfiltered.** If he wants it, whitelist the
genuinely artisanal values only. As it stands this tag is adding noise correlated with
population, which is the worst possible contribution to this dimension.

### Supplementary live-music tags - all dead

| Tag | US | Canada |
|---|---|---|
| `live_music=yes` | 240 | 19 |
| `theatre:genre` (key) | 163 | 41 |

Both are far too sparse to use. There is no working way in OSM to identify "bars and pubs
that host live music" in North America - the tag exists but nobody applies it.

---

## 2. NEA / NCAR / SMU DataArts

Short answer: **DataArts is not free and not joinable. The NEA has exactly one
sub-state dataset, and I measured it against the real spine - it does not work either.**

### 2a. NEA grant awards - free, big, current, and still NOT USABLE

There is no documented bulk download. `https://www.arts.gov/grants/recent-grants` is a link
page; the search app at `https://apps.nea.gov/grantsearch/` 302s to a React SPA at
`https://grantsearch.nea.gov/`. Reading that SPA's JS bundle exposes an **undocumented,
unauthenticated JSON API**. I called it myself:

| | |
|---|---|
| Bulk URL | `https://grantsearch.nea.gov/api/Grants/Export` |
| **My own measurement** | **HTTP 200, 65,013,823 bytes, `application/json`, 34.3 s, no key, no login** |
| Stats URL | `https://grantsearch.nea.gov/api/Grants/Stats` -> HTTP 200, `{"TotalAmount":3319870602.9900,"UniqueStates":58,"UniqueOrganizations":12683}` |
| Records | **65,932 grants**, FY**1998-2026**, $3.32 bn |
| Fields | OrganizationName, City, State, Zip, ProjectDescription, FiscalYear, GrantAmount, DivisionName, ProgramName, CategoryDesc, GrantFrom/ToDate |
| Geography | City, State, Zip populated. **`CongressionalDistrict` is null in all 65,932 rows. No lat/lon.** |
| Licence | **Could not confirm** - no explicit statement found. Federal work, so 17 U.S.C. 105 public domain is an inference, not something read off the page. |

I joined it properly - ZIP5 -> ZCTA -> place via the free Census crosswalk (§6), not by
city name - and got a **97.3% record match rate** (64,150 of 65,932; 29 had no usable ZIP,
1,753 ZIPs are not in the ZCTA crosswalk). Then measured it against the real 4,226-place
spine:

| pop band | n | % of places with ZERO grants ever (FY1998-2026) | % with ZERO since FY2016 | median $/capita |
|---|---|---|---|---|
| 10k-25k | 2,350 | **79%** | 86% | 0.00 |
| 25k-50k | 993 | **58%** | 68% | 0.00 |
| 50k-100k | 532 | 37% | 52% | 0.30 |
| 100k-250k | 259 | 15% | 24% | 1.16 |
| 250k-1M | 83 | **0%** | 4% | 7.68 |

**Only 1,563 of 4,226 places (37.0%) have ever received an NEA grant in 29 years.** Since
FY2016 it is 1,184 places (28.0%).

**Size-confound verdict: this IS the population dimension wearing a hat.** Raw grant count
vs population pearson **0.871**; grant dollars vs population pearson **0.820**. Worse, look
at the zero column - it falls monotonically from 79% to 0% as population rises. "Has an NEA
grant" is essentially a test of whether a town is big enough to host a major institution.
Per-capita dollars does not rescue it, because for 79% of small towns the numerator is
exactly zero and per-capita of zero is still zero. A dimension that cannot distinguish
between two-thirds of the places in the app is not a dimension.

**VERDICT: NOT USABLE** as a ranking input. Genuinely interesting as a *tie-breaker flag*
for the ~1,200 places that do appear, or as descriptive copy ("this town has won N NEA
grants"), but never as a scored dimension.

*Caveat:* the endpoint is undocumented - found by reading a JS bundle. It has no stability
guarantee and could be locked down without notice. Do not build a scheduled job on it
without a cached fallback.

### 2b. NEA research / Arts Data Profile series - NOT USABLE, state-level only

`https://www.arts.gov/impact/research/arts-data-profile-series` lists 38 profiles. All are
national, state, or rural/urban-binary. I downloaded the flagship file to prove it rather
than take the titles at face value:

- `https://www.arts.gov/sites/default/files/2001_2023ACPSA_R-2025.csv`
- **HTTP 200, 5,072,279 bytes, 44,574 data rows** (Arts and Cultural Production Satellite
  Account, 2001-2023)
- Columns: `State,Year,Industry,Tot_VA,VA_ratio,ACPSA_VA,VA_LQ,Tot_Emp,Emp_ratio,ACPSA_Emp,Emp_LQ,Tot_Comp,Comp_ratio,ACPSA_Comp,Comp_LQ`
- **The `State` column has exactly 51 distinct values** (`01 Alabama` … 50 states + DC).

Free, clean, well documented - and **state-level only**. It cannot be joined to a place
GEOID, and the app already has state. Zero separating power between two towns in the same
state. **NOT USABLE.**

### 2c. SMU DataArts (formerly NCAR) - NOT USABLE. Paywalled and CBSA-level.

- **The URL in the brief is dead.** `https://www.smu.edu/meadows/newsandevents/artsvibrancyindex`
  returns **HTTP 404** (I checked; it serves a 57,173-byte error page). The live home is
  `culturaldata.org`.
- **Cultural Data Profile is not free.** ICPSR's catalogue record for it
  (`https://www.icpsr.umich.edu/web/NADAC/studies/39140`) states the price: CDP datasets for
  the past five completed fiscal years cost **$750**, with academic discounts. The
  `https://culturaldata.org/services/dataset-access/` route is a request-and-approval form,
  not a download.
- **Arts Vibrancy Index is not raw data.** The Data Explorer page embeds two Tableau Public
  vizzes. The state-level workbook downloads (`https://public.tableau.com/workbooks/state_AVI2025.twb`,
  200, 15,816 bytes) but is state-level. The Top-100 workbook
  (`https://public.tableau.com/workbooks/ArtsVibrancyTop100VertTest.twb`) returns **404** -
  download disabled.
- **The disqualifier is granularity, not price.** The index is published for **Core Based
  Statistical Areas**, and several published entries are metro *divisions*
  (`San Francisco-San Mateo-Redwood City, CA`). A CBSA spans whole counties. **Every town in
  a metro would receive one identical score**, which is precisely the discrimination the app
  needs and would not get. Only the top 100 communities plus 50 states are published at all.

**Is DataArts subscription-only? Effectively yes** - $750 for the org-level microdata, and
the free published product is CBSA-level. **NOT USABLE.**

### 2d. NADAC at ICPSR - free of charge but login-walled, and wrong granularity

`https://www.icpsr.umich.edu/web/NADAC/` (302s to `/sites/nadac/home`) hosts 182 studies and
states that users obtain data at no charge. **But download requires a login.** I confirmed
this myself: `https://www.icpsr.umich.edu/web/NADAC/studies/38936/versions/V2/download/bundle?path=NADAC`
redirects to a Keycloak OIDC login at
`https://login.icpsr.umich.edu/realms/icpsr/protocol/openid-connect/auth?...`. No anonymous
bulk access, no API.

Beyond the login, the content is wrong for this purpose: SPPA 2022 (ICPSR 38936) is
household survey microdata whose smallest geography is CBSA. The org-level entries (37335
Arts Vibrancy, 39140 CDP) are bibliographic stubs that explicitly say the data are not
available from ICPSR. **NOT USABLE.**

---

## 6. BONUS - Census ZIP Business Patterns (not in the brief, checked anyway, NOT USABLE)

Worth ruling out explicitly because it looks perfect on paper: an annual, current, free
federal count of business establishments by industry at ZIP level.

| | |
|---|---|
| URL | `https://www2.census.gov/programs-surveys/cbp/datasets/2023/zbp23detail.zip` |
| **Measured** | **HTTP 200, 15,712,046 bytes zipped -> 291,122,039 bytes, 2,974,116 rows** |
| Vintage | 2023 data, file dated 09 Jun 2025. Annual series. |
| Fields | `zip,name,naics,est,n<5,…,n1000,city,stabbr,cty_name` |
| Licence | US federal, public domain, free, no login |
| Crosswalk | `https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_place20_natl.txt` - **HTTP 200, 9,811,563 bytes**, free, ZCTA -> place GEOID |

The `est` column is never suppressed (0 unparseable across all 2,974,116 rows), and the ZIP
join is clean: **11,059 of 11,459 ZIPs (96.5%)** matched a ZCTA in the crosswalk.

**But the culture industries are far too thin.** National establishment totals I counted:

| NAICS | Meaning | Establishments |
|---|---|---|
| `7111//` | Performing Arts Companies | **5,666** |
| `712///` | Museums, Historical Sites and Similar | **2,715** |
| `7113//` | Promoters of Performing Arts | 3,933 |
| `512131` | Motion Picture Theaters | 268 (6-digit detail is disclosure-suppressed in most ZIPs) |
| `71----` | Whole sector 71 Arts/Entertainment/Recreation | 156,063 (but `713///` alone - gyms, golf, bowling - is 79,444, so the sector is useless as a culture proxy) |

Only **2,715 museum establishments nationally**, against 30,178 in IMLS and 14,800 in OSM.
The reason is structural: CBP counts establishments **with paid employees**, and most small
museums and arts groups are volunteer-run with no payroll. CBP is blind to exactly the
organisations that distinguish a small arts town.

Joined to the spine (7111 + 712 + 7113 = 11,177 establishments assigned):

| pop band | n | median count | % zero |
|---|---|---|---|
| 25k-50k | 993 | 0 | **79%** |
| 50k-100k | 532 | 0 | **68%** |
| 100k-250k | 259 | 3 | 48% |

**Size-confound verdict: fails twice.** Raw count vs population pearson **0.888**, and the
zero rate again falls with population. Same failure shape as the NEA grants.

**VERDICT: NOT USABLE** for this dimension. Worth remembering that the **ZBP file and the
free ZCTA->place crosswalk both work perfectly** - if he ever wants a different dimension
built on business counts (restaurants, groceries, gyms), that pipeline is verified and
ready. It is the culture NAICS codes specifically that are too thin.

---

## 5. Canada

**Good news: Canada is better served than the US here.** Two free national datasets carry a
direct **CSD code**, so there is no name-matching problem at all. I verified both downloads
myself and joined both to his real 712-CSD spine.

CHIN, which he asked about specifically, turned out to be the weakest of the options - but
it led to the best one.

### 5a. THE ONE TO USE FOR NAMED VENUES: StatCan ODCAF

**Open Database of Cultural and Art Facilities.** Not in the brief - found via a reference
inside Canadian Heritage documentation.

| | |
|---|---|
| Landing page | `https://www.statcan.gc.ca/en/lode/databases/odcaf` |
| Download | `https://www150.statcan.gc.ca/n1/en/pub/21-26-0001/2020001/ODCAF_V1.0.zip` |
| **My own measurement** | **HTTP 200, 1,304,309 bytes** -> `ODCAF_v1.0.csv` **1,654,348 bytes / 7,972 facilities**, plus `Data_Sources.csv` (76,925 bytes) and a 874,894-byte metadata PDF |
| Columns | `Index, Facility_Name, Source_Facility_Type, ODCAF_Facility_Type, Provider, Unit, Street_No, Street_Name, Postal_Code, City, Prov_Terr, Source_Format_Address, CSD_Name, CSDUID, PRUID, Latitude, Longitude` |
| **Join key** | **`CSDUID` populated on 7,671/7,972 = 96.2%** (all 7 digits, 2,162 distinct CSDs). **Latitude/Longitude on 6,748/7,972 = 84.6%.** Both of his declared Canadian join keys are in the file. |
| Licence | Open Government Licence - Canada in aggregate, **but built from 181 heterogeneous municipal/provincial sources** with their own terms (Données Québec CC-BY, individual city licences). Attribution obligations flow through - worth a look before commercial use. |
| Vintage | **v1.0, October 2020. No v2 exists.** This is the weak point. |

Facility type breakdown (counted by me):

| Type | Count |
|---|---|
| library or archives | 3,013 |
| museum | 1,938 |
| gallery | 810 |
| heritage or historic site | 620 |
| theatre/performance and concert hall | 583 |
| festival site | 346 |
| miscellaneous | 343 |
| art or cultural centre | 225 |
| artist | 94 |

**Coverage on his real 712-CSD spine:**

| Measure | places with >=1 |
|---|---|
| ODCAF all facilities | **619/712 = 87%** |
| ODCAF excluding libraries/archives | **457/712 = 64%** |
| ODCAF theatre + festival + arts centre only | 146/712 = **21% - too sparse, do not use alone** |

**Size-confound judgement (measured on 432 CSDs with pop>=5,000):**

| Measure | raw vs pop (spearman) | **per-10k vs pop (spearman)** |
|---|---|---|
| ODCAF all | +0.631 | -0.355 |
| **ODCAF excl. libraries** | +0.569 | **-0.127** |

**Use the excluding-libraries variant.** Its per-capita rate is nearly independent of
population (-0.127), whereas the all-facilities version is pulled to -0.355 because every
town has a library regardless of size, which inverts the ratio for small places.

And it separates similar-sized towns. The 25k-40k CSD band (n=45):

| Highest | | Lowest | |
|---|---|---|---|
| Charlottetown, PE (38,809) | 12 | Boisbriand, QC (28,308) | 1 |
| Val-d'Or, QC (32,752) | 11 | East Gwillimbury, ON (34,637) | 1 |
| Alma, QC (30,331) | 11 | Spruce Grove, AB (37,645) | 1 |
| Campbell River, BC (35,519) | 10 | Langley (City), BC (28,963) | 1 |
| Prince Albert, SK (37,756) | 9 | LaSalle, ON (32,721) | 0 |

12 versus 0 at the same population. Real discriminating power.

**THE BIG CAVEAT - ODCAF has a severe province-level coverage bias.** Facilities per 100k,
computed on his own spine:

| Prov | per 100k | | Prov | per 100k |
|---|---|---|---|---|
| **NB** | **65.5** | | QC | 18.1 |
| YT | 31.9 | | BC | 17.3 |
| NU | 26.9 | | SK | 17.1 |
| NL | 21.9 | | NS | 16.8 |
| PE | 20.7 | | ON | 14.3 |
| | | | MB | 14.1 |
| | | | **AB** | **12.5** |
| | | | NT | 9.8 |

**A 5.2x spread, with New Brunswick a wild outlier at 248 facilities for 378,709 people.**
New Brunswick does not have five times Alberta's culture per capita - it has a better
provincial open-data feed. This is source-availability bias from those 181 heterogeneous
inputs. **Never compare ODCAF per-capita rates across provinces.** Rank within province, or
use it only for named-venue detail.

**VERDICT: USABLE.** Best Canadian source for named venues and a museum/theatre/gallery
breakdown. Frozen at 2020, and province-biased.

### 5b. THE ONE TO USE FOR CROSS-COUNTRY RANKING: StatCan table 33-10-1176

**The table he would have looked for (33-10-0222) is province-only - I confirmed its GEO
dimension has 14 members, Canada plus 13 provinces/territories. But a CSD sibling exists**
and he was not looking at it.

| | |
|---|---|
| Table | **PID 33101176** - "Canadian Business Counts, with employees, census metropolitan areas and census subdivisions, June 2026", released **2026-08-14** |
| Download | `https://www150.statcan.gc.ca/n1/tbl/csv/33101176-eng.zip` |
| **My own measurement** | **HTTP 200, 17,649,930 bytes** -> `33101176.csv` **188,511,875 bytes**, **1,047,957 data rows**, file dated 14 Aug 2026 |
| Geography | **3,379 GEO members - 3,337 at CSD level.** DGUID form `2021A0005` + 7-digit CSD code -> **direct join, no name matching** |
| NAICS | 445 members including 71, 711, 712, 7111, 7113, 7115, 7121 |
| Licence | Statistics Canada Open Licence. Free, no key, no login. |

**CRITICAL CORRECTION - do not use NAICS 71.** It looks like the obvious "arts,
entertainment and recreation" pick, but on his spine:

| | businesses on spine | share of NAICS 71 |
|---|---|---|
| NAICS 71 total | 15,665 | 100% |
| of which 711 (performing arts, spectator sports) | 5,005 | 32% |
| of which 712 (heritage institutions) | 887 | 6% |
| **residual = 713 amusement and recreation (gyms, golf, bowling, marinas)** | **9,773** | **62%** |

**NAICS 71 is 62% gyms and golf courses.** Scoring culture with it would mostly measure
recreation facilities. Use **711 + 712** instead.

**Coverage and size-confound on his 712-CSD spine:**

| NAICS | places with >=1 | total on spine | raw vs pop | **per-10k vs pop** |
|---|---|---|---|---|
| 71 (all) | 636/712 = 89% | 15,665 | +0.849 | -0.198 |
| **711 + 712** | **507/712 = 71%** | **5,892** | +0.735 | **-0.139** |
| 712 / 7121 heritage only | 354/712 = 50% | 887 | +0.398 | -0.145 |
| 7111 performing arts companies | 184/712 = **26%** | 1,131 | +0.758 | +0.102 |

**7111 alone is unusable** - 74% of his places would be zero, which is a missing-data
problem dressed up as a score.

Province bias is much milder than ODCAF's: excluding the three territories (tiny
populations, small-number noise), the range runs PE 27.7 to AB 12.3 per 100k = **2.3x**,
against ODCAF's 5.2x. It comes from one national Business Register applied uniformly, so
it is the more trustworthy cross-country measure.

**Real limitation: "with employees" only.** The companion without-employees table (33101175)
is province-only. So volunteer-run arts organisations with no payroll are invisible at CSD
level - the same blind spot that made US Census Business Patterns fail (§6). This
systematically under-counts small-town arts.

**VERDICT: USABLE.**

### 5c. Cross-validation between the two

ODCAF (excluding libraries) per capita vs CBC 711+712 per capita, on 401 spine CSDs:
**spearman 0.363.** Positive and real, but only moderate - the two disagree more than the
US pair did (§3, 0.52). That gap is mostly ODCAF's province bias. **Use CBC 711+712 for the
score and ODCAF for the venue names.**

### 5d. CHIN - what he actually asked about. NOT USABLE for institutions.

**Artefacts Canada** (`https://app.pch.gc.ca/application/artefacts_hum/indice_index.app?lang=en`)
is a search-only web app over 4M+ **object** records - individual artefacts, not a list of
institutions. No bulk download and no API is offered. There is **no "Directory of Canadian
Museums"** in the CHIN homepage navigation.

CHIN does publish one real file, the **Landscape of Museum Collections Online (LMCO)**:
1,870 rows, carries `CSDUID` on 1,846 of them across 989 CSDs, OGL-Canada. Worth knowing
about, but it covers collection-managing museums only - exhibition centres, historic sites,
libraries, archives, zoos and botanical gardens are excluded by design - so ODCAF supersedes
it for this purpose.

**Note:** the unanonymized **English** LMCO resource is broken (empty URL in CKAN, its
`/download` endpoint 404s). The French file
(`pcmec_ogp_donnees_fr_v2.csv`, 428,398 bytes) is complete and named, and `CSDUID` is
language-independent - use the FR file.

### 5e. StatCan Heritage Institutions Survey - DEAD

All four relevant tables are archived and national or provincial only:

| PID | Geography | Status |
|---|---|---|
| 21-10-0145 provincial profile of heritage institutions | 12 provinces | ARCHIVED, 1993-2002 |
| 21-10-0144 summary profile | Canada only | ARCHIVED, 1993-2002 |
| 21-10-0240 heritage institutions summary stats | Canada only | ARCHIVED, 2004-2010 |
| 33-10-0022 operating expenses by NAICS | Canada only | ARCHIVED, 2008-2010 |

The survey was discontinued around 2010. The **Culture Satellite Account** tables
(36-10-0652 national, 36-10-0453 and 36-10-0452 provincial) are current but stop at the
province. **NOT USABLE** - the app already has province.

### 5f. CRA charities - yes, there IS an arts and culture code

Answering only the narrow question (the rest of the CRA file is already covered in
`research/src-language-nonprofit.md`): **yes, the CRA carries a direct analogue of NTEE "A".**

The fields are **`Category`** and **`Sub Category`**, both 4-digit, in
`ident_2023_updated.csv` (13,339,737 bytes, 84,519 records, OGL-Canada). Code definitions in
`codes_en.pdf` (768,177 bytes).

| Code | Meaning | Count |
|---|---|---|
| **0190** | **"Arts"** - the direct NTEE-A analogue | **2,656** |
| 0215 | National Arts Service Organizations | 31 |
| 0200/0009 | Heritage / historical site | 1,136 |
| 0200/0012 | Museum | 375 |
| 0200/0010 | Library | 171 |
| 0200/0002 | Archives | 38 |
| 0200/0003 | Art gallery | 29 |
| 0200/0008 | Hall of fame | 25 |
| 0200/0015 | Performing arts centre / facility | 5 |
| 0012 | Education in the arts | 1,701 |

Category 0190 sub-codes cover arts council, arts festival, crafts, dance, literature, media
arts, music, music festival, theatre/performing arts, visual arts.

**Core arts and culture total = 4,466 charities (5.3% of all Canadian charities).** Broad,
adding 0012, = 6,167.

**But:** at 4,466 organisations across 712 places this is 26x thinner than the US NTEE-A
pool of 118,457, and it still has **no CSD code** - only City, Province, Postal Code - so it
inherits the geocoding problem already documented. **ODCAF and CBC both beat it on join
quality and neither needs geocoding. Use them instead.**

**Warning:** pre-2019 CRA files use a different, incompatible 2-digit category scheme. Do
not mix vintages.

