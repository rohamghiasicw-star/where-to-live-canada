# Source verification: airport global connectivity + humidity normals

Verified 2026-08-18. Every URL below was actually requested from this machine. Where a
link could not be confirmed working, it says so explicitly. No values are estimated.

App context: 4,197 US places (7-digit Census place GEOID + lat/lon), 710 Canadian places
(CSD code + lat/lon), road drive-time engine available.

---

# PART 1 - AIRPORT GLOBAL CONNECTIVITY

Target dimension: "can I get a direct international flight without a 4-hour drive".

## 1A. OpenFlights routes.dat - NOT USABLE

**Verdict: NOT USABLE. The route data was abandoned in June 2014 and the project says so
itself. It is 12 years stale.**

| | |
|---|---|
| URL (routes) | `https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat` |
| URL (airports) | `https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat` |
| HTTP status | 200 both. Files download fine. The links work - the *data* is what's dead. |
| Size | routes.dat 2,377,148 B (67,663 rows). airports.dat 1,127,225 B (7,698 rows). |
| Format | Headerless CSV. routes: `airline,airlineID,src,srcID,dst,dstID,codeshare,stops,equipment` |
| Licence | Open Database License (ODbL) 1.0 |
| Cost | Free |

### Last-update dates (from the GitHub commits API, not guessed)

- `data/routes.dat` - last commit touching this file: **2017-02-02** ("Update data exports").
  Prior commits 2014-08-06, 2014-01-16.
- `data/airports.dat` - last commit touching this file: **2019-05-13**.
- The repo itself is alive (`pushed_at` 2026-08-08) but that is PHP/site code, not the data.
  Newest data-bearing commit is the 2019 airports one.

### The project's own statement

openflights.org/data.php says, verbatim:

> "Warning: The third-party that OpenFlights uses for route data ceased providing updates
> in June 2014. The current data is of historical value only."

And: "As of June 2014, the database contains 67,663 routes between 3,321 airports on 548
airlines." The GitHub copies are described as "sporadically updated static snapshot[s]".

### Independently confirmed staleness (I ran these checks against the downloaded file)

Defunct carriers still present as live routes:

| Carrier | Status | Route rows still in routes.dat |
|---|---|---|
| FL AirTran | merged into Southwest 2014 | 726 |
| US US Airways | merged into American 2015 | 1,960 |
| AB Air Berlin | ceased 2017 | 798 |
| VX Virgin America | merged into Alaska 2018 | 66 |
| AZ Alitalia | ceased 2021 | 877 |
| BE Flybe | ceased | 268 |

Missing post-2014 reality: **BER (Berlin Brandenburg, opened Oct 2020) does not appear in
routes.dat at all.**

Derived international counts from the file (src country != dst country):
- 34,767 international route rows
- 1,172 airports worldwide with at least one international route
- **only 65 US airports and 19 Canadian airports** with any international route

That US figure alone disqualifies it. BTS reports 83 US airports with scheduled
international service in a *single month* (March 2026) - see 1B.

### Also: airports.dat is redundant

The `source` column of airports.dat is **"OurAirports" for all 7,698 rows**. It is a stale
2019 subset of OurAirports, which has 85,932 rows and updates nightly. There is no reason
to use OpenFlights airports.dat over OurAirports.

---

## 1B. US DOT BTS T-100 International Segment - USABLE (best source for US)

**Verdict: USABLE. Current, authoritative, free, public domain, and it cleanly yields
"airports with scheduled international service" plus a real connectivity score. The only
work is scripting an ASP.NET form POST - there is no static download URL.**

| | |
|---|---|
| Table | `T_T100I_SEGMENT_ALL_CARRIER` - T-100 International Segment (All Carriers) |
| Download page | `https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FJE&QO_fu146_anzr=Nv4%20Pn44vr45` |
| Database | `QO_VQ=EEE` = Air Carrier Statistics (Form 41 Traffic) - All Carriers |
| Format | ZIP containing `T_T100I_SEGMENT_ALL_CARRIER.csv` + `Documentation.csv` |
| Size | **374,075 B zipped / 2,734,227 B CSV / 9,677 data rows for one month** (March 2026, all 43 fields) |
| Latest data | **May 2026** (read from the BTS TableInfo page 2026-08-18) - roughly a 3-month lag |
| Coverage | 1990 to present, monthly |
| Licence | US Government work, public domain. No cost, no account, no API key. |
| Granularity | Airport-to-airport segment, by carrier, by month |
| Join key | IATA airport codes (`ORIGIN`, `DEST`) + `ORIGIN_AIRPORT_ID`. Join to lat/lon via OurAirports `iata_code`, then drive-time from place lat/lon. |

