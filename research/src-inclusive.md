# "Inclusive vibe" dimension - source verification

Verified 2026-08-21. Every number below was measured off a real HTTP response or read out of a
real downloaded file in this session. Nothing is estimated except where the word "extrapolated"
appears, and those cases are labelled inline. Anything I could not confirm is in the
**COULD NOT CONFIRM** section at the bottom, not in the body.

**Place counts I measured, not assumed:** `data/us/places.json` = **4,226 rows**;
`data/allplaces.json` = **712 rows** (Canada, CSD-keyed). The brief said 4,197 US and 710
Canadian; the small gaps are presumably a downstream filter. All US coverage percentages below
are against the 4,226 actually in the file.

---

## VERDICT TABLE

| # | Source | Verdict |
|---|---|---|
| 1 | HRC Municipal Equality Index 2025 | **USABLE WITH WORK, but only for 10.6% of places.** PDF-only, no licence. Real policy measure, real scores, tiny footprint. |
| 2 | MAP LGBTQ Policy Score / Equality Maps | **NOT USABLE at place level.** State-level by design. Confirmed in MAP's own words. |
| 2b | MAP Local Nondiscrimination Ordinances city listing | **NOT USABLE as a score.** Structurally excludes every city in a protective state, so absence means two opposite things. |
| 3 | FBI UCR/NIBRS hate crime bulk file | **NOT USABLE.** Agency-level, voluntary, no zero-fill, median 1 incident per reporting city per year. |
| 3b | BJS LEAIC ORI-to-FIPS-place crosswalk | **NOT USABLE.** 2012 vintage and login-walled at ICPSR. |
| 3c | FBI CDE agency API (free crosswalk substitute) | Works, free, has lat/lon - but it only fixes the join, not the data underneath it. |
| 4 | StatCan 35-10-0191 hate crime (CMA) | **NOT USABLE.** Finest published geography is the CMA - 41 of them for 712 CSDs. 64.2% of places get nothing. |
| 4b | StatCan 35-10-0066 / 0067 hate crime | **NOT USABLE.** 9 geographies total. |
| 4c | Canadian municipal inclusion index | **Does not exist.** No Canadian equivalent of the MEI found. |

**Bottom line up front: cut this dimension.** Reasoning in the final section.

---

## 1. HRC Municipal Equality Index (MEI)

### 1a. Is it downloadable as a table?

**No. It is PDF-only, one PDF per city.** There is no CSV, XLSX, JSON, or API anywhere on
hrc.org or reports.hrc.org. I checked:

| URL | HTTP | Bytes | What it is |
|---|---|---|---|
| `https://www.hrc.org/resources/municipal-equality-index` | 200 | 173,967 | Landing page. Zero `.csv`/`.xlsx`/`.json` links. |
| `https://reports.hrc.org/municipal-equality-index-2025` | 200 | 320,892 | The full 2025 report as a web page. Only downloadable assets are 7 issue-brief / city-spotlight PDFs. |
| `https://www.hrc.org/resources/mei-see-your-cities-scores` | 200 | 130,232 | "See your city's score" - it is just a list of 50 links to per-state pages. No API, no search endpoint, no Algolia/Elastic call. |
| `https://www.hrc.org/resources/mei-state/{state}/` | 200 | 132,727 - 485,193 | 50 pages, one per state. These are where the actual scorecard links live. |

The data lives in per-city one-page PDFs on S3:

```
https://hrc-prod-requests.s3-us-west-2.amazonaws.com/files/documents/
  MEI-Scorecard-Assets/MEI-25-Scorecards/MEI-2025-{City}-{State}.pdf
```

**The URL pattern is not reliable.** Of the 509 distinct 2025 scorecard URLs I harvested:

- 506 use `MEI-2025-{City}-{State}.pdf`
- 1 uses `2025-MEI-Hoover-Alabama.pdf` (order flipped)
- 2 use a bare `{City}-{ST}.pdf` - `Hayward-CA.pdf`, `Salt-Lake-City-UT.pdf`

So you cannot template the URL. You have to scrape the 50 state pages and take the hrefs.

### 1b. Extraction actually works

I downloaded 6 scorecards and ran `pdftotext -layout` on all 6. **6/6 parsed cleanly**, same
layout every time.

| PDF | Bytes | Extracted line |
|---|---|---|
| `MEI-2025-Birmingham-Alabama.pdf` | 211,191 | `TOTAL SCORE 94 + TOTAL FLEX SCORE 12 = Final Score 100` |
| `MEI-2025-Fort-Worth-Texas.pdf` | 211,077 | `TOTAL SCORE 82 + TOTAL FLEX SCORE 8 = Final Score 90` |
| `MEI-2025-Warwick-Rhode-Island.pdf` | 211,102 | `TOTAL SCORE 60 + TOTAL FLEX SCORE 4 = Final Score 64` |
| `MEI-2025-Casper-Wyoming.pdf` | 211,065 | `TOTAL SCORE 87 + TOTAL FLEX SCORE 5 = Final Score 92` |
| `MEI-2025-Henderson-Nevada.pdf` | 211,213 | `TOTAL SCORE 89 + TOTAL FLEX SCORE 12 = Final Score 100` |
| `MEI-2025-Northampton-Massachusetts.pdf` | 211,194 | `TOTAL SCORE 90 + TOTAL FLEX SCORE 15 = Final Score 100` |

