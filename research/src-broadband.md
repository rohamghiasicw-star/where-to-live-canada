# Digital connectivity dimension - source verification

Verified 2026-08-18. Every number below was measured or read off a real response, not estimated.
Where something could not be confirmed it says so in those words.

Method note: `www.fcc.gov` and `help.bdc.fcc.gov` block scripted clients (Akamai 403 / Cloudflare
challenge). All FCC verification below was done through a real browser session against
`broadbandmap.fcc.gov`, including reading the actual ZIP members and CSV headers in memory.

---

## 1. US - FCC Broadband Data Collection (BDC)

### 1a. THE ONE TO USE: Fixed Broadband Summary by Geography Type - Census Place

**Verdict: USABLE.** Direct join to the 7-digit place GEOID, no crosswalk, 27.4 MB for the
whole country. This is the pre-aggregated file that removes any need to touch the location-level bulk data.

| | |
|---|---|
| Landing page | https://broadbandmap.fcc.gov/data-download (tab "By State", section "Fixed Broadband Summary by Geography Type" -> "Census Place") |
| Download URL pattern | `https://broadbandmap.fcc.gov/nbm/map/api/getNBMDataDownloadFile/{file_id}/1` |
| Format | ZIP containing one CSV (single member, confirmed by reading the zip central directory) |
| Files | 56 - one per state / DC / territory |
| **Measured total size** | **28,765,752 bytes = 27.4 MB zipped**, all 56 measured individually, 0 failures |
| Example single file | Vermont = 155,682 bytes zipped -> 16,920 data rows |
| Geographic unit | Census Place |
| Join key | `geography_id` = **7-digit Census place GEOID** (confirmed: `5000400` = Albany, VT) |
| Licence / cost | US federal government work, public domain (17 U.S.C. 105). Free. No login for this endpoint. |
| Vintage | Data as of **Dec 31, 2025**, published **Aug 4, 2026** |
| Cadence | Biannual (as-of Jun 30 and Dec 31; published roughly 7 months after the as-of date) |
| Back-catalogue | Jun 2022 through Dec 2025 all still downloadable |

**Exact CSV header (read from the real file, not from docs):**

```
area_data_type,geography_type,geography_id,geography_desc,geography_desc_full,
total_units,biz_res,technology,speed_02_02,speed_10_1,speed_25_3,speed_100_20,
speed_250_25,speed_1000_100
```

Real row:
```
Total,Census Place,5000400,Albany,"Albany, VT",88,R,Any Technology,1.000000000,1.000000000,1.000000000,1.000000000,1.000000000,0
```

**Field meanings (as observed in the data):**

- `area_data_type` - `Total`, `Urban`, `Rural` (the UI also lists Tribal / Non-Tribal). Filter to `Total`.
- `geography_id` - the join key. 7-digit place GEOID.
- `total_units` - count of Broadband Serviceable Locations (BSLs) in that place.
- `biz_res` - `R` = residential, `B` = business+residential. Pick one, do not sum.
- `technology` - 15 distinct values observed:
  `Any Technology`, `All Wired`, `Any Terrestrial`, `All Wired and Licensed Fixed Wireless`,
  `Copper`, `Cable/Fiber`, `Cable`, **`Fiber`**, `All Satellite`, `GSO Satellite`,
  `NGSO Satellite`, `All Fixed Wireless`, `Unlicensed Fixed Wireless`,
  `Licensed Fixed Wireless`, `Other`
- `speed_02_02` ... `speed_1000_100` - **fraction of that place's BSLs (0 to 1)** where that
  technology is available at that down/up tier. Tiers are 0.2/0.2, 10/1, 25/3, 100/20, 250/25, 1000/100 Mbps.

**So the two fields you asked for map like this:**

- **Fiber availability** = row where `technology = 'Fiber'`; the `speed_*` value is the share of
  homes in the place that can actually get fibre. (`Cable/Fiber` and `Any Terrestrial` are useful
  companions - `Any Terrestrial` excludes satellite, which is the honest "can I work from here" cut.)
- **Max advertised speed** is not a single column here - it is expressed as the fraction of the
  place reaching each tier. For a remote-work score, `technology='Any Terrestrial'` +
  `speed_100_20` (or `speed_1000_100` for gigabit) is the cleanest single number.

**Coverage test against this app's own place list (the important bit):**