### There is NO static file URL - this is the one real catch

`https://transtats.bts.gov/PREZIP/T_T100I_SEGMENT_ALL_CARRIER.zip` and every similar guess
returns **404**. The `/PREZIP/` directory is browsable (644 files) but the only T-100
international file in it is `896821601_T_T100I_MARKET_ALL_CARRIER.zip` from **2015** - a
leftover session artifact, not a maintained export. PREZIP only carries current static
files for On-Time Performance and the Origin & Destination Survey.

**You must POST the download form.** I did this successfully. The mechanics:

1. GET the DL_SelectFields URL above, keep the cookie jar.
2. Scrape `__VIEWSTATE`, `__VIEWSTATEGENERATOR`, `__EVENTVALIDATION` from the HTML.
3. POST back to the same URL with each field name set to `on`, plus `chkAllVars=on`,
   `cboGeography=All`, `cboYear=<year>`, `cboPeriod=<month or All>`, `chkDownloadZip=on`,
   `btnDownload=Download`.
4. Response is `Content-Type: application/zip` with the CSV inside.

Table codes under `QO_VQ=EEE`, confirmed empirically by reading the returned
`Content-Disposition` filename for each:

| gnoyr_VQ | Table returned | Fields |
|---|---|---|
| **FJE** | **T_T100I_SEGMENT_ALL_CARRIER** (international segment - this is the one) | 43 |
| FJD | T_T100I_MARKET_ALL_CARRIER | 34 |
| FMF | T_T100_MARKET_ALL_CARRIER (combined) | 41 |
| FMG | T_T100_SEGMENT_ALL_CARRIER (combined dom+intl) | 50 |
| FIM | T_T100D_SEGMENT_US_CARRIER_ONLY (domestic - not what you want) | 45 |

Note the code is *not* guessable from the table name, and `FIM` (which looks like
"international market") actually serves the domestic table. Use **FJE**.

### How to derive "airports with scheduled international service"

Fields present include `DEPARTURES_SCHEDULED`, `DEPARTURES_PERFORMED`, `CLASS`,
`ORIGIN`, `ORIGIN_COUNTRY`, `ORIGIN_COUNTRY_NAME`, `DEST`, `DEST_COUNTRY`,
`DEST_COUNTRY_NAME`, `PASSENGERS`, `SEATS`, `AIRCRAFT_TYPE`.

Filter: `DEPARTURES_SCHEDULED > 0` AND `CLASS in ('F','G')` (scheduled service classes)
AND `ORIGIN_COUNTRY != DEST_COUNTRY`. Take `ORIGIN` where `ORIGIN_COUNTRY='US'`, and
`DEST` where `DEST_COUNTRY='US'` to catch inbound-only.

I ran exactly this on March 2026. Result: **83 US airports with scheduled international
service**, serving 78 distinct destination countries.

Distinct countries reachable direct, top 10 (a ready-made connectivity score):

| Airport | Countries direct | Scheduled departures |
|---|---|---|
| MIA | 46 | 10,126 |
| JFK | 45 | 6,957 |
| ATL | 44 | 6,035 |
| EWR | 42 | 5,295 |
| IAH | 29 | 5,867 |
| DFW | 28 | 5,590 |
| IAD | 27 | 2,277 |
| CLT | 26 | 2,940 |
| ORD | 25 | 4,619 |
| PHL | 22 | 1,800 |

Median across the 83 international airports is **3 countries**, and the tail is thin and
real (FAR, COS, CHS, ORF each 1 country, 8-12 scheduled departures a month). That tail is
exactly what a "can I fly abroad from here" dimension needs to grade honestly - a
one-country-eight-flights airport is not global connectivity.

### Pull 12 months, not one - the single-month number is badly wrong

`cboPeriod=All` with a single `cboYear` gets a whole year in one request. I did this for
calendar year 2025 and the result changes the picture:

| Pull | Zip | CSV | Rows | US airports w/ scheduled intl service |
|---|---|---|---|---|
| One month (Mar 2026) | 374,075 B | 2,734,227 B | 9,677 | **83** |
| Full year (2025) | **3,655,301 B** | **31,747,310 B** | **112,306** | **142** |

The full-year pull took **83 seconds**. All 12 months present.

**A single month misses 59 of 142 US international airports** - seasonal and low-frequency
service (ski charters, summer transatlantic, thin Caribbean markets) simply isn't there in
any given month. Always aggregate a full year.

Full-year 2025 top 5 by distinct countries direct: EWR 52, JFK 50, MIA 47, ATL 46, IAH 33.
Median across all 142 is **2 countries** - the tail gets even thinner once seasonal
one-country airports are included, which is the correct and honest result for this
dimension.