Mean measured size across those 6 = **211,140 bytes**. **Extrapolated** whole-set download
(509 x 211,140) ≈ **107 MB**. That number is an extrapolation from 6 measured files, not a
measurement - flagged as required.

Subscores are also extractable. Birmingham's card gave, verbatim, per category:
Non-Discrimination Laws `30 out of 30`, Municipality as Employer `23 out of 28`,
Municipal Services `12 out of 12`, Law Enforcement `22 out of 22`,
Leadership on LGBTQ+ Equality `7 out of 8`, plus FLEX rows.

The PDFs are Canva exports (`/Producer (Canva)`, `/Author (Cathryn Oakley)`,
`/CreationDate (D:20251114...)`), 1 page each, text layer intact - no OCR needed.

### 1c. Coverage and year

**Most recent edition: 2025**, published 14 Nov 2025 (from the PDF `CreationDate`), 14th
annual edition.

HRC's own count, quoted verbatim from `reports.hrc.org/municipal-equality-index-2025`:

> "The 2025 Municipal Equality Index rates 506 municipalities of varying sizes drawn from
> every state in the nation."

**I counted 510 distinct city+state pairs / 509 distinct scorecard PDF URLs** by scraping all
50 state pages. The 3-4 row gap between my count and HRC's stated 506 is unexplained; I am
reporting both rather than picking one.

**Washington, D.C. is deliberately excluded.** HRC's own words:

> "Washington, D.C. is a federal district. This means that it has powers and limitations so
> significantly different from the municipalities the MEI rates that the comparison would be
> unfair... Washington, D.C. is included in HRC's annual State Equality Index."

Confirmed operationally: `https://www.hrc.org/resources/mei-state/district-of-columbia/`
returns **404** (also tried `washington-dc`, `dc`, `district-columbia` - all 404).
`puerto-rico` also 404s.

### 1d. What it actually measures - it is a POLICY scorecard, confirmed

Confirmed. It scores the **municipal government's laws and policies**, not residents'
experience. The five categories, read off a real scorecard PDF:

1. **Non-Discrimination Laws** - does city/county/state law prohibit SO/GI discrimination in
   employment, housing, public accommodations
2. **Municipality as Employer** - non-discrimination in city employment, trans-inclusive
   healthcare benefits, city contractor NDO, inclusive workplace
3. **Municipal Services** - human rights commission, NDO enforcement by commission, LGBTQ+
   liaison to the city executive
4. **Law Enforcement** - police LGBTQ+ liaison/task force, and whether the city **reported
   hate crime statistics to the FBI** (12 of 22 points)
5. **Leadership on LGBTQ+ Equality** - public position on equality, pro-equality
   legislative/policy efforts, openly LGBTQ+ elected/appointed leaders

Plus FLEX bonus points. Total capped at 100 ("CANNOT EXCEED 100", printed on the card).

Every single line item is a government action. **There is no resident survey, no
lived-experience component, no public-opinion component.** HRC frames it as measuring
"a demonstrated commitment to equality through laws and policies".

This is the honest framing to carry into the app if you ship it: it is a measure of what
city hall has done, not of how it feels to live there.

### 1e. How cities are selected - and why this is the real problem

HRC's verbatim selection criteria:

> "These include the 50 state capitals, the 200 largest cities in the United States, the five
> largest cities or municipalities in each state, the cities home to the state's two largest
> public universities (including undergraduate and graduate enrollment), 75 cities and
> municipalities that have high proportions of same-sex couples and 98 cities selected by HRC
> and Equality Federation state groups members and supporters."

Two of those six criteria are **non-random and self-selecting**: "high proportions of same-sex
couples" and "selected by HRC and Equality Federation... members and supporters". A city gets
rated partly because it is already gay-friendly or because a local advocate asked for it.

**Absence from the MEI is not a low score. It is no data.** If you fill missing places with 0,
or with a state mean, you are inventing the number for 89% of the app.

**Three more things HRC says in the same passage that matter a lot:**

> "Significant overlap between these categories of cities brings the total number of cities
> rated in the 2025 MEI to 506, **which has been the number of cities rated since 2016**.
> In 2012, the MEI rated 137 cities; in 2013, 291; in 2014, 353; and in 2015, we rated 408
> cities."

**The city set has been frozen since 2016.** Coverage is not going to grow. 10.6% is the
ceiling, not a starting point you can wait out.

> "The 75 cities with the highest proportions of same-sex couples are drawn from an analysis of
> the **2010 Census** results by the Williams Institute at the UCLA School of Law..."

