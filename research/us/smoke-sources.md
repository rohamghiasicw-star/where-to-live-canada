# US wildfire smoke data for Livable

Research date: 2026-07-29. Every URL below was opened during this run. Every number in the
validation section was computed from the downloaded files, not quoted from memory or a search
snippet. Where a page refused a scripted fetch, that is stated.

The Canadian side of this app already learned the lesson the hard way: ECCC's "days with smoke
or haze" normal looks like the answer and is anti-correlated with real wildfire smoke
(Pearson -0.22), because it counts any visibility obstruction, mostly summer humidity haze. See
`research/smoke-data.md`. Canada ships ECCC FireWork Cumulative Effects instead: the air quality
model run with fires differenced against the run without, so the smoke is isolated from traffic
and wood stoves. 0.05 ug/m3 (St. John's) to 2.82 (Kamloops).

**The US has the same trap wearing a different mask, and it is EPA monitor data.**

---

## PART 1: The US trap. Total PM2.5 is not wildfire smoke. Verdict: DO NOT USE IT.

EPA AQS and AirNow publish measured PM2.5 in ug/m3, nationwide, hourly, back decades, with a
clean API. It is the obvious pick and it is the wrong one, for exactly one reason: a monitor
weighs particles, it does not ask where they came from.

Orr et al. 2025, a state-of-the-science review of wildfire-specific PM2.5 data
(Environmental Health Perspectives 133(6) 066001, doi:10.1289/EHP15672,
PDF: https://www.fs.usda.gov/rm/pubs_journals/2025/rmrs_2025_orr_a001.pdf), verbatim:

> "Ground-based monitors, like the EPA stations in the US, are commonly relied upon for
> measuring PM2.5 levels during wildfire occurrences. However, a significant limitation of these
> monitors is their inability to inherently distinguish between PM2.5 originating from wildfires
> and that from other sources, as they only measure the total PM2.5 mass concentrations."

Same review, on how small the fire share actually is: the three public wildfire-specific
datasets it compared put wildfire PM2.5 at "11.2%-36.9% of total PM2.5 in 2010 and 13.7%-21.2%
in 2018" in California, the smokiest state in the country. So 4 parts in 5 of a California
monitor reading is not fire, and in Ohio or Los Angeles the fire share is smaller still.

### I ran the same correlation the Canadian side ran, on US data

EPA AQS annual summaries, downloaded (real files, HTTP 200, ~4.5 MB each):

```
https://aqs.epa.gov/aqsweb/airdata/annual_conc_by_monitor_2016.zip
https://aqs.epa.gov/aqsweb/airdata/annual_conc_by_monitor_2018.zip
https://aqs.epa.gov/aqsweb/airdata/annual_conc_by_monitor_2020.zip
```

Parameter 88101 (PM2.5 local conditions), Metric Used "Daily Mean", Pollutant Standard
"PM25 24-hour 2012", event types "No Events" or "Events Included" so wildfire days stay in,
>=100 observations, sites present in all three years. Total PM2.5 per site = mean of the three
annual arithmetic means. Fire-attributed smoke per site = the surface built in Part 2, sampled
at the monitor's own lat/lon.

(One trap inside the trap: pairing Metric Used "Daily Mean" with Pollutant Standard
"PM25 Annual 2012" matches **zero** rows, because the annual standard is reported as "Quarterly
Means of Daily Means". A filter that looks right and silently returns an empty set.)

649 monitor sites qualified.

```
Pearson  r  (total PM2.5 vs fire-attributed smoke PM2.5) = +0.316
Spearman rank r                                          = +0.204
```

Not backwards the way Canada's element 87 was backwards, and in one respect that is worse: an
inverted field announces itself, plausible-looking noise does not. r = 0.32 means total PM2.5
explains about **10%** of the variation in wildfire smoke. Nine parts in ten of what you would be
ranking on is something else. And the two rankings share almost nothing:

| Top by TOTAL PM2.5 | total | smoke |
|---|---|---|
| Bakersfield CA | 18.74 | 0.72 |
| Hanford CA | 17.75 | 0.96 |
| Visalia CA | 17.21 | 1.00 |
| Corcoran CA | 17.00 | 0.92 |
| **Ontario CA** | **16.73** | **0.26** |
| Fresno CA | 16.38 | 0.99 |

| Top by FIRE-ATTRIBUTED smoke | total | smoke |
|---|---|---|
| **Hamilton MT** | **7.01** | **2.12** |
| Lemhi ID | 10.72 | 1.98 |
| Klamath Falls OR | 14.72 | 1.85 |
| Red Bluff CA | 9.55 | 1.78 |
| Chico CA | 12.48 | 1.73 |
| Missoula MT | 7.64 | 1.57 |

Read the two bolded rows together. **Ontario, California has 2.4x the total PM2.5 of Hamilton,
Montana and 12% of the wildfire smoke.** Ontario is in the LA basin: freeways, warehouses, port
drayage. Hamilton is in the Bitterroot Valley, which fills with smoke every August. Total PM2.5
puts Ontario first and Hamilton nowhere.

By state, monitor means:

| | total PM2.5 | smoke PM2.5 | sites |
|---|---|---|---|
| California | 10.90 | 0.66 | 93 |
| Pennsylvania | 8.79 | **0.26** | 38 |
| Indiana | 8.62 | 0.42 | 29 |
| Idaho | 8.61 | **1.21** | 6 |
| Montana | **6.61** | **1.17** | 13 |
| North Dakota | 4.63 | 0.65 | 7 |

Pennsylvania carries **33% more total PM2.5 than Montana and 22% of the wildfire smoke.**

That is the whole argument in one table. Shipping total PM2.5 would tell a family in Fresno or
Cleveland that they live in the smokiest air in America and tell a family in the Idaho panhandle
that theirs is clean. Backwards, for the same structural reason element 87 was backwards in
Canada.

**Verdict: EPA AQS / AirNow total PM2.5 is rejected as a wildfire smoke measure.** It is a fine
measure of *air pollution*, which is a different dimension and a different question.

---

## PART 2: What is shipped. Childs et al. 2022 daily 10 km smoke PM2.5.

This is the direct US analogue of FireWork CE, and it is what the build uses.

- **Paper:** Childs, M.L., Li, J., Wen, J., Heft-Neal, S., Driscoll, A., Wang, S., Gould, C.F.,
  Qiu, M., Burney, J., Burke, M. (2022). "Daily Local-Level Estimates of Ambient Wildfire Smoke
  PM2.5 for the Contiguous US." *Environmental Science & Technology* 56(19): 13607-13621.
  doi:10.1021/acs.est.2c02934, PMID 36134580.
  - Abstract, opened: https://pubmed.ncbi.nlm.nih.gov/36134580/
  - Full text PDF, opened and text-extracted: https://web.stanford.edu/~mburke/papers/ChildsEtAl2022_smoke.pdf
  - The publisher page https://pubs.acs.org/doi/10.1021/acs.est.2c02934 returns **HTTP 403** to
    scripted fetches. The author-hosted PDF above and PubMed served, and both are the same paper.
- **Lab page listing versions and downloads, opened:** https://www.stanfordecholab.com/wildfire_smoke
- **Code repo and data documentation, opened:** https://github.com/echolab-stanford/daily-10km-smokePM
- **Data, downloaded:** Harvard Dataverse doi:10.7910/DVN/DJVMTV, version 1.0, published
  2024-02-26, licence **CC BY-SA 4.0**, depositor Marissa Childs.
  Landing page https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DJVMTV is
  a JavaScript app and returns nothing useful to a scripted fetch. The API does:

```bash
# file manifest, licence, citation
curl "https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/DJVMTV"

# the files actually used
curl -L "https://dataverse.harvard.edu/api/access/datafile/8550337" -o smokePM_10km_20060101-20201231.csv  # 1,778,985,211 B
curl -L "https://dataverse.harvard.edu/api/access/datafile/8550317" -o grid.shp   # 13,621,316 B
curl -L "https://dataverse.harvard.edu/api/access/datafile/8550318" -o grid.shx   #    801,348 B
curl -L "https://dataverse.harvard.edu/api/access/datafile/8550315" -o grid.dbf   #  5,809,178 B
curl -L "https://dataverse.harvard.edu/api/access/datafile/8550346" -o README.txt #     10,743 B
```

All five returned HTTP 200 at exactly the advertised byte counts. Range requests work
(HTTP 206), so the 1.78 GB file resumes with `curl -C -`. No auth, no key, no GDAL.

### What it measures, and why it is not total PM2.5

From the paper, Figure 1a caption, verbatim:

> "Total fine particulate matter (PM2.5, black line) is observed at ground monitors. Plumes and
> trajectories from fires are used to identify smoke days (gray points). Non-smoke median PM2.5
> (blue dashed line) is the station- and month-specific median of PM2.5 on non-smoke days, and
> smoke PM2.5 (red line) is total PM2.5 above the non-smoke median on days with smoke overhead."

So the quantity is an **anomaly above each station's own non-fire seasonal baseline, on days a
fire plume is overhead**. Traffic, industry and wood stoves sit in the baseline and are
differenced out, which is the same trick FireWork CE performs with a counterfactual model run.
Smoke days themselves come from NOAA HMS smoke plume polygons plus HYSPLIT trajectories,
verbatim:

> "Smoke days (top layer) are defined based on the presence of smoke plumes (light gray areas) or
> the presence of 50 HYSPLIT trajectory points below 1.1 km and AOD missingness over 75%"

A gradient-boosted model then predicts that anomaly on a 10 km grid from satellite AOD, fire
cluster variables, HYSPLIT features, land cover, elevation and reanalysis meteorology. Top
features by gain, verbatim: "Predicted AOD contributed most to model performance, followed by
longitude, size of the nearest fire cluster, and dewpoint temperature."

### Specification, as obtained

| | |
|---|---|
| Variable | wildfire smoke PM2.5, **ug/m3** (fire-attributed, not total) |
| Years | **2006-01-01 to 2020-12-31**, 15 complete years, 5,479 days |
| Temporal resolution | daily |
| Spatial resolution | **10 km x 10 km**, 100,156 cells |
| Spatial coverage | **contiguous US only.** Grid centroid extent lon -124.925 to -66.848, lat 24.497 to 49.450. No Alaska, no Hawaii, no Puerto Rico |
| Format | CSV, columns `grid_id_10km, date, smokePM_pred`; `ID` in the grid shapefile joins to `grid_id_10km` |
| Projection | grid shipped in WGS84 (`GEOGCS["GCS_WGS_1984"...]`), so no reprojection needed. The `.dbf` also carries `COORDX`/`COORDY` on a 10,000 m spacing, confirming true 10 km cells |
| Validation | spatial out-of-sample **R2 = 0.67**, "within" R2 = 0.65, median per-monitor R2 = 0.63 with 90% between 0.21 and 0.88, and R2 = 0.70 against PurpleAir monitors never used in training |
| Licence | CC BY-SA 4.0 |

### The one gotcha in the file, and it is a big one

`README.txt` from the Dataverse record, verbatim:

> "All rows in this file are predictions on smoke days. Predictions on non-smoke days are by
> construction 0 ug/m^3 and not included in this file. A smoke PM2.5 prediction of 0 in this file
> means that the grid cell-day did have a smoke day but did not have elevated PM2.5."

Miss that and you compute the mean over the wrong denominator. Averaging the rows that exist
gives you "average smoke PM2.5 *on smoke days*", which rewards places that rarely see a plume,
and Florida would beat Idaho. The correct annual mean divides the total by **all 5,479 days**,
which is what `src/us/build_smoke.py` does, and which is the same construct as FireWork CE's
"Yearly average of wildfire contribution: surface PM2.5 [ug/m3]".

### What the build does

`src/us/build_smoke.py`, run end to end for this file:

1. Downloads the six Dataverse files (byte-count checked against the API manifest).
2. Parses the 10 km grid shapefile with `struct`, no GDAL. Cell centroid = mean of the four
   corners, because a 10 km square in the source projection is a slightly rotated quadrilateral
   in WGS84.
3. Streams the 1.78 GB CSV and sums `smokePM_pred` per cell. **51,434,138 rows.** Cross-checks:
   smoke mass landing on grid IDs that are absent from the shapefile is `-6e-08` out of `2.93e+08`,
   i.e. every row joins; and 0 of 100,156 cells are missing from the CSV entirely, so no cell
   needs a "never saw a plume" assumption.
4. Divides by 5,479 days.
5. Resamples to a regular 0.1 degree lat/lon grid by nearest source centroid, with a hard 7.1 km
   cutoff (the half-diagonal of a 10 km cell). Beyond that the output cell is **null**. That
   makes the output footprint the source footprint to within about 2 km, and makes extrapolation
   structurally impossible rather than a matter of discipline.

### The 2020 problem, which is Canada's 2023 problem

National mean of the annual mean across all 100,156 cells, computed from the file:

```
2006 0.265    2011 0.541    2016 0.261
2007 0.507    2012 0.793    2017 0.862
2008 0.368    2013 0.479    2018 0.908
2009 0.186    2014 0.297    2019 0.318
2010 0.201    2015 0.609    2020 1.400  <--
```

2020 is 1.5x the next worst year (2018, 0.908) and 7.5x the quietest (2009, 0.186). Score on 2020 alone and the map is a picture of
one fire season. The shipped surface is the **15-year mean**, so 2020 counts once out of fifteen.
Exactly the call the Canadian side made with 2023.

### Output

`data/us/smoke_grid.json`, 3.23 MB.

```
units  ug/m3
years  2006-2020
grid   lat0 18.0  lon0 -180.0  dlat 0.1  dlon 0.1  nlat 541  nlon 1161
cells  628,101 total, 93,922 with data (15.0%), the rest null
```

0.1 degree is about 11.1 km north-south and 8.5-10.3 km east-west across the CONUS latitudes,
which is the same order as the 10 km source, so nothing is invented and nothing meaningful is
thrown away. `values[i][j]` is at `lat = lat0 + i*dlat`, `lon = lon0 + j*dlon`, row 0
southernmost. 3 decimal places, which resolves the clean end (Canada's floor is 0.04).

The box deliberately spans Alaska, Hawaii and Puerto Rico even though every cell there is null.
If the grid stopped at the CONUS border, a nearest-neighbour or clamping sampler would hand
Anchorage the value from Montana. Spanning them and filling with null means the lookup returns
"no data", which is the truth.

### Validation, computed by sampling the shipped grid

Requested cities:

| | ug/m3 | | | ug/m3 |
|---|---|---|---|---|
| Chico CA | 1.762 | | Denver CO | 0.413 |
| Medford OR | 2.276 | | Phoenix AZ | 0.119 |
| Boise ID | 1.137 | | Chicago IL | 0.518 |
| Missoula MT | 1.625 | | Miami FL | 0.136 |
| Spokane WA | 1.423 | | Portland ME | 0.216 |

Regional means:

```
N California   1.590        Michigan UP    0.514
Montana west   1.428        Florida        0.361
Washington E   1.306        Maine coast    0.232
Idaho          1.199
Oregon         1.066
```

Every western region is above every eastern one. State means taken at the 4,156 real places in
`data/us/places.json` that resolve: smokiest MT 1.047, ID 1.011, OR 0.946, ND 0.656, WA 0.649;
cleanest AZ 0.151, ME 0.212, VT 0.213, NH 0.219, NM 0.226. Smokiest individual places: Ashland OR
2.365, Medford OR 2.276, Shasta Lake CA 2.251, Redding CA 2.083, Grants Pass OR 2.007. That is
the Rogue Valley and the Klamath, which is the right answer, and it is not an answer we told it
to give. Grid maximum 4.143 at 37.70N 119.10W, the Sierra Nevada around Yosemite: Rim 2013,
Ferguson 2018, Creek 2020, and nobody lives there.

Distribution over the 93,922 covered cells:

```
min 0.098   p10 0.217   p50 0.441   mean 0.523   p90 0.922   p95 1.225   p99 1.952   max 4.143
```

Against Canada's FireWork CE span of 0.04 to 2.82 ug/m3 at towns, this sits where it should: the
US floor is higher (0.10 vs 0.04, no Arctic or Atlantic-island equivalent) and the populated
ceiling is similar (US places top out at 2.365 in Ashland OR, Canada at 2.82 in Kamloops). Both
countries land in the same 0.1-3 ug/m3 band, which matters because `app/app.js` scores this field
on a shared scale and applies a hard dealbreaker at `mean_ugm3 > 1.5`. On this surface 2.5% of
CONUS cells and 15 of 4,226 US places clear 1.5.

### Two results worth flagging rather than burying

**Michigan's Upper Peninsula does not come out among the cleanest.** It reads 0.514, above the
national median of 0.441. That was not the expectation going in. It is not noise: the whole
northern tier reads as one coherent band of transported Canadian boreal smoke, decaying west to
east.

```
MN Arrowhead 0.538   MI Upper Peninsula 0.514   WI north 0.455
MI lower north 0.431   ME coast 0.232   NY Adirondacks 0.209   VT/NH north 0.193
```

Michigan as a state still ranks 22nd of 49 at 0.384, and coastal Maine and Florida are genuinely
near the floor. But the UP sits downwind of Ontario and Manitoba, and the data says so. The
paper's own validation notes "often very high performance at EPA monitors throughout California,
the Pacific Northwest, the upper Midwest, and the Northeast", so this is a region the model reads
well, not one where it is guessing.

**Arizona reads lowest in the country (0.151), which deserves a second look and survives it.**
The low value is a desert-basin value, not a statewide one: Phoenix basin 0.133 and Tucson 0.134,
but the AZ high country runs 0.298 at Flagstaff and 0.348 in the White Mountains, and the Gila in
New Mexico runs 0.439. So Arizona's forests are ordinary and its deserts are genuinely clean,
which is the pattern you would expect from a state whose fire season ends when the monsoon
arrives. Treat the desert Southwest numbers with a little extra caution anyway: the paper reports
"lower performance at monitors in the Southwest and the South".

---

## PART 3: The fallback we did not need. NOAA HMS smoke plumes.

Documented because the brief asked for it, and checked so the note is accurate rather than
assumed. Not used.

- Product page, opened: https://www.ospo.noaa.gov/products/land/hms.html
- Archive, verified a real Apache index at HTTP 200 (not an SPA):
  https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/2020/09/

HMS gives daily smoke plume polygons, shapefile and KML, archived by year and month. The OSPO
page lists years from 2006 onward; I opened the 2020/09 directory and it serves real files.
Its density field is **categorical** ("light, medium, heavy" since 2022-07-19, previously the
numeric codes 5/16/21). It carries **no PM2.5 concentration at all**. The only metric you can
build from it is **days per year under a plume**, which is a count, not a dose: a wisp of high
transported smoke that never reaches the ground counts the same as an evacuation-grade day.

Had we shipped HMS, `units` would have had to read `days/yr` and the field could not have been
compared against, or scored on the same scale as, the Canadian ug/m3 numbers. We did not, and it
is not in the output. Note that HMS is not wasted either way: it is the input that defines
"smoke day" inside the Childs model.

## PART 4: Known limits, stated plainly

1. **Modelled, not measured.** A machine-learning prediction of a monitor-derived anomaly, not a
   sensor reading. Spatial out-of-sample R2 = 0.67. Same class of caveat as Canada's FireWork CE,
   which is also model output. Say "modelled" in any public description.
2. **Contiguous US only. Alaska and Hawaii are null.** The source domain stops at the CONUS
   border. Alaska burns hard, so a zero there would be a lie about a place that has had
   million-acre fire seasons; the grid emits null and the app must show "no data", not "clean".
   Same for Hawaii, Puerto Rico and every other territory. There is no honest way to extrapolate
   a fire-attributed surface into a region the model never saw.
3. **The window ends in 2020, and that understates today.** Canada's surface is 2013-2024. This
   one is 2006-2020. Both are long-run means, but they are not the same window, and 2006-2013 was
   a quieter fire era. The same lab's follow-up (Childs et al., "Growing wildfire-derived PM2.5
   across the contiguous U.S. and implications for air quality regulation", preprint opened at
   https://eartharxiv.org/repository/view/8187/, 2024-12-09) reports population-average smoke
   exposure in 2020-2024 running **"2.6-6.9 times higher than the 2006 to 2019 average"** (the preprint renders the range with a LaTeX double hyphen; normalised here). So
   treat this surface as a conservative floor on current exposure, and treat US-vs-Canada
   comparisons as approximate at the margin.
4. **v2.0 (2006-2023/2024) exists but is BETA and not scriptable.** The lab page labels it
   "preliminary and subject to change" and serves it from a Dropbox folder. Tested: the folder
   link with `dl=1` returns `text/html`, not a zip, and the `dl=0` page is a JavaScript app with
   no file names in the markup, so there is no unattended download path. It is the obvious
   upgrade once it is versioned and DOI'd, and it would fix limit 3.
5. **10 km cells, resampled to 0.1 degrees.** One value per neighbourhood, no street-level
   detail. Irrelevant at this app's scale.
6. **Annual mean only.** This surface cannot answer "how many days above 35 ug/m3". The daily
   file can, and it is the same download, but that is a different field and a different question.