### The Canada gap - important

T-100 International Segment only covers segments with at least one US endpoint. Canadian
airports appear only via US routes (17 Canadian airports in the March 2026 file). A
Canadian airport's transatlantic or transpacific service is **not in this dataset at all**.
BTS cannot grade Canadian international connectivity. See 1D.

---

## 1C. OurAirports - USABLE, but it is not a route source

**Verdict: USABLE as the airport identity/geometry backbone. NOT USABLE on its own for the
international question - it publishes no route data of any kind.**

| | |
|---|---|
| URL | `https://davidmegginson.github.io/ourairports-data/airports.csv` |
| Mirror | `https://ourairports.com/data/airports.csv` (identical Content-Length) |
| HTTP status | 200 |
| Size | **12,703,051 B, 85,932 rows, 19 columns** |
| Last-Modified | **Tue, 18 Aug 2026 01:53:58 GMT** - i.e. refreshed the same day I checked |
| Update cadence | Nightly (stated on ourairports.com/data/) |
| Licence | **"All data is released to the Public Domain, and comes with no guarantee of accuracy or fitness for use."** (verbatim) |
| Cost | Free, no account |
| Join key | `iata_code`, `icao_code`, `ident`, plus `latitude_deg`/`longitude_deg` for the drive-time engine |

Columns: `id, ident, type, name, latitude_deg, longitude_deg, elevation_ft, continent,
iso_country, iso_region, municipality, scheduled_service, icao_code, iata_code, gps_code,
local_code, home_link, wikipedia_link, keywords`

Companion files all 200 and same timestamp: `runways.csv` (3,960,167 B),
`airport-frequencies.csv` (1,299,258 B), `countries.csv` (24,583 B), `regions.csv` (485,253 B).

`scheduled_service` is a yes/no flag with **no international/domestic distinction**:
- US: 32,619 airport records, 699 with `scheduled_service=yes`
- Canada: 3,358 records, 304 with `scheduled_service=yes`
- Global: 4,371 with `scheduled_service=yes`

**There is no route, schedule, airline, or destination column.** I checked the column list
directly and confirmed with the OurAirports data page. Use it for lat/lon and IATA
resolution; get "international" from BTS (US) and StatCan (Canada).

---

## 1D. Statistics Canada Table 23-10-0302 - USABLE WITH WORK (the Canada answer)

**Verdict: USABLE WITH WORK. It is the only current, free, per-airport international
measure I could confirm for Canada. It tells you an airport HAS international air-carrier
traffic and how much, but NOT which countries it flies to. Airport names need a one-time
manual join to lat/lon.**

| | |
|---|---|
| Table | 23-10-0302-01, "Domestic and international itinerant movements, by type of operation, at airports with NAV CANADA services and other selected airports, monthly" |
| Download URL | `https://www150.statcan.gc.ca/n1/tbl/csv/23100302-eng.zip` |
| HTTP status | 200, `application/zip` |
| Size | **2,910,960 B zipped -> 47,784,640 B CSV, 241,101 data rows** |
| Coverage | 2019-01 through **2026-05**, monthly. Cube released 2026-07-30, status "CURRENT". |
| Licence | Statistics Canada Open Licence. Free, no account. |
| Granularity | **129 named airports** (126 real + 3 "Total" rows) |
| Join key | Airport *name* only (e.g. "Calgary International, Alberta"). No IATA/ICAO code, no CSD code. |

Dimensions:
- Geography: Canada (1)
- Airports: 129 members
- Domestic and international itinerant movements: **Domestic / Transborder / Other international**
- Type of operation: 7, including "Air carrier movements, level I-III including foreign air carriers"

Columns: `REF_DATE, GEO, DGUID, Airports, Domestic and international itinerant movements,
Type of operation, UOM, UOM_ID, SCALAR_FACTOR, SCALAR_ID, VECTOR, COORDINATE, VALUE,
STATUS, SYMBOL, TERMINATED, DECIMALS`

Filtering to `Air carrier movements, level I-III including foreign air carriers` for
2026-05 (I ran this):
- **31 Canadian airports with >0 "Other international" movements** (beyond the US)
- **62 Canadian airports with >0 "Transborder" movements** (to/from the US)

Examples for 2026-05 "Other international": Calgary International 917, Halifax/Robert L.
Stanfield 489, Edmonton International 121, Hamilton 46, Gander International 34, Iqaluit 16.

### The two real limitations

1. **It counts aircraft movements, not routes.** You get "how much international traffic",
   never "flies direct to which countries". A US-style country-count score is impossible
   from this table. Grading Canada and the US on the same scale needs care - a movement
   count is not a country count.