One of the six selection criteria is anchored to a **2010** analysis - 16 years stale.

> "some of these small 'cities' are in fact unincorporated census-designated places. In that
> case, **we rated the laws and policies of the applicable incorporated local government (the
> entity actually rated, often the county**, will be clearly indicated)."

This is a data-integrity landmine and it explains the parenthetical names in my unmatched list.
For an unknown number of rows, **the score describes a county government but is labelled with a
CDP's name**. If you joined `Guerneville (Sonoma County) CA` to the Guerneville CDP, you would
be telling users that Sonoma County's policies are Guerneville's. Those rows have to be
identified and either dropped or re-attributed by hand.

### 1f. The join - I actually ran it

Join key is **name + state abbreviation**. There is no GEOID, no FIPS, no lat/lon anywhere in
the MEI product.

I ran the join for real: normalised both sides (lowercase, strip
city/town/village/township/borough/municipality/CDP, strip non-alphanumerics) and matched
against `data/us/places.json`.

```
places in app:                                    4,226
MEI 2025 cities:                                    510
MATCHED to an app place by norm(name)+state:        449
UNMATCHED:                                           61
=> % of app places that would get an MEI score:    10.6%
```

**449 of 4,226 places = 10.6% coverage. 89.4% get nothing.**

The 61 unmatched are instructive about how brittle a name join is:

- **Counties, not places**: `Fairfax County VA`, `Hawaii County HI`, `Honolulu County HI`,
  `Kauai County HI`, `Maui County HI`, `Kalawao County HI`
- **Parenthetical disambiguation HRC invented**: `Arlington (Arlington County) VA`,
  `Columbia (Howard County) MD`, `Enterprise (Clark County) NV`,
  `Guerneville (Sonoma County) CA`, `Metairie (Jefferson County) LA`,
  `Eldorado at Santa Fe (Santa Fe County) NM`
- **Consolidated city-counties named differently by Census**: HRC says `Louisville KY`,
  Census says `Louisville/Jefferson County`. HRC `Nashville TN` vs Census `Nashville-Davidson`.
  HRC `Lexington KY` vs Census `Lexington-Fayette`. HRC `Butte-Silver MT` (truncated).
- **A typo in HRC's own data**: the Illinois page lists **`Joilet`**. The Census place is
  `Joliet` (GEOID 1738570). Confirmed by grep against `meistates/illinois.html`. It appears
  three times, so it is systematic, not a rendering artefact.
- **CDPs and unincorporated places** that are not Census "places" in the app's set at all
- **New England towns** (`Barre VT`, `Brattleboro VT`, `Castleton VT`, `Essex VT`,
  `Montpelier VT`, `Fairfield CT`, `Kingston RI`, `Narragansett RI`) - town/place mismatch

Also found **6 name+state collisions inside the app's own place file**
(`tonawanda NY`, `university FL`, `kailua HI`, `hotsprings AR`, `fairwood WA`, +1), so a
name join is ambiguous in both directions.

A hand-built crosswalk could recover maybe 40-55 of the 61 - but that is a manual mapping
exercise you would have to redo every November when the new edition lands.

### 1g. Licence and cost

**No open licence. This is the hard blocker.**

- Free to view. No paywall, no login on any of the URLs above.
- The report page's schema.org block carries `"copyrightHolder": HRC, "copyrightYear": "2024"`.
- The only rights page on hrc.org is a **DMCA copyright complaint notice**
  (`https://www.hrc.org/human-rights-campaign-copyright-complaint-notice`, HTTP 200, 99,609
  bytes). It asserts copyright and a takedown process. There is **no** Creative Commons
  licence, no open-data licence, no terms-of-use page granting redistribution.

Scraping 509 copyrighted PDFs and republishing the extracted scores in a commercial product
is a rights question, not a technical one. Attribution alone does not clear it.

### 1h. Verdict

**USABLE WITH WORK - but only if you accept 10.6% coverage and get the rights sorted.**

The data is real, defensible, well-documented, and it genuinely measures municipal LGBTQ+
inclusion policy. It is the single best thing that exists for this dimension in the US.
It is also PDF-only, unlicensed, name-joined, and covers one place in ten.

---

## 2. Movement Advancement Project (MAP)

MAP moved from `lgbtmap.org` to **`mapresearch.org`** - `https://www.lgbtmap.org/equality-maps`
now 302s to `https://mapresearch.org/equality/` (confirmed: HTTP 200, 662,000 bytes, final URL
`https://mapresearch.org/equality/`).

### 2a. Is there a downloadable dataset?

**No bulk download of any kind.** No CSV, XLSX, JSON, or API on any page I fetched. MAP's own
data-request page says, verbatim:

> "Our Equality Maps data are always available online and updated in real-time. MAP's website
> is always the most up-to-date version of our data."

i.e. the website *is* the deliverable. Formal requests go through a form, and:

> "request fulfillment is up to the discretion of our team, and some data may not be available"

Source: `https://mapresearch.org/about/methodology/equality-program-data-requests/`
(HTTP 200, 209,185 bytes).

