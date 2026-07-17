# Wildfire smoke data for Livable

Research date: 2026-07-16. Every endpoint below was tested with curl. Every number was computed from real downloaded data, not quoted from memory.

---

## PART 1: NORMAL_ID=87 "Days with smoke or haze". Verdict: DROP IT.

Your hypothesis was right. It is worse than unusable. It is **negatively correlated** with real wildfire smoke, so shipping it would actively invert the map.

### What it actually measures

The element counts days on which a human observer logged **either** of two separate present weather obstructions to vision. They are two different phenomena, merged under one label.

**Smoke.** ECCC's own climate glossary entry is literally titled "Smoke or Haze", which is the tell that the two are collapsed into one element. Verbatim:

> "A suspension in the air of small particles produced by combustion. Viewed through smoke, the sun appears very red at sunrise and sunset. When high in the sky, smoke is tinged with orange. Smoke from nearby cities may be brown, dark gray or black. Smoke in extensive layers originating from forest fires give the sky a greenish-yellow hue. Evenly distributed smoke from distant sources is generally light gray or blue. In large quantities, smoke may be distinguished by its smell. Plumes of smoke of local origin are not reported as an atmospheric phenomenon."

Source: https://climate.weather.gc.ca/glossary_e.html

Note "smoke from nearby cities may be brown, dark gray or black". Combustion, yes, but explicitly including **urban and industrial** combustion. Forest fire is one clause among many.

**Haze.** A completely separate lithometeor, with no combustion in the definition at all. WMO International Cloud Atlas, verbatim:

> "A suspension in the air of extremely small, dry particles invisible to the naked eye and sufficiently numerous to give the air an opalescent appearance."

Source: https://cloudatlas.wmo.int/en/haze.html

Dry particles. Sulfate, industrial pollution, dust, sea salt. In southern Ontario that is overwhelmingly summer humidity haze plus the historical Windsor/Detroit and Ohio Valley industrial plume, which is exactly what you guessed.

**Reporting trigger.** MANOBS: haze, dust haze and smoke are reported when prevailing visibility drops to 6 statute miles (about 9.7 km) or less. So the element is a **visibility** counter, not a concentration or health measure. A hazy 8 mile day counts zero. A humid Toronto July afternoon at 5 miles counts one, same as a wildfire day.

- MANOBS landing page: https://www.canada.ca/en/environment-climate-change/services/weather-manuals-documentation/manobs-surface-observations.html (returns 403 to scripted fetches, browser only)
- MANOBS 7th ed. Amdt 19 PDF: https://www.canada.ca/content/dam/eccc/migration/main/manobs/73bc3152-e142-4aee-ac7d-cf30daff9f70/manobs_7e-a19_eng_web.pdf (canada.ca refused every scripted download attempt, HTTP/2 INTERNAL_ERROR then timeout. Definitions above are sourced from the ECCC glossary and WMO instead, which are equally authoritative and did serve.)

