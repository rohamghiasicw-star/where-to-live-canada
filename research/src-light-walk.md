# Source verification: nighttime lights + walkability (US + CA)

Verified 2026-08-18. Every URL below was actually requested. Where I could not confirm
something I say so explicitly rather than filling the gap.

**Bottom line**

| # | Source | Verdict |
|---|--------|---------|
| 1 | VIIRS annual nighttime lights, EOG direct | **NOT USABLE** as an automated source. Login wall + paid tier for programmatic access since 2026-06-01. |
| 1b | Same data, Zenodo mirror (CC-BY-4.0) | **USABLE** - verified end to end, sampled in Python, no login. |
| 2 | EPA National Walkability Index | **USABLE WITH WORK** - live, free, public domain. Published CSV has a broken join key; use the REST service or reconstruct. |
| 3 | Can-ALE 2.0 (2021) | **USABLE WITH WORK** - live, clean, 100% CSD coverage. **No licence attached** - that is the blocker, not the data. |
| 3b | StatCan Proximity Measures Database | **USABLE** - official, Open Government Licence, CSDUID already in the file. |

---

## 1. VIIRS nighttime lights annual composite

### 1a. Earth Observation Group direct - NOT USABLE

**Everything under the data tree is login-walled.** Tested:

```
https://eogdata.mines.edu/nighttime_light/annual/v22/
https://eogdata.mines.edu/nighttime_light/annual/v22/2022/
```

Both return `HTTP 302` to
`https://eogauth.mines.edu/realms/eog/protocol/openid-connect/auth?...` (Keycloak).
Because the redirect fires for every path, a 302 tells you nothing about whether a given
file exists - you cannot probe filenames from outside.

**The blocker.** Verbatim from `https://eogdata.mines.edu/products/register/`:

> "Effective June 1 2026 EOG is limiting programmatic access via OpenID Client to paid subscribers."

> "For paid subscribers who need to perform programmatic downloads, the new system uses OAuth2.0 protocol."

