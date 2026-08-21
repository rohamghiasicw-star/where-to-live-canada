# Source verification: outdoor activities (hiking, bicycling, skiing) - US + CA

Verified 2026-08-21. Target dimension, user's exact words: *"Outdoor activities ( hiking
bicycling proximity to skiing etc)"*. Scope: 4,197 US places, 710 Canadian CSDs.

Every URL below was actually requested and the response inspected. Byte counts are from
`Content-Length` or the file on disk, never estimated. Row counts and acreages are from
data I parsed myself. Anything I could not confirm is in the "Could not confirm" section
at the bottom rather than smoothed over.

**Bottom line**

| # | Source | Verdict |
|---|--------|---------|
| 1 | PAD-US 4.1 **flattened Vector Analysis** file | **USABLE** - proven end to end. 322k polygons, equal-area CRS, 50 km buffer sums in 0.01-0.28 s/place. One booby trap, see 1.4. |
| 1b | PAD-US 4.1 **raster** | **NOT USABLE** - 81 GB uncompressed for CONUS. 8.1 GB for Hawaii alone. |
| 1c | PAD-US **county summary CSV** | **NOT USABLE** as a join - carries no county FIPS, only a name string. County is the wrong geography anyway. |
| 1d | PAD-US **ArcGIS FeatureServer** | **NOT USABLE** for acreage - server-side `SUM` over-counts 2.6x. Measured. |
| 1e | PAD-US **full geodatabase + all state files** | **NOT USABLE** - login-walled behind ScienceBase sign-in. |
| 2 | CPCAD 2025 (ECCC) | **USABLE** - 22,438 polygons, equal-area CRS, whole country in 2.6 s. Cleanest source in this whole document. |
| 2b | CPCAD ArcGIS MapServer | **USABLE WITH WORK** - live, works, good fallback. Same over-count caveat as 1d if you use `outStatistics`. |
| 3 | **OpenSkiMap** ski_areas.csv | **USABLE** - 525 US + 235 CA operating areas, 100% lat/lon, rebuilt daily. The answer for skiing. |
| 3b | NSAA members list | **NOT USABLE** as data, **USABLE** as a benchmark - 492 US areas, free PDF, no per-area rows. |
| 3c | OSM `landuse=winter_sports` direct | **USABLE WITH WORK** - 721 CONUS / 611 CA polygons, but mixes Nordic+tubing hills and bboxes leak across the border. |
| 3d | CWSAA / Canadian Ski Council | **NOT USABLE** - login-walled or name-lists with no coordinates. |
| 4 | **USGS TNM** `Trans_TrailSegment` | **USABLE WITH WORK** - `lengthmiles` is a real attribute, national, but state coverage is wildly uneven. |
| 4b | USFS NFS Trails | **USABLE** - 86,303 segments, 163,204.6 mi, zero nulls. National-forest land only. |
| 4c | NPS trails | **USABLE WITH WORK** - 31,358 features, no length attribute, must compute geodesically. |
| 4d | OSM trails via Overpass `out geom` | **USABLE** - length IS obtainable. VT 40 MB/8.6 s, CA 300 MB/159 s. |
| 5 | **PeopleForBikes** City Ratings 2026 | **USABLE** - 3,014 unique place GEOIDs, joins directly. But its miles are NOT bike-lane miles. |
| 5b | Any government bike-lane mileage dataset | **NOT USABLE - does not exist.** BTS, FHWA and Census all checked and all empty. |

---

## 1. USGS Protected Areas Database (PAD-US)

### 1.1 Current version

**PAD-US 4.1, published 2025-03-31.** There is no 4.2 or 5.

Confirmed two ways: the ScienceBase parent item `65294599d34e44db0e2ed7cf` lists only 4.0
and 4.1 children, and the USGS data-history page states 4.1 released March 2025 is the
most recent. DOI `https://doi.org/10.5066/P96WBCHS`.

**Licence: public domain.** The USGS ArcGIS Online item for PAD-US states verbatim: "This
content describes the PAD-US dataset which is in the public domain." Free, no attribution
requirement, no account.

### 1.2 What actually downloads without a login - and what does not

This is the single most important operational fact about PAD-US, and it is not documented
anywhere on the USGS pages.

ScienceBase stores files two ways. The item JSON exposes this as `pathOnDisk`:

- `pathOnDisk: __disk__<hash>` -> served by `https://www.sciencebase.gov/catalog/file/get/...`
  **downloads freely.**
- `pathOnDisk: __s3__` -> only a `https://sciencebase.usgs.gov/manager/...` URL, which is a
  React app. I loaded it in a browser: it renders **"Sign in to ScienceBase"**, offering
  "Department of Interior Accounts" or login.gov, and states non-DOI users "must be
  sponsored by a USGS employee." **Login-walled.**

**Login-walled (all `__s3__`), confirmed:**

| File | Size |
|---|---|
| `PADUS4_1Geodatabase.zip` (full inventory, all 5 feature classes) | 1,523.4 MB |
| `PADUS4_1VectorAnalysis_PADUS_Only.zip` (standalone flattened) | 361.5 MB |
| `PADUS4_1VectorAnalysis_OtherExtents.zip` | 5,361.9 MB |
| **all 56 state/territory `PADUS4_1_State_XX_GDB_KMZ.zip` files** | 20-823 MB each |

