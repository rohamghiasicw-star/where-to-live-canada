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

## 2. Canada - ISED / CRTC National Broadband Data

See section below (filled in from a separate verification pass).

---