2. **The join needs manual work.** Airport names are StatCan strings with no code. I
   tested a normalised name match against OurAirports Canadian records: **91 of 126
   matched automatically, 35 need manual mapping** (e.g. "Halifax/Robert L. Stanfield
   International, Nova Scotia", "Montréal (St-Hubert)/Montréal Metropolitan, Quebec",
   "Inuvik/Mike Zubko, Northwest Territories"). That is a one-time ~35-row lookup table,
   not a blocker.

---

## 1E. Other free sources checked

**OpenSky Network historical flights - NOT USABLE without an account.**
`https://opensky-network.org/api/flights/departure?airport=KSEA&begin=...&end=...` returns
**HTTP 403** with body `You cannot access historical flights`. Anonymous historical access
is closed. Live state vectors are a different endpoint and would not give you a scheduled
route list anyway.

**AeroSCOPE (Zenodo)** - surfaced in search as a global open O-D air traffic dataset, but
it is **2019 data only** and research-oriented. I did not download it. Too stale for a
"current connectivity" dimension; not worth pursuing.

**OAG, Cirium, Innovata, travelscrape-style vendors** - all commercial/paid. Out of scope
for a free-source build.

**Wikipedia "Airlines and destinations" tables** - would be current and CC BY-SA, but it is
per-article HTML scraping with no stable schema and no downloadable structured export. Not
verified, not recommended over BTS.

## PART 1 BOTTOM LINE

- **US: use BTS T-100 International Segment (gnoyr_VQ=FJE), 12 months at a time.** It is
  the most current picture and the only one that yields a real per-airport country count.