Downloading with a browser User-Agent does not help; I tried. `curl` on the S3 bucket
(`prod-is-usgs-sb-prod-content.s3.amazonaws.com`) returns **403**, so the bucket needs a
signed URL.

**Free and direct, confirmed by actually downloading:**

| File | URL | Size |
|---|---|---|
| `PADUS4_1_Raster_CONUS.zip` | `https://www.sciencebase.gov/catalog/file/get/6759b67ed34edfeb8710a3db?f=__disk__c6%2F3a%2Fce%2Fc63aceb8653358a6d0438b141d86bc6fe4b51429` | **744,032,421 B** |
| `PADUS4_1_Raster_AK.zip` | same item, `?f=__disk__04%2F4a%2Fd3%2F044ad35d33f654ade579925b22f4c95af21d904d` | 151.5 MB |
| `PADUS4_1_Raster_HI.zip` | same item, `?f=__disk__b6%2Fb1%2Ff9%2Fb6b1f98d0cf5990ebdd323986e11c0065ea0fcd5` | **14,122,874 B** |
| Summary stats CSVs | item `6759b69fd34edfeb8710a3ea`, `?f=__disk__29%2F74%2F0b%2F29740bfde5519713b02c6190b07c47e965ce5d23` | **4,086,817 B** |

Item pages: raster `https://www.sciencebase.gov/catalog/item/6759b67ed34edfeb8710a3db`,
vector/stats `https://www.sciencebase.gov/catalog/item/6759b69fd34edfeb8710a3ea`.

### 1.3 The workaround that makes this all fine

**The freely-downloadable "Raster" zip also contains the flattened vector geodatabase.**

`PADUS4_1_Raster_CONUS.zip` (744 MB) contains `PADUS4_1VectorAnalysis_CONUS.gdb`. Extract
just that and skip the raster entirely:

```
unzip padus_conus.zip "PADUS4_1VectorAnalysis_CONUS.gdb/*" -d fv
```

Measured: **2.9 seconds, 423 MB on disk.** That is the same flattened product as the
login-walled 361 MB standalone file, for CONUS.

### 1.4 The flattened vector - and the trap in it

`PADUS4_1VectorAnalysis_CONUS.gdb`, layer `PADUS4_1_VectorAnalysis_CONUS`:

- **322,263 MultiPolygon features**
- CRS **`USA_Contiguous_Albers_Equal_Area_Conic` (NAD83)** - equal-area, so polygon area in
  m² is true area with no latitude correction. This is what makes the whole approach cheap.
- Fields include `Category`, `Pub_Access`, `GAP_Sts`, `GIS_Acres`, `Mang_Type`, `Des_Tp`,
  `Unit_Nm`, `IUCN_Cat`, `STUSPS`, `Shape_Area`
- Overlaps already resolved, prioritised by `GAP_Sts`

**THE TRAP.** 49 of the 322,263 records have `Category = ''` (empty) and `Pub_Access='UK'`.
These are **per-state "extent" background polygons covering all land, protected or not** -
they exist so USGS can compute percentages. The largest is **162,982,890 acres**. Summing
every polygon gives **2,000,695,199 acres**, which is roughly the entire land area of the
CONUS.

I hit this live. My first run returned 1,939,981 acres for Boulder, Bend, Des Moines *and*
Asheville - all four identical, and all equal to the area of the 50 km buffer itself
(1,940,566 acres). That is what a silent 100%-coverage bug looks like.

**Fix: filter `Category != ''` before anything else.** Drops exactly 49 records.

Distribution after the filter: Fee 223,929 / Easement 82,375 / Designation 10,322 /
Other 4,163 / Proclamation 1,394 / Unknown 31.

Note also `Category='Proclamation'` - national-forest *administrative* outer boundaries that
include private inholdings. Include or exclude deliberately; it is not land you can walk on.

### 1.5 The 50 km computation, measured

No ArcGIS needed. `pyogrio` + `shapely` + `pyproj` in a venv (none of GDAL, geopandas,
`ogrinfo` were installed on this machine - budget for `pip install pyogrio shapely pyproj`).

Recipe: read the layer, drop `Category==''`, build a `shapely.STRtree`, transform each
place's lat/lon into the file's Albers CRS with `pyproj`, buffer 50,000 m, `tree.query(buf,
predicate='intersects')`, `intersection()` the hits against the buffer, sum `area()/4046.8564224`.

Measured on this machine:

```
load + parse WKB + build STRtree ....... 51.6 s   (once)
per place ............................... 0.01 - 0.28 s
```

For 4,197 US places that is roughly **52 s + 5 minutes**. Entirely practical.

Real output (`ac` = acres of PAD-US land whose polygons intersect a 50 km radius, clipped
to the buffer; `%ofbuf` is share of the 1,940,566-acre disc):