That date has passed. A free account still exists ("Users will need to register a free
account with verified e-mail address to access EOG's resources"), and manual
browser download on a free account is *probably* still fine - **but I could not confirm
that, because confirming it requires creating an account, which I don't do.** Treat
free-tier manual download as unverified.

Token endpoint, if you ever do subscribe:
`https://eogauth.mines.edu/realms/eog/protocol/openid-connect/token` (returns 403 to an
unauthenticated GET). Tokens expire after 5 minutes.

- **Resolution:** 15 arc-second (~500 m at the equator)
- **Format:** GeoTIFF, DEFLATE-compressed internally, distributed `.gz` / `.tgz`
- **Licence:** CC BY 4.0. Page states: "Many of the VIIRS Nighttime Lights data are
  available under Creative Commons Attribution 4.0 International license." Note the
  hedge - *many*, not all. Credit "Earth Observation Group, Payne Institute for Public Policy".
- **Latest annual:** VNL V2 (v2.2 series), 2012-2024.
- **Exact 2024 filename** (recovered from the `TIFFTAG_DOCUMENTNAME` tag embedded in the
  Zenodo derivative, not from EOG's directory listing):
  `VNL_npp_2024_global_vcmslcfg_v2_c202502261200.average_masked.dat.tif`
  The presumed EOG path is `.../annual/v22/2024/<that name>.gz` - **not confirmed**, the
  auth wall makes it unverifiable from outside.

### 1b. Zenodo mirror - USABLE, verified end to end

Record `10.5281/zenodo.17294744`, 42 files, licence **CC-BY-4.0**, no login, direct HTTPS.

**Download URL (2024, the one to use):**
```
https://zenodo.org/api/records/17294744/files/nightlights.average_viirs.v21_m_500m_s_20240101_20241231_go_epsg4326_v20250904.tif/content
```

Confirmed by actually downloading it:

- **Size:** 63,713,625 bytes (60.8 MiB)
- **Format:** Cloud-Optimized GeoTIFF - 512x512 internal tiles, overviews `[2,4,8,16,32,64]`
- **CRS:** EPSG:4326 | **Grid:** 86400 x 35849 | **Pixel:** 0.0041666667 deg (15 arc-sec, ~500 m)
- **dtype:** `int16` | **nodata:** `-32768`
- **Bounds:** left -180, right 180, top 87.37, bottom -62.0 (all US + CA covered; northernmost CA settlement Alert is 82.5N)
- **Provenance:** internal tag names the EOG source file above, so this is genuinely VNL V2, not a lookalike.

**Scaling caveat.** Zenodo's description: values were "converted from 0-200 to 0-2000
scale". These are **not** raw nW/cm2/sr. Fine for a ranked/normalized dimension; do not
present them as physical radiance.

**Vintage caveat.** Years 2012-2024 are real VIIRS. Years 2000-2011 in that record are
*extrapolated by logistic regression* - do not use them.

**Sampling in Python - `rasterio`, verified working:**

```python
import rasterio
src = rasterio.open("ntl2024.tif")          # note: (lon, lat) order
val = list(src.sample([(-73.9855, 40.7580)]))[0][0]
# batch:
pts = [(lon, lat) for lat, lon in place_coords]
vals = [v[0] for v in src.sample(pts)]
```

Actual output from the real file:

| place | lat | lon | value |
|---|---|---|---|
| Times Square NYC | 40.7580 | -73.9855 | 503 |
| Downtown Toronto | 43.6532 | -79.3832 | 188 |
| Surrey BC | 49.1913 | -122.8490 | 92 |
| Great Basin NP NV | 38.9833 | -114.3000 | 0 |
| Death Valley CA | 36.5054 | -117.0794 | 0 |
| Cherry Springs SP PA | 41.6640 | -77.8160 | 0 |

Three certified dark-sky sites read 0, the densest urban core reads highest. The signal
behaves correctly.

**One honest limitation.** VIIRS measures light going *up* from a pixel, not sky
brightness overhead. A town next to a big city can read near-zero yet have a badly washed-out
sky. If you want true "can you see stars", the apt dataset is the World Atlas of Artificial
Night Sky Brightness (Falchi et al. 2016), DOI `10.5880/GFZ.1.4.2016.001` - the DOI
resolves, but **I did not follow it through to a download link, so treat it as an
unverified lead.**

---

## 2. EPA National Walkability Index (US) - USABLE WITH WORK

### Download URLs (all confirmed live)

| What | URL | Status | Size |
|---|---|---|---|
| Walkability Index (recommended file) | `https://edg.epa.gov/EPADataCommons/public/OA/WalkabilityIndex.zip` | 200 | 425,281,342 B (405.6 MiB) |
| Smart Location DB v3 CSV | `https://edg.epa.gov/EPADataCommons/public/OA/EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv` | 200 | 201,568,176 B (192 MiB) |
| Smart Location DB v3 zip | `https://edg.epa.gov/EPADataCommons/public/OA/SLD/SmartLocationDatabaseV3.zip` | 200 | 553,251,612 B |
| REST query service | `https://geodata.epa.gov/arcgis/rest/services/OA/WalkabilityIndex/MapServer/0/query` | 200 | n/a |
| User guide PDF | `https://www.epa.gov/system/files/documents/2023-10/epa_sld_3.0_technicaldocumentationuserguide_may2021_0.pdf` | 200 | 2,327,386 B |

**Broken link warning:** the epa.gov page links the SLD zip as
`.../EPADataCommons/public/SLD/SmartLocationDatabaseV3.zip` - that **404s**. The working
path has `/OA/` in it (table above).

`WalkabilityIndex.zip` contains, confirmed by reading the zip central directory:
- `National Walkability Index_Methodology and User Guide_June2021.pdf`
- `Natl_WI.gdb/` - an Esri File Geodatabase (read with `geopandas` + `pyogrio`, or GDAL's `OpenFileGDB` driver)

### The CSV has a destroyed join key

**This is the trap.** In `EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv`, both `GEOID10`
and `GEOID20` are written in **scientific notation**:

```
OBJECTID,GEOID10,GEOID20,STATEFP,COUNTYFP,TRACTCE,BLKGRPCE,...
1,4.8113E+11,4.8113E+11,48,113,7825,4,...
```

The 12-digit block group ID `481130078254` was flattened to 5 significant figures. Straight
Excel damage in the published file. **Do not join on those columns.**

Two clean ways around it:

**(a) Reconstruct from the component columns** - verified on 21,644 rows, zero failures,
all results 12 digits and unique:

```python
geoid = (row["STATEFP"].zfill(2) + row["COUNTYFP"].zfill(3)
         + row["TRACTCE"].zfill(6) + row["BLKGRPCE"])
```

**(b) Use the ArcGIS REST service** - `GEOID10`/`GEOID20` come back as
`esriFieldTypeString`, intact. No 400 MB download. 220,134 block groups total,
`maxRecordCount` 1000, paginate with `resultOffset`:

```
https://geodata.epa.gov/arcgis/rest/services/OA/WalkabilityIndex/MapServer/0/query
  ?where=STATEFP='44'
  &outFields=GEOID10,TotPop,NatWalkInd
  &returnGeometry=false&resultOffset=0&resultRecordCount=1000&f=json
```

Real response: `{'GEOID10': '440090503012', 'TotPop': 1182, 'NatWalkInd': 6.833...}`.
~221 paged requests covers the whole country.

### The score column

**`NatWalkInd`**, range **1 to 20**. Built from four ranked sub-scores, each 1-20:
`D2A_Ranked` (employment + housing mix), `D2B_Ranked` (employment mix),
`D3B_Ranked` (intersection density), `D4A_Ranked` (transit proximity).

Formula **verified arithmetically against a real row** (3, 10, 12, 14 -> 10.83333333):

```
NatWalkInd = (D2A_Ranked + D2B_Ranked)/6 + (D3B_Ranked + D4A_Ranked)/3
```

Street connectivity and transit each carry double the weight of the mix terms.

### Facts

- **Unit:** Census block group. EPA says "Census 2019 block group" - i.e. **2010-vintage boundaries**. This matters, see below.
- **Vintage:** SLD v3.0, published/modified 2021-05-13; zip last-modified 2021-06-08. No newer release found.
- **Licence:** Creative Commons Public Domain Dedication (CC0) per catalog.data.gov. Free, no registration.
- **Coverage:** 220,134 block groups, all 50 states + DC + PR.

### Aggregating block groups to a Census place

Block groups do **not** nest inside places, so you need a block-level crosswalk. Verified
recipe (run end to end on Rhode Island):

1. **Block -> place**: Census Block Assignment Files, `BlockAssign_ST<ss>_<XX>_INCPLACE_CDP.txt`,
   pipe/comma-delimited `BLOCKID|PLACEFP`.
2. **Block -> block group**: `BLOCKID[:12]`. Free, no file needed.
3. **Block population** for weighting: TIGER `TABBLOCK20` shapefile `.dbf`, fields
   `GEOID20` + `POP20`. (RI: `https://www2.census.gov/geo/tiger/TIGER2023/TABBLOCK20/tl_2023_44_tabblock20.zip`, 15,962,982 B)
4. **Place GEOID** = `STATEFP` + `PLACEFP` -> your 7-digit key.
5. Population-weight: `sum(POP20 * NatWalkInd) / sum(POP20)` per place.

Verified output, Rhode Island:

| place GEOID | name | pop | pop-weighted NatWalkInd |
|---|---|---|---|
| 4459000 | Providence | 166,150 | 15.62 |
| 4454640 | Pawtucket | 71,497 | 15.44 |
| 4422960 | East Providence | 47,139 | 14.24 |
| 4419180 | Cranston | 81,754 | 13.89 |
| 4474300 | Warwick | 82,823 | 13.02 |
| 4480780 | Woonsocket | 43,240 | 12.64 |

Providence ranking most walkable is the right answer, so the pipeline is sound.

**Vintage mismatch - use the 2010 BAF, not the 2020 one.** EPA's block groups are
2010-vintage. Measured cost of getting this wrong:

- With **2020** BAF (`.../data/baf2020/BlockAssign_ST44_RI.zip`): 13.0% of Providence's
  population sits in 2020 block groups absent from EPA's list and gets silently dropped
  (166,150 used out of a true 190,934).
- With **2010** BAF (`https://www2.census.gov/geo/docs/maps-data/data/baf/BlockAssign_ST44_RI.zip`,
  542,922 B, confirmed 200): **99.63%** block group match (812 of 815; the 3 misses are
  almost certainly water-only, zero-population).

So: 2010 BAF + 2010 block populations. The residual caveat is that 2010 BAF carries 2010
place boundaries - place limits move slowly, but annexations exist, so expect small
discrepancies in fast-growing Sun Belt cities.

---

## 3. Can-ALE (Canada)

**Answering the framing directly:** Can-ALE is **not retired**, and it is **not a StatCan
product**. It is academic work - McGill originally, now Ghasedi & Fuller (U Saskatchewan)
with Achot & Ross (Queen's). StatCan *publishes papers about it* in Health Reports
(82-003-X), but does not host or licence the data.

**Can-ALE 1.0 has been superseded by Can-ALE 2.0 (2025 update).** The old distribution
point `https://nancyrossresearchgroup.ca/research/can-ale/` is **dead (404)**. Data now
lives on GitHub: `walkabillylab/Can-ALE` (last pushed 2026-05-01). Methods paper:
`https://www150.statcan.gc.ca/n1/pub/82-003-x/2026006/article/00001-eng.htm`.

### 3a. Can-ALE 2.0 - USABLE WITH WORK (licence is the catch)

**Download URL (2021, the one to use):**
```
https://raw.githubusercontent.com/walkabillylab/Can-ALE/main/Results/Can-ALE/CanALE_2021.csv
```
Confirmed `HTTP 200`, **7,299,638 bytes**, plain CSV, no login.

Other years: `CanALE_2006.csv` (3,293,462 B), `CanALE_2011.csv` (7,299,811 B),
`CanALE_2016.csv` (7,052,957 B). I md5'd all three - they are genuinely distinct files,
not accidental copies.

- **Unit:** Dissemination Area. **Join key: `DAUID`** (8-digit). 57,932 DAs in the 2021 file.
- **Geography note:** measures are computed in a 1 km circular buffer around each DA's
  *population-weighted* centroid, not the DA polygon.

**Columns (2021 and 2016):**
```
DAUID, pop_density, dwel_density, int_density, poi_count, trstop_count,
z_dwel, z_int, z_poi_count, z_trstop,
ALE_index_class, ALE_transit_index_class, ALE_index, ALE_transit_index
```
- **`ALE_index`** - continuous score (sum of z-scores), the one to use
- **`ALE_index_class`** - 1-5 quintile class
- **`ALE_transit_index`** / `_class` - variant including transit stops

**Schema warning:** the **2011 file has a different schema** - no `pop_density`, no
`trstop_count`, no transit index; instead `poi, walk_rate, active_transport_rate,
transit_rate, all_modes_rate`. Only 2016 and 2021 share a schema. Do not write one parser
for all years.

**Authors' own warning (from the README):** "it is not considered reliable for longitudinal
analysis" - OSM POI coverage improved over time and transit data only exists for 2016 and
2021. Use one year standalone. Fine for us; don't build trends on it.

**LICENCE: NONE. This is the real blocker.** GitHub API reports `"license": null` and there
is no `LICENSE` file in the repo root (contents: `Appendix`, `CNAME`,
`Can-ALE2.0 Full UserGuide.pdf`, `Can-ALE_v1.0_release_2019`, `Codes`, `Data`, `README.md`,
`Results`). No licence means default copyright - **no grant of redistribution or commercial
use**. For a public app that ships these numbers, email the authors (Ghasedi / Fuller,
U Saskatchewan) and get written permission, or use 3b instead.

### Aggregating DA to CSD - verified clean

DAs **do** nest inside CSDs, so this is far easier than the US side. Crosswalk:

```
https://www12.statcan.gc.ca/census-recensement/2021/geo/aip-pia/attribute-attribs/files-fichiers/2021_92-151_X.zip
```
Confirmed 200, **9,832,890 B** zip -> `2021_92-151_X.csv`, 298,768,692 B, 498,785 dissemination
block rows. Relevant columns: `DAUID_ADIDU`, `CSDUID_SDRIDU`, `CSDNAME_SDRNOM`,
`DBPOP2021_IDPOP2021`.

Verified by running it:

- **0 DAs span more than one CSD** - the nesting is clean, no allocation factors needed
- 57,936 DAs, 5,161 CSDs, total population **36,991,981** - exactly the 2021 Census count
- Can-ALE joins at **100%**: 57,932 of 57,932 DAs matched, all 5,161 CSDs reachable,
  100.00% of national population covered

```python
# pop-weighted roll-up
num = sum(ale[da]["ALE_index"] * dapop[da] for da in das_in_csd)
val = num / sum(dapop[da] for da in das_in_csd)
```

Verified results:

| CSD | name | DAs | pop | pop-weighted `ALE_index` |
|---|---|---|---|---|
| 3520005 | Toronto | 3,743 | 2,794,356 | 3.577 |
| 5915004 | Surrey BC | 666 | 568,322 | 0.570 |

Toronto ~6x Surrey is the right shape.

### 3b. StatCan Proximity Measures Database - the licensed alternative

Since Can-ALE ships with no licence, this is the fallback that is unambiguously free to use.

**Download URL (2021 vintage, current):**
```
https://www150.statcan.gc.ca/n1/pub/17-26-0002/2023001/csv/pmd-eng.zip
```
Confirmed 200, **25,859,794 B** zip -> `pmd-eng/PMD-en.csv`, 163,802,227 B, **498,547
dissemination blocks**. Released 2023-06-27. (The older 2016-vintage release is at
`.../2020001/csv/pmd-eng.zip`, 10,526,411 B.)

- **Licence:** Open Government Licence - Canada. Free, no registration, commercial use fine.
- **Unit:** dissemination block (finer than DA).
- **Killer feature: no crosswalk needed.** `CSDUID`, `CSDNAME`, `CSDTYPE`, `CSDPOP` are
  already columns, alongside `DBUID`, `DBPOP`, `DAUID`, `DAPOP`, `lon`, `lat`.
- **Score columns:** ten gravity-model proximity indices -
  `prox_idx_emp`, `prox_idx_pharma`, `prox_idx_childcare`, `prox_idx_health`,
  `prox_idx_grocery`, `prox_idx_educpri`, `prox_idx_educsec`, `prox_idx_lib`,
  `prox_idx_parks`, `prox_idx_transit`, plus a composite `amenity_dense` flag.
- **Gotchas:** suppressed values appear as `..`; `CSDPOP` is comma-quoted (`"108,860"`) in
  the 2016 release, plain float in 2021.

Not a single walkability score like `NatWalkInd`, so you would compose your own index from
the proximity columns. But it is official, current, properly licensed, and already keyed to
CSD.

---

## Verification log

Things I confirmed by actually running them, not by reading about them:

- EOG `annual/v22/` and `annual/v22/2022/` both 302 to Keycloak; token endpoint 403s
- The "paid subscribers" sentence, pulled verbatim from the register page HTML
- `WalkabilityIndex.zip` 200 + exact byte count + its internal file list (zip central directory)
- The EPA CSV's scientific-notation GEOID defect, seen in the raw bytes
- GEOID reconstruction: 21,644 rows, 0 failures
- `NatWalkInd` formula: reproduced 10.83333333 from its four components
- EPA REST: 220,134 records, GEOIDs as strings
- Full RI block-group -> place aggregation, six places
- 2020-BAF vs 2010-BAF vintage cost: 13.0% vs 0.37% loss
- Can-ALE year files md5'd distinct; 2011 schema differs
- Can-ALE licence absence via GitHub API
- DA->CSD nesting: 0 spanning DAs, population total matched the census exactly
- Can-ALE -> CSD join: 100% of DAs, 100% of population
- Downloaded the 60.8 MiB nightlights COG and sampled 6 real coordinates in rasterio

Things I could **not** confirm:

- Whether a **free** EOG account can still download annual composites manually (would require creating an account)
- The exact EOG URL for the 2024 annual file (auth wall 302s every path identically)
- The World Atlas of Artificial Night Sky Brightness download link (DOI resolves; I did not follow it through)
- Whether EPA has any post-2021 walkability release (none found, but absence of evidence)
