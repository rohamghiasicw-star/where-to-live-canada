# "Healthier lifestyle" dimension - source verification

Verified 2026-08-21. Every number below was measured off a real HTTP response or read out of a
file actually downloaded to disk. Nothing here is estimated or recalled. Where something could
not be confirmed it says so, in those words, in the "Could not confirm" section at the bottom.

**Provenance:** every URL in this document was requested directly and returned the status and
byte count shown. All join percentages come from scripts run against the app's own
`data/us/places.json` and `data/allplaces.json`, not from documentation. Files actually
downloaded and parsed: the PLACES wide CSV (43.0 MB), the PLACES filtered export (11.2 MB), the
CHR analytic CSV (12.5 MB) and its dictionary, a Census Block Assignment File, a live Geocorr
run, both StatCan CCHS tables (27.0 MB each, ~490 MB uncompressed), both StatCan crosswalks
(45.9 + 48.1 MB) and the CIHI Indicator Library (70.3 MB, all 822,882 rows parsed). CDC's own
statements were read in a real browser because `www.cdc.gov` returns 403 to scripted clients.

**User request being served:** "Healthier lifestyle / Ex San Diego vs Kansas City" - a measure
that separates a fit, active, outdoorsy city from a sedentary one.

**Join keys available:** US 7-digit Census place GEOID, state, lat/lon, place->county FIPS map.
Canada CSD code, lat/lon.

**Headline, both countries:**

- **US: works, at true place level.** CDC PLACES publishes a real Place release - not tract-only -
  and it joins to **99.1%** of the app's US places with zero crosswalk work. Public domain.
  Two catches: **Pennsylvania and Kentucky are entirely empty in the 2025 release** (fixable from
  the 2024 release), and **CDC explicitly says not to rank overall health on a composite** of
  these measures, though comparing places on an individual measure is endorsed.
- **Canada: your "health regions are the floor" assumption is CONFIRMED - but your conclusion that
  this makes the dimension US-only is REFUTED.** A free StatCan CSD -> health-region crosswalk
  covers **100% of the app's 712 Canadian places** with zero split CSDs. The real objection is
  resolution, not joinability: **711 places share only 106 distinct values**, versus 4,052
  distinct value-triples across 4,056 US places. Physical activity specifically is only complete
  at a **2017/2018** vintage.
- **County Health Rankings: the data is fine, the licence is not.** Its Terms of Use bar
  commercial use without written consent. Use CDC PLACES County (public domain) instead.

---

## Verdict table

| # | Source | Granularity | Verdict |
|---|--------|-------------|---------|
| 1 | **CDC PLACES, Place Data 2025** (`eav7-hnsx` / `vgc8-iyc4`) | **Census place** | **USABLE** - the one to use |
| 1b | CDC PLACES, Place Data 2024 (`sd8v-uq83`) | Census place | **USABLE** - needed as the PA/KY backfill |
| 1c | CDC PLACES, County Data 2025 (`swc5-untb`) | County | USABLE - public-domain county fallback |
| 2 | County Health Rankings 2025 | County (5-digit FIPS) | **NOT USABLE for a commercial app** - licence forbids commercial use without written consent. Data itself is fine and free. |
| 3a | **StatCan CCHS table 13-10-0972-01** (obesity, smoking, self-rated health) | **Health region** (100 w/ data) | **USABLE** - 99% coverage, 2023/2024, OGL free |
| 3b | StatCan table 13-10-0113-01 (physical activity) | Health region (108 w/ data) | **USABLE WITH WORK** - only complete at **2017/2018**, needs the older crosswalk |
| 3c | **StatCan 82-402-X CSD->health-region crosswalk** | dissemination block -> CSD -> HR | **USABLE** - free CSV, **100% of the app's 712 places**, pop-weighted |
| 3e | CIHI Indicator Library XLSX | Health region (141 names) | USABLE WITH WORK for **smoking 2023-24 only**; NOT USABLE for physical activity (5 regions) |
| 3e | open.canada.ca / Health Canada | Canada + province only | **NOT USABLE** - nothing at CSD or finer |
| 3e | CANUE / Can-ALE / Can-BICS | dissemination area | **NOT USABLE** - application-gated to academics, and it measures the built environment, not behaviour |
| 4 | Tract->place crosswalk (Geocorr 2022 / Census BAF) | tract -> place, pop-weighted | USABLE - but **moot**, PLACES has a real place release |

---

## 1. CDC PLACES - Local Data for Better Health

### CONFIRMED: there is a true PLACE release. It is not tract-only.

Your belief was right. PLACES ships four separate geographic levels, each its own dataset:
county, **place**, census tract, and ZCTA. I pulled the whole Socrata catalogue to check
rather than trusting the docs.

Catalogue query actually run:
```
https://data.cdc.gov/api/catalog/v1?q=PLACES&limit=60&search_context=data.cdc.gov
-> HTTP 200, 1,119,185 bytes, resultSetSize 109
```

Both `data.cdc.gov` and `chronicdata.cdc.gov` serve the same dataset ids (both HTTP 200 on
`/resource/eav7-hnsx.json?$limit=1`). Use `data.cdc.gov`.

### 1a. The two formats of the 2025 Place release

There are two shapes of the same data. Pick based on how you want to load it.

| | **Long / tidy** | **Wide / "GIS Friendly"** |
|---|---|---|
| Dataset id | **`eav7-hnsx`** | **`vgc8-iyc4`** |
| Name | PLACES: Local Data for Better Health, Place Data, 2025 release | PLACES: Place Data (GIS Friendly Format), 2025 release |
| Landing page | https://data.cdc.gov/dataset/eav7-hnsx | https://data.cdc.gov/dataset/vgc8-iyc4 |
| Bulk CSV | `https://data.cdc.gov/api/views/eav7-hnsx/rows.csv?accessType=DOWNLOAD` | `https://data.cdc.gov/api/views/vgc8-iyc4/rows.csv?accessType=DOWNLOAD` |
| Rows | **2,150,438** (measured via `$select=count(*)`) | **29,923** data rows + 1 header (measured: `wc -l` = 29,924) |
| Columns | 24 | 166 |
| **Measured size** | not downloaded - see "Could not confirm" | **45,085,120 bytes = 43.0 MB** (downloaded, HTTP 200, 48.3 s) |
| Shape | one row per place x measure x value-type | one row per place, one column per measure |
| Join key | `locationid` | `placefips` |
| `rowsUpdatedAt` | 2025-12-12T15:59:44Z | 2025-12-04T10:44:01Z |

**Recommended: neither of the above. Use a filtered CSV export.** Socrata honours SoQL on the
`.csv` endpoint, so you can pull only the six lifestyle measures instead of 43 MB or 500 MB:

```
https://data.cdc.gov/resource/eav7-hnsx.csv
  ?$select=locationid,stateabbr,locationname,year,measureid,data_value,
           low_confidence_limit,high_confidence_limit,totalpopulation
  &$where=datavaluetypeid='CrdPrv' AND measureid in
          ('LPA','OBESITY','CSMOKING','BINGE','GHLTH','SLEEP')
  &$limit=250000
```
**Measured: HTTP 200, 11,753,830 bytes = 11.2 MB, 167,568 data rows, 13.7 seconds.** No API
token needed at this volume. Real first row:
```
"0146768","AL","Marion","2022","SLEEP","44.0","36.6","51.6","3176"
```

### 1b. Geographic level and join key - tested against the app's real place list

- Geographic unit: **incorporated places and Census Designated Places (CDPs)**. CDC's own words
  from the dataset description: "This dataset contains model-based place (incorporated and
  census-designated places) estimates."
- Join key: **`locationid`** (long format) / **`placefips`** (wide format) = the **7-digit Census
  place GEOID**. Confirmed all 29,923 values are exactly 7 characters. `0666000` = San Diego,
  `2938000` = Kansas City MO. **Direct join to your place GEOID. No crosswalk needed.**