| place | all PAD-US ac | open-access (`OA`) | GAP 1-2 | %ofbuf | polys | s |
|---|---|---|---|---|---|---|
| Boulder CO | 888,862 | 489,777 | 273,320 | 45.8% | 4,625 | 0.28 |
| Bend OR | 1,353,563 | 1,111,729 | 247,007 | 69.8% | 232 | 0.03 |
| Des Moines IA | 126,300 | 83,644 | 70,437 | 6.5% | 701 | 0.03 |
| Asheville NC | 557,360 | 323,657 | 207,418 | 28.7% | 537 | 0.16 |
| Miami FL | 516,701 | 288,296 | 279,505 | 26.6% | 1,634 | 0.06 |
| Lubbock TX | 5,092 | 2,823 | 732 | 0.3% | 142 | 0.01 |
| Burlington VT | 390,355 | 194,529 | 118,189 | 20.1% | 928 | 0.09 |

Bend 69.8% vs Lubbock 0.3% - a 230x spread. This discriminates well.

Recommendation: rank on the **`Pub_Access='OA'` (open access)** column, not the raw total.
"Open" is defined in the schema as requiring no special permit. That is the column that
actually means "land you can go hike on." `XA` (closed) includes military and some water
utility land and should not count as recreation.

### 1.6 Is there a pre-summarised table? Yes, but it does not join

`PADUS4_1SummaryStatistics_TabularData_CSV.zip.zip` (4,086,817 B, free) unzips to 11 CSVs
summarising by Congressional District, **County**, EPA Ecoregion III/IV, LCC, NA Ecoregion
I/II, National, Region, State, and Census Urban Areas.

The county file `PADUS4_1VectorAnalysis_Uni_Counties_Clip_CENSUS2022.csv` is 8.0 MB /
52,196 data rows, one row per county × `Pub_Access` × `GAP_Sts` × `IUCN_Cat` × manager.

**It carries no county FIPS.** The `BndryID` column - which should hold the code - contains
the **state name** ("Virginia", "Oregon"); only 58 distinct values across the whole file.
The county appears solely as a display string in `BndryName`: `"Roanoke County, VA"`.
Joining to your place->county FIPS map would need fuzzy name matching, which breaks on
Virginia's independent cities ("Roanoke County" vs "Roanoke city") and on Louisiana
parishes and Alaska boroughs.

Even if the key were clean, **county is the wrong geography** for "within reach". A town on
a county line has its nearest public land in the neighbouring county, and counties range
from 26 to 20,000 square miles. Use the buffer.

The Census Urban Areas file has the same shape and the same `BndryID` defect.

### 1.7 Why the raster is not the answer

Intuitively a 30 m raster in an equal-area projection is perfect: every cell is exactly
900 m², so a buffer sum needs no geometry work. The numbers kill it.

`PADUS4_1_Raster_CONUS.zip` is 744,032,421 B compressed and **80,975,251,972 B (81 GB)
uncompressed** across 76 files. From its central directory:

| member | uncompressed |
|---|---|
| `PADUS4_1_Raster_CONUS.ige` | 60,176,270,877 |
| `PADUS4_1_Raster_CONUS.rde` | 18,808,206,082 |
| `PADUS4_1_Raster_CONUS.rrd` | 1,262,097,172 |
| `PADUS4_1_Raster_CONUS.img.vat.dbf` | 286,787,178 |

Hawaii alone (14 MB zipped) expands to **8.1 GB**, its `.ige` being 6.06 GB - the bounding
box spans the NW Hawaiian Islands, so it is mostly nodata.

Format is ERDAS Imagine (`.img` + `.ige` spill file), not GeoTIFF. From the bundled
`RasterizationReport_PADUS4_1CONUS.txt`: 30 m cells, QGIS 3.34.13 Rasterize, `GAP_Sts` as
priority field, and **"There are: 15,211 records flagged with a value of 1 in the RastDrop
field ... these records were dropped from the raster because of conflicting overlaps."**

So the raster is 190x larger than the vector *and* has 15,211 fewer polygons. The vector
wins on every axis.

ScienceBase does not support HTTP range requests (it returned the full 744 MB body to a
`Range: bytes=0-100` header), so you cannot probe or partially fetch these.

### 1.8 The REST service, and why server-side stats lie

`https://services.arcgis.com/v01gqwM5QqNysAAi/arcgis/rest/services/PADUS_Public_Access/FeatureServer/0`

Live, no key, `supportsStatistics: true`, `maxRecordCount: 1000`, pagination supported,
`GIS_Acres` present. AGOL item `c91a5655a1be428daeb778888e60db24`, modified 2026-07-30,
described as "the current PAD-US Data". Sibling services: `PADUS_Protection_Status_by_GAP_Status_Code`,
`Fee_Managers_PADUS`.

Tempting, and wrong. A 100x100 km box around Boulder contains at most **2,471,054 acres of
anything**. A `groupByFieldsForStatistics=Pub_Access` sum returned:

```
OA 3,592,984   RA 567,066   UK 30,053   XA 2,220,305   =  6,410,408 acres
```

**2.6x the entire box.** Because `sum(GIS_Acres)` adds the *full* acreage of every polygon
that so much as clips the box - the largest single one in that query was **1,867,704
acres**. There is no server-side clip. You would have to pull geometry and clip locally,
at which point the local file is faster.

Useful for a **count** of protected units nearby, or as a spot-check. Not for area.

---

## 2. Canadian Protected and Conserved Areas Database (CPCAD)