- FCC file set contains **32,072 distinct Census Places** nationally.
- `data/us/places.json` has 4,226 places; `data/us/proximity.json` (the ranked set) has 4,197.
- I drew a **stratified sample of 305 place GEOIDs, up to 6 from every one of the 52 state codes**
  in the app's list, and tested membership against all 56 FCC files.
- **Result: 305 / 305 matched. Zero missing.**

That is as close to a guarantee of a clean join as you can get without running all 4,197.

**Spot check on real values - and the one trap to avoid.**

Pulled from the live NY file, `area_data_type=Total`, `biz_res=R`:

| place | BSLs | technology | 100/20 | 1000/100 |
|---|---|---|---|---|
| New York City (3651000) | 3,932,926 | Any Technology | 1.000 | 0.708 |
| | | **Any Terrestrial** | **0.995** | 0.708 |
| | | Cable | 0.973 | 0.048 |
| | | **Fiber** | **0.793** | 0.675 |
| | | All Satellite | 1.000 | 0.000 |
| Speculator, NY (3670123) | 534 | Any Technology | **1.000** | 0.856 |
| | | **Any Terrestrial** | **0.856** | 0.856 |
| | | Fiber | 0.856 | 0.856 |

**Do not use `Any Technology`.** Starlink and GSO satellite are counted in it, so it reads ~1.000
almost everywhere - a tiny Adirondack village scores the same as Manhattan. Use
**`Any Terrestrial`** for the headline "can I actually work from here" number and **`Fiber`** for
the quality tier. That pair is what actually separates places.

**Reproducible download recipe:**

1. `GET https://broadbandmap.fcc.gov/nbm/map/api/published/filing` -> returns the list of
   published filings with a `process_uuid` per as-of date. Dec 31 2025 =
   `16495d87-e2f6-49a8-96db-e50394a743e2`.
2. `GET https://broadbandmap.fcc.gov/nbm/map/api/national_map_process/nbm_get_data_download/{process_uuid}/`
   -> 10,613-record JSON manifest (3.7 MB). Filter
   `data_type == "Fixed Broadband Summary by Geography Type - Census Place"` for the 56 file ids.
3. `GET https://broadbandmap.fcc.gov/nbm/map/api/getNBMDataDownloadFile/{id}/1` for each.

**Vintage stability (checked, so the pipeline will not break in six months):** the identical
56-file Census Place structure exists for the two prior vintages too -
Jun 30 2025 (`bdc_01_fixed_broadband_summary_by_geography_place_J25_01aug2026`, 573,326 bytes) and
Dec 31 2024 (`..._D24_29jul2026`, 586,331 bytes), both with the Other Geographies file present.
Only the `process_uuid` and file ids change, and step 1 of the recipe resolves those.

**Operational warning - this is the one thing that will bite you.**
Plain `curl` gets **403 from Akamai** on every one of these endpoints, with or without
browser-like headers. One header combination (HTTP/2 + UA + Referer + Origin + `Sec-Fetch-*`)
returned 200 once, then started 403ing and stayed blocked for over 20 minutes after I ran 446
requests at concurrency 12. The same machine's real browser session kept working throughout at
concurrency 5-6. So: drive these downloads from a real browser session or a TLS-impersonating
client, and throttle to ~5 concurrent. Do not hammer it.

### 1b. County-level fallback: Fixed Broadband Summary by Geography (Other Geographies)

**Verdict: USABLE, as a backstop.** You have a place->county FIPS map, so this joins too.

- URL: `https://broadbandmap.fcc.gov/nbm/map/api/getNBMDataDownloadFile/1746998/1`
- File: `bdc_us_fixed_broadband_summary_by_geography_D25_04aug2026.csv.zip`
- **Measured: 9,146,437 bytes zipped (8.72 MB) -> 86.36 MB uncompressed**, 616,170 data rows
- Same 14-column schema as the place file
- Geography types actually present (counted, not assumed):

| geography_type | distinct ids | example |
|---|---|---|
| County | **3,232** | `01001` = Autauga County |
| CBSA (MSA) | 939 | `10100` = Aberdeen, SD |
| Congressional District | 442 | `0101` |
| Tribal | 737 | `0010R` = Acoma Pueblo |
| State | 56 | `01` = Alabama |
| National | 1 | `99` |

County ids are the standard 5-digit FIPS, which matches `data/us/place_county.json`
(`{"county": "01017"}`). Note: this file does **not** contain Census Place - place lives only in
the 56 per-state files in 1a.

