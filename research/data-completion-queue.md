# Data completion queue

Standing order (Roham, 2026-09-24): prepare the data to perfection AND wire it
into the app each pass, so every link sent to Doug is a better build than the
last. Data without a tile does not count as done.

Every source below was verified end to end by an agent in this session - real
download, real join test, measured coverage. Notes in `research/src-*.md`.

| # | Dimension | US source | CA source | Join | State |
| --- | --- | --- | --- | --- | --- |
| 1 | Your language | ACS C16001 | StatCan 98-401-X2021005 | GEOID / CSD | US **shipped**, CA building |
| 2 | Internet | FCC BDC place summary, 27.4 MB | CRTC CMR C-T9, 32.3 MB | **both direct, 7-digit** | queued |
| 3 | Natural hazard | FEMA NRI county CSV | NRCan Seismic PSRA | county FIPS / **csduid direct** | queued |
| 4 | Dark sky | VIIRS VNL V2 via Zenodo | same file, global raster | lat/lon sample | queued |
| 5 | Walkability | EPA National Walkability Index | StatCan Proximity Measures | block group -> place / **CSDUID** | queued |
| 6 | Coverage audit | every dimension, both countries | | | after 1-5 |

## Traps already paid for, do not rediscover

- **FCC**: never `technology='Any Technology'` - it counts Starlink and reads
  ~1.000 everywhere. Use `Any Terrestrial` + `Fiber`. Akamai 403s curl; throttle.
- **CRTC**: cp1252 not UTF-8, header on line 5, and the table's own title says
  "by CMA" while the geography is actually CSD. 50/10 is saturated (71% of places
  at exactly 100%) - rank on Gigabit.
- **FEMA**: `hazards.fema.gov` was unreachable; the working path is the ArcGIS
  Hub CSV. Riverine flood is `IFLD_RISKS`, not `RFLD_`.
- **VIIRS**: EOG's own download went paid 2026-06-01. Zenodo mirror is the same
  VNL V2 data, no account. Values rescaled 0-2000, not raw radiance.
- **EPA**: the published CSV writes GEOID in scientific notation (`4.8113E+11`),
  which destroys the join. Rebuild from STATEFP+COUNTYFP+TRACTCE+BLKGRPCE, and
  use the **2010** Block Assignment Files - 2020 silently drops 13% of a city.
- **Can-ALE**: joins at 100% and is tempting. It ships with **no licence at all**
  (`license: null`). Not usable in a public app. StatCan Proximity is the answer.
- **StatCan census CSV**: cp1252. Read as UTF-8 and Montreal becomes "montral"
  while the script reports success.

## Rules this queue follows

- A tile is not offered unless the data answers for most places. The Sun tile was
  offered in the US with zero coverage and returned "not recorded here" for all
  4,197 - worse than not existing, because it spends one of five picks.
- Saturation is measured per country at build time, never shared.
- Missing is `null`, never `0`. A fabricated zero ranks a town as having none.
