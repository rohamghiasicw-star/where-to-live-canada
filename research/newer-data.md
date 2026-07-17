# Newer-data sourcing research

Research date: 2026-07-17. Every URL below was tested live with `curl`. Nothing here is assumed; findings that are inferred vs. proven are labelled.

---

## PART 1 - Environment Canada Climate Normals 1991-2020

### Bottom line
**YES.** The 1991-2020 Canadian Climate Normals exist in machine-readable, per-station CSV form. They are NOT in the GeoMet API and NOT in a single bulk zip - they are served **one station at a time** from the legacy `climate.weather.gc.ca/climate_normals/` bulk endpoint. All the elements the app needs are present **except bright sunshine hours** (dropped in the 1991-2020 edition).

### What is NOT available (tested, negative)

- **GeoMet `climate-normals` collection is 1981-2010 only.** Confirmed:
  - `https://api.weather.gc.ca/collections/climate-normals/items?f=json&PERIOD_BEGIN=1991&limit=1` -> `numberMatched: 0`
  - `...&PERIOD_BEGIN=1981...` -> `numberMatched: 592926` (= the entire collection). Every record is `PERIOD_BEGIN=1981, PERIOD_END=2010`.
  - There is a `PERIOD_BEGIN`/`PERIOD_END` queryable but 1991 returns nothing.
- **No separate 1991-2020 GeoMet collection.** Full `collections?f=json` list checked - nothing normals-related beyond `climate-normals`. (Related: `ahccd-*` = adjusted homogenized trends, `ltce-*` = daily record extremes, `climate:candcsu6:*` / `climate:cmip5:*` / `climate:dcs:*` = **gridded model/scenario** products, not per-station normals.)
- **`https://dd.weather.gc.ca/climate/` -> HTTP 404.** No climate directory at the datamart root. (The datamart carries realtime + daily obs, not a normals bundle.)
- **Whole-province bulk download does NOT work.** `bulk_data_e.html?...&yr=1991&prov=BC` with no `stnID` returns only the 182-byte CSV header, zero data rows. You must request each station individually.
- **No single "all normals" file** on the CMC bulk server. `https://collaboration.cmc.ec.gc.ca/cmc/climate/Normals/` contains only the four *calculation-information PDFs* (1961-90, 1971-2000, 1981-2010, 1991-2020), no CSVs.
- **open.canada.ca** has no downloadable 1991-2020 normals resource. The "Canadian Climate Normals" entry in the "Climate Data Products" package (id `51dbf91e-509c-437b-ab9e-eca6d0bf6fa8`) is just an HTML link to `climate_normals/index_e.html` (format = HTML, no data file).

### What IS available (tested, positive) - the working method

The legacy site publishes a dedicated 1991-2020 normals product. There is a separate selector page (`station_select_1991_2020_e.html`), a separate results page (`results_1991_2020_e.html`), and the same `bulk_data_e.html` download endpoint - but keyed by a **new, large `stnID`** that is different from the 1981-2010 station IDs.

**The one gotcha:** the endpoint gates non-JS clients. The first request sets a `jsenabled=0` cookie and 302-redirects to a 404. Send the cookie `jsenabled=1` and the CSV body is returned **in the body of the 302 response itself** (Content-Type `text/csv`). With curl: `-b "jsenabled=1"` and read the body directly (do NOT follow the redirect - `-L` lands on the 404 template).

**Direct per-station download URL (proven working):**
```
https://climate.weather.gc.ca/climate_normals/bulk_data_e.html?ffmt=csv&lang=e&prov=<PROV>&yr=1991&stnID=<BIGID>&climate_id=<CLIMATEID>
```
Send `Cookie: jsenabled=1`. `yr=1991` is what selects the 1991-2020 edition (the server literally names the file `en_1991-2020_Normals_<PROV>_.csv`). `yr=1981` gives the old 1981-2010 file for the same site.