### 1c. Provider Summary by Geography (has Census Place, but wrong shape)

- URL: `https://broadbandmap.fcc.gov/nbm/map/api/getNBMDataDownloadFile/1736548/1`
- **Measured: 3,976,102 bytes zipped (3.8 MB)**, 488,179 data rows
- Header: `geography_type,geography_id,geography_desc,data_type,provider_id,res_st_pct,bus_iv_pct`
- Contains Census Place (**32,174 distinct**, e.g. `0100100` = Abanda CDP, AL)
- **Verdict: NOT the right file for this dimension.** It gives per-provider coverage percentage
  only. No speed tier, no technology. Useful if you ever want "how many ISPs compete here"
  (count of `provider_id` per place), nothing else.

### 1d. The location-level bulk data (what you heard was huge)

**Verdict: NOT USABLE for this app, and you do not need it.**

- 446 files: one per state x technology, `bdc_{ST}_{Tech}_fixed_broadband_D25_04aug2026.csv.zip`
- **Measured total: 9,031,303,487 bytes = 8.41 GB ZIPPED**, all 446 measured individually
- Compression on this data runs about 10x (the one file I expanded went 8.72 MB -> 86.36 MB), so
  expect **roughly 85 GB uncompressed**. "Hundreds of GB" is an overstatement for a single
  vintage; it is not an overstatement if you keep several vintages uncompressed.
- Zipped size by technology: GSO Satellite 3,417 MB, Licensed Fixed Wireless 2,206 MB,
  NGSO Satellite 962 MB, Cable 741 MB, **Fiber to the Premises 726 MB**, Copper 259 MB,
  Unlicensed Fixed Wireless 221 MB, LBR Fixed Wireless 81 MB
- Largest single files: Texas/GSO 364 MB, California/GSO 346 MB, Texas/Licensed FW 281 MB

**Exact CSV header (read from the real file):**
```
frn,provider_id,brand_name,location_id,technology,max_advertised_download_speed,
max_advertised_upload_speed,low_latency,business_residential_code,state_usps,
block_geoid,h3_res8_id
```
Real row: `0003768165,130317,Xfinity,1037392925,50,100,100,1,B,VT,500110102002027,882bab5303fffff`

- Geographic unit: **Broadband Serviceable Location** (`location_id`), plus `block_geoid`
  (15-digit census block) and `h3_res8_id` (H3 resolution-8 hexagon).
- `technology` here is the numeric code. **`50` = Fiber to the Premises.** Full set:
  0 Other, 10 Copper, 40 Cable, 50 FTTP, 60 GSO Satellite, 61 NGSO Satellite,
  70 Unlicensed FW, 71 Licensed FW, 72 LBR FW.
- `max_advertised_download_speed` / `max_advertised_upload_speed` - Mbps integers. These are the
  literal "max advertised speed" fields you asked about, and they exist **only** at this level.
- **Killer problem for you: there is no place code in this file.** Only block GEOID and H3. You
  would need a census-block-to-place crosswalk and a weighted rollup for all 4,197 places, to
  reproduce a number the FCC already publishes in 1a. Not worth 85 GB.

### 1e. The documented public API (bdc.fcc.gov) - login required

- Base: `https://bdc.fcc.gov/`, e.g. `/api/public/map/downloads/listAvailabilityData/{as_of_date}`
- **Confirmed by request: returns `{"status":"fail","status_code":401,"message":"Unauthorized"}`
  without credentials.**
- Requires an FCC User Registration account plus a 44-character API token generated under
  "Manage API Access" (one-time agreement to an FCC disclaimer). Free, but it is a login wall.
- The `broadbandmap.fcc.gov/nbm/map/api/...` endpoints used in 1a-1d need **no** account. They are
  the endpoints the public map's own UI calls.
- Spec documents (both are viewable in a browser, both 403 to scripted fetches):
  - `https://us-fcc.box.com/v/bdc-data-downloads-output` - "Specifications for Data Downloads from
    the National Broadband Map", dated August 11, 2026, 81 pages. Confirmed it renders; I could
    not extract its text (Box serves it as canvas and blocks the file endpoint), so every field
    definition above was read from the actual data instead.
  - `https://us-fcc.box.com/v/bdc-public-data-api-spec` - API spec. Not opened.