- **Canada: use StatCan 23-10-0302**, accepting that it gives volume, not destinations.
- **Use OurAirports for every airport's lat/lon and IATA code** to feed the drive-time engine.
- **Do not use OpenFlights routes.dat.** Dead since June 2014, by the project's own admission.
- The dimension is buildable for the US at full quality. Canada is buildable at lower
  quality (has/hasn't + volume), and the two countries are not directly comparable.

---

# PART 2 - RELATIVE HUMIDITY IN CLIMATE NORMALS

Doug's ask: "micro-climate targeting: optimal humidity".

## 2A. NOAA US Climate Normals 1991-2020 - USABLE WITH WORK, and "micro-climate" is the wrong word

**Verdict: USABLE WITH WORK. There is NO published relative humidity normal anywhere in the
1991-2020 product. There IS an hourly dew point normal, at 467 stations only. RH must be
derived from temperature + dew point, which makes it a derived value, not a published one.
The 467-station network is regional, not micro-climate.**

### Monthly normals - NO humidity at all. Rules out the easy path.

| | |
|---|---|
| URL | `https://www.ncei.noaa.gov/data/normals-monthly/1991-2020/access/<GHCN_ID>.csv` |
| Example verified | `.../access/USW00024233.csv` - 41,714 B |
| Station count | **15,616 station CSVs** |

Element roots present: `MLY-CLDD, MLY-DUTR, MLY-GRDD, MLY-HTDD, MLY-PRCP, MLY-SNOW,
MLY-SNWD, MLY-TAVG, MLY-TMAX, MLY-TMIN`.

**No humidity, no dew point, no wet bulb.** Confirmed twice: by grepping the column header
of a real station file, and via the NCEI search API -
`https://www.ncei.noaa.gov/access/services/search/v1/data?dataset=normals-monthly-1991-2020&dataTypes=MLY-DEWP-NORMAL&limit=1`
returns **count 0**.

### Hourly normals - dew point yes, relative humidity no

| | |
|---|---|
| Per-station URL | `https://www.ncei.noaa.gov/data/normals-hourly/1991-2020/access/<GHCN_ID>.csv` |
| Example verified | `.../access/USW00024233.csv` (Seattle-Tacoma) - **6,432,468 B, 7,361 rows, 113 columns** |
| Directory | `https://www.ncei.noaa.gov/data/normals-hourly/1991-2020/access/` - **467 station CSVs** |
| Station inventory | `https://www.ncei.noaa.gov/data/normals-hourly/1991-2020/doc/hly_inventory_30yr.txt` - 40,162 B, 467 lines, gives ID/lat/lon/elev/state/name/WMO |
| Bulk archive | `.../archive/us-climate-normals_1991-2020_v1.0.0_hourly_multivariate_by-station_c20210423.tar.gz` - **232,303,441 B** |
| Bulk (by variable) | `.../archive/us-climate-normals_1991-2020_v1.0.0_hourly_multivariate_by-variable_c20210423.tar.gz` - **243,943,659 B** |
| Docs | `.../doc/Normals_HLY_Documentation_1991-2020.pdf`, `Normals_Calculation_Methodology_2020.pdf` |
| Licence | US Government work, public domain. Free, no key. |
| Join key | GHCN-Daily station ID + `LATITUDE`/`LONGITUDE` columns -> nearest-station or drive-time join to place lat/lon |

**Complete element list in the hourly normals** (26 elements x 4 columns each):

```
HLY-TEMP-NORMAL   HLY-TEMP-10PCTL   HLY-TEMP-90PCTL
HLY-DEWP-NORMAL   HLY-DEWP-10PCTL   HLY-DEWP-90PCTL     <- the humidity-bearing element
HLY-PRES-NORMAL   HLY-PRES-10PCTL   HLY-PRES-90PCTL
HLY-CLDH-NORMAL   HLY-HTDH-NORMAL
HLY-CLOD-PCTCLR   HLY-CLOD-PCTFEW   HLY-CLOD-PCTSCT   HLY-CLOD-PCTBKN   HLY-CLOD-PCTOVC
HLY-HIDX-NORMAL   HLY-WCHL-NORMAL
HLY-WIND-AVGSPD   HLY-WIND-PCTCLM   HLY-WIND-VCTDIR   HLY-WIND-VCTSPD
HLY-WIND-1STDIR   HLY-WIND-1STPCT   HLY-WIND-2NDDIR   HLY-WIND-2NDPCT
```

Each element ships as four columns: the value, `meas_flag_<el>`, `comp_flag_<el>`,
`years_<el>`.

**There is no `HLY-RHUM-*` or any relative humidity element.** The closest published
proxies are `HLY-DEWP-NORMAL` (dew point, deg F) and `HLY-HIDX-NORMAL` (heat index, which
is itself a function of temperature and RH but only diverges from temperature in hot
conditions - for the Seattle row I pulled, HIDX 67.3 == TEMP 67.3 exactly).

Verified real data, Seattle-Tacoma, June 16 hour 16:
`HLY-TEMP-NORMAL 67.3`, `HLY-DEWP-NORMAL 48.3`, `HLY-HIDX-NORMAL 67.3`, `HLY-PRES-NORMAL 1017.6`.
Missing `HLY-DEWP-NORMAL` values in that file: **0 of 7,361 rows.**

### Station count carrying dew point: 467, and that is ALL of them

The NCEI search API gives an exact count, and the filter demonstrably works:

| Query | count |
|---|---|
| `dataset=normals-hourly-1991-2020` (no filter) | 467 |
| `&dataTypes=HLY-DEWP-NORMAL` | **467** |
| `&dataTypes=HLY-TEMP-NORMAL` | 467 |
| `&dataTypes=HLY-WIND-AVGSPD` | 467 |
| `&dataTypes=HLY-BOGUS-ELEMENT` (control) | **0** |

So every station in the hourly product carries dew point - there is no sparse subset
problem *within* the hourly network. The problem is that the hourly network itself is only
467 stations, against 15,616 in the monthly product.

Spread: 54 state/territory codes. Best covered CA 30, AK 29, TX 27, FL 23. Worst: DE 1,
RI 1, MH 1, AS 1, VT 2, CT 2, MA 2, GU 2, FM 2, MD 3, NH 3, ID 4.

### The number that decides this dimension

I computed great-circle distance from each of the app's 4,226 US places to the nearest
station in each network:

| | median | p75 | p90 | p95 | max |
|---|---|---|---|---|---|
| **Hourly / dew point (467 stns)** | **24.9 km** | 43.4 | **69.0** | 87.8 | 1,745.8 |
| Monthly / temp+precip (15,615 stns) | 4.1 km | 6.9 | 10.3 | 12.5 | 35.3 |

Places farther than a given distance from a dew point station:
- >25 km: **2,106 places (49.8%)**
- >50 km: 818 (19.4%)
- >100 km: 134 (3.2%)
- >150 km: 37 (0.9%)

**Half the app's US places are more than 25 km from the nearest dew point station, and one
in ten is more than 69 km away.** The existing temperature/precipitation dimensions run on
a network six times denser with a median of 4 km.

### The "never estimate a value" problem - read this before shipping

Two separate issues, both of which matter given the app's hard rule:

1. **RH is not published. It is derived.** RH = 100 x e(Td) / e(T) via the Magnus relation
   on `HLY-DEWP-NORMAL` and `HLY-TEMP-NORMAL`. Both inputs come from the same station and
   the same hour, so the inputs are real measurements, not guesses. But the output is a
   computed quantity that NOAA does not publish.
2. **Mean-of-inputs is not the mean of the output.** RH is a nonlinear function of T and
   Td, so RH computed from the *normal* T and the *normal* Td is not the same as the
   *normal* RH. This is Jensen's inequality, and it biases the result. NOAA's hourly
   normals documentation does not publish the magnitude of this bias for these elements,
   and **I did not measure it** - doing so would require the underlying hourly
   observations, not the normals. Do not state a bias figure without measuring it.

If the dimension ships, it should be labelled as **derived from published dew point and
temperature normals**, with the method named, and it should not be called "micro-climate".
At a 25 km median and 69 km p90, it is a regional humidity signal. Dew point is spatially
smoother than precipitation so interpolation is more defensible than it would be for rain,
but it degrades badly across coastal-to-inland and mountain transitions - precisely the
places where a "micro-climate" claim would be most visible and most wrong.

### If true measured RH is required instead of derived

- **USCRN (US Climate Reference Network)** measures RH directly.
  `https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/` - HTTP 200.
  Station list `https://www.ncei.noaa.gov/pub/data/uscrn/products/stations.tsv` - 255
  stations. But these are *observations*, not normals, and USCRN sites are deliberately
  rural reference locations - worse for city-level joins than the 467 hourly normals
  stations, not better.
- **Local Climatological Data (LCD)**
  `https://www.ncei.noaa.gov/data/local-climatological-data/` - HTTP 200. Carries hourly
  observed RH at airport stations, but again observations, not normals. Building your own
  30-year normal from LCD is a large job and would no longer be "the NOAA normal".

### Footnote: the older product is the same

The 1981-2010 hourly normals (`https://www.ncei.noaa.gov/data/normals-hourly/1981-2010/`,
HTTP 200, 457 station CSVs) carry the same element roots - `HLY-CLDH, HLY-CLOD, HLY-DEWP,
HLY-HIDX, HLY-HTDH, HLY-PRES, HLY-TEMP, HLY-WCHL, HLY-WIND`. Dew point yes, relative
humidity no. Switching periods does not solve it.

## 2B. ECCC Canadian Climate Normals - USABLE WITH WORK, and it works the OPPOSITE way to NOAA

**Verdict: USABLE WITH WORK. ECCC publishes relative humidity DIRECTLY as a normal - which
NOAA does not - but only at two fixed clock hours (06:00 and 15:00 LST), and it publishes
no dew point at all. Switch the app to the 1991-2020 normals: they exist, and they nearly
double humidity coverage over the 1981-2010 set the app currently uses.**

### The headline: 1991-2020 Canadian normals are released, and the app should move to them

The app currently uses Canadian Climate Normals **1981-2010**. The **1991-2020** normals
are published and downloadable. Evidence opened:
- `https://collaboration.cmc.ec.gc.ca/cmc/climate/Normals/Canadian_Climate_Normals_1991_2020_Calculation_Information.pdf`
  - HTTP 200, 606,146 B, 25 pages, footer "Date modified: 2025-05-30". Section 11.10.4 is "Humidity".
- The landing page lists 1991-2020 first, with its own search forms.

Humidity coverage roughly doubles:

| Period | Stations w/ relative humidity | Of total |
|---|---|---|
| 1981-2010 | 195 | of 1,135 (17.2%) |
| **1991-2020** | **345** | **of 448 (77.0%)** |

The jump is because 1991-2020 uses *composite* stations that merge nearby records.

### Best download - one file, verified end to end

| | |
|---|---|
| URL | `https://climate.weather.gc.ca/climate_normals/download/1991_e.html?area=canada_wide&product%5B%5D=data` |
| HTTP status | 200, ZIP |
| Size | **1,689,719 B zipped -> 12,651,414 B CSV, 69,068 rows** |
| Contents | `1991-2020_Canadian_Climate_Normals_CANADA_Data.csv` |
| Format | Long/tall: one row per station-element, months as columns |
| Licence | ECCC Data Servers End-use Licence v2.1. Free, no key, no auth. Attribution required: "Data Source: Environment and Climate Change Canada" |

Columns: `LOCATION_NAME, PROVINCE_OR_TERRITORY, PERIOD_OF_RECORD, ELEMENT_GROUP,
NORMALS_ELEMENT, Jan..Dec, Year, Code`

Per-province variant works too (`area=province&province[]=BC` -> 215,809 B). There is **no
1981-2010 equivalent of this bulk file** - `/climate_normals/download/1981_e.html` is 404.

### The humidity elements, verbatim

I ran the counts myself against the downloaded file and they match the independent check:

| `NORMALS_ELEMENT` (verbatim) | Locations |
|---|---|
| `Average Relative Humidity - 1500LST (%)` | **345** |
| `Average Relative Humidity - 0600LST (%)` | 343 |
| `Average Vapour Pressure (kPa)` | 338 |

448 distinct `LOCATION_NAME` in the file. `ELEMENT_GROUP = 'Humidity'`.

**There is no dew point element.** I searched all element names - none. The 1991-2020
calculation PDF discusses dewpoint only as an *input* to ECCC's RH calculation (via wet
bulb or a Dewcel), never as a published normal.

