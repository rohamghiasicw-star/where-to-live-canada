# Source verification: language spoken at home + non-profit density

Verified 2026-08-18. Every claim below was tested against the live endpoint on that
date. Where something could not be confirmed it says so explicitly rather than
guessing. Row counts, byte sizes and join rates are measured, not estimated.

App spine at time of testing: **4,226 US places** (`data/us/places.json`, 7-digit
GEOID) and **712 Canadian CSDs** (`data/census.json`, 7-digit CSD code).

---

## Summary table

| # | Source | Granularity | Join to spine | Cost | Verdict |
|---|--------|-------------|---------------|------|---------|
| 1 | ACS **C16001** | Place (SL160) | GEOID, **100% / 4,226** | Free | **USABLE** |
| 2 | StatCan **98-401-X2021005** | CSD | CSD code, **100% / 712** | Free | **USABLE** |
| 3 | IRS **EO BMF** | Mailing city/ZIP | none — needs geocoding | Free | **USABLE WITH WORK** |
| 4 | CRA **List of Charities** | Mailing city/postal | none — needs geocoding | Free | **USABLE WITH WORK** |

The two language sources are drop-in. The two non-profit sources are good data with
a real geocoding problem in front of them.

---

## 1. US — ACS language spoken at home

### The answer: C16001, and only C16001

**Table ID: `C16001`** — "Language Spoken at Home for the Population 5 Years and Over".
Universe: population 5 years and over. 38 estimate variables.

**`B16001` does not work at place level.** This is the important negative finding and
it is proven, not assumed. B16001 is the detailed ~120-language table everyone reaches
for first. I downloaded the whole file (2,786,063 bytes, 3,200 data rows) and counted
the summary levels present:

| Summary level | Rows |
|---|---|
| `795P200` PUMA | 2,486 |
| `5001900` Congressional district | 440 |
| `330M700` CBSA | 184 |
| `0400000` State | 52 |
| `314M700` Metropolitan division | 37 |
| `0100000` Nation | 1 |
| **`1600000` Place** | **0** |

Zero place rows. The detailed-language table is simply not published at SL160.

The Census "Detailed Languages Spoken at Home" special tabulation (2017-2021, 500+
languages) does not rescue this either — per the Census's own product page it is
published for nation, states, **counties with 100,000+ population**, and CBSAs. No
place level. <https://www.census.gov/data/tables/time-series/demo/language-use/2017-2021-lang-tables.html>

So C16001's 12 language groups are the hard ceiling for place-level language data.

### What you actually get (and what you don't)

Variable pattern: `C16001_<3-digit seq>E` for estimates, `M` for margin of error.
Each language occupies 3 consecutive cells: total, speaks English "very well",
speaks English less than "very well". The **total** cell is the one you want.

| Language group | Total cell |
|---|---|
| Total (universe) | `C16001_001E` |
| Speak only English | `C16001_002E` |
| **Spanish** | `C16001_003E` |
| **French, Haitian, or Cajun** | `C16001_006E` |
| German or other West Germanic | `C16001_009E` |
| **Russian, Polish, or other Slavic** | `C16001_012E` |
| Other Indo-European | `C16001_015E` |
| **Korean** | `C16001_018E` |
| **Chinese (incl. Mandarin, Cantonese)** | `C16001_021E` |
| **Vietnamese** | `C16001_024E` |
| **Tagalog (incl. Filipino)** | `C16001_027E` |
| Other Asian and Pacific Island | `C16001_030E` |
| **Arabic** | `C16001_033E` |
| Other and unspecified | `C16001_036E` |

Against your requested list:

- Got as named languages: **Spanish, Chinese, Tagalog, Vietnamese, Arabic, Korean**.
- **French** only as "French, Haitian, or Cajun" — bundled, cannot be separated.
- **Russian — NOT AVAILABLE separately.** It sits inside "Russian, Polish, or other
  Slavic languages". You cannot split it at place level.
- **Portuguese — NOT AVAILABLE separately.** It falls into "Other Indo-European
  languages" along with Hindi, Urdu, Italian, Farsi, Greek and others. Not splittable
  at place level.