- Also carries `geolocation` as a GeoJSON Point, plus `totalpopulation` and `totalpop18plus`.

**Join test actually run** against `data/us/places.json` (4,226 places in the file):

```
app US places                     : 4,226   (all 7-digit geoids)
PLACES rows                       : 29,923  (all 7-digit fips)
MATCHED on GEOID                  : 4,188   (99.10%)
MISSED                            :    38
  of which Puerto Rico            :    29
  Massachusetts                   :     4   (Methuen, Watertown, Amesbury, Easthampton)
  WI 2, TX 1, IL 1, FL 1
non-null LPA among matched        : 4,056 / 4,188  (96.85%)
```
Same 4,056 count for OBESITY, CSMOKING, BINGE and GHLTH - they are null together, never
independently.

Puerto Rico is a definite, structural exclusion, and CDC says so: "PLACES covers the entire
United States - 50 states and the District of Columbia". **PR rows in the file: 0.** Confirmed
51 StateAbbr values present (50 states + DC).

### 1c. THE GOTCHA: Pennsylvania and Kentucky are empty in the 2025 release

This is the biggest practical finding and it is not flagged anywhere obvious on the landing page.

In the **2025** release, PA and KY have **35 of the 40 measures completely null** - including
every one you asked for. Measured off the downloaded CSV:

```
PA: n=1,844 places, ALL-NULL measures: 35, filled: 5
KY: n=  550 places, ALL-NULL measures: 35, filled: 5
CA: n=1,545 places, ALL-NULL measures:  0, filled: 40
MO: n=  964 places, ALL-NULL measures:  0, filled: 40
```

The only 5 measures PA and KY do have are `COLON_SCREEN, DENTAL, MAMMOUSE, SLEEP, TEETHLOST` -
which is exactly the set CDC states is built from **BRFSS 2022** rather than BRFSS 2023.

**Cause CONFIRMED**, verbatim from https://www.cdc.gov/brfss/annual_data/annual_2023.html
(read in a real browser - see gotcha 1h.5):

> "The aggregate BRFSS combined landline and cell phone data set is built from the landline and
> cell phone data submitted for 2023 and includes data from **48 states**, the District of
> Columbia, Guam, Puerto Rico, and the US Virgin Islands. **During 2023, Kentucky and
> Pennsylvania were unable to collect enough data to meet the minimum requirements to be included
> in this public data set.**"

So it is an upstream BRFSS 2023 collection failure in those two states, not a PLACES publishing
choice. It will resolve on its own in the 2026 release if KY and PA hit their 2024 targets - but
do not count on that until you see it.

Philadelphia (`4260000`, pop 1,603,797) and Pittsburgh (`4261000`) both return null for
physical inactivity in the 2025 release. This affects 132 of your matched places (86 PA + 46 KY).

The gap is **state-wide across every geography**, not a place-level quirk. Verified:
- Place 2025 (`eav7-hnsx`): LPA non-null - PA 0, KY 0, CA 3,090
- Tract 2025 (`cwsq-ngmh`): LPA non-null - PA 0, KY 0, CA 9,070
- County 2025 (`swc5-untb`): LPA non-null - PA 0, KY 0, CA 116

**The fix: backfill PA and KY from the 2024 release.** Verified working:
- Dataset: **`sd8v-uq83`** - PLACES: Local Data for Better Health, Place Data 2024 release
- Same 29,923 distinct `locationid` values, so the join is identical
- LPA non-null counts: **PA 3,688, KY 1,100, CA 3,090** - PA and KY fully populated
- Real value: Philadelphia `4260000` LPA **year 2022, crude 26.5, age-adjusted 26.8**
- County equivalent for 2024 is `fu4u-a9bh` (PA 134 rows = 67 counties x 2 value types,
  KY 240 = 120 x 2)

Cost of the backfill: those two states carry a **2022** BRFSS vintage while everywhere else
carries **2023**. Store the vintage per place and either footnote it or accept the one-year skew.

### 1d. Measures - all five you asked for exist, plus sleep

40 distinct `measureid` values in the place file. The ones that matter here:

| measureid | Category | Short text | Full measure text | Year | Source |
|---|---|---|---|---|---|
| **`LPA`** | Health Risk Behaviors | Physical Inactivity | "No leisure-time physical activity among adults" | 2023 | BRFSS |
| **`OBESITY`** | Health Outcomes | Obesity | "Obesity among adults" | 2023 | BRFSS |
| **`CSMOKING`** | Health Risk Behaviors | Current Cigarette Smoking | "Current cigarette smoking among adults" | 2023 | BRFSS |
| **`BINGE`** | Health Risk Behaviors | Binge Drinking | "Binge drinking among adults" | 2023 | BRFSS |
| **`GHLTH`** | Health Status | General Health | "Fair or poor self-rated health status among adults" | 2023 | BRFSS |
| `SLEEP` | Health Risk Behaviors | Short Sleep Duration | "Short sleep duration among adults" | **2022** | BRFSS |