**Derive dew point from `Average Vapour Pressure (kPa)`** at those 338 locations, using
ECCC's own relation from the PDF: `e = 6.11 * exp[5417.7530 * ((1/273.16) - (1/Td))]`,
e in hPa, Td in Kelvin. Invert for Td.

### The 1981-2010 route, if needed

- Per-station CSV: `https://climate.weather.gc.ca/climate_normals/bulk_data_e.html?ffmt=csv&lang=e&prov=BC&yr=1981&stnID=889&submit=Download+Data`
  - **Gotcha: returns the CSV in the body of a 302 response** with `Location: http://climate.weather.gc.ca/template`. `curl -L` follows it and lands on a 404 HTML page. **Do not follow redirects.** 15,326 B for Vancouver Intl.
  - `stnID` drives it; `prov` is ignored. `yr=1991` returns header-only - this endpoint does not serve 1991-2020.
- MSC Datamart mirror, cleanest for scripting:
  `https://dd.weather.gc.ca/today/climate/observations/normals/csv/1981-2010/<PROV>/climate_normals_<PROV>_<CLIMATE_ID>_1981-2010.csv`
  - e.g. `.../BC/climate_normals_BC_1108447_1981-2010.csv` - HTTP 200, 12,787 B. Keyed by
    climate ID, no redirect games. **721 files total. Files are latin-1, not UTF-8.**
