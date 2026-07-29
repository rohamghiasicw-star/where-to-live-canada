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
"PM25 Annual 2012", event types "No Events" or "Events Included" so wildfire days stay in,
>=200 observations, sites present in all three years. Total PM2.5 per site = mean of the three
annual arithmetic means. Fire-attributed smoke per site = the surface built in Part 2, sampled
at the monitor's own lat/lon.

<!--TRAP-->

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

<!--BUILD-->

---

## PART 3: The fallback we did not need. NOAA HMS smoke plumes.

Documented because the brief asked for it, and checked so the note is accurate rather than
assumed. Not used.

- Product page, opened: https://www.ospo.noaa.gov/products/land/hms.html
- Archive, verified a real Apache index at HTTP 200 (not an SPA):
  https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/2020/09/

HMS gives daily smoke plume polygons, shapefile and KML, archived from 2005-2006 to the present.
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
   exposure in 2020-2024 running **"2.6--6.9 times higher than the 2006 to 2019 average"**. So
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