Cleanest source in this document. Everything works.

- Landing: `https://open.canada.ca/data/en/dataset/6c343726-1e92-451a-876a-76e17d398a1c`
- Machine-readable: `https://open.canada.ca/data/api/action/package_show?id=6c343726-1e92-451a-876a-76e17d398a1c`
- **Licence: Open Government Licence - Canada** (`https://open.canada.ca/en/open-government-licence-canada`), from the CKAN API's `license_title`. Free, attribution only.
- Data current as of **2024-12-31**; catalogue record modified **2026-03-25**.

### 2.1 Download - the browse path does NOT serve the file

The CKAN record points at a *directory*:
`https://data-donnees.az.ec.gc.ca/data/species/protectrestore/canadian-protected-conserved-areas-database/Databases`

That is a JS single-page app. Requesting the obvious file path under it returns a **2,200-byte
HTML shell with `Content-Type: text/html`** - for *any* filename, including ones I invented,
so you cannot probe for existence there either. `HEAD` is useless across this whole host.

The real endpoints, recovered from the SPA bundle and confirmed by reading the rendered
anchors in a browser:

- Directory listing: `https://data-donnees.az.ec.gc.ca/api/path_contents?path=<urlencoded path>`
- **File download: `https://data-donnees.az.ec.gc.ca/api/file?path=<urlencoded path>`** (302s to the blob; needs `-L`. It 404s on `HEAD` - use `GET`.)

Listing returns exactly two files, both dated 2026-03-25:

| File | Reported |
|---|---|
| `ProtectedConservedArea_2025.zip` (EN) | 126 MiB |
| `AireProtégéeConservée_2025.zip` (FR) | 127 MiB |

**Working URL, downloaded and verified:**

```
https://data-donnees.az.ec.gc.ca/api/file?path=%2Fspecies%2Fprotectrestore%2Fcanadian-protected-conserved-areas-database%2FDatabases%2FProtectedConservedArea_2025.zip
```

**132,159,054 bytes**, real zip, 64 entries, 155 MB uncompressed. Contains
`ProtectedConservedArea_2025.gdb` (147 MB), a data-dictionary XLSX, a user manual PDF and
the FGDC XML.