- GeoMet OGC API: `https://api.weather.gc.ca/collections/climate-normals` - titled
  "Climate - Normals 1981-2010", 592,926 features. Element field is `E_NORMAL_ELEMENT_NAME`.
  Only moisture elements: `Mean of 0600 LST relative humidity %` (NORMAL_ID 116, 164
  stations), `Mean of 1500 LST relative humidity %` (117, 168 stations), `Mean of hourly
  vapour pressure kPa` (114, 135 stations). No dew point. `MONTH` 1-13 where 13 = annual.
  There is no `climate-normals-elements` collection (404).
- Verbatim 1981-2010 humidity rows, Vancouver Intl (stnID 889, climate ID 1108447):
  ```
  "Humidity"
  "Average Vapour Pressure (kPa)","0.7","0.7","0.8",...,"1.0","A"
  "Average Relative Humidity - 0600LST (%)","89.1","86.7","85.6",...,"85.9","A"
  "Average Relative Humidity - 1500LST (%)","81.2","74.5","70.1",...,"70.3","A"
  ```

### Join keys - the 1991-2020 data file has no coordinates

The data CSV carries **`LOCATION_NAME` + `PROVINCE_OR_TERRITORY` only. No climate ID, no
lat/lon.** You must join to the station inventory:

`https://climate.weather.gc.ca/climate_normals/station_inventory_e.html?yr=1991`
- HTTP 200, 88,583 B, 938 rows / 448 composite stations
- Columns: `COMPOSITE_STATION_NAME, NORMALS_CODE, STATION_NAME, CLIMATE_ID,
  WMO_IDENTIFIER, TC_IDENTIFIER, PROVINCE_OR_TERRITORY, LATITUDE, LONGITUDE, ELEVATION(m)`
- Join on `LOCATION_NAME` = `COMPOSITE_STATION_NAME`. **Join on name only** - the province
  field differs in format between the two files (`BC` vs `BRITISH COLUMBIA`).
- I verified this join: **345 of 345 RH locations geocode cleanly.** No manual mapping needed.

(1981-2010 inventory, if needed: same URL with `yr=1981` - 100,173 B, 1,135 stations,
keyed on `CLIMATE_ID` with `WMO_IDENTIFIER` and `TC_IDENTIFIER` also present.)

### Coverage against the app's actual 712 Canadian places

I computed great-circle distance from each place in `data/coords.json` to the nearest of
the 345 geocoded RH locations:

| | median | p75 | p90 | p95 | max |
|---|---|---|---|---|---|
| **Canada, ECCC 1991-2020 RH (345 stns)** | **20.8 km** | 39.1 | **58.0** | 72.1 | 230.2 |

- >25 km: 300 places (42.1%)
- >50 km: 120 places (16.9%)
- >100 km: 10 places (1.4%)
- >150 km: 1 place (0.1%)

This is very close to the US picture (median 24.9 km, p90 69.0 km). Same conclusion: it is
a regional signal, not micro-climate.

