# Civic data (pro sports + rapid transit) - claim-by-claim sourcing

Research date: **2026-07-29**. Output: `data/civic.json`, 79 records.

Every URL below was actually opened during this build. Nothing here is from memory.
Where a page could not be fetched, that is stated explicitly and the claim rests on a
different source that did serve. Where a fact could not be verified, the entry was
**left out of the dataset**, and the omission is logged in the last section.

Keys are `name` + `prov` exactly as they appear in `data/climate.json` (712 entries).
Anything not in that list cannot be a key, so a few real facts (Cavalry FC, King Township)
are recorded here but are deliberately absent from the JSON.

Totals: **13 places with a pro team**, **74 places with transit**
(5 subway, 18 light rail, 51 commuter rail), **33 teams** across 8 leagues.

---

## PART 1 - PRO SPORTS

Rule applied: the team must physically play its home games inside that census
subdivision. Being *named* for a metro is not enough. Four teams failed this test and
are handled below (Cavalry FC, Montréal Victoire, Pacific FC, Vancouver FC).

### 1.1 Leagues covered and their 2026 status

| League | Canadian teams | Source opened |
|---|---|---|
| NHL | 7 | https://en.wikipedia.org/wiki/National_Hockey_League |
| NBA | 1 | https://en.wikipedia.org/wiki/Toronto_Raptors |
| WNBA | 1 | https://en.wikipedia.org/wiki/Toronto_Tempo |
| MLB | 1 | https://en.wikipedia.org/wiki/Toronto_Blue_Jays |
| MLS | 3 | https://en.wikipedia.org/wiki/Major_League_Soccer |
| CFL | 9 | https://en.wikipedia.org/wiki/Canadian_Football_League |
| NWSL | **0** | https://en.wikipedia.org/wiki/National_Women%27s_Soccer_League |
| PWHL | 4 | https://en.wikipedia.org/wiki/Professional_Women%27s_Hockey_League |
| CPL | 8 clubs, 7 usable | https://en.wikipedia.org/wiki/Canadian_Premier_League |

NHL fetch, verbatim on the only recent relocation: *"On April 18, 2024, the Arizona
Coyotes suspended operations and sold their hockey assets ... to a new team in Salt Lake
City."* That produced the Utah Mammoth, a US team. **No change to the Canadian seven.**

NWSL fetch returned 16 clubs, all American, plus Columbus and Atlanta for 2028. The
article describes the league as the top level of *the United States* league system.
**No Canadian NWSL team exists, so the league contributes nothing to this dataset.**

MLS fetch, verbatim: *"MLS comprises 30 teams, with 27 in the United States and 3 in
Canada."* Newest club San Diego FC (2025) is American.

### 1.2 2026 franchise changes that a stale dataset would get wrong

These are the reason this file exists. All four were verified individually.

1. **Valour FC (Winnipeg, CPL) no longer exists.**
   https://en.wikipedia.org/wiki/Valour_FC - infobox *"Dissolved: November 21, 2025"*;
   body *"Valour FC suspended operations following the 2025 CPL season."*
   Corroborated at https://en.wikipedia.org/wiki/Princess_Auto_Stadium, which no longer
   lists Valour as a tenant. **Winnipeg drops from 3 leagues to 2.**

2. **York United FC is now Inter Toronto FC.**
   https://en.wikipedia.org/wiki/York_United_FC - *"On November 27, 2025, the club
   rebranded from York United FC to Inter Toronto FC."* Same venue: *"Inter Toronto FC
   plays its home matches at York Lions Stadium in York University's Keele Campus in
   York University Heights, a neighbourhood of North York, Toronto."*

3. **FC Supra du Québec is a new CPL club, and it is in LAVAL, not Montréal.**
   https://en.wikipedia.org/wiki/FC_Supra_du_Qu%C3%A9bec - infobox *"Stadium: Stade
   Boréale, Laval, Quebec"*; *"The club was founded in September 2025 and played its
   first match on April 11, 2026."* It has played real matches, so it counts.

4. **Toronto Tempo (WNBA) began play May 2026 at Coca-Cola Coliseum, Toronto.**
   https://en.wikipedia.org/wiki/Toronto_Tempo - *"Beginning play in May 2026, they are
   the first WNBA team located outside of the United States."* Arena and location fields:
   *"Arena: Coca-Cola Coliseum"*, *"Location: Toronto, Ontario"*. Corroborated at
   https://en.wikipedia.org/wiki/Coca-Cola_Coliseum - *"It also serves as the home arena
   of the Toronto Tempo of the Women's National Basketball Association since their debut
   in 2026."*
   **Note for the caller: WNBA was not in the requested league list.** It was included
   because it is unambiguously top-tier and is exactly the recent change the brief asked
   to catch. Dropping it costs Toronto one league and nothing else.