Verified pulls:
- AGASSIZ, BC - `stnID=312000000&climate_id=1100119` -> 31 KB, 173 rows, full element set.
- TORONTO (CITY), ON - `stnID=207000000&climate_id=6158355` -> 27 KB, 152 rows.

### CSV format (identical to the 1981-2010 bulk format)
Header row:
```
"LOCATION_NAME","PROVINCE_OR_TERRITORY","PERIOD_OF_RECORD","ELEMENT_GROUP","NORMALS_ELEMENT","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Year","Code"
```
One row per element, 12 monthly columns + annual + a data-quality `Code` (A-F). `PERIOD_OF_RECORD` = `Normal` (the 1991-2020 value) or `Long-Term` (all-time extreme). UTF-8 BOM, degree symbols in element names.

### Elements present (verified) vs. what the app needs
The app's `normals_by_station.json` currently carries tmean / tmax / tmin / snow (+ presumably precip). All are present in 1991-2020:

| App field | 1991-2020 `NORMALS_ELEMENT` (ELEMENT_GROUP = Temperature/Precipitation) |
|---|---|
| tmean | `Daily Average (°C)` |
| tmax | `Daily Maximum (°C)` |
| tmin | `Daily Minimum (°C)` |
| snow (total snowfall) | `Snowfall (cm)` |
| total precipitation | `Precipitation (mm)` |
| (rain only) | `Rainfall (mm)` |

Also included: snow depth, degree-days, days-with-X-temp/precip/snow counts, wind, humidity, pressure, humidex, wind chill, frost-free probabilities. Far richer than the current app fields.

**Bright sunshine: NOT available.** Neither AGASSIZ nor TORONTO (CITY) has any `Sunshine`/`Bright`/`Solar`/`Radiation` element in the 1991-2020 file. ECCC largely discontinued sunshine measurement, and it was dropped from the 1991-2020 normals. If the app uses bright-sunshine hours, that single field must stay on 1981-2010 (or be sourced elsewhere, e.g. reanalysis). Everything else upgrades cleanly.

### Station coverage - roughly 450 stations nationally
The 1991-2020 edition is a curated "principal station" set, much smaller than 1981-2010. Per-province station counts (distinct `climate_id` from `station_select_1991_2020_e.html?searchType=stnProv&lstProvince=<P>&selRowPerPage=100`):

```
AB 41   BC 57   MB 25   NB 21   NL 32   NS 24   NT 24
NU 30   ON 70   PE  8   QC 70   SK 27   YT 21     => ~450 total
```
Caveat: ON and QC both report exactly 70 and the `startRow` pager did not advance, so those two may be display-capped - treat ~450 as a floor. (`selRowPerPage` only accepts small values; `=1000` returns empty.) Compare to the current 1981-2010 set the app uses, which is thousands of stations - so switching to 1991-2020 means **fewer stations, i.e. some towns will match to a more distant station.** This is the real tradeoff, not data availability.

### Station-enumeration recipe (to build the station list + get each `stnID`)
The big `stnID` is not derivable and not in the public Station Inventory CSV (that file uses the old small IDs). Two ways to get it:

1. **Per province (to (re)build the whole 1991-2020 station set):**
   - `GET station_select_1991_2020_e.html?searchType=stnProv&lstProvince=<PROV>&selRowPerPage=100&startRow=1` -> parse the `results_1991_2020_e.html?...&climate_id=<CID>` links (gives every station's `climate_id` + name + lat/lon).
   - For each `climate_id`: `GET results_1991_2020_e.html?...&climate_id=<CID>&dispBack=0` -> parse the hidden form `<form action="bulk_data_e.html" id="dl-data">`; its inputs give `stnID`, `climate_id`, `prov`, `stnname`.
   - Then hit the `bulk_data_e.html` URL above. (~2 requests + 1 download per station, ~450 stations = trivial one-time crawl. Always send `-b "jsenabled=1"`.)

2. **Reuse the app's existing stations (less work, keeps current town->station matching):**
   The app already matches towns to stations by GeoMet `STN_ID`. GeoMet `climate-normals` exposes both `STN_ID` and `CLIMATE_IDENTIFIER` per station. Map each existing station's `CLIMATE_IDENTIFIER` -> run step-1b's `results_1991_2020_e.html?climate_id=<CLIMATE_IDENTIFIER>` to get the 1991-2020 `stnID` (empty form / header-only CSV = that station has no 1991-2020 normal, fall back to 1981-2010 or nearest 1991-2020 station).

### Fallback (only if you want a normal that matches your *exact* current station set, or need sunshine)
Not required for 1991-2020 station normals (they exist), but documented since the app already uses these collections for gap-filling: compute your own recent normal from **GeoMet `climate-monthly`** (per-station monthly summaries). Verified coverage is current: latest `LOCAL_DATE` = **2026-06**, sorted `-LOCAL_DATE`. `climate-daily` also current (2026-07). So a self-computed 1991-2020 (or trailing 15-yr) mean per station is fully feasible from `climate-monthly` for temperature/precip/snow, and this is the ONLY route to a recent value for stations that lack an official 1991-2020 normal. Sunshine is not in these collections either.

### Recommendation - Part 1
Integrate the official 1991-2020 normals via the per-station `bulk_data_e.html?...&yr=1991` endpoint (method above). Upgrade tmean/tmax/tmin/snow/precip. Keep bright sunshine on 1981-2010 (it doesn't exist in 1991-2020). Accept the sparser (~450) station network, or use the 1981-2010 station only as a positional fallback when the nearest 1991-2020 station is too far. This is a real, ~1-degree-warmer, defensible upgrade to the climate layer.

---

## PART 2 - Newer population than the 2021 Census

### Bottom line
- **2026 Census population counts: NOT available yet.** First release (population and dwelling counts) is **February 10, 2027.**
- **Annual population ESTIMATES at the census-subdivision (town) level ARE newer and available now: July 1, 2025**, table **17-10-0155**, downloadable CSV, 5,201 geographies, only 6 suppressed. Worth integrating.

### 2026 Census timing (tested)
From StatCan's census program index (`www12.statcan.gc.ca/census-recensement/index-eng.cfm`), "Upcoming 2026 Census releases":
- **November 18, 2026** - 2026 Census geographic and reference products
- **February 10, 2027** - **Population and dwelling counts** (this is the first town-level population release)
- **May 5, 2027** - Age, gender, and sex at birth; type of dwellings

So as of mid-2026 there is **zero** downloadable 2026 population data at any geography. (`.../census-recensement/2026/...` paths currently 404 to the WET error template.) The census was taken May 2026; counts land Feb 2027, matching the 2021 cadence (2021 counts released Feb 9, 2022).

### StatCan annual population estimates (tested - StatCan WDS REST API)
Found the full family of sub-provincial estimate cubes. The current (2021-boundary) ones all run to **July 1, 2025** (`cubeEndDate 2025-01-01`, released 2026-01-14):

| Product | Geography | Latest ref | Status |
|---|---|---|---|
| **17-10-0155** | **Census subdivision (CSD = town/city)** | **2025** | active (2021 boundaries) |
| 17-10-0152 | Census division | 2025 | active |
| 17-10-0148 | CMA / census agglomeration | 2025 | active |
| 17-10-0150 | Economic region | 2025 | active |
| 17-10-0142 | Census subdivision (2016 boundaries) | 2022 | **inactive** (superseded by 155) |

**17-10-0155 is the one** - it reaches town granularity, exactly what the app keys on.
- Metadata (`POST getCubeMetadata` body `[{"productId":17100155}]`): title "Population estimates, July 1, by census subdivision, 2021 boundaries"; Geography dimension has **5,201 members** (Canada + provinces/territories + all CSDs); start 2001, end 2025; released 2026-01-14.
- Full CSV: `GET https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/17100155/en` returns `{"object":"https://www150.statcan.gc.ca/n1/tbl/csv/17100155-eng.zip"}`. Downloaded (2.8 MB zip -> 16.7 MB `17100155.csv` + metadata). REF_DATE runs `2001 ... 2023, 2024, 2025`.
- Data quality: for 2025, of 5,201 rows only **6** are blank/suppressed (`STATUS = ".."`); the other 5,195 have clean values, no quality flags. Near-complete town coverage.

### Join key (clean, direct)
`census.json` in the app keys CSDs by a 7-digit `code` (e.g. Carbonear = `1001370`). 17-10-0155 carries a `DGUID` whose trailing 7 digits are the same standard CSD code:
- Surrey (CY), BC - DGUID `2021A00055915004` -> code `5915004`, **2025 pop 703,531** (vs 2021 Census 568,322).
- Vancouver (CY), BC - DGUID `2021A00055915022` -> `5915022`, 2025 pop 740,454.
- Halifax (RGM), NS - DGUID `2021A00051209034` -> `1209034`, 2025 pop 516,822.

Strip `2021A0005` (the CSD DGUID vintage/type prefix) from DGUID -> 7-digit code -> direct join to the app's existing `code`. Filter `REF_DATE=2025` for the newest value.

### Caveats
- These are **modelled July-1 estimates** (Population Estimates Program), not a census enumeration - built on the 2021 Census base rolled forward with births/deaths/migration. Good for "current size," slightly less authoritative than a census count, and CSD-level estimates carry more uncertainty than provincial ones. But they are official StatCan and the best available town-level population until Feb 2027.
- 2021 boundaries, so a handful of post-2021 CSD amalgamations may differ from the app's current CSD list; join on code and spot-check unmatched rows.

### Recommendation - Part 2
Yes - integrate 17-10-0155 (July 1 2025) as the population field, joined by CSD code via DGUID. It's 4 years newer than the 2021 Census and captures large real shifts (Surrey +24%). Keep the 2021 Census as the source for everything else it provides (density, income, dwellings, commute, etc. - the estimates table has population only). Revisit in Feb 2027 when actual 2026 Census counts publish.

---

## Exact URLs used (all tested this session)
- GeoMet collections: `https://api.weather.gc.ca/collections?f=json`
- GeoMet normals period check: `https://api.weather.gc.ca/collections/climate-normals/items?f=json&PERIOD_BEGIN=1991&limit=1`
- GeoMet monthly recency: `https://api.weather.gc.ca/collections/climate-monthly/items?f=json&limit=3&sortby=-LOCAL_DATE`
- 1991-2020 station download (per station): `https://climate.weather.gc.ca/climate_normals/bulk_data_e.html?ffmt=csv&lang=e&prov=BC&yr=1991&stnID=312000000&climate_id=1100119` (Cookie: jsenabled=1)
- 1991-2020 province station list: `https://climate.weather.gc.ca/climate_normals/station_select_1991_2020_e.html?searchType=stnProv&lstProvince=BC&selRowPerPage=100&startRow=1`
- 1991-2020 results/stnID page: `https://climate.weather.gc.ca/climate_normals/results_1991_2020_e.html?searchType=stnName&txtStationName=toronto&searchMethod=contains&climate_id=6158355&dispBack=0`
- Calc-info PDF: `https://collaboration.cmc.ec.gc.ca/cmc/climate/Normals/Canadian_Climate_Normals_1991_2020_Calculation_Information.pdf`
- StatCan cube metadata: `POST https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata` body `[{"productId":17100155}]`
- StatCan full CSV: `https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/17100155/en` -> `https://www150.statcan.gc.ca/n1/tbl/csv/17100155-eng.zip`
- 2026 Census schedule: `https://www12.statcan.gc.ca/census-recensement/index-eng.cfm`