### The cross-border asymmetry - the thing that will bite

The two countries publish **opposite halves** of the same physics:

| | NOAA US 1991-2020 | ECCC Canada 1991-2020 |
|---|---|---|
| Relative humidity | **not published** - derive from T + Td | **published directly** |
| Dew point | **published** (`HLY-DEWP-NORMAL`) | **not published** - derive from vapour pressure |
| Time resolution | hourly, all 24 hours | **two clock hours only: 06:00 + 15:00 LST** |
| Stations | 467 | 345 (450 locations in file) |

So a single cross-border humidity number requires a derivation on **both** sides, in
opposite directions, and the time bases do not match. NOAA gives you a full diurnal curve;
ECCC gives you two snapshots. To compare a US place with a Canadian one you would have to
sample the US hourly normals at roughly 06:00 and 15:00 local and derive RH there - which
is doable and defensible, but it must be done deliberately, and the resulting dimension is
"average of two clock-hour RH readings", not "average humidity".

**Neither country publishes a daily-mean or monthly-mean relative humidity normal.**

---

# SUMMARY TABLE

| Source | Verdict | One-line reason |
|---|---|---|
| OpenFlights routes.dat | **NOT USABLE** | Route feed dead since June 2014 per the project itself; still lists AirTran, US Airways, Air Berlin, Alitalia; only 65 US intl airports vs BTS's 83 in one month |
| OpenFlights airports.dat | **NOT USABLE** | Stale 2019 snapshot whose every row is sourced from OurAirports; use OurAirports directly |
| BTS T-100 Intl Segment (FJE) | **USABLE** | Current to May 2026, free, public domain, yields 83 US intl airports + direct country counts; needs a scripted form POST, no static URL |
| OurAirports airports.csv | **USABLE** (as backbone) | Refreshed nightly, public domain, gives lat/lon + IATA for the drive-time join; carries no route data at all |
| StatCan 23-10-0302 | **USABLE WITH WORK** | Only current per-airport Canadian international measure; movements not destinations; 35 of 126 airport names need manual lat/lon mapping |
| OpenSky historical flights | **NOT USABLE** | HTTP 403 anonymous, "You cannot access historical flights" |
| NOAA monthly normals 1991-2020 | **NOT USABLE** for humidity | No humidity or dew point element exists; API returns count 0 for MLY-DEWP-NORMAL |
| NOAA hourly normals 1991-2020 | **USABLE WITH WORK** | Dew point at all 467 stations, but no published RH (must derive, nonlinear bias), and 50% of US places sit >25 km from a station - regional, not micro-climate |
| NOAA USCRN / LCD | **NOT USABLE** as a normal | True measured RH but observations only, and rural siting is worse for city joins |
| ECCC Canadian Normals **1991-2020** | **USABLE WITH WORK** | RH published directly at 345 of 448 locations, one 1.7 MB download, 345/345 geocode - but 06:00/15:00 LST only, no dew point, and 42% of Canadian places sit >25 km out |
| ECCC Canadian Normals 1981-2010 | **USABLE, but superseded** | Only 195 of 1,135 stations carry RH; 1991-2020 nearly doubles that from a single file - move the app over |

---

# WHAT I WOULD DO

**Airports - build it, US-first.**
Pull BTS T-100 International Segment (`gnoyr_VQ=FJE`) for the most recent complete calendar
year, one request, 3.7 MB. That gives 142 US airports and a countries-reachable-direct
count per airport. Join to OurAirports for lat/lon, run the drive-time engine, and the
dimension is real. Canada gets a weaker version off StatCan 23-10-0302 (has/hasn't +
volume, no destinations) and should be scored on its own scale, not pooled with the US.
Drop OpenFlights entirely.

**Humidity - the data exists, but the pitch does not.**
Doug asked for "micro-climate targeting: optimal humidity". What is actually available is
a ~350-470 station network per country where half the app's places sit more than 20-25 km
from the nearest station and one in ten is 58-69 km out, with no published RH on the US
side, no published dew point on the Canadian side, and no daily-mean RH on either. That
supports a **regional humidity band** dimension. It does not support the word
"micro-climate", and it does not support a value that traces to a published number on both
sides of the border without a stated derivation.

Two honest options:
- **Ship it as derived and labelled** - name the method, name the two clock hours, call it
  regional not micro, and accept that the value is computed rather than published.
- **Cut it** - if the "never invent or estimate a value" rule is meant strictly, a
  nonlinear derivation off two clock-hour readings interpolated across 25-70 km is exactly
  the kind of number the rule exists to keep out.

That call is a product decision, not a data one. The data side is now fully mapped either way.
