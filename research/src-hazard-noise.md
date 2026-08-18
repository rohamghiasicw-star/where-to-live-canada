# Source verification: hazard risk + transportation noise

Verified 2026-08-18. Every status below was observed directly (HTTP code, byte count, or parsed file contents). Where I could not confirm something I say so.

## Verdict table

| # | Source | Unit | Join key | Verdict |
|---|---|---|---|---|
| 1 | FEMA National Risk Index | US county + census tract | STCOFIPS / TRACTFIPS | **USABLE** |
| 2 | BTS National Transportation Noise Map | US 30 m raster | lat/lon | **USABLE WITH WORK** |
| 3a | Canada hazard: NRCan flood susceptibility | 30 m raster, national | lat/lon | **USABLE** |
| 3b | Canada hazard: NRCan seismic risk (PSRA) | Census Subdivision | csduid | **USABLE** |
| 3c | Canada hazard: wildfire | national but awkward | lat/lon | **USABLE WITH WORK** |
| 3d | Canada noise: any national dataset | none exists | n/a | **NOT USABLE** |

---

## 1. FEMA National Risk Index (US hazard)

### The catch first

`hazards.fema.gov` was **unreachable from two independent networks** during this check. TLS connect failed from this machine on both IPs returned by Cloudflare and Google DNS (curl exit 35), and the Anthropic-side fetcher returned ECONNRESET. The browser pane also refused the origin. So I **could not confirm** that the official FEMA-hosted bulk downloads are live today.

Wayback proves those URLs were real and served real bytes:

- `https://hazards.fema.gov/nri/Content/StaticDocuments/DataDownload//NRI_Table_Counties/NRI_Table_Counties.zip` - archived 200, 7,801,229 bytes (2025-02-10)
- `https://hazards.fema.gov/nri/Content/StaticDocuments/DataDownload//NRI_Table_CensusTracts/NRI_Table_CensusTracts.zip` - archived 200, 150,428,643 bytes (2025-05-06)
- `https://hazards.fema.gov/nri/Content/StaticDocuments/DataDownload//NRI_GDB_Counties/NRI_GDB_Counties.zip` - archived 200, 90,345,202 bytes
- `https://hazards.fema.gov/nri/Content/StaticDocuments/DataDownload//NRI_Shapefile_CensusTracts/NRI_Shapefile_CensusTracts.zip` - archived 200, 599,196,813 bytes
- `https://hazards.fema.gov/nri/Content/StaticDocuments/DataDownload/NRIDataDictionary.csv` - archived 200, ~7.9 KB
- Per-state CSVs exist too: `.../NRI_Table_CensusTracts/NRI_Table_CensusTracts_Alabama.zip` etc.

But the last **successful** Wayback capture of `hazards.fema.gov/nri/data-resources` was 2025-12-13 (HTTP 200). Every 2026 capture of `hazards.fema.gov/nri/*` records a 301 or 302 at capture time. Treat the hazards.fema.gov host as **doubtful** until you can hit it from a network that reaches it.

Also checked and ruled out: the NRI is **not** in the OpenFEMA API (`/api/open/v1/DataSets` returns 48 datasets, none of them NRI), and `catalog.data.gov`'s CKAN API returned 404.

### The path that actually works (verified end to end)

FEMA publishes the same data as ArcGIS feature services under the org `FEMA_NationalRiskIndex`, and ArcGIS Hub serves a **real bulk CSV** off them. I downloaded it.

**Counties CSV (verified: HTTP 200, 18,918,805 bytes, 468 columns, 3,231 data rows)**
```
https://hub.arcgis.com/api/v3/datasets/39485e8035d446a5bff03259508ae355_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1
```
Content-Disposition filename `National_Risk_Index_Counties.csv`.

**Census tracts CSV (verified: HTTP 200, Content-Type text/csv - not fully downloaded)**
```
https://hub.arcgis.com/api/v3/datasets/9da4eeb936544335a6db0cd7a8448a51_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1
```
Content-Disposition filename `National_Risk_Index_Census_Tracts.csv`. Swap `format=csv` for `geojson`, `shapefile`, or `filegdb`.

**Underlying feature services (both verified with live queries):**
- Counties: `https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0` - 3,232 records
- Tracts: `https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Census_Tracts/FeatureServer/0` - 85,154 records
- Capabilities `Query,Extract,ChangeTracking`, pagination supported, maxRecordCount 2000. So 2 pages for counties, 43 for tracts if you page instead of bulk-downloading.