### 2b. Geography - state, not municipal

MAP's own words:

> "The LGBTQ Policy Score is a summary measure across 50+ LGBTQ-related laws and policies
> currently on the books in each state. MAP tracks these policies across all 50 states, the
> District of Columbia (D.C.), and the five U.S. territories."

And from `https://mapresearch.org/about/methodology/` (HTTP 200, 238,603 bytes):

> "By providing in-depth policy scores by state..."

**MAP's scoring product is state-level. Full stop.** For 4,226 US places that means 51 distinct
values. That is not a place-level dimension, it is a state colour-in.

MAP is also explicit that its score is *not* a vibe measure:

> "the policy score only looks at existing laws and policies and is therefore only one measure
> of LGBTQ equality and experiences. The scores and maps do not reflect active legislation
> that has been proposed but not passed, nor does it reflect social climate, public opinion,
> the efforts of advocates..."

### 2c. The one municipal thing MAP has - and why it still fails

`https://mapresearch.org/equality-map/local-nondiscrimination-ordinances/`
(HTTP 200, **1,271,929 bytes**) has a **"City and County Listing"** tab with the full list
inline in the HTML. I scraped it:

- **58** `City and County Listing:` blocks (one per state per SO/GI sub-map)
- **427** distinct municipality strings
- of which **57** are counties/boroughs/parishes and **370** are city-ish
- **109** carry an asterisk = partial protections only

MAP's own headline number, verbatim:

> "As of January 1, 2026, there are 21 states, Washington D.C. ... and at least 390
> municipalities that fully and explicitly prohibit discrimination against LGBTQ people in
> employment, housing, and public accommodations."

**The killer sentence, also verbatim:**

> "Note this count of municipalities does not include municipalities in states with statewide
> protections, or municipalities with only partial protection."

I verified this operationally. **None** of these are in the listing:
Los Angeles, San Francisco, Oakland, Sacramento, Seattle, Boston, New York, Denver, Chicago,
Portland, Minneapolis. All 11 absent.

So absence from the list means *either* "this city has no LGBTQ+ protections" *or* "this city
is in California and the whole state already protects you". Those are opposite meanings sharing
one encoding. You cannot build a per-place score on a field where the null is ambiguous.

You could in principle reconstruct it: state-has-protection OR city-is-on-the-list. But then
~89% of the signal is just the state map, which is dimension #2 again.

### 2d. Licence and cost

Free, no paywall, no login. MAP's words:

> "You do not have to pay to access our data. However, we are a very small, nonprofit team with
> limited resources... If we can provide the data you request, we will likely ask if you have
> any funding available to support this request."

No Creative Commons or open-data licence stated. MAP asks for a specific citation format:

> "Movement Advancement Project. 'Equality Maps: Local Nondiscrimination Ordinances.'
> https://mapresearch.org/map-sections/overview/. Accessed August 21, 2026."

### 2e. MAP's ICPSR deposit - checked, also state-level

`https://www.icpsr.umich.edu/web/RCMD/studies/37877` (HTTP 200, 74,422 bytes) -
*Mapping LGBTQ Equality: 2010 to 2020*. Its own summary:

> "presented the status of LGBTQ equality at the U.S. **state level** by examining a policy
> tally by the Movement Advancement Project (MAP), and encompassed nearly 40 LGBTQ-related laws
> and policies across all 50 states, the District of Columbia, and the five U.S. territories
> as of January 1, 2020."

State-level, snapshot at 2010 and 2020, so 6 years stale. Not municipal.

### 2f. Verdict

**MAP LGBTQ Policy Score: NOT USABLE** - state-level by design, no download, 51 values for
4,226 places.

**MAP Local NDO city listing: NOT USABLE as a place score** - scrapeable, but its null is
ambiguous by construction and it omits every city in the 21 protective states, including
almost every big blue city.

---

## 3. US federal / academic

### 3a. FBI UCR/NIBRS hate crime - the bulk file, downloaded and read

This one I have in full on disk.

| | |
|---|---|
| Discovery endpoint | `https://cde.ucr.cjis.gov/LATEST/s3/signedurl?key=additional-datasets/hate-crime/hate_crime.zip` (HTTP 200, returns a 15-min presigned S3 URL) |
| Actual file | `cde-prd-data.s3.us-gov-east-1.amazonaws.com/additional-datasets/hate-crime/hate_crime.zip` |
| **Measured download** | **5,848,445 bytes zipped** |
| Members | `hate_crime.csv` (71,229,707 bytes) + `Hate Crime Methodology.pdf` (663,702 bytes), both dated 2026-07-23 |
| Rows | **277,135** data rows |
| Years | **1991 - 2025** |
| Licence / cost | US federal government work, public domain. Free, no login. |

Header, read off the real file:

```
incident_id,data_year,ori,pug_agency_name,pub_agency_unit,agency_type_name,state_abbr,
state_name,division_name,region_name,population_group_code,population_group_description,
incident_date,adult_victim_count,juvenile_victim_count,total_offender_count,
adult_offender_count,juvenile_offender_count,offender_race,offender_ethnicity,victim_count,
offense_name,total_individual_victims,location_name,bias_desc,victim_types,
multiple_offense,multiple_bias
```

(Yes, `pug_agency_name` is misspelled in the FBI's own header.)

**Geography published: the law enforcement agency (ORI code). Not a place. Not a county.
Not a tract.** Agency types present, all years:

```
City 220,084 | County 40,129 | University or College 9,340 | State Police 3,664
Other 2,108 | Federal 982 | Other State Agency 647 | Tribal 181
```

Bias categories are rich and directly on-dimension - measured counts, all years:
`Anti-Gay (Male) 27,423`, `Anti-Lesbian, Gay, Bisexual, or Transgender (Mixed Group) 10,466`,
`Anti-Lesbian (Female) 5,495`, `Anti-Transgender 2,730`, `Anti-Gender Non-Conforming 995`,
`Anti-Bisexual 810`, `Anti-Heterosexual 690`. Plus race/religion categories
(`Anti-Black or African American 91,934`, `Anti-Jewish 36,281`, etc.).

### 3b. The reporting-coverage problem, measured rather than asserted

This is the well-known problem and here it is in numbers I computed from the file itself.

**Reporting is voluntary.** From the bundled `Hate Crime Methodology.pdf` (last updated
01/16/2026), verbatim:

> "The law enforcement agencies that **voluntarily participate** in the Hate Crime Statistics
> Data Collection..."

> "the UCR Program **does not apply offense estimation procedures to account for missing data
> from agencies that do not participate** in the Hate Crime Statistics Program."

> "the reader is cautioned against making simplistic comparisons between the statistical data
> of this data collection and that of others with differing methodologies or even comparing
> individual reporting units solely on the basis of their agency type."

That last line is the FBI telling you not to do the exact thing a per-place score would do.

**Distinct agencies appearing in the file, by year (measured):**

| Year | Incidents | Distinct ORIs with >=1 incident |
|---|---|---|
| 2020 | 9,965 | 2,760 |
| 2021 | 11,069 | 3,077 |
| 2022 | 11,918 | 3,208 |
| 2023 | 12,161 | 3,251 |
| 2024 | 11,932 | 3,174 |
| 2025 | 10,881 | 3,067 |

**The file contains incidents only.** An agency that filed a Zero Report is recorded by the FBI
as zero, but **it does not appear in this CSV**. So a missing agency is indistinguishable
between "reported zero" and "did not report at all". There is no participation flag in the file
and I could not find a participation file on the CDE S3 (probed 11 plausible keys, all returned
`{}`).

**And the counts that do exist are statistical noise at place level.** For 2025, City agencies
only:

```
city agencies reporting >=1 incident:              2,114
median incidents per reporting city agency:            1
agencies reporting exactly 1 incident:  1,101  =  52.1%
agencies reporting <= 2 incidents:                 71.1%
agencies reporting <= 5 incidents:      1,874  =  88.6%
top: Los Angeles 562, New York 456, Las Vegas Metro 165, Portland 160, Phoenix 140
```

**More than half of every city that reported anything at all reported exactly one incident in
the entire year.** A per-capita rate built on n=1 is not a measurement, and the difference
between a city at 0 and a city at 1 is overwhelmingly about whether the department filled in a
form.

### 3c. Can it join to a place? The crosswalk situation

**BJS Law Enforcement Agency Identifiers Crosswalk (LEAIC), ICPSR 35158.**
`https://www.icpsr.umich.edu/web/NACJD/studies/35158` - HTTP 200, 60,227 bytes.

Its own summary confirms it is exactly the right tool:

> "The LEAIC records contain common match keys for merging reported crime data and Census
> Bureau data. These linkage variables include the Originating Agency Identifier (ORI) code,
> Federal Information Processing Standards (FIPS) state, county and place codes..."

Two blockers:

1. **Vintage is 2012.** Title is literally *"Law Enforcement Agency Identifiers Crosswalk,
   United States, 2012"*, version date 2018-09-18. Fourteen years old.
2. **Login-walled.** `https://www.icpsr.umich.edu/cgi-bin/bob/zipcart2?path=NACJD&study=35158&bundle=all&ds=1`
   redirects to `https://www.icpsr.umich.edu/rpxlogin` with the page title **"Unable to Log In"**
   (HTTP 200, 27,658 bytes). No anonymous download.

**Verdict on LEAIC: NOT USABLE** - stale and login-walled.

**Free alternative that does work (for the join only):** the FBI CDE agency API accepts the
public `DEMO_KEY`:

```
https://api.usa.gov/crime/fbi/cde/agency/byStateAbbr/VT?API_KEY=DEMO_KEY
HTTP 200, 21,806 bytes
```

Real record:

```json
{"ori":"VT0050000","counties":"ESSEX","is_nibrs":true,
 "latitude":44.565365,"longitude":-71.56149,"state_abbr":"VT","state_name":"Vermont",
 "agency_name":"Essex County Sheriff's Office","agency_type_name":"County",
 "nibrs_start_date":"2011-01-01"}
```

That gives ORI + lat/lon + county name, free, no login, keyed by state. You could
point-in-polygon the lat/lon into a Census place. **But note the lat/lon is the agency's
station location, not its jurisdiction boundary** - a county sheriff's HQ sits inside some
city, and would falsely attribute county-wide incidents to that city.

**`DEMO_KEY` rate limit, measured.** I pulled 6 states in sequence: CA (HTTP 200, 221,180
bytes, 867 agencies), TX (200, 430,377, 1,754), NY (200, 134,904, 537), FL (200, 218,938, 833),
WY (200, 17,202, 69), then **MT returned HTTP 429** (173 bytes). So `DEMO_KEY` dies after
~5 calls. A free api.data.gov key would be required for all 50 states.

This fixes the join. It does not fix the underlying data.

### 3d. Verdict

**FBI hate crime: NOT USABLE for a per-place inclusivity score.**

Reason, in one line: it is voluntary agency-level reporting with no zero-fill, where 52% of
reporting cities report a single incident a year, so the score would mostly measure whether a
police department files paperwork.

### 3e. Other US federal / academic - checked, nothing found

- **No US federal dataset of municipal non-discrimination ordinances exists.** MAP is the
  de-facto registry and it is a nonprofit. I found no Census, DOJ, HUD, or EEOC product at
  place level.
- **Harvard Dataverse `doi:10.7910/DVN/JYKL9M`** - *"Replication Data for: Bureaucratic
  Responsiveness to LGBT Americans"* (checked via Dataverse API, HTTP 200, 15,728 bytes,
  11 files, `license: None`). It is a one-shot 2015-era **audit experiment** on marriage
  license officials, not an index. Not usable.