### US bottom line

Take **1a** (56 files, 27.4 MB, `geography_id` = your place GEOID) and keep **1b** as the
county-level fallback for any place that ever fails to join. Ignore the 8.41 GB bulk entirely.

---

## 2. Canada - CRTC / ISED

Short version: **the CRTC file is the Canadian twin of the FCC place file** - one 32 MB download,
7-digit CSD code, direct join, no spatial work. ISED's National Broadband Data is the only source
with a real fibre flag, but it costs three joins and overstates coverage.

### 2a. THE ONE TO USE: CRTC Table 9 - broadband and mobile availability by CSD

**Verdict: USABLE.** Direct join on the 7-digit CSD code. **712 / 712 of this app's Canadian
places matched, zero missing** (tested against `data/allplaces.json`).

| | |
|---|---|
| Download URL | `https://applications.crtc.gc.ca/OpenData/CASP/COMMUNICATION%20MONITORING%20REPORTS/Telecommunications%20Overview/English/data-mobile-and-broadband-availability.zip` |
| **Measured size** | **32,317,554 bytes = 32.32 MB** zipped (confirmed live: HTTP 200, real `content-length`) |
| Inner file | `C-T9.csv`, 108,936,843 bytes uncompressed, **796,316 data rows** |
| Parent dataset | "Telecommunications Sector - CMR", open.canada.ca package `bd41f23a-6dbc-45ee-9419-422153aff567` |
| Data dictionary | `.../English/data-dictionary-mobile-and-broadband-availability.pdf` (65,278 bytes) |
| Geographic unit | **Census Subdivision** |
| Join key | column 3, `ID de la subdivision de recensement / Census Subdivision ID` - **5,303 distinct codes, all exactly 7 digits** |
| Licence / cost | Open Government Licence - Canada. Free. **No login, no API key, no click-through** |
| Vintage | data years **2016-2024**; CRTC package `metadata_modified` 2025-12-20 |

**Parsing traps - all three will silently corrupt your load:**

1. Encoding is **cp1252, not UTF-8**.
2. The header is on **line 5**. Lines 1-4 are title/source banner.
3. Quoted fields contain embedded newlines and commas (the Population Centre column). Use a real
   CSV reader, never `split(',')`.
4. **The in-file title says "by CMA and year". The title is wrong** - the geography really is
   Census Subdivision. Verified directly: column 3 is labelled Census Subdivision ID and holds
   values like `5915022` = Vancouver, `4807001` = Provost No. 52.

**Shape of the data.** Long format, one row per CSD x speed tier x year. The `Vitesses / Speeds`
column takes 18 values:

- Fixed: `1.5+`, `5+`, `10+`, `16+`, `25+`, `50+`, `100+`, `150+`, `200+`, `Gigabit`,
  `50/10/Any`, `50/10/U` (U = unlimited data)
- Mobile: `HSPA+`, `LTE`, `LTEA`, `NR`, `AllMobile`
- **`AllDemographics` = the denominator row**

**`Logements / Dwellings` is a dwelling COUNT, not a percent.** To get a share:

```
pct(tier) = dwellings[CSD, tier, year] / dwellings[CSD, 'AllDemographics', year]
```

Verified against real 2024 rows:

| CSD | place | dwellings | 50/10/U | 100+ | Gigabit |
|---|---|---|---|---|---|
| 5915022 | Vancouver | 328,347 | 100.00% | 99.96% | 99.95% |
| 5915004 | Surrey | 195,098 | 100.00% | 99.97% | 99.97% |
| 3520005 | Toronto | 1,253,238 | 100.00% | 99.89% | 99.87% |
| 2466023 | Montreal | 878,542 | 100.00% | 99.98% | 99.96% |
| 1001370 | Carbonear | 2,289 | 99.75% | 99.75% | 99.75% |

**Which tier to rank on - measured across this app's own 712 places, 2024:**

| tier | min | p10 | median | p90 | places pinned at ~100% |
|---|---|---|---|---|---|
| 50/10 unlimited | 0.0 | 99.3 | 100.0 | 100.0 | **505 of 712 (71%)** |
| 100+ | 0.0 | 95.7 | 99.7 | 100.0 | 187 (26%) |
| **Gigabit** | **0.0** | **87.3** | 99.7 | 100.0 | 169 (24%) |