If the product needs Russian or Portuguese specifically for the US, that dimension
cannot be built from published place-level data. Canada has them (see §2), so the two
countries will not be symmetric on this. Worth deciding deliberately rather than
discovering later.

### How to pull it — the API will not work, use the bulk file

`api.census.gov` data endpoints returned the **"Missing Key"** HTML page for every
query I tried, including `for=place:*&in=state:06`. Your own `src/us/build_places.py`
header already documents this and says it fails "keyed or not".

- Verified by me: **unkeyed data requests fail.**
- **Could not verify:** whether a request with a valid key succeeds — there is no
  Census API key anywhere in the repo, so I had nothing to test with. I am not
  repeating the "keyed or not" claim as my own finding.
- Verified by me: **metadata endpoints are still open and key-free**, e.g.
  `https://api.census.gov/data/2024/acs/acs5/groups/C16001.json` returned HTTP 200.
  Keep resolving variable IDs from this rather than from memory.

**The working, key-free path** (same mechanism `build_places.py` already uses):

```
https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-c16001.dat
```

- Format: pipe-delimited (`|`) text, UTF-8, first row is the header.
- Size: **70,921,995 bytes** (67.6 MB) for all geographies.
- Filter to places by streaming and keeping lines starting `1600000US` — that drops
  it to **32,330 place rows**, which is every place the ACS publishes.
- **Column naming differs from the API**: the summary file calls it `C16001_E003`,
  the API calls it `C16001_003E`. Same trap `load_acs()` already handles.
- Join key: strip the `1600000US` prefix off `GEO_ID` to get the 7-digit place GEOID.
- Suppression: negative values (`-666666666` etc.) are flags, not numbers. Null them.

### Join test against the real spine

- 4,226 app places, **4,226 matched (100.00%)**, zero missing.
- **4,226/4,226 (100.00%)** have a non-null Spanish estimate.

### Sanity check — the numbers are real

Computed as language total / `C16001_001E`:

| Place | Result | Reality check |
|---|---|---|
| Dearborn, MI | Arabic **48.6%** | Largest Arab-American concentration in the US |
| Monterey Park, CA | Chinese **42.1%** | "The first suburban Chinatown" |
| Daly City, CA | Tagalog **20.1%** | Most Filipino city in the US |
| Hialeah, FL | Spanish **91.9%** | Overwhelmingly Cuban-American |

All four land where they should. The pipeline is producing correct values.

**Licence/cost:** US Government work, public domain. Free, no key, no registration.

**VERDICT: USABLE.** Drops straight into the existing build. The one real limitation
is that Russian and Portuguese cannot be isolated at place level.

---

## 2. Canada — StatCan 2021 mother tongue + language spoken at home

### Product

**`98-401-X2021005`** — Census Profile, 2021 Census of Population, **Census
subdivision** level. This is the exact same product `src/extract_census.py` already
reads, so no new source is being introduced — only new `CHARACTERISTIC_ID`s.

```
https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=005
```

- Downloaded: **196,875,109 bytes** (188 MB) ZIP → `98-401-X2021005_eng_CSV.zip`.
- Inner CSV `98-401-X2021005_English_CSV_data.csv`: **2,590,635,849 bytes** (2.41 GB),
  14,386,308 rows.
- **Encoding is cp1252, not UTF-8** — the trap already noted in `extract_census.py`.
- Join key: `ALT_GEO_CODE` (col 2) = the 7-digit CSD code. `DGUID` = `2021A0005` + code.
  Verified all keys are exactly 7 characters.

Tip: to explore characteristic IDs without touching the 2.41 GB file, pull `GEONO=002`
(CMA/CA level, only 7 MB zipped). The characteristic IDs are identical across geography
levels — that is how the ID list below was built.

### Two parallel blocks, offset by exactly 342

- **Mother tongue** block starts at `393` = "Total - Mother tongue for the total
  population excluding institutional residents - 100% data".
- **Language spoken most often at home** block starts at `735` = "Total - Language
  spoken most often at home ... 100% data".
- `home_id = mother_tongue_id + 342`. I verified this offset holds for all 30
  languages checked — every label matched exactly.

### Characteristic IDs (verified against the published labels)