### 1.3 The "named for a metro, plays in a suburb" traps

| Team | Named for | Actually plays in | Source |
|---|---|---|---|
| **Cavalry FC** (CPL) | Calgary | **Foothills County, AB** | https://en.wikipedia.org/wiki/ATCO_Field - location field *"Foothills County, Alberta, Canada"*. Also https://en.wikipedia.org/wiki/Cavalry_FC - *"ATCO Field is located on the grounds of Spruce Meadows in Foothills County"*, club described only as *"based in the Calgary metropolitan region"*. |
| **Montréal Victoire** (PWHL) | Montréal | **Laval, QC** | https://en.wikipedia.org/wiki/Montreal_Victoire - infobox home arena *"Place Bell"*, *"Laval, Quebec"*; *"the team announced that Place Bell would serve as its primary home venue for the 2024-25 season."* Arena page https://en.wikipedia.org/wiki/Place_Bell - *"Place Bell is a multi-purpose arena in Laval, Quebec"*, address *"1950 Rue Claude-Gagné"*, and lists *"Montréal Victoire ... permanent home since 2024-25 season."* |
| **Pacific FC** (CPL) | Victoria / Vancouver Island | **Langford, BC** | https://en.wikipedia.org/wiki/Pacific_FC - *"Canadian professional soccer club based in Langford, British Columbia"*, *"Starlight Stadium is a stadium in Langford, British Columbia"*. Victoria BC gets **nothing**. |
| **Vancouver FC** (CPL) | Vancouver | **Langley (District), BC** | https://en.wikipedia.org/wiki/Vancouver_FC - infobox *"Langley, British Columbia (district municipality)"*. Venue page https://en.wikipedia.org/wiki/Langley_Events_Centre - address *"7888 200th Street, Langley, British Columbia V2Y 3J4"*, in the **Township of Langley**, and *"Willoughby Stadium (adjacent to the Events Centre) hosts Vancouver FC."* Keyed to `Langley (District)`, **not** `Langley (City)`. |

Trap that is **not** a trap: the **Ottawa Senators** at the Canadian Tire Centre.
https://en.wikipedia.org/wiki/Canadian_Tire_Centre - *"a multi-purpose arena in the
suburb of Kanata in Ottawa, Ontario"*, and *"In 2001, Kanata was merged into the City of
Ottawa, thus bringing the arena officially into the Canadian capital."* Same for the
**Ottawa Charge** (PWHL), whose infobox home arena is the Canadian Tire Centre:
https://en.wikipedia.org/wiki/Ottawa_Charge. Both key to `Ottawa, ON`.

### 1.4 Every team, with the page that puts it in that municipality

**Toronto, ON - 8 leagues**

| Team | League | Venue | Source |
|---|---|---|---|
| Toronto Maple Leafs | NHL | Scotiabank Arena, Toronto | https://en.wikipedia.org/wiki/National_Hockey_League |
| Toronto Raptors | NBA | Scotiabank Arena, Toronto | https://en.wikipedia.org/wiki/Toronto_Raptors (*"Location: Toronto, Ontario"*) |
| Toronto Tempo | WNBA | Coca-Cola Coliseum, Toronto | https://en.wikipedia.org/wiki/Toronto_Tempo |
| Toronto Blue Jays | MLB | Rogers Centre, Toronto | https://en.wikipedia.org/wiki/Toronto_Blue_Jays (*"primarily at Rogers Centre in downtown Toronto"*) |
| Toronto FC | MLS | BMO Field, Toronto | https://en.wikipedia.org/wiki/BMO_Field (*"the home field of Toronto FC of Major League Soccer"*) |
| Toronto Argonauts | CFL | BMO Field, Toronto | https://en.wikipedia.org/wiki/BMO_Field ; https://en.wikipedia.org/wiki/Canadian_Football_League |
| Toronto Sceptres | PWHL | Coca-Cola Coliseum, Toronto | https://en.wikipedia.org/wiki/Coca-Cola_Coliseum |
| Inter Toronto FC | CPL | York Lions Stadium, Toronto | https://en.wikipedia.org/wiki/York_United_FC |

**Montréal, QC - 3 leagues.** Note the Victoire is *not* here, see 1.3.

| Team | League | Venue | Source |
|---|---|---|---|
| Montreal Canadiens | NHL | Bell Centre, Montreal | https://en.wikipedia.org/wiki/National_Hockey_League |
| CF Montréal | MLS | Saputo Stadium, Montreal | https://en.wikipedia.org/wiki/Saputo_Stadium (*"a soccer-specific stadium at Olympic Park in the borough of Mercier-Hochelaga-Maisonneuve in Montreal"*) |
| Montreal Alouettes | CFL | Percival Molson Memorial Stadium, Montreal | https://en.wikipedia.org/wiki/Percival_Molson_Memorial_Stadium |