- Searches for an academic municipal-NDO panel with replication data returned only MAP,
  HRC, and a Wikipedia list. **NOT USABLE.**
- I also searched specifically for a **city-level LGBTQ+ inclusion index with broader coverage
  than the MEI**. Nothing surfaced. Every result pointed back to the HRC MEI itself. As far as
  I can establish, **the MEI is the only municipal LGBTQ+ inclusion index in the US**, and its
  506-city footprint is the ceiling, not a starting point.
- **State-run hate crime portals** exist for some states, but they are 50 separate schemas with
  50 separate geographies and 50 separate update cadences. Not verified individually - clearly
  not shippable across 4,226 places, and it would still be the same voluntary-reporting data.

---

## 4. Canada

App side, measured: `data/allplaces.json` = **712 CSDs**, each with a 7-digit CSD code
(`"code": "1001370"`), a CSD type string, lat/lon, and province. Provinces present:
QC 169, BC 117, ON 109, AB 108, SK 68, NB 39, MB 33, NS 28, NL 26, PE 7, NU 5, YT 2, NT 1.

### 4a. StatCan police-reported hate crime - the tables actually exist

I queried the StatCan Web Data Service cube metadata endpoint directly
(`POST https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata`) for four candidate product
IDs. Real results:

| PID | Title | Geographies | Latest |
|---|---|---|---|
| **35-10-0191** | Police-reported hate crime, number of incidents and rate per 100,000 population, **Provinces, Territories, Census Metropolitan Areas** and Canadian Forces Military Police | **58** | **2025** |
| 35-10-0066 | Police-reported hate crime, by type of motivation, selected regions and Canada (selected police services) | **9** | 2025 |
| 35-10-0067 | Police-reported hate crime, by most serious violation, selected regions and Canada (selected police services) | **9** | 2025 |
| 35-10-0177 | Incident-based crime statistics, by detailed violations, Canada, provinces, territories, CMAs | 57 | 2025 |

35-10-0066/0067 are **9 geographies only** - Canada plus Atlantic/QC/ON/MB/SK/AB/BC/Territories.
Useless at place level. **35-10-0191 is the finest hate-crime geography Statistics Canada
publishes.**

### 4b. Table 35-10-0191 - downloaded and read

| | |
|---|---|
| Table page | `https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3510019101` |
| CSV download | `https://www150.statcan.gc.ca/n1/tbl/csv/35100191-eng.zip` |
| HTTP / **measured size** | 200 / **15,131 bytes zipped** |
| Unzipped | `35100191.csv` 219,871 bytes + `35100191_MetaData.csv` 11,134 bytes |
| Rows | **1,368** |
| Range | 2014 - **2025**, annual. Released **2026-07-22 08:30**. |
| Licence | **Statistics Canada Open Licence** - "worldwide, royalty-free, non-exclusive licence". Free, no login. (`https://www.statcan.gc.ca/en/reference/licence` -> 302 -> `/en/terms-conditions/open-licence`, HTTP 200, 26,879 bytes) |

Real header:

```
REF_DATE,GEO,DGUID,Statistics,UOM,UOM_ID,SCALAR_FACTOR,SCALAR_ID,VECTOR,COORDINATE,
VALUE,STATUS,SYMBOL,TERMINATED,DECIMALS
```

Real 2025 rows:

```
2025, Total police-reported hate crime, Number of hate crime incidents, 4708
2025, Total police-reported hate crime, Rate per 100,000 population,    11.4
2025, Total Non-Census metropolitan area, Number of hate crime incidents, 630
2025, Total Non-Census metropolitan area, Rate per 100,000 population,    6.1
```

**Suppression: not the problem here.** I counted every STATUS and SYMBOL cell in the file:

```
STATUS: {'': 1281, '..': 87}      # '..' = not available, 6.4% of cells
SYMBOL: {'': 1368}                # zero suppression symbols
```

No `x` (confidentiality suppression) and no `F` (too unreliable) anywhere. Statistics Canada
publishes these counts cleanly. **The geography is the blocker, not suppression.**

### 4c. The geography, and the CSD join - computed, not guessed

The 58 geographies break down as: 3 aggregate rows (Total / Total non-CMA / Total CMA),
13 provinces and territories, **41 Census Metropolitan Areas**, and Canadian Forces Military
Police.

**A CMA is not a CSD.** The Vancouver CMA contains Vancouver, Surrey, Burnaby, Richmond,
Coquitlam, Langley and more, all as separate CSDs. So I built the real correspondence rather
than hand-waving it.

Source: **StatCan 2021 Census Geographic Attribute File**,
`https://www12.statcan.gc.ca/census-recensement/2021/geo/aip-pia/attribute-attribs/files-fichiers/2021_92-151_X.zip`
- HTTP 200, **9,832,890 bytes zipped**, unzips to a single CSV of **298,768,692 bytes**.
Columns used: `CSDUID_SDRIDU`, `CMAUID_RMRIDU`, `CMANAME_RMRNOM`, `CMATYPE_RMRGENRE`.
It holds **5,161 CSDs**. All 712 of the app's CSD codes were found in it - **0 misses**.

Joining the app's 712 CSDs to the 41 published CMAs:

```
app CSDs:                                                    712
  inside a CMA published in table 35-10-0191:   255  =  35.8%
  inside a Census Agglomeration - NOT published: 143  =  20.1%
  outside any CMA/CA entirely:                   314  =  44.1%
```

**64.2% of Canadian places get nothing at all.** And the 35.8% that get something do not get a
value for their own municipality - they inherit their CMA's number, shared with every other
municipality in that CMA:

```
Montréal CMA:              77 CSDs would all receive the identical number
Toronto CMA:               20
Vancouver CMA:             19
Edmonton CMA:              15
Victoria CMA:              11
Québec CMA:                 9
St. Catharines-Niagara:     9
St. John's CMA:             7
Saskatoon CMA:              7
```

So **zero of 712 CSDs would receive a value measured at their own geography.** Surrey, Burnaby
and Vancouver would all show the same "inclusive vibe" number. That is not a place-level
dimension.

**Verdict on StatCan hate crime: NOT USABLE at CSD level.** The data is genuinely good - clean,
current to 2025, openly licensed, unsuppressed - and the geography is simply two levels too
coarse for this app.

### 4d. Canadian municipal inclusion index

There is no Canadian equivalent of the HRC Municipal Equality Index. See the parallel
verification note in COULD NOT CONFIRM item 7 for the limits of that statement.

### 4e. Canada verdict

| Source | Verdict |
|---|---|
| StatCan 35-10-0191 (hate crime, CMA) | **NOT USABLE** - 41 CMAs for 712 CSDs; 64.2% get nothing, the rest inherit a regional average shared with up to 76 other municipalities. |
| StatCan 35-10-0066 / 35-10-0067 | **NOT USABLE** - 9 geographies. |
| Canadian municipal inclusion index | **Does not exist** as far as I could establish. |

---

## RECOMMENDATION

**Cut the dimension.**

The user who asked for it was right that it would be tough, and here is the specific reason,
which is not "the data is messy" but something worse:

**Every real measure that exists is a measure of the local government, not of the place.** The
MEI scores what city hall passed. MAP scores what the statehouse passed. The FBI counts what a
police department chose to file. None of them measure whether a person moving there would feel
welcome, and all three say so in their own documentation.

And the coverage arithmetic does not survive contact with 4,226 places:

- Best-in-class source (HRC MEI) covers **449 / 4,226 = 10.6%**, PDF-only, with no
  redistribution licence and a name-only join that breaks on every consolidated city-county.
  And the rated-city list has been **frozen at 506 since 2016** by HRC's own statement, so this
  is not a coverage problem that improves if you wait.
- The only source with full coverage (MAP state score) has **51 distinct values**. Shipping
  that as a place-level "inclusive vibe" is dressing up a state map as local knowledge.
- The only source that is genuinely per-locality (FBI) is **median 1 incident per city per
  year** and cannot distinguish zero from silent.