### Version, geography, columns

- **Version: `NRI_VER = "December 2025"`** (read from live records, not from a page).
- **Geographic units: county AND census tract.** Also states, tribal counties, tribal tracts.
- **Join keys:** `STCOFIPS` (5-digit state+county FIPS, string) and `TRACTFIPS` (11-digit, string). Your 7-digit place GEOID does not join directly. You need your place -> county FIPS map for the county file, or a point-in-polygon of place lat/lon against tract geometry for the tract file. Tract is much better resolution for wildfire and flood, so it is worth the point-in-polygon.
- 467 fields on the county layer.

**Composite scores:**
| Column | Meaning |
|---|---|
| `RISK_SCORE` | National Risk Index score, composite (0-100) |
| `RISK_RATNG` | Rating string, e.g. "Very High", "Relatively High" |
| `RISK_SPCTL` | State percentile, composite |
| `RISK_VALUE` | Dollar-denominated composite |
| `EAL_SCORE` | Expected Annual Loss, composite |
| `SOVI_SCORE` | Social Vulnerability |
| `RESL_SCORE` | Community Resilience |

**Per-hazard scores.** Pattern is `<HAZ>_RISKS` (score 0-100), `<HAZ>_RISKR` (rating string), `<HAZ>_RISKV` (dollar value). All 18 hazards present at both county and tract level:

| You asked for | Column |
|---|---|
| Flood (riverine/inland) | `IFLD_RISKS` |
| Flood (coastal) | `CFLD_RISKS` |
| Wildfire | `WFIR_RISKS` |
| Hurricane | `HRCN_RISKS` |
| Tornado | `TRND_RISKS` |
| Earthquake | `ERQK_RISKS` |

Other 12: `AVLN` avalanche, `CWAV` cold wave, `DRGT` drought, `HAIL`, `HWAV` heat wave, `ISTM` ice storm, `LNDS` landslide, `LTNG` lightning, `SWND` strong wind, `TSUN` tsunami, `VLCN` volcanic, `WNTW` winter weather.

Note there is **no `RFLD_` prefix** - riverine flooding is `IFLD_`. Easy trap.

**Real values pulled live (proof the join works):**
```
06037 Los Angeles CA  RISK_SCORE 100     Very High         WFIR_RISKS 99.94  ERQK_RISKS 100
36061 New York    NY  RISK_SCORE 98.79   Relatively High   WFIR_RISKS 9.92   HRCN_RISKS 96.79
36061000100 (tract)   RISK_SCORE 0.235   Very Low
```

### Licence and cost

Free, no key, no login. Not a standard open licence - it is a FEMA Terms & Conditions page. Key clauses, verbatim from the item metadata:

> "The National Risk Index data are meant for planning purposes only. This National Risk Index dataset was created for broad nationwide comparisons and is not a substitute for localized risk assessment analysis."

Also contains a "No Reverse Engineering of Data" clause and reserves the right to suspend access. Nothing prohibits display or redistribution of derived rankings, but it is **not** a public-domain grant. If you surface it, credit FEMA and label it as planning-level national comparison data.

### File sizes

- Counties CSV: 18.9 MB (measured)
- Tracts CSV: not measured; the equivalent FEMA-hosted zip was ~150 MB compressed
- FEMA GDB counties: ~90 MB, tracts ~336-420 MB; shapefile tracts ~540-600 MB (Wayback-measured)

### Verdict

**USABLE.** Current (December 2025), county and tract, all six hazards you named plus twelve more, clean FIPS join, verified working bulk CSV. Use the ArcGIS Hub download, not hazards.fema.gov, until that host is confirmed live.

---

## 2. BTS National Transportation Noise Map (US noise)

### Bulk data is downloadable. Confirmed.

Not viewer-only. Real zip files, real bytes. I downloaded one and opened it.

Download index page: `https://www.bts.gov/geospatial/national-transportation-noise-map`

**Current release: 2022/2023 data, published May 2026.** Aviation and rail are 2022, roads are 2023. Note the URLs all say `_2022` even for the road files the page labels 2023.

Sizes below were read from live HTTP 200 responses (Content-Length):