All are `data_value_unit` = `%`. Two value types per measure, selected by `datavaluetypeid`:
- **`CrdPrv`** = Crude prevalence (the raw share of that place's adults)
- **`AgeAdjPrv`** = Age-adjusted prevalence (removes the effect of a place's age structure)

**Use `AgeAdjPrv` for a lifestyle ranking.** A retirement town looks unhealthy on crude
prevalence purely because it is old, which is not what "healthier lifestyle" means. Crude is the
better choice only if you want "what is the actual state of the people here".

The other 34 measures, for reference: ACCESS2, ARTHRITIS, BPHIGH, BPMED, CANCER, CASTHMA, CHD,
CHECKUP, CHOLSCREEN, COGNITION, COLON_SCREEN, COPD, DENTAL, DEPRESSION, DIABETES, DISABILITY,
EMOTIONSPT, FOODINSECU, FOODSTAMP, HEARING, HIGHCHOL, HOUSINSECU, INDEPLIVE, LACKTRPT,
LONELINESS, MAMMOUSE, MHLTH, MOBILITY, PHLTH, SELFCARE, SHUTUTILITY, STROKE, TEETHLOST, VISION.

### 1e. The San Diego vs Kansas City test - it works

Your exact example, real values pulled from `vgc8-iyc4` (crude prevalence, %):

| Place | GEOID | Pop | **Phys. inactivity** | **Obesity** | Smoking | Binge drink | Fair/poor health | Short sleep |
|---|---|---|---|---|---|---|---|---|
| **San Diego, CA** | 0666000 | 1,386,932 | **19.8** | **24.2** | 9.3 | 16.9 | 17.9 | 34.5 |
| **Kansas City, MO** | 2938000 | 508,090 | **29.7** | **38.5** | 15.6 | 16.7 | 21.5 | 36.5 |
| **Kansas City, KS** | 2036000 | 156,607 | **35.3** | **41.2** | 18.3 | 15.3 | 26.0 | 37.7 |

Physical inactivity spreads 19.8 -> 35.3 and obesity 24.2 -> 41.2 across exactly the pair the
user named. The dimension separates them cleanly and in the expected direction.

Note binge drinking runs the *other* way (San Diego highest at 16.9). If you fold binge drinking
into a composite "healthy" score it will penalise fit, affluent, social cities. Recommend LPA +
OBESITY as the spine, with GHLTH as a sanity check, and leave BINGE out or make it its own axis.

### 1f. MODELLED, not measured - and CDC has an explicit position on ranking

These are **small-area model-based estimates**, not measurements of the place. The method is
**multilevel regression and poststratification (MRP)** - verbatim from
https://www.cdc.gov/places/methodology/index.html:

> "PLACES uses a multilevel regression and poststratification (MRP) method to generate estimates
> of each measure at the county, place (incorporated and census designated), census tract, and
> ZIP Code Tabulation Area (ZCTA) levels for adults >=18 years in the United States."

#### READ THIS BEFORE DESIGNING THE SCORE

CDC's FAQ has a question aimed directly at what this app does. Verbatim from
https://www.cdc.gov/places/faqs/index.html:

> **"Can I use the data for ranking?** Because these are modeled and not direct estimates, the
> data **should not be used for ranking the overall health** of any county, place, census tract,
> or ZCTA. PLACES does not provide a weighted composite score for the included counties, places,
> census tracts, or ZCTAs. Therefore, the data should not be used to rank the overall health of a
> local area. **However, counties, places, census tracts, or ZCTAs can be compared on individual
> measures.**"

That last sentence is the permission you need, and it shapes the design:

- **Sanctioned:** ranking places on **one named measure** - "physical inactivity, CDC PLACES
  2025". Comparing places on individual measures is explicitly endorsed.
- **Not sanctioned:** blending LPA + OBESITY + CSMOKING + GHLTH into a "health score" and ranking
  overall health on it. CDC names that exact thing and says not to do it.
- **Practical route:** keep the dimension as a single named measure (physical inactivity is the
  cleanest fit for "fit, active, outdoorsy vs sedentary"), label the source, and let the other
  measures live as separate displayed facts rather than blended ingredients. This is a
  presentation constraint, not a licence one - the data is public domain and nothing stops you
  technically. But if the app ever gets scrutiny, "we ranked on a single CDC measure and named
  it" is defensible and "we invented a composite health score from CDC data" is not.

CDC also warns about comparing point estimates naively:

> "it is not adequate to simply compare point estimates. The confidence intervals should also be
> considered, and some are very broad. The smaller the areas are, the broader the confidence
> intervals of an estimate will be. ... It may not be appropriate to draw conclusions when
> comparing estimates that have very broad confidence intervals."

and endorses age-adjustment for exactly your use case:

> "age-adjusted estimates that adjust for potential differences in the age-distribution across
> geographic units can be used for county- and place-level comparisons."

**Suggested citation**, verbatim from the same FAQ:
> "Centers for Disease Control and Prevention. PLACES: Local Data for Better Health. Accessed
> [date]. https://www.cdc.gov/places"

#### Why the 132 nulls, beyond PA/KY

CDC's FAQ, verbatim:
> "**Why do some geographic units not have estimates?** Estimates were calculated for all
> geographic units that had an adult population of 50 or more (total population >= 50 people,
> regardless of age before the 2024 release). ... If the count is less than 50, the estimate is
> not reported."

So outside PA/KY, missing values mean a place with fewer than 50 adults. Check `TotalPop18plus`
before treating a null as an error.

#### The dataset description

CDC's own dataset description, verbatim from the `data.cdc.gov` views API:

> "This dataset contains model-based place (incorporated and census-designated places)
> estimates. ... Because the small area model cannot detect effects due to local interventions,
> users are cautioned against using these estimates for program or policy evaluations. Data
> sources used to generate these model-based estimates are Behavioral Risk Factor Surveillance
> System (BRFSS) 2023 or 2022 data, Census Bureau 2020 population data, and American Community
> Survey 2019-2023 or 2018-2022 estimates. The 2025 release uses 2023 BRFSS data for 35 measures
> and 2022 BRFSS data for 5 measures (all teeth lost, dental visits, mammograms, colorectal
> cancer screening, and short sleep duration) that the survey collects data on every other year."

What that means in practice: nobody surveyed a representative sample of Fleetwood or Poway. CDC
fits a model on national BRFSS responses plus each area's demographic profile, then predicts the
prevalence. Two demographically similar towns in the same state will get similar estimates
**because they are demographically similar**, not because anyone measured them.

Practical consequences for the app:
1. **Never call it "measured" or "surveyed".** Honest phrasing: "CDC model-based estimate" or
   "CDC PLACES modelled estimate, 2025 release (BRFSS 2023)".
2. Every row ships `low_confidence_limit` / `high_confidence_limit`. San Diego LPA age-adjusted
   is 20.0 with a 95% CI of **17.9 to 22.4**. Small places have much wider intervals. If two
   places' intervals overlap, the ranking gap between them is not real - consider banding rather
   than showing an exact rank.
3. Because the model is demography-driven, this dimension will correlate hard with income and
   education. It is partly re-describing wealth. Worth knowing before you weight it.

### 1g. Licence and cost

**Public domain. Free. No login, no API key at these volumes.**
- Socrata `licenseId`: **`PUBLIC_DOMAIN`**, `license.name`: "Public Domain" (read from
  `https://data.cdc.gov/api/views/eav7-hnsx.json`)
- Attribution string in the metadata: "Centers for Disease Control and Prevention, National
  Center for Chronic Disease Prevention and Health Promotion, Division of Population Health"
- US federal government work, 17 U.S.C. 105. **Commercial use is fine.**

### 1h. Field gotchas found by reading the actual file

1. **In the wide format `vgc8-iyc4`, the `PlaceName` column contains the FIPS code, not the
   name.** The human-readable name is in **`LocationName`**. Verified:
   ```
   {"stateabbr":"CA","placename":"0666000","locationname":"San Diego","placefips":"0666000"}
   ```
   This looks like a CDC publishing bug in the 2025 GIS-friendly file. Do not key display names
   off `PlaceName`.
2. Wide-format column names are lowercased in the JSON API but TitleCase in the CSV download
   (`lpa_crudeprev` vs `LPA_CrudePrev`).
3. One wide-format column is renamed between id and label: field `isolation_crudeprev` carries
   the label `LONELINESS_CrudePrev`. In the long format the measureid is `LONELINESS`.
4. Null is an empty string in the CSV, not `NA` or `0`.
4. **`www.cdc.gov` returns HTTP 403 to every scripted client** - plain curl, curl with a browser
   User-Agent, and WebFetch all got 403 with 400-406 byte bodies on
   `/places/methodology/index.html`, `/places/about/index.html` and `/places/faqs/index.html`.
   The pages load fine in a real browser session. The **data** endpoints on `data.cdc.gov` are
   not affected and never 403'd. Every CDC quote in this document was read in a browser.
   Note also: a court-ordered banner is currently served at the top of CDC pages stating the site
   has been restored to its 2025-01-29 version and may change. The PLACES FAQ page is stamped
   **DEC. 11, 2025**, so the PLACES content itself is current.

### VERDICT 1: **USABLE.** True Census-place granularity, direct 7-digit GEOID join, 99.1% match
against the app's own place list, public domain, free, all five requested measures present, and
it separates San Diego from Kansas City exactly as intended. Two conditions: backfill PA and KY
from the 2024 release, and describe the numbers as modelled estimates rather than measurements.

---

## 2. County Health Rankings (Univ. of Wisconsin Population Health Institute / RWJF)

### 2a. The file

| | |
|---|---|
| Landing page | https://www.countyhealthrankings.org/health-data/methodology-and-sources/data-documentation (HTTP 200, 50,974 bytes) |
| **Bulk CSV** | **https://www.countyhealthrankings.org/sites/default/files/media/document/analytic_data2025_v3.csv** |
| HTTP | **200**, `application/octet-stream` |
| **Measured size** | **13,085,361 bytes = 12.5 MB** |
| Rows | 3,206 lines = **2 header rows + 3,204 data rows** |
| Columns | **796** |
| Data dictionary | `.../DataDictionary_2025.xlsx` - HTTP 200, **29,136 bytes** |
| Also offered | `analytic_data2025_v3.sas7bdat`, `chr_trends_csv_2025.csv`, `2025 County Health Rankings Data - v4.xlsx`, and a 2026-03-25 supplement (`analytic_supplement_20260325[1].csv`) |
| Release year field | 2025 |

**Gotcha: the CSV has TWO header rows.** Line 1 is human-readable labels, line 2 is the variable
codes. Parse with `next(reader)` twice and key off row 2.
```
line 1: State FIPS Code,County FIPS Code,5-digit FIPS Code,State Abbreviation,Name,Release Year,...
line 2: statecode,countycode,fipscode,state,county,year,county_clustered,v001_rawvalue,...
```

### 2b. Geographic granularity and join key

Measured from the file, not assumed:
```
national rows (statecode 00)          :     1
state-level rows (countycode 000)     :    51
true county rows                      : 3,152
```
Join key = **`fipscode`**, and **all 3,152 values are exactly 5 characters** (`01001`, `01003`,
...). Matches your place->county FIPS map directly.

### 2c. The columns you asked for - all three exist

| Measure | **Variable** | Description (verbatim from DataDictionary_2025.xlsx) | Non-null | Range |
|---|---|---|---|---|
| **Physical Inactivity** | **`v070_rawvalue`** | "Percentage of adults age 18 and over reporting no leisure-time physical activity (age-adjusted)." | 3,144 / 3,152 (99.7%) | 0.1180 - 0.4730 |
| **Access to Exercise Opportunities** | **`v132_rawvalue`** | "Percentage of population with adequate access to locations for physical activity." | 3,097 / 3,152 (98.3%) | 0.0000 - 1.0000 |
| **Food Environment Index** | **`v133_rawvalue`** | "Index of factors that contribute to a healthy food environment, from 0 (worst) to 10 (best)." | 3,100 / 3,152 (98.4%) | 0.0000 - 10.0000 |

Bonus columns in the same file, all verified present and populated:

| Measure | Variable | Non-null |
|---|---|---|
| Access to Parks ("population living within a half mile of a park") | `v179_rawvalue` | 2,846 (90.3%) |
| Adult Obesity | `v011_rawvalue` | 3,144 (99.7%) |
| Adult Smoking | `v009_rawvalue` | 3,144 (99.7%) |
| Poor or Fair Health | `v002_rawvalue` | 3,144 (99.7%) |
| Limited Access to Healthy Foods | `v083_rawvalue` | - |
| Food Insecurity | `v139_rawvalue` | - |
| Life Expectancy | `v147_rawvalue` | - |

Each measure also ships `_numerator`, `_denominator`, `_cilow`, `_cihigh`, and most ship a
`_flag` (0 = no flag, 1 = unreliable, 2 = suppressed) plus race-stratified variants
(`_race_aian`, `_race_asian`, `_race_black`, `_race_hisp`, ...). Note the ranges: v070, v132 and
v179 are **proportions 0-1**, not percentages, while v133 is a **0-10 index**. Do not mix scales.

**Ratios are decimals, not percents** - San Diego County v070 = `0.183`, i.e. 18.3%.

### 2d. It DOES cover Pennsylvania and Kentucky

The one thing CHR gives you that PLACES 2025 does not:
```
PA:  67 counties, Physical Inactivity non-null: 67
KY: 120 counties, Physical Inactivity non-null: 120
```
Because CHR's 2025 release uses **BRFSS 2022**, the same vintage as the PLACES 2024 backfill.

### 2e. Join test against the app's places

Run through `data/us/place_county.json` (31,617 entries, `{"county":"01017","multi_county":false}`):
```
app places                              : 4,226
  no county in the map                  :    38
  county not present in CHR             :     0
  CHR row present but v070 null         :    35
  USABLE physical inactivity via county : 4,153  (98.27%)
  (of which flagged multi_county        :   346)
```
Real values:
```
San Diego County, CA  06073  PhysInact 0.183  AccessExercise 0.9753  FoodEnvIdx 8.8  Parks 0.8018
Jackson County,   MO  29095  PhysInact 0.217  AccessExercise 0.9212  FoodEnvIdx 7.6  Parks 0.7325
Wyandotte County, KS  20209  PhysInact 0.353  AccessExercise 0.9272  FoodEnvIdx 7.0  Parks 0.7126
```
Directionally consistent with the PLACES place-level result, but note how much the county
average flattens it: county physical inactivity spreads 18.3 -> 35.3, while the place-level
numbers for the actual cities spread 19.8 -> 35.3. **A county value is not a city value** -
San Diego County includes El Cajon and Borrego Springs.

### 2f. Also modelled, and it says so

Verified by fetching
`https://www.countyhealthrankings.org/health-data/health-factors/health-behaviors/diet-and-exercise/physical-inactivity`
(HTTP 200, 52,645 bytes) and reading the rendered text:
- Data Source: **"Behavioral Risk Factor Surveillance System"**
- "The 2025 Annual Data Release used data from 2022 for this measure."
- "Physical Inactivity estimates are created using statistical modeling"
- "the 2022 Annual Data Release, the source for this measure switched from the United States
  Diabetes Surveillance System to BRFSS"

So CHR physical inactivity and PLACES LPA are **the same underlying survey, modelled twice**.
They are not independent corroboration of each other.

### 2g. THE BLOCKER: the licence forbids commercial use

Read from https://www.countyhealthrankings.org/terms-use (HTTP 200, 41,433 bytes, "Last updated:
December 16, 2024"). Verbatim:

> "CHR&R grants you a non-exclusive license to access and use those portions of the CHR&R Website
> without a password or logon **for personal or non-profit purposes including educational,
> research, or public health**, subject to the terms of this Agreement"

and, explicitly:

> "The CHR&R website Content **may not be copied or otherwise used for commercial use** (including
> without limitation, use to train AI models intended to be offered as commercial products)
> **without CHR&R's express prior written consent.** To discuss commercial use please email:
> [address redacted on the page]"

Preferred citation, if you do use it:
> "University of Wisconsin Population Health Institute. County Health Rankings & Roadmaps.
> www.countyhealthrankings.org"

This is not a CC or public-domain dataset. If "livable" is or will be a commercial product,
shipping CHR values is a licence violation unless you get written consent first.

### 2h. The public-domain replacement for CHR

You do not actually need CHR for the three headline behaviours, because CDC publishes the same
things at county level in the public domain:

**CDC PLACES: Local Data for Better Health, County Data, 2025 release**
- Dataset id: **`swc5-untb`**
- Bulk CSV: `https://data.cdc.gov/api/views/swc5-untb/rows.csv?accessType=DOWNLOAD`
- Rows: **229,298** (measured). Long format, same 24-column schema as the place file.
- Join key: `locationid` = **5-digit county FIPS**
- Licence: `PUBLIC_DOMAIN`
- Carries LPA, OBESITY, CSMOKING, BINGE, GHLTH - same measure ids
- Same PA/KY hole in 2025; backfill from **`fu4u-a9bh`** (County Data 2024), verified populated

What is genuinely CHR-only, with no public-domain equivalent found: **Access to Exercise
Opportunities (v132)** and **Food Environment Index (v133)**. Both are CHR-constructed composites.
See "Could not confirm" for what I did and did not check as substitutes.

### VERDICT 2: **NOT USABLE for a commercial app** as-is - the Terms of Use restrict use to
personal/non-profit/educational/research/public-health purposes and expressly bar commercial use
without written consent. The data itself is free, complete (99.7% county coverage), well
documented, correctly joined on 5-digit FIPS, and covers PA/KY. If the app is non-commercial, it
is **USABLE**. If it is commercial, use **CDC PLACES County (`swc5-untb`, public domain)**
instead for inactivity/obesity/smoking, and either drop the exercise-access and food-environment
angles or email CHR for consent.

---

## 3. Canada

### Your working assumption: HALF right. Health region IS the floor - but that does not make the dimension US-only.

You assumed (a) Canada floors out at health region, and (b) that being far coarser than a CSD
would make the dimension US-only. **(a) is CONFIRMED. (b) is REFUTED.**

There is a **free, machine-readable, dissemination-block-level CSD -> health-region crosswalk**,
and I ran it against your actual 712 Canadian places:

```
APP CANADIAN PLACES                        : 712
matched into the CSD->health-region crosswalk : 712   (100.00%)
places whose CSD spans >1 health region       :   0
```

**100% coverage, zero split CSDs.** Every Canadian place in the app can be assigned a health
region with no ambiguity. The join is not the problem. **The resolution is the problem** - see
3f, which is the part that should actually drive your decision.

Everything below I fetched and parsed myself.

### 3a. The health survey: StatCan CCHS, table 13-10-0972-01

| | |
|---|---|
| Table | **13-10-0972-01**, productId **13100972** - "Health characteristics, two-year period estimates" |
| Landing page | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310097201 |
| Download resolver | `https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/13100972/en` -> HTTP 200, 88 bytes, returns `{"status":"SUCCESS","object":"https://www150.statcan.gc.ca/n1/tbl/csv/13100972-eng.zip"}` |
| **Bulk file** | **https://www150.statcan.gc.ca/n1/tbl/csv/13100972-eng.zip** |
| HTTP / size | **200, 28,345,293 bytes = 27.0 MB zipped** (5.9 s) |
| Unzipped | `13100972.csv` = **511,729,459 bytes = 488 MB**, plus `13100972_MetaData.csv` = 25,083 bytes |
| Rows | **2,042,150** data rows |
| Reference periods | `2015/2016, 2017/2018, 2019/2020, 2021/2022, **2023/2024**` |
| Licence | Open Government Licence - Canada. Free, no login. |

Real header:
```
REF_DATE,GEO,DGUID,Age group,Sex,Indicators,Characteristics,UOM,UOM_ID,SCALAR_FACTOR,
SCALAR_ID,VECTOR,COORDINATE,VALUE,STATUS,SYMBOL,TERMINATED,DECIMALS
```

**Finest geography actually published = health region.** Measured from the real `DGUID` values in
the 2023/2024 slice:
```
health-region DGUIDs (prefix 2023A0007) : 100
province/territory DGUIDs (2021A0002)   :  13
Canada                                  :   1
```
Join key is the last 4 digits of `DGUID` = the **HRUID2023** code, which matches the crosswalk
exactly (`2023A00075923` -> HR `5923`).

**27 indicators.** Read them all; the lifestyle-relevant ones are:
`Body mass index, adjusted self-reported, obese` / `...overweight`, `Current smoker, daily`,
`Current smoker, daily or occasional`, `Heavy drinking`,
`Fruit and vegetable consumption, 5 times or more per day`,
`Perceived health, very good or excellent` / `...fair or poor`,
`Perceived mental health, very good or excellent` / `...fair or poor`,
`Perceived life stress, most days quite a bit or extremely stressful`,
`Life satisfaction, satisfied or very satisfied`,
`Sense of belonging to local community, somewhat strong or very strong`.

**There is NO physical-activity indicator in this table.** Confirmed against all 27.

**Suppression is much lower than feared on the measures that matter.** Measured on the
2023/2024 x Percent x Both sexes slice, health-region rows only:

| Indicator | Coverage | Range | STATUS codes |
|---|---|---|---|
| BMI obese | **99/100 (99%)** | 12.5 - 63.7 | 99 blank, 1 `F` |
| Current smoker, daily or occasional | **99/100 (99%)** | 5.9 - 63.1 | 99 blank, 1 `x` |
| Perceived health, very good or excellent | **99/100 (99%)** | 34.3 - 64.5 | 99 blank, 1 `F` |
| Perceived mental health, very good or excellent | **99/100 (99%)** | 39.6 - 71.8 | 99 blank, 1 `F` |
| Heavy drinking | **99/100 (99%)** | 8.1 - 34.0 | 98 blank, 1 `E`, 1 `x` |
| Fruit and vegetable consumption | **3/100 (3%)** | 18.5 - 26.7 | 97 `..`, 3 blank |

So: obesity, smoking, self-rated health and self-rated mental health are essentially complete at
health-region level. **Fruit/veg is effectively unpublished - do not plan around it.**

STATUS codes: `''` = usable, `..` = not available, `F` = too unreliable to publish, `x` =
suppressed for confidentiality, `E` = use with caution (value IS present).

Real obesity values, 2023/2024:
```
5932 Vancouver HSDA, BC                     17.2
5923 Fraser South HSDA, BC (= Surrey)       23.0
3595 City of Toronto Health Unit, ON        22.5
2406 Région de Montréal, QC                 22.7
4832 Calgary Zone, AB                       27.1
1204 Zone 4 - Central, NS (= Halifax)       35.1
```
These are survey estimates with sampling variability - the table ships
`Low/High 95% confidence interval, percent` as separate `Characteristics` rows, plus
`Statistically different from the Canada rate`.

**VERDICT 3a: USABLE.** Free, OGL, 99% coverage at health region for obesity / smoking /
self-rated health, current to 2023/2024.

### 3b. Physical activity: only in table 13-10-0113-01, and only at 2017/2018

This is the measure closest to "fit, active, outdoorsy", and it lives in a different, now-inactive
table.

| | |
|---|---|
| Table | **13-10-0113-01**, productId **13100113** |
| **Bulk file** | **https://www150.statcan.gc.ca/n1/tbl/csv/13100113-eng.zip** |
| HTTP / size | **200, 28,278,082 bytes = 27.0 MB zipped** (12.8 s) |
| Unzipped | `13100113.csv` = **499,363,467 bytes = 476 MB** |
| Indicators | 32, including the two the newer table dropped |
| Licence | OGL, free |

The two real indicator strings:
```
Physical activity, 150 minutes per week, adult (18 years and over)
Physical activity, average 60 minutes per day, youth (12 to 17 years old)
```

**Coverage by period** (adult 150 min/week, Percent, Both sexes, Total, health-region rows only):

| Period | HR rows | With a value | Range |
|---|---|---|---|
| 2015/2016 | 108 | **108 (100%)** | 40.1 - 72.6 |
| **2017/2018** | 108 | **108 (100%)** | **38.0 - 71.9** |
| 2019/2020 | 106 | 17 (16%) | 38.4 - 64.7 |
| 2021/2022 | 108 | 3 (3%) | 57.0 - 69.5 |

COVID destroyed 2019/2020 and 2021/2022 collection. **2017/2018 is the freshest complete
physical-activity-by-health-region data that exists in Canada.** It is 8 years old.

Real 2017/2018 values:
```
Canada                                      56.0
5932 Vancouver HSDA, BC                     71.9   <- tied highest in the country
5923 Fraser South HSDA, BC                  59.0
4832 Calgary Zone, AB                       61.5
2406 Région de Montréal, QC                 59.5
3595 City of Toronto Health Unit, ON        56.5
1204 Zone 4 - Central, NS                   58.8
lowest : Zone 4 (Edmundston area), NB       38.0
highest: East Kootenay HSDA, BC             71.9
```
**A 34-point spread, and it points the right way** - Vancouver and the BC mountain regions at the
top, northern New Brunswick at the bottom. This is the Canadian analogue of the San Diego result.

**Vintage trap:** this table's `DGUID` prefix is `2015A0007`, i.e. **HR2015/2018 boundaries, not
HR2023.** Joining it to the HR2023 crosswalk matches only 90 of 109 codes and silently drops all
of Newfoundland and Saskatchewan. **You must use the vintage-matched 2018 crosswalk** (3c).

**VERDICT 3b: USABLE WITH WORK.** The only real physical-activity signal in Canada below the
province. Costs: an 8-year-old vintage and a second, older crosswalk.

### 3c. The crosswalk - free, CSV, and it fully covers your places

**Current vintage (use with CCHS 13100972):**

| | |
|---|---|
| Product | 82-402-X, "Health regions: boundaries and correspondence with census geography", 2024001 edition |
| **URL** | **https://www150.statcan.gc.ca/n1/pub/82-402-x/2024001/corr/COMPREHENSIVE_HR2023_21.csv** |
| HTTP / size | **200, `text/csv`, 48,083,541 bytes = 45.9 MB** (10.4 s) |
| **Encoding** | **latin-1, NOT utf-8** - French names crash a naive utf-8 read |
| Rows | **498,786** at dissemination-block level |
| Real header | `DBUID2021,CSDUID2021,HRUID2023,ENGNAME,FRENAME,DBPOP2021` (note: trailing empty columns pad every row) |
| Distinct CSDUID2021 | **5,161** |
| Distinct HRUID2023 | **105** |
| CSDs spanning >1 HR | **48 (0.93%)** - and `DBPOP2021` lets you population-weight the split |
| Licence | OGL. Free. Machine-readable CSV, **not PDF-only.** |

**Older vintage (required for the physical-activity table):**
- **https://www150.statcan.gc.ca/n1/pub/82-402-x/2018001/corr/Comprehensive_HR2018_16.csv**
- HTTP 200, **50,438,910 bytes = 48.1 MB**, latin-1, quoted fields
- Header: `"DBUID2016","CSDUID2016","HRUID2018","ENGNAME","FRENAME","DBPOP2016"`
- 5,162 distinct CSDUID2016, **111** distinct HRUID2018

**Join tests I actually ran against `data/allplaces.json` (712 places, all 7-digit codes):**

```
--- HR2023 crosswalk (for CCHS obesity / smoking / self-rated health) ---
matched                            : 712  (100.00%)
missed                             :   0
app places whose CSD spans >1 HR   :   0

--- HR2018 crosswalk (for physical activity) ---
matched (2021 codes into 2016 file): 711  (99.86%)
missed                             :   1  -> L'Epiphanie, QC (2460037), amalgamated in 2021
```

Verified sample joins:
```
Surrey     5915004 -> HR 5923 Fraser South HSDA          (pop 568,322)
Vancouver  5915022 -> HR 5932 Vancouver HSDA             (pop 662,248)
Toronto    3520005 -> HR 3595 City of Toronto Health Unit(pop 2,794,356)
Montréal   2466023 -> HR 2406 Région de Montréal         (pop 1,762,949)
Calgary    4806016 -> HR 4832 Calgary Zone               (pop 1,306,784)
Halifax    1209034 -> HR 1204 Zone 4 - Central           (pop 439,819)
```

**End-to-end test, app CSD -> HR2018 -> physical activity 2017/2018:**
```
APP CANADIAN PLACES              : 712
  no CSD in crosswalk            :   1
  HR has no PA value             :  10   (PA codes 3531, 3552, 4714 absent from the crosswalk)
  USABLE physical-activity value : 701   (98.46%)
  value range across app places  : 38.0 - 71.9
most active : Fernie / Cranbrook / Kimberley / Invermere / Radium Hot Springs / Creston, BC (71.9)
least active: Edmundston / Saint-Quentin / Saint-Léonard / Grand Falls, NB (38.0)
```

**VERDICT 3c: USABLE.** Free, complete, machine-readable, population-weighted, and it covers
100% (HR2023) / 99.9% (HR2018) of your Canadian places.

### 3d. How many health regions

The answer depends on vintage and on whether BC is published at HSDA or Health Authority level.
Real counts from files fetched:

| Source | Count |
|---|---|
| `COMPREHENSIVE_HR2025_21.csv` (2026001 ed.) | **91** - BC collapsed to Health Authority |
| `COMPREHENSIVE_HR2023_21.csv` (2024001 ed.) | **105** - BC at HSDA level |
| `Comprehensive_HR2018_16.csv` (2018001 ed.) | **111** |
| CCHS 13100972, 2023/2024 slice, measured | **100 with data** |
| PA table 13100113, 2017/2018, measured | **108 with data** |

**Use the 2024001 / HR2023 edition** - the 2026001 edition throws away BC's HSDA detail, which is
exactly the detail that distinguishes Vancouver from Fraser South.

### 3e. CIHI and the federal open-data portal

**CIHI - one genuinely useful free file, one dead end.** I downloaded and parsed it myself.

- `https://www.cihi.ca/en/access-data-and-reports/open-data` -> **HTTP 404.** That page does not
  exist. "Your Health System" (yourhealthsystem.cihi.ca) redirects to a notice that it has been
  **retired** and consolidated into Indicator Library / Dashboards / Insight+.
- The live free bulk file:
  **https://www.cihi.ca/sites/default/files/document/indicator-library-all-indicator-data-en.xlsx**
  - HTTP 200, **73,663,913 bytes = 70.3 MB** XLSX. **No login, no cookie, no click-through.**
  - **822,882** data rows, **118** distinct indicators, single sheet
  - Real header: `Place or organization, Province/territory, Region, Corporation, Reporting level,
    Indicator, Measure type, Indicator segment, Segment value, Time scale, Time frame, ...`
  - `Reporting level` counts: `Province/territory` 389,716, `Facility` 201,434,
    **`Health region` 137,548**, `National` 59,218, `Corporation` 34,666, `Hospital peer group` 300
  - **141** distinct health-region names
  - Lifestyle indicators present: exactly two - `Smoking` and
    `Physical Activity (Age 18 and Older)`
  - Measured health-region coverage:
    - **`Smoking` 2023-2024: 60 rows, 60 real values (100%)** - e.g. `Labrador-Grenfell Zone (N.L.) 19.5`, `Central Zone (N.L.) 15.3`, `Western Zone (N.L.) 14.5`
    - `Smoking` 2019-2020: 62 rows, 47 real values
    - **`Physical Activity (Age 18 and Older)` 2019-2020: 62 rows, only 5 real values** - e.g. `Calgary Zone (Alta.) 64.7`, `Central Zone (Alta.) 58.9`. No other time frame exists.
  - **No geographic code column.** The join is by place NAME only (`Labrador-Grenfell Zone (N.L.)`),
    and Ontario is aggregated to ~5 Ontario Health regions rather than 34 public health units, so
    it does not line up with the StatCan health-region list without manual mapping.
- **VERDICT CIHI: USABLE WITH WORK for smoking only** (60 health regions at 2023-2024, the
  freshest sub-provincial smoking figure found anywhere, free and unwalled). **NOT USABLE for
  physical activity** - 5 regions is nothing.

**Health Canada / open.canada.ca (CKAN): NOT USABLE.** Seven `package_search` queries, all
HTTP 200, produced nothing at CSD or finer. `Leisure-time physical activity` (dataset
`02ada3d3-356c-47b6-a431-bedb84329774`, OGL, resource `13100490-eng.zip`) is **Canada, provinces
and territories only**. The only health-region physical-activity hits are NRCan Atlas of Canada
products from **1996-97**. Everything else returned Census Profile or boundary files.

**CANUE / Can-ALE / Can-BICS: NOT USABLE, and the "it's free" premise is wrong.**
`https://canue.ca/data-tools/canue-data/` (HTTP 200) states CANUE data are available to Canadian
academic researchers and trainees who must apply via a data access web form; the portal
`https://www.canuedata.ca/` (HTTP 200) offers `Data Request - Apply to download data from Canue`,
and a signed agreement is required
(`https://canue.ca/wp-content/uploads/2025/08/CANUE-Data-Use-and-Sharing-via-Third-Party-Agreement_ENG.pdf`,
HTTP 200, 360,849 bytes). It is application-gated, not an open download. It is also indexed by **postal code**, not CSD,
which would need PCCF (a paid StatCan product). **And separately: Can-ALE and Can-BICS measure
walkability and bikeability of the built environment. They are a PROXY for active living, not a
health outcome or a measured behaviour.** They would tell you a place is walkable, not that its
residents are fit. Do not substitute one for the other.

**Bonus, verified as a lead not a source:** table **13-10-0973-01** publishes the same 27 CCHS
indicators for **42 CMAs** (`https://www150.statcan.gc.ca/n1/tbl/csv/13100973-eng.zip` - verified
HTTP 200, 25,922,096 bytes = 24.7 MB zipped; contents not parsed - OGL). A
CMA maps to a city more intuitively than a health region does, but 42 CMAs covers only large
metros versus 103 health regions covering the country. For 712 places, health region wins on
coverage.

### 3f. THE REAL PROBLEM - it is resolution, not the join

The join works perfectly. What does not work is that **a health region is not a city.** Measured:

```
CANADA - effective resolution
  app places with a health region : 711
  distinct health regions hit     : 106
  places per health region        : mean 6.7, median 5, MAX 52
  biggest buckets (every place in one shares ONE identical value):
     HR 2416 (QC): 52 places
     HR 4833 (AB): 30 places
     HR 4835 (AB): 28 places
     HR 2415 (QC): 25 places
```
```
US - effective resolution (CDC PLACES, place level)
  app places with a value                     : 4,056
  distinct (LPA, OBESITY, CSMOKING) triples   : 4,052  (99.9%)
```

Read those two blocks together. **In the US, essentially every place carries its own independent
modelled estimate.** In Canada, **711 places share 106 values.** Fernie, Cranbrook, Kimberley,
Invermere, Radium Hot Springs and Creston all score exactly 71.9 because they are all in East
Kootenay - the number says nothing about any one of them.

(Caution on a misleading comparison: US physical inactivity alone shows only 332 distinct printed
values across 4,056 places, but those ties are **1-decimal rounding artifacts** on independent
estimates. The Canadian ties are **structural** - identical by construction. Do not compare the
single-measure distinct counts directly; that is why the triple is shown above.)

Consequences you should decide on deliberately:
- A user comparing two towns in the same health region gets **identical numbers**, which reads as
  broken rather than as coarse.
- The measure will look most "informative" in provinces with many small health regions and least
  in Quebec and Alberta, which is an artifact of administrative geography, not of health.
- Ranking 712 Canadian places on 106 values means ~85% of any ranking position is arbitrary
  tie-breaking.

### VERDICT 3 (Canada): **USABLE WITH WORK - with a resolution caveat you should decide on before building.**

Refuting your assumption cleanly: **health region IS the floor (confirmed), but a free CSD ->
health-region crosswalk exists and covers 100% of your places, so the dimension does NOT have to
be US-only.** What is true is that the Canadian number is ~6.7x coarser than the US one and
8 years old for the physical-activity measure specifically.

Three honest options:

**A. US-only.** Cleanest. The US measure is place-level and current; the Canadian one is regional
and partly stale. Mixing them into one cross-border ranking compares things that are not alike.

**B. Ship Canada, but as a regional attribute, not a place score.** Use CCHS 13100972 (2023/2024)
for obesity / smoking / self-rated health at 99% coverage, and label it in the UI as
"health region: Fraser South" rather than presenting it as a fact about Surrey. Add physical
activity from 13100113 only if you are willing to print "2017/2018".

**C. Ship Canada on obesity + smoking + self-rated health only, drop physical activity.** Avoids
the 8-year-old number and the second crosswalk. Costs you the measure that best matches
"fit, active, outdoorsy".

My read: **B or C.** The join is solid enough that A is leaving real information on the table -
but only if the UI is honest that the value describes a region.

---

## 4. If PLACES had been tract-only - the aggregation question

**This is moot.** PLACES ships a real Place release (section 1), so no tract aggregation is
needed. Answering anyway because you asked.

### 4a. What it would take

Population-weight the tracts into the place:

```
place_value = SUM( tract_value * tract_pop_in_place ) / SUM( tract_pop_in_place )
```

Tracts do not nest inside places - a tract can straddle a city boundary, and a big city contains
many whole tracts plus partial ones. So you need an **allocation factor**: the share of each
tract's population that falls inside the place. That is exactly what a population-weighted
crosswalk provides.

Caveats that would apply: the result is an average of model outputs, so confidence intervals do
not carry through cleanly (you would have to treat the aggregate CI as unknown rather than
computing one); and a place made of one partial tract would inherit that whole tract's value.

**CDC explicitly endorses this aggregation** and publishes the recipe. Verbatim from
https://www.cdc.gov/places/faqs/index.html:

> "**Can I aggregate the data to estimate the prevalence for a group of areas (such as a group of
> counties or census tracts)? Yes.** ... For each area (e.g., county, census tract), estimate the
> number of adults reporting a specific measure (N) by multiplying the relevant census population
> counts or estimates (Pop) from Step 1 by the specific prevalence estimate (p) and dividing by
> 100 (N = Pop x p / 100). Sum the estimated number of adults calculated in Step 3 across all the
> included areas to generate the aggregate estimate for a specific measure. Divide this by the
> sum of the total population count/estimate to obtain the aggregate prevalence estimate."