Minor gotcha: the French filename's accents make `unzip` throw a bogus "write error (disk
full?)" on some systems. Extract just the layer: `unzip cpcad.zip "ProtectedConservedArea_2025.gdb/*"`.

### 2.2 Structure

Three layers. The one you want is `ProtectedConservedArea_2025`:

- **22,438 MultiPolygon features**
- CRS **`Canada_Albers_Equal_Area_Conic` (NAD83)** - equal-area again, same cheap maths as PAD-US
- `BIOME`: **T (terrestrial) 21,509 / M (marine) 929**
- Fields: `NAME_E`, `IUCN_CAT`, `TYPE_E`, `O_AREA_HA`, `OWNER_TYPE`, `GOV_TYPE`, `MGMT_E`,
  `PA_OECM_DF`, `IPCA`, `STATUS`, `ESTYEAR`, `Shape_Area`, plus a separate
  `ProtectedConservedAreaDelisted_2025` layer for removed sites.

**Filter `BIOME='T'`.** The 929 marine polygons are enormous and would put Halifax and
Vancouver at the top of a *hiking* ranking on the strength of ocean.

There is no `Pub_Access` equivalent - CPCAD has no public-access field at all. `IUCN_CAT`
and `TYPE_E` are the closest proxies. That is a genuine asymmetry against PAD-US; do not
present a US "open access acres" number and a Canadian "all protected acres" number as the
same metric.

### 2.3 The 50 km computation, measured

Identical recipe to PAD-US. Much faster because the file is smaller:

```
load + parse + STRtree ......... 2.6 s   (once)
per place ...................... 0.01 - 0.13 s
```

710 CSDs run in well under a minute total.

| place | terrestrial ac in 50 km | %ofbuf | polys | s |
|---|---|---|---|---|
| Canmore AB | 1,302,279 | 67.1% | 16 | 0.02 |
| Mont-Tremblant QC | 318,823 | 16.4% | 106 | 0.01 |
| Vancouver BC | 240,285 | 12.4% | 461 | 0.13 |
| Halifax NS | 168,314 | 8.7% | 314 | 0.04 |
| Toronto ON | 48,355 | 2.5% | 194 | 0.02 |
| Regina SK | 38,206 | 2.0% | 50 | 0.02 |

Canmore (Banff/Kananaskis) at 67% vs Regina at 2%. Behaves exactly as it should.

### 2.4 REST alternative

`https://maps-cartes.ec.gc.ca/arcgis/rest/services/CWS_SCF/CPCAD/MapServer/0`
(French mirror at `.../BDCAPC/MapServer/0`; WMS also published.)

`supportsStatistics: true`, `maxRecordCount: 25000`, supports GeoJSON and PBF, native SR
EPSG:3978. A live query of a 50 km envelope around Vancouver returned **812 features** with
`exceededTransferLimit: null` - comfortably inside the limit.

Good fallback and good for spot-checks. But `sum(O_AREA_HA)` has the **same over-count flaw
as PAD-US** - my Vancouver query summed 3,291,540 ha of official area for polygons merely
*touching* the box. Pull geometry and clip locally, or just use the file.

### 2.5 Pre-summarised table?

**No usable one.** ECCC publishes a `Statistics` directory but it is **PDF only**. There is
no CSD-level or municipality-level protected-area table anywhere in CPCAD. The buffer
computation is the only route, which is fine given it runs in seconds.

---

## 3. Ski areas

### 3.1 OpenSkiMap - USABLE, and the recommendation

`https://tiles.openskimap.org/csv/ski_areas.csv`

- **3,272,486 bytes**, `Last-Modified: Thu, 20 Aug 2026 23:14:34 GMT` - rebuilt within a day of checking
- **12,213 rows worldwide**, one row per ski area
- Columns: `name, countries, regions, localities, status, has_downhill, has_nordic,
  downhill_distance_km, nordic_distance_km, vertical_m, min_elevation_m, max_elevation_m,
  lift_count, surface_lifts_count, run_convention, wikidata_id, websites, openskimap, id,
  geometry, lat, lng, sources`
- Companion files at the same host: `geojson/ski_areas.geojson` (21.8 MB, with polygons),
  `geojson/lifts.geojson`, `geojson/runs.geojson`, and `openskidata.gpkg` (407 MB)
- **Licence: ODbL** - OSM-derived. Attribution + share-alike.

**Counts I computed myself from the file.** Filter `status='operating'` AND
`has_downhill='yes'` AND non-empty `name`:

| filter | US | CA |
|---|---|---|
| rows mentioning the country | 1,948 | 829 |
| operating + downhill + named | 595 | 284 |
| **+ at least 1 mapped lift (recommended)** | **525** | **235** |
| + ≥2 lifts | 450 | 194 |
| + ≥4 lifts (destination resorts) | 338 | 102 |

Field completeness on the recommended US set (n=525): **lat/lng 525/525, vertical_m
525/525**, downhill_distance_km 486, website 491. Canada (n=235): lat/lng 235/235,
vertical_m 235/235, downhill_distance_km 226.

Note `has_downhill` takes `yes`/`no`, **not** `true`/`false` - filtering on `'true'` silently
returns zero rows. I made that mistake first.

`status` values across the file: operating 10,873 / abandoned 1,058 / empty 198 /
proposed 52 / never_opened 27 / disused 5. So the operating filter is meaningful and the
dataset does track closures.

**No skiable-acres field exists.** Use `lift_count` and `vertical_m` (both 100% populated)
as the size proxy. Polygon area from the GeoJSON is not a substitute - resort boundaries
include non-skiable terrain.

### 3.2 NSAA - benchmark only

`https://nsaa.org/webdocs/Media_Public/IndustryStats/ski_areas_per_season_2025.pdf`
(161,673 B, free, no login). I extracted the text. Verbatim:

> "reports 492 ski areas in operation across 37 states during the 2024/25 season, according
> to the Kottke National End-of-Season Survey"

It also carries the 1992-2025 series (2023/24: 486, 2013/14: 470, 1997/98: 521).

**Aggregate only - no per-area rows, no coordinates.** The members directory is
login-walled and NSAA states it does not release per-area data. A companion free PDF
`ski_areas_by_state_2025.pdf` gives per-state counts.

Use it as the sanity check: OpenSkiMap's 525 is **+6.7%** against NSAA's 492, which is the
expected direction - OSM maps small community and muncipal hills that the Kottke operator
survey does not cover.

### 3.3 Raw OSM via Overpass - workable but messier

Counts I ran myself against `https://overpass-api.de/api/interpreter`:

| query | result | time |
|---|---|---|
| `landuse=winter_sports` ways+relations, CONUS bbox | **721** (659 w + 62 r) | 3.0 s |
| same, Canada bbox | **611** (568 w + 43 r) | ~4 s |
| same, Alaska bbox | **17** (16 w + 1 r) | ~5 s |
| `aerialway=chair_lift` ways, CONUS | **2,432** | 3.8 s |
| `aerialway=chair_lift` ways, Canada | **1,613** | 77.4 s |
| `aerialway=chair_lift` ways, Alaska | **20** | 75.8 s |

`out center tags` on the CONUS set returned 210,223 bytes in 86 s: **721 polygons, 690
named, 721 with centroids**, 319 with a website, 123 with a wikidata id.

Two real problems, both of which OpenSkiMap has already solved for you:

1. **Bounding boxes leak across the border.** My "CONUS" bbox picked up *Earl Bales Park
   Ski and Snowboard Centre* at 43.75, -79.43 - that is Toronto. You would need a
   point-in-polygon test against a country boundary.
2. **`landuse=winter_sports` is not "ski resort".** The same tag covers Nordic centres,
   tubing hills and municipal rope-tow hills. "Active Backwoods Retreat Ski Trails" is
   cross-country. There is no clean operating-downhill-resort filter without also joining
   lifts and runs - which is exactly the work OpenSkiMap does nightly.

Go with OpenSkiMap. One 3.3 MB request beats rebuilding this.

### 3.4 Canadian associations - NOT USABLE

Per the ski-areas research pass: `https://cwsaa.org/members/` **redirects to
`https://cwsaa.org/login/`**. The public `cwsaa-members` page lists names grouped by
division with no coordinates, and states the detailed directory requires login. It is also
western-Canada only, missing Quebec and Ontario, which between them hold most Canadian
areas. `https://www.skicanada.org/ski-areas/` is name lists with zero coordinates.

---

## 4. Trails

Answer to the direct question: **yes, several national US trail datasets exist with mileage
as a real attribute** - and yes, OSM trail length is obtainable from Overpass geometry.

### 4.1 USGS National Transportation Dataset - best coverage

TNM publishes trails inside the NTD as layer **`Trans_TrailSegment`**.

- API: `https://tnmaccess.nationalmap.gov/api/v1/products?datasets=National%20Transportation%20Dataset%20(NTD)&max=200&outputFormat=JSON` -> **170 items = 57 extents x 3 formats** (FileGDB / GeoPackage / Shapefile), all published 2026-02-11
- National GeoPackage `https://prd-tnm.s3.amazonaws.com/StagedProducts/Tran/National/GPKG/Transportation_National_GPKG.zip` - API-reported **13,487,927,460 B (13.5 GB)**
- **Per-state, much better**: `https://prd-tnm.s3.amazonaws.com/StagedProducts/Tran/GPKG/TRAN_{State}_State_GPKG.zip`
- Licence: ScienceBase `rights: None`. Free, no login.

I downloaded three state files and read them with sqlite3 (a GeoPackage is a SQLite DB, so
this needs no GDAL at all):

| state | zip | segments | `sum(lengthmiles)` | nulls |
|---|---|---|---|---|
| District of Columbia | 5,819,052 B | 2,096 | 257.6 | 0 |
| Vermont | 59,016,374 B | 18,544 | **8,495.0** | 0 |
| Rhode Island | 22,273,389 B | **105** | **32.5** | 0 |

**`lengthmiles` (REAL) is a genuine attribute with zero nulls.** Other columns: `name`,
`trailtype`, `trailsurface`, `hikerpedestrian`, `bicycle`, `nationaltraildesignation`,
`networklength`, `primarytrailmaintainer`. SRS **EPSG:4269**, so it joins straight to TIGER
place polygons.

**The catch, and it is a big one: coverage is state-dependent.** Vermont has 8,495 miles.
Rhode Island, its New England neighbour, has **32.5** - a 260x gap that reflects whether the
state GIS agency contributed data, not whether the state has trails. **Audit every state's
total before ranking, and treat near-zero states as missing data rather than as zero
trails**, or you will rank Rhode Island towns bottom for a reason that is not real.

Also: do **not** use the `bicycle` column as a bike-infrastructure signal. It is
overwhelmingly "Undefined".

### 4.2 USFS National Forest System Trails - best mileage quality

- File GDB `https://data.fs.usda.gov/geodata/edw/edw_resources/fc/Trans_Trail_NFS_Publish.gdb.zip` -> **200, 118,461,776 B, Last-Modified Mon 17 Aug 2026**
- Shapefile `https://data.fs.usda.gov/geodata/edw/edw_resources/shp/Trans_Trail_NFS_Publish.zip` -> **200, 245,832,165 B**
- Clearinghouse: `https://data.fs.usda.gov/geodata/edw/datasets.php`
- REST: `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0`

**`SEGMENT_LENGTH` (double) is the mileage attribute.** A stats query I ran against the REST
service returned exactly:

```
{"mi":163204.613,"n":86303}
```

**86,303 segments, 163,204.613 miles, zero nulls.** Metadata defines it as "The length of
the trail or trail segment in miles. Calculated as EMP - BMP". Licence `<accconst>None</accconst>`.

Also carries `HIKER_PEDESTRIAN_MANAGED`, `BICYCLE_MANAGED`, `TRAIL_SURFACE`,
`NATIONAL_TRAIL_DESIGNATION`.

Two limits: **National Forest System land only**, and there is no state or place field -
only `ADMIN_ORG`, a 6-digit region/forest/district code. Since NFS trail mostly sits
*outside* incorporated places, use a radius join from each place, not point-in-polygon.
Prefer the `.gdb`; the shapefile truncates field names to 10 chars (`SEGMENT_LE`).

### 4.3 NPS - no length attribute

- `https://mapservices.nps.gov/arcgis/rest/services/NationalDatasets/NPS_Public_Trails_Geographic/FeatureServer/0` -> I queried it: **31,358 features**
- Bulk shapefile `https://public-nps.opendata.arcgis.com/api/download/v1/items/839d48f9ee7047509d7ea9868819c978/shapefile?layers=0` -> 302 then **200, application/zip, ~45.5 MB**

**No mileage field** - only `Shape__Length`, which on the Geographic service is in decimal
degrees. You must compute geodesic length yourself. Fields: `TRLNAME`, `TRLTYPE`, `TRLUSE`,
`TRLSURFACE`, `UNITCODE`, `UNITNAME`.

### 4.4 BLM - small, western only

`https://gis.blm.gov/arcgis/rest/services/transportation/BLM_Natl_GTLF_Public_Display/MapServer`
layer 7 "Trails Managed for Public": 19,587 features, `SUM(GIS_MILES)` **7,842.633**.
`GIS_MILES` and `BLM_MILES` are real attributes and `ADMIN_ST` gives you a free state join.
Only 11-12 western states (CO 2,957 mi, AK 1,094, ID 1,016 ... NM 27, WY 19; OR null).
Too small to move a national ranking.

### 4.5 OSM trails via Overpass - yes, length works

**Direct answer: yes.** `out geom;` returns the full node list for every way, and summing
haversine distances between consecutive nodes gives you mileage. I did it end to end.

Measured against `https://overpass-api.de/api/interpreter`, query shape
`way["highway"="path"](bbox); out geom;`:

| state bbox | response | time | ways | computed miles |
|---|---|---|---|---|
| Vermont | **39.9 MB** | **8.6 s** | 19,929 | **6,242** |
| California | **299.6 MB** | **159.1 s** | 122,183 | **40,760** |

So budget roughly **40 MB / 9 s for a small state and 300 MB / 2.7 min for the largest**.
A 50-state sweep of one tag is on the order of 3-4 GB of transfer. That is fine overnight,
painful interactively. `highway=footway`, `highway=bridleway` and `route=hiking` would each
need their own pass.

**Two operational notes that match your existing experience:**

1. `https://overpass-api.de/api/status` reports **`Rate limit: 2`** - only two concurrent
   slots per IP. I exceeded it and got a hard **HTTP 429**, and separately the classic
   `runtime error: ... Dispatcher_Client::request_read_and_idx::timeout. The server is
   probably too busy`. **Run strictly serially.** Your regex-alternation 504s are the same
   resource ceiling from the other direction: one exact-match tag per query, one query at a
   time.
2. The `kumi.systems` mirror returned empty bodies and `Internal Server Error` throughout my
   testing on 2026-08-21. Do not plan a fallback on it without re-testing.

If you would rather not hammer Overpass, **Geofabrik** ships the same data as extracts:
`https://download.geofabrik.de/north-america/us-latest.osm.pbf` -> 302 to `us-260820.osm.pbf`,
**12,095,659,298 B (12.1 GB)**, Last-Modified 2026-08-20, refreshed daily; 53 per-state
sub-extracts at `https://download.geofabrik.de/north-america/us.html`. ODbL.

### 4.6 Recreation.gov / RIDB - not for mileage

Bulk export `https://ridb.recreation.gov/downloads/RIDBFullExport_V1_CSV.zip` is free and
needs no key (**246,248,095 B**, 21 CSVs; the JSON API itself returns **401** without a key).
`Facilities_API_v1.csv` has ~109,199 rows with lat/lon and HIKING activity codes. **No trail
mileage anywhere in it.** Usable only as a recreation-facility density proxy.

---

## 5. Bicycling infrastructure

**Direct answer to the question: no, there is no national US dataset of bike-lane mileage.
OSM is effectively the only route to actual bike-lane geometry.** Checked and empty:

- **BTS National Transportation Atlas Database.** `https://geodata.bts.gov/api/feed/dcat-us/1.1.json`
  lists **142 datasets**; searching bike/bicycle/pedestrian/nonmotorized/bikeway/greenway
  returns exactly two, **"Bikeshare"** and **"Bikeshare Scooter Systems"**. There is no
  bikeway layer in NTAD at all. The bikeshare CSV (16.9 MB, ~78,380 rows) is a station-year
  panel with lat/lon - a bikeshare-presence proxy only.
- **FHWA Highway Statistics** (`https://www.fhwa.dot.gov/policyinformation/statistics.cfm`) -
  motor fuel, registrations, licences, highway mileage, travel, finance. No bicycle or
  nonmotorized mileage table at any level.
- **Census** publishes no bikeway mileage at any geography. Only ACS commute mode share,
  which you already have as `commute_bike_pct`.

### 5.1 PeopleForBikes City Ratings 2026 - USABLE, with an important caveat

`https://cityratings.peopleforbikes.org/data/2026/all-pfb-cr-results-2026.csv`

- **849,288 bytes**, `text/csv`, **3,019 data rows, all United States**. Free, no account.
- Historical scores 2020-2026: `.../all-pfb-cr-historical-results-2026.csv` (93,760 B)

**It joins straight to your place GEOIDs**, which is what makes it worth using. I verified
the key myself:

- `census_fips_code` filled **3,019/3,019**
- lengths: **7 chars on 2,365 rows, 6 chars on 654 rows** - the leading zero is stripped for
  single-digit state FIPS. **Zero-pad to 7.** (Crested Butte CO ships as `818310`, needs
  `0818310`.)
- after padding: **3,014 unique GEOIDs**, with 5 duplicate pairs (alias rows) to dedupe
- `census_latitude` / `census_longitude` also 3,019/3,019

**The caveat that matters: its mileage columns are not bike-lane mileage.**
`total_low_stress_miles` (2,997/3,019 filled) and `total_high_stress_miles` (3,015/3,019)
are the *total road and path network* classified by traffic stress. A quiet residential
street with no bike infrastructure of any kind counts as low-stress. It is a rideability
measure, not an infrastructure inventory - which is arguably better for your purpose, but
do not label it "bike lane miles".

Also useful: `overall_score` (0-100, 3,019/3,019), `recreation_trails`, `recreation_parks`,
`transit`, `residential_speed_limit`. Note `recreation_trails` is only ~1,218/3,019 filled.

Coverage ceiling: **3,014 of your 4,197 places, about 72%.** New York City appears as
boroughs, with no "New York, NY" row.

**Licence: unstated.** No terms or licence page was located on the site. Upstream inputs are
OSM via Geofabrik (ODbL) plus TIGER/Line, so ODbL share-alike may flow through. Attribute
PeopleForBikes and treat the licence as unconfirmed.

### 5.2 League of American Bicyclists - thin

The Bicycle Friendly Community list is **448 records** with lat/lon on 441, award tier
(Bronze 299 / Silver 113 / Gold 32 / Platinum 3), population and area - but **no mileage
field of any kind**, no FIPS, and no published CSV. It is served from a WordPress
admin-ajax endpoint requiring a per-page scraped nonce, so it is brittle. 448 of 4,197
places, binary tier signal.

### 5.3 Canada

**Nothing equivalent exists.** No PeopleForBikes coverage (the file is 100% US), no national
bikeway inventory from StatCan or Transport Canada. For the 710 CSDs, OSM `highway=cycleway`
is the only option, with the same Overpass cost profile as section 4.5.

---

## Recommended stack

| dimension | US | Canada |
|---|---|---|
| Public land within 50 km | PAD-US 4.1 flattened vector, `Category != ''`, rank on `Pub_Access='OA'` | CPCAD 2025, `BIOME='T'` |
| Skiing | OpenSkiMap CSV, drive-time to nearest of the 525 | same file, 235 areas |
| Trail mileage | TNM `Trans_TrailSegment` `lengthmiles`, per-state GPKG, + USFS radius join | OSM Overpass only |
| Bicycling | PeopleForBikes `overall_score` (72% coverage), ACS `commute_bike_pct` elsewhere | ACS-equivalent only |

Two notes on method:

**Use your drive-time engine for skiing, not straight-line distance.** Ski areas are in
mountains and mountain roads are slow; 40 km of switchbacks is an hour. You have the engine,
and this is the dimension where it pays off most. The 760 North American areas mean 4,197 x
nearest-few lookups, which is tractable.

**Keep the US and Canadian protected-land numbers as separate normalised ranks, not one
pooled scale.** PAD-US has a public-access field and CPCAD does not, PAD-US includes
Proclamation boundaries and CPCAD has no equivalent, and the two are compiled to different
standards. Percentile within country is defensible; a shared absolute acreage scale is not.

---

## Could not confirm

Listed explicitly rather than glossed. None of these block the build.

1. **PAD-US full-inventory geodatabase and state files** - I confirmed the ScienceBase
   sign-in page appears, but I did **not** create an account, so I cannot confirm whether a
   free login.gov account is actually sufficient to download them, or whether DOI
   sponsorship is genuinely required for these public-domain files. The workaround in 1.3
   makes this moot for CONUS.
2. **PAD-US Alaska and Hawaii flattened vectors** - I proved the pattern end to end for
   CONUS by extracting and reading `PADUS4_1VectorAnalysis_CONUS.gdb`. For **Hawaii** I
   downloaded the zip and confirmed `PADUS4_1VectorAnalysis_HI.gdb/` is present in its
   listing, but did not extract or read the layer. For **Alaska** (151.5 MB) I did not
   download the zip at all, so the presence of `PADUS4_1VectorAnalysis_AK.gdb` inside it is
   inferred from the CONUS/HI pattern, not observed. Verify before relying on it.
3. **Exact PAD-US version behind the ArcGIS FeatureServer** - the item says "the current
   PAD-US Data" and was modified 2026-07-30, which is *after* 4.1's March 2025 release. It
   may carry interim updates that differ from the 4.1 files. I could not pin a version
   string on it.
4. **PeopleForBikes licence** - no licence, terms or copyright page was found on
   cityratings.peopleforbikes.org. Treat as unstated, not as permissive.
5. **NSAA per-state PDF** - I verified the national figure (492 areas, 37 states, 2024/25)
   by extracting text from the PDF myself. I did **not** separately open the by-state PDF;
   the state breakdown quoted in the ski research pass is second-hand.
6. **CWSAA and Canadian Ski Council login walls** - reported from the ski research pass, not
   re-fetched by me directly.
7. **Overpass mirrors** - `overpass.kumi.systems` failed for me on 2026-08-21 (empty bodies,
   500s). That may be a transient outage rather than a permanent state; re-test before
   writing it off.
8. **TNM state coverage beyond DC, VT and RI** - I measured three states. The Rhode Island
   hole is real and I confirmed it, but I have **not** audited the other 53 extents. Do that
   before the ranking goes live.
9. **CPCAD `.gdb` vs REST parity** - I read the geodatabase (22,438 features) and separately
   queried the REST service (812 features near Vancouver). I did not reconcile the two
   against each other feature-for-feature.
10. **Canada `landuse=winter_sports` "out center" pull** - I have the count (611) but the
    detailed centroid/name pull for Canada and Alaska did not complete before I moved on.
    OpenSkiMap supersedes it anyway.