| File | URL | Bytes |
|---|---|---|
| CONUS aviation | `https://www.bts.gov/bts-net-storage/CONUS_aviation_noise_2022.zip` | 229,798,043 |
| CONUS rail | `https://www.bts.gov/bts-net-storage/CONUS_rail_noise_2022.zip` | 552,175,516 |
| CONUS road | `https://www.bts.gov/bts-net-storage/CONUS_road_noise_2022.zip` | 1,113,715,793 |
| CONUS road+rail+aviation | `https://www.bts.gov/bts-net-storage/CONUS_rail_road_and_aviation_noise_2022.zip` | 1,633,481,316 |
| Alaska aviation | `https://www.bts.gov/bts-net-storage/Alaska_aviation_noise_2022.zip` | 7,097,088 |
| Hawaii aviation | `https://www.bts.gov/bts-net-storage/Hawaii_aviation_noise_2022.zip` | 1,769,809 |

Also `CONUS_road_and_aviation_noise_2022.zip`, plus Alaska/Hawaii road and combined variants, and full 2020 / 2018 / 2016 archives at the same path pattern.

**Access friction:** `www.bts.gov` sits behind Akamai and returns 403 to plain curl and to WebFetch. A browser works. Curl works with a full browser header set including `Referer: https://www.bts.gov/geospatial/national-transportation-noise-map` - that is how I pulled the Hawaii file. Range requests get 403. After one successful download Akamai started 403ing me on the CONUS file, so **budget for rate limiting** and download from a real browser session if scripted pulls get blocked.

### Format: Esri file geodatabase mosaic raster, not GeoTIFF

I unzipped `Hawaii_aviation_noise_2022.zip` and looked inside. It contains:
- `Hawaii_aviation_noise.gdb/` - an Esri file geodatabase holding one mosaic raster dataset (`Hawaii_Hawaii_aviation_noise_mosaic`) with the base raster item named `HI_aviation_noise`
- `Hawaii_aviation_noise.Overviews/` - pyramid TIFFs with `.tfw` world files

For CONUS, BTS's own repair instructions state the package holds three things:

> "an Esri file geodatabase with one mosaic raster dataset inside, a folder for the mosaic's overview files, and a folder containing all the state rasters used to build the mosaic dataset"

Source: `https://www.bts.gov/explore-topics-and-geography/geography/national-transportation-noise-map-repairing-continental-us`. **I could not verify the CONUS package contents directly** - Akamai 403'd my download attempt. So the "folder of state rasters" is BTS's claim, not something I opened. It matters, because those state rasters are probably the practical route into GDAL.

**The 2016, 2018 and 2020 CONUS mosaics ship with broken internal paths** and need a manual "Repair Mosaic Dataset Paths" in ArcCatalog/ArcGIS Pro or they render as a black checkerboard. The 2022 CONUS files are not flagged for this on the page.

### GDAL cannot open the mosaic. This is the real cost.

I installed GDAL 3.12.4 (via rasterio) and tried to open the Hawaii geodatabase four ways, including the `OpenFileGDB:"path.gdb":rastername` subdataset syntax. **All failed.** GDAL's OpenFileGDB driver reads the vector tables in the gdb - I listed all 11 layers including the mosaic catalog `AMD_..._CAT` - but it will not open the mosaic raster itself. Reading the catalog's `LowPS`/`HighPS` cell-size doubles came back as garbage floats, so I could not read the cell size out of the file either.

So your options for a lat/lon sample are:
1. Use the per-state source rasters BTS says ship inside the CONUS zip (best bet, if they are plain TIFF - unverified)
2. Convert the mosaic to GeoTIFF once in ArcGIS Pro, then sample with rasterio
3. Buy/borrow ArcGIS

### The web services cannot be sampled. Confirmed dead end.

The item metadata points to `https://tiles.arcgis.com/tiles/xOi1kZaI0eWDREZv/arcgis/rest/services` for services beginning `NTAD_Noise_2022.`. There are 54 MapServers there, e.g. `NTAD_Noise_2022_CONUS_aviation_road/MapServer`. I read the service JSON:

```
capabilities        = Map,TilesOnly,Tilemap
singleFusedMapCache = True
exportTilesAllowed  = False
```

`TilesOnly` means **no Query, no Identify, no Export**. These serve pre-rendered PNG tiles only. You cannot get a dB value at a lat/lon from them. The BTS org has **zero ImageServers**. Same for `maps.dot.gov/BTS/NationalTransportationNoiseMap/` - that is the viewer, not an API.