**Canada is worse, and it is worse in a way that cannot be worked around.** There is no
Canadian MEI. The only real measure is StatCan hate crime, and its finest published geography
is the CMA: 41 values for 712 places, 64.2% of which fall outside any published CMA entirely.
Of the 255 that do fall inside one, 77 would share Montréal's single number. **Zero of 712
Canadian places would get a figure measured at their own geography.** So even in the best case
you would ship a US dimension covering 10.6% of US places and a Canadian dimension covering
0% honestly - two different things wearing one label.

Three ways this could go wrong if you ship it anyway, in descending order of how bad:

1. **Filling the 89% gap.** Any imputation - state mean, 0, regional average - manufactures a
   number for nine places in ten. On a dimension this sensitive that is not a rounding error,
   it is a claim about a community that nobody made.
2. **Rewarding paperwork.** An FBI-based score would rank a town that never files above a town
   with an active hate-crimes unit that reports diligently. That is backwards.
3. **The proxy trap.** The tempting fix is % same-sex households, or % foreign-born, or a
   diversity index. Those are demographic composition, not inclusion, and using them means
   telling users a place is "inclusive" because of who already lives there. Do not do it.

**If you want to keep something anyway**, the only honest version is a narrow, clearly-labelled
badge rather than a scored dimension:

> "Rated 100/100 on the Human Rights Campaign's 2025 Municipal Equality Index, which scores
> city laws and policies on LGBTQ+ inclusion."

Shown **only** on the ~449 places that have a score, with **no value and no penalty** on the
other 3,777, and with HRC's permission for the redistribution. That is defensible because it
never implies anything about a place that was not rated. It is a badge, not a ranking.

But as a scored dimension that every place gets a number on - **there is nothing here you can
ship honestly. Cut it.**

---

## COULD NOT CONFIRM

Things I could not verify to the standard above. Do not treat any of these as facts.

1. **FBI's own agency-participation totals.** A search snippet claimed "16,419 agencies
   participated... 84.9 percent of the agencies enrolled... 95.1% population coverage" for
   2024. **I could not confirm this from a primary source.** `www.fbi.gov` returns HTTP 403 to
   scripted clients and a Cloudflare "Just a moment..." challenge with browser headers;
   `ucr.fbi.gov` also 403s; WebFetch on the press release also returned 403. The DOJ mirror
   (`https://www.justice.gov/hatecrimes/hate-crime-statistics`, HTTP 200, 68,121 bytes) carries
   the incident totals (2024: 11,679 incidents, 14,243 victims) **but not the agency
   participation count**. Use my own measured figure instead: **3,174 distinct ORIs appear in
   the 2024 data, 3,067 in 2025.**

2. **The 506 vs 509/510 gap in the MEI.** HRC says 506 municipalities, "which has been the
   number of cities rated since 2016". I harvested 509 distinct scorecard PDF URLs and 510
   distinct city+state anchor pairs from the 50 state pages. I did not resolve which is right;
   the likeliest explanation is a few stray or duplicate links on the state pages, but I did
   not prove it.

2b. **How many MEI rows are actually county policies wearing a CDP's name.** HRC says this
   happens ("often the county") and says it "will be clearly indicated", but I did not count
   the affected rows or check how the indication is formatted inside the PDFs.

3. **MEI category denominators across all 509 cities.** Partly resolved: I extracted the
   "N out of M" lines from **6** scorecards and the denominators were identical every time -
   Non-Discrimination Laws /30, Municipality as Employer /28, Municipal Services /12, Law
   Enforcement /22 (one card showed Non-Discrimination at `28 out of 30`, i.e. the numerator
   moves, not the denominator). Leadership /8 is present but formatted differently and my
   regex missed it on 5 of 6. **I did not check all 509** - a parser should still read the
   denominator per card rather than hardcode it.

4. **Whether HRC would license the MEI scores for commercial redistribution.** Not asked, not
   answered. I confirmed only that no open licence is published.

5. **MAP's exact municipality count.** The page I read says "at least 390". A search snippet
   said 395. I am reporting the 390 I read myself off the live page.

6. **StatCan discrimination / sense-of-belonging survey measures (CCHS, GSS).** I did not
   verify these myself. They would in any case be published at province or health-region
   level, and a health region is not a CSD - but treat that as reasoning, not a checked fact.

7. **"No Canadian municipal inclusion index exists."** I searched and found none, and none
   surfaced anywhere in this session's work. But **absence of evidence from my searches is not
   proof of absence** - I did not exhaustively check Egale Canada, the Canadian Centre for
   Diversity and Inclusion, or provincial human-rights commissions one by one. My confidence
   is high, not certain. If this dimension is revived, that is the first thing to re-check.

8. **A Canadian police-service-level hate crime table** (finer than CMA, closer to a
   municipality). The two "selected police services" tables I checked (35-10-0066/0067) publish
   only 9 aggregate regions despite the name. I did not exhaustively search the StatCan
   catalogue for a per-service table.