Note CDC's step 1 caveat: use the **relevant** population, not total population. Most measures
are adults 18+ (`TotalPop18plus`), but some are restricted (e.g. women 21-65 for mammography).
For LPA and OBESITY, `TotalPop18plus` is the correct weight.

### 4b. Is a free population-weighted tract->place crosswalk available? YES - two of them.

**Option A - MCDC Geocorr 2022 (the direct one).** Free, no login, and **scriptable** - I ran a
real request end to end.

- Form: https://mcdc.missouri.edu/applications/geocorr2022.html (HTTP 200, 26,525 bytes)
- Endpoint: `https://mcdc.missouri.edu/cgi-bin/broker` (GET)
- Required params, as verified working:
  ```
  _PROGRAM=apps.geocorr2022.sas   _SERVICE=MCDC_long   _debug=0
  state=Vt50            <- postal-abbrev + FIPS, e.g. Ca06, Ks20. NOT bare "50".
  g1_=tract  g2_=place  wtvar=pop20  nozerob=1
  fileout=1  filefmt=csv  lstfmt=html
  latitude=  longitude=  distance=  kiloms=0    <- must be PRESENT (even empty) or SAS errors out
  oropt=0  afacts2=1  sort2=0  xycentr=0
  ```
- Real run (Vermont): HTTP 200, "17976 census blocks selected", **389 observations**, output at
  `https://mcdc.missouri.edu/temp/geocorr2022_<jobid>.csv` - downloaded, HTTP 200,
  **32,374 bytes**, 391 lines (2 header rows + 389 data rows).