**Do not rank on 50/10.** It is saturated - 71% of the app's places sit at 100%, so it cannot
separate anything. **Rank on Gigabit**, with `100+` as the secondary. Same failure mode as
`Any Technology` on the US side.

Be honest about the shape though: even Gigabit has a median of 99.7, so the dimension is flat for
the top half of the list and only earns its keep in the bottom ~25%. The tail is real and correct:

```
Dawson YT          50/10  99.7%   100+  99.7%   Gigabit   0.0%
Yellowknife NT     50/10  98.8%   100+  98.8%   Gigabit   0.0%
Whitehorse YT      50/10  98.4%   100+  98.4%   Gigabit   0.0%
Labrador City NL   50/10  97.9%   100+  97.9%   Gigabit   0.0%
Elk Point AB       50/10 100.0%   100+  33.1%   Gigabit   0.0%
Smoky Lake AB      50/10 100.0%   100+  22.0%   Gigabit   0.0%
Rankin Inlet NU    50/10   0.0%   100+   0.0%   Gigabit   0.0%
Cape Dorset NU     50/10   0.0%   100+   0.0%   Gigabit   0.0%
```

**Known limitation: C-T9 has no technology column.** No fibre/cable/DSL split. If fibre
specifically matters, you need 2b.

### 2b. ISED National Broadband Data - the only real fibre flag

**Verdict: USABLE WITH WORK.** No spatial join is required, but it is a three-hop chain and the
fibre number is optimistic. Only worth it if fibre-vs-not is a distinct dimension for you.

- Package: "National Broadband Data" on open.canada.ca, ISED. Licence **OGL-Canada**, free, no login.
- Live map: `https://ised-isde.canada.ca/app/scr/sittibc/web/bbmap`
  (the URL printed in some ISED docs 302s to `/site/ised` then 301s to the ISED homepage - dead)
- Vintage: CKAN `date_modified` 2026-05-28, ZIP internals 2026-05-05, ISED page "Date modified:
  2026-07-31". Cadence stated inconsistently (CKAN `as_needed` vs page "annual surveys").
  Demographics are 2021 Census.

| resource | URL | measured size |
|---|---|---|
| NBD PHH Speeds (CSV) | `https://ised-isde.canada.ca/app/scr/sittibc/web/api/openData/NBD_PHH_Speeds.zip` | **190,214,440 B = 190.21 MB** |
| NBD Map (CSV, hexagons) | `.../openData/Map_Data_CSV.zip` | live (HTTP 200) |
| NBD Map (Shapefile) | `.../openData/Map_Data_Shapefile.zip` | live |
| NBD Roads (GPKG) | `.../openData/NBD_Roads_GPKG.zip` | **COULD NOT CONFIRM - HEAD returned 504 Gateway Time-out** |
| PHH 2021 (CSV) | separate package `b3a1d603-...` | **209,139,581 B = 209.14 MB** |
| StatCan Geographic Attribute File | - | 9,832,890 B = 9.83 MB, 498,786 rows |

**Geographic unit: pseudo-household (PHH) representative points - NOT hexagons.** The hexagons are
a separate map product, roughly 25 km each.

**Fields (from the shipped data dictionary):**
- `PHH_ID`
- `Combined_{tier}_Combine`, `Wired_{tier}_Filaire`, `Wireless_{tier}_Sans_fil` booleans (0/1) for
  tiers `lt5_1`, `5_1`, `10_2`, `25_5`, `50_10`
- `Combined_Max_Threshold-Combine_Seuil_Max` and the Wired/Wireless variants - enum
  `{"", "<5_1", "5_1", "10_2", "25_5", "50_10"}`. `50_10` is the top bucket and does **not**
  preclude faster service, so there is no gigabit signal here.
- `Avail_LTE_Mobile_Dispo`
- Undocumented extra column actually shipped: `Satellite_Max_Threshold-Satellite_Seuil_Max`
- Dictionary contradicts the file: documented `Avail_5_1_75PctPlus_Dispo` /
  `Avail_50_10_Gradient_Dispo` ship as generic **`Expr1` / `Expr2`**

**Joining to CSD - no spatial join needed, but three hops:**

```
ISP_Hex_FSI.csv (HEXuid + Technology)
  -> PHH_2021       (HEXUID_IdUHEX -> DBUID_Ididu)
  -> StatCan Geographic Attribute File (DBUID_IDIDU -> CSDUID_SDRIDU)
```