**Vancouver, BC - 4 leagues**

| Team | League | Venue | Source |
|---|---|---|---|
| Vancouver Canucks | NHL | Rogers Arena, Vancouver | https://en.wikipedia.org/wiki/National_Hockey_League |
| Vancouver Whitecaps FC | MLS | BC Place, Vancouver | https://en.wikipedia.org/wiki/BC_Place ; https://en.wikipedia.org/wiki/Vancouver_Whitecaps_FC (infobox *"BC Place, Vancouver, British Columbia"*) |
| BC Lions | CFL | BC Place, Vancouver | https://en.wikipedia.org/wiki/BC_Place |
| Vancouver Goldeneyes | PWHL | Pacific Coliseum, Vancouver | https://en.wikipedia.org/wiki/Vancouver_Goldeneyes ; https://en.wikipedia.org/wiki/Pacific_Coliseum (*"an indoor arena located at Hastings Park in Vancouver"*) |

**Ottawa, ON - 4 leagues**

| Team | League | Venue | Source |
|---|---|---|---|
| Ottawa Senators | NHL | Canadian Tire Centre, Ottawa (Kanata) | https://en.wikipedia.org/wiki/Canadian_Tire_Centre |
| Ottawa Redblacks | CFL | TD Place Stadium, Ottawa | https://en.wikipedia.org/wiki/TD_Place_Stadium (*"an outdoor stadium in Ottawa, Ontario ... home of the Ottawa Redblacks"*) |
| Ottawa Charge | PWHL | Canadian Tire Centre, Ottawa | https://en.wikipedia.org/wiki/Ottawa_Charge |
| Atlético Ottawa | CPL | TD Place Stadium, Ottawa | https://en.wikipedia.org/wiki/Atl%C3%A9tico_Ottawa (*"Atlético Ottawa play at TD Place at Lansdowne Park in the Glebe neighbourhood of Ottawa"*) |

**Everywhere else**

| Place | Team | League | Source |
|---|---|---|---|
| Calgary, AB | Calgary Flames | NHL | https://en.wikipedia.org/wiki/National_Hockey_League |
| Calgary, AB | Calgary Stampeders | CFL | https://en.wikipedia.org/wiki/McMahon_Stadium (*"a Canadian football stadium in Calgary, Alberta"*) |
| Edmonton, AB | Edmonton Oilers | NHL | https://en.wikipedia.org/wiki/National_Hockey_League |
| Edmonton, AB | Edmonton Elks | CFL | https://en.wikipedia.org/wiki/Commonwealth_Stadium_(Edmonton) (*"located in the McCauley neighbourhood of Edmonton"*) |
| Winnipeg, MB | Winnipeg Jets | NHL | https://en.wikipedia.org/wiki/National_Hockey_League |
| Winnipeg, MB | Winnipeg Blue Bombers | CFL | https://en.wikipedia.org/wiki/Princess_Auto_Stadium (*"an outdoor stadium in Winnipeg, Manitoba"*) |
| Hamilton, ON | Hamilton Tiger-Cats | CFL | https://en.wikipedia.org/wiki/Hamilton_Stadium (*"Hamilton Tiger-Cats (CFL) 2014-present"*) |
| Hamilton, ON | Forge FC | CPL | https://en.wikipedia.org/wiki/Forge_FC (infobox *"Hamilton Stadium, Hamilton, Ontario"*) |
| Regina, SK | Saskatchewan Roughriders | CFL | https://en.wikipedia.org/wiki/Mosaic_Stadium (*"an open-air stadium at REAL District in Regina, Saskatchewan"*) |
| Halifax, NS | HFX Wanderers FC | CPL | https://en.wikipedia.org/wiki/HFX_Wanderers_FC (infobox *"Wanderers Grounds, Halifax, Nova Scotia"*) |
| Laval, QC | Montréal Victoire | PWHL | https://en.wikipedia.org/wiki/Place_Bell |
| Laval, QC | FC Supra du Québec | CPL | https://en.wikipedia.org/wiki/FC_Supra_du_Qu%C3%A9bec |
| Langford, BC | Pacific FC | CPL | https://en.wikipedia.org/wiki/Pacific_FC |
| Langley (District), BC | Vancouver FC | CPL | https://en.wikipedia.org/wiki/Langley_Events_Centre |

---

## PART 2 - RAPID TRANSIT