- Real header and row:
  ```
  "county","tract","state","place","stab","CountyName","PlaceName","pop20","afact"
  "50001","9603.00","50","74650","VT","Addison VT","Vergennes city, VT",2553,1
  ```
  `afact` is the tract-to-place allocation factor. `pop20` is 2020 Census population.
  `[not in a place]` appears as place code `99999`.
- Two traps I hit: `state=50` fails with a SAS error, it must be `Vt50`; and omitting
  `latitude`/`longitude` fails with "Apparent symbolic reference LONGITUDE not resolved" even
  though they are irrelevant to a tract->place run.

**Option B - Census 2020 Block Assignment Files (build it yourself).** Free, public domain.
- Directory: `https://www2.census.gov/geo/docs/maps-data/data/baf2020/` (HTTP 200)
- Per state: `BlockAssign_ST50_VT.zip` - downloaded, HTTP 200, **467,182 bytes**
- Contains 8 members; the relevant one is **`BlockAssign_ST50_VT_INCPLACE_CDP.txt`**
  (449,043 bytes), real header + rows:
  ```
  BLOCKID|PLACEFP
  500019601001000|
  500019601001003|
  ```
- `BLOCKID` is the 15-digit block GEOID, so **tract = `BLOCKID[0:11]`** and the place GEOID is
  state FIPS + `PLACEFP`. Blocks not in any place have an empty `PLACEFP`.