| Language | Mother tongue | Spoken at home |
|---|---|---|
| English | 396 | 738 |
| French | 397 | 739 |
| Arabic | 507 | 849 |
| Vietnamese | 519 | 861 |
| Tagalog (Pilipino, Filipino) | 537 | 879 |
| Tamil | 551 | 893 |
| Polish | 569 | 911 |
| **Russian** | 570 | 912 |
| Ukrainian | 579 | 921 |
| German | 589 | 931 |
| Greek | 606 | 948 |
| Gujarati | 611 | 953 |
| Hindi | 612 | 954 |
| Punjabi (Panjabi) | 621 | 963 |
| Urdu | 625 | 967 |
| Italian | 640 | 982 |
| **Portuguese** | 641 | 983 |
| Spanish | 643 | 985 |
| Korean | 647 | 989 |
| Mandarin | 686 | 1028 |
| Yue (Cantonese) | 690 | 1032 |

Rollup parents, when you want the family rather than the leaf:

| Family | Mother tongue | Spoken at home | Children |
|---|---|---|---|
| Chinese languages | 684 | 1026 | Hakka 685, Mandarin 686, Min Dong 687, Min Nan 688, Wu 689, Yue 690, Chinese n.o.s. 691, n.i.e. 692 |
| Persian languages | 632 | 974 | Dari 633, Iranian Persian 634, Persian (Farsi) n.o.s. 635 |

**Watch this one:** for Farsi use the parent `632` ("Persian languages"), not `635`
("Persian (Farsi), n.o.s."). The leaf is only the residual and reads implausibly low
(0.1-0.3% in Persian-heavy CSDs). Same logic for Chinese — `684` if you want all
Chinese languages together, `686`/`690` if you want Mandarin and Cantonese apart.

Canada is **much** richer than the US here: Mandarin and Cantonese split, plus Punjabi,
Portuguese, Russian, Urdu, Hindi, Gujarati, Tamil and Persian all as distinct
languages. None of those are separable in the US data.

### Join test against the real spine

- 712 app CSDs, **712 matched (100.00%)**, zero missing.
- Non-null mother-tongue total: **712/712 (100.00%)**.
- Non-null Punjabi: **712/712**. Non-null home-language Spanish: **712/712**.
- Extraction across all CSDs yields **5,161 CSDs** carrying language data — far more
  than the 712 needed.

### Sanity check — mother tongue as % of CSD total

| CSD | Result | Reality check |
|---|---|---|
| Surrey, BC (5915004) | Punjabi **22.7%** | Largest Punjabi population in Canada |
| Richmond, BC (5915015) | Cantonese **21.5%**, Mandarin **21.1%** | Majority ethnic-Chinese city |
| Brampton, ON (3521010) | Punjabi **21.7%** | Major Punjabi centre |
| Markham, ON (3519036) | Cantonese **21.3%**, Mandarin **14.6%** | Major Chinese centre |
| Montréal, QC (2466023) | Arabic **5.7%**, Spanish **4.6%** | Matches known profile |
| Toronto, ON (3520005) | Mandarin 4.1%, Cantonese 3.7%, Portuguese 2.2% | Matches known profile |

Cross-checked at CMA level too: Abbotsford-Mission Punjabi 19.25%, Winnipeg Tagalog
5.43%, Bathurst NB French 64.42%. All correct.

**Licence/cost:** Statistics Canada Open Licence. Free, no registration.

**VERDICT: USABLE.** Same file the build already downloads — this is close to free to add.

---

## 3. US — IRS Exempt Organizations Business Master File

### Download

Landing page: <https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf>

Four regional CSVs (there are also per-state files `eo_<st>.csv`, better for
incremental refreshes):

| File | URL | Bytes | Rows |
|---|---|---|---|
| Region 1 (CT ME MA NH NJ NY RI VT) | `https://www.irs.gov/pub/irs-soi/eo1.csv` | 48,629,769 | 278,014 |
| Region 2 (DE DC IL IN IA KY MD MI MN NE NC ND OH PA SC SD VA WV WI) | `https://www.irs.gov/pub/irs-soi/eo2.csv` | 125,728,575 | 719,134 |
| Region 3 (AL AK AR AZ CA CO FL GA HI ID KS LA MS MO MT NV NM OK OR TX TN UT WA WY) | `https://www.irs.gov/pub/irs-soi/eo3.csv` | 164,634,273 | 955,286 |
| Region 4 (international + other) | `https://www.irs.gov/pub/irs-soi/eo4.csv` | 861,858 | 4,906 |
| **Combined** | | **339,853,692** (324 MB) | **1,957,340** |

