# US political lean, 2024 presidential, by county

Built by `src/us/build_politics.py`. Outputs `data/us/politics.json` (3,142 counties)
and `data/us/place_county.json` (31,617 Census places).

This is the US sibling of the Canadian `src/build_politics.py`, and it uses the same
-100 (left) to +100 (right) vote-weighted scale.

---

## 1. The honest limitation, up front

**County lean is a much blunter instrument than the Canadian riding lean, and in the
biggest counties a single number is close to meaningless.**

A Canadian federal riding holds about 110,000 people by design, because ridings are
drawn to be roughly equal. US counties are not drawn for anything. They range from
Loving County, Texas (48 people) to Los Angeles County (9.76 million). Los Angeles
County alone is bigger than 40 US states and bigger than nine Canadian provinces. Its
lean here is -34.0, which is a real average and a useless description of any actual
place inside it: Beverly Hills, Compton, Lancaster and Malibu all collapse into that
one number. Santa Clarita and Santa Monica get the same political value. In riding
terms, LA County is about 90 ridings glued together and then averaged.

The scale of it: **50 counties have over a million people and hold 29.9% of the US
population. 148 counties have over 500,000 people and hold 50.7%.** So for roughly half
of Americans, the county lean in this file is an average over a unit large enough to
contain both a solid-left city and a solid-right exurb. The counties where the number
should be treated as nearly meaningless, worst first:

| county | population | lean here | why the average lies |
| --- | --- | --- | --- |
| Los Angeles, CA | 9,757,179 | -34.0 | ~90 ridings' worth of people, city core to desert exurbs |
| Cook, IL | 5,182,617 | -42.5 | Chicago plus the conservative outer townships |
| Harris, TX | 5,009,302 | -5.6 | inner Houston is solid left, the ring is solid right, they cancel to "swing" |
| Maricopa, AZ | 4,673,096 | +3.5 | central Phoenix, Scottsdale and Sun City averaged to zero |
| San Diego, CA | 3,298,799 | -17.3 | coastal city vs inland east county |
| Orange, CA | 3,170,435 | -2.8 | Santa Ana vs Newport Beach |
| Miami-Dade, FL | 2,838,461 | +11.5 | flipped 2020->2024 and is internally split by neighbourhood |
| Dallas, TX | 2,656,028 | -22.6 | city vs northern suburbs |
| Riverside / San Bernardino, CA | 2.2-2.5M each | +1.3 / +2.1 | enormous desert counties, "swing" describes nowhere in them |
| Clark, NV | 2,398,871 | -2.7 | all of metro Las Vegas in one row |
| King, WA | 2,340,211 | -53.5 | Seattle drowns out east King County |

Every county with 1,000,000+ people carries `"coarse": true` in `politics.json` so the
app can down-weight it, caveat it, or refuse to use it as a place-level signal.

There is a second, related distortion on the join side. A place that straddles county
lines is assigned to the single county holding most of its population (that is what the
spec asked for), and for some places that "most" is a minority of the place. **New York
city is the worst case in the file**: it spans five counties, the largest share is
Brooklyn at 30.9%, and the five county leans run from -64.8 (Manhattan) to +29.8 (Staten
Island). NYC therefore inherits Brooklyn's -44.0, when the true citywide two-party lean
across the five boroughs in this same file is -38.8, and no single borough figure
describes the city. 65 places have less than
55% of their population in the county they were assigned. For those rows the file also
stores `pop_by_county`, so a consumer that wants to can compute a population-weighted
lean across the parts instead of taking the winner. That would be strictly better and is
not what this build does, by instruction.

Third: a county lean is a **2024 presidential** lean. It is not a measure of local
politics, of how a place feels to live in, or of anything current. It is one election,
one office, one day.

---

## 2. Which election source, and why

Ranked by how much they are trusted, and what actually happened:

**First choice, could not be used: MIT Election Data and Science Lab, "County
Presidential Election Returns 2000-2024"**, Harvard Dataverse,
`doi:10.7910/DVN/VOQCHQ` (v20.0, released 2026-02-25, file
`countypres_2000-2024.tab`). This is the correct academic instrument and it is
county-level out of the box. Every download route returns:

```
{"status":"ERROR","message":"You may not download this file without the
 required Guestbook response for guestbookID 458."}
```

The file is gated behind a Harvard Dataverse guestbook form that collects personal
details. Tried the plain access API, `?format=original`, and `?gbrecs=true`; all
refused. Submitting that form on someone's behalf is not something this build does, so
this dataset is unavailable to a script. **If you want the canonical academic county
file, download it by hand from
<https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ> and it
can be swapped in as a drop-in replacement.**

**Used as the primary: MIT Election Data and Science Lab, `2024-elections-official`**
(<https://github.com/MEDSL/2024-elections-official>). Official precinct-level returns
transcribed from each state's own canvass, one zip per state, same lab, same
methodology, published openly on GitHub with a per-state source list and a codebook.
Aggregated to county here. Chosen because it is the academic/official-canvass source and
because it is the only option that gives **real Alaska boroughs** (see §5) and a real
third-party vote breakdown. Cost of using it: the aggregation has to be done and
checked, which is where the rest of this document comes from. 3,067 of 3,142 counties
come from here.

**Used only as a referee: MEDSL `2024-president-state.csv`** from the same repo, the
official certified state totals. Never written into the output. Every state's aggregated
county sum is checked against it, and that check is what caught all the defects in §4.

**Used only as a per-county repair: `tonmcg/US_County_Level_Election_Results_08-24`**
(<https://github.com/tonmcg/US_County_Level_Election_Results_08-24>), a long-running
public county-results repository built from AP/network feeds. This is news-derived, so
it is deliberately subordinate. It is used for exactly 75 county rows (2.4%) where the
primary failed the referee check, and **every one of those rows is labelled
`"source": "tonmcg_county"`** so it can be filtered out or re-sourced. Its national
state-total agreement is excellent (50 of 51 states match the certified D and R totals
to the vote), which is why it is trustworthy enough for spot repair.

Note on the ordering, because it matters: a state whose own aggregated total already
matches the certified total is **left alone even when individual counties disagree with
tonmcg**, because in that case tonmcg is the one that is wrong. Oregon and Washington
are the live examples: four Oregon counties differ from tonmcg by 2-4%, but the MEDSL
aggregation reproduces Oregon's certified state total to -0.02% while tonmcg's Oregon is
off by -0.98%. Those counties were not "repaired".

---

## 3. The lean formula

Party positions on the axis, stated in the script so they can be argued with:

```python
AXIS = {'DEMOCRAT': -100.0, 'REPUBLICAN': 100.0}

lean = (AXIS['DEMOCRAT']*dem_votes + AXIS['REPUBLICAN']*rep_votes) / (dem_votes + rep_votes)
     = (rep_votes - dem_votes) / (dem_votes + rep_votes) * 100
```

So the lean is the two-party margin in percentage points: -100 = every two-party vote
Democratic, 0 = even split, +100 = every two-party vote Republican. It is vote-weighted
by construction.

Two judgement calls in there:

1. **The two parties are pinned to the ends of the scale.** The Canadian file spreads six
   parties across the axis (Liberal -18, Conservative +60, NDP -68, Bloc -8, Green -52,
   PPC +82) and takes a vote-weighted mean, so no Canadian riding gets anywhere near
   +/-100. The US file uses the full width. **A US +45 and a Canadian +45 are not the
   same thing and must not be compared.** If cross-country comparability matters more
   than within-country spread, rescale the US lean by about 0.6 and say so in the app.
2. **Third parties are counted but excluded from the lean.** They are 2.2% of the
   national vote in this file and they do not share an axis: Libertarian sits right of
   Republican on economics, Green sits left of Democratic, and the largest single bloc
   (Kennedy, where he stayed on the ballot) is not placeable at all. Assigning them
   positions would push invented precision into every county for under two points of
   vote. `other_votes` is carried in every row so anyone who disagrees can redo it.

Labels use the same bands as the Canadian file, so the app's wording stays consistent:
solid left < -40, leans left < -12, swing < +12, leans right < +40, else solid right.
On these bands the country splits 1,646 solid right / 827 leans right / 361 swing /
229 leans left / 79 solid left. Trump carried 2,678 counties, Harris 464. That lopsided
county count is not a lopsided vote count, and the app must not present it as one.

Every row carries `dem_votes`, `rep_votes`, `other_votes`, `total_votes`, `dem_pct`,
`rep_pct` and `two_party_votes` so the arithmetic can be re-derived from the row itself.
`dem_pct` and `rep_pct` are shares of **total** votes, not of the two-party vote.

---

## 4. What was wrong in the raw precinct data, and what was done about it

The referee check is: each state's summed county totals must reproduce the certified
state total within 0.5% for both D and R. Five states failed. All five failures were
real defects, not rounding.

| state | what was wrong | what was done |
| --- | --- | --- |
| **LA** | MEDSL's Louisiana note: "Louisiana reports early voting only at the parish level, as such early votes are NOT included in the precinct data." All 64 parishes were ~48% short of certified. Early voters are not a random sample, so the lean itself was biased, not just the totals. | all 64 parishes replaced from the reference file |
| **MO** | MEDSL parks Kansas City under a synthetic `county_fips = 36000`. `36` is New York's state FIPS, so left alone it drops 124,288 Missouri votes into New York. | pseudo-county dropped; the four Kansas City counties (Cass 29037, Clay 29047, Jackson 29095, Platte 29165) replaced from the reference file, since the pseudo-county cannot be split back apart |
| **IN** | three counties broken in the source: St. Joseph (18141) is exactly 2x (each precinct appears twice under two labels), Hendricks (18063) has a county-total row mislabelled as precinct "1229-Washington 29", Monroe (18105) has only 26 of its precincts | those three counties replaced |
| **NJ** | NJ publishes election-district rows *and* a municipal roll-up row for the same municipality ("Allendale" alongside "Allendale 1..4"), double counting everything | 693 roll-up rows dropped by a strict-prefix rule; 3 residual counties (Gloucester 34015, Mercer 34021, Union 34039) replaced |
| **ME** | Cumberland County 4% short (ballots not present in the precinct file) | Cumberland (23005) replaced; that closed the state gap exactly (5,310 votes) |

Applied to every state, not just the failures:

- **Voting-mode double counting.** States report either one `TOTAL` row per candidate or
  one row per mode (election day / absentee / early / provisional), and CT, DE, OK, RI, NJ
  and NY report **both**. Summing blindly double counts those. Rows are grouped on
  (county, jurisdiction, precinct, candidate, party, district) and `TOTAL` wins when it
  appears alongside split modes.
- **Meta rows dropped.** `OVERVOTES`, `UNDERVOTES`, `TOTAL BALLOTS CAST`, `CAST VOTES`,
  `REGISTERED VOTERS` and similar arrive in the `candidate` column. Left in, they
  inflated Maine's "other" to 853,331 (from `TOTAL BALLOTS CAST`) and Oregon's to
  329,210 (from `CAST VOTES`).
- **Suppressed counts.** Some small jurisdictions in CA, KS, NV and NM publish `votes = "*"`
  for privacy. Those rows are skipped, not guessed.
- **Shannon County SD (46113) renamed to Oglala Lakota County (46102)** in 2015; MEDSL
  still uses the old code. Remapped.
- **California precinct suffixes** (`202` and `202A` etc.) are summed, per the Statewide
  Database FAQ that MEDSL cites; they are absentee splits, not duplicates.

Remaining residuals after all of it (worst six states, D and R vs certified):

```
RI  dem -0.49%  rep -0.05%      WA  dem -0.11%  rep -0.18%
AK  dem -0.24%  rep -0.03%      CA  dem -0.07%  rep -0.16%
VA  dem +0.07%  rep +0.05%      PA  dem -0.06%  rep -0.01%
```

Rhode Island and Georgia are the only states with votes on rows carrying no county code
at all: **RI 1,570 votes and GA 858 votes are unallocated and simply absent** from the
county file. That is the whole of Rhode Island's residual.

---

## 5. Alaska: reports by district, not by county

Alaska is the one state that does not publish everything by borough, and it needed a
documented decision rather than a workaround.

What the source actually contains: MEDSL's Alaska file carries **both** a borough
(`county_fips`, e.g. `02020` Anchorage) on precinct rows **and** a state house district
(`jurisdiction_name`, e.g. `DISTRICT 18`). But Alaska publishes its absentee, early and
question ballots only for the whole house district, so those rows arrive with an **empty
`county_fips`**. That is 164,890 votes, about **49% of Alaska's presidential vote**.
Alaska house districts do not nest inside boroughs, so the district-only votes cannot
simply be handed to a borough.

The two off-the-shelf county-level files both dodge this by not using boroughs at all:
MEDSL's own county dataset and tonmcg both key Alaska on **state house districts
02001-02040**, which are useless for a place-to-county join (Anchorage is not a
district).

What this build does, so Alaska keys on boroughs like every other state:

```
borough total = the borough's own precinct votes
              + that house district's district-only votes, split across the
                district's boroughs in proportion to the same candidate's
                precinct votes in each borough
```

Done per candidate, so a district's absentee ballots are shared out along the same
partisan split the district's precincts showed. Result: **all 30 Alaska boroughs and
census areas present**, summing to Alaska's certified state total within -0.24% D /
-0.03% R (401 votes are stranded in districts with no precinct rows at all and are
dropped). **Every Alaska row carries `"imputed": "ak_district_allocation"`.** Alaska
borough leans are half measured and half allocated, and they are the one part of this
file that is partly modelled rather than counted. Anchorage lands at -1.5 (swing), which
matches the reported Anchorage result.

## 5b. Connecticut, Hawaii, DC

- **Connecticut** is keyed on the **pre-2022 eight counties** (09001-09015), not the nine
  post-2022 planning regions, because that is what both the election returns and the
  2020 Census place file use. Current Census population products use the planning
  regions, so CT county population had to be rebuilt by summing town estimates back into
  the old counties via `national_cousub2020.txt`. If the app ever moves to planning
  regions, CT has to be rebuilt on both sides at once. (tonmcg uses planning regions,
  which is why CT is excluded from repair.)
- **Hawaii: Kalawao County (15005) is absent.** Population 82, the Kalaupapa settlement
  on Molokai. It has no election district of its own; the source carries no `15005` rows
  at all and every Molokai precinct is crosswalked to Maui County (15009), so Kalawao's
  voters are counted inside Maui. So the file has 3,142 counties, not 3,143. Any Kalawao
  place will not join. Checked directly: 70 Maui precincts, zero Kalawao.
- **DC** is one row, `11001`, as it should be. tonmcg splits DC into eight ward rows
  (11001-11008); those are not real county FIPS and are not used.

---

## 6. Place to county

`data/us/place_county.json`, 31,617 rows, 7-digit place GEOID (state FIPS + place FIPS)
to 5-digit county FIPS.

Base relationship: **`national_place_by_county2020.txt`**, the Census Bureau's national
place-by-county reference file. 2020 vintage, which matches the county vintage of the
election data (including old Connecticut). Covers incorporated places and CDPs. Puerto
Rico and the island areas are in that file; **571 territory places are dropped** because
there is no county lean for them.

30,323 places sit in one county. **1,294 straddle county lines** (up to five counties;
NYC and Dallas both hit five). For those, the county holding **the largest share of the
place's population** wins, and the row records it:

```json
"2938000": {"county": "29095", "multi_county": true,
            "counties": ["29037","29047","29095","29165"],
            "pop_by_county": {"29037":97,"29047":143075,"29095":317383,"29165":55477},
            "share": 0.615, "weight_source": "subest2024_sumlev157"}
```

`multi_county: true` on all 1,294. `share` is the winning county's fraction of the
place's population, so a consumer can see how shaky the assignment is.

Two population sources, both authoritative, both recorded per row in `weight_source`:

- **`subest2024_sumlev157`** (1,107 places): Census Population Estimates
  `sub-est2024.csv`, summary level 157 = place part within county, `POPESTIMATE2024`.
  This file omits county parts that hold no population, so a part missing from the
  weights is treated as zero rather than unknown (Dallas's Ellis and Rockwall slivers,
  for example).
- **`census2020_blocks_tigerweb`** (187 places): SUB-EST covers incorporated places and
  MCDs but **not CDPs**, so 193 straddling CDPs plus a few incorporated places had no
  weights. For those, exact **2020 Census block population inside the place boundary** is
  pulled from TIGERweb: fetch the place polygon, then sum `POP100` over the census blocks
  it contains, grouped by county. That is a direct decennial count, not an estimate.
  Example: Cullomburg CDP, AL = 105 people in Choctaw County (01023), 21 in Washington
  County (01129), so 01023 wins.

**Nothing is unresolved: 0 places fell back to an arbitrary tiebreak**, and 0 places map
to a county with no lean.

How shaky the multi-county assignments are:

```
share 0.95-1.00 : 602      the sliver cases, safe
share 0.80-0.95 : 301
share 0.60-0.80 : 270
share 0.50-0.60 : 115      near-even splits, treat with care
share below 0.50:   6      the assigned county holds a minority of the place
```

The six worst, with the spread of county leans they are choosing between: New York city
NY (0.31, leans -64.8 to +29.8), Braselton town GA (0.32, -16.7 to +55.4), Four Corners
CDP FL (0.40, -13.8 to +24.9), Emerson village NE (0.46, +7.0 to +59.7), Wamac city IL
(0.47), Sheldahl city IA (0.47). For those the lean the app shows is close to a coin
flip between real, different answers.

---

## 7. Validation

```
counties written : 3142      (3,144 current county-equivalents, minus Kalawao HI,
                              minus 1 because CT is 8 old counties not 9 regions)
  from MEDSL precinct returns : 3067
  repaired from tonmcg        : 75    (LA 64, MO 4, IN 3, NJ 3, ME 1)

national votes   : 155,692,359   dem 75,003,641  rep 77,288,712  other 3,400,006
MEDSL official   : 155,259,378   difference +432,981  (+0.279%)
```

D is within -0.02% and R within -0.02% of the certified national totals; **the whole
+0.28% difference is in `other_votes`** (+460,821). That is expected: the precinct files
list individual write-in candidates by name, while the state file aggregates or omits
some of them. The FEC's official 2024 national turnout for president is about
156.30 million, which includes write-ins and blanks this file does not, so 155.69M sits
between MEDSL's 155.26M and the FEC's 156.30M and is the right order of magnitude. The
task expected "roughly 155 million"; the actual figure is 155.69M, which is +0.4% above
155M and -0.4% below the FEC number.

Spot checks, all as expected:

| FIPS | county | lean | label | dem | rep | check |
| --- | --- | --- | --- | --- | --- | --- |
| 06075 | San Francisco County, CA | **-67.6** | solid left | 323,706 | 62,592 | strongly negative, yes |
| 11001 | District of Columbia | **-86.6** | solid left | 294,185 | 21,076 | strongly negative, yes |
| 48393 | Roberts County, TX | **+92.9** | solid right | 20 | 547 | strongly positive, yes (most Republican county in the country) |
| 48431 | Sterling County, TX | +86.3 | solid right | 43 | 583 | strongly positive, yes |
| 04013 | Maricopa County, AZ | **+3.5** | swing | 980,016 | 1,051,531 | near zero, yes |
| 06037 | Los Angeles County, CA | -34.0 | leans left | 2,416,522 | 1,189,227 | the coarseness problem in one row |
| 02020 | Anchorage Municipality, AK | -1.5 | swing | 64,781 | 62,922 | partly allocated, see §5 |
| 09001 | Fairfield County, CT | -19.9 | leans left | 267,019 | 178,263 | old CT county, see §5b |
| 29095 | Jackson County, MO | -19.6 | leans left | 187,026 | 125,610 | Kansas City repair worked |
| 22071 | Orleans Parish, LA | -68.9 | solid left | 130,749 | 24,119 | Louisiana repair worked |
| 15005 | Kalawao County, HI | ABSENT | | | | Hawaii does not report it |

Extremes: most left is DC -86.6, then Prince George's County MD -77.0 and Baltimore city
-74.9. Most right is Roberts County TX +92.9, then Hayes County NE +92.3 and Grant
County NE +91.8. Those are all tiny-population counties, which is what you would expect
at the tails.

---

## 8. Every URL opened for this build

Election data:
- <https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/VOQCHQ> (dataset metadata, MEDSL county file, v20.0)
- <https://dataverse.harvard.edu/api/access/datafile/13573089> and `?format=original`, `?gbrecs=true` (all refused, guestbook 458)
- <https://electionlab.mit.edu/data> (MEDSL data index, confirmed the county dataset exists and links to Dataverse only)
- <https://api.github.com/orgs/MEDSL/repos> (found `2024-elections-official`)
- <https://api.github.com/repos/MEDSL/2024-elections-official/git/trees/HEAD?recursive=1> (file inventory; confirmed there is a `2024-senate-county.csv` but **no** president-county file)
- <https://raw.githubusercontent.com/MEDSL/2024-elections-official/main/README.md> (per-state sources and warnings, incl. the Louisiana early-vote gap, the Missouri 36000 note, the NJ municipal-total note, the Indiana straight-party warning)
- <https://raw.githubusercontent.com/MEDSL/2024-elections-official/main/codebook.md>
- <https://raw.githubusercontent.com/MEDSL/2024-elections-official/main/2024-president-state.csv>
- `https://raw.githubusercontent.com/MEDSL/2024-elections-official/main/individual_states/{ak..wy}24.zip` (51 files, ~128 MB zipped)
- <https://raw.githubusercontent.com/tonmcg/US_County_Level_Election_Results_08-24/master/2024_US_County_Level_Presidential_Results.csv>
- <https://www.fec.gov/documents/5644/2024presgeresults.pdf> (FEC official 2024 presidential general election results, the reference for the ~156.3M national turnout figure quoted in §7; not used as build input)

Geography and population:
- <https://www2.census.gov/geo/docs/reference/codes2020/> (directory listing)
- <https://www2.census.gov/geo/docs/reference/codes2020/national_place_by_county2020.txt>
- <https://www2.census.gov/geo/docs/reference/codes2020/national_cousub2020.txt>
- <https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/cities/totals/sub-est2024.csv>
- <https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Census2020/MapServer> (layer list; 10 = Census Blocks, 26 = Incorporated Places, 28 = Census Designated Places)
- <https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Census2020/MapServer/10> (field list, confirmed `POP100` and grouped statistics support)
- TIGERweb `/26/query` and `/28/query` for place geometry, `/10/query` for block `POP100` grouped by county (about 400 calls, cached)

Checked and rejected:
- <https://api.census.gov/data/2020/dec/pl/geography.json> and `/2020/dec/dhc/geography.json` (summary level 159 "place (or part)" within county exists in DHC) but every data query now returns **"Missing Key"**; the Census API requires an API key, so this route is unavailable to this build and TIGERweb was used instead
- <https://voterportal.sos.la.gov/static/2024-11-05> and `/Graphical/...` (Louisiana SOS parish results are a JavaScript app with no machine-readable export found, so the LA repair came from the reference file rather than the state directly)
- <https://api.github.com/repos/openelections/openelections-data-la/contents/> (no 2024 directory, so no OpenElections fallback for Louisiana)
- <https://github.com/rearc-data/mit-county-presidential-2000-2016> (mirror of the MEDSL county file, stops at 2016)

---

## 9. Known gaps, in one place

1. Kalawao County HI (15005) has no row. Hawaii does not report it separately.
2. RI 1,570 votes and GA 858 votes have no county code in the source and are dropped.
3. Alaska's 30 boroughs are ~51% counted, ~49% allocated from house-district totals.
   Flagged `imputed`.
4. 75 county rows (LA 64, MO 4, IN 3, NJ 3, ME 1) come from a news-derived file, not the
   academic one. Flagged `source: "tonmcg_county"`.
5. `other_votes` runs about 15% high nationally against the certified state file because
   the precinct files itemise write-ins. D, R and therefore every `lean` are unaffected.
6. Connecticut is on the pre-2022 counties. Everything else is on the current vintage.
7. Indiana's source is known by MEDSL to fold straight-party votes into candidate totals
   in some counties. The three counties where that broke the arithmetic were repaired;
   there may be smaller residual inflation elsewhere in Indiana that is under the 2%
   detection threshold. It inflates D and R together, so the effect on lean is small.
8. The lean is 2024 presidential only. No midterm, state, or local behaviour is in it.