- **The BAF carries no population**, so on its own it gives you an unweighted crosswalk. To
  population-weight it you must join block population from the 2020 Census PL 94-171 / DHC
  release. Geocorr has already done exactly this, which is why Option A is less work.

**Not the right file:** `https://www2.census.gov/geo/docs/maps-data/data/rel2020/` - I listed
this directory and its `place/` and `tract/` subdirectories. They contain only
**same-geography-across-vintages** files (`tab20_place20_place10_natl.txt`,
`tab20_tract20_tract10_natl.txt`), i.e. 2020-to-2010 comparisons. There is **no** tract-to-place
relationship file there. My first two guessed URLs
(`tab20_place20_tract20_natl.txt`, `tab20_tract20_place20_natl.txt`) both returned **HTTP 404**.

### VERDICT 4: **USABLE WITH WORK, but moot.** A free, population-weighted tract->place crosswalk
exists and I generated one (Geocorr 2022, `afact` column, scriptable GET). You do not need it,
because PLACES publishes places directly.

---

## Recommended build

1. Pull the **filtered CSV** from `eav7-hnsx` (11.2 MB, 13.7 s) for `LPA, OBESITY, CSMOKING,
   GHLTH` at `datavaluetypeid='AgeAdjPrv'`.
2. Pull the same filter from **`sd8v-uq83`** (2024 release) and use it **only** for PA and KY.
   Record `year` per place so the vintage is honest.