### Resolution and metric

- **Metric: 24-hour equivalent A-weighted sound level (24-hr LAeq), in dBA.** Confirmed from the BTS item metadata and from `https://data.bts.gov/stories/s/National-Transportation-Noise-Map/ri89-bhxh/`.
- **dB floor: the published exposure tables start at 45 dBA**, and pixels below ~45 dBA LAeq are reported as missing rather than as a low value. Confirmed from the BTS story tables (bands run "45 to 49", "50 to 54" ... "80 or more").
- **Resolution: 30 m.** This is what the BTS documentation states. **I could not open the current documentation PDF to quote it directly** - `https://rosap.ntl.bts.gov/view/dot/90910/dot_90910_DS1.pdf` (299 KB, checksum published) 403s to both curl and WebFetch, and the browser could reach the ROSA-P landing page but not extract PDF text. The machine-readable ArcGIS/DCAT metadata carries no resolution field at all. What I could measure directly: the Hawaii overview pyramids have cell sizes of 360, 1080, 1440 and 4320 m, which is consistent with a fine base raster but does not by itself prove 30 m. **Treat 30 m as documentation-reported, not file-verified.**
- Projection: state/region Albers Equal Area Conic (Hawaii package uses `Hawaii_Albers_Equal_Area_Conic`).
- Modes: aviation, road, rail, separately and combined. CONUS, Alaska, Hawaii.

### Licence

Public domain. Verbatim:

> "This NTAD dataset is a work of the United States government as defined in 17 U.S.C. § 101 and as such are not protected by any U.S. copyrights. This work is available for unrestricted public use."

Attribution requested: "Acknowledgment of the Bureau of Transportation Statistics (BTS)." Free, no key.

### The disclaimer you must respect

BTS says this repeatedly and it cuts against exactly what you want to use it for:

> "should not be used to evaluate noise levels in individual locations and/or at specific times"

and the tool documentation notes shielding is not modelled - no barriers, no terrain - so noise is overestimated in shielded areas. It also excludes helicopters, maritime, and all non-transportation sources.

For a coarse "is there a flight path or interstate over this town" signal at city scale this is defensible. Do not present it as a measured noise level for an address.

### Verdict

**USABLE WITH WORK.** Bulk data is genuinely downloadable and public domain. Three real costs: (a) Esri mosaic geodatabase that open-source GDAL will not open, so you need a one-time ArcGIS conversion or the per-state rasters, (b) 1.6 GB for the combined CONUS layer plus Akamai rate limiting, (c) a vendor disclaimer that argues against point-level use. Budget a day, not an hour.

---

## 3. Canada

Your working assumption was that no clean national CSD-level dataset exists for either hazard or noise.

**For noise: CONFIRMED. Nothing national exists.**
**For hazard: REFUTED, partially. Three real national datasets exist, and one of them is already keyed to CSD.**

### 3a. Flood - NRCan flood susceptibility - USABLE

A complete national 30 m flood susceptibility layer, and you can point-sample it over HTTP without downloading anything.