My combined count of **1,957,340** matches the record count the IRS states on its own
page exactly. Current extract date per the IRS: **August 11, 2026**. `Last-Modified`
headers read 10 Aug 2026, so this is a live, actively maintained file.

Format: CSV, 28 columns —
`EIN, NAME, ICO, STREET, CITY, STATE, ZIP, GROUP, SUBSECTION, AFFILIATION,
CLASSIFICATION, RULING, DEDUCTIBILITY, FOUNDATION, ACTIVITY, ORGANIZATION, STATUS,
TAX_PERIOD, ASSET_CD, INCOME_CD, FILING_REQ_CD, PF_FILING_REQ_CD, ACCT_PD, ASSET_AMT,
INCOME_AMT, REVENUE_AMT, NTEE_CD, SORT_NAME`

Code definitions: <https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf>

### Does it carry usable geography? Yes — but not a GEOID

Measured across all 1,957,340 rows:

- `CITY` populated: **100.0%**
- `STATE` populated: **100.0%** (63 distinct values incl. territories and blanks)
- `ZIP` populated: **100.0%** — but in **ZIP+4** form (`01069-1507`). Split on `-` for ZIP5.

There is **no Census place GEOID and no county code**. This is the whole difficulty.

### Is NTEE populated enough to filter to volunteerable orgs? Yes

- `NTEE_CD` populated: **1,382,893 / 1,957,340 = 70.7%**.
- The remaining **29.3% have no NTEE code at all** and will be silently dropped by any
  NTEE filter. That is a real, non-uniform bias — treat the output as "orgs with a
  known NTEE code", not "all orgs".

Major-group counts (first character of `NTEE_CD`), which is what matters for a
volunteering dimension:

| Code | Meaning | Count |
|---|---|---|
| A | Arts, Culture & Humanities | 118,457 |
| B | Education | 185,932 |
| C | Environment | 28,634 |
| **D** | **Animal-Related** (shelters, rescues) | **41,512** |
| E | Health Care | 46,039 |
| F | Mental Health & Crisis | 27,521 |
| **K** | **Food, Agriculture & Nutrition** (food banks, community gardens) | **20,436** |
| L | Housing & Shelter | 31,019 |
| N | Recreation & Sports | 113,170 |
| O | Youth Development | 58,179 |
| **P** | **Human Services** | **154,309** |
| S | Community Improvement | 72,380 |
| T | Philanthropy & Grantmaking | 105,079 |
| X | Religion-Related | 204,365 |

The specific categories you named are all directly addressable: animal shelters = `D`,
food banks and community gardens = `K`, plus `P` human services and `L` housing/shelter.

### Filtering out the entities nobody can volunteer at

Two clean structural filters, both fully populated:

- `SUBSECTION = '03'` → 501(c)(3) orgs: **1,634,789**.
- `FOUNDATION = '04'` → private non-operating foundations (grantmaking shells):
  **120,719**, excludable.
- `STATUS = '01'` → active: **1,949,212**.

A combined filter of 501(c)(3) + public-charity `FOUNDATION` codes (10-16) + a
program-type NTEE major group yields **901,962 organizations** — a credible
denominator for a volunteering-density measure.

### The join is the problem

Naive `CITY` + `STATE` matching against the 4,226-place spine, normalized
(uppercase, punctuation stripped):

- **1,252,534 / 1,957,340 = 64.0% matched.**
- Only 437 landed on an ambiguous name — name collisions are *not* the issue.

The missing 36% is **systematically biased against large cities**, which is the worst
possible bias for this metric. The top unmatched groups show exactly why:

| IRS `CITY` | Orgs | Why it fails |
|---|---|---|
| `BROOKLYN` NY | 15,834 | Borough, not a Census place (part of New York city) |
| `SAINT LOUIS` MO | 9,169 | Spine has `St. Louis` |
| `LOUISVILLE` KY | 4,645 | Spine has `Louisville/Jefferson County` |
| `BRONX` NY | 4,065 | Borough, not a Census place |
| `NASHVILLE` TN | 4,046 | Spine has `Nashville-Davidson` |
| `HONOLULU` HI | 3,752 | Census name is `Urban Honolulu` CDP |
| `SAINT PAUL` MN | 3,484 | Spine has `St. Paul` |
| `COLORADO SPGS` CO | 3,093 | USPS abbreviation |
| `SALT LAKE CTY` UT | 2,477 | USPS abbreviation |
| `FT LAUDERDALE` FL | 2,185 | USPS abbreviation |

Three separate failure classes: USPS abbreviations, consolidated city-county names,
and postal cities that are not Census places at all. String matching cannot fix this
reliably, and a half-fixed match silently under-counts the biggest cities.

**The path that does work**, verified today, both key-free:

1. **Batch geocode** — `POST` a CSV of `id,street,city,state,zip` (up to 10,000 rows)
   to `https://geocoding.geo.census.gov/geocoder/geographies/addressbatch` with
   `benchmark=Public_AR_Current&vintage=Current_Current`. Tested with 3 addresses,
   all returned `Match/Exact` with lat/lon. **It returns state, county, tract and
   block but NOT the place** — so this step gives you coordinates, not the GEOID.
2. **Coordinates → place GEOID.** Verified that
   `https://geocoding.geo.census.gov/geocoder/geographies/coordinates` with
   `layers=Incorporated Places` returns the 7-digit GEOID (tested: `-122.083521,
   37.423120` → GEOID `0649670`, "Mountain View city"). One request per point is far
   too slow for 1.96M orgs, so do this step **offline as a point-in-polygon against
   the TIGER place shapefile** (`cb_2024_us_place_500k.zip`) — the build already
   consumes TIGER files, so the machinery exists.

~1.96M addresses is roughly 196 batch requests. Feasible, not instant.
**Not verified:** end-to-end runtime, or the match rate the geocoder achieves on real
IRS addresses at volume. I only tested 3 addresses.

### Caveat worth building around

The BMF address is the org's **mailing address**, not where it operates. PO boxes,
a treasurer's home, and accountants' offices are common. A national charity
headquartered in one town inflates that town's count. For a *volunteering ecosystem*
signal this is a genuine validity limit, not just noise — consider excluding orgs
above a revenue threshold, or normalizing per capita and treating outliers with
suspicion.

**Licence/cost:** US Government work, public domain. Free, no key.

**VERDICT: USABLE WITH WORK.** The data is excellent — fresh, complete on
city/state/ZIP, and NTEE-filterable to real volunteering categories. The work is
entirely in the geocoding join, and it is not optional: naive city matching gets 64%
and systematically loses the largest cities.

---

## 4. Canada — CRA List of Charities

### Bulk download: yes

Dataset: **"2024 List of charities"** on open.canada.ca, package id
`80c00cdb-1358-415c-bb8b-0de7f12675b8`. Annual releases exist continuously from
**1990 through 2024**; 2024 is the newest.

The file you want is **Identification**:

```
https://open.canada.ca/data/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8/resource/694fdc72-eae4-4ee0-83eb-832ab7b230e3/download/ident_2024_updated.csv
```

- Format: CSV. Size: **13,203,780 bytes** (12.6 MB). **83,761 charities.**
- Columns: `BN, Category, Sub Category, Designation, Legal Name, Account Name,
  Address Line 1, Address Line 2, City, Province, Postal Code, Country`

22 other CSVs ship in the same package (financial data, directors, programs,
compensation, web addresses) if a richer signal is ever wanted.

Supporting docs:
- Codes list: `.../resource/e9f81074-9fc7-456f-8ce1-6fd101b77963/download/codes_en.pdf`
- Data dictionary: `.../resource/b5c8bd25-fd2d-4aec-a220-a233f88157aa/download/open-data-data-dictionary-v2.0_eng.pdf`

### Does it carry city? Yes — 100%

Measured across all 83,761 rows:

- `City` populated: **100.0%**
- `Country = CA`: **100.0%**
- `Postal Code` present, `Province` present. Provincial spread is sane:
  ON 30,570 / QC 15,472 / BC 12,040 / AB 9,181 / MB 4,574 / SK 3,952 / NS 3,501 /
  NB 2,469 / NL 1,131 / PE 569 / YT 132 / NT 101 / NU 35.

### Filtering to volunteerable orgs

`Designation` is fully populated and cleanly separates operating charities from
grantmaking shells (decoded from the codes PDF):

| Code | Meaning | Count |
|---|---|---|
| **C** | **Charitable Organization** (runs its own programs) | **72,356** |
| A | Public Foundation | 4,639 |
| B | Private Foundation | 6,766 |

`Designation = 'C'` is the direct analogue of the IRS public-charity filter.

`Category` (4-digit) gives topic. Decoded, the volunteering-relevant ones:

| Code | Category | Count |
|---|---|---|
| 0001 | Organizations Relieving Poverty | 11,130 |
| 0160 | Community Resource | 4,809 |
| 0170 | Environment | (in file) |
| 0175 | Agriculture | (in file) |
| 0180 | Animal Welfare | 1,037 |
| 0190 | Arts | 2,652 |
| 0200 | Public Amenities | 6,218 |
| 0210 | Foundations (exclude) | 8,490 |
| 0030 | Christianity | 25,350 |

`Sub Category` goes finer still and maps almost exactly onto the volunteering use
case — e.g. under category 0001: `0004` operating a food bank, `0006` operating a
shelter, `0010` providing meals, `0009` low-cost housing.

Note the shape of the sector: 0030 Christianity alone is 25,350 of 83,761. A raw
count is largely a count of churches unless categories are filtered deliberately.

### The join — same problem as the IRS, and harder

Available keys: `City`, `Province`, `Postal Code`. **No CSD code.**

The official postal-code → CSD crosswalk is StatCan's **Postal Code Conversion File
(PCCF, 92-154-X)**, and it is **not freely available**. Per the StatCan catalogue
page, direct distribution ceased in February 2018; it now reaches only StatCan
partners and Data Liberation Initiative members, and the general public must license
it from Canada Post. So the clean crosswalk is paywalled.

**Not verified:** I did not test a free geocoding route for Canadian addresses, and
I did not measure a city-name match rate against the 712-CSD spine. Given that the
US city-name match managed only 64% against a much larger spine, and the Canadian
spine covers 712 of 5,161 CSDs, I would expect city-name matching to be **worse**
here, not better — but that is an expectation, not a measurement. Test it before
committing.

A likely-workable free path, untested: geocode `Address Line 1 + City + Province +
Postal Code` with an open geocoder, then point-in-polygon against the StatCan CSD
boundary file (the build already holds `data/csd_coords.json` for all 5,161 CSDs).

**Licence/cost:** Open Government Licence - Canada. Free, no registration.

**VERDICT: USABLE WITH WORK.** Clean, small, complete file with better built-in
category coding than the IRS version. The blocker is the same geocoding join, made
harder because the official postal→CSD crosswalk is licensed rather than open.

---

## What I could not confirm

Listed plainly so none of it gets mistaken for verified fact:

1. Whether a **valid Census API key** makes `api.census.gov` data endpoints work. No
   key exists in the repo to test with. Unkeyed requests definitely fail.
2. The **end-to-end runtime and real-world match rate** of geocoding 1.96M IRS
   addresses. Only 3 sample addresses were tested against the batch geocoder.
3. Any **free postal-code → CSD crosswalk** for Canada. PCCF is confirmed licensed;
   I did not find and test an open substitute.
4. The **city-name match rate for CRA charities** against the 712-CSD spine — not
   measured.

## Reproduction artifacts

Working files from this verification (scratch, not committed):

- `/tmp/c16001_places.dat` — C16001 filtered to 32,330 place rows
- `/tmp/g5/csd_lang.json` — 5,161 CSDs × mother-tongue + home-language values
- `/tmp/g2/chars.json` — all 2,631 StatCan characteristic IDs and labels
- `/tmp/eo_all.csv` — 1,957,340 IRS BMF rows combined
- `/tmp/cra_ident_2024.csv` — 83,761 CRA charities