3. Join on 7-digit GEOID. Expect ~99% coverage; Puerto Rico has no data and never will from this
   source.
4. **Rank on ONE named measure, not a blended health score.** CDC's FAQ says outright that the
   data "should not be used for ranking the overall health" of a place, but that places "can be
   compared on individual measures" (section 1f). **Physical inactivity (`LPA`) is the single
   best fit** for "fit, active, outdoorsy vs sedentary" and it is the measure that separated
   San Diego from Kansas City most cleanly. Show OBESITY, CSMOKING and GHLTH as supporting facts
   beside it rather than folding them into one number.
5. Keep **BINGE out** of anything composite regardless - it runs backwards (San Diego scores
   worst of the three test cities).
6. Label it "CDC PLACES modelled estimate, 2025 release (BRFSS 2023)" in the UI, never
   "measured" or "surveyed". Cite: "Centers for Disease Control and Prevention. PLACES: Local
   Data for Better Health. Accessed [date]. https://www.cdc.gov/places". Consider banding places
   whose confidence intervals overlap instead of showing a hard rank - CDC warns the intervals
   for small places are very broad.
7. Skip County Health Rankings unless the app is non-commercial or you get written consent. Use
   `swc5-untb` (public domain) if you want a county-level layer.

**Canada, if you ship it (option B/C from section 3f):**