`transit_type` uses a closed vocabulary of three values, matching the schema in the brief:
`subway`, `light rail`, `commuter rail`. Where a place has more than one system, the
highest-order one wins the type and the name, and every system's source is still recorded
in `sources`.

One honest caveat on vocabulary: **SkyTrain and the REM are fully grade-separated
automated light metro**, not street-running light rail. The brief's own example maps
Vancouver to `"light rail"` / `"SkyTrain"`, so that convention is followed for
consistency rather than re-litigated per system.

### 2.1 Subway (5 places)

**Toronto, ON - TTC subway.** Five lines running as of 2026: Lines 1, 2, 4, 5 and 6.
https://en.wikipedia.org/wiki/Toronto_subway
- Line 5 Eglinton **opened February 8, 2026**, Mount Dennis to Kennedy, entirely inside
  Toronto: https://en.wikipedia.org/wiki/Line_5_Eglinton
- Line 6 Finch West **opened December 7, 2025**, entirely inside Toronto:
  https://en.wikipedia.org/wiki/Line_6_Finch_West
- Line 3 Scarborough is **closed** (derailment July 24, 2023, never reopened) - noted so
  nobody re-adds it.
- Toronto also has GO rail: https://en.wikipedia.org/wiki/List_of_GO_Transit_stations

**Vaughan, ON - TTC subway.** Two Line 1 stations are physically in Vaughan.
- Vaughan Metropolitan Centre, infobox *"3150 Highway 7 West, Vaughan, Ontario"*:
  https://en.wikipedia.org/wiki/Vaughan_Metropolitan_Centre_station
- Highway 407, infobox *"7332 Jane Street, Vaughan, Ontario"*, and *"one of only two TTC
  subway stations situated outside Toronto's city limits"*:
  https://en.wikipedia.org/wiki/Highway_407_station