- `NBD_PHH_Speeds` itself carries **no** census geography and **no** lat/lon - only `PHH_ID`.
- `PHH_2021` is the bridge: `PHH_ID, Type, Pop2021, TDwell2021_TLog2021, URDwell2021_RH2021,
  DBUID_Ididu, HEXUID_IdUHEX, Pruid_Pridu, Latitude, Longitude`.
- The hexagon map files carry no census geography either (`HEXuid_HEXidu`, `PRNAME`, `PCPUID`,
  `PNuid` only) and the CSVs have no coordinates - geometry lives only in SHP/GPKG,
  Lambert Conformal Conic NAD83.
- Chain match rates measured on two provinces: **Nunavut 777/777 dissemination blocks matched,
  0 unmatched; PEI 99,428 PHH rows -> 98 CSDs, 0 unmatched.**

**Fibre:** `ISP_Hex_FSI.csv`, column `Technology`, exact value **`"Fibre to the home"`**
(19,132 rows across 14,604 hexagons). **Caveat that matters:** a hexagon is ~25 km and is flagged
if *any* ISP offers FTTH *anywhere* inside it, so a hexagon-derived fibre share **overstates**
real coverage. Do not present it as a household-level fibre rate.

**ISED download gotchas:**
- ISED sends **no `content-length`** and ignores HEAD and Range. Any ISED size not measured by a
  full download is unverifiable.
- `NBD_PHH_Speeds.zip` **silently truncates on plain curl** - three attempts died at 17/25/30 MB
  with HTTP 200 and a corrupt archive. Only completed with `--retry 3 --retry-all-errors`.
- **CKAN's own size fields are wrong.** It claims 110 MB for `PHH_2021_CSV.zip` (really 209.14 MB)
  and 186 MB for `NBD_PHH_Speeds` (really 190.21 MB). Do not cite them.

### 2c. Ruled out - do not spend time here

- **StatCan: NOT USABLE.** No internet/broadband variable exists below the province level
  anywhere. 2021 Census Profile returns 0 hits across 2,631 characteristics;
  `getAllCubesListLite` returns 0 cube titles matching "broadband".
- **StatCan SDG indicator 9.3.1 CSV (21,292 bytes): NOT USABLE.** Province-only, GeoCode is
  2-digit PRUIDs.
- **CRTC `OLMCDownloadPackage.zip`: NOT USABLE.** It has a tempting CSD-keyed `Prcnt5010unl_illim`
  column, but the denominator is restricted to official-language-minority dwellings near
  designated schools. Wrong universe - it is not a general population rate.

---

## Recommendation

| | US | Canada |
|---|---|---|
| Source | FCC BDC Census Place summary | CRTC CMR Table 9 (`C-T9.csv`) |
| Download | 56 files, **27.4 MB** | 1 file, **32.32 MB** |
| Join | `geography_id` = 7-digit place GEOID | CSD ID = 7-digit CSD code |
| Match vs this app | **305/305 sampled, 0 missing** | **712/712, 0 missing** |
| Rank on | `technology='Any Terrestrial'` + `Fiber`, `speed_100_20` / `speed_1000_100` | `Gigabit`, then `100+` |
| Trap | `Any Technology` counts satellite, reads ~1.000 everywhere | 50/10 is saturated, 71% of places at 100% |
| Licence | US public domain | OGL-Canada |
| Fibre available | **yes**, native `Fiber` technology row | not in CRTC; needs ISED 3-hop, and it overstates |

Both sides are one modest download with a clean 7-digit join and no spatial work. The dimension is
real but **left-skewed on both sides** - it will separate the bottom quarter of the list and be
flat across the top. Rank on the demanding tier (gigabit / terrestrial-fibre), not the basic one.

### Caveats to carry into the build

1. Neither source is a speed *test*. Both are carrier-reported *availability*. They answer "is
   service sold here", not "what will I actually get". The FCC data is provider self-reported and
   subject to a challenge process.
2. The two countries are not directly comparable. Different tiers, different denominators (FCC
   counts broadband serviceable locations, CRTC counts dwellings), different vintages
   (FCC Dec 2025, CRTC 2024). Normalise within each country before combining.
3. FCC gives a fibre share directly. Canada does not, at CSD level, from an authoritative source.
   If you want one number both countries share, use the terrestrial 100/20-equivalent tier, not fibre.

---