The ECCC Climate Normals technical documentation page (https://www.canada.ca/en/environment-climate-change/services/climate-change/canadian-centre-climate-services/display-download/technical-documentation-climate-normals.html) also 403s to scripted fetches. The ropensci `weathercan` glossary mirrors the element list and confirms `smoke_or_haze` carries **no published definition** in the normals docs at all, which is its own red flag: https://docs.ropensci.org/weathercan/articles/glossary_normals.html

### The killshot: I correlated it against real wildfire smoke

I extracted ECCC's own FireWork wildfire-attributed PM2.5 (see Part 2) for all 129 of your towns, then correlated it against the element 87 value already sitting in `data/climate.json`. 128 towns had both.

```
Pearson r  (element 87 vs real wildfire PM2.5) = -0.221
Spearman rank r                                = -0.313
```

**Negative.** Not weak. Backwards. Look at the two rankings side by side:

| Top by element 87 | days/yr | real wildfire PM2.5 |
|---|---|---|
| Nelson BC | 99.0 | 2.39 |
| Windsor ON | 92.6 | 0.38 |
| London ON | 92.3 | 0.36 |
| Goderich ON | 92.3 | 0.37 |
| Stratford ON | 92.3 | 0.37 |
| Guelph ON | 73.1 | 0.39 |

| Top by real wildfire PM2.5 | µg/m³ | element 87 days/yr |
|---|---|---|
| Kamloops BC | 2.82 | **3.5** |
| Penticton BC | 2.53 | **2.8** |
| Kelowna BC | 2.40 | **4.0** |
| Nelson BC | 2.39 | 99.0 |
| Vernon BC | 2.24 | **4.0** |
| Cranbrook BC | 2.20 | **0.7** |
| Yellowknife NT | 2.07 | **6.4** |

Kamloops is the smokiest town in your entire list and element 87 gives it **3.5 days a year**. Windsor is near the cleanest for wildfire smoke and element 87 gives it **92.6 days**, 26x more. Ship element 87 and your app tells a Kelowna family they are moving somewhere with clean air and tells a Windsor family they live in the smokiest place in Canada. Both backwards.

(Nelson BC at 99.0 is the one town scoring high on both, and it is a coincidence of mechanism, not signal: a deep valley that traps everything, wood stove smoke and inversion haze included.)

### Three more reasons it is structurally broken

1. **Human observers only.** Automated stations (AWOS/AWS) cannot distinguish smoke from haze and largely stopped reporting these codes. The 1981-2010 normal is a record of *which stations still had a paid human squinting at the horizon*, which correlates with airport size, not fire.
2. **It is 1981-2010.** The window closes 15 years ago. The Canadian wildfire smoke regime changed materially after roughly 2015. Even a perfect smoke element on that window would describe a climate that no longer exists. Note the API's `climate-normals` collection is 1981-2010 only; the 1991-2020 normals exist elsewhere but do not fix the fundamental problem.
3. **Visibility threshold, not dose.** No relationship to PM2.5 concentration or health risk.

**Verdict: cut element 87 from `pull_climate.py`.** Straight answer, as asked: it is not a wildfire smoke indicator, it never was, and it is anti-correlated with the thing you want. There is no salvage, no rescaling, no "use it for BC only" version. Drop it.

---

## PART 2: The options, tested

### RECOMMENDED: ECCC FireWork "Cumulative Effects" wildfire PM2.5 (RAQDPS-FW.CE)

**This is the one. It is purpose-built for exactly your question and almost nobody knows it exists.**

- **What it measures:** the **wildfire-attributable increment** of surface PM2.5. ECCC runs its air quality model twice, once with fires and once without, and differences them. So it is not total PM2.5 contaminated by traffic and wood stoves. It is *the smoke, isolated*. Layer title, verbatim from GetCapabilities: `"Yearly average of wildfire contribution: surface PM2.5 [ug/m³]"`.
- **Spatial coverage:** national 10 km grid (729 x 599 native). **Reaches every town.** All 129 of your places resolved, including Iqaluit, Dawson City, Churchill and Tofino. Zero off-grid.
- **Temporal coverage:** **2013 to 2024**, 12 complete years. Yearly and monthly means both available.
- **Machine-downloadable:** yes, WCS GetCoverage, no auth, no key. **~1.75 MB per year, ~21 MB for the entire archive.**

```bash
curl "https://geo.weather.gc.ca/geomet?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage\
&COVERAGEID=RAQDPS-FW.CE_PM2.5-DIFF-YAvg&FORMAT=image/tiff\
&TIME=2023-01-01T00:00:00Z&SUBSETTINGCRS=EPSG:4326&OUTPUTCRS=EPSG:4326\
&SUBSET=x(-141,-52)&SUBSET=y(41,84)" -o fw_2023.tif
# HTTP 200, 604318 bytes, float32 GeoTIFF 411x367, EPSG:4326
```

Ask for `SUBSETTINGCRS/OUTPUTCRS=EPSG:4326` and GeoMet reprojects off the native rotated pole for you, so **you do not need GDAL or rasterio**. Pillow reads the tags:

- origin (tag 33922): `-141.0, 80.210751236`
- pixel scale (tag 33550): `0.2165450121654501, 0.10684128402179834`
- sample with `col=int((lon-ox)/sx)`, `row=int((oy-lat)/sy)`, mean a 3x3 window to soften cell edges

Layers: `RAQDPS-FW.CE_PM2.5-DIFF-YAvg` (yearly), `RAQDPS-FW.CE_PM2.5-DIFF-MAvg` (monthly, 2013-01 to 2024-12), plus `-DMax` daily-maximum variants if you want a peak-severity score alongside the average.

**It passes the smell test hard.** 12-year mean, computed from the real files:

| smokiest | µg/m³ | | cleanest | µg/m³ |
|---|---|---|---|---|
| Kamloops BC | 2.82 | | Charlottetown PE | 0.11 |
| Penticton BC | 2.53 | | Antigonish NS | 0.10 |
| Kelowna BC | 2.40 | | Sydney NS | 0.08 |
| Nelson BC | 2.39 | | Bonavista NL | 0.07 |
| Vernon BC | 2.24 | | St. John's NL | 0.05 |
| Yellowknife NT | 2.07 | | Iqaluit NU | 0.04 |

BC Interior on top, Atlantic and Arctic at the bottom. Yellowknife's 2023 value is **11.8**, the year the whole city was evacuated for fire. Lytton peaks in 2017, BC's record year. The data knows what happened.

**Limits, honestly:**
1. **It is model output, not measurement.** A physics/chemistry simulation differenced against a counterfactual no-fire run, not a sensor reading. Defensible and it is ECCC's own operational product, but say "modelled" if you ever describe the method publicly.
2. **Averages only, no daily series.** You get annual and monthly means plus daily-max. You cannot reconstruct "how many days over 35 µg/m³". For a normal that is fine, arguably better since it is pre-aggregated. If you want a *smoke days count* specifically, this cannot give it to you.
3. **2013-2024, stops at 2024.** No 2025 yet, and it cannot be extended from operational output (that retains 30 days). 12 years is a short normal by WMO standards (30), but it covers the modern fire regime, which is the point.
4. **10 km cells.** One value per town, no intra-city detail. Irrelevant at your scale.
5. **Do not use WMS GetFeatureInfo to read values.** It silently censors below ~1 µg/m³ and returns `200 {}` with no feature, so clean towns look like errors. WCS returns true floats down to 0.0. This bit us mid-research.

### On the 2023 over-indexing you flagged: you were right to worry, and here is the size of it

National mean across your 129 towns, by year:

```
2013 0.23   2017 1.24   2021 1.39
2014 0.37   2018 0.66   2022 0.29
2015 0.50   2019 0.26   2023 1.79  <-- 
2016 0.06   2020 0.53   2024 0.48
```

2023 is roughly **3x a typical year and 30x 2016**. Concretely:

- Score on **2023 alone** and towns move by up to **82 rank places** (Nanaimo 38th to 120th, Victoria 44th to 119th). That would be a garbage map.
- Score on the **full 12-year mean** vs excluding 2023 and the max move is **48 places**, and the towns that move are the Ottawa valley cluster (Almonte, Perth, Kingston, Brockville, Picton). They rank higher *with* 2023 because 2023 was their one big smoke year in twelve.

**Use the full 12-year mean (2013-2024).** It lets 2023 count once out of twelve, which is honest: eastern Ontario really did eat serious smoke that year and pretending otherwise is its own distortion. Do not drop 2023, and do not let it drive. If you want to be extra defensible, also store the 12-year **median** or a "worst year" field and let the UI show both.

### Runner-up: NAPS PM2.5 (strong, but not smoke-specific)

You guessed this was the strongest option. It is genuinely good, and it is the right answer to a slightly different question.

- **What it measures:** measured hourly ground-level PM2.5, µg/m³. **All** PM2.5. Traffic, wood stoves, industry, dust and wildfire, undifferentiated. Isolating the wildfire share is a research project (that is literally what CanOSSEM and FireWork-CE exist to do).
- **Coverage:** 764 stations all-time, **278 active, 235 of those measure continuous PM2.5**, across 185 distinct cities. By urbanization: 89 large urban, 36 medium, 52 small urban, **57 non-urban/rural**. Better rural reach than I expected.
- **Against your actual 129 towns** (nearest active PM2.5 station, computed):

```
<=  10 km :  68 / 129  (53%)      median 5.8 km
<=  25 km :  76 / 129  (59%)      max    646 km
<=  50 km :  96 / 129  (74%)
<= 100 km : 120 / 129  (93%)
<= 200 km : 127 / 129  (98%)
```
Worst: Churchill MB 646 km, Dawson City YT 434 km, Kenora ON 189 km, Timmins ON 176 km.

- **Temporal:** hourly PM2.5 **1998 to 2024**, 27 complete years. 2025 is not posted yet (integrated data only).
- **Machine-downloadable:** yes, but **the documented `/data/` URL is a trap**. `https://data-donnees.az.ec.gc.ca/data/air/monitor/...` is a JavaScript SPA and returns **HTTP 200 with 2200 bytes of HTML** instead of your file. Silent corruption. The real API:

```bash
# list a directory
curl "https://data-donnees.az.ec.gc.ca/api/path_contents?path=/air/monitor/national-air-pollution-surveillance-naps-program/Data-Donnees/2023"

# download a file (note: api/file, URL-encoded path, leading slash)
curl "https://data-donnees.az.ec.gc.ca/api/file?path=%2Fair%2Fmonitor%2Fnational-air-pollution-surveillance-naps-program%2FData-Donnees%2F2023%2FContinuousData-DonneesContinu%2FHourlyData-DonneesHoraires%2FPM25_2023.csv" -o PM25_2023.csv
# HTTP 200, 14,824,404 bytes

# station master list (764 rows, has lat/lon/urbanization/PM2.5 flags)
curl "https://data-donnees.az.ec.gc.ca/api/file?path=%2Fair%2Fmonitor%2Fnational-air-pollution-surveillance-naps-program%2FProgramInformation-InformationProgramme%2FStationsNAPS-StationsSNPA.csv" -o naps_stations.csv
# HTTP 200, 203,728 bytes
```

I downloaded 2014-2024 (11 files, ~125 MB) to confirm it holds up. It does. Format: 8 header lines then CSV, one row per station-day, columns `Pollutant, Method Code, NAPS ID, City, Province, Latitude, Longitude, Date, H01..H24`. **Lat/lon are embedded in every row**, so you never need to join to the station list. `-999` = no data, zeros are valid. Presence flags in the station CSV are `X`, not `1`.

**Gotcha that will bite you:** city names are not clean. Vancouver is `Metro Vancouver - Vancouver`. There are 13 `Metro Vancouver - *` entries. **Match on lat/lon, never on city name.**

**It does detect wildfire smoke clearly.** Daily means I computed from `PM25_2023.csv`:

| city | median µg/m³ | days >35 | top days |
|---|---|---|---|
| Ottawa | 5.6 | 8 | **2023-06-07 = 189**, 06-25 = 168, 06-06 = 140 |
| Edmonton | 8.9 | 45 | **2023-05-20 = 316**, 05-21 = 262 |
| Toronto | 7.2 | 5 | 2023-06-28 = 79, 06-30 = 77 |
| Halifax | 4.6 | **0** | 2023-12-18 = 21 |

Ottawa's peak lands exactly on the June 2023 Quebec smoke event, Edmonton's on the May 2023 Alberta fires. The signal is unmistakable.

**Use NAPS if** you later want a *smoke days count* ("14 days above 35 µg/m³") rather than an annual average, since FireWork-CE cannot produce a day count. You would need to define smoke days as an anomaly above each station's own seasonal background to avoid crediting Hamilton's industry as wildfire. That is real work, and it caps you at 53% of towns within 10 km.

### Rejected: ECCC AQHI historical. There is no archive.

Dead end, and the metadata **lies about it**. `aqhi-observations-realtime` advertises:

```json
"temporal": { "interval": [["2013-01-01T00:00:00+00:00", null]] }
```

That is fiction. Tested:

```
datetime=2015-07-01/2015-07-02  -> numberMatched = 0
datetime=2023-06-01/2023-06-30  -> numberMatched = 0     (the record smoke month!)
sortby=observation_datetime     -> earliest record = 2026-07-14
total rows in collection        -> 8,229
```

Actual retention is about **2 to 3 days**. 134 stations. The 2013 start date is nominal and unbacked by a single row. If you had trusted the metadata you would have built a normal on an empty set. There is no multi-year AQHI archive on GeoMet or the MSC Datamart.

### Rejected: CanOSSEM. Right idea, not obtainable.

Scientifically it is the ideal product: random forest, daily 24h mean PM2.5, **5 km x 5 km, all inhabited Canada, 2010-2022**, optimized specifically for wildfire smoke, RMSE < 3 µg/m³.

**But the data is not published.** Both repos (https://github.com/BCCDC-PHSA/CanOSSEM and https://github.com/namanpaul/CanOSSEM) contain **model code only**, R scripts, no estimates, no DOI, no download link, no data availability statement. Access routes to a named contact (naman.paul@bccdc.ca) or a formal BCCDC data access request (https://www.bccdc.ca/about/accountability/data-access-requests). Not a pipeline you can build an app on. Paper: https://www.sciencedirect.com/science/article/pii/S0048969722050550

Worth an email if Livable gets serious, since 5 km beats 10 km. Not a launch dependency.

### Rejected for primary, useful as a secondary: CWFIS / NBAC burned area

Fire activity, not smoke exposure. Smoke travels 1000+ km, which is the entire reason your founding text message happened in the first place: "fires spreading smoke from up north". Proximity to burn is a poor proxy for what you actually breathe. Ottawa in June 2023 hit 189 µg/m³ with no fire anywhere near it.

Real URLs (the `/datamart/` UI is an SPA and returns **false 200s full of HTML** for any download path, same trap as NAPS):

```
https://cwfis.cfs.nrcan.gc.ca/downloads/                       <- real Apache index
https://cwfis.cfs.nrcan.gc.ca/downloads/nbac/
  NBAC_1972to2025_20260513_shp.zip        1.17 GB   1972-2025, all years
  NBAC_MRB_1972to2025_250m.tif.zip        9.6 MB    <- cheapest, most recent burn raster
  NBAC_2023_20260513.zip                  181.5 MB
https://cwfis.cfs.nrcan.gc.ca/downloads/hotspots/archive/1994-2011_hotspots.zip   79.8 MB
https://cwfis.cfs.nrcan.gc.ca/downloads/nfdb/fire_poly/current_version/NFDB_poly.zip  742 MB
```

NBAC covers **1972-2025 complete, no gaps**, zipped shapefile. If you ever want a "fire on the doorstep" field distinct from "smoke in the air", `NBAC_MRB_1972to2025_250m.tif.zip` at 9.6 MB is the cheap way. Secondary at most.

Note: operational FireWork has been **merged into RAQDPS**. The documented path `https://dd.weather.gc.ca/model_raqdps-fw/10km/grib2/` is **404 dead**. Current smoke forecast ships as `..._MSC_RAQDPS_PM2.5-WildfireSmokePlume_Sfc_...grib2` on a 30-day rolling window. Forecast only, no use for normals. The `RAQDPS-FW.CE` archive is a separate, quieter product and is the one you want.

---

## Recommendation

**Use `RAQDPS-FW.CE_PM2.5-DIFF-YAvg` via GeoMet WCS, 12-year mean over 2013-2024.**

Because it is the only option that is all four of: **wildfire-specific** (already differenced against a no-fire run, so no confounding with traffic or wood stoves), **complete for every town** (129/129, 10 km national grid, no nearest-station gap), **long enough for a normal** (12 years spanning the modern fire regime), and **trivially machine-downloadable** (21 MB total, no auth, no GDAL).

Concrete access, verified working today:

```
GET https://geo.weather.gc.ca/geomet?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage
    &COVERAGEID=RAQDPS-FW.CE_PM2.5-DIFF-YAvg
    &FORMAT=image/tiff
    &TIME={YYYY}-01-01T00:00:00Z          for YYYY in 2013..2024
    &SUBSETTINGCRS=EPSG:4326&OUTPUTCRS=EPSG:4326
    &SUBSET=x(-141,-52)&SUBSET=y(41,84)
```
Read tags 33922 (origin) and 33550 (pixel scale) with Pillow, sample a 3x3 window at each town's lat/lon, average the 12 years. A working extractor is at `/tmp/fwx.py` and the extracted result for all 129 towns is at `/tmp/fw_towns.json`.

**The honest limits, in one place:** it is **modelled, not measured**. It is **annual/monthly averages, not a daily series**, so it cannot give you a "smoke days per year" count. It **stops at 2024**. **12 years is short** for a climate normal (WMO wants 30), though the older data would misrepresent today's fire regime anyway. And **2023 is a 3x outlier** that must be diluted across the full window, never scored alone.

If you later want the headline number to be a day count rather than an average, that is a NAPS job: hourly 1998-2024 via `api/file`, define a smoke day as an anomaly over each station's own seasonal background, and accept that only 53% of your towns sit within 10 km of a monitor. Different question, different tradeoff, more work.

**And delete element 87 from `pull_climate.py` today.** It is pointing the wrong way.