- Pioneer Village **straddles the boundary** (*"The northern portion of the station lies
  in the City of Vaughan ... and the southern portion in the City of Toronto"*) so it was
  not used as the deciding evidence: https://en.wikipedia.org/wiki/Pioneer_Village_station
- Opened December 17, 2017: https://en.wikipedia.org/wiki/Toronto%E2%80%93York_Spadina_Subway_Extension
- Vaughan also has GO rail (Rutherford, Maple): https://en.wikipedia.org/wiki/Barrie_line

**Montréal / Laval / Longueuil, QC - Montréal Métro.** 68 stations, 4 lines.
https://en.wikipedia.org/wiki/Montreal_Metro and
https://en.wikipedia.org/wiki/List_of_Montreal_Metro_stations
- Laval: three stations from the 2007 Orange line extension - Cartier, De la Concorde,
  Montmorency. Verbatim: *"This extension added 5.2 kilometres to the network and three
  stations in Laval (Cartier, De la Concorde and Montmorency)."*
  https://en.wikipedia.org/wiki/Montmorency_station
- Longueuil: one station, Longueuil-Université-de-Sherbrooke, terminus of the Yellow line.

### 2.2 Light rail / light metro (18 places)

**SkyTrain, BC (7 places): Vancouver, Burnaby, New Westminster, Surrey, Richmond,
Coquitlam, Port Moody.**
- Expo Line station-by-city table (Vancouver, Burnaby, New Westminster, Surrey):
  https://en.wikipedia.org/wiki/Expo_Line_(SkyTrain)
- Millennium Line incl. Evergreen Extension. **Port Moody has two stations** (Moody Centre
  *"Barnet Highway at Williams Street"*, Inlet Centre *"Barnet Highway at Ioco Road"*) and
  Coquitlam has four (Burquitlam, Coquitlam Central, Lincoln, Lafarge Lake-Douglas):
  https://en.wikipedia.org/wiki/Millennium_Line
- Canada Line, 9 stations in Vancouver and 8 in Richmond incl. YVR-Airport on Sea Island,
  which is part of Richmond: https://en.wikipedia.org/wiki/Canada_Line
- **Not yet open, so not counted:** Broadway Subway extension (stations marked 2027) and
  the Surrey Langley SkyTrain extension (stations marked 2029, incl. Fleetwood, Clayton,
  Langley City Centre). **`Langley (City)` and `Langley (District)` therefore get no
  transit.** Source for both: the SkyTrain article's under-construction station list at
  https://en.wikipedia.org/wiki/SkyTrain_(Vancouver) - *"54 stations"* with *"13 under
  construction"*.

**Calgary, AB - CTrain.** https://en.wikipedia.org/wiki/CTrain - *"CTrain ... is a light
rail system in Calgary, Alberta."* Red and Blue lines running; Green Line under
construction, southeast leg *"expected to be completely built by 2039"*. The system is
entirely within Calgary; the Airdrie extension is long-term aspiration only, so
**Airdrie gets nothing**.

**Edmonton, AB - Edmonton LRT.** Capital, Metro and Valley Line Southeast in service,
all inside Edmonton: https://en.wikipedia.org/wiki/Edmonton_Light_Rail_Transit
Valley Line West is **not open** - construction runs through 2026 with service expected
2028: https://www.edmonton.ca/projects_plans/transit/valley-line-west
No line reaches St. Albert, Spruce Grove or Strathcona County, so **those get nothing**.

**Ottawa, ON - O-Train.** https://en.wikipedia.org/wiki/O-Train - *"The O-Train network
currently operates one light rail line, Line 1, and two diesel light rail lines, Line 2
and Line 4."* All stations are inside the City of Ottawa. **No line crosses into Gatineau**
(the Gatineau LRT is proposal-stage), so **Gatineau QC gets nothing**.

**Kitchener and Waterloo, ON - ION.** https://en.wikipedia.org/wiki/Ion_rapid_transit -
light rail runs Conestoga station (Waterloo) to Fairway station (Kitchener) only.
**Cambridge is served by ION *bus* route 302, not light rail.** Stage 2 LRT to Cambridge
was approved by Regional Council in November 2025 but *"construction may not begin on that
line until 2028."* **Cambridge ON therefore gets nothing.**
Kitchener additionally has GO rail: https://en.wikipedia.org/wiki/Kitchener_line

**REM, QC (6 places): Brossard, Deux-Montagnes, Kirkland, Mont-Royal, Pointe-Claire,
Sainte-Anne-de-Bellevue** (plus Montréal and Laval, which are already subway).
Network page: https://en.wikipedia.org/wiki/R%C3%A9seau_express_m%C3%A9tropolitain
- Rive-Sud branch, opened 31 July 2023: Brossard, Du Quartier, Panama (all Brossard);
  Île-des-Sœurs and Gare Centrale (Montréal). https://en.wikipedia.org/wiki/Panama_station
- Deux-Montagnes branch, opened 17 November 2025: adds Île-Bigras and Sainte-Dorothée
  (Laval), Ville-de-Mont-Royal (**Town of Mount Royal**, address *"1300 Canora Road,
  Mount Royal, Quebec"* - https://en.wikipedia.org/wiki/Ville-de-Mont-Royal_station),
  Grand-Moulin and Deux-Montagnes (Deux-Montagnes -
  https://en.wikipedia.org/wiki/Deux-Montagnes_station)
- Anse-à-l'Orme branch, opened 18 May 2026. Official REM release, verbatim: the branch
  *"adds four new stations located in the cities of Pointe-Claire, Kirkland and
  Sainte-Anne-de-Bellevue."*
  https://rem.info/en/news/may-18-2026-scheduled-opening-date-anse-lorme-branch
  Station pages: https://en.wikipedia.org/wiki/Kirkland_station ,
  https://en.wikipedia.org/wiki/Fairview%E2%80%93Pointe-Claire_station ,
  https://en.wikipedia.org/wiki/Anse-%C3%A0-l%27Orme_station
- **Not open, so not counted:** YUL-Aéroport branch (projected Q4 2027) - **Dorval gets
  only commuter rail**, not REM. Griffintown-Bernard-Landry and Bridge-Bonaventure
  (~2030), both Montréal anyway.
- **Sainte-Marthe-sur-le-Lac has no REM station**, verified against
  https://en.wikipedia.org/wiki/Grand-Moulin_station

### 2.3 Commuter rail (51 places)

**West Coast Express, BC (4 commuter-only places).**
https://en.wikipedia.org/wiki/West_Coast_Express - verbatim: *"Service is provided between
Downtown Vancouver and the municipalities of Port Moody, Coquitlam, Port Coquitlam, Pitt
Meadows, Maple Ridge, and Mission."* Still running (7,200 weekday riders, Q1 2026).
Commuter-only: **Port Coquitlam, Pitt Meadows, Maple Ridge, Mission**. Vancouver,
Coquitlam and Port Moody are already SkyTrain.

**GO Transit, ON (23 commuter-only places).** Master cross-check:
https://en.wikipedia.org/wiki/List_of_GO_Transit_stations

| Place | Stations | Line / station source |
|---|---|---|
| Ajax | Ajax | https://en.wikipedia.org/wiki/Lakeshore_East_line |
| Aurora | Aurora | https://en.wikipedia.org/wiki/Barrie_line |
| Barrie | Barrie South, Allandale Waterfront | https://en.wikipedia.org/wiki/Barrie_line |
| Bradford West Gwillimbury | Bradford | https://en.wikipedia.org/wiki/Bradford_West_Gwillimbury |
| Brampton | Bramalea, Brampton, Mount Pleasant | https://en.wikipedia.org/wiki/Kitchener_line |
| Burlington | Appleby, Burlington, **Aldershot** | https://en.wikipedia.org/wiki/Aldershot_GO_Station |
| East Gwillimbury | East Gwillimbury | https://en.wikipedia.org/wiki/Barrie_line |
| Guelph | Guelph Central | https://en.wikipedia.org/wiki/Guelph_Central_Station |
| Halton Hills | **Georgetown, Acton** | https://en.wikipedia.org/wiki/Georgetown_GO_Station |
| Hamilton | Hamilton GO Centre, West Harbour, Confederation | https://en.wikipedia.org/wiki/Confederation_GO_Station |
| Markham | Unionville, Centennial, Markham, Mount Joy | https://en.wikipedia.org/wiki/Stouffville_line |
| Milton | Milton | https://en.wikipedia.org/wiki/Milton_GO_Station |
| Mississauga | Port Credit, Clarkson, Dixie, Cooksville, Erindale, Streetsville, Meadowvale, Lisgar, Malton | https://en.wikipedia.org/wiki/Milton_line |
| Newmarket | Newmarket | https://en.wikipedia.org/wiki/Barrie_line |
| Niagara Falls | Niagara Falls | https://en.wikipedia.org/wiki/Lakeshore_West_line |
| Oakville | Oakville, Bronte | https://en.wikipedia.org/wiki/Lakeshore_West_line |
| Oshawa | Oshawa | https://en.wikipedia.org/wiki/Lakeshore_East_line |
| Pickering | Pickering | https://en.wikipedia.org/wiki/Lakeshore_East_line |
| Richmond Hill | **Langstaff, Richmond Hill, Gormley, Bloomington** | https://en.wikipedia.org/wiki/Richmond_Hill_line |
| St. Catharines | St. Catharines | https://en.wikipedia.org/wiki/St._Catharines_railway_station |
| Stratford | Stratford | https://www.gotransit.com/en/find-a-station-or-stop/sf/stratford-go |
| Whitby | Whitby | https://en.wikipedia.org/wiki/Lakeshore_East_line |
| Whitchurch-Stouffville | Stouffville, **Old Elm** | https://en.wikipedia.org/wiki/Stouffville_line |

GO station-location corrections that were caught and applied:
- **Aldershot is in Burlington, not Hamilton.** Station infobox: *"1199 Waterdown Road,
  Burlington, Ontario."* https://en.wikipedia.org/wiki/Aldershot_GO_Station
- **Georgetown and Acton are in Halton Hills** - *"a railway station in Georgetown, a
  community in the town of Halton Hills."* https://en.wikipedia.org/wiki/Georgetown_GO_Station
- **Langstaff, Gormley and Bloomington are all in Richmond Hill, not Markham or
  Whitchurch-Stouffville.** Gormley infobox *"1650 Stouffville Road, Richmond Hill"*
  (https://en.wikipedia.org/wiki/Gormley_GO_Station); Bloomington *"1796 Bloomington Road,
  Richmond Hill"* (https://en.wikipedia.org/wiki/Bloomington_GO_Station); Langstaff
  *"10 Red Maple Road, Richmond Hill"* (https://en.wikipedia.org/wiki/Langstaff_GO_Station)
- **Milliken is in Toronto (Scarborough), not Markham** - infobox *"39 Redlea Avenue,
  Scarborough, Ontario."* https://en.wikipedia.org/wiki/Milliken_GO_Station
- **Lincolnville was renamed Old Elm** in 2021; still Whitchurch-Stouffville.
- **Stratford GO is brand new**, service began **July 6, 2026**. Line page: *"On July 6,
  2026, service returned to Stratford."* https://en.wikipedia.org/wiki/Kitchener_line ;
  GO's own station page https://www.gotransit.com/en/find-a-station-or-stop/sf/stratford-go
  and https://www.gotransit.com/en/partners-and-promotions/take-go-transit-to-stratford
- **Vaughan Metropolitan Centre is a subway station, not a GO rail station.** Vaughan's GO
  rail stations are Rutherford and Maple.
- **Year-round Niagara service confirmed:** GO Transit, verbatim, *"GO Transit has service
  to Niagara Falls all year round!"*
  https://www.gotransit.com/en/travelling-with-us/promotions-and-events/Niagara ;
  Metrolinx *"For the first time ever, GO Transit is introducing year-round weekday train
  service between Niagara Falls and Toronto"*, with stops at St. Catharines and Hamilton
  West Harbour: https://www.metrolinx.com/en/discover/weekday-go-train-service-to-niagara-region

**exo, QC (24 commuter-only places).** Five lines, all showing normal service on
https://exo.quebec/en/trip-planner/train. Network page:
https://en.wikipedia.org/wiki/Exo_commuter_rail

| Place | Line | Source |
|---|---|---|
| Baie-D'Urfé, Beaconsfield, Dorval, Hudson, L'Île-Perrot, Montréal-Ouest, Vaudreuil-Dorion | Vaudreuil-Hudson (11) | https://en.wikipedia.org/wiki/Vaudreuil%E2%80%93Hudson_line |
| Terrasse-Vaudreuil | Vaudreuil-Hudson (11) | https://en.wikipedia.org/wiki/Pincourt%E2%80%93Terrasse-Vaudreuil_station |
| Blainville, Rosemère, Sainte-Thérèse, Saint-Jérôme | Saint-Jérôme (12) | https://en.wikipedia.org/wiki/Saint-J%C3%A9r%C3%B4me_line |
| Mirabel | Saint-Jérôme (12) | https://en.wikipedia.org/wiki/Mirabel_station |
| McMasterville, Mont-Saint-Hilaire, Saint-Basile-le-Grand, Saint-Bruno-de-Montarville, Saint-Lambert | Mont-Saint-Hilaire (13) | https://en.wikipedia.org/wiki/Mont-Saint-Hilaire_line |
| Candiac, Delson | Candiac (14) | https://en.wikipedia.org/wiki/Candiac_line |
| Saint-Constant | Candiac (14) | https://en.wikipedia.org/wiki/Sainte-Catherine_station_(Exo) |
| Mascouche, Repentigny, Terrebonne | Mascouche (15) | https://en.wikipedia.org/wiki/Mascouche_line |

Montréal, Laval, Longueuil, Pointe-Claire and Sainte-Anne-de-Bellevue are also on exo
lines, but rank higher as subway or REM.

exo station-location corrections that were caught and applied:
- **"Sainte-Catherine" station is in Saint-Constant, not Sainte-Catherine.** Station page,
  verbatim: *"Sainte-Catherine station is a commuter rail station operated by Exo in
  Saint-Constant, Quebec, Canada"*, address *"333 Sainte-Catherine Road, Saint-Constant,
  Quebec J5A 1V7."* **`Sainte-Catherine, QC` therefore gets NOTHING.**
  https://en.wikipedia.org/wiki/Sainte-Catherine_station_(Exo)
- **"Pincourt-Terrasse-Vaudreuil" station is in Terrasse-Vaudreuil, not Pincourt.**
  Verbatim: *"a commuter rail station operated by Exo in Terrasse-Vaudreuil, Quebec"*,
  address *"4, 4e Boulevard Terrasse-Vaudreuil."* **`Pincourt, QC` gets NOTHING.**
  https://en.wikipedia.org/wiki/Pincourt%E2%80%93Terrasse-Vaudreuil_station
- **The Deux-Montagnes exo line no longer exists.** Closed permanently 31 December 2020,
  replaced by the REM Deux-Montagnes branch on 17 November 2025.
- **Boisbriand and Chambly have no station.** The Saint-Jérôme line passes near Boisbriand
  but stops at Sainte-Thérèse, Rosemère and Blainville.
- Mascouche line terminus moved from Ahuntsic to Côte-de-Liesse on 12 January 2026 for REM
  transfer: https://en.wikipedia.org/wiki/C%C3%B4te-de-Liesse_station

---

## PART 3 - DELIBERATELY LEFT OUT

Nothing below is in `data/civic.json`. Each is either unverifiable, not yet real, or
outside the key space.

**Sports**

| Excluded | Why |
|---|---|
| **Cavalry FC (CPL)** | Plays at ATCO Field in **Foothills County, AB**, which is not a `climate.json` key. Assigning it to Calgary would be exactly the metro-name error the brief warned about. Calgary keeps NHL + CFL = 2. |
| **PWHL Hamilton** | Announced 13 May 2026 for TD Coliseum, Hamilton, but the 2026-27 season has **not started** as of 2026-07-29 - no game has been played. https://en.wikipedia.org/wiki/2026%E2%80%9327_PWHL_season . Easy to add on the season opener; Hamilton is already in the file at 2 leagues. |
| **NWSL entirely** | Zero Canadian clubs, current or announced. |
| **Northern Super League (NSL)** | A real Canadian top-tier women's league (e.g. Ottawa Rapid FC at TD Place - https://en.wikipedia.org/wiki/TD_Place_Stadium), but **not in the requested league list**, so it was not enumerated. Adding it would change several `pro_league_count` values. Flagging rather than silently including. |
| **CPL Windsor** | Expansion rights announced in 2022 with a 2026 goal, but the CPL's own 2026 club table lists 8 clubs and Windsor is not among them. https://en.wikipedia.org/wiki/Canadian_Premier_League |
| CEBL, AHL, WHL/OHL/QMJHL, USL, NLL | Not top-tier / not in the requested list. |

**Transit**

| Excluded | Why |
|---|---|
| **Mississauga and Brampton - Hazel McCallion (Hurontario) LRT** | **Not open.** Metrolinx still writes in future tense: *"Once in service, the 18-kilometre Hazel McCallion Line will bring..."* https://www.metrolinx.com/en/projects-and-programs/hazel-mccallion-lrt . Global News, 2 July 2026: *"originally slated to be done in 2024, but is now tracking to be finished in 2028."* https://globalnews.ca/news/11950196/hazel-mccallion-lrt-new-projects/ . Wikipedia: *"as of April 2026, Metrolinx has refused to reveal a completion date to the public."* https://en.wikipedia.org/wiki/Hazel_McCallion_Line . Both are marked **commuter rail** on GO, per the brief. |
| **Clarington, ON** | Lakeshore East Bowmanville extension is **under construction**, not in service. Metrolinx: *"The Bowmanville Extension is currently in construction"*, no completion date. https://www.metrolinx.com/en/projects-and-programs/lakeshore-east-line-go-expansion/what-were-building/bowmanville-extension |
| **King, ON (King City GO)** | King Township is genuinely served, but `King` is **not a key in climate.json** (only `Kingston` matches). Cannot be added. |
| **Cambridge, ON** | ION *bus* only. LRT Stage 2 construction not before 2028. |
| **Langley (City) and Langley (District), BC** | Surrey Langley SkyTrain stations marked 2029. Note Langley (District) still appears in the file, for Vancouver FC. |
| **Gatineau, QC** | No O-Train station; Gatineau LRT is proposal-stage. Its Rapibus is BRT, which is outside the brief's definition. |
| **Sainte-Catherine, QC and Pincourt, QC** | Station *names*, not station *locations*. See 2.3. |
| **Dorval, QC** | Marked commuter rail only. The REM airport branch is projected Q4 2027. |
| **Boisbriand, Chambly, Sainte-Marthe-sur-le-Lac, QC** | No station verified. |
| **St. Albert, Spruce Grove, Airdrie, AB** | Extensions are proposals only. |
| **Victoria, BC** | No rail transit, and Pacific FC plays in Langford. |
| **London and St. Marys, ON** | GO pilot rail service ended October 2023 and neither appears on any current line page. Single-sourced (https://en.wikipedia.org/wiki/GO_Transit), so excluded rather than asserted either way. |
| Woodbine, King-Liberty, Caledonia, Bloor-Lansdowne, Breslau GO stations | Under construction or planned. Woolwich (Breslau) is not a `climate.json` key anyway. |

---

## PART 4 - SOURCING LIMITATIONS, STATED PLAINLY

1. **Several official transit sites refused scripted fetches.** `translink.ca`,
   `calgarytransit.com`, `grt.ca/en/ion-light-rail.aspx`, `edmonton.ca/.../lrt-network` and
   `gotransit.com/en/find-a-station` all returned HTTP 404 or blocked. Where that happened,
   the claim rests on Wikipedia line and station articles that **were** fetched, and in the
   GO/REM cases on official pages that did serve (`gotransit.com` Stratford and Niagara
   pages, `metrolinx.com` project pages, `rem.info` press release, `exo.quebec` live status).
2. **exo.quebec never rendered station lists** - the schedule pages are JavaScript-driven.
   exo's own site confirmed the five line names and live status; station-to-municipality
   mapping is from Wikipedia line and station articles.
3. **No source enumerates the municipality of all 68 Montréal Métro stations one by one.**
   Both the EN and FR articles name only the Laval three and the Longueuil one as
   off-island. That "no other municipality has a métro station" is therefore a
   verified-by-omission finding, not an explicit negative statement.
4. **Not every Toronto GO station was infobox-verified individually.** Two independent
   sources agree and none were contested. Every *disputed* station (Aldershot, Milliken,
   Gormley, Bloomington, Langstaff, Georgetown, Acton, Sainte-Catherine,
   Pincourt-Terrasse-Vaudreuil) was resolved against the station's own page.
5. **A few exo Vaudreuil-Hudson mid-line stations** (Beaurepaire, Cedar Park, Valois, Pine
   Beach, Île-Perrot) come from the line article, not each station's own page. They do not
   change the municipality list, which is also supported by terminus and named stations.
6. `data/climate.json` holds **712** entries, not the 710 quoted in the brief. All 79 keys
   written here were validated against it programmatically; the build aborts on any key
   that does not match a real `name` + `prov` pair.