- Landing: `https://open.canada.ca/data/en/dataset/3202e0a0-0afb-4120-b102-b0c41f0fb9eb`
- Full raster: `https://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/water/flood-susceptibility/fs-trends/fs-2000-2023-current.tif` - **verified HTTP 200, 5,901,141,883 bytes (5.9 GB), Content-Type image/tiff, Accept-Ranges: bytes**. BigTIFF/COG, 30 m, EPSG:3979, 153,735 x 179,486 px, values 0-100.
- **Point sampling via WMS GetFeatureInfo. I ran this myself:**
```
https://datacube.services.geo.ca/ows/fs-trends?service=WMS&version=1.3.0&request=GetFeatureInfo
  &layers=fs-2000-2023-current&query_layers=fs-2000-2023-current&styles=default
  &format=image/png&info_format=application/json&crs=EPSG:4326
  &width=101&height=101&i=50&j=50&bbox=<lat-d>,<lon-d>,<lat+d>,<lon+d>
```
Live results: Surrey BC 10, Toronto 21, Halifax 36. All HTTP 200, property `band-0-pixel-value`. 710 places sequentially is roughly 7 minutes.
- Companion layers on the same endpoint: `-current-iqr` (uncertainty, and it is material - Ottawa's IQR is 23 against a value of 49), `-wet-extreme`, `-dry-extreme`, `-slope`, `-trend-class`. Forward-looking projections at `https://datacube.services.geo.ca/ows/fs-future` (2050/2070/2100, SSP 245/585).
- **Gotcha:** open water scores high. A point in the Gulf of St Lawrence returned 53. Sample a populated centroid, or buffer and take a percentile.
- **No WCS** (404). Per-point WMS or local COG range-reads only.
- Join key: lat/lon. No CSD.
- Licence: Open Government Licence - Canada. Free.

**Dead end to avoid:** the archived Flood Susceptibility Index files `FS-national-2015-index.tif` and `-class.tif` both return **403 Forbidden**. Use the `fs-trends` collection.

**FHIMP is not a hazard layer.** The Canada Flood Map Inventory (`https://open.canada.ca/data/en/dataset/a13a2575-5bda-4bfd-a9b1-5bd2dd583f09`, gpkg verified 200, 5,694,369 bytes) is 675 polygons whose attribute is literally "Presence of mapped flood areas". NRCan states it "does not display flood zones or extents" and "may be incomplete". **NOT USABLE.**

### 3b. Seismic - NRCan PSRA - USABLE, and already CSD-keyed

This is the only Canadian hazard product that ships keyed to Census Subdivision.

- Landing: `https://open.canada.ca/data/en/dataset/7590d295-5c17-44c8-ad2e-2e8f1a4b6054`
- Download: `https://ftp.cartes.canada.ca/pub/nrcan_rncan/Seismology_Sismologie/CanadaSRM/psra_indicators_csd.zip` - **verified HTTP 200, 27,178,861 bytes, application/zip**
- GeoPackage, 42.5 MB unzipped, **5,162 rows**, full national CSD coverage (~90% populated).
- **Join key: `csduid`, TEXT(7). Direct join to your CSD codes.** Plus `csdname`.
- Pre-computed composite: `eqri_norm_score_b0` and `eqri_norm_rank_b0`.
- Sample values: Victoria 44.4, Vancouver 36.7, Richmond 36.6, Surrey 33.5, Montreal 28.9, Ottawa 17.0, Toronto 14.8, Calgary 11.4, Halifax 8.5, Winnipeg 7.5.
- **Ranking gotcha:** use the rate-normalized fields (`eqri_norm_*`, `eDtr_*`, `eCr_*`). The absolute fields just rank by population.
- Licence: OGL-Canada. Free.

**Also: a free lat/lon seismic hazard API, no key.** `https://www.earthquakescanada.nrcan.gc.ca/api/canshm/graphql`. I tested it:
```
POST {"query":"{ NBC2020(latitude: 49.1913, longitude: -122.8490)
       { siteDesignationsXv(vs30: 450, poe50: [2.0]) { poe50 pga sa0p2 sa1p0 } } }"}
-> HTTP 200 {"data":{"NBC2020":{"siteDesignationsXv":[{"poe50":2.0,"pga":0.428,"sa0p2":1.0,"sa1p0":0.41}]}}}
```
Roots `NBC2020` / `NBC2025`. GraphQL aliases batch it, ~60 points per request, so 710 places is about 12 requests. No published rate limit; robots.txt does not disallow `/api/`.

Bulk grid alternative (Open File 8950): `https://ostr-backend-prod.azure.cloud.nrcan-rncan.gc.ca/server/api/core/bitstreams/c36e469b-89ab-4ef9-a874-903def23bab4/content` - 200, 232,033,937 bytes. NBCC 2020 only, and it is a Delaunay triangulation not a grid, so offline use needs barycentric interpolation. Prefer the API. Avoid Open File 8629 (679-locality table) - it is the superseded trial model.

### 3c. Wildfire - USABLE WITH WORK, no good forward-looking option

- **Projected Burn Probability**: `https://open.canada.ca/data/en/dataset/2d0b4927-38e4-451b-9e7f-cb586a1ac01b`, baseline zip verified 200 at 4,453,620,389 bytes (4.45 GB), 30 m, projections to 2100. Two killers: coverage is **forested ecozones only** (prairie and tundra municipalities are nodata), and its WMS returns `LayerNotQueryable` so there is **no remote point sampling**. You process 4.4 GB per scenario or nothing.
- **Best cheap path - historical fire points (NFDB):** `https://cwfis.cfs.nrcan.gc.ca/downloads/nfdb/fire_pnt/current_version/NFDB_point_txt.zip` - verified 200, 93,915,643 bytes. Supports a defensible "fires within X km over N years" density score.
- **FBP fuel types 250 m:** `https://ca.nfis.org/fss/fss?command=retrieveByName&fileName=FBP_FuelTypes_Canada_2026_250m.tif&fileNamespace=fire_behaviour_prediction` - verified 200, image/tiff, 49,085,574 bytes. An exposure input, not a risk rating.
- CWFIS daily fire danger samples fine at lat/lon but it is **today's weather**. Ranking on it would rank last night's conditions. NOT USABLE here.
- **WUI / Wildland-Human Interface national map: could not confirm any public download.** The CWFIS GeoNetwork catalogue was enumerated in full (58 records, no WUI layer) and CKAN returns 0 for "WUI Canada". Appears to be publication-only.
- The datamart at `https://cwfis.cfs.nrcan.gc.ca/datamart` is a React SPA, but `https://cwfis.cfs.nrcan.gc.ca/downloads/` is a plain Apache index with stable direct URLs.
- Licence: OGL-Canada. Free.

### 3d. Canadian Disaster Database - USABLE WITH WORK, historical only

- Landing: `https://www.publicsafety.gc.ca/cnt/rsrcs/cndn-dsstr-dtbs/index-en.aspx` (200)
- Download: `https://open.canada.ca/data/dataset/1c3d15f9-9cfa-4010-8462-0d67e493d9b9/resource/c701e05e-4554-4c96-b7c9-0ec4a845fe91/download/cdd-extract-1.xlsx` - 302 to Azure blob, then 200, 551,792 bytes. **XLSX, not CSV.**
- 1,490 rows, 1,053 natural. Columns `PLACE`, `GEOG_OBJ` (WKT), `PROVINCES_AFFECTED`. 1,342 POINT + 147 POLYGON.
- **Granularity is the problem.** ~49% of `PLACE` strings are regional ("Southern Ontario", "Prairie Provinces"). Only 619 distinct coordinates across 910 natural point events - `POINT (-105 50)` is reused 38 times as a stand-in for the Prairies.
- Range 1900-01-09 to 2022-12-22. Roughly 3.5 years stale. No CSD key.
- It is a **historical event log, not a forward-looking risk score.** OGL-Canada, free.

### 3e. National Risk Profile - NOT USABLE

- Landing: `https://www.publicsafety.gc.ca/cnt/mrgnc-mngmnt/ntnl-rsk-prfl/index-en.aspx` (200). PDF: `https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/2023-nrp-pnr/2023-npr-pnr-en.pdf` - 200, 9,542,571 bytes, 179 pages.
- **Narrative only.** Full-text counts across the PDF: "census subdivision" 0, ".csv" 0, "download" 0. All six annexes are terminology and methodology - no data annex.
- Public Safety Canada's entire CKAN catalogue is 13 datasets and the NRP is not one of them. Risk ratings are ordinal expert votes on national scenarios.

### 3f. Canadian transportation noise - NOT USABLE. Nothing national exists.

This is a confirmed negative from primary sources, not a failure to find something.

**Health Canada: publications, zero datasets.** A CKAN query filtered to Health Canada + data formats (CSV/SHP/GEOJSON) + noise terms returns **count 0**. All six Health Canada noise entries are typed `info / publication` with HTML-only resources ("Noise and your health", "Airplanes", "Wind Turbine Noise", etc.). No map, no geodata.

**Transport Canada NEF/NEP: no national dataset, and structurally there cannot be one.** From TP 1247E section 4.3.1 (`https://tc.canada.ca/sites/default/files/migrated/tp1247e.pdf`, verified 200, 724,010 bytes):

> "Noise contours (NEFs, NEPs and Planning Contours) are the property of the sponsoring aerodrome operator or airport authority"

> "Transport Canada does not retain copies of NEFs and NEPs submitted to it for technical review."

TC distributes the NEF **calculation software** on request, not contour data. `open.canada.ca` search for "NEF contour" returns count 0. The TC page itself says the NEF "is not intended for use by the general public".

One exception found, Calgary only: `https://data.calgary.ca/resource/g5qu-w8fb.geojson` - verified 200, 84,277 bytes, 5 MultiPolygons, `dblevel` 25/30/35/40. Licence "See Terms of Use", commercial terms not verified. Use `g5qu-w8fb`, not the sibling `hj37-nnn4` which returns empty features. Toronto Pearson could not be confirmed (Radware blocked the fetch).

**CANUE: a noise metric exists, but it is 5 cities and academic-only.** Metadata `https://www.canuedata.ca/metadata/CANUE_METADATA_NHNSE_AVA_YY.pdf` (200, 41,926 bytes). Dataset `NHNSE_AVA_YY`, A-weighted Leq dB, keyed to 6-digit postal code. Coverage is **Vancouver, Toronto, Montreal, Longueuil, Halifax only**. Access barrier from `https://www.canuedata.ca/request.php`:

> "In order to receive data from CANUE, your institution must participate in the DMTI Spatial SMART Consortium Agreement... you will be asked to download, sign and return a data sharing agreement."

Hardcoded list of ~40 Canadian universities. Use conditions: "should not be re-distributed for any reason", "exclusive purposes of teaching, academic research and publishing". **Not available to you.**

**Municipal noise maps: city-specific, nowhere near national.** An exhaustive open.canada.ca sweep (noise, bruit, sonore, Lden, decibel, sound level, environmental noise, noise map, acoustic environment - "Lden" returns 0) found only five genuine noise datasets nationwide, all Quebec, all single-city: high noise sector Trois-Rivieres (GeoJSON 200, 93,099 bytes), acoustic level measurements for one Montreal street (CSV 200, 11.2 MB, meter readings not a map), and three Laval sound-constraint layers. All CC-BY, free. Toronto/Vancouver/Ottawa city-native portals were **not individually checked** - flagged as an open item, though the federated CKAN sweep argues against anything being there.

**Why nothing national exists:** Canada has no federal noise-mapping mandate comparable to the EU Environmental Noise Directive. There is no agency tasked with producing one.

**Proxies, clearly labelled as proxies:**
- StatCan aircraft movements: `https://www150.statcan.gc.ca/n1/tbl/csv/23100019-eng.zip` - 200, 102,489 bytes, annual per towered airport, no coordinates. **Table 23-10-0008 is archived and ends 2022-09 - do not build on it.** OGL-Canada.
- OpenSky ADS-B live states: `https://opensky-network.org/api/states/all?lamin=...` - 200 anonymously, returned 19 live aircraft over a Surrey BC box. Anonymous is live-only, 400 credits/day. **Licence for commercial use could not be confirmed** - the REST docs carry no licensing terms. Needs weeks of continuous sampling per place.
- National AADT road network: **not completed.** Only provincial publishers seen (BC, NB, AB, ON, QC each separately); absence of a national compilation was not proven.

### CSD bridge

2021 Census Subdivision cartographic boundaries: `https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcsd000b21a_e.zip` - verified 200, 155,981,521 bytes. Free. That is how you get from your 710 places to centroids for the flood raster sampling, or join straight to `csduid` for seismic.

---

## Recommended build

**US disaster resilience:** FEMA NRI census tract via the ArcGIS Hub CSV, point-in-polygon your place lat/lon into tracts, fall back to county via your FIPS map where a tract lookup fails. Use `RISK_SCORE` as the headline and the six named `_RISKS` columns as the breakdown. Ships today.

**US quiet:** BTS noise is real but costs a day. If you want the dimension cheap and honest, ship it as aviation-only first - CONUS aviation is 230 MB, not 1.6 GB.

**Canada hazard:** seismic is ready-made at CSD (`eqri_norm_score_b0`, direct `csduid` join). Flood is ~7 minutes of WMS point sampling against populated centroids. Wildfire has no clean answer - the honest option is historical fire density from the 94 MB NFDB point file.

**Canada quiet:** do not ship this dimension. There is no source. Showing the dimension for US places and hiding it for Canadian ones is the only non-invented option.

## Open items

- `hazards.fema.gov` live status - unreachable from two networks, could not confirm
- BTS 30 m resolution - documentation-reported, PDF not openable, not file-verified
- BTS CONUS zip contents (the per-state rasters folder) - BTS's claim, Akamai 403'd verification
- Whether GDAL can read those per-state rasters - unverified, this determines whether BTS noise is a day or a week
- Toronto/Vancouver/Ottawa city-native open data portals for noise layers - not individually checked
- Canadian national AADT compilation - absence not proven
- OpenSky commercial licence terms - could not confirm