8. `COMPREHENSIVE_HR2023_21.csv` (45.9 MB, **latin-1**) -> `CSDUID2021` to `HRUID2023`, weighting
   by `DBPOP2021` for the 48 split CSDs nationally (none of yours split, so a simple lookup works).
9. Table **13100972** at `2023/2024`, `Characteristics='Percent'`, `Sex='Both sexes'` -> obesity,
   smoking, perceived health, perceived mental health. Drop `STATUS` in `..`/`F`/`x`; keep `E`
   but flag it. Skip fruit/veg entirely (3% coverage).
10. Physical activity only if you accept a 2017/2018 label: table **13100113** joined via
    **`Comprehensive_HR2018_16.csv`**, not the 2023 crosswalk.
11. **Label every Canadian value with its health region in the UI.** Six BC mountain towns
    scoring an identical 71.9 is correct data and looks like a bug unless you say why.

---

## Could not confirm

Listed explicitly so nothing here reads as verified when it is not.

1. **Size of the full long-format place CSV (`eav7-hnsx`, 2,150,438 rows).** Not downloaded. A
   HEAD on the export URL returns `Content-Length: 0` (Socrata streams it), so no size could be
   read without pulling the whole file. **I am not stating a size for it.** The wide file
   (43.0 MB) and the filtered pull (11.2 MB) were both measured directly.
2. **App place count.** Your brief says 4,197 US places; `data/us/places.json` contains
   **4,226**. All join percentages above are against the 4,226 in the file. I did not track down
   what filters the shipped app applies, so the final in-app coverage may differ slightly.
3. **Underlying sources for CHR `v132` (Access to Exercise Opportunities) and `v133` (Food
   Environment Index).** I read their dictionary descriptions but did **not** fetch their source
   documentation, so I cannot say what feeds them or whether those inputs are separately
   licensable.
4. **USDA substitutes for the food-environment angle.** I confirmed only that two landing pages
   respond: `https://www.ers.usda.gov/data-products/food-environment-atlas` (HTTP 200, 36,232
   bytes) and `https://www.ers.usda.gov/data-products/food-access-research-atlas` (HTTP 200,
   41,509 bytes). I did **not** download either dataset, check its geography, its join key, its
   vintage, or its licence. Treat these as leads, not as verified sources.
5. **CHR `analytic_supplement_20260325[1].csv` (the 2026-03-25 supplement).** Seen as a link on
   the documentation page. **Not downloaded, not inspected.** Unknown what it adds.
6. **Geocorr at national scale.** I ran one state (Vermont) successfully. I did **not** test a
   50-state run, so I cannot speak to runtime, output size, or rate limiting.
7. **Whether `PlaceName` carrying the FIPS code in `vgc8-iyc4` is a known CDC bug.** Observed
   directly in both the API and the CSV, but I found no CDC erratum confirming it (cdc.gov 403s).

**Canada:**

8. **StatCan table 13-10-0931-01** (premature and potentially avoidable mortality by 2023-boundary
   health regions, released 2025-11-28). Identified from the StatCan cube list. **Not downloaded,
   header/GEO values/suppression not read.** It is a health *outcome*, not a lifestyle behaviour,
   but it would share the HR2023 crosswalk. Treat as a lead.
9. **CIHI Insight+** (`/en/secure/insight-indicators`) - the path contains `secure` and the page
   renders a login control. **No authentication attempted**, so what geography it exposes and
   whether it holds the physical-activity data the free XLSX omits is unknown.
10. **CIHI Dashboards** (`https://www.cihi.ca/en/access-data-and-reports/dashboards`, HTTP 200,
    80,822 bytes) - link structure read, but **no individual dashboard's underlying data was
    loaded**, so granularity and export options are unconfirmed.
11. **CANUE's actual Can-ALE / Can-BICS files** - variables, dissemination-area granularity,
    vintage and size are **unverified**; the access wall stopped inspection and no data request
    was submitted. Note the premise that Can-ALE "is free" is **contradicted** by canue.ca and
    canuedata.ca, but the data itself was never seen.
12. **Provincial health ministries** (Ontario PHU tabs, BC LGA/HSDA custom tabulations, Alberta
    Health Zone tabs) - **not swept.** If any province publishes physical activity below health
    region, this research would not have found it. Only a BC LGA hospitalization dataset surfaced
    incidentally via CKAN, and it was not downloaded.
13. **StatCan PCCF** (postal code -> CSD/DA) cost and licence - **not fetched.** Relevant only if
    the CANUE path were ever pursued.
14. **`COMPREHENSIVE_HR2025_21.csv` (91 HRs) and the BC HSDA recovery file `BCHSDA_HR2025_21.csv`.**
    The counts quoted in 3d come from the parallel sweep; I independently verified the **HR2023**
    (45.9 MB) and **HR2018** (48.1 MB) crosswalks byte-for-byte and joined both myself, but I did
    **not** personally download the 2025-edition files. The recommendation to use the 2024001 /
    HR2023 edition does not depend on them.
