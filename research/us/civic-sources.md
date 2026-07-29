# US civic data (pro sports + rapid transit) - claim-by-claim sourcing

Research date: **2026-07-29**. Output: `data/us/civic.json`.
Companion to the Canadian file `research/civic-sources.md` / `data/civic.json`; identical
schema, with `state` (2-letter USPS) replacing `prov`.

**Every URL below was actually opened during this build.** Wikipedia article text was
pulled as raw wikitext through the MediaWiki API
(`https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvslots=main&titles=...`),
so the quotes below are the article source, not a summary. Official transit-agency sites
were tried at least once per system; where one blocked or 404'd, that is stated in Part 4
and the claim rests on the Wikipedia line and station articles that did serve.

Where a fact could not be verified, the entry was **left out of the dataset** and the
omission is logged in Part 3. Nothing in this file is from memory.

## Method for the trap the brief warned about

For sports, the deciding evidence is always the **venue's** article, not the team's name:
its `location =` infobox field and its `{{Short description}}`, both of which name a
municipality. Where the two disagreed (Michelob Ultra Arena's short description says "Las
Vegas" while its location field and street address say Paradise) the location field and
address won, and the conflict is recorded. Forty-two US teams are keyed to a
municipality (or state) other than the one in their name.

For transit, the deciding evidence is a **station-level** source: a `List of <system>
stations` article with a City/Municipality/Location column, or the individual station
article's address, or - where the agency's own API served (MBTA, and others noted in
Part 4) - the agency's own `municipality` field. Anchor cities alone were never accepted;
the suburb list is the point of the exercise.

## Totals in `data/us/civic.json`

**1056 records** across 36 states/territories.

- **74 places with a pro team**, 172 team-slots.
- **1027 places with rapid transit**: 119 subway, 168 light rail, 740 commuter rail.
- 45 places have both.

Teams by league:

| League | US teams |
|---|---|
| MLB | 29 |
| MLS | 27 |
| NBA | 29 |
| NFL | 32 |
| NHL | 25 |
| NWSL | 16 |
| WNBA | 14 |

Places by transit system:

| System | type | places |
|---|---|---|
| NJ Transit Rail | `commuter rail` | 117 |
| Metra | `commuter rail` | 111 |
| Long Island Rail Road | `commuter rail` | 92 |
| Metro-North Railroad | `commuter rail` | 86 |
| MBTA Commuter Rail | `commuter rail` | 77 |
| SEPTA Regional Rail | `commuter rail` | 67 |
| Metrolink | `commuter rail` | 41 |
| Washington Metro | `subway` | 33 |
| BART | `subway` | 26 |
| LA Metro Rail | `light rail` | 26 |
| MARC Train | `commuter rail` | 23 |
| MetroLink | `light rail` | 15 |
| SEPTA Metro | `light rail` | 15 |
| Tri-Rail | `commuter rail` | 13 |
| Link light rail | `light rail` | 12 |
| River LINE | `light rail` | 12 |
| Caltrain | `commuter rail` | 11 |
| FrontRunner | `commuter rail` | 11 |
| MBTA subway | `subway` | 11 |
| DART Rail | `light rail` | 10 |
| RTD Light Rail | `light rail` | 10 |
| SunRail | `commuter rail` | 10 |
| MARTA | `subway` | 9 |
| Miami Metrorail | `subway` | 9 |
| South Shore Line | `commuter rail` | 9 |
| TRAX | `light rail` | 9 |
| Chicago "L" | `subway` | 8 |
| New Mexico Rail Runner Express | `commuter rail` | 8 |
| RTD Commuter Rail | `commuter rail` | 8 |
| SMART | `commuter rail` | 8 |
| Virginia Railway Express | `commuter rail` | 8 |
| CTrail Hartford Line | `commuter rail` | 7 |
| PATCO Speedline | `subway` | 7 |
| Sacramento RT Light Rail | `light rail` | 7 |
| San Diego Trolley | `light rail` | 7 |
| Shore Line East | `commuter rail` | 7 |
| Sounder commuter rail | `commuter rail` | 7 |
| Baltimore Light RailLink | `light rail` | 6 |
| MAX Light Rail | `light rail` | 6 |
| Pittsburgh Light Rail | `light rail` | 5 |
| Altamont Corridor Express | `commuter rail` | 4 |
| Hudson-Bergen Light Rail | `light rail` | 4 |
| PATH | `subway` | 4 |
| RTA Rapid Transit | `light rail` | 4 |
| SPRINTER | `light rail` | 4 |
| VTA light rail | `light rail` | 4 |
| Baltimore Metro SubwayLink | `subway` | 3 |
| COASTER | `commuter rail` | 3 |
| METRO light rail | `light rail` | 3 |
| SEPTA Metro | `subway` | 3 |
| Tren Urbano | `subway` | 3 |
| Valley Metro Rail | `light rail` | 3 |
| WES Commuter Rail | `commuter rail` | 3 |
| WeGo Star | `commuter rail` | 3 |
| A-train | `commuter rail` | 2 |
| CapMetro Rail | `commuter rail` | 2 |
| LA Metro Rail | `subway` | 2 |
| Newark Light Rail | `light rail` | 2 |
| Buffalo Metro Rail | `light rail` | 1 |
| Lynx Blue Line | `light rail` | 1 |
| METRORail | `light rail` | 1 |
| New York City Subway | `subway` | 1 |
| TEXRail | `commuter rail` | 1 |
| The Tide | `light rail` | 1 |
| Trinity Railway Express | `commuter rail` | 1 |

---
## PART 1 - PRO SPORTS

**Rule applied:** a team counts for a place only if it plays its home games inside that
municipality's boundary. Being *named* for a metro is not enough. **Forty-two US teams** failed that test and are keyed to a place other than the one in
their name; every one is listed in 1.3.

### 1.1 Leagues covered, US team counts, and the article opened

| League | US teams found | Primary source opened |
|---|---|---|
| NFL | 32 | https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums |
| NBA | 29 | https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_arenas |
| MLB | 29 | https://en.wikipedia.org/wiki/List_of_Major_League_Baseball_stadiums |
| NHL | 25 | https://en.wikipedia.org/wiki/List_of_National_Hockey_League_arenas |
| MLS | 27 | https://en.wikipedia.org/wiki/2026_Major_League_Soccer_season |
| WNBA | 14 | https://en.wikipedia.org/wiki/2026_WNBA_season |
| NWSL | 16 | https://en.wikipedia.org/wiki/2026_National_Women%27s_Soccer_League_season |

Totals reconcile against each league's own size: NBA 30 minus Toronto = 29; MLB 30 minus
Toronto = 29; NHL 32 minus the seven Canadian clubs = 25; MLS 30 minus Toronto, Montréal,
Vancouver = 27; WNBA 15 minus Toronto = 14; NWSL 16, all American. **172 team-slots across
74 places.**

The MLS count is anchored on the 2026 season article's own infobox, verbatim:
*"num_teams = 30"*, and on the article's full stadium table, which was read row by row.
The NWSL count is anchored on the 2026 season article's stadium table (16 rows) plus
*"Boston Legacy and Denver Summit are playing their inaugural season."*
The WNBA count is anchored on the 2026 season article: *"The league expanded from 13 to 15
teams with the addition of the Portland Fire and Toronto Tempo ... This followed the
addition of the Golden State Valkyries in 2025."*

### 1.2 The 2025-2026 changes a stale dataset would get wrong

1. **The Oakland Athletics no longer exist as "Oakland", and Oakland CA gets nothing.**
   The club is now just the **Athletics**, playing in **West Sacramento, California**.
   https://en.wikipedia.org/wiki/Athletics_(baseball_team) - short description
   *"Major League Baseball franchise in West Sacramento, California"*, infobox
   *"misc = Based in West Sacramento since 2025"*, and an in-source editor note
   *"Please DO NOT change to Las Vegas until the club officially relocates to that city."*
   Venue: https://en.wikipedia.org/wiki/Sutter_Health_Park - *"Baseball park in West
   Sacramento, California"*. The MLB stadium list confirms the row
   *"Sutter Health Park | 13,416 | West Sacramento, California | Grass | Athletics"*.
   The Las Vegas ballpark is in the list's **future** table (Paradise NV, 2028), so
   **Paradise gets no MLB team yet**. **Oakland, CA is absent from this dataset entirely.**

2. **Inter Miami CF moved into Miami proper for 2026.** Nu Stadium at Miami Freedom Park
   opened April 2026. https://en.wikipedia.org/wiki/Nu_Stadium - infobox
   *"address = 1900 NW 37th Avenue"*, *"location = Miami Freedom Park, Miami, Florida"*,
   caption *"The stadium on its opening day in April 2026"*. The 2026 MLS stadium table
   lists *"Inter Miami CF | Nu Stadium | 26,700"*. The club's old home was in Fort
   Lauderdale, so **Fort Lauderdale loses its MLS entry** and Miami gains one.

3. **The Tampa Bay Rays are back in St. Petersburg.** Hurricane Milton pushed them to
   Tampa's Steinbrenner Field for all of 2025. https://en.wikipedia.org/wiki/Tampa_Bay_Rays
   - *"the Rays have returned to Tropicana Field for the 2026 season"*, and pastparks
   *"George M. Steinbrenner Field (2025)"*. https://en.wikipedia.org/wiki/Tropicana_Field -
   infobox *"reopened = April 6, 2026"*. So **St. Petersburg FL, not Tampa**, has the MLB
   team. Tampa still has the NFL Buccaneers and NHL Lightning.

4. **Utah Mammoth** is the current name of the ex-Arizona franchise, at the Delta Center in
   Salt Lake City. https://en.wikipedia.org/wiki/Utah_Mammoth - infobox history
   *"Utah Mammoth 2025-present"*, *"arena = Delta Center"*, *"city = Salt Lake City, Utah"*.
   **Phoenix/Glendale AZ has no NHL team.**

5. **Three brand-new franchises played their first games in 2026 and are in the data:**
   - **Portland Fire (WNBA)** - https://en.wikipedia.org/wiki/Portland_Fire - infobox
     *"Portland Fire 2026-present"*, *"arena = Moda Center"*, *"location = Portland, Oregon"*.
   - **Boston Legacy FC (NWSL)** - https://en.wikipedia.org/wiki/Boston_Legacy_FC -
     *"Joining in 2026 ... the club plans to play its inaugural season at Gillette Stadium
     in Foxborough"*. Keyed to **Foxborough MA**, not Boston.
   - **Denver Summit FC (NWSL)** - https://en.wikipedia.org/wiki/2026_Denver_Summit_FC_season
     - *"The Summit play their home games at Centennial Stadium, in Centennial, Colorado."*
     Keyed to **Centennial CO**, not Denver. The permanent stadium slipped: the club article
     notes *"In July 2026, the team announced delays may push the opening 'closer to the
     opening of the 2029 season'"*.
   Golden State Valkyries (WNBA, 2025, San Francisco) is also included and sourced.

6. **The Chicago Stars FC left Bridgeview for Evanston.**
   https://en.wikipedia.org/wiki/Chicago_Stars_FC - *"In September 2025, with the club's
   lease at SeatGeek Stadium in Bridgeview set to expire, the Stars announced they would
   play the 2026 season at Northwestern Medicine Field at Martin Stadium."*
   https://en.wikipedia.org/wiki/Martin_Stadium_(Northwestern_University) - *"location =
   Evanston, Illinois"*. **Bridgeview IL is out, Evanston IL is in.**

7. **The Connecticut Sun's last season in Connecticut is 2026.**
   https://en.wikipedia.org/wiki/2026_WNBA_season - *"This will be the last season for the
   Connecticut Sun in Uncasville, Connecticut after Houston Rockets owner Tilman Fertitta
   purchased the franchise with the intention to relocate the team to Houston to revive the
   Houston Comets."* The Sun *are* in the 2026 data at Uncasville; the Houston Comets are
   **not**, because they have not played. Flag for a 2027 refresh.

8. **Not yet, so not counted:** the Cleveland Browns' Brook Park OH stadium and the
   Commanders' RFK-campus stadium are both in the NFL list's *future* table; the Bears',
   Broncos', Chiefs (Kansas City **Kansas**), Titans and Rays replacement venues likewise.
   Same for the OKC Thunder, 76ers, Mavericks and Spurs future arenas in the NBA list, and
   the Flames/Stars(Plano)/Flyers/Senators future arenas in the NHL list.

### 1.3 Every "named for city X, actually plays in city Y" case found

| Team | Named for | Plays in | Proof |
|---|---|---|---|
| New York Giants (NFL) | New York | **East Rutherford, NJ** | https://en.wikipedia.org/wiki/MetLife_Stadium - *"Stadium in East Rutherford, New Jersey"*, *"location = East Rutherford, New Jersey"* |
| New York Jets (NFL) | New York | **East Rutherford, NJ** | same |
| Dallas Cowboys (NFL) | Dallas | **Arlington, TX** | https://en.wikipedia.org/wiki/AT%26T_Stadium - *"Stadium in Arlington, Texas"* |
| Texas Rangers (MLB) | Texas | **Arlington, TX** | https://en.wikipedia.org/wiki/Globe_Life_Field - *"Baseball park in Arlington, Texas"* |
| Dallas Wings (WNBA) | Dallas | **Arlington, TX** | https://en.wikipedia.org/wiki/College_Park_Center - *"Multi-purpose arena in Arlington, Texas"*; team infobox *"arena = College Park Center, location = Arlington, Texas"* |
| San Francisco 49ers (NFL) | San Francisco | **Santa Clara, CA** | https://en.wikipedia.org/wiki/Levi%27s_Stadium - *"Stadium in Santa Clara, California"* |
| Washington Commanders (NFL) | Washington | **Landover, MD** | https://en.wikipedia.org/wiki/Northwest_Stadium - *"Stadium in Landover, Maryland"* |
| Miami Dolphins (NFL) | Miami | **Miami Gardens, FL** | https://en.wikipedia.org/wiki/Hard_Rock_Stadium - *"Multi-purpose stadium in Miami Gardens, Florida"* |
| New England Patriots (NFL) | New England | **Foxborough, MA** | https://en.wikipedia.org/wiki/Gillette_Stadium - *"Stadium in Foxborough, Massachusetts"* |
| New England Revolution (MLS) | New England | **Foxborough, MA** | same |
| Boston Legacy FC (NWSL) | Boston | **Foxborough, MA** | https://en.wikipedia.org/wiki/Boston_Legacy_FC |
| Buffalo Bills (NFL) | Buffalo | **Orchard Park, NY** | https://en.wikipedia.org/wiki/Highmark_Stadium - *"Stadium in Orchard Park, New York"* |
| Las Vegas Raiders (NFL) | Las Vegas | **Paradise, NV** | https://en.wikipedia.org/wiki/Allegiant_Stadium - *"Stadium in Paradise, Nevada"* |
| Vegas Golden Knights (NHL) | Las Vegas | **Paradise, NV** | https://en.wikipedia.org/wiki/T-Mobile_Arena - *"Multi-purpose indoor arena in Paradise, Nevada"* |
| Las Vegas Aces (WNBA) | Las Vegas | **Paradise, NV** | https://en.wikipedia.org/wiki/Michelob_Ultra_Arena - *"location = Paradise, Nevada"* (its own short description says "Las Vegas" - the location field and address 3950 S Las Vegas Blvd are the Strip, which is Paradise) |
| Los Angeles Rams (NFL) | Los Angeles | **Inglewood, CA** | https://en.wikipedia.org/wiki/SoFi_Stadium - *"Stadium in Inglewood, California"* |
| Los Angeles Chargers (NFL) | Los Angeles | **Inglewood, CA** | same |
| Los Angeles Clippers (NBA) | Los Angeles | **Inglewood, CA** | https://en.wikipedia.org/wiki/Intuit_Dome - *"Indoor arena in Inglewood, California"* |
| Arizona Cardinals (NFL) | Arizona | **Glendale, AZ** | https://en.wikipedia.org/wiki/State_Farm_Stadium - *"Stadium in Glendale, Arizona"* |
| Atlanta Braves (MLB) | Atlanta | **Cumberland, GA** | https://en.wikipedia.org/wiki/Truist_Park - *"Baseball park in Metro Atlanta, Georgia"*, *"location = Cumberland, Georgia"* with the editor note *"Please do not change the location without consensus"*. Cumberland is an unincorporated CDP in Cobb County. |
| Atlanta Dream (WNBA) | Atlanta | **College Park, GA** | https://en.wikipedia.org/wiki/Gateway_Center_Arena - *"Indoor arena in suburban Atlanta"*, *"location = College Park, Georgia"* |
| Los Angeles Angels (MLB) | Los Angeles | **Anaheim, CA** | https://en.wikipedia.org/wiki/Angel_Stadium - *"Baseball park in Anaheim, California"* |
| Athletics (MLB) | (formerly Oakland) | **West Sacramento, CA** | see 1.2 item 1 |
| Tampa Bay Rays (MLB) | Tampa Bay | **St. Petersburg, FL** | https://en.wikipedia.org/wiki/Tropicana_Field |
| Florida Panthers (NHL) | Florida | **Sunrise, FL** | https://en.wikipedia.org/wiki/Amerant_Bank_Arena - *"Indoor arena in Sunrise, Florida"* |
| Minnesota Wild (NHL) | Minnesota | **Saint Paul, MN** | https://en.wikipedia.org/wiki/Grand_Casino_Arena - *"Arena in Saint Paul, Minnesota"* (renamed from Xcel Energy Center) |
| Minnesota United FC (MLS) | Minnesota | **Saint Paul, MN** | https://en.wikipedia.org/wiki/Allianz_Field - *"Soccer stadium in St. Paul, Minnesota"* |
| New Jersey Devils (NHL) | New Jersey | **Newark, NJ** | NHL arena list row *"Prudential Center | Newark, New Jersey | New Jersey Devils"* |
| New York Islanders (NHL) | New York | **Elmont, NY** | https://en.wikipedia.org/wiki/UBS_Arena - *"Multi-purpose indoor arena in Elmont, New York"*. Elmont is an unincorporated CDP in the Town of Hempstead. |
| Colorado Rapids (MLS) | Colorado | **Commerce City, CO** | https://en.wikipedia.org/wiki/Dick%27s_Sporting_Goods_Park - *"Soccer stadium in Commerce City, Colorado"* |
| LA Galaxy (MLS) | Los Angeles | **Carson, CA** | https://en.wikipedia.org/wiki/Dignity_Health_Sports_Park - *"Sports complex and stadium in Carson, California"* |
| FC Dallas (MLS) | Dallas | **Frisco, TX** | https://en.wikipedia.org/wiki/Toyota_Stadium_(Frisco,_Texas) - *"location = Frisco, Texas"* |
| New York Red Bulls (MLS) | New York | **Harrison, NJ** | https://en.wikipedia.org/wiki/Sports_Illustrated_Stadium - *"location = Harrison, New Jersey"* |
| Gotham FC (NWSL) | New York / New Jersey | **Harrison, NJ** | same; club infobox *"stadium = Sports Illustrated Stadium, Harrison, New Jersey"* |
| Philadelphia Union (MLS) | Philadelphia | **Chester, PA** | https://en.wikipedia.org/wiki/Subaru_Park - *"Soccer stadium in Chester, Pennsylvania"* |
| Real Salt Lake (MLS) | Salt Lake | **Sandy, UT** | https://en.wikipedia.org/wiki/America_First_Field - *"Soccer stadium in Sandy, Utah"* |
| Utah Royals (NWSL) | Utah | **Sandy, UT** | same; club infobox *"stadium = America First Field, Sandy, Utah"* |
| Sporting Kansas City (MLS) | Kansas City | **Kansas City, KANSAS** | https://en.wikipedia.org/wiki/Sporting_Park - *"Soccer stadium in Kansas City, Kansas"*. Distinct from the Chiefs / Royals / KC Current, all in Kansas City **Missouri**. |
| North Carolina Courage (NWSL) | North Carolina | **Cary, NC** | https://en.wikipedia.org/wiki/WakeMed_Soccer_Park - *"Soccer stadium in Cary, North Carolina"* |
| Chicago Stars FC (NWSL) | Chicago | **Evanston, IL** | see 1.2 item 6 |
| Denver Summit FC (NWSL) | Denver | **Centennial, CO** | see 1.2 item 5 |
| Connecticut Sun (WNBA) | Connecticut | **Uncasville, CT** | https://en.wikipedia.org/wiki/Mohegan_Sun_Arena - *"address = 1 Mohegan Sun Boulevard"*, *"location = Uncasville, Connecticut"* |

### 1.4 Traps that turned out NOT to be traps

- **Detroit Pistons are genuinely in Detroit.** They left the Palace of Auburn Hills in
  2017. https://en.wikipedia.org/wiki/Little_Caesars_Arena - *"Multi-purpose arena in
  Detroit, Michigan"*, *"location = Detroit, Michigan"*. Auburn Hills MI gets nothing.
- **Brooklyn Nets, New York Mets, New York Yankees, New York City FC, New York Liberty.**
  Brooklyn, Queens and the Bronx are boroughs of New York City, not Census places. All key
  to **New York, NY**. Sources: NBA arena list (*"Barclays Center | Brooklyn, New York"*),
  MLB stadium list (*"Citi Field | Queens, New York"*, *"Yankee Stadium | Bronx, New
  York"*), the 2026 MLS table (*"New York City FC | Yankee Stadium / Citi Field"*), and
  https://en.wikipedia.org/wiki/New_York_Liberty (*"arena = Barclays Center, location =
  Brooklyn, New York City"*).
- **Anaheim Ducks** really are in Anaheim: https://en.wikipedia.org/wiki/Honda_Center -
  *"Multi-purpose indoor arena in Anaheim, California"*.
- **Kansas City Chiefs, Royals and Current** are all in Kansas City **Missouri**
  (Arrowhead and Kauffman per the NFL/MLB lists; CPKC Stadium per
  https://en.wikipedia.org/wiki/CPKC_Stadium - *"Soccer stadium in Kansas City, Missouri"*).
  Only Sporting KC is in Kansas.
- **Washington Mystics** are in DC, not Maryland: https://en.wikipedia.org/wiki/CareFirst_Arena
  - *"Multipurpose arena in Washington, D.C."*, *"address = 1100 Oak Drive SE"*.

---

## PART 2 - RAPID TRANSIT

`transit_type` uses the closed vocabulary `subway` / `light rail` / `commuter rail`.
Where a place is served by more than one system the **highest tier wins** the type and
the name (subway > light rail > commuter rail), and every system's source URL is still
carried in that record's `sources`. Per the brief, the MBTA Green Line is filed as
`subway` alongside the Red/Orange/Blue lines, and Cleveland's heavy-rail Red Line is
filed as `light rail` with the RTA's light-rail Blue/Green lines; both departures from a
strict technical reading are flagged in their sections.

The eight regional sections below are the raw claim-by-claim logs. Each one lists the
systems it covered, how station-to-municipality was established, its place-by-place
table with URLs, its streetcar judgement calls, and what it deliberately excluded.

### 2.1 New York City core + all of New Jersey

Scope: NYC Subway, Staten Island Railway, PATH, Hudson-Bergen Light Rail, Newark Light Rail,
River LINE, and all 12 NJ Transit Rail Operations lines. **All New York State stations were
skipped** (Port Jervis Line and the Pascack Valley Line north of the state border are operated
for Metro-North and belong to another agent).

**143 Census places output** - 5 subway, 19 light rail, 119 commuter rail.

#### Systems covered

| System | Type assigned | Source URL(s) | How station -> city was established |
|---|---|---|---|
| New York City Subway | subway | [https://en.wikipedia.org/wiki/New_York_City_Subway](https://en.wikipedia.org/wiki/New_York_City_Subway) | Lead: "a rapid transit system in New York City, serving four of the city's five boroughs: Manhattan, Brooklyn, Queens, and the Bronx." All 472 open stations are inside the city, so exactly one Census place: New York. Boroughs are not Census places. |
| Staten Island Railway | subway | [https://en.wikipedia.org/wiki/Staten_Island_Railway](https://en.wikipedia.org/wiki/Staten_Island_Railway) | Lead: "a rapid transit line in the New York City borough of Staten Island." Entirely inside New York City -> no new place. |
| PATH | subway | [https://en.wikipedia.org/wiki/PATH_(rail_system)](https://en.wikipedia.org/wiki/PATH_(rail_system)) | Article's "Station list" table has explicit State and City columns. Open stations: New York NY (Ninth St, 14th St, 23rd St, 33rd St, Christopher St, World Trade Center); Jersey City NJ (Exchange Place, Grove Street, Journal Square, Newport); Harrison NJ; Hoboken NJ; Newark NJ. |
| Hudson-Bergen Light Rail | light rail | [https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) | "Stations" table's first column is City, with rowspans. 24 stations across exactly 6 municipalities. |
| Newark Light Rail | light rail | [https://en.wikipedia.org/wiki/Newark_Light_Rail](https://en.wikipedia.org/wiki/Newark_Light_Rail) | "Stations" table's first column is Location. City Subway line: 10 open stations in Newark, Silver Lake in Belleville, Grove Street in Bloomfield. Broad Street branch: "All stations are in Newark." |
| River LINE | light rail | [https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) | "Stations" table's first column is Location with rowspans; individual station articles used to settle Beverly/Edgewater Park, Hamilton Avenue, Bordentown, Cass Street. |
| NJ Transit Rail Operations (all 12 lines) | commuter rail | [https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) | "Active stations" tables carry a Location column per station. 151 rows "Operated by NJ Transit" + 14 "Operated by others" = the 165 stations the article's lead cites. ~30 township / mis-named stations were then confirmed one by one against their own station articles (address + lead sentence). |

Line coverage check (from the Lines column of the station table): Northeast Corridor, North Jersey
Coast, Raritan Valley, Morristown, Gladstone, Montclair-Boonton, Main, Bergen County, Pascack
Valley, Port Jervis (NY only - skipped), Atlantic City, Princeton (the "Dinky") = all 12, plus the
event-only Meadowlands service.

#### Place-by-place

##### New York City Subway / Staten Island Railway / PATH

| Place | State | Station(s) | Notes | Source |
|---|---|---|---|---|
| New York | NY | all 472 subway stations + all 21 Staten Island Railway stations + PATH 9th/14th/23rd/33rd St, Christopher St, World Trade Center |  | [1](https://en.wikipedia.org/wiki/New_York_City_Subway) [2](https://en.wikipedia.org/wiki/Staten_Island_Railway) [3](https://en.wikipedia.org/wiki/PATH_(rail_system)) |

##### PATH

| Place | State | Station(s) | Notes | Source |
|---|---|---|---|---|
| Harrison | NJ | Harrison |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) |
| Hoboken | NJ | Hoboken |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) [2](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) [3](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Jersey City | NJ | Exchange Place, Grove Street, Journal Square, Newport |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) [2](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) |
| Newark | NJ | Newark Penn Station |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) [2](https://en.wikipedia.org/wiki/Newark_Light_Rail) [3](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |

##### Hudson-Bergen Light Rail

| Place | State | Station(s) | Notes | Source |
|---|---|---|---|---|
| Bayonne | NJ | 45th Street, 34th Street, 22nd Street, 8th Street |  | [1](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) |
| Hoboken | NJ | 9th Street-Congress Street, 2nd Street, Hoboken Terminal |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) [2](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) [3](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Jersey City | NJ | Newport, Harsimus Cove, Harborside, Exchange Place, Essex Street, Marin Boulevard, Jersey Avenue, Liberty State Park, Garfield Avenue, Martin Luther King Drive, West Side Avenue, Richard Street, Danforth Avenue |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) [2](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) |
| North Bergen | NJ | Tonnelle Avenue | North Bergen Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) |
| Union City | NJ | Bergenline Avenue |  | [1](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) |
| Weehawken | NJ | Port Imperial, Lincoln Harbor | Weehawken Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) |

##### Newark Light Rail

| Place | State | Station(s) | Notes | Source |
|---|---|---|---|---|
| Belleville | NJ | Silver Lake | Belleville Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/Newark_Light_Rail) |
| Bloomfield | NJ | Grove Street | Bloomfield Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/Newark_Light_Rail) [2](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Newark | NJ | Newark Penn, Military Park, Washington Street, Warren Street/NJIT, Norfolk Street, Orange Street, Park Avenue, Bloomfield Avenue, Davenport Avenue, Branch Brook Park + Broad Street branch (NJPAC/Center Street, Harriet Tubman Square, Atlantic Street, Riverfront Stadium, Newark Broad Street) |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) [2](https://en.wikipedia.org/wiki/Newark_Light_Rail) [3](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |

##### River LINE

| Place | State | Station(s) | Notes | Source |
|---|---|---|---|---|
| Beverly | NJ | Beverly/Edgewater Park | Station is in Beverly city despite the name; Edgewater Park Township has no station | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) [2](https://en.wikipedia.org/wiki/Beverly/Edgewater_Park_station) |
| Bordentown | NJ | Bordentown |  | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) [2](https://en.wikipedia.org/wiki/Bordentown_station) |
| Burlington | NJ | Burlington Towne Centre, Burlington South |  | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) |
| Camden | NJ | Walter Rand Transportation Center, Cooper Street-Rutgers University, Aquarium, Entertainment Center |  | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) |
| Cinnaminson | NJ | Cinnaminson | Cinnaminson Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) |
| Delanco | NJ | Delanco | Delanco Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) |
| Florence | NJ | Florence | Florence Township; Florence CDP is the village in it | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) [2](https://en.wikipedia.org/wiki/Florence_station_(River_Line)) |
| Palmyra | NJ | Palmyra |  | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) |
| Pennsauken | NJ | Pennsauken-Route 73, Pennsauken Transit Center, 36th Street | Pennsauken Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) [2](https://en.wikipedia.org/wiki/Pennsauken_Transit_Center) [3](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Riverside | NJ | Riverside | Riverside Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) |
| Riverton | NJ | Riverton |  | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) |
| Roebling | NJ | Roebling | Roebling CDP, Florence Township | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) [2](https://en.wikipedia.org/wiki/Roebling_station) |
| Trenton | NJ | Trenton, Hamilton Avenue, Cass Street |  | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) [2](https://en.wikipedia.org/wiki/Hamilton_Avenue_station_(River_Line)) [3](https://en.wikipedia.org/wiki/Cass_Street_station) |

##### NJ Transit Rail

| Place | State | Station(s) | Notes | Source |
|---|---|---|---|---|
| Aberdeen | NJ | Aberdeen–Matawan | Aberdeen Township (MCD); NJ townships are not Census places, township name used per spec. Station straddles Aberdeen Township and Matawan borough. | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Aberdeen%E2%80%93Matawan_station) |
| Absecon | NJ | Absecon |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Allendale | NJ | Allendale |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Allenhurst | NJ | Allenhurst |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Annandale | NJ | Annandale | Annandale CDP, Clinton Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Annandale_station) |
| Asbury Park | NJ | Asbury Park |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Atco | NJ | Atco | Atco CDP, Waterford Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Atco_station) |
| Atlantic City | NJ | Atlantic City |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Avenel | NJ | Avenel | Avenel CDP, Woodbridge Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Avenel_station) |
| Basking Ridge | NJ | Basking Ridge; Lyons | Basking Ridge CDP, Bernards Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Basking_Ridge_station) [3](https://en.wikipedia.org/wiki/Lyons_station) |
| Bay Head | NJ | Bay Head |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Belmar | NJ | Belmar |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Berkeley Heights | NJ | Berkeley Heights | Berkeley Heights Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Bernardsville | NJ | Bernardsville |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Bloomfield | NJ | Bloomfield; Watsessing Avenue | Bloomfield Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/Newark_Light_Rail) [2](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Boonton | NJ | Boonton |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Bound Brook | NJ | Bound Brook |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Bradley Beach | NJ | Bradley Beach |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Branchburg | NJ | North Branch | Branchburg Township (MCD); township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/North_Branch_station) |
| Bridgewater | NJ | Bridgewater | Bridgewater Township (MCD); township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Bridgewater_station_(NJ_Transit)) |
| Budd Lake | NJ | Mount Olive | Budd Lake CDP, Mount Olive Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Mount_Olive_station) |
| Chatham | NJ | Chatham |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Cherry Hill | NJ | Cherry Hill | Cherry Hill Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Clifton | NJ | Clifton; Delawanna |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Cranford | NJ | Cranford | Cranford CDP, coextensive with Cranford Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Cranford_station) |
| Denville | NJ | Denville; Mount Tabor | Denville Township (MCD); township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Denville_station) [3](https://en.wikipedia.org/wiki/Mount_Tabor_station) |
| Dover | NJ | Dover |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Dunellen | NJ | Dunellen |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| East Orange | NJ | Brick Church; East Orange |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| East Rutherford | NJ | Meadowlands |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Edison | NJ | Edison | Edison Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Egg Harbor City | NJ | Egg Harbor City |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Elizabeth | NJ | Elizabeth; North Elizabeth |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Emerson | NJ | Emerson |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Fair Lawn | NJ | Broadway; Radburn |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Broadway_station_(NJ_Transit)) [3](https://en.wikipedia.org/wiki/Radburn_station) |
| Fanwood | NJ | Fanwood |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Far Hills | NJ | Far Hills |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Garfield | NJ | Garfield; Plauderville |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Garwood | NJ | Garwood |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Gillette | NJ | Gillette | Gillette CDP, Long Hill Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Gillette_station) |
| Glen Ridge | NJ | Glen Ridge |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Glen Rock | NJ | Glen Rock–Boro Hall; Glen Rock–Main Line |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Hackensack | NJ | Anderson Street; Essex Street |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Hackettstown | NJ | Hackettstown |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Hamilton | NJ | Hamilton | Hamilton Township, Mercer County (MCD); township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Hamilton_station_(NJ_Transit)) |
| Hammonton | NJ | Hammonton |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Hawthorne | NJ | Hawthorne |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Hazlet | NJ | Hazlet | Hazlet Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| High Bridge | NJ | High Bridge |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Hillsdale | NJ | Hillsdale |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Ho-Ho-Kus | NJ | Ho-Ho-Kus |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Hoboken | NJ | Hoboken Terminal |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) [2](https://en.wikipedia.org/wiki/Hudson%E2%80%93Bergen_Light_Rail) [3](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Iselin | NJ | Metropark | Iselin CDP, Woodbridge Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Metropark_station) |
| Landing | NJ | Lake Hopatcong | Landing CDP, Roxbury Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Lake_Hopatcong_station) |
| Lebanon | NJ | Lebanon |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Lincoln Park | NJ | Lincoln Park |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Linden | NJ | Linden |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Lindenwold | NJ | Lindenwold |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Little Falls | NJ | Little Falls; Montclair State University | Little Falls Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Montclair_State_University_station) |
| Little Silver | NJ | Little Silver |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Long Branch | NJ | Elberon; Long Branch |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Lyndhurst | NJ | Lyndhurst | Lyndhurst Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Madison | NJ | Madison |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Mahwah | NJ | Mahwah | Mahwah Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Manasquan | NJ | Manasquan |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Maplewood | NJ | Maplewood | Maplewood Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Matawan | NJ | Aberdeen–Matawan |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Aberdeen%E2%80%93Matawan_station) |
| Metuchen | NJ | Metuchen |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Middletown | NJ | Middletown | Middletown Township (MCD); township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Middletown_station_(NJ_Transit)) |
| Millburn | NJ | Millburn | Millburn Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Millington | NJ | Millington | Millington CDP, Long Hill Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Millington_station) |
| Montclair | NJ | Bay Street; Montclair Heights; Mountain Avenue; Walnut Street; Watchung Avenue | Montclair Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Montclair_Heights_station) |
| Montvale | NJ | Montvale |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Morris | NJ | Convent Station | Morris Township (MCD); Convent Station is an unincorporated community in it, not a CDP | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Convent_Station_(NJ_Transit)) |
| Morris Plains | NJ | Morris Plains |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Morristown | NJ | Morristown |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Mount Arlington | NJ | Mount Arlington |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Mountain Lakes | NJ | Mountain Lakes |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Netcong | NJ | Netcong |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| New Brunswick | NJ | Jersey Avenue; New Brunswick |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Jersey_Avenue_station) |
| New Providence | NJ | Murray Hill; New Providence | Murray Hill is a section of New Providence borough; no Murray Hill CDP | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Murray_Hill_station_(NJ_Transit)) |
| Newark | NJ | Newark Broad Street; Newark Penn Station; Newark Liberty International Airport (NEC / North Jersey Coast Line) |  | [1](https://en.wikipedia.org/wiki/PATH_(rail_system)) [2](https://en.wikipedia.org/wiki/Newark_Light_Rail) [3](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Oceanport | NJ | Monmouth Park |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Oradell | NJ | Oradell |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Orange | NJ | Highland Avenue; Orange |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Park Ridge | NJ | Park Ridge |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Passaic | NJ | Passaic |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Paterson | NJ | Paterson |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Peapack and Gladstone | NJ | Gladstone; Peapack |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Pennsauken | NJ | Pennsauken Transit Center | Pennsauken Township (MCD); NJ townships are not Census places, township name used per spec | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) [2](https://en.wikipedia.org/wiki/Pennsauken_Transit_Center) [3](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Perth Amboy | NJ | Perth Amboy |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Plainfield | NJ | Netherwood; Plainfield |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Point Pleasant Beach | NJ | Point Pleasant Beach |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Princeton | NJ | Princeton |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Princeton Junction | NJ | Princeton Junction | Princeton Junction CDP, West Windsor Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Princeton_Junction_station) |
| Rahway | NJ | Rahway |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Ramsey | NJ | Ramsey; Ramsey Route 17 |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Raritan | NJ | Raritan |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Red Bank | NJ | Red Bank |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Ridgewood | NJ | Ridgewood |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| River Edge | NJ | New Bridge Landing; River Edge |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Roselle Park | NJ | Roselle Park |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Rutherford | NJ | Rutherford |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Secaucus | NJ | Secaucus Junction |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Short Hills | NJ | Short Hills | Short Hills CDP, Millburn Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Short_Hills_station) |
| Somerville | NJ | Somerville |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| South Amboy | NJ | South Amboy |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| South Orange | NJ | Mountain Station; South Orange |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Spring Lake | NJ | Spring Lake |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Stirling | NJ | Stirling | Stirling CDP, Long Hill Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Stirling_station_(NJ_Transit)) |
| Summit | NJ | Summit |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Teterboro | NJ | Teterboro |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Towaco | NJ | Towaco | Towaco CDP, Montville Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Trenton | NJ | Trenton Transit Center |  | [1](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)) [2](https://en.wikipedia.org/wiki/Hamilton_Avenue_station_(River_Line)) [3](https://en.wikipedia.org/wiki/Cass_Street_station) |
| Union | NJ | Union | Union CDP, Union Township, Union County | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Union_station_(NJ_Transit)) |
| Upper Montclair | NJ | Upper Montclair | Upper Montclair CDP, Montclair Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Upper_Montclair_station) |
| Waldwick | NJ | Waldwick |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Wayne | NJ | Mountain View–Wayne; Wayne Route 23 | Wayne Township (MCD); township name used per spec | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Mountain_View_station_(NJ_Transit)) [3](https://en.wikipedia.org/wiki/Wayne_Route_23_Transit_Center) |
| Westfield | NJ | Westfield |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Westwood | NJ | Westwood |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| White House Station | NJ | White House | White House Station CDP (commonly 'Whitehouse Station'), Readington Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/White_House_station) |
| Wood-Ridge | NJ | Wesmont; Wood-Ridge |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |
| Woodbridge | NJ | Woodbridge | Woodbridge CDP, Woodbridge Township | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) [2](https://en.wikipedia.org/wiki/Woodbridge_station_(NJ_Transit)) |
| Woodcliff Lake | NJ | Woodcliff Lake |  | [1](https://en.wikipedia.org/wiki/List_of_NJ_Transit_stations) |

##### Tier resolution where a place has more than one system

| Place | Systems present | Tier assigned |
|---|---|---|
| New York NY | NYC Subway + Staten Island Railway + PATH | subway |
| Newark NJ | PATH + Newark Light Rail + NJ Transit Rail | subway |
| Hoboken NJ | PATH + Hudson-Bergen Light Rail + NJ Transit Rail | subway |
| Jersey City NJ | PATH + Hudson-Bergen Light Rail | subway |
| Harrison NJ | PATH only | subway |
| Bloomfield NJ | Newark Light Rail + NJ Transit Montclair-Boonton | light rail |
| Trenton NJ | River LINE + NJ Transit Northeast Corridor | light rail |
| Pennsauken NJ | River LINE + NJ Transit Atlantic City Line | light rail |
| Camden NJ | River LINE (+ PATCO Speedline, another agent's scope) | light rail here; **should resolve to subway at merge** because PATCO is heavy rail |
| Lindenwold NJ | NJ Transit Atlantic City Line (+ PATCO Speedline terminus, another agent) | commuter rail here; **should resolve to subway at merge** |

#### Streetcar / borderline judgements

| System | Call | Why |
|---|---|---|
| River LINE (Camden-Trenton) | **light rail** | Diesel DMU "hybrid rail" on a fully exclusive former Pennsylvania/Camden & Amboy freight right-of-way, time-shared with freight only outside passenger hours: "Hybrid rail service in southern New Jersey" ([https://en.wikipedia.org/wiki/River_Line_(NJ_Transit)](https://en.wikipedia.org/wiki/River_Line_(NJ_Transit))). No mixed street running; 34 miles, 20 stations, station-spacing and ROW are rapid-transit-like, so it counts as light rail rather than a streetcar. |
| Newark Light Rail (City Subway) | **light rail** | Legacy 1935 streetcar subway, but "The original Newark City Subway line had its own right-of-way and did not share city streets with local traffic, except at the Orange Street grade crossing" ([https://en.wikipedia.org/wiki/Newark_Light_Rail](https://en.wikipedia.org/wiki/Newark_Light_Rail)). Runs in a tunnel through downtown Newark. Counts. Note the 2002 Belleville/Bloomfield extension is at-grade on a former Erie Railroad branch, still exclusive ROW, not street-running. |
| Hudson-Bergen Light Rail | **light rail** | Purpose-built LRT on former Conrail/waterfront freight ROW plus the Bergen Hill tunnel; some short street-median segments in Jersey City/Bayonne but the spine is exclusive. |
| Staten Island Railway | **subway** | Per the brief. Third-rail, high-platform, full grade separation, fare-integrated with the subway; it is inside New York City so it adds no place. |
| Princeton "Dinky" (Princeton Branch) | **commuter rail** | 2.7-mile NJ Transit electric shuttle, part of NJ Transit Rail Operations, listed in the NJ Transit station table. Not a streetcar. Adds Princeton and Princeton Junction. |
| NJ Transit Meadowlands service | **commuter rail, counted** | The Meadowlands station at East Rutherford is an active NJ Transit station in the "Active stations" table; the Meadowlands Rail Line runs event-day service only. Counted, but flagged: East Rutherford's only rail is event service. |

#### Deliberately excluded

| Thing | Why |
|---|---|
| Every New York State station on the Port Jervis Line (Port Jervis, Otisville, Middletown-Town of Wallkill, Campbell Hall, Salisbury Mills-Cornwall, Harriman, Tuxedo, Sloatsburg, Suffern) and the Pascack Valley Line north of the border (Spring Valley, Nanuet, Pearl River) | Out of scope by assignment - operated for Metro-North Railroad, owned by the Metro-North agent. The station table's "Operated by others" section lists all of them with NY locations. |
| Philadelphia PA (30th Street Station) | 30th Street is the western terminus of NJ Transit's Atlantic City Line, but Philadelphia is out of my assigned scope and is a SEPTA subway city; leaving it to the SEPTA agent to avoid a tier conflict. |
| Andover Township NJ (Andover station, Lackawanna Cut-Off Phase 1) | **Not open.** Article short description: "Planned NJ Transit Rail Station"; the restoration article says service "is expected to begin in 2026" / "projected to begin no earlier than 2026". |
| North Brunswick NJ (North Brunswick infill station, NEC) | Not open - opening listed as "TBA" in the Infill stations table. |
| All "Proposed expansion stations" (West Trenton Line, Lackawanna Cut-Off west of Andover incl. Analomink PA, Belle Mead, etc.) | Proposed only, no passenger service. |
| Edgewater Park Township NJ | Named in the "Beverly/Edgewater Park" station name but the station is not in it: "located on Railroad Avenue in Beverly, Burlington County, New Jersey" ([https://en.wikipedia.org/wiki/Beverly/Edgewater_Park_station](https://en.wikipedia.org/wiki/Beverly/Edgewater_Park_station)). |
| Hamilton Township, Mercer County (for the River LINE) | The River LINE's Hamilton Avenue station is **in Trenton**: "located on Hamilton Avenue in Trenton, New Jersey" ([https://en.wikipedia.org/wiki/Hamilton_Avenue_station_(River_Line)](https://en.wikipedia.org/wiki/Hamilton_Avenue_station_(River_Line))). Hamilton Township is still included, but for the NEC's separate Hamilton station. |
| Parsippany-Troy Hills NJ / Mount Tabor CDP | The Mount Tabor station is in Denville: "a New Jersey Transit station in Denville, New Jersey ... just west of the small community of Mount Tabor, New Jersey in Parsippany-Troy Hills" ([https://en.wikipedia.org/wiki/Mount_Tabor_station](https://en.wikipedia.org/wiki/Mount_Tabor_station)). Assigned to Denville, and Mount Tabor CDP not claimed. |
| Lyons CDP NJ | Lyons station's address is "4 Lyons Road, Basking Ridge, New Jersey 07059" and its lead says it is "in Basking Ridge" ([https://en.wikipedia.org/wiki/Lyons_station](https://en.wikipedia.org/wiki/Lyons_station)), so it was assigned to Basking Ridge CDP rather than the nearby Lyons CDP. |
| Watsessing CDP, Silver Lake CDP, Montclair State University CDP, Great Notch CDP | These are real Census CDPs sitting inside Bloomfield / Belleville / Little Falls, and stations of matching name exist, but no source I fetched places the station inside the **CDP boundary** (the station articles say only "in Bloomfield, New Jersey", "in Belleville, New Jersey", "the Great Notch area of Little Falls"). Assigned to the municipality instead rather than guess. |
| Kingsland station (Lyndhurst) | **Closed June 2025**, replaced by the new Lyndhurst station. Same municipality either way. |
| Newark AirTrain, PATH Newark Airport extension, HBLR Northern Branch / Route 440 / Secaucus extensions, Glassboro-Camden Line | People-mover or proposed/not open. |

#### 2025-2026 changes caught

- **Kingsland station (Lyndhurst Township, Main Line) closed June 8, 2025**, and a **new Lyndhurst station opened July 8, 2025**, replacing both Kingsland and the old 1918 Lyndhurst stop. Net effect on this dataset: none, both stops are in Lyndhurst Township. Source: List of NJ Transit stations, Former stations table, citing nj.com "This new NJ Transit Station Replaces 2 Old Stops, Including a 1918 'Relic'" (Apr 28, 2025).
- **NJ Transit took over River LINE operations from Alstom on September 3, 2025**; HBLR operations transitioned to ACI-Herzog JV by September 2025. Operator changes only, no station changes.
- **Andover (Lackawanna Cut-Off) still not open** as of the sources read - service "expected to begin in 2026". Excluded.
- MTA MetroCard sales ended December 31, 2025 (SIR/Subway); no station openings or closures.
- No new NYC Subway, Staten Island Railway, PATH, Newark Light Rail or HBLR stations opened or closed in 2025-2026 per the articles read.

#### Sourcing limitations

| Official site | Result | Fallback |
|---|---|---|
| `mta.info` (`/agency/staten-island-railway`, `/maps/subway`) | **HTTP 403** - blocks scripted fetches | Wikipedia NYC Subway + Staten Island Railway articles |
| `panynj.gov/path/en/schedules-maps.html` and `/stations.html` | HTTP 200 but a ~2.7 KB JavaScript shell; none of the station names (Newark, Harrison, Journal Square, Grove Street, Exchange Place, Newport, Hoboken, World Trade Center, 33rd) appear in the served HTML | Wikipedia PATH station list table (has State + City columns) |
| `njtransit.com/hudson-bergen-light-rail`, `/river-line`, `/newark-light-rail`, `/rail`, `/hudson-bergen-light-rail-to-from` | **HTTP 404** on every content slug (client-rendered SPA; the 404 body is a ~600 KB shell). `/stations` 302-redirects. `content.njtransit.com/.../rail-system-map.pdf` 404. | Wikipedia system + line + station articles |

Census place names were checked against the 2020 Census place-by-county file already in the
workspace (`place_by_county2020.txt`, 710 New Jersey rows). Important consequence: **New Jersey
townships are not Census "places"** - the file contains zero rows with "Township". Per the shared
spec ("If a station is in a NJ township with no village, use the town name (e.g. Cherry Hill)"),
township stations are recorded under the township name with "Township" stripped, and `cdp_notes`
says so. Where the station's own community is a verified Census CDP inside the township, the CDP
name is used instead (Iselin, Avenel, Woodbridge, Basking Ridge, Gillette, Millington, Stirling,
Annandale, Atco, Budd Lake, Landing, Towaco, Short Hills, White House Station, Princeton Junction,
Roebling, Upper Montclair, Cranford, Union).

One name to sanity-check downstream: **"Morris" NJ** (Convent Station, Morristown Line). The
municipality is Morris Township; there is no Morris CDP and Convent Station is an unincorporated
community, not a CDP, so the stripped township name is the only option the spec allows.

### 2.2 Long Island Rail Road, Metro-North, and Connecticut

**193 Census places** (NY 150, CT 42, MA 1). All `transit_type` = `commuter rail`.

#### Systems covered

| System | Type assigned | Source URL(s) | How station -> city was established |
|---|---|---|---|
| Long Island Rail Road (11 branches, 126 open passenger stations) | commuter rail | [List of Long Island Rail Road stations](https://en.wikipedia.org/wiki/List_of_Long_Island_Rail_Road_stations) + all 126 individual station articles | The LIRR station list carries only a County column, so each station's own article was fetched and its infobox `address` / lead sentence read (e.g. Cold Spring Harbor station: "located at West Pulaski Road (CR 11) and East Gate Drive ... in **West Hills**, Suffolk County"). Every station coordinate was then reverse-geocoded through the **US Census geocoder** (`geographies/coordinates`, benchmark Public_AR_Current, vintage Current_Current) to get the point-in-polygon incorporated place / CDP. Names were finally checked against the Census 2020 place-by-county list. |
| Metro-North Hudson Line | commuter rail | [Hudson Line (Metro-North)](https://en.wikipedia.org/wiki/Hudson_Line_(Metro-North)) + station articles | The line article's station table has a **Location** column; each was cross-checked against the station article lead and a Census reverse-geocode of the station coordinate. |
| Metro-North Harlem Line | commuter rail | [Harlem Line](https://en.wikipedia.org/wiki/Harlem_Line) + station articles | Same method (Location column + station article + Census reverse-geocode). |
| Metro-North New Haven Line | commuter rail | [New Haven Line](https://en.wikipedia.org/wiki/New_Haven_Line) + station articles | Same method. The table also carries a State column, which separates the NY and CT halves. |
| Metro-North New Canaan Branch | commuter rail | [New Canaan Branch](https://en.wikipedia.org/wiki/New_Canaan_Branch) | Same method. |
| Metro-North Danbury Branch | commuter rail | [Danbury Branch](https://en.wikipedia.org/wiki/Danbury_Branch) | Same method. |
| Metro-North Waterbury Branch | commuter rail | [Waterbury Branch](https://en.wikipedia.org/wiki/Waterbury_Branch) | Same method. |
| Metro-North Port Jervis Line (west of Hudson; MTA/Metro-North territory, trains operated by NJ Transit under contract) | commuter rail | [Port Jervis Line](https://en.wikipedia.org/wiki/Port_Jervis_Line) + station articles | Same method. All **New York** stations owned here per the task split; NJ stations (Hoboken, Secaucus, Mahwah) left to the NJ agent. |
| Metro-North Pascack Valley Line (NY portion) | commuter rail | [Pascack Valley Line](https://en.wikipedia.org/wiki/Pascack_Valley_Line) + station articles | Same method. NY stations only: Pearl River, Nanuet, Spring Valley. |
| Shore Line East (CTrail) | commuter rail | [Shore Line East](https://en.wikipedia.org/wiki/Shore_Line_East) + <https://shorelineeast.com/> (official, **served HTTP 200**) | Wikipedia station table has a Location column; the official site's station list corroborated all 14 stops. |
| CTrail Hartford Line | commuter rail | [Hartford Line](https://en.wikipedia.org/wiki/Hartford_Line) + station articles | Wikipedia station table; open stations distinguished from planned ones by the grey `bgcolor=dfdfdf` / italic "Future station" rows. |

#### Place-by-place

##### Long Island Rail Road

| Place | State | Station(s) | Source URL |
|---|---|---|---|
| New York | NY | Penn Station, Grand Central Madison, Jamaica, Woodside, Long Island City, Hunterspoint Avenue, Forest Hills, Kew Gardens, Flushing-Main Street, Mets-Willets Point, Murray Hill, Broadway, Auburndale, Bayside, Douglaston, Little Neck, Hollis, Queens Village, Belmont Park, St. Albans, Locust Manor, Laurelton, Rosedale, Far Rockaway, Atlantic Terminal, Nostrand Avenue, East New York (+ Metro-North Harlem/Hudson/New Haven Bronx stations) | https://en.wikipedia.org/wiki/Grand_Central_Madison |
| Albertson | NY | Albertson | https://en.wikipedia.org/wiki/Albertson_station |
| Baldwin | NY | Baldwin | https://en.wikipedia.org/wiki/Baldwin_station_(LIRR) |
| Bellerose | NY | Bellerose | https://en.wikipedia.org/wiki/Bellerose_station |
| Bellerose Terrace | NY | Elmont-UBS Arena | https://en.wikipedia.org/wiki/Elmont%E2%80%93UBS_Arena_station |
| Bellmore | NY | Bellmore | https://en.wikipedia.org/wiki/Bellmore_station |
| Bethpage | NY | Bethpage | https://en.wikipedia.org/wiki/Bethpage_station |
| Carle Place | NY | Carle Place | https://en.wikipedia.org/wiki/Carle_Place_station |
| Cedarhurst | NY | Cedarhurst | https://en.wikipedia.org/wiki/Cedarhurst_station |
| East Rockaway | NY | East Rockaway, Centre Avenue | https://en.wikipedia.org/wiki/East_Rockaway_station |
| East Williston | NY | East Williston | https://en.wikipedia.org/wiki/East_Williston_station |
| Elmont | NY | Elmont-UBS Arena | https://en.wikipedia.org/wiki/Elmont%E2%80%93UBS_Arena_station |
| Farmingdale | NY | Farmingdale | https://en.wikipedia.org/wiki/Farmingdale_station |
| Floral Park | NY | Floral Park, Bellerose | https://en.wikipedia.org/wiki/Floral_Park_station |
| Freeport | NY | Freeport | https://en.wikipedia.org/wiki/Freeport_station_(LIRR) |
| Garden City | NY | Garden City, Country Life Press, Nassau Boulevard, Merillon Avenue, Stewart Manor | https://en.wikipedia.org/wiki/Garden_City_station_(LIRR) |
| Garden City Park | NY | Merillon Avenue | https://en.wikipedia.org/wiki/Merillon_Avenue_station |
| Glen Cove | NY | Glen Cove, Glen Street, Sea Cliff | https://en.wikipedia.org/wiki/Glen_Cove_station |
| Glen Head | NY | Glen Head | https://en.wikipedia.org/wiki/Glen_Head_station |
| Great Neck Plaza | NY | Great Neck | https://en.wikipedia.org/wiki/Great_Neck_station |
| Hempstead | NY | Hempstead | https://en.wikipedia.org/wiki/Hempstead_station_(LIRR) |
| Hewlett | NY | Hewlett | https://en.wikipedia.org/wiki/Hewlett_station |
| Hicksville | NY | Hicksville | https://en.wikipedia.org/wiki/Hicksville_station |
| Inwood | NY | Inwood | https://en.wikipedia.org/wiki/Inwood_station_(LIRR) |
| Island Park | NY | Island Park | https://en.wikipedia.org/wiki/Island_Park_station |
| Lawrence | NY | Lawrence | https://en.wikipedia.org/wiki/Lawrence_station_(LIRR) |
| Locust Valley | NY | Locust Valley | https://en.wikipedia.org/wiki/Locust_Valley_station |
| Long Beach | NY | Long Beach | https://en.wikipedia.org/wiki/Long_Beach_station_(LIRR) |
| Lynbrook | NY | Lynbrook | https://en.wikipedia.org/wiki/Lynbrook_station |
| Malverne | NY | Malverne, Westwood | https://en.wikipedia.org/wiki/Malverne_station |
| Manhasset | NY | Manhasset | https://en.wikipedia.org/wiki/Manhasset_station |
| Massapequa | NY | Massapequa | https://en.wikipedia.org/wiki/Massapequa_station |
| Massapequa Park | NY | Massapequa Park | https://en.wikipedia.org/wiki/Massapequa_Park_station |
| Merrick | NY | Merrick | https://en.wikipedia.org/wiki/Merrick_station |
| Mineola | NY | Mineola | https://en.wikipedia.org/wiki/Mineola_station_(LIRR) |
| New Hyde Park | NY | New Hyde Park | https://en.wikipedia.org/wiki/New_Hyde_Park_station |
| Oceanside | NY | Oceanside | https://en.wikipedia.org/wiki/Oceanside_station_(LIRR) |
| Oyster Bay | NY | Oyster Bay | https://en.wikipedia.org/wiki/Oyster_Bay_station |
| Plandome | NY | Plandome | https://en.wikipedia.org/wiki/Plandome_station |
| Port Washington | NY | Port Washington | https://en.wikipedia.org/wiki/Port_Washington_station |
| Rockville Centre | NY | Rockville Centre | https://en.wikipedia.org/wiki/Rockville_Centre_station |
| Roslyn Harbor | NY | Greenvale | https://en.wikipedia.org/wiki/Greenvale_station |
| Roslyn Heights | NY | Roslyn | https://en.wikipedia.org/wiki/Roslyn_station_(LIRR) |
| Seaford | NY | Seaford | https://en.wikipedia.org/wiki/Seaford_(LIRR_station) |
| Syosset | NY | Syosset | https://en.wikipedia.org/wiki/Syosset_station |
| Valley Stream | NY | Valley Stream, Gibson | https://en.wikipedia.org/wiki/Valley_Stream_station |
| Wantagh | NY | Wantagh | https://en.wikipedia.org/wiki/Wantagh_station |
| Westbury | NY | Westbury | https://en.wikipedia.org/wiki/Westbury_station_(LIRR) |
| West Hempstead | NY | West Hempstead, Hempstead Gardens, Lakeview | https://en.wikipedia.org/wiki/West_Hempstead_station |
| Williston Park | NY | East Williston | https://en.wikipedia.org/wiki/East_Williston_station |
| Woodmere | NY | Woodmere | https://en.wikipedia.org/wiki/Woodmere_station |
| Amagansett | NY | Amagansett | https://en.wikipedia.org/wiki/Amagansett_station |
| Amityville | NY | Amityville | https://en.wikipedia.org/wiki/Amityville_station |
| Babylon | NY | Babylon | https://en.wikipedia.org/wiki/Babylon_station |
| Bay Shore | NY | Bay Shore | https://en.wikipedia.org/wiki/Bay_Shore_station |
| Baywood | NY | Deer Park | https://en.wikipedia.org/wiki/Deer_Park_station_(LIRR) |
| Brentwood | NY | Brentwood | https://en.wikipedia.org/wiki/Brentwood_station_(LIRR) |
| Bridgehampton | NY | Bridgehampton | https://en.wikipedia.org/wiki/Bridgehampton_station |
| Central Islip | NY | Central Islip | https://en.wikipedia.org/wiki/Central_Islip_station |
| Copiague | NY | Copiague | https://en.wikipedia.org/wiki/Copiague_station |
| East Farmingdale | NY | Pinelawn | https://en.wikipedia.org/wiki/Pinelawn_station |
| East Hampton | NY | East Hampton | https://en.wikipedia.org/wiki/East_Hampton_station |
| East Islip | NY | Great River | https://en.wikipedia.org/wiki/Great_River_station |
| East Northport | NY | Northport | https://en.wikipedia.org/wiki/Northport_station |
| Greenlawn | NY | Greenlawn | https://en.wikipedia.org/wiki/Greenlawn_station |
| Greenport | NY | Greenport | https://en.wikipedia.org/wiki/Greenport_station_(LIRR) |
| Hampton Bays | NY | Hampton Bays | https://en.wikipedia.org/wiki/Hampton_Bays_station |
| Huntington Station | NY | Huntington | https://en.wikipedia.org/wiki/Huntington_station_(LIRR) |
| Islip | NY | Islip | https://en.wikipedia.org/wiki/Islip_station_(LIRR) |
| Kings Park | NY | Kings Park | https://en.wikipedia.org/wiki/Kings_Park_station_(LIRR) |
| Lindenhurst | NY | Lindenhurst | https://en.wikipedia.org/wiki/Lindenhurst_station_(LIRR) |
| Manorville | NY | Yaphank-BNL (opened Jul 17 2026) | https://en.wikipedia.org/wiki/Yaphank%E2%80%93BNL_station |
| Mattituck | NY | Mattituck | https://en.wikipedia.org/wiki/Mattituck_station |
| Medford | NY | Medford | https://en.wikipedia.org/wiki/Medford_station |
| Montauk | NY | Montauk | https://en.wikipedia.org/wiki/Montauk_station |
| North Bellport | NY | Bellport | https://en.wikipedia.org/wiki/Bellport_station |
| Oakdale | NY | Oakdale | https://en.wikipedia.org/wiki/Oakdale_station |
| Patchogue | NY | Patchogue | https://en.wikipedia.org/wiki/Patchogue_station |
| Port Jefferson | NY | Port Jefferson | https://en.wikipedia.org/wiki/Port_Jefferson_station_(LIRR) |
| Port Jefferson Station | NY | Port Jefferson | https://en.wikipedia.org/wiki/Port_Jefferson_station_(LIRR) |
| Remsenburg-Speonk | NY | Speonk | https://en.wikipedia.org/wiki/Speonk_station |
| Riverhead | NY | Riverhead | https://en.wikipedia.org/wiki/Riverhead_station |
| Ronkonkoma | NY | Ronkonkoma | https://en.wikipedia.org/wiki/Ronkonkoma_station |
| St. James | NY | St. James | https://en.wikipedia.org/wiki/St._James_station_(LIRR) |
| Sayville | NY | Sayville | https://en.wikipedia.org/wiki/Sayville_station |
| Shirley | NY | Mastic-Shirley | https://en.wikipedia.org/wiki/Mastic%E2%80%93Shirley_station |
| Smithtown | NY | Smithtown | https://en.wikipedia.org/wiki/Smithtown_station |
| Southampton | NY | Southampton | https://en.wikipedia.org/wiki/Southampton_station_(LIRR) |
| Southold | NY | Southold | https://en.wikipedia.org/wiki/Southold_station |
| Stony Brook | NY | Stony Brook | https://en.wikipedia.org/wiki/Stony_Brook_station_(LIRR) |
| West Hills | NY | Cold Spring Harbor | https://en.wikipedia.org/wiki/Cold_Spring_Harbor_station |
| Westhampton Beach | NY | Westhampton | https://en.wikipedia.org/wiki/Westhampton_station |
| Wyandanch | NY | Wyandanch | https://en.wikipedia.org/wiki/Wyandanch_station |

##### Metro-North Railroad

| Place | State | Station(s) | Source URL |
|---|---|---|---|
| Yonkers | NY | Yonkers, Ludlow, Glenwood, Greystone (Hudson) | https://en.wikipedia.org/wiki/Yonkers_station |
| Hastings-on-Hudson | NY | Hastings-on-Hudson (Hudson) | https://en.wikipedia.org/wiki/Hastings-on-Hudson_station |
| Dobbs Ferry | NY | Dobbs Ferry (Hudson) | https://en.wikipedia.org/wiki/Dobbs_Ferry_station |
| Irvington | NY | Irvington, Ardsley-on-Hudson (Hudson) | https://en.wikipedia.org/wiki/Irvington_station_(Metro-North) |
| Tarrytown | NY | Tarrytown (Hudson) | https://en.wikipedia.org/wiki/Tarrytown_station |
| Sleepy Hollow | NY | Philipse Manor (Hudson) | https://en.wikipedia.org/wiki/Philipse_Manor_station |
| Briarcliff Manor | NY | Scarborough (Hudson) | https://en.wikipedia.org/wiki/Scarborough_station_(Metro-North) |
| Ossining | NY | Ossining (Hudson) | https://en.wikipedia.org/wiki/Ossining_station |
| Croton-on-Hudson | NY | Croton-Harmon (Hudson) | https://en.wikipedia.org/wiki/Croton%E2%80%93Harmon_station |
| Montrose | NY | Cortlandt (Hudson) | https://en.wikipedia.org/wiki/Cortlandt_station |
| Peekskill | NY | Peekskill (Hudson) | https://en.wikipedia.org/wiki/Peekskill_station |
| Philipstown | NY | Garrison, Manitou (Hudson) | https://en.wikipedia.org/wiki/Garrison_station_(Metro-North) |
| Cold Spring | NY | Cold Spring (Hudson) | https://en.wikipedia.org/wiki/Cold_Spring_station_(Metro-North) |
| Beacon | NY | Beacon (Hudson) | https://en.wikipedia.org/wiki/Beacon_station_(Metro-North) |
| New Hamburg | NY | New Hamburg (Hudson) | https://en.wikipedia.org/wiki/New_Hamburg_station |
| Poughkeepsie | NY | Poughkeepsie (Hudson terminal) | https://en.wikipedia.org/wiki/Poughkeepsie_station |
| Mount Vernon | NY | Mount Vernon West, Fleetwood (Harlem); Mount Vernon East (New Haven) | https://en.wikipedia.org/wiki/Mount_Vernon_East_station |
| Bronxville | NY | Bronxville (Harlem) | https://en.wikipedia.org/wiki/Bronxville_station |
| Tuckahoe | NY | Tuckahoe, Crestwood (Harlem) | https://en.wikipedia.org/wiki/Tuckahoe_station_(Metro-North) |
| Scarsdale | NY | Scarsdale (Harlem) | https://en.wikipedia.org/wiki/Scarsdale_station |
| Hartsdale | NY | Hartsdale (Harlem) | https://en.wikipedia.org/wiki/Hartsdale_station |
| White Plains | NY | White Plains, North White Plains (Harlem) | https://en.wikipedia.org/wiki/White_Plains_station |
| Valhalla | NY | Valhalla (Harlem) | https://en.wikipedia.org/wiki/Valhalla_station |
| Hawthorne | NY | Hawthorne (Harlem) | https://en.wikipedia.org/wiki/Hawthorne_station_(Metro-North) |
| Pleasantville | NY | Pleasantville (Harlem) | https://en.wikipedia.org/wiki/Pleasantville_station_(Metro-North) |
| Chappaqua | NY | Chappaqua (Harlem) | https://en.wikipedia.org/wiki/Chappaqua_station |
| Mount Kisco | NY | Mount Kisco (Harlem) | https://en.wikipedia.org/wiki/Mount_Kisco_station |
| Bedford Hills | NY | Bedford Hills (Harlem) | https://en.wikipedia.org/wiki/Bedford_Hills_station |
| Katonah | NY | Katonah (Harlem) | https://en.wikipedia.org/wiki/Katonah_station |
| Golden's Bridge | NY | Goldens Bridge (Harlem) | https://en.wikipedia.org/wiki/Goldens_Bridge_station |
| North Salem | NY | Purdy's, Croton Falls (Harlem) | https://en.wikipedia.org/wiki/Croton_Falls_station |
| Brewster | NY | Brewster (Harlem) | https://en.wikipedia.org/wiki/Brewster_station_(Metro-North) |
| Southeast | NY | Southeast (Harlem) | https://en.wikipedia.org/wiki/Southeast_station |
| Patterson | NY | Patterson (Harlem) | https://en.wikipedia.org/wiki/Patterson_station_(Metro-North) |
| Pawling | NY | Pawling (Harlem); Appalachian Trail flag stop is elsewhere in Pawling town | https://en.wikipedia.org/wiki/Pawling_station |
| Wingdale | NY | Harlem Valley-Wingdale (Harlem) | https://en.wikipedia.org/wiki/Harlem_Valley%E2%80%93Wingdale_station |
| Dover Plains | NY | Dover Plains (Harlem) | https://en.wikipedia.org/wiki/Dover_Plains_station |
| Amenia | NY | Wassaic (Harlem terminal), Tenmile River | https://en.wikipedia.org/wiki/Wassaic_station |
| Pelham | NY | Pelham (New Haven) | https://en.wikipedia.org/wiki/Pelham_station_(Metro-North) |
| New Rochelle | NY | New Rochelle (New Haven) | https://en.wikipedia.org/wiki/New_Rochelle_station |
| Larchmont | NY | Larchmont (New Haven) | https://en.wikipedia.org/wiki/Larchmont_station |
| Mamaroneck | NY | Mamaroneck (New Haven) | https://en.wikipedia.org/wiki/Mamaroneck_station |
| Harrison | NY | Harrison (New Haven) | https://en.wikipedia.org/wiki/Harrison_station_(Metro-North) |
| Rye | NY | Rye (New Haven) | https://en.wikipedia.org/wiki/Rye_station_(Metro-North) |
| Port Chester | NY | Port Chester (New Haven) | https://en.wikipedia.org/wiki/Port_Chester_station |
| Suffern | NY | Suffern (Port Jervis) | https://en.wikipedia.org/wiki/Suffern_station |
| Sloatsburg | NY | Sloatsburg (Port Jervis) | https://en.wikipedia.org/wiki/Sloatsburg_station |
| Tuxedo | NY | Tuxedo (Port Jervis) | https://en.wikipedia.org/wiki/Tuxedo_station |
| Woodbury | NY | Harriman (Port Jervis) | https://en.wikipedia.org/wiki/Harriman_station |
| Beaver Dam Lake | NY | Salisbury Mills-Cornwall (Port Jervis) | https://en.wikipedia.org/wiki/Salisbury_Mills%E2%80%93Cornwall_station |
| Hamptonburgh | NY | Campbell Hall (Port Jervis) | https://en.wikipedia.org/wiki/Campbell_Hall_station |
| Scotchtown | NY | Middletown-Town of Wallkill (Port Jervis) | https://en.wikipedia.org/wiki/Middletown%E2%80%93Town_of_Wallkill_station |
| Mount Hope | NY | Otisville (Port Jervis) | https://en.wikipedia.org/wiki/Otisville_station |
| Port Jervis | NY | Port Jervis (Port Jervis terminal) | https://en.wikipedia.org/wiki/Port_Jervis_station |
| Pearl River | NY | Pearl River (Pascack Valley) | https://en.wikipedia.org/wiki/Pearl_River_station |
| Nanuet | NY | Nanuet (Pascack Valley) | https://en.wikipedia.org/wiki/Nanuet_station |
| Spring Valley | NY | Spring Valley (Pascack Valley terminal) | https://en.wikipedia.org/wiki/Spring_Valley_station_(New_York) |
| Greenwich | CT | Greenwich (New Haven, New Canaan Br) | https://en.wikipedia.org/wiki/Greenwich_station_(Connecticut) |
| Cos Cob | CT | Cos Cob (New Haven) | https://en.wikipedia.org/wiki/Cos_Cob_station |
| Riverside | CT | Riverside (New Haven) | https://en.wikipedia.org/wiki/Riverside_station_(Connecticut) |
| Old Greenwich | CT | Old Greenwich (New Haven) | https://en.wikipedia.org/wiki/Old_Greenwich_station |
| Stamford | CT | Stamford Transportation Center; Glenbrook, Springdale (New Canaan Br) | https://en.wikipedia.org/wiki/Stamford_Transportation_Center |
| Noroton Heights | CT | Noroton Heights (New Haven, Danbury Br) | https://en.wikipedia.org/wiki/Noroton_Heights_station |
| Darien | CT | Darien (New Haven, Danbury Br) | https://en.wikipedia.org/wiki/Darien_station |
| Norwalk | CT | South Norwalk, East Norwalk, Rowayton (New Haven); Merritt 7 (Danbury Br) | https://en.wikipedia.org/wiki/South_Norwalk_station |
| Westport | CT | Westport (New Haven) | https://en.wikipedia.org/wiki/Westport_station_(Metro-North) |
| Greens Farms | CT | Green's Farms (New Haven) | https://en.wikipedia.org/wiki/Greens_Farms_station |
| Southport | CT | Southport (New Haven) | https://en.wikipedia.org/wiki/Southport_station_(Metro-North) |
| Fairfield | CT | Fairfield, Fairfield-Black Rock (New Haven) | https://en.wikipedia.org/wiki/Fairfield_station_(Connecticut) |
| Bridgeport | CT | Bridgeport (New Haven, Waterbury Br, Shore Line East) | https://en.wikipedia.org/wiki/Bridgeport_station_(Connecticut) |
| Stratford | CT | Stratford (New Haven, Waterbury Br, Shore Line East) | https://en.wikipedia.org/wiki/Stratford_station_(Metro-North) |
| Milford | CT | Milford (New Haven, Shore Line East) | https://en.wikipedia.org/wiki/Milford_station_(Connecticut) |
| West Haven | CT | West Haven (New Haven, Shore Line East) | https://en.wikipedia.org/wiki/West_Haven_station |
| New Haven | CT | Union Station, State Street (New Haven Line, Shore Line East, Hartford Line) | https://en.wikipedia.org/wiki/Union_Station_(New_Haven) |
| New Canaan | CT | New Canaan (terminal), Talmadge Hill (New Canaan Br) | https://en.wikipedia.org/wiki/New_Canaan_station |
| Wilton | CT | Wilton (Danbury Br) | https://en.wikipedia.org/wiki/Wilton_station_(Metro-North) |
| Cannondale | CT | Cannondale (Danbury Br) | https://en.wikipedia.org/wiki/Cannondale_station |
| Branchville | CT | Branchville (Danbury Br) | https://en.wikipedia.org/wiki/Branchville_station |
| Bethel | CT | Bethel (Danbury Br) | https://en.wikipedia.org/wiki/Bethel_station_(Connecticut) |
| Danbury | CT | Danbury (Danbury Br terminal) | https://en.wikipedia.org/wiki/Danbury_station |
| Waterbury | CT | Waterbury (Waterbury Br terminal) | https://en.wikipedia.org/wiki/Waterbury_station_(Metro-North) |
| Naugatuck | CT | Naugatuck (Waterbury Br) | https://en.wikipedia.org/wiki/Naugatuck_station |
| Beacon Falls | CT | Beacon Falls (Waterbury Br) | https://en.wikipedia.org/wiki/Beacon_Falls_station |
| Seymour | CT | Seymour (Waterbury Br) | https://en.wikipedia.org/wiki/Seymour_station_(Connecticut) |
| Ansonia | CT | Ansonia (Waterbury Br) | https://en.wikipedia.org/wiki/Ansonia_station |
| Derby | CT | Derby-Shelton (Waterbury Br) | https://en.wikipedia.org/wiki/Derby%E2%80%93Shelton_station |

##### Shore Line East

| Place | State | Station(s) | Source URL |
|---|---|---|---|
| Branford | CT | Branford | https://en.wikipedia.org/wiki/Branford_station |
| Guilford | CT | Guilford | https://en.wikipedia.org/wiki/Guilford_station |
| Madison | CT | Madison | https://en.wikipedia.org/wiki/Madison_station_(Connecticut) |
| Clinton | CT | Clinton | https://en.wikipedia.org/wiki/Clinton_station_(Connecticut) |
| Westbrook | CT | Westbrook | https://en.wikipedia.org/wiki/Westbrook_station_(Connecticut) |
| Old Saybrook | CT | Old Saybrook | https://en.wikipedia.org/wiki/Old_Saybrook_station |
| New London | CT | New London Union Station (eastern terminal) | https://en.wikipedia.org/wiki/New_London_Union_Station |

##### CTrail Hartford Line

| Place | State | Station(s) | Source URL |
|---|---|---|---|
| Wallingford | CT | Wallingford | https://en.wikipedia.org/wiki/Wallingford_station_(Connecticut) |
| Meriden | CT | Meriden | https://en.wikipedia.org/wiki/Meriden_station |
| Berlin | CT | Berlin | https://en.wikipedia.org/wiki/Berlin_station_(Connecticut) |
| Hartford | CT | Hartford Union Station | https://en.wikipedia.org/wiki/Hartford_Union_Station |
| Windsor | CT | Windsor | https://en.wikipedia.org/wiki/Windsor_station_(Connecticut) |
| Windsor Locks | CT | Windsor Locks | https://en.wikipedia.org/wiki/Windsor_Locks_station |
| Springfield | MA | Springfield Union Station (northern terminal) | https://en.wikipedia.org/wiki/Springfield_Union_Station_(Massachusetts) |

##### Quotes for the non-obvious assignments

- **Cold Spring Harbor station -> **West Hills** CDP** - "It is located at West Pulaski Road (CR 11) and East Gate Drive, just south of Woodbury Road in West Hills, Suffolk County, New York."
- **Deer Park station -> **Baywood** CDP** - "It is located at Pineaire Drive, Executive (formerly Grant) Avenue, and Long Island Avenue in Baywood, New York."
- **Northport station -> **East Northport** CDP** - Infobox address: "Larkfield Road and Bellerose Avenue, East Northport, New York".
- **Bellport station -> **North Bellport** CDP** - "located at Bellport Station Road and Montauk Highway in North Bellport, Suffolk County".
- **Great River station -> **East Islip** CDP** - "a railroad station on the Montauk Branch ... at Connetquot Avenue and Hawthorne Avenue in East Islip, New York."
- **Stewart Manor station -> **Garden City** village** - "Contrary to its name, the station is not within the village of Stewart Manor - the west end of the station is one block east of its boundary with Garden City."
- **Sea Cliff station -> **Glen Cove** city** - "It is located on Sea Cliff Avenue and Glen Keith Road ... in the City of Glen Cove, in Nassau County."
- **Roslyn station -> **Roslyn Heights** CDP** - "It is located Station Plaza at Lincoln and Railroad Avenues ... in Roslyn Heights, Nassau County."
- **Greenvale station -> **Roslyn Harbor** village** - "The station is located off Helen Street ... within the Village of Roslyn Harbor."
- **Great Neck station -> **Great Neck Plaza** village** - "a station on the Long Island Rail Road's Port Washington Branch in the Village of Great Neck Plaza."
- **Bellerose station -> **Bellerose** + **Floral Park** villages** - "located in the incorporated villages of Bellerose and Floral Park, in Nassau County."
- **East Williston station -> **East Williston** + **Williston Park** villages** - "located at Hillside Avenue (NY 25B) and Pennsylvania Avenue on the border between East Williston and Williston Park."
- **Merillon Avenue station -> **Garden City Park** + **Garden City**** - "It is located at Nassau Boulevard and Merillon Avenue in Garden City Park and Garden City, in Nassau County."
- **Elmont-UBS Arena station -> **Elmont** + **Bellerose Terrace**** - "a station along the Main Line of the Long Island Rail Road (LIRR) in Elmont and Bellerose Terrace, New York."
- **Port Jefferson station -> **Port Jefferson** village + **Port Jefferson Station** CDP** - Port Jefferson Station article: "The Long Island Rail Road station is on the hamlet's northern border with the Incorporated Village of Port Jefferson."
- **Yaphank-BNL station -> **Manorville** CDP** - Article: "located in East Yaphank, New York" (not a Census place); mailing address 201 Precision Drive, Shirley NY. Census reverse-geocode of 40.849303/-72.864516 returns **Manorville CDP, Brookhaven town**.
- **Scarborough station -> **Briarcliff Manor** village** - "located in the Scarborough area of Briarcliff Manor, New York." (Census point-in-polygon of the article's coordinate returns Ossining village - the two adjoin.)
- **Cortlandt station -> **Montrose** CDP** - Census reverse-geocode of 41.247/-73.9232 = Montrose CDP, Cortlandt town.
- **Harriman station -> **Woodbury** village (Orange County)** - "an active commuter railroad station in the town of Woodbury, Orange County, New York. Located on State Route 17 south of the eponymous hamlet" (i.e. south of Harriman).
- **Salisbury Mills-Cornwall station -> **Beaver Dam Lake** CDP** - "a commuter railroad station in the Beaver Dam Lake section of the town of Cornwall, Orange County."
- **Middletown-Town of Wallkill station -> **Scotchtown** CDP** - Census reverse-geocode returns Scotchtown CDP, Wallkill town - the station is outside the City of Middletown, as its name says.
- **Otisville station -> town of **Mount Hope**** - "a commuter railroad station in the town of Mount Hope, Orange County. Located on Kelly Hill Road" - outside Otisville village.
- **Tuxedo station -> **Tuxedo** village** - "an active commuter railroad station in the town of Tuxedo, Orange County." Tuxedo, New York: "The village was incorporated in 2021 and comprises all of the town that is not part of the village of Tuxedo Park." Census current place layer GEOID 3675779.
- **Westport station -> town of **Westport**** - Census point-in-polygon returns Saugatuck CDP, which is a neighbourhood of the town of Westport; the town name is used per the CT rule.
- **Berlin station -> town of **Berlin**** - Census point-in-polygon returns Kensington CDP, the village inside the town of Berlin where the station stands.

#### Streetcar / borderline judgements

| System / thing | Call | Why |
|---|---|---|
| Metro-North **Port Jervis Line** and **Pascack Valley Line** | **INCLUDED as commuter rail** (NY stations only) | These are Metro-North (MTA) services west of the Hudson; NJ Transit operates the trains under contract. They are conventional heavy commuter rail, not streetcar. Per the task split the NJ agent skips all NY stations, so every NY station on both lines is here. |
| **Shore Line East** | commuter rail | Peak-oriented CTDOT commuter service on the Northeast Corridor, New Haven to New London. Not Amtrak-only: it is a separate branded commuter operation with its own fares/timetable, confirmed on the official site. |
| **CTrail Hartford Line** | commuter rail | CTDOT-branded commuter service, New Haven to Springfield, launched Jun 16 2018, operated by TransitAmerica/Alternate Concepts. Amtrak trains are cross-honoured but the CTrail trains are their own commuter operation. Not counted as "Amtrak-only". |
| LIRR / Metro-North **subway-like segments** | still commuter rail | Even the electrified third-rail inner zones (Grand Central to Croton-Harmon, Penn to Jamaica) are branded and fared as commuter rail, so `transit_type` stays `commuter rail`. New York NY separately has the NYC Subway, which is a higher tier and should win in the merge. |
| Streetcar / light-rail systems | none in scope | No streetcar, trolley, people-mover or funicular falls inside this batch, so no streetcar call was needed. |

#### Deliberately excluded

| Thing | Why |
|---|---|
| **Yaphank** CDP, NY (Yaphank station) | **2026 change.** Yaphank station "was a station in Yaphank, New York ... from 1845 to 2026. ... It was replaced by the new Yaphank-BNL station 3.5 mi to the east in 2026." The old station is closed, so Yaphank CDP no longer has an open station and is left out. |
| **Breakneck Ridge** station (Fishkill town, NY) | "a **temporarily closed** rail station on the Metro-North Hudson Line." Not currently serving passengers. Fishkill town has no Census place at the point anyway. |
| LIRR **Hillside Facility** and **Morris Park Facility / Boland's Landing** | Employee-only stops, not public passenger stations: "Not included in this count are two additional stations that serve employees of the LIRR." Both are in Queens -> New York NY, already included. |
| CTrail **Enfield** station | Not open. Table: *2027 (planned)*. |
| CTrail **West Hartford**, **Newington**, **North Haven** stations | Not open. Table: *Future station*. |
| Metro-North **Wall Street** (Norwalk), **Kent Road** (Wilton), **Georgetown** (Wilton), **Sanford** (Redding) - Danbury Branch | All greyed out as closed in the Danbury Branch table. Kent Road: "Metro-North ceased stops at Kent Road on January 16, 1994." Wall Street closed 1956; a 2022 CTDOT study concluded against reopening. Redding CT therefore gets **no** entry. |
| Metro-North **Springdale Cemetery** and **Woodway** - New Canaan Branch | Greyed out as closed. |
| LIRR/Metro-North stations in **NYC boroughs** as separate places | Boroughs are not Census places - all collapse to the single "New York", NY row. |
| **Ridgefield** CT as a separate name | Branchville station is in the Branchville CDP inside the town of Ridgefield; Branchville is the Census place used. The Ridgefield CDP (town centre) has no station. |
| **Redding** CT, **Weston** CT, **Trumbull** CT, **Shelton** CT | No open station inside these towns. Derby-Shelton station is on the Derby side of the Housatonic. |
| **Mount Pleasant** town, NY as a separate name | The Mount Pleasant station point falls in no CDP, but the town is already represented by Valhalla, Hawthorne, Pleasantville and Sleepy Hollow, all included. Adding the town would double-count. |
| **Pawling** town, NY as a separate name (Appalachian Trail flag stop) | Pawling village is already included from Pawling station; the Appalachian Trail stop is elsewhere in the same town. |
| **Westhampton** CDP, NY | The Westhampton station coordinate reverse-geocodes into **Westhampton Beach village**, which is what was used. Westhampton CDP could not be confirmed to contain the station, so it was not added. |
| **Stony Brook University** CDP, NY | The Stony Brook station coordinate point-in-polygons into Stony Brook University CDP, but the article says "located in Stony Brook, New York, adjacent to the campus" - **Stony Brook** CDP was used and the campus CDP dropped rather than listing both. |
| **Otisville** village, **Harriman** village, NY | Both are real Census places named after their stations, but both stations sit **outside** the village lines (town of Mount Hope and town/village of Woodbury respectively), per the station articles. Not added. |
| NJ stations on the Port Jervis / Pascack Valley lines (Hoboken, Secaucus, Mahwah, and the whole NJ portion) | Out of scope - assigned to the NJ agent. |

##### Places written as a TOWN name, not a Census place (flagged, caller may want to drop or remap)

The shared spec allows a NY/New England **town** name where the station sits in a town with no village, and the task note says to use CT town names. These 21 rows are therefore town (county-subdivision) names, not names in the Census 2020 place file. Every one carries a `cdp_notes` saying so.

| Place | State | Why it is a town name | Census place actually containing the station point |
|---|---|---|---|
| Philipstown | NY | Garrison + Manitou stations, no CDP at either point | none |
| North Salem | NY | Purdy's + Croton Falls stations, no CDP at either point | none |
| Southeast | NY | Southeast station, outside Brewster village | none |
| Patterson | NY | Patterson station, no CDP at the point | none |
| Amenia | NY | Wassaic + Tenmile River stations | point falls outside both Wassaic CDP and Amenia CDP |
| Hamptonburgh | NY | Campbell Hall station, no CDP at the point | none |
| Mount Hope | NY | Otisville station, outside Otisville village | none |
| Darien | CT | CT town rule | Darien Downtown CDP |
| Westport | CT | CT town rule | Saugatuck CDP |
| Fairfield | CT | CT town rule; no Fairfield CDP exists | none (town only) |
| Stratford | CT | CT town rule | Stratford Downtown CDP |
| Wilton | CT | CT town rule | Wilton Center CDP |
| Beacon Falls | CT | CT town rule | none (town only) |
| Seymour | CT | CT town rule | none (town only) |
| Branford | CT | CT town rule | Branford Center CDP |
| Guilford | CT | CT town rule | Guilford Center CDP |
| Madison | CT | CT town rule | Madison Center CDP |
| Westbrook | CT | CT town rule | Westbrook Center CDP |
| Old Saybrook | CT | CT town rule | Old Saybrook Center CDP |
| Wallingford | CT | CT town rule | Wallingford Center CDP |
| Berlin | CT | CT town rule | Kensington CDP |
| Windsor | CT | CT town rule | none (town only) |

(`Tuxedo`, NY is **not** in this group: it is a genuine incorporated village, just newer than the 2020 place file - incorporated Dec 23 2019, consolidated with the town Jan 1 2021, Census current-vintage GEOID 3675779.)

#### Sourcing limitations

| Source tried | Result |
|---|---|
| `https://www.mta.info/agency/long-island-rail-road` | **HTTP 403 Access Denied** (Akamai). Same for `new.mta.info`. |
| `https://www.mta.info/agency/metro-north-railroad` | **HTTP 403 Access Denied**. |
| `https://www.ctrail.com/hartford-line` | **HTTP 000** - no response / connection not completed. |
| `https://shorelineeast.com/` | **HTTP 200, served.** Station list corroborated: Stamford, Bridgeport, Stratford, Milford, West Haven, New Haven Union Station, State Street, Branford, Guilford, Madison, Clinton, Westbrook, Old Saybrook, New London. |
| `https://geocoding.geo.census.gov/geocoder/geographies/coordinates` | **Served, used heavily.** Point-in-polygon place/CDP for every station coordinate. This is what caught Yaphank-BNL -> Manorville, Deer Park -> Baywood, Cortlandt -> Montrose, Salisbury Mills -> Beaver Dam Lake, Middletown -> Scotchtown, Harriman -> Woodbury. |
| `https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress` | Returned non-JSON for the address form of the query; abandoned in favour of the coordinate form. |
| `https://nominatim.openstreetmap.org/reverse` | Too slow under rate limiting (timed out on a batch of 13). Not used; Wikipedia article prose + the Census coordinate geocoder were used instead. |

Because both MTA sites block scripted fetches, **all LIRR and Metro-North station existence / open-status facts come from Wikipedia line and station articles** (spec rule 2 fallback), with municipality independently confirmed by the Census coordinate geocoder.

#### 2025-2026 changes caught

1. **Yaphank-BNL station opened July 17 2026** on the LIRR Greenport Branch, serving Brookhaven National Laboratory, and **the old Yaphank station closed** after 181 years (1845-2026). Net effect: **Manorville** CDP gains commuter rail, **Yaphank** CDP loses it. This is the newest station in the batch.
2. **Elmont-UBS Arena station** (opened Nov 2021, full service Oct 2022) is the reason Elmont and Bellerose Terrace are in - the old Belmont Park stop was race-day only.
3. **Grand Central Madison** opened Jan 25 2023 as the LIRR's second Manhattan terminal (East Side Access), so LIRR now reaches Grand Central as well as Penn Station.
4. **Village of Tuxedo**, NY - incorporated Dec 23 2019, consolidated with the town Jan 1 2021, so it appears in the current Census place layer but not in the 2020 place-by-county file. Tuxedo station is inside it.
5. **CTrail Hartford Line** infill stations are still not open: **Enfield** is now dated *2027 (planned)*; **West Hartford**, **Newington** and **North Haven** remain "Future station". A Jan 2025 federal grant of $11.6M funds extending some weekend trains to Windsor Locks.
6. **Breakneck Ridge** (Hudson Line hikers' flag stop) is currently listed as **temporarily closed**.

### 2.3 Greater Boston - the MBTA network

**88 Census places.** 11 `subway`, 77 `commuter rail`. 84 MA, 4 RI.
Compiled 2026-07-29.

Massachusetts place naming follows the task brief: cities and **towns** are the places
(e.g. Brookline, Weston, Hingham), because the Census 2020 place layer for MA covers only
58 cities plus 191 partial-coverage CDPs and would drop most station towns entirely. Where
a station sits in a village or neighborhood inside a larger municipality (North Billerica,
Bradford, East Taunton), the municipality is used and the village is recorded in
`cdp_notes`.

---

#### Systems covered

| System | Type assigned | Source URL(s) | How station -> city was established |
|---|---|---|---|
| MBTA subway - Red Line (incl. Ashmont + Braintree branches) | `subway` | https://en.wikipedia.org/wiki/MBTA_subway , https://en.wikipedia.org/wiki/Red_Line_(MBTA) , https://api-v3.mbta.com/stops?filter[route]=Red | Red Line article's "Station listing" table has a **Location** column (Cambridge / Somerville / Boston neighborhoods / Quincy / Braintree). Cross-checked stop-by-stop against the official MBTA v3 API `municipality` field. |
| MBTA subway - Orange Line | `subway` | https://en.wikipedia.org/wiki/Orange_Line_(MBTA) , https://api-v3.mbta.com/stops?filter[route]=Orange | Same: Location column + API `municipality`. |
| MBTA subway - Blue Line | `subway` | https://en.wikipedia.org/wiki/Blue_Line_(MBTA) , https://api-v3.mbta.com/stops?filter[route]=Blue | Same. |
| MBTA subway - Green Line, branches B/C/D/E incl. the Green Line Extension | `subway` (per brief) | https://en.wikipedia.org/wiki/Green_Line_(MBTA) , .../Green_Line_B_branch , .../Green_Line_C_branch , .../Green_Line_D_branch , .../Green_Line_E_branch , .../Green_Line_Extension | Each branch article has a Location column; API `municipality` per stop for Green-B/C/D/E. |
| MBTA subway - Ashmont-Mattapan High-Speed Line (Mattapan trolley) | `subway` (per brief; MBTA calls it light rail, branded as part of the Red Line) | https://en.wikipedia.org/wiki/Ashmont%E2%80%93Mattapan_High-Speed_Line , https://api-v3.mbta.com/stops?filter[route]=Mattapan | Route section + Location column; API `municipality`. |
| MBTA Commuter Rail - 12 lines: Fairmount, Fall River/New Bedford, Fitchburg, Framingham/Worcester, Franklin/Foxboro, Greenbush, Haverhill, Kingston, Lowell, Needham, Newburyport/Rockport, Providence/Stoughton | `commuter rail` | https://en.wikipedia.org/wiki/List_of_MBTA_Commuter_Rail_stations (gold source) + each line article + https://api-v3.mbta.com/stops?filter[route]=CR-* | The List article carries an explicit **City/neighborhood** column, described in its own Key as "Identifies the municipality (and for Boston, the neighborhood) in which the station is located." Every one of the 143 active stations was then re-derived independently from the official MBTA v3 API, which returns a `municipality` string per stop. The two sources agreed on every station. |
| MBTA Silver Line (SL1-SL5, SLW) | **EXCLUDED - bus rapid transit** | https://en.wikipedia.org/wiki/Silver_Line_(MBTA) , https://en.wikipedia.org/wiki/MBTA_subway | See "Streetcar / borderline judgements". |

##### Official agency site: served

The MBTA did **not** block scripted fetches. `https://www.mbta.com/stops/commuter-rail`
returned HTTP 200 (720 KB) and `https://www.mbta.com/schedules/CR-Foxboro/line` returned
HTTP 200 (236 KB) with a plain `Mozilla/5.0` UA. More usefully, the unauthenticated
**MBTA v3 API** (`https://api-v3.mbta.com`) served every request, and its `/stops`
endpoint returns a `municipality` attribute per stop - so the primary station-to-city
mapping in this file is confirmed against the transit agency's own data, not only
Wikipedia.

Live checks made against the API on 2026-07-29:
- `/routes?filter[type]=0,1,2` returned exactly 8 subway routes (Red, Mattapan, Orange,
  Green-B/C/D/E, Blue) and 13 type-2 routes (the 12 commuter rail lines plus a separate
  `CR-Foxboro` "Foxboro Event Service" route). No Silver Line route appears under rail
  types 0/1/2 - it is type 3 (bus).
- `/schedules?filter[route]=Mattapan&filter[date]=2026-07-29` returned a full day of
  service, confirming the Mattapan trolley is currently operating.
- `/schedules?filter[route]=CR-Franklin&filter[stop]=FS-0049-S&filter[date]=2026-07-29`
  returned **21 scheduled stop events at Foxboro today** - i.e. ordinary timetabled
  service, not event-only.

---

#### Place-by-place

##### MBTA subway (`subway`) - 11 places

| Place | State | System | Station(s) | Source URL |
|---|---|---|---|---|
| Boston | MA | MBTA subway | All Red/Orange/Blue/Green central + branch stations plus Mattapan-line Ashmont, Cedar Grove, Butler, Mattapan | https://en.wikipedia.org/wiki/MBTA_subway |
| Cambridge | MA | MBTA subway | Red: Alewife, Porter, Harvard, Central, Kendall/MIT. Green D+E: Lechmere ("East Cambridge") | https://en.wikipedia.org/wiki/Red_Line_(MBTA) , https://en.wikipedia.org/wiki/Green_Line_D_branch |
| Somerville | MA | MBTA subway | Red: Davis. Orange: Assembly. Green D: Union Square. Green E: East Somerville, Gilman Square, Magoun Square | https://en.wikipedia.org/wiki/Green_Line_Extension |
| Medford | MA | MBTA subway | Orange: Wellington. Green E: Ball Square, Medford/Tufts | https://en.wikipedia.org/wiki/Green_Line_E_branch |
| Malden | MA | MBTA subway | Orange: Malden Center, Oak Grove | https://en.wikipedia.org/wiki/Orange_Line_(MBTA) |
| Revere | MA | MBTA subway | Blue: Wonderland, Revere Beach, Beachmont | https://en.wikipedia.org/wiki/Blue_Line_(MBTA) |
| Quincy | MA | MBTA subway | Red: North Quincy, Wollaston, Quincy Center, Quincy Adams | https://en.wikipedia.org/wiki/Red_Line_(MBTA) |
| Braintree | MA | MBTA subway | Red: Braintree | https://en.wikipedia.org/wiki/Red_Line_(MBTA) |
| Milton | MA | MBTA subway | Mattapan: Milton, Central Avenue, Valley Road, Capen Street | https://en.wikipedia.org/wiki/Ashmont%E2%80%93Mattapan_High-Speed_Line |
| Brookline | MA | MBTA subway | Green C: 13 stations (Saint Mary's St -> Englewood Ave). Green D: Longwood, Brookline Village, Brookline Hills, Beaconsfield, Reservoir | https://en.wikipedia.org/wiki/Green_Line_C_branch |
| Newton | MA | MBTA subway | Green D: Chestnut Hill, Newton Centre, Newton Highlands, Eliot, Waban, Woodland, Riverside | https://en.wikipedia.org/wiki/Green_Line_D_branch |

Collapsed-row quotes for the non-obvious ones:

- **Milton** - Mattapan-line article: "The line begins and ends within the city of Boston,
  but most of the southern half of its route is in the northern part of the neighboring
  town of Milton." The station table gives `rowspan=4 | Milton` for Milton, Central
  Avenue, Valley Road, Capen Street.
- **Newton** - Green Line D branch station table: `rowspan=7 | Newton` covering Chestnut
  Hill through Riverside. API confirms `municipality: Newton` for all seven.
- **Brookline** - Green Line C branch station table: `rowspan=16 | Brookline`.
- **Boston College (Green B)** - listed as `Brighton / Newton`. The MBTA API gives
  `municipality: Boston` for Boston College station, so the B branch adds no Newton claim
  of its own; Newton is carried by the D branch instead.

##### MBTA Commuter Rail (`commuter rail`) - 77 places

Grouped by line. Boston, Quincy, Braintree, Malden, Medford, Cambridge, Somerville,
Newton, Brookline, Milton and Revere are all commuter-rail-served too where noted below,
but appear in the JSON as `subway` because subway is the higher tier.

**Greenbush Line** - https://en.wikipedia.org/wiki/Greenbush_Line

| Place | Station(s) |
|---|---|
| Weymouth | Weymouth Landing/East Braintree, East Weymouth |
| Hingham | West Hingham, Nantasket Junction |
| Cohasset | Cohasset |
| Scituate | North Scituate, Greenbush |

**Kingston Line** - https://en.wikipedia.org/wiki/Kingston_Line

| Place | Station(s) |
|---|---|
| Weymouth | South Weymouth |
| Abington | Abington |
| Whitman | Whitman |
| Hanson | Hanson |
| Halifax | Halifax |
| Kingston | Kingston |

Line article, Route section: "At Braintree, the line switches to the **Plymouth Branch**,
which continues southeast through Weymouth, Abington, Whitman, Hanson, Halifax, and
Kingston."

**Fall River/New Bedford Line** (South Coast Rail Phase 1) - https://en.wikipedia.org/wiki/Fall_River/New_Bedford_Line

| Place | Station(s) |
|---|---|
| Randolph | Holbrook/Randolph |
| Brockton | Montello, Brockton, Campello |
| Bridgewater | Bridgewater |
| Middleborough | Middleborough (new, 2025) |
| Taunton | East Taunton (2025) |
| Freetown | Freetown (2025) |
| Fall River | Fall River Depot (2025) |
| New Bedford | Church Street (2025), New Bedford (2025) |

**Fairmount Line** - https://en.wikipedia.org/wiki/Fairmount_Line - all 9 stations are in
Boston (Newmarket, Uphams Corner, Four Corners/Geneva, Talbot Avenue, Morton Street,
Blue Hill Avenue, Fairmount, Readville, South Station). Adds no new place.

**Providence/Stoughton Line** - https://en.wikipedia.org/wiki/Providence/Stoughton_Line

| Place | State | Station(s) |
|---|---|---|
| Westwood | MA | Route 128 |
| Canton | MA | Canton Junction, Canton Center |
| Stoughton | MA | Stoughton |
| Sharon | MA | Sharon |
| Mansfield | MA | Mansfield |
| Attleboro | MA | Attleboro, South Attleboro |
| Pawtucket | RI | Pawtucket/Central Falls |
| Providence | RI | Providence |
| Warwick | RI | T.F. Green Airport |
| North Kingstown | RI | Wickford Junction |

Boston also has Back Bay, Ruggles, Forest Hills, Hyde Park and Readville on this line.

**Franklin/Foxboro Line** - https://en.wikipedia.org/wiki/Franklin/Foxboro_Line

| Place | Station(s) |
|---|---|
| Dedham | Endicott, Dedham Corporate Center |
| Westwood | Islington |
| Norwood | Norwood Depot, Norwood Central, Windsor Gardens |
| Walpole | Walpole |
| Foxborough | Foxboro |
| Norfolk | Norfolk |
| Franklin | Franklin, Forge Park/495 |

**Needham Line** - https://en.wikipedia.org/wiki/Needham_Line - Needham (Hersey, Needham
Junction, Needham Center, Needham Heights); the rest (Roslindale Village, Bellevue,
Highland, West Roxbury, Forest Hills, Ruggles, Back Bay, South Station) are Boston.

**Framingham/Worcester Line** - https://en.wikipedia.org/wiki/Framingham/Worcester_Line

| Place | Station(s) |
|---|---|
| Newton | Newtonville, West Newton, Auburndale |
| Wellesley | Wellesley Farms, Wellesley Hills, Wellesley Square |
| Natick | Natick Center, West Natick |
| Framingham | Framingham |
| Ashland | Ashland |
| Southborough | Southborough |
| Westborough | Westborough |
| Grafton | Grafton |
| Worcester | Worcester |

Boston also has Lansdowne and Boston Landing on this line.

**Fitchburg Line** - https://en.wikipedia.org/wiki/Fitchburg_Line

| Place | Station(s) |
|---|---|
| Cambridge | Porter |
| Belmont | Belmont Center, Waverley |
| Waltham | Waltham, Brandeis/Roberts |
| Weston | Kendal Green, Silver Hill |
| Lincoln | Lincoln |
| Concord | Concord, West Concord |
| Acton | South Acton |
| Littleton | Littleton/Route 495 |
| Ayer | Ayer |
| Shirley | Shirley |
| Leominster | North Leominster |
| Fitchburg | Fitchburg, Wachusett |

**Lowell Line** - https://en.wikipedia.org/wiki/Lowell_Line

| Place | Station(s) |
|---|---|
| Medford | West Medford |
| Winchester | Wedgemere, Winchester Center |
| Woburn | Anderson/Woburn |
| Wilmington | Wilmington |
| Billerica | North Billerica |
| Lowell | Lowell |

**Haverhill Line** - https://en.wikipedia.org/wiki/Haverhill_Line

| Place | Station(s) |
|---|---|
| Malden | Malden Center, Oak Grove |
| Melrose | Wyoming Hill, Melrose/Cedar Park, Melrose Highlands |
| Wakefield | Greenwood, Wakefield |
| Reading | Reading |
| Wilmington | North Wilmington |
| Andover | Ballardvale, Andover |
| Lawrence | Lawrence |
| Haverhill | Bradford, Haverhill |

**Newburyport/Rockport Line** - https://en.wikipedia.org/wiki/Newburyport/Rockport_Line

| Place | Station(s) |
|---|---|
| Chelsea | Chelsea |
| Lynn | River Works, Lynn (interim platforms) |
| Swampscott | Swampscott |
| Salem | Salem |
| Beverly | Beverly, North Beverly, Montserrat, Beverly Farms |
| Hamilton | Hamilton/Wenham |
| Wenham | Hamilton/Wenham (southern end of platform) |
| Ipswich | Ipswich |
| Rowley | Rowley |
| Newburyport | Newburyport |
| Manchester-by-the-Sea | Manchester |
| Gloucester | West Gloucester, Gloucester |
| Rockport | Rockport |

##### Trap-by-trap verification (each one checked against a station or line article)

| Trap | Verdict | Verbatim evidence |
|---|---|---|
| Route 128 station | **Westwood**, not Boston/Dedham | List article City column: `Route 128 ... Westwood`. MBTA API: `Route 128 \| Westwood`. |
| Readville, Hyde Park | **Boston** | List article: `Readville ... Boston/Hyde Park`; `Hyde Park ... Boston/Hyde Park`. |
| Silver Hill, Hastings, Kendal Green | **Weston** | Kendal Green article: "Kendal Green station is an MBTA Commuter Rail station in Weston, Massachusetts". Silver Hill article: "...station in Weston, Massachusetts". Hastings is indefinitely closed; Weston still qualifies via Kendal Green + Silver Hill. |
| Brandeis/Roberts | **Waltham** | List article: `Brandeis/Roberts ... Waltham`. API: `Brandeis/Roberts \| Waltham`. |
| Windsor Gardens | **Norwood** | List article: `Windsor Gardens ... Norwood`. API: `Windsor Gardens \| Norwood`. |
| Plimptonville | **Walpole**, and indefinitely closed | List article: `Plimptonville ... Walpole`, and the article's lead lists Plimptonville among "Five additional stations ... indefinitely closed due to service cuts during the COVID-19 pandemic." Walpole is in the dataset via Walpole station instead. |
| Norfolk | **Norfolk** (own town) | List article: `Norfolk ... Norfolk`. |
| Forge Park/495 | **Franklin** | List article: `Forge Park/495 ... Franklin`. |
| Foxboro / Gillette Stadium | **Foxborough** | List article: `Foxboro ... Foxborough`. API: `Foxboro \| Foxborough`. |
| Ballardvale, Andover | **Andover** (both) | List article gives Andover for both. |
| Bradford | **Haverhill** | Bradford station article: "an MBTA Commuter Rail station in the Bradford neighborhood of Haverhill, Massachusetts". API: `Bradford \| Haverhill`. |
| Montserrat, Prides Crossing, Beverly Farms | **Beverly** (all three) | List article gives Beverly for each. Prides Crossing is one of the five indefinitely closed stations; Beverly qualifies on the other three anyway. |
| Manchester | **Manchester-by-the-Sea** | List article: `Manchester ... Manchester-by-the-Sea`. API: `Manchester \| Manchester-by-the-Sea`. |
| Hamilton/Wenham | **Hamilton AND Wenham** | Station article: "is an MBTA Commuter Rail station in Hamilton and Wenham, Massachusetts ... straddling the Hamilton-Wenham town line, with the southern end of the platform geographically in Wenham." Article also carries both `Category:Buildings and structures in Hamilton, Massachusetts` and `...in Wenham, Massachusetts`. The MBTA API reports only `Hamilton`, which is noted in `cdp_notes` for both entries. |
| Cohasset / Nantasket Junction | **Cohasset** / **Hingham** | List article: `Cohasset ... Cohasset`; `Nantasket Junction ... Hingham`. Nantasket Beach is in Hull, but the station is not. |
| Halifax | **Halifax** (own town) | List + Kingston Line articles. |
| Middleborough / Lakeville | **Middleborough**; Lakeville dropped | See 2025 changes below. |
| East Taunton | **Taunton** | Station article: "The station is located in the southeast portion of Taunton along the New Bedford Secondary". API: `East Taunton \| Taunton`. East Taunton is a village inside the city of Taunton, not a separate Census place. |
| North Billerica | **Billerica** | Station article: "an MBTA Commuter Rail station in Billerica, Massachusetts ... located in the North Billerica village". |
| Pawtucket/Central Falls | **Pawtucket only** | Station article: "is a commuter rail station in Pawtucket, Rhode Island. It opened ... January 23, 2023." The pre-1981 station "located slightly northeast on the border of Pawtucket and Central Falls" is a different, closed structure. Central Falls is therefore **not** in the dataset. |
| Everett (named in the task brief as a candidate) | **NOT included** | MBTA subway article: the Orange Line's "northern end was relocated in 1975 from Everett to Oak Grove (Malden, MA)". Everett has had no rapid transit station since 1975 and no commuter rail station. |
| Chelsea | **commuter rail, not subway** | Silver Line SL3 serves Chelsea but is BRT. Chelsea's rail service is the Newburyport/Rockport Line station only. |

---

#### Streetcar / borderline judgements

| System | Call | Why |
|---|---|---|
| **MBTA Green Line** (B, C, D, E, incl. the Green Line Extension to Somerville and Medford) | Counted as `"subway"` | Per the explicit instruction in the shared spec: "MBTA Red/Orange/Blue **and Green Line** (treated as subway per brief)". Independently defensible on the spec's own streetcar test: the Green Line runs through the Tremont Street Subway and the Boylston Street Subway downtown, and the C/D/E outer branches use reserved median or fully private right-of-way (the D branch is a former Boston & Albany railroad line, entirely grade-separated). MBTA's own classification is light rail (MBTA subway article: "one branched light rail system (Green)"). Source: https://en.wikipedia.org/wiki/Green_Line_(MBTA) , https://en.wikipedia.org/wiki/MBTA_subway |
| **Green Line Extension** (Union Square branch + Medford branch) | Counted; already open | Union Square (Somerville) opened March 21, 2022; the Medford branch (East Somerville, Gilman Square, Magoun Square, Ball Square, Medford/Tufts) opened December 12, 2022 - both dates from the E/D branch station tables and https://en.wikipedia.org/wiki/Green_Line_Extension . Not a "not yet open" exclusion. |
| **Ashmont-Mattapan High-Speed Line** (Mattapan trolley, PCC streetcars) | Counted as `"subway"` per the brief; would qualify as light rail on the spec's own test regardless | Route section: "The right-of-way is owned by the MBTA and has only two at-grade crossings on its 2.6 mi route." It is a fully reserved former commuter-rail alignment with no mixed street running, running 6-minute peak headways - the opposite of a downtown mixed-traffic loop. It is branded and mapped as part of the Red Line. Only new place it contributes is Milton. Source: https://en.wikipedia.org/wiki/Ashmont%E2%80%93Mattapan_High-Speed_Line |
| **MBTA Silver Line** (SL1, SL2, SL3, SL4, SL5, SLW) | **EXCLUDED - bus rapid transit, not rail** | Silver Line article, first line of body: "The **Silver Line** is a bus route system in Boston and Chelsea, Massachusetts, operated by the Massachusetts Bay Transportation Authority (MBTA). It is operated as part of the MBTA bus system, but branded as bus rapid transit (BRT) as part of the MBTA subway system." The MBTA subway article's own line count reads "3 heavy rail ... 2 light rail ... **1 bus rapid transit (Silver)**". The MBTA v3 API returns no Silver Line route under rail types 0/1/2. **This is why Chelsea is `commuter rail`, not `subway`** - SL3's Chelsea branch is a busway, so Chelsea's only rail is its Newburyport/Rockport Line station. Source: https://en.wikipedia.org/wiki/Silver_Line_(MBTA) |
| **CapeFLYER** | **EXCLUDED - seasonal excursion service** | Described in the Fall River/New Bedford Line article as "Seasonal CapeFlyer excursion service", summer weekends only. It is the only remaining service at Lakeville station, so Lakeville is excluded (see below). Buzzards Bay / Bourne / Hyannis are likewise out of scope. Source: https://en.wikipedia.org/wiki/Fall_River/New_Bedford_Line |
| **`CR-Foxboro` "Foxboro Event Service"** | Route excluded as event-only, but **Foxborough is still in** on regular Franklin/Foxboro Line service | The API lists a separate `CR-Foxboro` route named "Foxboro Event Service" (Gillette Stadium specials via Providence/Attleboro/Dedham). That route on its own would be event-only and would not qualify. Foxborough qualifies instead on the *scheduled* Franklin/Foxboro Line: "Foxboro service and the line's renaming were made permanent effective October 2, 2023," and a live API schedule query returned 21 timetabled Foxboro stop events for 2026-07-29. |

---

#### Deliberately excluded

| Thing | Why |
|---|---|
| MBTA Silver Line SL1/SL2/SL3/SL4/SL5/SLW | Bus rapid transit, not rail (spec rule 4). Affects Chelsea's tier and adds no places. |
| Everett, MA | No rail station. Orange Line's northern terminus was moved from Everett to Oak Grove in Malden in 1975; Everett has bus service only. |
| Central Falls, RI | Pawtucket/Central Falls station (2023) is in Pawtucket. Only the long-closed pre-1981 station sat on the city line. |
| Lakeville, MA | Middleborough/Lakeville station "closed for commuter rail service on March 24, 2025; still used for seasonal CapeFlyer service." Seasonal excursion service only, so excluded. |
| Plymouth, MA | Plymouth station "has been indefinitely closed since 2021" (closed April 5, 2021, when the line was renamed the Kingston Line). No other station in Plymouth. |
| Woburn's Mishawum station | One of the five indefinitely closed stations. Woburn is still in the dataset via Anderson/Woburn. |
| Weston's Hastings station | Indefinitely closed. Weston is still in via Kendal Green and Silver Hill. |
| Beverly's Prides Crossing station | Indefinitely closed. Beverly is still in via four other stations. |
| Walpole's Plimptonville station | Indefinitely closed. Walpole is still in via Walpole station. |
| Blue Line extension to Lynn | Proposed only; Blue Line's northern terminus is Wonderland in Revere. Lynn is in the dataset as commuter rail. |
| South Coast Rail Phase 2 stations - Battleship Cove (Fall River), Easton Village and North Easton (North Easton/Stoughton), Raynham Place (Raynham), Taunton (downtown) | "Five additional stations are planned, but not funded, as part of the second phase of the South Coast Rail project." Not open. Excludes **Raynham** and **Easton** entirely; Fall River, Taunton and Stoughton are already in via open stations. |
| West Station (Boston) | Planned, not funded/open. |
| South Salem station (Salem) | "municipally planned"; not open. Salem already in. |
| Berkley, MA | The Fall River/New Bedford Line splits at Myricks Junction in Berkley, but there is no station in Berkley. |
| Chelmsford, Gardner, North Andover, Blackstone, Lexington, Bedford, Arlington, Sudbury, Wayland, Medfield, Millis, Dover, Medway, Hudson, Nashua NH, Manchester NH, Concord NH, Dover NH, Exeter NH, Portsmouth NH, Durham NH, Plaistow NH, Atkinson NH, East Kingston NH, Newfields NH, Newmarket NH, Newton NH, Hampton NH, North Hampton NH | Former MBTA / predecessor-railroad stations, all closed between 1965 and 1996 per the List article's "Former stations" tables. No current service. |
| Amtrak-only places (e.g. Route 128 is shared, but Amtrak-only stops in the corridor) | Intercity Amtrak-only service excluded per spec rule 4. Every place in this file has MBTA service. |
| Boston Logan people-mover / Massport shuttles, MBTA ferries | Not rail rapid transit. |

---

#### 2025-2026 changes caught

1. **South Coast Rail Phase 1 DID open - March 24, 2025.** "The first phase opened on
   March 24, 2025, becoming part of the Fall River/New Bedford Line." Six new stations,
   36.1 mi of track. This adds five brand-new places to the dataset:
   **Taunton** (East Taunton station), **Freetown**, **Fall River** (Fall River Depot),
   **New Bedford** (Church Street + New Bedford), and a relocated
   **Middleborough**. Source: https://en.wikipedia.org/wiki/South_Coast_Rail
2. **Middleborough/Lakeville station closed March 24, 2025** and service moved 0.7 mi
   north to the new Middleborough station: "Commuter rail service was moved to
   Middleborough station 0.7 miles north. The station was renamed to Lakeville station and
   is still served by the CapeFlyer." Net effect: **Lakeville leaves the dataset,
   Middleborough enters it.** This is the single most likely error in any pre-2025 list.
3. **The line was renamed** from Middleborough/Lakeville Line to **Fall River/New Bedford
   Line** in 2025 (API route id is still `CR-NewBedford`).
4. **Silver Hill station (Weston) reopened November 18, 2024** after being indefinitely
   closed in April 2021 - and the `List of MBTA Commuter Rail stations` article is stale on
   this point, still listing Silver Hill among the five indefinitely closed stations while
   the station's own article and the live MBTA API both show it in service. Weston was
   already in the dataset via Kendal Green, so no place count changes.
5. **Foxboro station**: midday service was temporarily cancelled from **August 11, 2025**
   for construction of a permanent accessible platform (compounded by an Amtrak signal-
   bungalow fire on August 1, 2025), and **midday service resumed June 1, 2026** after the
   work finished. Foxborough therefore has continuous scheduled weekday service and stays
   in the dataset.
6. **Kingston Line**: off-peak and weekend stops at JFK/UMass removed effective
   **July 21, 2025** (peak-hour peak-direction only). No place effect.
7. **Fairmount Line weekend diversions** began June 2, 2025 for track work, with weekend
   Franklin/Foxboro trains pushed back to the Northeast Corridor. No place effect.
8. **Lynn**: still running on interim platforms (opened December 18, 2023); the permanent
   station's location was re-evaluated in 2024 and a design firm was selected in 2025, with
   completion not expected before 2030. Lynn stays in on the interim station.

---

#### Sourcing limitations

- **Nothing blocked me.** The MBTA's public site served over plain curl (HTTP 200 on both
  `https://www.mbta.com/stops/commuter-rail` and `https://www.mbta.com/schedules/CR-Foxboro/line`),
  and the unauthenticated MBTA v3 API served every `/routes`, `/stops` and `/schedules`
  query. Because `/stops` exposes a `municipality` field, the station-to-city mapping in
  this file is double-sourced (Wikipedia station-list + transit agency data) for all 143
  active commuter rail stations and all 153 subway stations.
- **One first-attempt API quirk:** `filter[route]=CR-Providence` and `CR-Foxboro` initially
  returned zero stops because zsh glob-expanded the unquoted square brackets in the URL;
  re-issuing with percent-encoded `filter%5Broute%5D` returned the full 18-stop
  Providence/Stoughton list including all four Rhode Island stations. No data was missing.
- **One genuine judgement call, flagged rather than hidden: Wenham, MA.** The MBTA's own
  `municipality` field for Hamilton/Wenham station says only `Hamilton`. Wenham is included
  on the strength of the station article's explicit statement that the platform straddles
  the town line "with the southern end of the platform geographically in Wenham," plus the
  article's Wenham category. If the consumer of this dataset wants strict
  one-station-one-municipality behaviour, Wenham is the single row to drop (making the
  count 87).
- **One stale upstream source, worked around:** the `List of MBTA Commuter Rail stations`
  article's lead still lists Silver Hill among the indefinitely closed stations although it
  reopened on November 18, 2024. Resolved in favour of the station article and the live API.
- **Massachusetts Census place geography is genuinely awkward** and I did not silently
  paper over it. The Census 2020 place layer for MA contains only 58 incorporated places
  (cities) plus 191 CDPs; most station towns (Weston, Wenham, Manchester-by-the-Sea,
  Middleborough, Cohasset, Halifax, Norfolk, Hingham as a town, ...) are MCDs, not places,
  and villages like North Billerica and East Taunton are neither. Per the task brief I used
  the city/town municipality as the place name throughout, which is also what the spec's own
  "Brookline" example implies.

### 2.4 Philadelphia, Baltimore, Washington DC

**166 Census places** across PA (81), MD (50), VA (20), NJ (9), DE (3), WV (2), DC (1).
Tiers: subway 46, light rail 21, commuter rail 99.

Place-name rule applied throughout: use the **2020 Census place** (incorporated place or CDP)
that a fetched source names as the station's location. Where the named community is *not* a 2020
Census place, fall back to the **PA/NJ township** (explicitly allowed by the shared spec). MD, VA,
DE and WV have no township fallback, so a station in an unincorporated non-CDP community there is
**excluded and logged** (see section 4). Census-place status was checked against
`scratchpad/place_by_county2020.txt` (2020 Census place-by-county file, `PLACENAME`/`TYPE` columns).

---

#### 1. Systems covered

| System | Type assigned | Source URL(s) | How station -> city was established |
|---|---|---|---|
| SEPTA Metro **B** (Broad Street Line) + **L** (Market-Frankford Line) | **subway** | [List of SEPTA Metro stations](https://en.wikipedia.org/wiki/List_of_SEPTA_Metro_stations), [Broad Street Line](https://en.wikipedia.org/wiki/Broad_Street_Line), [Market–Frankford Line](https://en.wikipedia.org/wiki/Market%E2%80%93Frankford_Line) | The station list has a dedicated "Neighborhood/Municipality/Borough" + "County" column for every station. Named in the spec's subway list. |
| SEPTA Metro **M** (Norristown High Speed Line, ex-Route 100) | **light rail** (judged, see §3) | [Norristown High Speed Line](https://en.wikipedia.org/wiki/Norristown_High_Speed_Line), [List of SEPTA Metro stations](https://en.wikipedia.org/wiki/List_of_SEPTA_Metro_stations) | Same municipality column in the station list. |
| SEPTA Metro **T** (subway-surface trolleys, ex-Routes 10/34/13/11/36) | **light rail** | [SEPTA subway–surface trolley lines](https://en.wikipedia.org/wiki/SEPTA_subway%E2%80%93surface_trolley_lines) | Infobox `locale` = "Philadelphia, Yeadon, and Darby, Pennsylvania"; route table gives the western termini (Darby Transit Center, Yeadon). |
| SEPTA Metro **D** (Media–Sharon Hill, ex-Routes 101/102) | **light rail** | [Media–Sharon Hill Line](https://en.wikipedia.org/wiki/Media%E2%80%93Sharon_Hill_Line), [List of SEPTA Metro stations](https://en.wikipedia.org/wiki/List_of_SEPTA_Metro_stations) | The line article's stop table has a "Location" column grouping every stop by municipality. |
| SEPTA Regional Rail (all 13 lines) | **commuter rail** | [List of SEPTA Regional Rail stations](https://en.wikipedia.org/wiki/List_of_SEPTA_Regional_Rail_stations) (Featured List) + the 13 per-line articles + ~50 individual station articles | Station list has a sourced "Location" column; per-line articles have a second "Location" column that often gives the *township* instead. Where the two conflicted I fetched the station article (logged below). |
| PATCO Speedline | **subway** | [PATCO Speedline](https://en.wikipedia.org/wiki/PATCO_Speedline), official [ridepatco.org/stations](https://www.ridepatco.org/stations/) | Wikipedia station table has a municipality column ("Haddon Twp.", "Cherry Hill", "Voorhees"); the official site (HTTP 200, served fine) confirmed the 14-station roster. Named in the spec's subway list. |
| Baltimore Metro SubwayLink | **subway** | [Baltimore Metro SubwayLink](https://en.wikipedia.org/wiki/Baltimore_Metro_SubwayLink) | Station table "Location" column + the explicit sentence *"All stations except Owings Mills, Old Court, and Milford Mill are located in Baltimore."* |
| Baltimore Light RailLink | **light rail** | [List of Baltimore Light RailLink stations](https://en.wikipedia.org/wiki/List_of_Baltimore_Light_RailLink_stations), [Baltimore Light RailLink](https://en.wikipedia.org/wiki/Baltimore_Light_RailLink) | The list article gives cross-streets **plus the community** for all 33 stops. |
| MARC Train (Penn, Camden, Brunswick) | **commuter rail** | [Penn Line](https://en.wikipedia.org/wiki/Penn_Line), [Camden Line](https://en.wikipedia.org/wiki/Camden_Line), [Brunswick Line](https://en.wikipedia.org/wiki/Brunswick_Line) | Each line article's station table has State + Town/City columns for every stop. |
| Washington Metro (WMATA) | **subway** | [List of Washington Metro stations](https://en.wikipedia.org/wiki/List_of_Washington_Metro_stations) + 43 individual station articles | The list article's "Jurisdiction" column is **county-level only**, so every suburban station's CDP was taken from its own article (lead sentence or infobox `borough`). Named in the spec's subway list. |
| Virginia Railway Express | **commuter rail** | [Virginia Railway Express](https://en.wikipedia.org/wiki/Virginia_Railway_Express), [Manassas Line](https://en.wikipedia.org/wiki/Manassas_Line) | Both line tables have a "Location" column. |

---

#### 2. Place-by-place

##### SEPTA Metro - subway (B / L)

| Place | State | Station(s) | Source |
|---|---|---|---|
| Philadelphia | PA | ~50 B + L stations, all Philadelphia County | List of SEPTA Metro stations |
| Upper Darby | PA | 69th Street Transit Center (L terminus). Township, Delaware County. Quote: *"69th Street Transit Center† \| L1 M1 D1 D2 \| Upper Darby \| Delaware"* | List of SEPTA Metro stations |
| Millbourne | PA | Millbourne (L). Quote: *"Millbourne \| L1 \| Millbourne \| Delaware"* | List of SEPTA Metro stations |

##### SEPTA Metro - light rail (M / T / D)

| Place | State | Station(s) | Source |
|---|---|---|---|
| Upper Darby (already subway) | PA | M: Parkview. D1/D2: Lansdowne Ave, Congress Ave, Beverly Blvd, Hilltop Rd, Avon Rd, Walnut St, Fairfield Ave, Marshall Rd, Garrettford, Drexel Manor, Drexel Park, Drexelbrook, Drexeline, Anderson Ave, Aronimink, School Lane, Huey Ave, Creek Rd, Irvington Rd | Media–Sharon Hill Line; SEPTA Metro list |
| Drexel Hill | PA | D1/D2 trunk + branches. CDP inside Upper Darby Twp. Line-article rowspans: *"Drexel Hill \| Drexeline / Drexelbrook / Anderson Avenue / Aronimink / School Lane / Huey Avenue"* and *"Drexel Hill \| Drexel Hill Junction / Irvington Road / Drexel Park"* | Media–Sharon Hill Line |
| Springfield | PA | D1: Pine Ridge, Paper Mill Rd, Springfield Mall, Thomson Ave, Woodland Ave, Leamy Ave, Saxer Ave, Brookside–Springfield, Scenic Rd. **Springfield Township, DELAWARE County** | Media–Sharon Hill Line; SEPTA Metro list |
| Media | PA | D1 terminus Orange Street/Media + Veterans Sq, Olive, Jackson, Monroe, Edgemont, Manchester, Providence Rd/Media, Beatty Rd. Quote: *"D1 … South Terminal: **Media** Orange St at State St"* | Media–Sharon Hill Line |
| Clifton Heights | PA | D2: Clifton–Aldan, Springfield–Madison, Penn St, Baltimore Ave | Media–Sharon Hill Line |
| Aldan | PA | D2 street stops: Magnolia Ave, Woodlawn–Providence (Shisler Ave closed 2010). Quote: *"it goes into the street in Aldan"* | Media–Sharon Hill Line |
| Collingdale | PA | D2: MacDade Blvd, Andrews Ave, Bartram Ave, North St | Media–Sharon Hill Line |
| Sharon Hill | PA | D2 terminus Chester Pike/Sharon Hill | Media–Sharon Hill Line |
| Haverford | PA | M: Ardmore Ave, Ardmore Junction, Beechwood–Brookline, Haverford, Penfield, Township Line Rd, Wynnewood Rd. **Haverford Township, Delaware County** | List of SEPTA Metro stations |
| Radnor | PA | M: Bryn Mawr, Garrett Hill, Radnor, Stadium, Villanova. **Radnor Township** (no Radnor CDP exists in 2020) | List of SEPTA Metro stations |
| Lower Merion | PA | M: County Line, Matsonford, Roberts Road. **Lower Merion Township, Montgomery County** | List of SEPTA Metro stations |
| Upper Merion | PA | M: Gulph Mills, Hughes Park. **Upper Merion Township** | List of SEPTA Metro stations |
| Bridgeport | PA | M: Bridgeport, DeKalb Street | List of SEPTA Metro stations |
| Norristown | PA | M northern terminus Norristown Transit Center | List of SEPTA Metro stations |
| Yeadon | PA | T3 outer terminal ("Yeadon"); + RR Fernwood–Yeadon. Quote: *"locale = Philadelphia, Yeadon, and Darby, Pennsylvania"* | SEPTA subway–surface trolley lines |
| Darby | PA | T4 (and limited T3) terminal, Darby Transit Center; + RR Darby. Quote: *"The T4 travels along Woodland Avenue in Philadelphia and Main Street in Darby"* | SEPTA subway–surface trolley lines |

##### PATCO Speedline - subway

| Place | State | Station(s) | Source |
|---|---|---|---|
| Philadelphia | PA | 15–16th & Locust, 12–13th & Locust, 9–10th & Locust, 8th & Market, Franklin Square (reopened 2025) | PATCO Speedline; ridepatco.org |
| Camden | NJ | City Hall, Broadway (WRTC), Ferry Avenue | PATCO Speedline |
| Collingswood | NJ | Collingswood | PATCO Speedline |
| Westmont | NJ | Westmont. CDP in **Haddon Township** - line table row: *"Haddon Twp. \| Westmont"* | PATCO Speedline |
| Haddonfield | NJ | Haddonfield | PATCO Speedline |
| Cherry Hill | NJ | Woodcrest - line table row: *"Cherry Hill \| Woodcrest"*. "Woodcrest" is not a NJ Census place, so the township name is used | PATCO Speedline |
| Ashland | NJ | Ashland. CDP in **Voorhees Township** - line table row: *"Voorhees \| Ashland"* | PATCO Speedline |
| Lindenwold | NJ | Lindenwold (eastern terminus) | PATCO Speedline |

##### Baltimore Metro SubwayLink - subway

| Place | State | Station(s) | Source |
|---|---|---|---|
| Baltimore | MD | Reisterstown Plaza, Rogers Ave, West Cold Spring, Mondawmin, Penn-North, Upton–Avenue Market, State Center, Lexington Market, Charles Center, Shot Tower, Johns Hopkins Hospital. Quote: *"All stations except Owings Mills, Old Court, and Milford Mill are located in Baltimore."* | Baltimore Metro SubwayLink |
| Owings Mills | MD | Owings Mills (west terminus) | Baltimore Metro SubwayLink |
| Lochearn | MD | Old Court, Milford Mill - table rowspan: *"Lochearn \| Old Court / Milford Mill"* | Baltimore Metro SubwayLink |

##### Baltimore Light RailLink - light rail

| Place | State | Station(s) | Source (all: List of Baltimore Light RailLink stations) |
|---|---|---|---|
| Baltimore (already subway) | MD | Mt. Washington, Cold Spring Lane, Woodberry, North Ave, Mt. Royal/MICA, Cultural Center, Mt. Vernon, Lexington Market, Baltimore Arena, Convention Center, Camden Yards, Stadium/Federal Hill, Westport, Cherry Hill, Penn Station | list article |
| Cockeysville | MD | Warren Road - *"Warren & Beaver Dam / Cockeysville"* | list article |
| Timonium | MD | Fairgrounds, Timonium - both *"…/ Timonium"* | list article |
| Lutherville | MD | Lutherville - *"West end of Ridgely Road / Lutherville"* | list article |
| Towson | MD | Falls Road - *"Falls & Lake Roland Park entrance / Towson"* | list article |
| Linthicum | MD | North Linthicum, Linthicum, BWI Business District - all *"… / Linthicum Heights"* (2020 CDP name is "Linthicum") | list article |
| Glen Burnie | MD | Ferndale, Glen Burnie - both *"MD 648 & … / Glen Burnie"*. The source puts Ferndale station in Glen Burnie, so the separate Ferndale CDP is **not** claimed | list article |

##### SEPTA Regional Rail - commuter rail (all 13 lines)

All 155 stations were walked. Philadelphia (subway tier) holds ~60 of them across the Airport, Chestnut Hill East, Chestnut Hill West, Cynwyd, Fox Chase, Manayunk/Norristown, Media/Wawa, Paoli/Thorndale, Trenton, Warminster, West Trenton and Wilmington/Newark lines, plus Center City (30th Street, Suburban, Jefferson, Temple University, Penn Medicine). Non-Philadelphia places:

| Place | State | Line / station(s) | Notes + source |
|---|---|---|---|
| Lansdowne | PA | MED: Lansdowne, Gladstone | station list + Media/Wawa Line |
| Aldan / Clifton Heights | PA | MED: Clifton–Aldan, Primos | already light-rail tier |
| Ridley | PA | WIL: Crum Lynne; MED: Secane | **Ridley Township**. *"Crum Lynne is an unincorporated community in Ridley Township"*; *"Secane is an unincorporated community in Ridley Township and Upper Darby Township"* - neither is a 2020 place |
| Morton | PA | MED: Morton | borough |
| Swarthmore | PA | MED: Swarthmore | borough |
| Nether Providence | PA | MED: Wallingford, Moylan–Rose Valley | **Nether Providence Township**. *"Wallingford is an unincorporated community in Nether Providence Township"*; Moylan–Rose Valley station *"is a SEPTA Regional Rail station in Nether Providence Township"* |
| Upper Providence | PA | MED: Media station | **Upper Providence Township, Delaware County**. *"Media station is a SEPTA regional rail station in Upper Providence Township, Delaware County, Pennsylvania"*. Conflict logged in §5 |
| Middletown | PA | MED: Elwyn, Wawa | **Middletown Township, Delaware County**. Wawa Station *"located adjacent to U.S. Route 1 in Middletown Township, Delaware County"*; *"Elwyn is an unincorporated community located in Middletown Township, Delaware County"* |
| Darby / Sharon Hill | PA | WIL: Darby, Sharon Hill, Curtis Park | already light-rail tier |
| Folcroft, Glenolden, Norwood, Prospect Park, Ridley Park, Eddystone, Marcus Hook | PA | WIL | Delaware County boroughs, all named directly in the station list and the Wilmington/Newark Line table |
| Chester | PA | WIL: Chester Transit Center, Highland Avenue | city |
| Ardmore, Bryn Mawr, Rosemont, Villanova, Wayne, St. Davids | PA | PAO | Census CDPs; townships given in `cdp_notes` |
| Radnor | PA | PAO: Radnor | already light-rail tier. *"Radnor station … 291 King of Prussia Road … in Radnor Township"* |
| Lower Merion | PA | PAO: Haverford, Wynnewood | already light-rail tier. Haverford station and Wynnewood station both carry `[[Category:Lower Merion Township, Pennsylvania]]`; neither "Haverford" nor "Wynnewood" is a 2020 place |
| Merion Station | PA | PAO: Merion | CDP; SEPTA calls the station "Merion" |
| Narberth | PA | PAO: Narberth | borough |
| Tredyffrin | PA | PAO: Strafford | **Tredyffrin Township**; Strafford station carries `[[Category:Tredyffrin Township, Pennsylvania]]`, "Strafford" is not a 2020 place |
| Berwyn | PA | PAO: Berwyn, Daylesford | CDP. *"Daylesford station … at Glenn Avenue and Lancaster Avenue in Berwyn, Pennsylvania"* (+ Tredyffrin Twp category) |
| Devon, Paoli, Exton, Thorndale | PA | PAO (Exton also covers Whitford: *"Whitford station … South Whitford Road and Spackman Lane, Exton, Pennsylvania"*) | CDPs |
| Malvern, Downingtown | PA | PAO | boroughs |
| Bala Cynwyd | PA | CYN: Bala, Cynwyd | CDP in Lower Merion Twp |
| Conshohocken | PA | NOR: Conshohocken | borough |
| Whitemarsh | PA | NOR: Miquon, Spring Mill | **Whitemarsh Township**. *"Miquon station … in the Miquon section of Whitemarsh Township"*; *"Spring Mill is an unincorporated community in Whitemarsh Township"* |
| Norristown | PA | NOR: Norristown TC, Main Street, Elm Street | already light-rail tier |
| Jenkintown | PA | LAN/WAR/WTR: Jenkintown–Wyncote | borough |
| Elkins Park | PA | WAR/WTR: Elkins Park | CDP in Cheltenham Twp |
| Cheltenham | PA | FOX: Cheltenham; WAR/WTR: Melrose Park | **Cheltenham Township**. *"Cheltenham is an unincorporated community in Cheltenham Township"*; *"Melrose Park is an unincorporated section of Cheltenham Township"* |
| Glenside | PA | LAN/WAR: Glenside | CDP |
| Abington | PA | WAR: Crestmont, Ardsley; WTR: Noble, Rydal, Meadowbrook | **Abington Township, Montgomery County**. *"Crestmont station is a railroad station in the Crestmont section of Abington Township"*; Noble/Rydal/Meadowbrook infobox addresses all read *"Abington Township, Pennsylvania"*; *"Ardsley is an unincorporated community located in Abington Township"* |
| Roslyn, Willow Grove | PA | WAR | CDPs |
| Hatboro | PA | WAR | borough |
| Warminster | PA | WAR: Warminster | **Warminster Township**. *"Warminster station … is located in Warminster, Pennsylvania"* (line table also says "Warminster"). Conflict with the station list's "Warminster Heights" logged in §5 |
| Oreland | PA | LAN: Oreland | CDP in Springfield Twp (Montgomery) |
| Fort Washington | PA | LAN | CDP in Upper Dublin Twp |
| Ambler | PA | LAN | borough |
| Lower Gwynedd | PA | LAN: Gwynedd Valley, Penllyn | **Lower Gwynedd Township**. *"Gwynedd Valley is an unincorporated community in Lower Gwynedd Township"*; *"Penllyn station is a station situated in the village of Penllyn, Lower Gwynedd Township"* |
| North Wales | PA | LAN | borough |
| Lansdale | PA | LAN: Lansdale, 9th Street, Pennbrook | borough. *"9th Street station … at 9th Street near Shaw Avenue in Lansdale"*; Pennbrook short description *"Railway station in Lansdale, Pennsylvania"* |
| Hatfield | PA | LAN: Fortuna | **Hatfield Township**; Fortuna station article names Hatfield Township |
| Chalfont, New Britain, Doylestown | PA | LAN | Bucks County boroughs |
| Cornwells Heights, Croydon | PA | TRE | CDPs |
| Bensalem | PA | TRE: Eddington; WTR: Neshaminy Falls | **Bensalem Township**. *"Eddington station is a SEPTA Regional Rail station in the Eddington section of Bensalem Township"*; Neshaminy Falls address *"Bristol Road and Linden Street, Bensalem Township, Pennsylvania"* |
| Bristol | PA | TRE | borough |
| Tullytown | PA | TRE: "Levittown" station | borough. The Trenton Line table rowspans *"Tullytown \| Levittown / Tullytown(closed)"* |
| Trevose | PA | WTR: Trevose | CDP in Bensalem Twp |
| Lower Moreland | PA | WTR: Bethayres, Philmont | **Lower Moreland Township**. *"Bethayres is an unincorporated community in Lower Moreland Township"*; Philmont station links Lower Moreland Township |
| Langhorne Manor | PA | WTR: "Langhorne" station | borough; address *"Langhorne Manor, Pennsylvania (Langhorne address)"* |
| Woodbourne | PA | WTR: Woodbourne | CDP in Middletown Twp (Bucks) - *"a train station located on Woodbourne Road in Middletown Township"* |
| Yardley | PA | WTR | borough |
| Claymont, Wilmington, Newark | DE | WIL: Claymont; Wilmington; Newark + Churchmans Crossing | The Wilmington/Newark Line table rowspans *"Newark \| Churchmans Crossing / Newark"* |
| Trenton | NJ | TRE: Trenton Transit Center | *"Trenton, New Jersey"*, zone NJ. Overlaps the NJ agent's scope |
| Ewing | NJ | WTR: West Trenton | NJ township; "West Trenton" is not a 2020 Census place. Overlaps the NJ agent's scope |

##### MARC Train - commuter rail

| Place | State | Line: station(s) | Source |
|---|---|---|---|
| Washington | DC | Penn / Camden / Brunswick: Union Station | all three line articles (already subway tier) |
| New Carrollton, Seabrook, Bowie (Bowie State), Odenton, Middle River (Martin State Airport), Edgewood, Aberdeen, Perryville | MD | Penn | Penn Line table "Town/City" column |
| Baltimore | MD | Penn: West Baltimore, Baltimore Penn Station; Camden: Camden Station | already subway tier |
| Riverdale Park (Riverdale), College Park, Greenbelt, Beltsville (Muirkirk), Laurel (Laurel + Laurel Race Track), Savage, Jessup | MD | Camden | Camden Line table |
| Silver Spring, Kensington, Garrett Park, Rockville, Washington Grove, Gaithersburg (Gaithersburg + Metropolitan Grove), Germantown, Barnesville, Frederick (Frederick + Monocacy), Point of Rocks, Brunswick | MD | Brunswick | Brunswick Line table; Gaithersburg and Frederick each carry a `rowspan=2` covering two stations |
| Harpers Ferry, Martinsburg | WV | Brunswick | Brunswick Line table, state column "WV" |

##### Washington Metro - subway

Washington DC holds 41 stations. Suburban jurisdictions, each pinned from the station's own article because the list article gives counties only:

| Place | State | Station(s) | Quote / evidence |
|---|---|---|---|
| Bethesda | MD | Bethesda, Medical Center | *"…in Bethesda, Maryland"*; Medical Center disambig: *"a rapid transit station in Bethesda, Maryland"* |
| North Bethesda | MD | North Bethesda, Grosvenor–Strathmore | *"…in North Bethesda, Maryland"*; Grosvenor: *"area of North Bethesda"* |
| Rockville | MD | Rockville, Twinbrook | *"…the Twinbrook neighborhood of Rockville"* |
| Redland | MD | Shady Grove | *"…is a Washington Metro station in Redland, Montgomery County, Maryland"* - **not** Rockville, Derwood postal |
| Forest Glen | MD | Forest Glen | infobox `borough = Forest Glen, Maryland` |
| Silver Spring | MD | Silver Spring | `borough = Silver Spring, Maryland` |
| Wheaton | MD | Wheaton | `borough = Wheaton, Maryland` |
| Glenmont | MD | Glenmont | `borough = Glenmont, Maryland` |
| Greenbelt | MD | Greenbelt | `borough = Greenbelt, Maryland` (cites MTA Maryland station list) |
| College Park | MD | College Park–University of Maryland | *"located in College Park, Maryland"* |
| Hyattsville | MD | Hyattsville Crossing, West Hyattsville | both *"…in Hyattsville, Maryland"* |
| Cheverly | MD | Cheverly | `borough = Cheverly, Maryland` |
| Landover | MD | Landover | *"…in Landover, Maryland"* |
| New Carrollton | MD | New Carrollton | *"…just outside the city limits of New Carrollton"*; MARC Penn Line table names the place New Carrollton |
| Capitol Heights | MD | Capitol Heights, Addison Road | *"…in Capitol Heights, Maryland"*; Addison Road article links Capitol Heights |
| Summerfield | MD | Morgan Boulevard | *"…in Summerfield, Prince George's County … with a Landover postal address"* |
| Lake Arbor | MD | Downtown Largo | *"…in Lake Arbor, Prince George's County … with a Largo postal address"* - **not** the Largo CDP |
| Suitland | MD | Suitland, Branch Avenue | both *"…in Suitland, Maryland"* |
| Hillcrest Heights | MD | Naylor Road | *"…in Hillcrest Heights, Maryland"* |
| Temple Hills | MD | Southern Avenue | `borough = Temple Hills, Maryland` |
| **Arlington** | **VA** | Arlington Cemetery, Ballston–MU, Clarendon, Court House, Crystal City, East Falls Church, Pentagon, Pentagon City, Rosslyn, Virginia Square–GMU | **Arlington VA, not Arlington TX.** The 2020 Census has exactly one place in Arlington County: `Arlington CDP`, coextensive with the county |
| Alexandria | VA | King Street–Old Town, Braddock Road, Van Dorn Street, Eisenhower Avenue, Potomac Yard | independent city; Potomac Yard opened May 19, 2023 |
| Merrifield | VA | Dunn Loring | *"The station is in Merrifield, with a Vienna mailing address."* |
| Springfield | VA | Franconia–Springfield | *"…located in Springfield, Virginia"* |
| Tysons | VA | McLean, Tysons, Greensboro, Spring Hill | McLean: *"located in the unincorporated community of Tysons, with a McLean postal address"*; Greensboro/Spring Hill `borough = Tysons, Virginia` |
| Huntington | VA | Huntington | *"…in the Huntington area of Fairfax County (though its mailing address says Alexandria)"* |
| McNair | VA | Innovation Center | *"at the intersection of the SR 267 and SR 28 in McNair, near the Fairfax/Loudoun county line"* |
| Reston | VA | Wiehle–Reston East, Reston Town Center | *"…in Reston, an unincorporated area in northern Virginia"* |
| Herndon | VA | Herndon | `borough = Herndon, Virginia`; see the caveat in §3 |
| Idylwood | VA | West Falls Church | *"…in Idylwood, Virginia"* - **not** Falls Church city, and not the West Falls Church CDP |
| Ashburn | VA | Ashburn (Silver Line west terminus) | `borough = Ashburn, Virginia`, address 43655 Ashburn Metro Drive |
| Sterling | VA | Loudoun Gateway | `borough = Sterling, Virginia`, address 22505 Lockridge Road |

##### Virginia Railway Express - commuter rail

| Place | State | Line: station(s) | Source |
|---|---|---|---|
| Washington | DC | both lines: Union Station, L'Enfant | already subway tier |
| Arlington | VA | both: Crystal City. Manassas Line table row: *"Arlington \| Crystal City"* | already subway tier |
| Alexandria | VA | both: Alexandria Union Station | already subway tier |
| Springfield | VA | Manassas: Backlick Road; Fredericksburg: Franconia–Springfield | already subway tier |
| Burke | VA | Manassas: Rolling Road (and Burke Centre per the Manassas Line table) | VRE + Manassas Line |
| Burke Centre | VA | Manassas: Burke Centre | VRE article table |
| Manassas Park | VA | Manassas: Manassas Park | both tables |
| Manassas | VA | Manassas: Manassas | both tables |
| Lorton | VA | Fredericksburg: Lorton | VRE article table |
| Woodbridge | VA | Fredericksburg: Woodbridge | VRE article table |
| Quantico | VA | Fredericksburg: Quantico | VRE article table |
| Fredericksburg | VA | Fredericksburg: Fredericksburg | VRE article table |

---

#### 3. Streetcar / borderline judgements

| System | Call | Why |
|---|---|---|
| **SEPTA Metro M (Norristown High Speed Line / ex-Route 100)** - the brief did not name it, so I judged it | **light rail** | Arguments for subway: *"the line is fully grade separated, collects power from a third rail, and has high-level platforms common to rapid transit systems"*; APTA categorised it as *"Intermodal High Speed rapid rail transit"*. Arguments against: Wikipedia's own type field is **"Light metro"**, the article notes *"onboard fare collection, mostly single-car operation, and frequent stops more common to light rail systems"*, and SEPTA's 2008 budget classified it as light rail. Decisive factor: the shared spec **enumerates** which systems count as "subway" and names only SEPTA's Broad Street + Market-Frankford lines. Calling the M light rail keeps it consistent with the spec's own list. Practical effect: Bridgeport and Upper Merion are light rail rather than subway; Haverford/Radnor/Lower Merion/Norristown are light rail rather than commuter rail (highest tier wins). Source: [Norristown High Speed Line](https://en.wikipedia.org/wiki/Norristown_High_Speed_Line). |
| **SEPTA Metro T (subway-surface trolleys T1–T5)** | **light rail** | The spec explicitly rules these in: they run in the Market Street subway tunnel between 13th Street and the 36th/40th Street portals, sharing the tunnel with the L. Source: [SEPTA subway–surface trolley lines](https://en.wikipedia.org/wiki/SEPTA_subway%E2%80%93surface_trolley_lines). |
| **SEPTA Metro D (Media–Sharon Hill, ex-101/102)** | **light rail** | Interurban on *"their exclusive right of way in Upper Darby"* for ~2 mi, then private ROW through Drexel Hill and Springfield, with only short street-running segments at the Media and Aldan ends. Wikipedia types it `Light rail` and groups it with the South Shore Line and the River Line as a surviving interurban. Source: [Media–Sharon Hill Line](https://en.wikipedia.org/wiki/Media%E2%80%93Sharon_Hill_Line). |
| **SEPTA Metro G (Route 15, Girard Avenue trolley)** | **NOT counted** | Mixed street traffic on Girard Avenue for its entire length, no tunnel and no exclusive ROW - a heritage PCC line. Adds no place either way: it is wholly inside Philadelphia, which is already subway. Source: [List of SEPTA Metro stations](https://en.wikipedia.org/wiki/List_of_SEPTA_Metro_stations) (G1 stops at Broad–Girard and Front–Girard only). |
| **Baltimore Light RailLink** | **light rail** | *"Most of the light rail's route is on dedicated right-of-way that has grade crossings equipped with crossing gates."* The Howard Street downtown segment is street-running, but the system is overwhelmingly exclusive ROW at rapid-transit speed. Source: [Baltimore Light RailLink](https://en.wikipedia.org/wiki/Baltimore_Light_RailLink). |
| **Herndon VA (WMATA Herndon station)** | **included, flagged** | The station's infobox `borough = Herndon, Virginia` and it carries `[[Category:Herndon, Virginia]]`, but WMATA's own jurisdiction column says only "Fairfax County", the platform address is 12530 Sunrise Valley Drive (south of the Dulles Toll Road), and the article says the *"Town of Herndon has initiated transportation oriented development of the land on the north side of the station"* and taxes *"properties within the town boundaries"* - wording that suggests the platform itself is just outside the incorporated town. Kept because two fields in the source name Herndon, but treat it as the softest VA entry. |
| **VRE Clifton station (Clifton town VA)** | **NOT counted** | *"Clifton station is a limited-use Virginia Railway Express train station… serves as a station stop during special seasonal events in the town, most notably the town's annual Clifton Day… A temporary platform is erected for when the station is in use."* The Manassas Line article omits it from its own station list. Not usable transit access. |

---

#### 4. Deliberately excluded

| Thing | Why |
|---|---|
| **Purple Line** (MD light rail, Bethesda–New Carrollton) | Under construction, not open to passengers. |
| **Baltimore Red Line** | Planned/re-studied, no track. |
| **DC Streetcar** (H Street/Benning Road) | Mixed street traffic, no exclusive ROW - fails the spec's streetcar test. DC is already subway, so no place is lost. |
| **VRE Potomac Shores station** (Dumfries VA) | Line table row is greyed and reads *"(under development)"*. |
| **SEPTA D2 extension to Darby Transit Center**; SEPTA Trolley Modernization infill stations | Proposed only. Darby is already in via the T. |
| **VRE Clifton station / Clifton town VA** | Special-events-only seasonal stop, temporary platform (see §3). |
| **BWI Airport** Light RailLink station | Location given only as *"BWI Airport Concourse E / Anne Arundel County"* - airport land, no Census place. The MARC **BWI Rail Station** is separately excluded (Hanover, below). |
| **Washington Dulles International Airport** Metro station | `borough = Dulles, Virginia`; "Dulles" is not a 2020 Census place (Loudoun County has "Dulles Town Center CDP", a different location). |
| **Hunt Valley MD** (4 Light RailLink stations) | Unincorporated Baltimore County community; **not** in the 2020 Census place file (was a CDP in 2010). |
| **Halethorpe MD** (Light RailLink Patapsco + Baltimore Highlands; MARC Penn Halethorpe) | Same - not a 2020 Census place. Note a separate `Baltimore Highlands CDP` does exist in Baltimore County, but no source I fetched puts the platform inside it (the source says Halethorpe). |
| **Pumphrey MD** (Light RailLink Nursery Road) | Not a 2020 Census place. |
| **Hanover MD** (MARC Penn BWI Rail Station) | Penn Line table row *"Hanover \| BWI Airport"*; Hanover MD is not a 2020 Census place. |
| **Dorsey MD, St. Denis MD** (MARC Camden) | Camden Line names both; neither is a 2020 Census place. |
| **Boyds MD, Dickerson MD** (MARC Brunswick) | Named by the Brunswick Line table; neither is a 2020 Census place. |
| **Monocacy MD, Metropolitan Grove MD, Muirkirk MD, Laurel Race Track** | Station names only - the line tables place them in Frederick, Gaithersburg, Beltsville and Laurel respectively, all of which ARE in the output. |
| **Christiana DE** (Churchmans Crossing) | The SEPTA station list says "Christiana, Delaware", but the Wilmington/Newark Line table puts Churchmans Crossing in **Newark**, and Christiana is not a 2020 Census place. Newark DE is in the output. |
| **Trainer PA** (Wilmington/Newark Line) | Station closed March 26, 1978 (*"SEPTA discontinues station stops at Trainer and Naaman on Wilmington Line"*). |
| **Penndel PA** (West Trenton Line) | Named in the line table but has no station in the station list - the row is a closed stop. |
| **North Hills PA** (Lansdale/Doylestown, North Hills station) | *"North Hills is an unincorporated community in Abington, Springfield, and Upper Dublin"* townships - three candidate townships, no CDP, no source pinning the platform. Could not verify. |
| **Colmar PA / Link Belt PA** (Lansdale/Doylestown) | *"Colmar … located in Hatfield and Montgomery Township"* - straddles two townships, not a Census place, platform not pinned. Hatfield Township IS in the output via Fortuna station. |
| **Wyndmoor PA / Wyndmoor CDP** (Chestnut Hill East, Wyndmoor station) | Both sources put this station in Philadelphia, not in the Montgomery County CDP: *"Wyndmoor station is a SEPTA Regional Rail station at 256 East Willow Grove Avenue at Wyndmoor Street in the Chestnut Hill region of Philadelphia"*; the station list's Location column also reads "Philadelphia (Chestnut Hill)". |
| **Doylestown Township PA** (Delaware Valley University station) | Station list says "Doylestown Township"; that is a separate MCD from Doylestown borough but shares the name, so emitting it would duplicate the borough row. Logged instead. |
| **Warminster Heights PA** | The SEPTA station list names this CDP, but the Warminster Line table and the station article both say "Warminster". Warminster Township is emitted instead (see §5). |
| **Takoma Park MD** | No Metro station. The WMATA "Takoma" station's jurisdiction is District of Columbia. |
| **Chevy Chase MD / Friendship Heights Village CDP** | Friendship Heights station *"straddl[es] the border of Washington, D.C., and Montgomery County, Maryland"*, but its infobox `borough = Washington, D.C.` and the list article's jurisdiction column says District of Columbia. No source pins a Maryland place, so no MD place claimed. |
| **Oxon Hill / National Harbor MD, Forestville MD, Largo CDP MD** | No WMATA station in any of them. Branch Avenue is in Suitland, Downtown Largo is in Lake Arbor, and there is no Oxon Hill/National Harbor station at all. |
| **Vienna VA (town) and Fairfax VA (city)** | The Metro "Vienna/Fairfax-GMU" station *"is in the median"* of I-66 in unincorporated Fairfax County and merely *"provides easy access to the nearby Town of Vienna, the City of Fairfax"*. Neither incorporated place contains a station, and no CDP is named for the platform. |
| **Falls Church city VA** | The "West Falls Church" and "East Falls Church" stations are in Idylwood CDP and Arlington County respectively; neither is in the independent city. |
| **Franconia VA** | Franconia CDP exists, but the Franconia–Springfield station article says *"located in Springfield, Virginia"*. Springfield CDP is emitted. |
| **Bristow VA** (VRE Broad Run) | Named by both VRE tables but not a 2020 Census place (was a CDP in 2010). |
| **Featherstone VA** (VRE Rippon) | VRE table row *"Featherstone \| Rippon"*; not a 2020 Census place. |
| **Brooke VA, Leeland VA** (VRE Brooke, Leeland Road) | Stafford County unincorporated communities; neither is a 2020 Census place. |
| **Olive VA** (VRE Spotsylvania) | VRE table row *"Olive \| Spotsylvania"*; not a 2020 Census place. Spotsylvania Courthouse CDP is a different location and no source pins the platform there. |
| **Duffields WV** (MARC Brunswick) | Jefferson County unincorporated; not a 2020 Census place. |
| Amtrak-only stations on shared track (Coatesville, Parkesburg, Edgemoor, Naaman, Morrisville, Andalusia) | Either Amtrak-only or closed SEPTA stops. |

---

#### 5. Conflicting sources resolved

| Station | Source A | Source B | Call |
|---|---|---|---|
| SEPTA **Media** (Media/Wawa Line) | Station list: **Upper Providence Township** (cites a Delaware County Planning Dept report) | Media/Wawa Line table: **Media** | Emitted **Upper Providence** (the station article's lead also says Upper Providence Township, and it cites an Upper Providence map). Media borough is in the dataset anyway via the D1 trolley. |
| SEPTA **Wawa** | Station list: "Wawa" (not a Census place) | Media/Wawa Line table: **Chester Heights** | Emitted **Middletown** township - the station article says it twice: *"located adjacent to U.S. Route 1 in Middletown Township, Delaware County"* and *"briefly referred to as 'Middletown' for its location in Middletown Township"*. |
| SEPTA **Warminster** | Station list: **Warminster Heights** CDP | Line table + station article: **Warminster** | Emitted **Warminster** (township). Warminster Heights CDP lies inside Warminster Township, so the township is the claim both sources support. |
| SEPTA **Churchmans Crossing** | Station list: **Christiana DE** | Wilmington/Newark Line table: **Newark DE** | Emitted **Newark** - Christiana is not a 2020 Census place. |
| SEPTA **Burke Centre** (VRE) | VRE article: **Burke Centre** | Manassas Line article: **Burke** | Emitted **both** CDPs; each is a real 2020 place and Rolling Road independently anchors Burke. |
| SEPTA **Fernwood–Yeadon** | Station list: "Upper Darby/Yeadon" | Media/Wawa Line table: **Yeadon** | Both places already in the dataset. |
| SEPTA **Levittown** | Station list: **Tullytown** | Trenton Line table rowspan: **Tullytown** | Agreed - Tullytown, not the Levittown CDP. |
| WMATA **Crestmont** (MARC/SEPTA analogue: Crestmont station, Warminster Line) | Line table: **Abington Township** | Station list: "Crestmont" | Emitted **Abington**; the station article says *"the Crestmont section of Abington Township, Montgomery County"*. |
| WMATA **New Carrollton** | Station article: *"just outside the city limits of New Carrollton"* | MARC Penn Line table: **New Carrollton** | Emitted **New Carrollton** with the caveat recorded in `cdp_notes`. |

---

#### 6. Sourcing limitations

| Official site | Result | Fallback |
|---|---|---|
| `https://www.septa.org/rail/` | HTTP 200 but only ~9.8 KB - a JS/redirect shell with no station data | Wikipedia station-list articles (the SEPTA Regional Rail list is a Featured List with a sourced Location column citing SEPTA's own street & transit maps) |
| `https://www.ridepatco.org/stations/` | **HTTP 200, served fine (19.5 KB)** | Used it - confirmed the 14-station roster incl. Franklin Square, Ferry Avenue, Broadway (WRTC) |
| `https://www.mta.maryland.gov/schedule/lightrail` | **HTTP 200, served fine (1.1 MB)** | Wikipedia's list article was used for the station->community mapping because it carries the community names explicitly |
| `https://www.wmata.com/rider-guide/stations/` | HTTP 301 -> redirected to `https://www.wmata.com/ridertools`, which does not carry the per-station jurisdiction table | 43 individual Wikipedia station articles (lead sentence + infobox `borough`); the list article's jurisdiction column is county-level only and is not sufficient |
| `https://www.vre.org/service/stations/` | **HTTP 403 - blocked scripted fetches** | Wikipedia VRE + Manassas Line articles, both of which have a "Location" column |

Other limitations:
- The **2020 Census place file dropped many former CDPs** in PA (Wynnewood, Havertown, Secane, Wallingford, Crum Lynne, Radnor, Haverford, Strafford, Gwynedd Valley, Ardsley, Melrose Park, Noble, Rydal, Meadowbrook, Bethayres, Colmar, North Hills, Elwyn, Wawa, Primos, Fortuna, Spring Mill, Miquon, Daylesford) and in MD/VA (Hunt Valley, Halethorpe, Pumphrey, Hanover, Bristow, Featherstone). For PA I fell back to the township, which the shared spec permits; for MD/VA/WV/DE there is no township fallback, so those stations are logged in §4 instead of guessed at.
- Several PA place names in the output are **township names that repeat across counties** - `Middletown` (Delaware Co), `Springfield` (Delaware Co, light rail; distinct from Springfield Twp Montgomery), `Radnor`, `Haverford`, `Warminster`, `Abington`, `Bensalem`. Each carries the county in `cdp_notes`.
- `Trenton NJ` and `Ewing NJ` are inside the New Jersey agent's scope too and will need de-duplication at merge.

---

#### 7. 2025-2026 changes caught

1. **SEPTA Metro renaming took effect in 2025.** The station list marks dozens of stations *"Formerly known as … (2025)"*: Routes 10/34/13/11/36 became **T1–T5**, Routes 101/102 became **D1/D2**, Route 100 / Norristown High Speed Line became **M**, the Broad Street Line became **B** and the Market-Frankford Line became **L**. Station renames in the same wave include Allegheny -> Broad–Allegheny and Kensington–Allegheny, Girard -> Broad–Girard and Front–Girard, Spring Garden -> Broad–Spring Garden, 36th Street -> 36th–Sansom, Springfield Road -> Brookside–Springfield and Springfield–Madison, Sharon Hill -> Chester Pike/Sharon Hill, Providence Road -> Providence Road/Media, 30th Street -> Drexel Station at 30th Street (2024).
2. **SEPTA T trolley tunnel is closed.** New 4-inch trolley-pole sliders installed in Fall 2025 damaged overhead infrastructure, causing passenger evacuations on Oct 14 and Oct 22, 2025. *"Service was suspended on November 7th, and is expected to continue until January 2026"*; shuttle buses began Dec 15, 2025 (SEPTA news + CBS Philadelphia, Dec 17 2025). The T places (Philadelphia, Yeadon, Darby) are still in the dataset - this is a temporary tunnel closure with bus substitution, not a line abandonment, and Philadelphia/Darby/Yeadon all hold their tier from other rail anyway.
3. **PATCO Franklin Square station reopened in 2025**, after being closed since 1979 (a $29.3M renovation begun in 2022). It is on the official 14-station list at ridepatco.org. Philadelphia already held the subway tier.
4. **PATCO weekday overnight service is temporarily suspended from September 2025 to August 2026** (PATCO news release, "Overnight Weekday Pilot Extended Through August 2026").
5. **Baltimore Metro SubwayLink is replacing its whole fleet.** The first Hitachi trainset made its ceremonial first run at Rogers Avenue station on **January 7, 2026**; replacement of the 1983 Budd Universal Transit Vehicles runs in phases *"from 2026 to 2027"*.
6. **Confirmed (older but explicitly checked as instructed): Silver Line Phase 2 to Ashburn opened November 15, 2022.** Three station articles independently date it: Ashburn (*"The station's platform on opening day, November 15, 2022"*), Herndon (*"opened on November 15, 2022"*) and Washington Dulles International Airport (*"platform on opening day, November 15, 2022"*). Loudoun Gateway's photo caption is dated November 2022. So the 6 Phase 2 stations - Reston Town Center, Herndon, Innovation Center, Dulles Airport, Loudoun Gateway, Ashburn - are open and counted (Dulles Airport excluded only for lack of a Census place).
7. Also noted: WMATA **Hyattsville Crossing** is the renamed Prince George's Plaza; **Potomac Yard** (Alexandria) opened May 19, 2023; SEPTA **Wawa Station** reopened August 21, 2022 after being closed since 1986.

### 2.5 Chicago region

Scope: Chicago "L" (CTA), Metra, South Shore Line (NICTD). Everything below was read as
Wikipedia wikitext through `fetch.sh` (cached under `scratchpad/wiki/`) plus one live pull
of the official NICTD stations page. **128 Census places** total: 8 subway, 120 commuter rail.

#### Systems covered

| System | Type assigned | Source URL(s) | How station -> city was established |
|---|---|---|---|
| Chicago "L" (CTA) | `subway` (heavy rail rapid transit, per brief) | https://en.wikipedia.org/wiki/List_of_Chicago_%22L%22_stations ; https://en.wikipedia.org/wiki/Chicago_%22L%22 | The station table's **Location** column carries a Chicago community area for city stations and a suburb link for suburban ones. Every suburb was then re-checked against its own station article. The list article states the system "serves the [[Chicago\|city of Chicago]] and seven of its surrounding suburbs" - I found exactly 7 suburbs, which is the cross-check. |
| Metra | `commuter rail` | https://en.wikipedia.org/wiki/List_of_Metra_stations + all 11 line articles (BNSF Line, Heritage Corridor (Metra), Metra Electric, Milwaukee District North Line, Milwaukee District West Line, North Central Service, Rock Island District, SouthWest Service, Union Pacific North Line, Union Pacific Northwest Line, Union Pacific West Line) | `List of Metra stations` has an explicit **Location** column, documented in its own Key section as "The municipality or Chicago neighborhood in which the station is located". I parsed all 243 active rows out of the wikitext, then re-derived the municipality independently from each line article's own rowspanned Location column and diffed **both directions**. Line-article municipalities absent from the master list were all **closed** stations (the line articles shade closed rows `bgcolor=dfdfdf`). The reverse diff - master-list municipalities absent from the line article that is supposed to serve them - returned exactly **one** hit across 243 stations: Park Forest / 211th Street, resolved against the station article and excluded. |
| South Shore Line (NICTD) | `commuter rail` | https://en.wikipedia.org/wiki/South_Shore_Line ; https://en.wikipedia.org/wiki/Lakeshore_Corridor ; https://en.wikipedia.org/wiki/Monon_Corridor ; https://mysouthshoreline.com/plan-your-trip/stations-map/ | Corridor articles carry a Location column; the official NICTD stations page gave a street address per station and an authoritative list of the 21 stations currently open. Ambiguous ones (Dune Park, Portage/Ogden Dunes, Munster/Dyer, Hudson Lake) were settled against the individual station article **and** the municipality article. |

#### Place-by-place

##### Chicago "L" - 8 places, all IL (`subway`)

The "L" runs entirely within Illinois. Only these municipalities physically contain a station:

| Place | State | System | Station(s) | Source URL |
|---|---|---|---|---|
| Chicago | IL | Chicago "L" (all 8 lines) | ~130 stations incl. O'Hare, Midway, Howard, 95th/Dan Ryan | https://en.wikipedia.org/wiki/List_of_Chicago_%22L%22_stations |
| Cicero | IL | Chicago "L" (Pink) | 54th/Cermak (terminal), Cicero (Pink) | https://en.wikipedia.org/wiki/54th/Cermak_station - "located at [[Cermak Road]] between 54th and Laramie Avenues in [[Cicero, Illinois]]" |
| Evanston | IL | Chicago "L" (Purple) | Central, Davis, Dempster, Foster, Main, Noyes, South Boulevard | https://en.wikipedia.org/wiki/List_of_Chicago_%22L%22_stations (7 rows, Location = Evanston, Illinois) |
| Forest Park | IL | Chicago "L" (Blue) | Forest Park (terminal), Harlem (Forest Park branch) | https://en.wikipedia.org/wiki/Forest_Park_station - "located in the village of [[Forest Park, Illinois]]"; https://en.wikipedia.org/wiki/Harlem_station_(CTA_Blue_Line_Forest_Park_branch) - "serving the [[Blue Line (CTA)\|Blue Line]]'s Forest Park branch in [[Forest Park, Illinois]]" |
| Oak Park | IL | Chicago "L" (Green, Blue) | Harlem/Lake (terminal), Oak Park (Green), Oak Park (Blue), Ridgeland, Austin (Green) | https://en.wikipedia.org/wiki/Harlem/Lake_station - "located between the [[Oak Park, Illinois\|Oak Park]] and [[Forest Park, Illinois\|Forest Park]] boundary line at Harlem Avenue" |
| Rosemont | IL | Chicago "L" (Blue) | Rosemont | https://en.wikipedia.org/wiki/Rosemont_station_(CTA) - "at the intersection of River Road and I-190 in the suburb of [[Rosemont, Illinois]]" |
| Skokie | IL | Chicago "L" (Yellow) | Dempster-Skokie (terminal), Oakton-Skokie | https://en.wikipedia.org/wiki/Dempster%E2%80%93Skokie_station - "at 5005 [[Dempster Street]] in [[Skokie, Illinois]]" |
| Wilmette | IL | Chicago "L" (Purple) | Linden (terminal) | https://en.wikipedia.org/wiki/Linden_station_(CTA) - "The station is located at 349 Linden Avenue in [[Wilmette, Illinois]]" |

Trap checks done on the "L":
- **Berwyn, IL is NOT on the "L".** The Red Line's `Berwyn` station "is located at 1121 West Berwyn Avenue in the [[Edgewater, Chicago\|Edgewater]]" community area of Chicago and "is named for the [[Berwyn (SEPTA station)\|Berwyn station]]" in Pennsylvania. Separately, 54th/Cermak "was previously known as the Cicero-Berwyn Terminal, it is located about 1 mi from the city of [[Berwyn, Illinois]]" - 1 mile away is not in it. (Berwyn IS in the dataset, but for **Metra**.)
- **Des Plaines, IL is NOT on the "L".** Rosemont station "is located only 1 mile from the [[Des Plaines, Illinois\|City of Des Plaines]] at its westernmost border" and "handles more suburban commuters from Des Plaines than any other suburb" - still 1 mile outside. (Des Plaines IS in the dataset, for **Metra** UP-NW.)
- **Elmwood Park, IL is NOT on the "L"** - no Location cell in the station table names it. (It is in the dataset for **Metra** MD-W.)
- Three different stations are called `Harlem`, in three different places: Norwood Park **Chicago** (Blue/O'Hare), **Forest Park** (Blue/Forest Park), and `Harlem/Lake` in **Oak Park** (Green). Two different stations are called `Cicero`: Austin **Chicago** (Blue and Green, named for Cicero Avenue) and **Cicero, IL** (Pink).
- `Austin` (Green Line) is the one genuine conflict inside Wikipedia: the station list's Location column says Oak Park, while the station article says it "is located ... in the [[Austin, Chicago\|Austin neighborhood]] on [[Chicago]]'s West Side and borders the village of [[Oak Park, Illinois\|Oak Park]]". Immaterial to the output - Oak Park qualifies on four other stations.

##### Metra - 118 rows below (117 IL + 1 WI); 111 emitted as `commuter rail` in the JSON

Six Metra municipalities (Chicago, Cicero, Evanston, Oak Park, Rosemont, Wilmette) also have "L" stations,
so they are emitted once at the higher `subway` tier per the spec. One row below - **Park Forest** - is
listed for completeness but is **NOT emitted**; see Deliberately excluded. 118 - 6 - 1 = 111.

| Place | State | System (lines) | Station(s) | Source URL |
|---|---|---|---|---|
| Antioch | IL | Metra (NCS) | Antioch | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Arlington Heights | IL | Metra (UP-NW) | Arlington Heights, Arlington Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Aurora | IL | Metra (BNSF) | Route 59, [[Aurora Transportation Center|Aurora]] | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Barrington | IL | Metra (UP-NW) | Barrington | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Bartlett | IL | Metra (MD-W) | Bartlett | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Bellwood | IL | Metra (UP-W) | Bellwood | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Bensenville | IL | Metra (MD-W) | Bensenville | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Berkeley | IL | Metra (UP-W) | Berkeley | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Berwyn | IL | Metra (BNSF) | Berwyn, Harlem Avenue, LaVergne | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Blue Island | IL | Metra (ME/RI) | 119th Street, 123rd Street, Blue Island, Blue Island/Vermont Street, Prairie Street | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Brookfield | IL | Metra (BNSF) | Brookfield, Congress Park, Hollywood | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Buffalo Grove | IL | Metra (NCS) | Buffalo Grove | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Calumet Park | IL | Metra (ME) | Ashland/Calumet Park, Burr Oak | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Cary | IL | Metra (UP-NW) | Cary | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Chicago | IL | Metra (BNSF/HC/ME/MD-N/MD-W/NCS/RI/SWS/UP-N/UP-NW/UP-W) | 103rd Street/Beverly Hills, 103rd Street/Rosemoor, 103rd Street/Washington Heights, 107th Street, 107th Street/Beverly Hills, 111th Street/Morgan P... | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Chicago Ridge | IL | Metra (SWS) | Chicago Ridge | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/SouthWest_Service |
| Cicero | IL | Metra (BNSF) | Cicero | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Clarendon Hills | IL | Metra (BNSF) | Clarendon Hills | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Crystal Lake | IL | Metra (UP-NW) | Crystal Lake, Pingree Road | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Deerfield | IL | Metra (MD-N) | Deerfield, Lake Cook Road | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Des Plaines | IL | Metra (UP-NW) | Cumberland, Des Plaines | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Downers Grove | IL | Metra (BNSF) | Belmont, Fairview Avenue/Downers Grove, Main Street/Downers Grove | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| East Hazel Crest | IL | Metra (ME) | Calumet | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Elburn | IL | Metra (UP-W) | Elburn | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Elgin | IL | Metra (MD-W) | Big Timber Road/Elgin, Elgin, National Street/Elgin | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Elmhurst | IL | Metra (UP-W) | Elmhurst | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Elmwood Park | IL | Metra (MD-W) | Elmwood Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Evanston | IL | Metra (UP-N) | Central Street/Evanston, Davis Street/Evanston, Main Street/Evanston | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Flossmoor | IL | Metra (ME) | Flossmoor | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Fox Lake | IL | Metra (MD-N) | Fox Lake | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Fox River Grove | IL | Metra (UP-NW) | Fox River Grove | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Franklin Park | IL | Metra (MD-W/NCS) | Belmont Avenue/Franklin Park, Franklin Park, Mannheim | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Geneva | IL | Metra (UP-W) | Geneva | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Glen Ellyn | IL | Metra (UP-W) | Glen Ellyn | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Glencoe | IL | Metra (UP-N) | Glencoe | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Glenview | IL | Metra (MD-N) | Glenview, The Glen/North Glenview | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Golf | IL | Metra (MD-N) | Golf | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Grayslake | IL | Metra (MD-N/NCS) | Grayslake, Washington Street/Grayslake | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Hanover Park | IL | Metra (MD-W) | Hanover Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Harvard | IL | Metra (UP-NW) | Harvard | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Harvey | IL | Metra (ME) | 147th Street/Sibley, Harvey | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Hazel Crest | IL | Metra (ME) | Hazel Crest | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Highland Park | IL | Metra (UP-N) | Braeside, Highland Park, Ravinia, Ravinia Park  (Seasonal) | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Highwood | IL | Metra (UP-N) | Fort Sheridan, Highwood | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Hinsdale | IL | Metra (BNSF) | Highlands, Hinsdale, West Hinsdale | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Homewood | IL | Metra (ME) | Homewood | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Itasca | IL | Metra (MD-W) | Itasca | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Joliet | IL | Metra (HC/RI) | [[Joliet Gateway Center|Joliet]] | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Heritage_Corridor_(Metra) |
| Kenilworth | IL | Metra (UP-N) | Kenilworth | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| La Grange | IL | Metra (BNSF) | LaGrange Road, Stone Avenue | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Lake Bluff | IL | Metra (UP-N) | Lake Bluff | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Lake Forest | IL | Metra (MD-N/UP-N) | Lake Forest, Lake Forest | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Lake Villa | IL | Metra (NCS) | Lake Villa | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Lemont | IL | Metra (HC) | Lemont | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Heritage_Corridor_(Metra) |
| Libertyville | IL | Metra (MD-N/NCS) | Libertyville, Prairie Crossing, Prairie Crossing | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Lisle | IL | Metra (BNSF) | Lisle | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Lockport | IL | Metra (HC) | Lockport | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Heritage_Corridor_(Metra) |
| Lombard | IL | Metra (UP-W) | Lombard | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Long Lake | IL | Metra (MD-N) | Long Lake | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Manhattan | IL | Metra (SWS) | Manhattan | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/SouthWest_Service |
| Matteson | IL | Metra (ME) | Matteson | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Maywood | IL | Metra (UP-W) | Maywood | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| McHenry | IL | Metra (UP-NW) | McHenry | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Melrose Park | IL | Metra (UP-W) | Melrose Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Midlothian | IL | Metra (RI) | Midlothian | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Rock_Island_District |
| Mokena | IL | Metra (RI) | Hickory Creek, Mokena | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Rock_Island_District |
| Morton Grove | IL | Metra (MD-N) | Morton Grove | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Mount Prospect | IL | Metra (UP-NW) | Mount Prospect | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Mundelein | IL | Metra (NCS) | Mundelein | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Naperville | IL | Metra (BNSF) | Naperville | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| New Lenox | IL | Metra (RI/SWS) | Laraway Road, New Lenox | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Rock_Island_District |
| North Chicago | IL | Metra (UP-N) | Great Lakes, North Chicago | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Northbrook | IL | Metra (MD-N) | Northbrook | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Oak Forest | IL | Metra (RI) | Oak Forest | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Rock_Island_District |
| Oak Lawn | IL | Metra (SWS) | Oak Lawn Patriot | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/SouthWest_Service |
| Oak Park | IL | Metra (UP-W) | Oak Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Olympia Fields | IL | Metra (ME) | Olympia Fields | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Orland Park | IL | Metra (SWS) | 143rd Street/Orland Park, 153rd Street/Orland Park, 179th Street/Orland Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/SouthWest_Service |
| Palatine | IL | Metra (UP-NW) | Palatine | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Palos Heights | IL | Metra (SWS) | Palos Heights | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/SouthWest_Service |
| Palos Park | IL | Metra (SWS) | Palos Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/SouthWest_Service |
| ~~Park Forest~~ (EXCLUDED) | IL | Metra (ME) | 211th Street/Lincoln Highway | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric ; https://en.wikipedia.org/wiki/211th_Street/Lincoln_Highway_station |
| Park Ridge | IL | Metra (UP-NW) | Dee Road, Park Ridge | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Prospect Heights | IL | Metra (NCS) | Prospect Heights | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Richton Park | IL | Metra (ME) | Richton Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| River Forest | IL | Metra (UP-W) | River Forest | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| River Grove | IL | Metra (MD-W/NCS) | River Grove | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Riverdale | IL | Metra (ME) | Ivanhoe, Riverdale | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Riverside | IL | Metra (BNSF) | Riverside | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Robbins | IL | Metra (RI) | Robbins | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Rock_Island_District |
| Romeoville | IL | Metra (HC) | Romeoville | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Heritage_Corridor_(Metra) |
| Roselle | IL | Metra (MD-W) | Roselle | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Rosemont | IL | Metra (NCS) | Rosemont | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Round Lake | IL | Metra (MD-N) | Round Lake | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_North_Line |
| Round Lake Beach | IL | Metra (NCS) | Round Lake Beach | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Schaumburg | IL | Metra (MD-W) | Schaumburg | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Schiller Park | IL | Metra (NCS) | Schiller Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Summit | IL | Metra (HC) | Summit | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Heritage_Corridor_(Metra) |
| Tinley Park | IL | Metra (RI) | 80th Avenue/Tinley Park, Tinley Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Rock_Island_District |
| University Park | IL | Metra (ME) | University Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Metra_Electric |
| Vernon Hills | IL | Metra (NCS) | Vernon Hills | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Villa Park | IL | Metra (UP-W) | Villa Park | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Waukegan | IL | Metra (UP-N) | Waukegan | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| West Chicago | IL | Metra (UP-W) | West Chicago | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Western Springs | IL | Metra (BNSF) | Western Springs | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Westmont | IL | Metra (BNSF) | Westmont | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/BNSF_Line |
| Wheaton | IL | Metra (UP-W) | College Avenue, Wheaton | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Wheeling | IL | Metra (NCS) | Wheeling | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/North_Central_Service |
| Willow Springs | IL | Metra (HC) | Willow Springs | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Heritage_Corridor_(Metra) |
| Wilmette | IL | Metra (UP-N) | Wilmette | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Winfield | IL | Metra (UP-W) | Winfield | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_West_Line |
| Winnetka | IL | Metra (UP-N) | Hubbard Woods, Indian Hill, Winnetka | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Winthrop Harbor | IL | Metra (UP-N) | Winthrop Harbor | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Wood Dale | IL | Metra (MD-W) | Wood Dale | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Milwaukee_District_West_Line |
| Woodstock | IL | Metra (UP-NW) | Woodstock | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_Northwest_Line |
| Worth | IL | Metra (SWS) | Worth | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/SouthWest_Service |
| Zion | IL | Metra (UP-N) | Zion | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |
| Kenosha | WI | Metra (UP-N) | Kenosha | https://en.wikipedia.org/wiki/List_of_Metra_stations ; https://en.wikipedia.org/wiki/Union_Pacific_North_Line |

Metra trap checks, each verified in two independent articles:

| Trap | Ruling | Evidence |
|---|---|---|
| Ravinia, Ravinia Park, Braeside | **Highland Park** | `List of Metra stations` groups all four (with Highland Park) under `[[Highland Park, Illinois]]`; UP-N line article has `rowspan="4" \| [[Highland Park, Illinois\|Highland Park]]` over Highland Park / Ravinia / Ravinia Park / Braeside. Ravinia Park is marked *Seasonal*. |
| Rondout | **excluded - station is closed** | MD-N: "Until 1984, there was a stop in Rondout. The station building itself was demolished in the mid-1960s." Its row is shaded closed and it is absent from `List of Metra stations`. Rondout survives only as a junction/dispatch point. |
| Prairie Crossing (two stations) | **Libertyville**, not Grayslake | `Prairie Crossing station`: "is a pair of [[Metra]] stations located in [[Libertyville, Illinois]]"; MD-N line article: `rowspan="2"\|[[Libertyville, Illinois\|Libertyville]]` over Prairie Crossing (MD-N) and Libertyville. Grayslake is in the dataset anyway on its own two stations (Grayslake, Washington Street/Grayslake). |
| Big Timber Road, National Street | **Elgin** | Three Elgin rows in `List of Metra stations`: Big Timber Road/Elgin, Elgin, National Street/Elgin, all Location = `[[Elgin, Illinois]]`. |
| Route 59 | **Aurora / Naperville border** - both already qualify | `Route 59 station`: "a [[Metra]] station along the [[BNSF Line]] on the border of [[Aurora, Illinois]], and [[Naperville, Illinois]]"; BNSF line article Location cell reads `[[Naperville, Illinois\|Naperville]]/[[Aurora, Illinois\|Aurora]]`. Both cities also have their own eponymous stations. |
| Fairview Avenue | **Downers Grove** | BNSF: `rowspan=3\|[[Downers Grove, Illinois\|Downers Grove]]` over Fairview Avenue/Downers Grove, Main Street/Downers Grove, Belmont. |
| Highlands, Hinsdale, West Hinsdale | **Hinsdale** (all three) | BNSF: `rowspan=3\|[[Hinsdale, Illinois\|Hinsdale]]` over Highlands, Hinsdale, West Hinsdale. |
| Congress Park | **Brookfield**, not La Grange | BNSF: `rowspan=3\|[[Brookfield, Illinois\|Brookfield]]` over Hollywood, Brookfield, Congress Park. La Grange is separately in the dataset for LaGrange Road + Stone Avenue. |
| Riverside | **Riverside** | BNSF single-station row `[[Riverside, Illinois\|Riverside]]`. |
| Harlem Avenue | **Berwyn** - and there is only **one** active Metra `Harlem Avenue` | BNSF: `rowspan=3\|[[Berwyn, Illinois\|Berwyn]]` over LaVergne, Berwyn, Harlem Avenue. No other line has an active station of that name. (The three *"L"* Harlem stations are a separate matter, above.) |
| Kensington / 115th Street | **Chicago** | `List of Metra stations` Location = `[[Kensington, Chicago]]` (a Chicago community). On the South Shore Line, "Kensington/115th Street - South Shore service withdrawn February 15, 2012". |
| Blue Island | **Blue Island** - five stations, not two | `List of Metra stations` puts 119th Street, 123rd Street, Blue Island, Blue Island/Vermont Street and Prairie Street all in `[[Blue Island, Illinois]]` (Rock Island Beverly branch + Metra Electric Blue Island branch). |
| Hazel Crest / Homewood / Flossmoor / Olympia Fields / Matteson / Richton Park / University Park | **all confirmed, all Metra Electric main line** | Metra Electric line article Location column; `East Hazel Crest` is a *separate* village and holds the `Calumet` station. |
| Antioch, Fox Lake, Kenosha WI | **all confirmed** | Antioch = NCS outer terminal; Fox Lake = MD-N outer terminal; Kenosha = UP-N outer terminal, Location `[[Kenosha, Wisconsin\|Kenosha, WI]]`, the only non-Illinois Metra place. |
| Great Lakes | **North Chicago** | UP-N: `rowspan="3"\|[[North Chicago, Illinois\|North Chicago]]` over Abbott's Platform (closed), North Chicago, Great Lakes. |
| Fort Sheridan | **Highwood** | UP-N: `rowspan="2"\|[[Highwood, Illinois\|Highwood]]` over Fort Sheridan and Highwood. |
| Lake Cook Road | **Deerfield** | MD-N: `rowspan=2\|[[Deerfield, Illinois\|Deerfield]]` over Deerfield and Lake Cook Road. |
| Two stations both named `Lake Forest` | **Lake Forest** (MD-N one "Formerly named Everett", UP-N one) | `List of Metra stations` rows `{{stl\|Metra\|Lake Forest\|mdn}}` and `{{stl\|Metra\|Lake Forest\|upn}}`, both Location `[[Lake Forest, Illinois]]`. |

##### South Shore Line (NICTD) - 10 places (Chicago IL counted at the subway tier)

Official NICTD list of open stations (21), fetched live: Millennium Station, Van Buren St., Museum Campus/11 St.,
57th St., 63rd St., Hegewisch, Hammond Gateway, South Hammond, Munster Ridge, Munster/Dyer, East Chicago,
Gary/Chicago Airport, Gary Metro Center, Miller, Portage/Ogden Dunes, Dune Park, Beverly Shores, 11th Street,
Carroll Ave., Hudson Lake, South Bend International Airport.

| Place | State | System | Station(s) | Source URL |
|---|---|---|---|---|
| Chicago | IL | South Shore Line (emitted as `subway` for the "L") | Millennium Station, Van Buren Street, Museum Campus/11th Street, 57th Street, 63rd Street, Hegewisch (+ McCormick Place, special events only) | https://en.wikipedia.org/wiki/Lakeshore_Corridor - `rowspan="15" \| [[Chicago\|Chicago, IL]]`; NICTD gives "13730 South Brainard Ave., Chicago" for Hegewisch |
| Hammond | IN | South Shore Line | Hammond Gateway, South Hammond | https://en.wikipedia.org/wiki/Hammond_Gateway_station - "is a [[South Shore Line]] station in [[Hammond, Indiana]]"; https://en.wikipedia.org/wiki/South_Hammond_station - "is a [[South Shore Line]] [[rail station]] in [[Hammond, Indiana]]" |
| Munster | IN | South Shore Line | Munster Ridge, Munster/Dyer (terminal) | https://en.wikipedia.org/wiki/Munster_Ridge_station - "is a [[South Shore Line]] [[rail station]] in [[Munster, Indiana]]"; https://en.wikipedia.org/wiki/Munster/Dyer_station |
| East Chicago | IN | South Shore Line | East Chicago | https://en.wikipedia.org/wiki/Lakeshore_Corridor - `rowspan="3" \|[[East Chicago, Indiana\|East Chicago]]` |
| Gary | IN | South Shore Line | Gary/Chicago Airport (Clark Road), Gary Metro Center, Miller | https://en.wikipedia.org/wiki/Gary/Chicago_Airport_station - "located in the Brunswick neighborhood of [[Gary, Indiana]]"; NICTD: "200 West 4th Ave., Gary" and "760 S. Lake Street, Gary, Indiana" |
| Ogden Dunes | IN | South Shore Line | Portage/Ogden Dunes | https://en.wikipedia.org/wiki/Ogden_Dunes,_Indiana - "The town is the site of the [[Portage / Ogden Dunes (NICTD)\|Portage / Ogden Dunes]] station"; station infobox address "U.S. Highway 12 and Hillcrest Road, [[Ogden Dunes, Indiana]]" |
| Beverly Shores | IN | South Shore Line | Beverly Shores (flag stop) | https://en.wikipedia.org/wiki/Beverly_Shores_station - "is a [[train station]] in [[Beverly Shores, Indiana]]" |
| Michigan City | IN | South Shore Line | 11th Street, Carroll Avenue | NICTD: "114 E 11th Street, Michigan City" and "503 North Carroll Avenue, Michigan City" |
| Hudson Lake | IN | South Shore Line | Hudson Lake (flag stop) | https://en.wikipedia.org/wiki/Hudson_Lake_station - "a train stop operated by the [[South Shore Line]] in the unincorporated community of [[Hudson Lake, Indiana]]" (a 2020 CDP) |
| South Bend | IN | South Shore Line | South Bend Airport (eastern terminus) | https://en.wikipedia.org/wiki/South_Bend_Airport_station - infobox address "4485 Progress Drive, [[South Bend, Indiana]]" |

#### Streetcar / borderline judgements

| System | Call | Why |
|---|---|---|
| Chicago streetcar network | **n/a - none exists** | The CTA "was created in 1947 to take over and save the rapid transit and **streetcar** systems"; Chicago's streetcars are long gone and there is no modern replacement. No streetcar or light rail line operates anywhere in the Chicago region, so nothing in this region is typed `light rail`. Source: https://en.wikipedia.org/wiki/List_of_Chicago_%22L%22_stations |
| Chicago "L" as a whole | **`subway`** | Heavy-rail rapid transit: third rail, full signal separation, metro frequency, and the spec names it explicitly. Includes the surface/median Yellow, Purple-north and Blue-Forest-Park segments - they are the same fully grade-separated railroad, not street running. |
| Metra Electric | **`commuter rail`**, not subway | Electrified, high-platform and frequent by commuter standards, but it is a Metra commuter railroad with zone fares and diesel-territory branches, not a metro. Kept at the commuter tier; no place depends on this call except through tier precedence, and every Metra Electric place is Chicago-side suburbs already typed `commuter rail`. |
| South Shore Line | **`commuter rail`** | Interurban-descended, NICTD-operated commuter railroad. Street running in Michigan City (the last interurban-style segment) **ended February 27, 2022** and the realignment is complete, so no mixed-traffic operation remains. |
| Fox River Trolley Museum (South Elgin), Illinois Railway Museum (Union) | **excluded** | Heritage/museum operations, not scheduled transit. Not fetched as sources; named here only so the omission is explicit. |
| O'Hare Airport Transit System | **excluded** | Airport people-mover, excluded by spec rule 4. |

#### Deliberately excluded

| Thing | Why |
|---|---|
| **Portage, IN** | Served by the Portage/Ogden Dunes station but the station is not in it. Wikipedia: "is a station in [[Porter County, Indiana]] serving the municipalities of [[Portage, Indiana]] and [[Ogden Dunes, Indiana]]" - the physical site is Ogden Dunes (infobox address + the Ogden Dunes town article). |
| **Dyer, IN** | Munster/Dyer is the terminal's name, not its location. `Dyer, Indiana`: "Dyer commuters to Chicago are served by [[Munster/Dyer station]], a [[South Shore Line]] [[rail station]] in [[Munster, Indiana]]. The main station and parking lots are in Munster while overflow parking is in Dyer." Overflow parking is not a station. |
| **Park Forest, IL** | The **only** internal Wikipedia conflict I found in 243 Metra stations, and the only place that lost its qualification. `List of Metra stations` puts `211th Street/Lincoln Highway` in Park Forest, but the Metra Electric line article has `rowspan="2" \|[[Olympia Fields, Illinois\|Olympia Fields]]` over Olympia Fields **and** 211th Street, and the station article opens "is a [[commuter rail]] station along the Main Branch of the [[Metra Electric]] line in [[Olympia Fields, Illinois]]", then explains: "The station is located at the junction of three municipalities. The northern part of the platform and the parking lot west of the station lie in Olympia Fields, the eastern parking lot in Park Forest, and the western parking lot and bus station in Matteson." Park Forest gets a **parking lot**, not a platform. 211th Street is Park Forest's only Metra station, so Park Forest is dropped; Olympia Fields and Matteson already qualify on their own eponymous stations. Flagging as a judgement call - if the caller wants "any part of the station facility" to count, Park Forest goes back in. |
| **Chesterton, IN and Porter, IN** | Dune Park cannot be pinned to either. Three sources disagree: `Lakeshore Corridor` Location says Porter; NICTD's official address says "33 East U.S. Highway 12, Chesterton"; the station article says it "is a station in [[Westchester Township, Porter County, Indiana]], located **north of** the municipalities of [[Chesterton, Indiana\|Chesterton]] and [[Porter, Indiana\|Porter]]" and `Chesterton, Indiana` says "The South Shore Line stops **north of** Chesterton at the [[Dune Park station]]". Unincorporated township land, no Census place -> left out per spec rule 1. |
| **La Porte, IN** | Hudson Lake station is in the Hudson Lake CDP in Hudson Township, not in the city of La Porte. The old `Hillside` stop in LaPorte "Closed by 1942". |
| **Town of Pines, IN** | "The station serves the town of Beverly Shores as well as the nearby [[Town of Pines]]" - the Pines station itself "Closed by 1985". |
| **Dune Acres, IN** | Dune Acres station "Closed 1994". |
| **Rolling Prairie, New Carlisle, Hesston, Lydick, Ardmore, Springfield, Olive, Burnham IL, Tremont IN** | All South Shore stops closed between 1941 and 1994 (shaded closed rows in `Lakeshore Corridor`). |
| **Downtown Hammond station** | "Future infill station" on the Monon Corridor - not open. Hammond already qualifies twice. |
| **Ingleside IL, Prairie View IL, La Fox IL, Medinah IL** | Each has a genuine open Metra station, but each is an unincorporated community that is **not a 2020 Census place** (checked against the Census 2020 place-by-county file: no CDP or incorporated place of that name in Illinois). No Census place to emit. |
| **Rondout IL** | MD-N stop closed 1984 (see traps table). |
| **Techny IL** | MD-N stop "Closed 1971". |
| **Eola IL** | BNSF stop "Closed to passengers prior to 1971, closed entirely later". |
| **Central Stickney IL** | Heritage Corridor's `Glenn` station "Closed 1989". |
| **Beach Park IL** | UP-N `Dunes Park` stop "Closed after October 28, 1956". |
| **Lincolnwood IL, Skokie IL (Metra)** | UP-NW Skokie-branch stops, both "Skokie branch; Closed December 1, 1958". Skokie is in the dataset only for the CTA Yellow Line. |
| **Spring Grove, Solon Mills IL; Zenda, Walworth WI** | MD-N stops "Closed October 1, 1982" - service beyond Fox Lake was abolished. |
| **Racine, South Milwaukee, Cudahy, Milwaukee WI** | UP-N predecessor stops, all closed 1957-1971. |
| **St. Charles IL** | UP-W St. Charles branch station, closed. |
| **Auburn Park (Chicago)** | Metra Rock Island infill station **still under construction** in 2026 (Metra's own page targets end of 2026). Chicago already qualifies. |
| **103rd, 111th, Michigan, 130th (CTA Red Line Extension)** | Planned for 2030. All would be in Chicago anyway. |
| **Central (Blue, 2029), Racine (Green, 2029)** | CTA infill reopenings not yet built; both in Chicago. |
| **Johnsburg, Prairie Grove, Ridgefield, Marengo, Belvidere, Rockford IL; Kinzie-Fulton Market** | Proposed-only Metra / Rockford intercity stations. |
| **Wadsworth, Green Oaks, Gurnee, Richmond IL** | MD-N extension studies only: "there are not any plans to construct the extension". |
| **St. John, IN** | "a possible later extension" beyond Munster/Dyer - not built. |
| **Amtrak-only places** (e.g. Dyer IN's Amtrak station, Homewood/Joliet Amtrak platforms) | Intercity-only service is out of scope; Homewood and Joliet qualify on Metra regardless. |
| **Valparaiso IN** | Appears in the Rock Island article only as the `ChicaGo Dash` **bus**; the South Shore's Valparaiso branch is a proposal. BRT/bus excluded. |
| **Lansing IL** | Cited in the March 2026 press coverage as benefiting from the new Monon Corridor ("giving Lansing residents a closer train option to Chicago") but has no station. |

#### Sourcing limitations

| Site | Result |
|---|---|
| `https://www.transitchicago.com/maps/` (CTA, official) | **Blocked - HTTP 403** with a desktop Chrome user-agent. Fell back entirely to `List of Chicago "L" stations` + per-station Wikipedia articles, which was sufficient (the suburb count in the list article's own lead independently corroborates the 7 suburbs). |
| `https://metra.com/stations` (Metra, official) | **HTTP 404** - that path does not exist. `https://metra.com/` root served (HTTP 200), but the station directory is client-side rendered, so no machine-readable municipality list was obtainable. Fell back to `List of Metra stations` **and** all 11 line articles, cross-diffed. Metra's own newsroom was read via search for the 2026 construction program / Auburn Park status. |
| `https://www.mysouthshoreline.com/stations` (NICTD, official) | **Served** after following a 301 to `https://mysouthshoreline.com/plan-your-trip/stations-map/` (HTTP 200, 304 KB). Gave the authoritative 21-station open list plus street addresses; used as a primary source for Michigan City, Gary, Chicago and to expose the Dune Park address conflict. |
| Census place validation | Every emitted place name was checked against the Census 2020 place-by-county file already present in the workspace (`place_by_county2020.txt`), which is how Ingleside / Prairie View / La Fox / Medinah were caught as non-places and Long Lake IL / Hudson Lake IN confirmed as CDPs. |

#### 2025-2026 changes caught

1. **The South Shore Line's West Lake / Monon Corridor opened to passengers on March 31, 2026.** `South Shore Line`: "The project was originally estimated to open to revenue service in May 2025, but ultimately began operation March 31, 2026." That adds four open stations - Hammond Gateway and South Hammond (Hammond), Munster Ridge and Munster/Dyer (Munster) - and puts **Munster, IN** into the dataset as a new rail place. `Downtown Hammond` remains a future infill station. `Monon Corridor` is categorised "Railway lines opened in 2026". The confirming NICTD timetable on the official site is dated April 1, 2026.
2. **Dyer, IN did *not* gain a station** despite the branch being marketed as the Munster/Dyer extension - the platform and parking are in Munster, Dyer has overflow parking only.
3. **Double Track Northwest Indiana is finished** (Gary-Michigan City, opened May 2024; street running through Michigan City ended February 27, 2022) and, contrary to earlier plans, "Carroll Avenue station remains open despite prior plans to close it as part of the project." So Michigan City still has two stations, not one.
4. **Metra Electric Rock Island-side churn in 2025:** 103rd Street/Rosemoor reopened March 3, 2025 and 95th Street/Chicago State University closed the same day for reconstruction. Both are in Chicago - no place-level effect.
5. **Auburn Park (Metra, Rock Island) is still not open** as of this run; Metra's 2026 construction program targets completion by the end of 2026.
6. Governance note, no dataset effect: the Illinois **Northern Illinois Transit Authority Act** was enacted December 16, 2025 (cited in the CTA station list for the 2029 Central and Racine infill dates). It restructures RTA/CTA/Metra/Pace oversight but changes no station.

### 2.6 California

Scope: all California rail rapid transit / light rail / commuter rail except intercity
Amtrak. 143 Census places output (28 subway, 48 light rail, 67 commuter rail).
Research date 2026-07-29. Every place below is backed by a Wikipedia station-list article
fetched this session (raw wikitext via the MediaWiki API), plus the official agency site
where it served.

#### Systems covered

| System | Type assigned | Source URL(s) | How station -> city was established |
|---|---|---|---|
| BART (incl. eBART DMU segment) | subway | https://en.wikipedia.org/wiki/List_of_Bay_Area_Rapid_Transit_stations ; https://en.wikipedia.org/wiki/Pleasant_Hill/Contra_Costa_Centre_station ; official https://www.bart.gov/stations (HTTP 200) | The 50-row sortable station table has a dedicated **Location** column linking the municipality article. |
| Caltrain (electrified 2024) | commuter rail | https://en.wikipedia.org/wiki/List_of_Caltrain_stations ; https://en.wikipedia.org/wiki/Bayshore_station_(Caltrain) ; https://en.wikipedia.org/wiki/Caltrain | Station table has a **Location** column (rowspans group stations by city). Closed-stations table used to drop Atherton. |
| SF Muni Metro | light rail (counts, see judgements) | https://en.wikipedia.org/wiki/Muni_Metro ; https://en.wikipedia.org/wiki/List_of_Muni_Metro_stations | Article infobox `locale = San Francisco`; grep of the 117-station list found **no** station outside San Francisco (no Daly City stop). Adds no new place - SF is already subway via BART. |
| VTA light rail | light rail | https://en.wikipedia.org/wiki/List_of_VTA_light_rail_stations | Station table **Location** column; 59 open stations resolve to exactly 6 cities. |
| Altamont Corridor Express (ACE) | commuter rail | https://en.wikipedia.org/wiki/Altamont_Corridor_Express ; official https://acerail.com/stations/ (HTTP 200, served) | Wikipedia station table **Location** column, cross-checked station-for-station against the official ACE stations page. |
| SMART | commuter rail | https://en.wikipedia.org/wiki/Sonoma%E2%80%93Marin_Area_Rail_Transit ; official https://www.sonomamarintrain.org/stations (HTTP 200) | Station table has a literal **Municipality** column plus an **Opened** column, and a separate `Planned` block. |
| Sacramento RT Light Rail | light rail | https://en.wikipedia.org/wiki/List_of_Sacramento_RT_light_rail_stations | Station table has a **Jurisdiction** column; under-construction / proposed stations are in separate tables. |
| LA Metro Rail - B and D Lines | subway | https://en.wikipedia.org/wiki/List_of_Los_Angeles_Metro_Rail_stations ; https://en.wikipedia.org/wiki/D_Line_(Los_Angeles_Metro)| 110-row station table with **Location** and **Date opened** columns; per-line articles used for the 2025/2026 extensions. |
| LA Metro Rail - A, C, E, K Lines | light rail | https://en.wikipedia.org/wiki/List_of_Los_Angeles_Metro_Rail_stations ; https://en.wikipedia.org/wiki/A_Line_(Los_Angeles_Metro) ; https://en.wikipedia.org/wiki/Del_Amo_station ; https://en.wikipedia.org/wiki/Florence-Graham,_California | Same table; the `Location` cell writes city-of-LA stations as "Los Angeles (Neighborhood)" and separate municipalities/CDPs as a bare wikilink, which is what disambiguated the traps. |
| Metrolink (7 lines + Arrow) | commuter rail | https://en.wikipedia.org/wiki/List_of_Metrolink_(California)_stations ; https://en.wikipedia.org/wiki/Metrolink_(California) | 68-row station table with **Location** and **Date opened** columns; separate Closed and Future tables. |
| San Diego Trolley (Blue/Orange/Green/Copper + Silver heritage) | light rail | https://en.wikipedia.org/wiki/List_of_San_Diego_Trolley_stations ; https://en.wikipedia.org/wiki/San_Diego_Trolley | 62-station table with a **Location** column that writes San Diego stations as "San Diego, <neighborhood>" and suburbs as `[[City, California]]`. |
| COASTER | commuter rail | https://en.wikipedia.org/wiki/Coaster_(rail_service) | Station table has a **Location** column with rowspans per city. |
| SPRINTER | light rail (judged - see below) | https://en.wikipedia.org/wiki/Sprinter_(rail_service) | Station table **Location** column: "The line has fifteen stations serving Oceanside, Vista, San Marcos, and Escondido". |

#### Place-by-place

##### BART -> "subway" (26 places)
Location column of the 50-station table. Antioch, Berkeley, Colma, Concord, Daly City,
Dublin, El Cerrito, Fremont, Hayward, Lafayette, Millbrae, Milpitas, Oakland, Orinda,
Pittsburg, Pleasanton, Richmond, San Bruno, San Francisco, San Jose, San Leandro,
South San Francisco, Union City, Walnut Creek, plus 2 CDPs below.

| Place | Station(s) | Note / source quote |
|---|---|---|
| Oakland | 12th St, 19th St, Coliseum, Fruitvale, Lake Merritt, MacArthur, Rockridge, West Oakland, Oakland Int'l Airport | all rows read `[[Oakland, California\|Oakland]]` - confirms the Rockridge/Lake Merritt/West Oakland/Coliseum trap |
| San Francisco | 16th St Mission, 24th St Mission, Balboa Park, Civic Center, Embarcadero, Glen Park, Montgomery St, Powell St | Location `[[San Francisco]]` |
| Berkeley | Ashby, Downtown Berkeley, North Berkeley | |
| El Cerrito | El Cerrito del Norte, El Cerrito Plaza | |
| Concord | Concord, **North Concord/Martinez** | trap confirmed: North Concord/Martinez Location = `Concord` |
| Pittsburg | Pittsburg/Bay Point, Pittsburg Center (eBART) | |
| Antioch | Antioch (eBART, opened 2018) | only eBART serves it |
| Fremont | Fremont, **Warm Springs/South Fremont** | trap confirmed |
| San Jose | **Berryessa/North San José** (2020) | Location `[[San Jose, California\|San José]]` |
| Milpitas | Milpitas (2020) | |
| San Leandro | San Leandro, **Bay Fair** | Bay Fair Location = San Leandro |
| Hayward | Hayward, South Hayward | |
| Dublin + Pleasanton | Dublin/Pleasanton, West Dublin/Pleasanton | Location cell is literally `[[Dublin, California\|Dublin]]/[[Pleasanton, California\|Pleasanton]]` - both cities counted |
| Castro Valley (CDP) | Castro Valley | unincorporated Alameda County CDP |
| Contra Costa Centre (CDP) | Pleasant Hill/Contra Costa Centre | see below - **Pleasant Hill the city is excluded** |

**Pleasant Hill trap resolved.** Station article: "Pleasant Hill/Contra Costa Centre station
is located in the unincorporated Contra Costa Centre area of Contra Costa County ... south
of incorporated Pleasant Hill." The station-list Location column says Walnut Creek (also
already in the set). Output uses the **Contra Costa Centre CDP**, and the city of
Pleasant Hill is NOT in the dataset.

##### Caltrain -> "commuter rail" (11 new places; others outranked)
Belmont, Brisbane, Burlingame, Gilroy, Menlo Park, Morgan Hill, Palo Alto, Redwood City,
San Carlos, San Martin (CDP), San Mateo.
Also served but assigned a higher tier by another system: San Francisco, South San Francisco,
San Bruno, Millbrae, San Jose (BART = subway); Mountain View, Sunnyvale, Santa Clara
(VTA = light rail).

- San Mateo covers **Hayward Park and Hillsdale** (rowspan `[[San Mateo, California]]`), so no separate places.
- Palo Alto covers **California Avenue and the Stanford station** (3-row rowspan `[[Palo Alto, California]]`). Stanford CDP is therefore NOT added; the Stanford stop is also italicised "*Select weekend trains on game days only*".
- **Broadway** station Location = `[[Burlingame, California]]` (the "Broadway Burlingame" trap).
- **Bayshore** = Brisbane. Station article: "the platform itself is in Brisbane, California while the main parking lot is in San Francisco." Both cities are in the dataset anyway.
- **Atherton EXCLUDED** - it is in the *Closed stations* table: "Atherton | 2020 | ... | Closed due to low ridership and the hold-out rule."

##### SF Muni Metro -> "light rail" (0 new places)
All 117 stations in San Francisco (already subway via BART). See judgements.

##### VTA light rail -> "light rail" (4 new places)
Campbell, Mountain View, Santa Clara, Sunnyvale. (San Jose and Milpitas also have VTA
stations but are subway via BART.) A grep of every `[[City, California]]` link in the
open-stations table returns exactly: San Jose 42, Sunnyvale 8, Mountain View 6, Campbell 4,
Milpitas 4, Santa Clara 4. Almaden and Oakridge (closed 2019) and Evelyn (closed 2015)
are in the Former stations table and were not used.

##### ACE -> "commuter rail" (4 new places)
Lathrop, Livermore, Stockton, Tracy. (Pleasanton and Fremont = BART subway; Santa Clara
and San Jose = higher tier.) Full current station set, matching the official site
one-for-one: Stockton (Robert J. Cabral), Lathrop/Manteca -> Lathrop, Tracy,
Vasco Road -> Livermore, Livermore, Pleasanton, Fremont, Great America -> Santa Clara,
Santa Clara, San Jose Diridon.

##### SMART -> "commuter rail" (8 places)
| Place | Station(s) | Opened |
|---|---|---|
| Larkspur | Larkspur | Dec 14, 2019 |
| San Rafael | San Rafael, Marin Civic Center | Aug 25, 2017 |
| Novato | Novato-San Marin, Downtown Novato, Novato Hamilton | Aug 25, 2017 |
| Petaluma | Petaluma Downtown; **Petaluma North (Jan 10, 2025)** | 2017 / 2025 |
| Cotati | Cotati | Aug 25, 2017 |
| Rohnert Park | Rohnert Park | Aug 25, 2017 |
| Santa Rosa | Santa Rosa Downtown, Santa Rosa-Guerneville Road | Aug 25, 2017 |
| Windsor | Windsor | **May 31, 2025** |

##### Sacramento RT -> "light rail" (7 places)
Folsom (Glenn, Iron Point, Historic Folsom), Rancho Cordova (Cordova Town Center,
Mather Field/Mills, Sunrise, Zinfandel), Sacramento (43 stations), plus four
unincorporated CDPs from the Jurisdiction column: Gold River (Hazel), La Riviera
(Butterfield, Tiber), North Highlands (Watt/I-80), Rosemont (Starfire, Watt/Manlove).

##### LA Metro Rail
**Subway (B + D Lines): Los Angeles, Beverly Hills.**
The brief's assumption that B and D are "both entirely in Los Angeles" is now WRONG - see
the 2026 change below.

**Light rail (A, C, E, K Lines): 26 new places.**

| Place | Line | Station(s) |
|---|---|---|
| Long Beach | A | 1st St, 5th St, Anaheim St, Downtown Long Beach, Pacific Ave, Pacific Coast Highway, Wardlow, Willow St |
| Santa Monica | E | 17th St/SMC, 26th St/Bergamot, Downtown Santa Monica |
| Pasadena | A | Allen, Del Mar, Fillmore, Lake, Memorial Park, Sierra Madre Villa |
| South Pasadena | A | South Pasadena |
| Arcadia / Monrovia / Duarte / Irwindale / Azusa | A | Arcadia; Monrovia; Duarte/City of Hope; Irwindale; Azusa Downtown + APU/Citrus College |
| Glendora / San Dimas / La Verne / Pomona | A | Glendora; San Dimas; La Verne/Fairplex; Pomona North - **all opened Sept 19, 2025** |
| Compton | A | Artesia, Compton |
| Lynwood | C | Lynwood |
| Downey | C | Lakewood Boulevard (the "Paramount?" trap - Location = `[[Downey, California]]`) |
| Norwalk | C | Norwalk |
| Hawthorne | C | Crenshaw, Hawthorne/Lennox |
| El Segundo | K | Douglas, El Segundo, Mariposa |
| Redondo Beach | K | Redondo Beach |
| Inglewood | K | Downtown Inglewood, Fairview Heights, Westchester/Veterans |
| Culver City | E | Culver City |
| East Los Angeles (CDP) | E | Atlantic, East LA Civic Center, Maravilla |
| Rancho Dominguez (CDP) | A | Del Amo - "in the Los Angeles County community of Rancho Dominguez and **near** the city of Carson" |
| Florence-Graham (CDP) | A | Firestone, Florence, Slauson - the CDP article: "The census area includes the communities of Florence, Firestone Park, and Graham" |
| Willowbrook (CDP) | A + C | Willowbrook/Rosa Parks |

Brief's "?" cities correctly absent because no open station is inside them: **Carson**
(Del Amo is Rancho Dominguez CDP), **South Gate**, **Paramount** (Lakewood Blvd is Downey),
**Torrance** (K Line extension to Torrance is only planned).
LAX: **LAX/Metro Transit Center** (C+K) opened Jun 6, 2025 and is in Los Angeles
(Westchester); the LAX Automated People Mover is a people mover and out of scope.

##### Metrolink -> "commuter rail" (41 new places)
Acton (CDP), Anaheim (Anaheim + Anaheim Canyon), Baldwin Park, Buena Park, Burbank
(Burbank Airport-North, Burbank Airport-South, Downtown Burbank), Camarillo, Claremont,
Commerce, Corona (North Main + West), Covina, El Monte, Fontana, Fullerton, Glendale,
Industry, Irvine, Jurupa Valley (Jurupa Valley/Pedley), Laguna Niguel, Lancaster,
Montclair, Montebello, Moorpark, Moreno Valley, Ontario (Ontario-East), Orange, Oxnard,
Palmdale, Perris (Downtown + South), Rancho Cucamonga, Redlands (Downtown, Esri,
University - **Arrow, opened Oct 24, 2022**), Rialto, Riverside (Downtown, Hunter Park/UCR,
La Sierra), San Bernardino (Depot, Downtown, Tippecanoe), San Clemente (San Clemente +
San Clemente Pier), San Juan Capistrano, Santa Ana, Santa Clarita, Simi Valley, Tustin,
Upland, Ventura (Ventura-East).
Higher tier elsewhere: Los Angeles (subway), Norwalk, Pomona, La Verne (LA Metro light
rail), Oceanside (SPRINTER light rail).

Traps checked against the Location column:
- **Via Princessa, Newhall, Santa Clarita, Vista Canyon -> Santa Clarita** (all four rows).
- **Sylmar/San Fernando -> `[[Los Angeles]]`** (NOT the city of San Fernando).
- **Chatsworth, Northridge, Van Nuys, Sun Valley, Cal State L.A. -> `[[Los Angeles]]`**; **Burbank Airport-North/South and Downtown Burbank -> `[[Burbank]]`**.
- **Industry -> `[[Industry, California]]`** (City of Industry).
- **Norwalk/Santa Fe Springs -> `[[Norwalk, California]]`**; Santa Fe Springs not sourced, so excluded.
- **Laguna Niguel/Mission Viejo -> `[[Laguna Niguel]]`**; Mission Viejo not sourced, so excluded.
- **Fairplex -> `[[La Verne, California]]`**, marked "*(fair days)*"; La Verne is in the set anyway via the A Line.
- **Vincent Grade/Acton -> `[[Acton, California]]`** (CDP).
- **Oceanside** is the only San Diego County Metrolink stop (Orange County + Inland Empire-Orange County Lines).

##### San Diego Trolley -> "light rail" (7 places)
San Diego (all downtown/Mission Valley/La Jolla/University City/San Ysidro stations are
written "San Diego, <neighborhood>" - includes the 2021 UC San Diego Blue Line extension:
Nobel Drive, UC San Diego Central Campus, UC San Diego Health La Jolla, VA Medical Center,
Executive Drive, UTC, Balboa Ave, Clairemont Dr, Tecolote Rd), National City (8th St,
24th St), Chula Vista (E St, H St, Palomar St), Lemon Grove (Lemon Grove Depot,
Massachusetts Ave), La Mesa (70th St, Amaya Dr, Grossmont, La Mesa Blvd, Spring St),
El Cajon (Arnele Ave, El Cajon, Gillespie Field), Santee (Santee).

##### COASTER -> "commuter rail" (3 new places)
Carlsbad (Carlsbad Village, Carlsbad Poinsettia), Encinitas, Solana Beach.
Oceanside -> SPRINTER light rail; San Diego (Sorrento Valley, Old Town, Santa Fe Depot)
-> Trolley light rail. Downtown San Diego station is listed "Planned" and excluded.

##### SPRINTER -> "light rail" (4 places)
Escondido (Nordahl Rd, Escondido Transit Center), Oceanside (7 stations), San Marcos
(Palomar College, San Marcos Civic Center, Cal State San Marcos), Vista (Vista Transit
Center, Civic Center-Vista, Buena Creek).

#### Streetcar / borderline judgements

| System | Call | Why |
|---|---|---|
| **SF Muni Metro** (J, K, L, M, N, T, S) | **COUNTS as light rail** | Per the brief's explicit instruction and because it is a genuine rapid-transit-grade operation: "Five services ... run on separate surface alignments and merge into a single east-west tunnel, the Market Street subway. The T Third Street uses a north-south tunnel downtown, the Central Subway." Downtown operation is fully grade-separated in two subways with high-platform boarding. It adds no new place (San Francisco already subway via BART). Source: https://en.wikipedia.org/wiki/Muni_Metro |
| **SF F Market & Wharves + E Embarcadero** | **EXCLUDED** | Heritage streetcar lines running in mixed traffic on Market St / the Embarcadero, "served by heritage streetcars" (opened 1995). Fails the dedicated-ROW test in the spec. |
| **SF cable cars** | **EXCLUDED** | Spec rule 4 excludes cable cars/funiculars outright. |
| **eBART (BART Yellow Line, Pittsburg Center + Antioch)** | **COUNTS as subway with BART** | Diesel multiple-unit feeder, but it runs on an exclusive grade-separated alignment in the SR-4 median, is branded and operated as the BART Yellow Line, and passengers cross-platform transfer at a dedicated transfer platform: "A diesel multiple unit feeder service, eBART, opened from Pittsburg/Bay Point to Antioch in 2018." Antioch is in the dataset only because of it. |
| **Oakland Airport Connector** | not counted as its own rail mode | Spec rule 4 excludes people movers; it is "cable-hauled automated guideway transit (AGT)". Oakland is already subway from 8 BART heavy-rail stations, so nothing changes. |
| **SPRINTER (Oceanside-Escondido)** | **COUNTS as light rail** | FTA-classified "hybrid rail", but it is a 22-mile fully exclusive-ROW DMU line on the Escondido Subdivision (plus an elevated viaduct into CSU San Marcos), 15 stations at ~1.5 mi spacing, "every 30 to 60 minutes ... 34 per day each direction". Frequency + stop spacing + exclusive ROW = light rail, not peak-only commuter rail. This is why Oceanside is typed "light rail" rather than "commuter rail". |
| **San Diego Trolley Silver Line** | rides along, no effect | "a 'downtown loop' heritage streetcar line (Silver) that operates on holidays" - a heritage overlay on existing Trolley track. It is entirely inside San Diego, which already counts from the Blue/Orange/Green/Copper lines. |
| **San Diego Trolley Copper Line** | counts (regular Trolley line) | Opened September 2024, El Cajon-Santee shuttle on existing Trolley track. Both cities already counted. |
| **Arrow (San Bernardino-Redlands)** | **COUNTS as Metrolink commuter rail** | DMU service opened Oct 24, 2022; operated by Metrolink/SBCTA over the mainline into San Bernardino-Downtown. Stop spacing (~2 mi) is commuter-rail-ish and it is timetabled and branded within Metrolink, so it stays commuter rail. Adds Redlands. |

#### Deliberately excluded

| Thing | Why |
|---|---|
| **Pleasant Hill (city)** | Its BART station is not in it - "located in the unincorporated Contra Costa Centre area of Contra Costa County ... south of incorporated Pleasant Hill." Contra Costa Centre CDP used instead. |
| **Emeryville** | No BART station in the 50-row Location column (MacArthur is Oakland). Emeryville has only Amtrak Capitol Corridor / Coast Starlight, which is out of scope. |
| **San Francisco International Airport** (as a place) | The SFO BART station's Location cell reads `[[San Mateo County, California\|San Mateo County]]` - unincorporated airport land, not a Census place. San Bruno and Millbrae are in the set. |
| **Atherton** | Caltrain station closed 2020 (Closed stations table). |
| **Stanford (CDP)** | The Stanford Caltrain stop is inside the Palo Alto rowspan in the Location column, and runs "*Select weekend trains on game days only*". Not separately sourced to Stanford CDP -> left out per the no-invention rule. |
| **Santa Fe Springs** | Only appears in the station *name* "Norwalk/Santa Fe Springs"; the Location column says Norwalk. |
| **Mission Viejo** | Only in the name "Laguna Niguel/Mission Viejo"; Location column says Laguna Niguel. |
| **Sonoma County Airport (SMART station area)** | Municipality column reads "Unincorporated Sonoma County" with no CDP named - no verifiable Census place. |
| **Claremont + Montclair (as LA Metro light rail)** | A Line Foothill Extension Phase 2B to Claremont: "Construction is expected to break ground in 2027 and be completed in 2031", and the Claremont/Montclair segments were split apart in Sept 2025. Claremont and Montclair ARE in the dataset, but as **Metrolink commuter rail** only. |
| **ACE Ceres / Modesto / Merced / Manteca / Ripon / Natomas / Sacramento extension** | Not open. Wikipedia: service to Ceres and Natomas "again pushed back to 2026, with service to Merced and infill stations opening by 2030." Confirmed against the live official page https://acerail.com/stations/ - it lists 10 stations, Stockton through San Jose, with **zero** occurrences of Ceres, Merced, Turlock, Ripon or Natomas. |
| **SMART Healdsburg + Cloverdale** | Healdsburg "Expected 2028" (ground broken March 2026); Cloverdale "Unfunded". |
| **LA Metro D Line Beverly Drive, Century City, Westwood/UCLA, Westwood/VA Hospital** | Under construction, 2027. |
| **SacRT Dos Rios (Sept 2026) and Railyards (Aug 2026); Horn Rd, Rancho Cordova (2029)** | Under construction / proposed as of the fetch. Sacramento and Rancho Cordova are already in the set. |
| **Metrolink Placentia, L.A. General Medical Center, Pico Rivera, Hemet, San Jacinto** | All in the Future stations table, status "Planned", opening TBD. So Placentia, Pico Rivera, Hemet and San Jacinto are NOT in the dataset. |
| **Metrolink Auto Club Speedway (Fontana)** | Closed station (racetrack closed 2023). Fontana still counts via the Fontana station. |
| **COASTER Downtown San Diego station** | Listed "Planned". |
| **VTA Almaden, Oakridge, Evelyn** | Closed 2019 / 2015. |
| **Amtrak-only places** (Capitol Corridor, Pacific Surfliner, San Joaquins, Coast Starlight) | Out of scope per the task. This is why e.g. Davis, Martinez, Salinas, Santa Barbara, Bakersfield, Fresno are absent. |
| **LAX Automated People Mover; Oakland Airport Connector as a standalone system** | People movers / AGT (spec rule 4). |
| **Santa Barbara Metrolink extension** | Scrapped Jan 2026 in favour of an extra Pacific Surfliner train. |

#### 2025-2026 changes caught

1. **LA Metro D Line Extension Section 1 opened May 8, 2026** - Wilshire/La Brea,
   Wilshire/Fairfax (Los Angeles) and **Wilshire/La Cienega (Beverly Hills)**. The D Line
   is no longer entirely within the city of Los Angeles: "The D Line is a 9 mi line that
   begins at Wilshire/La Cienega station in Beverly Hills." **Beverly Hills is therefore a
   new "subway" place.** This contradicts the brief's assumption.
2. **LA Metro A Line Foothill Extension Phase 2B opened September 19, 2025** - four new
   stations: Glendora, San Dimas, La Verne/Fairplex, Pomona North. All four cities added
   as light rail. Claremont (2031) and Montclair are NOT open.
3. **LAX/Metro Transit Center (C + K Lines) opened June 6, 2025** - Los Angeles.
4. **SMART Windsor station opened May 31, 2025** - Windsor added. SMART's **Petaluma North**
   opened January 10, 2025. SMART went to 24 weekday round trips on April 12, 2026.
5. **ACE Ceres/Merced extension has NOT opened** (checked against the live agency site);
   only the historic 10-station Stockton-San Jose route runs.
6. **Metrolink cut its schedule ~20% in March 2026** (EMD F125 reliability), with more cuts
   and a fare increase floated for October 2026. No station closures resulted, so the place
   list is unaffected.
7. San Diego Trolley **Copper Line** (El Cajon-Santee) opened September 2024; Caltrain
   completed **full electrification September 21, 2024** (diesel retired) - both slightly
   before the window but relevant context.

#### Sourcing limitations

- **Wikipedia wikitext was the primary source for every system** (via the caching
  `fetch.sh` helper -> MediaWiki API). Station-list articles were used wherever they exist
  because they carry an explicit Location / Municipality / Jurisdiction column.
- Official sites tried once each with a browser UA. Served HTTP 200:
  `bart.gov/stations`, `vta.org/go/routes`, `acerail.com/stations/`,
  `sonomamarintrain.org/stations`, `metro.net/riding/schedules/`.
  Redirected/blocked to a useless body (HTTP 301 with 0-430 bytes, no station data):
  `caltrain.com/stations`, `sacrt.com/apps/light-rail/`,
  `sdmts.com/schedules-real-time-maps-and-routes/trolley`,
  `gonctd.com/services/coaster/`, `gonctd.com/services/sprinter/`.
- **metrolinktrains.com/stations/ returned HTTP 200 but is an Angular single-page app** -
  the station list is client-rendered (`{{station.name}}` / `{{station.city}}` placeholders
  in the served HTML), so it is not machine-readable. Fell back entirely to
  `List of Metrolink (California) stations`.
- Only the ACE station roster was fully cross-verified against an official agency page.
  Everything else rests on the Wikipedia station-list Location columns plus individual
  station articles for the non-obvious municipalities (Pleasant Hill/Contra Costa Centre,
  Bayshore/Brisbane, Del Amo/Rancho Dominguez, Firestone/Florence-Graham).
- **Not fully resolvable:** the LA Metro C Line **Vermont/Athens** station's Location cell
  reads "Los Angeles (Athens / South Los Angeles)". Athens/West Athens is an unincorporated
  CDP, so the true Census place for that one station is ambiguous. It makes no difference
  to the output - Los Angeles is already in the set, and no separate Athens or West Athens
  place was added, since the source formats it as a City-of-LA row.

### 2.7 Texas, the South, Florida, Puerto Rico

**66 Census places** across TX (17), FL (32), GA (9), TN (3), PR (3), NC (1), VA (1).
Types: 21 subway, 13 light rail, 32 commuter rail.

#### Method note - how station -> Census place was established

Two-stage verification for every place:

1. **Wikipedia station-list articles** (the gold source per the spec) which carry an explicit
   Jurisdiction / Municipality / Location / Town column.
2. **US Census Geocoder, coordinates endpoint** (`benchmark=Public_AR_Census2020&vintage=Census2020_Census2020&layers=all`)
   run against the station's coordinates or street address. If the response contains no
   `Incorporated Places` and no `Census Designated Places` layer, the point is in unincorporated
   territory covered by **no Census place** - and that place is excluded.

Stage 2 mattered a lot here: postal city names in the South and Florida routinely differ from the
Census place (e.g. SunRail's Sand Lake Road station is postally "Orlando, FL 32809" but sits in
**Pine Castle CDP**; Tri-Rail's Golden Glades station is postally "Miami" but sits in the
**Golden Glades CDP**). Nine candidate places were dropped because the station provably sits
outside every Census place.

#### Systems covered

| System | Type assigned | Source URL(s) | How station -> city was established |
|---|---|---|---|
| DART Rail (Dallas) incl. Silver Line | light rail | https://en.wikipedia.org/wiki/List_of_DART_light_rail_stations , https://en.wikipedia.org/wiki/Silver_Line_(DART) | Station list has a **Jurisdiction** column for all 73 stations; every non-Dallas jurisdiction re-verified with the Census geocoder |
| Trinity Railway Express | commuter rail | https://en.wikipedia.org/wiki/Trinity_Railway_Express | Station table has a **Municipality** column; Bell + Trinity Lakes re-verified against station articles + official TRE station list |
| TEXRail (Trinity Metro) | commuter rail | https://en.wikipedia.org/wiki/TEXRail | Station table has a **Municipality** column; all 3 municipalities geocode-verified |
| A-train (DCTA) | commuter rail | https://en.wikipedia.org/wiki/A-train_(Denton_County_Transportation_Authority) | Station table has a **Municipality** column; Highland Village/Lewisville Lake geocode-verified as Lewisville |
| METRORail (Houston) | light rail | https://en.wikipedia.org/wiki/METRORail | Article: "light rail system in **Houston**, Texas", `locale = Houston`; all four line termini geocode-verified as Houston city |
| CapMetro Rail Red Line (Austin) | commuter rail | https://en.wikipedia.org/wiki/Capital_MetroRail | Station table has **County / Community** columns; Leander + Lakeline + Downtown geocode-verified |
| MARTA rail (Atlanta) | subway | https://en.wikipedia.org/wiki/MARTA_rail | Station table has a per-station **city** column for all 38 stations; every non-Atlanta city geocode-verified |
| Lynx Blue Line (Charlotte) | light rail | https://en.wikipedia.org/wiki/Lynx_Blue_Line | Station list is by Charlotte **neighborhood**; both termini geocode-verified as Charlotte city |
| WeGo Star (Nashville) | commuter rail | https://en.wikipedia.org/wiki/WeGo_Star | Per-station articles give the municipality; Martha station geocode-verified inside Lebanon city |
| The Tide (Norfolk) | light rail | https://en.wikipedia.org/wiki/The_Tide_(light_rail) | Article: Norfolk "began developing a network that would be constructed **entirely within its city limits**"; both termini geocode-verified |
| Miami Metrorail | subway | https://en.wikipedia.org/wiki/List_of_Miami-Dade_Transit_metro_stations , https://en.wikipedia.org/wiki/Metrorail_(Miami-Dade_County) | Station list has a **Location** column sourced to the county's own "2010 Census Designated Places: Miami-Dade County" map; every CDP re-verified with the geocoder |
| Tri-Rail | commuter rail | https://en.wikipedia.org/wiki/Tri-Rail | Station table has a **Location** column; all 18 stations geocode-verified |
| SunRail | commuter rail | https://en.wikipedia.org/wiki/SunRail , https://sunrail.com/stations/ (official, served 200) | Route table has **County / Town** columns; official page gives street addresses; all 17 stations geocode-verified |
| Tren Urbano (San Juan) | subway | https://en.wikipedia.org/wiki/Tren_Urbano | Lead + infobox: "the capital municipality of **San Juan**, and the adjacent municipalities of **Guaynabo** and **Bayamón**"; 8 station coordinates geocode-verified into San Juan / Bayamón / Guaynabo *zona urbana* |

#### Place-by-place

##### DART Rail - light rail (Texas)
Source for all: https://en.wikipedia.org/wiki/List_of_DART_light_rail_stations (Jurisdiction column)

| Place | State | Station(s) | Verification |
|---|---|---|---|
| Dallas | TX | ~45 stations incl. EBJ Union, West End, Cityplace/Uptown, plus Silver Line Knoll Trail and Cypress Waters | List: Jurisdiction = Dallas. Cypress Waters footnoted "located in an **exclave** of Dallas near Coppell"; geocoder -> Dallas city |
| Plano | TX | Downtown Plano, Parker Road, **12th Street**, **Shiloh Road** | geocoder -> Plano city (both Silver Line stations) |
| Richardson | TX | Arapaho Center, CityLine/Bush, Galatyn Park, Spring Valley, **UT Dallas** | geocoder -> Richardson city |
| Garland | TX | Downtown Garland, Forest/Jupiter | geocoder -> Garland city |
| Rowlett | TX | Downtown Rowlett | geocoder -> Rowlett city |
| Carrollton | TX | Downtown Carrollton, North Carrollton/Frankford, Trinity Mills | geocoder -> Carrollton city |
| Farmers Branch | TX | Farmers Branch | geocoder -> Farmers Branch city |
| Irving | TX | Belt Line, Dallas College North Lake, Hidden Ridge, Irving Convention Center, Las Colinas Urban Center, University of Dallas | geocoder -> Irving city |
| **Addison** | TX | **Addison** (Silver Line only) | "Addison station ... Addison ... **October 25, 2025**"; geocoder -> Addison town |
| **Grapevine** | TX | **DFW Airport North** (Silver Line + TEXRail), Grapevine-Main Street (TEXRail), and DFW Airport Terminal A/B | geocoder -> Grapevine city for all four |

##### Trinity Railway Express / TEXRail - commuter rail (Texas)
| Place | State | Station(s) | Verification |
|---|---|---|---|
| Fort Worth | TX | TRE: T&P, Fort Worth Central, Trinity Lakes, Bell, CentrePort/DFW. TEXRail: North Side, Mercantile Center | Bell station article: "is a Trinity Railway Express commuter rail station in **Fort Worth**, Texas ... near Fort Worth's border with Hurst"; geocoder -> Fort Worth city. Trinity Lakes article: "located in eastern **Fort Worth**, Texas, on the border with Hurst" + official TRE stations page `borough = Fort Worth, Texas` |
| North Richland Hills | TX | NRH/Iron Horse, NRH/Smithfield | TEXRail table Municipality = North Richland Hills; geocoder confirms both |

(Dallas and Irving also have TRE stations but rank higher as light rail.)

##### A-train - commuter rail (Texas)
| Place | State | Station(s) | Verification |
|---|---|---|---|
| Denton | TX | Downtown Denton Transit Center, MedPark | A-train table Municipality = Denton |
| Lewisville | TX | Highland Village/Lewisville Lake, Old Town, Hebron | A-train table Municipality = Lewisville for all three (the Highland Village station only *serves* the "City of Highland Village"); geocoder -> Lewisville city for all three |

(Trinity Mills is in Carrollton, already counted as light rail.)

##### METRORail - light rail (Texas)
| Place | State | Station(s) | Verification |
|---|---|---|---|
| Houston | TX | all 37 Red / Green / Purple Line stations | Article lead: "**METRORail** is the 22.7 mi **light rail** system in **Houston**, Texas"; `locale = Houston, Texas`. Termini geocode-verified: Northline TC, Theater District, Fannin South, Magnolia Park TC, Palm Center -> all Houston city |

##### CapMetro Rail Red Line - commuter rail (Texas)
| Place | State | Station(s) | Verification |
|---|---|---|---|
| Austin | TX | Lakeline, Howard, Kramer, McKalla, Crestview, Highland, MLK Jr., Plaza Saltillo, Downtown | Route table Community column = "..., Austin" for all; Lakeline listed as "Avery Ranch-Lakeline, **Austin**" and geocoder -> Austin city |
| Leander | TX | Leander (northern terminus) | geocoder -> Leander city |

##### MARTA - subway (Georgia)
Source: https://en.wikipedia.org/wiki/MARTA_rail (per-station city column, all 38 stations)

| Place | State | Station(s) | Verification |
|---|---|---|---|
| Atlanta | GA | 24 stations incl. Five Points, Airport-adjacent core, East Lake, Lakewood/Fort McPherson (Atlanta/East Point), H.E. Holmes, Bankhead, SEC District | geocoder spot-checks -> Atlanta city |
| College Park | GA | **Airport**, College Park | Table: Airport station city = "College Park"; geocoder -> College Park city (**not** Hapeville) |
| East Point | GA | East Point; Lakewood/Fort McPherson (shared) | Table: "Atlanta / East Point"; geocoder -> East Point city |
| Decatur | GA | Decatur, **Avondale**; East Lake listed "Atlanta/Decatur" | Table: Avondale station city = "Decatur"; geocoder -> Decatur city (**not** Avondale Estates) |
| Chamblee | GA | Chamblee | geocoder -> Chamblee city |
| Doraville | GA | Doraville (Gold Line terminus) | geocoder -> Doraville city |
| Brookhaven | GA | Brookhaven/Oglethorpe | City incorporated 2013; geocoder -> Brookhaven city |
| Dunwoody | GA | Dunwoody | City incorporated 2008; geocoder -> Dunwoody city |
| Sandy Springs | GA | Medical Center, Sandy Springs, North Springs | City incorporated 2005; geocoder -> Sandy Springs city for all three |

##### Lynx Blue Line - light rail (North Carolina)
| Place | State | Station(s) | Verification |
|---|---|---|---|
| Charlotte | NC | all 26 stations | Article: the line "runs along South Boulevard to its southern terminus just north of Interstate 485 at the **Pineville city limits**". Station list is entirely Charlotte neighborhoods. geocoder: I-485/South Boulevard and UNC Charlotte-Main -> Charlotte city |

##### WeGo Star - commuter rail (Tennessee)
| Place | State | Station(s) | Verification |
|---|---|---|---|
| Nashville | TN | Riverfront, Donelson, Hermitage | Donelson station "is a train station in **Nashville**, Tennessee"; Hermitage station "is a train station in **Nashville**, Tennessee ... serving Nashville's Hermitage area". geocoder Riverfront -> "Nashville-Davidson metropolitan government (balance)" |
| Mount Juliet | TN | Mt. Juliet | Station article: "is a train station in **Mount Juliet**, Tennessee" |
| Lebanon | TN | Lebanon, Hamilton Springs, **Martha** | Hamilton Springs "is a train station in **Lebanon**, Tennessee". Martha station (65 Martha Circle) geocodes to **Lebanon city** despite Wikipedia's "Martha, Tennessee" address label |

##### The Tide - light rail (Virginia)
| Place | State | Station(s) | Verification |
|---|---|---|---|
| Norfolk | VA | all 11 stations | "Norfolk began developing a network that would be constructed **entirely within its city limits**"; "The current eastern end of The Tide is at *Newtown Road*, which is the Norfolk-Virginia Beach boundary line." geocoder: EVMC/Fort Norfolk and Newtown Road -> Norfolk city |

##### Miami Metrorail - subway (Florida)
Source: https://en.wikipedia.org/wiki/List_of_Miami-Dade_Transit_metro_stations (Location column, cited to Miami-Dade County's own Census-designated-places map)

| Place | State | Station(s) | Verification |
|---|---|---|---|
| Miami | FL | Allapattah, Brickell, Coconut Grove, Culmer, Douglas Road, Government Center, Historic Overtown/Lyric Theatre, Santa Clara, UHealth-Jackson, Vizcaya | List: "Miami (<neighborhood>)" |
| Hialeah | FL | Hialeah, Okeechobee, Tri-Rail Transfer | geocoder -> Hialeah city for all three |
| Coral Gables | FL | University | geocoder -> Coral Gables city |
| South Miami | FL | South Miami | geocoder -> South Miami city |
| Medley | FL | Palmetto (Green Line north terminus) | List: "Medley"; geocoder at 25.84333,-80.32417 -> **Medley town** |
| Brownsville *(CDP)* | FL | Brownsville, Earlington Heights | geocoder -> **Brownsville CDP** |
| Gladeview *(CDP)* | FL | Northside, Dr. Martin Luther King Jr. Plaza | geocoder (3150 NW 79th St / 6205 NW 27th Ave) -> **Gladeview CDP** |
| Glenvar Heights *(CDP)* | FL | Dadeland North | List: "Glenvar Heights (Dadeland)"; geocoder (8300 S Dixie Hwy) -> **Glenvar Heights CDP** |
| Kendall *(CDP)* | FL | Dadeland South (southern terminus) | List: "Kendall (Dadeland)"; geocoder (9150 S Dadeland Blvd) -> **Kendall CDP** |

##### Tri-Rail - commuter rail (Florida)
Source: https://en.wikipedia.org/wiki/Tri-Rail (Location column). Every station geocode-verified.

| Place | State | Station(s) | Verification |
|---|---|---|---|
| Mangonia Park | FL | Mangonia Park (north terminus) | geocoder -> Mangonia Park town |
| West Palm Beach | FL | West Palm Beach | geocoder -> West Palm Beach city |
| Lake Worth Beach | FL | Lake Worth Beach | geocoder -> Lake Worth Beach city (renamed from "Lake Worth" 2019) |
| Boynton Beach | FL | Boynton Beach | geocoder -> Boynton Beach city |
| Delray Beach | FL | Delray Beach | geocoder -> Delray Beach city |
| Boca Raton | FL | Boca Raton | geocoder -> Boca Raton city |
| Deerfield Beach | FL | Deerfield Beach | geocoder -> Deerfield Beach city |
| Pompano Beach | FL | Pompano Beach | geocoder -> Pompano Beach city |
| Fort Lauderdale | FL | Cypress Creek, Fort Lauderdale | geocoder -> Fort Lauderdale city for **both** (Cypress Creek is **not** in Oakland Park) |
| Dania Beach | FL | Fort Lauderdale Airport | Location column = Dania Beach; geocoder -> Dania Beach city |
| Hollywood | FL | Sheridan Street, Hollywood | geocoder -> Hollywood city for both |
| Golden Glades *(CDP)* | FL | Golden Glades | geocoder (25.921529,-80.216949) -> **Golden Glades CDP** on the 2020 vintage. Wikipedia: "**Biscayne Gardens** is served by Tri-Rail at the Golden Glades station" - see naming note below |
| Opa-locka | FL | Opa-locka | geocoder -> Opa-locka city |

(Hialeah's Hialeah Market + Metrorail Transfer and Miami's MiamiCentral are Tri-Rail stations too, but both places rank higher as subway.)

##### SunRail - commuter rail (Florida)
Sources: https://en.wikipedia.org/wiki/SunRail (County/Town columns) + https://sunrail.com/stations/ (official addresses). Every station geocode-verified.

| Place | State | Station(s) | Verification |
|---|---|---|---|
| DeBary | FL | DeBary | geocoder -> DeBary city |
| Lake Mary | FL | Lake Mary | geocoder -> Lake Mary city |
| Longwood | FL | Longwood | geocoder -> Longwood city |
| Altamonte Springs | FL | Altamonte Springs | geocoder -> Altamonte Springs city |
| Maitland | FL | Maitland | geocoder -> Maitland city |
| Winter Park | FL | Winter Park/Amtrak | geocoder -> Winter Park city |
| Orlando | FL | AdventHealth, LYNX Central, Church Street, Orlando Health/Amtrak | geocoder -> Orlando city for all four |
| Pine Castle *(CDP)* | FL | Sand Lake Road | Wikipedia Town = "Pine Castle"; official address "8030 South Orange Ave., **Orlando**, FL 32809" (postal); geocoder -> **Pine Castle CDP** |
| Meadow Woods *(CDP)* | FL | Meadow Woods | official address "120 Fairway Woods Blvd., **Orlando**, FL 32824" (postal); geocoder -> **Meadow Woods CDP** |
| Kissimmee | FL | Kissimmee/Amtrak | geocoder -> Kissimmee city |

##### Tren Urbano - subway (Puerto Rico)
| Place | State | Station(s) | Verification |
|---|---|---|---|
| San Juan | PR | Sagrado Corazón, Hato Rey group, Universidad, Río Piedras, Cupey, Centro Médico, San Francisco, Las Lomas, Martínez Nadal | Lead: "the capital **municipality of San Juan**"; geocoder -> "San Juan zona urbana" for Sagrado Corazón, Martínez Nadal, Las Lomas, San Francisco |
| Bayamón | PR | Bayamón (terminus), Deportivo, Jardines | geocoder -> "Bayamón zona urbana" for all three |
| Guaynabo | PR | Torrimar | Station list: "Torrimar (**Guaynabo**)"; geocoder -> "Guaynabo zona urbana" |

Naming note: PR municipios are county-equivalents in the Census hierarchy; the *places* are the
"<name> zona urbana" CDPs (`San Juan zona urbana` 1276770, `Bayamón zona urbana` 1206593,
`Guaynabo zona urbana` 1232522). Per the task brief, the municipio name is used with state `PR`.

#### Streetcar / borderline judgements

| System | Call | Why | Source |
|---|---|---|---|
| **New Orleans Streetcars** (St. Charles, Canal/City Park, Riverfront, Rampart-St. Claude) | **EXCLUDE** | Legacy streetcar, not rapid-transit-like. St. Charles Line infobox: `character = Primarily in neutral ground (central median), **street running** between Howard Avenue and Canal Street`; Canal Line infobox: `character = Runs in neutral ground (median strip) along Canal St, **in mixed traffic** on Carrollton Ave`. The "neutral ground" median is at grade, crossed at every block, and the CBD sections run in the curb lane ("With the exception of Carondelet Street and the downtown portion of St. Charles where the line runs in the curbside lane..."). No subway/tunnel segment - the distinguishing feature the brief uses to admit SF Muni Metro and SEPTA subway-surface. **Consequence: New Orleans, LA does not appear in the dataset.** | https://en.wikipedia.org/wiki/St._Charles_Streetcar_Line , https://en.wikipedia.org/wiki/Canal_Streetcar_Line , https://en.wikipedia.org/wiki/Streetcars_in_New_Orleans |
| **Atlanta Streetcar** (Downtown Loop) | EXCLUDE | `character = At-grade street running`; 2.7 mi downtown loop, 12 stops. Atlanta is already in the set via MARTA. | https://en.wikipedia.org/wiki/Atlanta_Streetcar |
| **CityLynx Gold Line** (Charlotte) | EXCLUDE | `character = Street running`; "criticized for its street running design, **instead of having a dedicated right of way**". Charlotte already in via Blue Line. | https://en.wikipedia.org/wiki/CityLynx_Gold_Line |
| **El Paso Streetcar** | EXCLUDE | `character = Streetcar in mixed traffic`; categorised as a heritage streetcar system. **El Paso, TX is therefore not in the dataset.** | https://en.wikipedia.org/wiki/El_Paso_Streetcar |
| **M-Line Trolley** (Dallas) | EXCLUDE | "heritage streetcar line in the Uptown neighborhood of Dallas ... uses restored historic streetcar vehicles". Dallas already in via DART. | https://en.wikipedia.org/wiki/M-Line_(Dallas) |
| **Dallas Streetcar** (Oak Cliff) | EXCLUDE | `character = Street running` (modern streetcar). Dallas already in. | https://en.wikipedia.org/wiki/Dallas_Streetcar |
| **Galveston Island Trolley** | EXCLUDE | `type = Heritage streetcar`, `character = street-running`; reopened Oct 2021 but "limited to three days a week". **Galveston, TX not in dataset.** | https://en.wikipedia.org/wiki/Galveston_Island_Trolley |
| **MATA Trolley** (Memphis) | EXCLUDE (twice over) | Heritage streetcar, and **not operating**: all service suspended Aug 2024; as of March 2026 TDOT requirements are still outstanding and MATA "aims to put these streetcars into service in **fall 2026**". Rubber-tired trolley buses run instead. **Memphis, TN not in dataset.** | https://en.wikipedia.org/wiki/MATA_Trolley |
| **Metro Streetcar / River Rail** (Little Rock + North Little Rock) | EXCLUDE | `type = Heritage streetcar`, 3.4 mi figure-eight loop; the article itself says converting it into "a more effective rail rapid transit line" would require the proposed airport extension. **Little Rock and North Little Rock, AR not in dataset.** | https://en.wikipedia.org/wiki/River_Rail_Streetcar |
| **TECO Line Streetcar** (Tampa) | EXCLUDE | `type = Heritage streetcar`, `character = Fully at-grade`, 2.7 mi downtown-Ybor connector. **Tampa, FL not in dataset.** | https://en.wikipedia.org/wiki/TECO_Line_Streetcar |
| **Metromover** (Miami) | EXCLUDE | `transit_type = Automated people mover`, fare-free downtown circulator - the spec excludes people movers. Miami is already in via Metrorail. | https://en.wikipedia.org/wiki/Metromover |
| **Brightline** (Miami-Orlando) | EXCLUDE | Short description: "**Intercity** rail service in Florida"; infobox `type = Inter-city higher-speed rail`; lead: "an **intercity rail** route, with some aspects of a commuter rail ... the only **privately owned** and operated intercity passenger railroad in the United States". Reservation-based, airline-style fares, not a transit service. **Consequence: Aventura, FL is not in the dataset** (its only rail is the Brightline infill station opened Dec 2022). Miami / Fort Lauderdale / Boca Raton / West Palm Beach / Orlando are all in anyway via Tri-Rail, Metrorail or SunRail. | https://en.wikipedia.org/wiki/Brightline |
| **DART Silver Line** classification | INCLUDED as light rail | Wikipedia calls it a "hybrid rail service" (Stadler FLIRT DMUs, 30 min peak / hourly off-peak), but it is one of the five lines of DART Rail and all its stations are carried in the article *List of DART light rail stations*. Following the task brief's mapping (DART -> "light rail"). **Flag for the parent:** if you would rather treat hybrid rail as commuter rail, the affected rows are Addison TX and Grapevine TX (Grapevine also has TEXRail commuter rail, so it stays a rail place either way). | https://en.wikipedia.org/wiki/List_of_DART_light_rail_stations , https://en.wikipedia.org/wiki/Silver_Line_(DART) |
| **MBTA-style "Green Line" analogues** | n/a | No system in this scope needed the subway-vs-light-rail exception. MARTA, Miami Metrorail and Tren Urbano are all third-rail, fully grade-separated heavy rail -> `subway`. |

#### Deliberately excluded

##### Not open to passengers yet
| Thing | Why |
|---|---|
| DART **D2 Subway** (4 downtown Dallas stations) | "put on indefinite hiatus in 2023" |
| DART deferred stations (Knox-Henderson, Loop 12, Plano Road, South Las Colinas) | Never built; "not included in DART's current long-term plans" |
| CapMetro **North Burnet/Uptown** station, Austin | "Planned to open in 2027" |
| TEXRail **Medical District** extension, Fort Worth | Groundbreaking late 2026, opening 2029 |
| A-train **Corinth, TX** infill station | Corinth must first vote to join DCTA; "as of 2026 there are no plans for such an election" -> **Corinth excluded** |
| SunRail **Orlando International Airport** station (Phase 3) | Listed as a future station |
| Tren Urbano **Phase 1A** (San Mateo, Minillas) | Not built |
| MARTA Streetcar East Extension | Construction not complete; mayor pulled support in 2025 |
| Virginia Beach Tide extension | Referendum failed 2016 |

##### Station closed / service suspended
| Thing | Why |
|---|---|
| **Richland Hills, TX** | TRE Richland Hills station **closed Feb 17, 2024**, replaced by Trinity Lakes station (Fort Worth) on Feb 19, 2024. No station in Richland Hills any more. |
| **Memphis, TN** | MATA Trolley fully suspended since Aug 2024, still down as of March 2026. |
| DART Convention Center station, Dallas | "Closed until 2029 due to renovations to the Kay Bailey Hutchison Convention Center" - does not affect Dallas, which has 40+ other stations. |

##### Station sits in unincorporated territory - no Census place
All verified with the Census geocoder (2020 benchmark **and** current benchmark), which returned
neither an `Incorporated Places` nor a `Census Designated Places` layer for the point.

| Thing | Why |
|---|---|
| MARTA **Kensington** station (3350 Kensington Rd) | Article: "an at-grade subway station in **unincorporated DeKalb County**". Geocoder: no place. -> **Clarkston GA excluded** (it is only *served* by buses from this station) |
| MARTA **Indian Creek** station (3901 Durham Park Rd) | Article: "in **unincorporated DeKalb County**". Geocoder: no place. -> **Stone Mountain / Tucker / Redan GA excluded** |
| Miami **Miami International Airport** station (Miami Intermodal Center, 3600 NW 21st St) | Station list Location = "Miami-Dade County" (unincorporated). Geocoder: no place. Miami & Hialeah are in via other stations. |
| SunRail **DeLand** station (2491 Old New York Ave) | Geocoder: **no place** at 29.017806,-81.35272 and at the street address, on both the 2020 and current benchmarks (a downtown DeLand control address does return "DeLand city"). Wikipedia says the station is "in DeLand, Florida, **located west of the downtown area**" - the postal city, not the municipality. -> **DeLand FL excluded.** *Parent override candidate:* the station is named for and serves DeLand, and the extension did open Aug 12, 2024. |
| SunRail **Sanford** station (2720 W State Road 46) | Geocoder: **no place** at 28.813168,-81.298673 (a downtown Sanford control address returns "Sanford city"). The station is 2 mi west of downtown; SunRail runs a separate "Sanford Trolley" bus to reach downtown. -> **Sanford FL excluded.** *Parent override candidate.* |
| SunRail **Poinciana** station (5025 S Rail Ave) | Geocoder: **no place** at 28.258829,-81.484368 on both benchmarks (a Poinciana residential control address returns "Poinciana CDP"). The station is north of the CDP and "also serves the nearby communities of Intercession City and Campbell". -> **Poinciana FL excluded.** *Parent override candidate.* |
| SunRail **Tupperware** station (3205 Orange Ave) | Geocoder: no place. Wikipedia calls it a "station in **Hunter's Creek**, Florida" but also "the northernmost SunRail station in **Osceola County**", while Hunter's Creek CDP is in **Orange** County - internally contradictory, and the point is in unincorporated Osceola County. -> **Hunter's Creek FL excluded.** |
| Dallas/Fort Worth International Airport | Not a Census place (a joint airport board jurisdiction). The DART list writes the jurisdiction as "DFW Airport"; the Census geocoder puts both DFW Airport Terminal A and Terminal B stations **inside Grapevine city**, which is already in the set. |

##### No station in that place at all (candidate cities checked and dropped)
| Thing | Why |
|---|---|
| **Coppell, TX** | The Silver Line's Cypress Waters station is footnoted "located in an exclave of Dallas near Coppell" / "Located in an exclave that borders non-DART member Coppell"; geocoder -> Dallas city. Coppell is not a DART member. |
| **University Park / Highland Park, TX** | SMU/Mockingbird station's jurisdiction is Dallas. |
| **Hurst, TX** | The TRE table's Municipality cell says "Hurst" for Bell station but its own footnote says "Bell station is **located in Fort Worth** but uses a Hurst postal code", and the Bell station article + geocoder agree on Fort Worth. Trinity Lakes is in eastern Fort Worth per its article and the official TRE station page. (Note: Wikipedia's Trinity Lakes coordinate 32.8055,-97.2095 lands in Hurst city, but it is west of I-820 whereas the station is described as "just to the east of Interstate 820"; a corrected point east of I-820 geocodes to Fort Worth city.) |
| **Grand Prairie, TX** | The TRE alignment does not stop there; no station in the TRE station table. |
| **Highland Village, TX** | The A-train's Highland Village/Lewisville Lake station is in **Lewisville** per the Municipality column and the geocoder; it merely *serves* the City of Highland Village. |
| **Cedar Park, TX** and **Lakeway, TX** | Neither has a CapMetro Rail station; the Red Line's only non-Austin station is Leander. |
| **Hapeville, GA** | MARTA's Airport station is in **College Park** (table + geocoder). |
| **Avondale Estates, GA** | MARTA's Avondale station is in **Decatur** (table + geocoder). |
| **Pineville, NC** | The Blue Line stops "just north of Interstate 485 at the Pineville city limits"; I-485/South Boulevard station geocodes to Charlotte city. |
| **Virginia Beach, VA** | The Tide's Newtown Road terminus is on the Norfolk side of the Norfolk/Virginia Beach line. |
| **Martha, TN** | Not excluded as a place - the station geocodes into **Lebanon city**, so it folds into Lebanon rather than adding a place. |
| **Miami Springs, FL** | No Tri-Rail or Metrorail station; Okeechobee and Hialeah Market stations are both in Hialeah. |
| **Oakland Park, FL** | Tri-Rail's Cypress Creek station is in Fort Lauderdale (table + geocoder). |
| **Westview, FL** | No Metrorail station in the Westview CDP; the nearby stations are in Gladeview and Brownsville CDPs. |
| **Aventura, FL** | Only rail is Brightline (excluded as intercity). |
| **New Orleans, LA / El Paso, TX / Galveston, TX / Memphis, TN / Little Rock + North Little Rock, AR / Tampa, FL** | Only rail is a streetcar/heritage trolley system - see the judgement table. |

##### Other modes excluded per spec
MIA Mover (Miami airport monorail), Orlando International Airport Terminal Link people movers,
Jacksonville Skyway, METRORapid Silver Line (Houston BRT), Lymmo (Orlando BRT),
South Dade TransitWay (BRT), MARTA / CapMetro / METRO planned BRT lines,
Amtrak-only stations, Grapevine Vintage Railroad (tourist steam railroad).

#### 2025-2026 changes caught

1. **DART Silver Line opened to passengers October 25, 2025** - the single biggest change in this
   scope. 26 mi hybrid-rail line, "connecting seven cities and DFW Airport". Newly added places:
   **Addison, TX** and **Grapevine, TX** (Grapevine previously had TEXRail only). New stations in
   already-covered cities: 12th Street + Shiloh Road (Plano), UT Dallas (Richardson),
   Knoll Trail + Cypress Waters (Dallas), Downtown Carrollton interchange (Carrollton),
   DFW Airport North (Grapevine), DFW Airport Terminal B. **Coppell was NOT added** - the
   Cypress Waters station is in a Dallas exclave next to (non-member) Coppell.
2. **DART Convention Center station (Dallas) is temporarily closed until 2029** for Kay Bailey
   Hutchison Convention Center reconstruction.
3. **MARTA's Dome/GWCC/Philips Arena/CNN Center station now appears as "SEC District" station** in
   the station list - a rename, no place impact.
4. **Golden Glades CDP was renamed "Biscayne Gardens CDP" by the Census Bureau in 2023** (BAS23 /
   BAS24 TIGERweb), same GEOID 1226375. The 2020 Census place file still says "Golden Glades CDP",
   and ACS was still publishing "Golden Glades CDP" as of the article's last check. **I output
   `"Golden Glades"`** (matches the 2020 vintage this project's `place_by_county2020.txt` uses, and
   matches the station name) with the rename flagged in `cdp_notes`. Swap to "Biscayne Gardens" if
   the app keys on a post-2023 place vintage.
5. **Memphis MATA Trolley is still fully suspended** - down since Aug 2024; as of 4 March 2026 TDOT
   had "outlined requirements needed before downtown Memphis trolleys return", and MATA is targeting
   **fall 2026**. Memphis stays out.
6. **Trinity Metro TEXRail Medical District extension**: April 2026 announcement - groundbreaking by
   end of 2026, opening **2029**. Not counted.
7. TRE has **leased Northstar (Minneapolis) equipment for the 2026 FIFA World Cup** to add service -
   extra capacity, no new stations.
8. Slightly older but recent and verified: **SunRail's DeLand extension opened August 12, 2024**
   (Phase 2 North) and **TRE's Richland Hills station closed Feb 17, 2024**, replaced by Trinity
   Lakes station Feb 19, 2024.

#### Sourcing limitations

##### Official agency sites - one attempt per system, with `-A "Mozilla/5.0 ..."` and `-L`

| Agency site | Result |
|---|---|
| `https://sunrail.com/stations/` | **200, served.** Used it - gave the official street address of all 17 stations, which is what exposed the postal-city vs Census-place mismatches (Sand Lake Road "Orlando" -> Pine Castle CDP, etc.) |
| `https://trinityrailwayexpress.org/stations/` | 200, served (also cited inside the Trinity Lakes station article for `borough = Fort Worth`) |
| `https://ridetrinitymetro.org/texrail/` | 200, served |
| `https://www.capmetro.org/rail` | 200, served |
| `https://www.itsmarta.com/rail-stations.aspx` | 200, served |
| `https://gohrt.com/routes/light-rail/` | 200, served |
| `https://www.miamidade.gov/transportation-publicworks/metrorail-stations.asp` | 200, served |
| `https://www.gobrightline.com/` | 200, served |
| `https://www.dart.org/about/dart-rail-and-bus/dart-rail` | **404** - fell back to the Wikipedia DART station list (which cites DART's own Silver Line rail guide PDF and the CBS News opening story) |
| `https://www.dcta.net/routes-and-schedules/a-train` | **404** - fell back to the Wikipedia A-train article |
| `https://www.ridemetro.org/rider-guide/maps-schedules` | **404** - fell back to Wikipedia METRORail + Census geocoder on the four termini |
| `https://www.charlottenc.gov/CATS/Ride/Rail` | **403 Forbidden** (bot-blocked) - fell back to Wikipedia Lynx Blue Line |
| `https://www.wegotransit.com/ride/routes-schedules/wego-star/` | **404** - fell back to Wikipedia WeGo Star + the seven per-station articles |
| `https://www.tri-rail.com/stations/` | **404 (0 bytes)** - fell back to the Wikipedia Tri-Rail station table + geocoder on all 18 stations |
| `https://ati.pr.gov/tren-urbano` | **404** - fell back to Wikipedia Tren Urbano + geocoder on 8 station coordinates |

##### Other limitations
- **`geocoding.geo.census.gov` address endpoint is unreliable for rural/highway addresses.**
  "2720 W State Road 46, Sanford FL" was silently matched to "2720 **E** State Hwy 46" (the wrong
  side of town, in Midway CDP), and "3205 Orange Ave, Kissimmee" / "5025 S Rail Ave" returned no
  match at all. Wherever an address lookup looked suspicious I used the **coordinates** endpoint
  with the station's Wikipedia coordinate instead, and ran a nearby control address to confirm the
  place layer was working at that location.
- **One coordinate is demonstrably wrong in Wikipedia:** Trinity Lakes station (TRE) is given as
  32.8055,-97.2095, which is west of I-820 and geocodes to Hurst city, while the article text says
  the station is "just to the **east** of Interstate 820". I went with the text + the official TRE
  page (Fort Worth) and logged Hurst as excluded.
- **DeLand / Sanford / Poinciana are genuine source conflicts**, not unverifiable cases: Wikipedia
  and the official SunRail page name the city; the Census boundary says unincorporated. I applied
  the spec's "it is in that municipality" test and excluded them, and flagged all three as parent
  override candidates above.
- Nashville's Census place name is the awkward "Nashville-Davidson metropolitan government
  (balance)"; I output `"Nashville"` and noted it.
- Puerto Rico has no true "incorporated place" layer - municipios are county-equivalents. I output
  the municipio names per the task brief and recorded the corresponding `zona urbana` CDP GEOIDs.

### 2.8 Mountain West, Pacific Northwest, Midwest / Rust Belt

**105 Census places.** 68 `light rail`, 37 `commuter rail`, 0 `subway`.
By state: UT 20, WA 19, CO 18, MO 10, OR 9, NM 8, IL 5, PA 5, OH 4, AZ 3, MN 3, NY 1.

Method note that applies throughout: Wikipedia line/station-list articles supplied the
station->municipality claim, and every non-obvious or boundary case was then re-checked
against the **US Census coordinate geocoder**
(`https://geocoding.geo.census.gov/geocoder/geographies/coordinates`, benchmark
`Public_AR_Current`, vintage `Current_Current`), which returns the containing Incorporated
Place / Census Designated Place polygon. Where the two disagreed I probed a small grid
around the platform and said so below. All 105 output names were validated against the
2024 Census place gazetteer (one exception, Mount Lebanon PA, resolved via the geocoder's
place layer - see below).

---

#### Systems covered

| System | Type assigned | Source URL(s) | How station -> city was established |
|---|---|---|---|
| RTD light rail (D, E, H, L, R, W) | `light rail` | [D](https://en.wikipedia.org/wiki/D_Line_(RTD)) [E](https://en.wikipedia.org/wiki/E_Line_(RTD)) [H](https://en.wikipedia.org/wiki/H_Line_(RTD)) [L](https://en.wikipedia.org/wiki/L_Line_(RTD)) [R](https://en.wikipedia.org/wiki/R_Line_(RTD)) [W](https://en.wikipedia.org/wiki/W_Line_(RTD)) | Every RTD line article carries an explicit **Municipality** (R Line: "Community") column. Verified by geocoder. |
| RTD commuter rail (A, B, G, N) | `commuter rail` | [A](https://en.wikipedia.org/wiki/A_Line_(RTD)) [B](https://en.wikipedia.org/wiki/B_Line_(RTD)) [G](https://en.wikipedia.org/wiki/G_Line_(RTD)) [N](https://en.wikipedia.org/wiki/N_Line_(RTD)) | Same **Municipality** column. Verified by geocoder. |
| UTA TRAX (Blue, Red, Green) | `light rail` | [Blue](https://en.wikipedia.org/wiki/Blue_Line_(TRAX)) [Red](https://en.wikipedia.org/wiki/Red_Line_(TRAX)) [Green](https://en.wikipedia.org/wiki/Green_Line_(TRAX)) | Each line article has a **Municipality** column. All 9 places geocoder-verified. |
| UTA FrontRunner | `commuter rail` | [FrontRunner](https://en.wikipedia.org/wiki/FrontRunner) | Station table has County + city columns. All 15 open stations geocoded. |
| Valley Metro Rail (A, B lines) | `light rail` | [Valley Metro Rail](https://en.wikipedia.org/wiki/Valley_Metro_Rail) | Route description: *"consists of two lines serving 50 stations on 38.5 miles of tracks within the cities of Phoenix, Tempe, and Mesa."* Terminals + boundary stations geocoded. |
| Sound Transit Link (1, 2, T lines) | `light rail` | [List of Link stations](https://en.wikipedia.org/wiki/List_of_Link_light_rail_stations) [1 Line](https://en.wikipedia.org/wiki/1_Line_(Sound_Transit)) [2 Line](https://en.wikipedia.org/wiki/2_Line_(Sound_Transit)) [T Line](https://en.wikipedia.org/wiki/T_Line_(Sound_Transit)) | Station list has a **Location** column; 19 suburban/boundary stations independently geocoded. |
| Sounder | `commuter rail` | [Sounder](https://en.wikipedia.org/wiki/Sounder_commuter_rail) | Station table gives County; all 12 stations geocoded to place. |
| TriMet MAX (5 lines) | `light rail` | [List of MAX stations](https://en.wikipedia.org/wiki/List_of_MAX_Light_Rail_stations) [MAX](https://en.wikipedia.org/wiki/MAX_Light_Rail) | **No city column exists** in the MAX station list, so I geocoded **all 86 station articles** individually. |
| TriMet WES | `commuter rail` | [WES](https://en.wikipedia.org/wiki/Westside_Express_Service) + official [trimet.org/wes/](https://trimet.org/wes/) | Wikipedia station table has a **Location** column; TriMet's own page states *"WES ... is a commuter rail line serving Beaverton, Tigard, Tualatin and Wilsonville."* |
| METRO light rail (Blue, Green) | `light rail` | [Blue](https://en.wikipedia.org/wiki/Blue_Line_(Minnesota)) [Green](https://en.wikipedia.org/wiki/Green_Line_(Minnesota)) | Terminus labels + geocoding of all 14 non-downtown stations. |
| St. Louis MetroLink (Red, Blue) | `light rail` | [List of MetroLink stations](https://en.wikipedia.org/wiki/List_of_MetroLink_(St._Louis)_stations) + official [metrostlouis.org/metrolink/](https://www.metrostlouis.org/metrolink/) | Station list has a **City** column; **all 38 stations geocoded** (5 disagreements resolved below). Metro's own station address list corroborated the Illinois municipalities. |
| Cleveland RTA Rapid Transit (Red, Blue, Green, Waterfront) | `light rail` | [RTA Rapid Transit](https://en.wikipedia.org/wiki/RTA_Rapid_Transit) [Red Line](https://en.wikipedia.org/wiki/Red_Line_(RTA_Rapid_Transit)) | Station list has a **Jurisdiction** column and states outright: *"The stations are fully or partially within the city limits of Cleveland, Shaker Heights, East Cleveland, and Brook Park."* |
| Pittsburgh Light Rail ("the T") | `light rail` | [List of Pittsburgh LR stations](https://en.wikipedia.org/wiki/List_of_Pittsburgh_Light_Rail_stations) | Per-station jurisdiction links; 10 boundary stations geocoded. |
| Buffalo Metro Rail | `light rail` | [Buffalo Metro Rail](https://en.wikipedia.org/wiki/Buffalo_Metro_Rail) | `locale = Buffalo, New York`; lead says the line runs *"from the new DL&W Station in Canalside, to the south campus of the University at Buffalo in the northeast corner of the city."* Single-city system. |
| NM Rail Runner Express | `commuter rail` | [Rail Runner](https://en.wikipedia.org/wiki/New_Mexico_Rail_Runner_Express) | The article has **no station table**, so I enumerated the 15 active stations from Wikipedia's `Category:Railway stations in New Mexico` and geocoded every one. |

---

#### Place-by-place

##### Denver - RTD light rail (`light rail`, "RTD Light Rail")

| Place | State | Station(s) | Source |
|---|---|---|---|
| Denver | CO | 30+ stations on D/E/H/L/R/W | [D Line](https://en.wikipedia.org/wiki/D_Line_(RTD)) |
| Aurora | CO | Dayton, Nine Mile, Iliff, Florida (H); Peoria, Fitzsimons, Colfax, 13th Ave, 2nd Ave & Abilene, Aurora Metro Center (R) | [H Line](https://en.wikipedia.org/wiki/H_Line_(RTD)), [R Line](https://en.wikipedia.org/wiki/R_Line_(RTD)) |
| Lakewood | CO | Red Rocks College, Federal Center, Oak, Garrison, Lakewood-Wadsworth, Lamar, Sheridan (W) | [W Line](https://en.wikipedia.org/wiki/W_Line_(RTD)) |
| Golden | CO | Jefferson County Government Center-Golden (W terminus) | W Line table: `| {{Rtds\|Jefferson County Government Center–Golden}} | [[Golden, Colorado\|Golden]]`; station article short description *"Light rail station in Golden, Colorado"*; geocoder -> Golden city |
| Englewood | CO | Englewood (D) | [D Line](https://en.wikipedia.org/wiki/D_Line_(RTD)); geocoder -> Englewood city |
| Sheridan | CO | Oxford-City of Sheridan (D) | geocoder -> Sheridan city |
| Littleton | CO | Littleton-Downtown, Littleton-Mineral (D) | geocoder -> Littleton city |
| Greenwood Village | CO | Orchard, Arapahoe at Village Center (E/R) | geocoder -> Greenwood Village city |
| Centennial | CO | Dry Creek (E/R) | **Boundary case, see below** |
| Lone Tree | CO | County Line, Lincoln, Sky Ridge, Lone Tree City Center, RidgeGate Parkway (E) | geocoder -> Lone Tree city (County Line, RidgeGate Pkwy) |

##### Denver - RTD commuter rail (`commuter rail`, "RTD Commuter Rail")

| Place | State | Station(s) | Source |
|---|---|---|---|
| Denver | CO | Union Station, 38th & Blake, 40th & Colorado, Central Park, 61st & Peña, Denver Airport (A); 41st & Fox (B/G); 48th & Brighton (N) | already `light rail` - higher tier wins |
| Aurora | CO | Peoria, 40th Ave & Airport Blvd (A) | already `light rail` |
| Westminster | CO | Westminster (B terminus) | geocoder -> Westminster city |
| North Washington | CO | Pecos Junction (B/G) | B and G Line tables both give `[[North Washington, Colorado\|North Washington]]`; geocoder -> **North Washington CDP** (this overrides the station article's `borough = Denver`, which is wrong) |
| Wheat Ridge | CO | Wheat Ridge/Ward (G terminus) | geocoder -> Wheat Ridge city |
| Arvada | CO | Arvada Ridge, Olde Town Arvada, 60th & Sheridan/Arvada Gold Strike (G) | geocoder -> Arvada city |
| Berkley | CO | Clear Creek/Federal (G) | G Line table `[[Berkley, Colorado\|Berkley]]`; station article *"Commuter rail station in Berkley, Colorado"*; geocoder -> **Berkley CDP** |
| Thornton | CO | Eastlake/124th, Thornton Crossroads/104th, Original Thornton/88th (N) | station article *"Commuter rail station in Thornton, Colorado"*; geocoder -> Thornton city |
| Northglenn | CO | Northglenn/112th (N) | geocoder -> Northglenn city |
| Commerce City | CO | Commerce City/72nd (N) | **Boundary case, see below** |

**Denver boundary cases (Colorado cities routinely do not annex highway/rail right-of-way):**

- **Dry Creek station** (Centennial) - the platform point geocodes to unincorporated Arapahoe County, but probes 200 m north, south and west all return `Centennial city` (east returns `Inverness CDP`). Both the E Line and R Line tables name the municipality `Centennial`. **Included.**
- **Commerce City/72nd station** - platform point geocodes to unincorporated Adams County; the probe 200 m east returns `Commerce City city`. The N Line table names `Commerce City`. **Included.**
- **Lincoln station** also geocodes to unincorporated Douglas County, but Lone Tree is already established by County Line and RidgeGate Parkway, so nothing turns on it.

##### Salt Lake City - UTA TRAX (`light rail`, "TRAX")

| Place | State | Station(s) | Source |
|---|---|---|---|
| Salt Lake City | UT | 25 stations across Blue/Red/Green incl. Airport, Salt Lake Central, University Medical Center | [Blue](https://en.wikipedia.org/wiki/Blue_Line_(TRAX)) / [Red](https://en.wikipedia.org/wiki/Red_Line_(TRAX)) / [Green](https://en.wikipedia.org/wiki/Green_Line_(TRAX)) Municipality columns |
| South Salt Lake | UT | Central Pointe, Millcreek, Meadowbrook | geocoder -> South Salt Lake city for all three |
| Murray | UT | Murray North, Murray Central, Fashion Place West | geocoder -> Murray city |
| Midvale | UT | Midvale Fort Union, Midvale Center, Bingham Junction | geocoder -> Midvale city |
| Sandy | UT | Historic Sandy, Sandy Expo, Sandy Civic Center, Crescent View | geocoder -> Sandy city |
| Draper | UT | Kimballs Lane, Draper Town Center | geocoder -> Draper city |
| West Jordan | UT | Historic Gardner, West Jordan City Center, 2700 W Sugar Factory Rd, Jordan Valley, 4800 W Old Bingham Hwy | geocoder -> West Jordan city |
| South Jordan | UT | South Jordan Parkway, South Jordan Downtown, Daybreak Parkway | geocoder -> South Jordan city |
| West Valley City | UT | River Trail, Redwood Junction, Decker Lake, West Valley Central | geocoder -> West Valley City city |

**Millcreek, UT is NOT served.** The TRAX station named "Millcreek" is in South Salt Lake
(geocoder -> `South Salt Lake city` at 40.699606, -111.894007), and the Blue/Red Line
tables both assign it to South Salt Lake. Millcreek city (incorporated 2016) has no station.

##### Salt Lake / Utah Valley - FrontRunner (`commuter rail`, "FrontRunner")

Ogden, Roy, Clearfield, Layton, Farmington, Woods Cross, Lehi, American Fork, Vineyard,
Orem, Provo - all geocoder-verified from the [FrontRunner](https://en.wikipedia.org/wiki/FrontRunner)
station table (one station each, except Salt Lake City which has North Temple + Salt Lake
Central). Salt Lake City, Murray, South Jordan and Draper are also FrontRunner stops but
are already `light rail`, so the higher tier wins.

- **American Fork** - the platform point geocodes to unincorporated Utah County (rail corridor); probes 400 m N, S, NW and SE all return `American Fork city`, and the station article gives `borough = [[American Fork, Utah]]`. **Included.**
- **Pleasant View** - excluded, see below.
- **Pleasant Grove** has no FrontRunner station.

##### Phoenix - Valley Metro Rail (`light rail`)

Phoenix (Metro Parkway ... Baseline/Central + downtown/Washington St), Tempe (Priest Drive,
Center Parkway, Dorsey/Apache Blvd), Mesa (Sycamore, Mesa Drive, Gilbert Road/Main Street).
All six terminal/boundary stations geocoded. *"...within the cities of Phoenix, Tempe, and Mesa."*

##### Seattle - Link light rail (`light rail`, "Link light rail")

| Place | State | Station(s) | Source |
|---|---|---|---|
| Seattle | WA | 20+ stations incl. Judkins Park (2 Line) | Location column |
| Tukwila | WA | Tukwila International Boulevard | geocoder -> Tukwila city |
| SeaTac | WA | SeaTac/Airport, Angle Lake | geocoder -> SeaTac city |
| Kent | WA | **Kent Des Moines, Star Lake** (both opened Dec 6 2025) | geocoder -> `Kent city` for both (47.38944,-122.29444 and 47.35917,-122.29778) |
| Federal Way | WA | **Federal Way Downtown** (opened Dec 6 2025) | geocoder -> Federal Way city |
| Shoreline | WA | Shoreline South/148th, Shoreline North/185th | geocoder -> Shoreline city |
| Mountlake Terrace | WA | Mountlake Terrace | geocoder -> Mountlake Terrace city |
| Lynnwood | WA | Lynnwood City Center (1 Line terminus, Aug 30 2024) | geocoder -> Lynnwood city |
| Bellevue | WA | South Bellevue, East Main, Bellevue Downtown, Wilburton, Spring District, BelRed | geocoder -> Bellevue city |
| Mercer Island | WA | Mercer Island | geocoder -> Mercer Island city |
| Redmond | WA | Overlake Village, Redmond Technology, Marymoor Village, Downtown Redmond | geocoder -> Redmond city |
| Tacoma | WA | 10 T Line stations incl. Tacoma Dome | geocoder -> Tacoma city |

**Des Moines, WA is NOT served** - "Kent Des Moines station" is named for Kent-Des Moines
Road and sits inside Kent (Wikipedia Location column: `Midway, Kent`; geocoder agrees).

##### Puget Sound - Sounder (`commuter rail`, "Sounder commuter rail")

Lakewood, Puyallup, Sumner, Auburn, Edmonds, Mukilteo, Everett - all geocoder-verified.
Tacoma (South Tacoma + Tacoma Dome), Kent, Tukwila and Seattle (King Street) are also
Sounder stops but already `light rail`. **No DuPont station exists** (proposed extension only).
Sounder is still running: the N Line's reduced schedule *"remained at its reduced, two-trip
schedule until service was restored in September 2024."*

##### Portland - MAX (`light rail`, "MAX Light Rail")

All 86 MAX station articles were geocoded. Result, by place:

| Place | State | Stations | Source |
|---|---|---|---|
| Portland | OR | 56 stations | geocoder -> Portland city |
| Beaverton | OR | Beaverton TC, Beaverton Central, Beaverton Creek, Millikan Way, Merlo Road/SW 158th, Elmonica/SW 170th, Sunset TC | geocoder -> Beaverton city |
| Hillsboro | OR | Willow Creek/SW 185th, Quatama, Orenco, Hawthorn Farm, Fair Complex/Hillsboro Airport, Hillsboro Health District, Washington/SE 12th, Hillsboro Central/SE 3rd, Hatfield Government Center | geocoder -> Hillsboro city |
| Gresham | OR | Rockwood/E 188th, Ruby Junction/E 197th, Civic Drive, Gresham City Hall, Gresham Central TC, Cleveland Avenue, E 162nd, E 172nd, E 181st | geocoder -> Gresham city |
| Milwaukie | OR | Milwaukie/Main Street | geocoder -> Milwaukie city |
| Oak Grove | OR | SE Park Avenue (Orange Line terminus) | geocoder -> **Oak Grove CDP** (45.430684, -122.635134) |

**Clackamas is NOT a place.** Clackamas Town Center Transit Center and SE Fuller Road both
geocode to unincorporated Clackamas County with **no CDP**, and Wikipedia confirms Clackamas,
Oregon is a *"Former [[Census-designated place]] (CDP)"* / *"unincorporated community and
former census-designated place"*. Excluded. Gladstone has no MAX station.

##### Portland - WES (`commuter rail`, "WES Commuter Rail")

Beaverton (already `light rail`), Tigard, Tualatin, Wilsonville. TriMet's own page:
*"WES (Westside Express Service) is a commuter rail line serving Beaverton, Tigard,
Tualatin and Wilsonville."*

##### Minneapolis-St Paul - METRO light rail (`light rail`, "METRO light rail")

Minneapolis, **St. Paul** (Census writes it `St. Paul city`), Bloomington
(American Boulevard, Bloomington Central, 30th Avenue, Mall of America).

**Fort Snelling is NOT a Census place.** Fort Snelling, Terminal 1-Lindbergh and
Terminal 2-Humphrey all geocode to unincorporated Hennepin County with no CDP
(county subdivision = the Fort Snelling unorganized territory). Excluded.

##### St. Louis - MetroLink (`light rail`, "MetroLink")

| Place | State | Station(s) | Source |
|---|---|---|---|
| St. Louis | MO | 8th & Pine, Central West End, Civic Center, Convention Center, Cortex, Delmar Loop, Forest Park-DeBaliviere, Grand, Laclede's Landing, Skinker, Stadium, Union Station (+ Shrewsbury-Lansdowne, shared) | City column + geocoder |
| Clayton | MO | Clayton (also Forsyth per Metro's own address list) | geocoder -> Clayton city |
| University City | MO | Forsyth, University City-Big Bend | geocoder -> University City city |
| Wellston | MO | Wellston | geocoder -> Wellston city |
| Maplewood | MO | Maplewood-Manchester, Sunnen | geocoder -> Maplewood city |
| Brentwood | MO | Brentwood I-64 | geocoder -> Brentwood city |
| Richmond Heights | MO | Richmond Heights | geocoder -> Richmond Heights city |
| Shrewsbury | MO | Shrewsbury-Lansdowne I-44 | **see below** |
| Pagedale | MO | Rock Road | City column `[[Pagedale, Missouri]]`; geocoder -> Pagedale city |
| Normandy | MO | UMSL South | geocoder -> Normandy city |
| East St. Louis | IL | 5th & Missouri, East Riverfront, Emerson Park, Jackie Joyner-Kersee Center, Washington Park | City column + geocoder + Metro address list |
| Fairview Heights | IL | Fairview Heights | **see below** |
| Swansea | IL | Swansea | geocoder -> Swansea village |
| Belleville | IL | Belleville, Memorial Hospital, College | geocoder -> Belleville city (Belleville, Memorial Hospital) |
| Shiloh | IL | Shiloh-Scott | geocoder -> Shiloh village |

**Five station-to-city disagreements, all resolved explicitly:**

1. **Shrewsbury-Lansdowne I-44** - the station-list City column says "St. Louis" and the point geocodes to `St. Louis city`, but the station article's short description is *"MetroLink station in **Shrewsbury and St. Louis**, Missouri"* and its street address (7201 Lansdowne Ave, per both Wikipedia and Metro's own list) address-geocodes to 38.5923, -90.3197 -> `Shrewsbury city`. **Both places included.**
2. **Fairview Heights** - point geocodes to `East St. Louis city`, but probes 400 m north and east return `Fairview Heights city`, the station article is *"MetroLink station in Fairview Heights, Illinois"* with `borough = Fairview Heights`, and Metro's own address list gives *"Fairview Heights 9720 W. Route 161, Fairview Heights, IL 62208"*. **Included.**
3. **North Hanley -> Berkeley: EXCLUDED.** Three sources give three answers - station list says Berkeley, station article short description says "Carsonville" (not a 2024 Census place), `borough` says "St. Louis, Missouri". The address 4300 N Hanley Rd address-geocodes to 38.71961, -90.31710 = **unincorporated St. Louis County** (Berkeley 400 m N and W, Cool Valley 400 m E). Cannot confirm -> left out.
4. **UMSL North -> Bellerive Acres: EXCLUDED.** The platform straddles Bellerive Acres / Normandy at ~40 m scale (probes flip between the two). Station article says Normandy, which is already in via UMSL South. Cannot confirm Bellerive Acres -> left out.
5. **Washington Park station -> Washington Park village: EXCLUDED.** The station-list City column says `[[Washington Park, Illinois]]`, but the station article's `borough = [[East St. Louis, Illinois]]` and the article coordinate geocodes to `East St. Louis city`. The village boundary is ~150 m north. Two of three sources say East St. Louis -> left out and logged. East St. Louis is in the dataset regardless.

##### Cleveland - RTA Rapid Transit (`light rail`, "RTA Rapid Transit")

Cleveland, Shaker Heights, East Cleveland (Superior, Windermere - Red Line),
Brook Park (Brookpark - Red Line).

Direct quote from the station list: *"The stations are fully or partially within the city
limits of Cleveland, Shaker Heights, East Cleveland, and Brook Park."*

- **Cleveland Heights is NOT served.** Zero occurrences of "Cleveland Heights" in the station list; Coventry station's Jurisdiction is `Cleveland / Shaker Heights` and it geocodes to Shaker Heights city.
- **Brookpark station** straddles the line - Jurisdiction column reads `Cleveland / Brook Park`; the point geocodes to Cleveland city, probes 300 m S and E return `Brook Park city`. Included on the strength of the article's explicit statement.

**My mode call, stated as instructed:** Cleveland RTA is genuinely two systems. The **Red
Line is heavy-rail rapid transit** (high platforms, near-full grade separation, its own
right-of-way) while the **Blue, Green and Waterfront lines are light rail** - the article's
own caption reads *"RTA Rapid Transit heavy rail (left) and light rail (right) trains"* and
its infobox lists `transit_type = Rapid transit / Light rail`. I assigned **`light rail` to
all four places**, for two reasons: the brief puts Cleveland under light rail, and the spec
enumerates exactly which systems count as `"subway"` and Cleveland RTA is not among them.
The consequence worth flagging: **East Cleveland and Brook Park are served *only* by the
heavy-rail Red Line**, so on a strict mode reading those two (and Cleveland) would be
`subway`. Shaker Heights would remain `light rail` either way.

##### Pittsburgh - the T (`light rail`, "Pittsburgh Light Rail")

Pittsburgh (26 stations), Bethel Park (23), Castle Shannon (8), Dormont (4),
Mount Lebanon (2: Mt. Lebanon, Poplar). All geocoder-verified.

- **Whitehall, Baldwin, Upper St. Clair and South Park are NOT served.** Whitehall and Baldwin have no station at all. Walthers station (Upper St. Clair) is in the **former/closed** station table (closed Sept 5 1999), as is Brookside Farms.
- **Library station -> "South Park": EXCLUDED as a place.** The station geocodes to unincorporated Allegheny County, `County Subdivisions -> ['South Park township']`, **no incorporated place and no CDP**. PA townships are Minor Civil Divisions, not Census places. The station-list article assigns Library to Bethel Park, which is already in the dataset.
- **Mount Lebanon** is a home-rule township that the Census *does* treat as an incorporated place - `Incorporated Places -> [('Mount Lebanon municipality', '4251794')]`. It is missing from the local 2024 gazetteer file, so I verified the geocoder's place layer is trustworthy for PA by testing it against two real townships: Upper St. Clair and South Park both return `Incorporated Places -> []`, while Bethel Park and Mount Lebanon both return a place GEOID.

##### Buffalo - Metro Rail (`light rail`)

Buffalo only. 14 stations, `locale = Buffalo, New York`, every station in a Buffalo
neighbourhood (University Heights, North Park, Allentown, Canalside, ...).

##### New Mexico - Rail Runner Express (`commuter rail`)

All 15 active stations enumerated from `Category:Railway stations in New Mexico` and geocoded:

| Place | State | Station(s) | Geocoder result |
|---|---|---|---|
| Belen | NM | Belen | Belen city |
| Los Lunas | NM | Los Lunas | Los Lunas village |
| South Valley | NM | Bernalillo County/International Sunport | **South Valley CDP** (35.03028, -106.65722) |
| Albuquerque | NM | Downtown Albuquerque (Alvarado) | Albuquerque city |
| North Valley | NM | Montaño, Los Ranchos/Journal Center | **North Valley CDP** (both; 5-point probe on Los Ranchos/Journal Center returned North Valley CDP at every point) |
| Edith Enclave | NM | Sandia Pueblo | **Edith Enclave CDP** (5-point probe, all points) |
| Bernalillo | NM | Downtown Bernalillo, Sandoval County/US 550 | Bernalillo town |
| Santa Fe | NM | Santa Fe County/NM 599, Zia Road, South Capitol, Santa Fe Depot | Santa Fe city |

- **Los Ranchos de Albuquerque is NOT served** - the "Los Ranchos/Journal Center" station is in North Valley CDP, not the village.
- **Isleta Pueblo and Kewa (Santo Domingo Pueblo) stations: EXCLUDED.** Both geocode to unincorporated land with **no CDP**, even on a +/-1 km probe. `Isleta CDP`, `Santo Domingo Pueblo CDP` and `Pueblo of Sandia Village CDP` all exist in the gazetteer but none of them contains the respective station. Handled as the task asked: excluded with reason rather than guessed.

---

#### Streetcar / borderline judgements

| System | Call | Why | Source |
|---|---|---|---|
| **UTA S Line** (Sugar House streetcar) | **Borderline; no effect on output** | Genuinely runs on **exclusive right-of-way** (the former D&RGW freight alignment UTA bought in 2002), not mixed street traffic - so it is not the "downtown loop" case the spec excludes. But it is only 2 mi, single track with passing tracks, 25 mph max, 7 stations, 1,246 daily riders - functionally a streetcar. **Moot either way:** its two municipalities (Salt Lake City, South Salt Lake) both already qualify via TRAX. Not counted as an independent qualifier. | [S Line](https://en.wikipedia.org/wiki/S_Line_(Utah_Transit_Authority)) |
| **Tempe Streetcar** (Valley Metro S Line) | **Excluded** | Valley Metro's own line table types it `Streetcar` (vs `Light rail` for A and B). Named in the spec's exclusion list. Tempe already qualifies via the A Line, so no place is lost. | [Valley Metro Rail](https://en.wikipedia.org/wiki/Valley_Metro_Rail) |
| **Seattle Streetcar** (South Lake Union, First Hill) | **Excluded** | Mixed-traffic downtown circulators sharing lanes with cars; both entirely inside Seattle, which already qualifies via Link. No place lost. | [Seattle Streetcar](https://en.wikipedia.org/wiki/Seattle_Streetcar) |
| **Portland Streetcar** (A/B/NS Loops) | **Excluded** | Mixed street traffic in inner Portland; entirely inside Portland, which already qualifies via MAX. No place lost. | [Portland Streetcar](https://en.wikipedia.org/wiki/Portland_Streetcar) |
| **Detroit QLINE** | **Excluded** | *"a 3.3 mi streetcar system ... running along Woodward Avenue for its entire route"* - mixed traffic, explicitly named in the spec's exclusion list. | [QLINE](https://en.wikipedia.org/wiki/QLine) |
| **Detroit People Mover** | **Excluded** | `transit_type = [[People mover\|Automated people mover]]`; an elevated automated downtown circulator. Spec rule 4 excludes people-movers. | [Detroit People Mover](https://en.wikipedia.org/wiki/Detroit_People_Mover) |
| **Milwaukee "The Hop"** | **Excluded** | *"a modern streetcar system"*, 2.1 mi M-Line + 0.4 mi L-Line downtown, mixed traffic. Named in the spec's exclusion list. | [The Hop](https://en.wikipedia.org/wiki/The_Hop_(streetcar)) |
| **KC Streetcar** | **Excluded** | *"a one-route streetcar system in Kansas City, Missouri"*, free-to-ride Main Street alignment in mixed traffic. Named in the spec's exclusion list. Extended 3.5 mi south to UMKC in **October 2025** and 0.7 mi north to Berkley Riverfront Park in **May 2026** - still a streetcar, still excluded. | [KC Streetcar](https://en.wikipedia.org/wiki/KC_Streetcar) |
| **Monongahela / Duquesne Inclines** (Pittsburgh) | **Excluded** | Funiculars. Spec rule 4 excludes funiculars/inclines outright. | spec rule 4 |
| **Las Vegas Monorail** | **Excluded - flagged for the caller** | Not in my assigned scope (Nevada was not named), and it is a 3.9 mi **automated monorail** resort circulator linking Strip casinos, closest in kind to the people-movers the spec excludes. If the caller decides it qualifies, the places would be **Paradise CDP** and **Winchester CDP**, Clark County NV - per the lead: *"It connects several large casinos in the unincorporated communities of Paradise and Winchester just south of Las Vegas city limits."* Still operating (LVCVA funded it to 2035 in May 2025). Raising it rather than deciding unilaterally, because the spec's own `cdp_notes` examples name "Paradise NV", which suggests someone is expected to cover it. | [Las Vegas Monorail](https://en.wikipedia.org/wiki/Las_Vegas_Monorail) |

---

#### Deliberately excluded

| Thing | Why |
|---|---|
| **Northstar Line** (Minneapolis, Fridley, Coon Rapids, Anoka, Ramsey, Elk River, Big Lake) | **DISCONTINUED.** `close = 2026-01-04`. *"In August 2025, Metro Transit officially announced the termination of the line in favor of bus service."* Metro Transit's own page: *"More frequent and flexible bus service began Jan. 5, 2026 ... Metro Transit has transitioned from commuter rail to expanded bus service."* Fridley, Coon Rapids, Anoka, Ramsey, Elk River and Big Lake therefore have **no** rapid transit. Minneapolis keeps `light rail`. |
| **METRO Green Line Extension** (St. Louis Park, Hopkins, Minnetonka, Eden Prairie) | Not open. `status = Under construction`, `open = 2027`, 16 stations planned. |
| **MetroLink MidAmerica Airport extension** (Mascoutah IL) | Not open. Listed under "Projects in progress"; *"expected to be operational in early 2026"*; absent from the 38-station current table. |
| **Link Pinehurst infill station** (Seattle) | Not open - *"An infill station at Pinehurst is scheduled to open in 2026."* Seattle already qualifies. |
| **Link / Sounder future extensions** (Everett Link, Tacoma Dome Link incl. Fife, West Seattle, Ballard, Kirkland, Issaquah; DuPont) | Not open (2032-2044 targets). Everett and Tacoma already qualify via Sounder / T Line. |
| **RTD B Line north of Westminster** (Boulder, Longmont, Louisville, Broomfield) | Proposed only - all six stations flagged `''Proposed''`, target 2042. |
| **RTD N Line north of Eastlake** (North Thornton/Hwy 7, York/144th) | Proposed, 2042. Thornton already qualifies. |
| **RTD D Line extension** (Highlands Ranch, C-470 & Lucent) | Never built - *"station construction has received insufficient funding. There is no clear date."* |
| **TRAX Highland and 14600 South stations** (Draper) | `Planned (no scheduled date)`. Draper already qualifies. |
| **Pleasant View, UT** (FrontRunner) | Station is greyed out as *"Temporarily closed"* - *"Service suspended August 12, 2018; expected to resume in the future."* Not open to passengers. |
| **Des Moines, WA** | Kent Des Moines station is inside Kent (Location column: `Midway, Kent`; geocoder: `Kent city`). |
| **Millcreek, UT** | The TRAX "Millcreek station" is in South Salt Lake. |
| **Cleveland Heights, OH** | No station. Coventry station's jurisdiction is `Cleveland / Shaker Heights`. |
| **Whitehall / Baldwin / South Park Twp / Upper St. Clair, PA** | Whitehall and Baldwin have no station. Walthers (Upper St. Clair) and Brookside Farms are closed stations. Library station is in South Park **township**, an MCD with no incorporated place and no CDP at that point. |
| **Clackamas / Gladstone, OR** | Clackamas Town Center TC and SE Fuller Road geocode to unincorporated Clackamas County with no CDP; Clackamas is a **former** CDP. Gladstone has no station. |
| **Fort Snelling, MN** | Fort Snelling, Terminal 1-Lindbergh, Terminal 2-Humphrey all geocode to unincorporated Hennepin County, no CDP (Fort Snelling unorganized territory). |
| **Berkeley / Bridgeton, MO** | Lambert Airport Terminal 1 and Terminal 2 geocode to **unincorporated** St. Louis County airport land (nearest neighbours Edmundson and St. Ann, not Berkeley or Bridgeton). North Hanley geocodes to unincorporated county (see disagreement #3 above). No station verifiably inside either city. |
| **Washington Park, IL** | Sources conflict (station list says the village; station article `borough` and the Census polygon at the article coordinate both say East St. Louis, whose boundary the platform sits on). Left out per spec rule 1. |
| **Bellerive Acres, MO** | UMSL North straddles the Bellerive Acres / Normandy line at ~40 m; cannot confirm. Normandy included instead. |
| **Los Ranchos de Albuquerque, NM** | The "Los Ranchos/Journal Center" station is in North Valley CDP (5-point probe, unanimous). |
| **Isleta Pueblo and Kewa (Santo Domingo Pueblo) stations, NM** | Both on pueblo land - geocode to no incorporated place and no CDP even at +/-1 km. |
| **RTD R Line Sky Ridge / Lone Tree City Center / RidgeGate Pkwy** | Noted as *"Indefinitely closed in 2020"* **on the R Line**, but they are open and served by the E Line, so Lone Tree stands. |
| **Denton A-train, South Shore Line / West Lake Corridor (IN), Cincinnati Bell Connector, Kenosha heritage streetcar, Amtrak Cascades / Hiawatha / Winter Park Express, ABQ Rapid Transit, METRO Orange/Red/A/C/D Lines (MSP), HealthLine (Cleveland)** | Out of my region (Denton TX, South Shore = Chicago metro - already fetched by another agent, do not double-count), or excluded by spec rule 4/5 (streetcar, heritage trolley, intercity Amtrak, BRT). |

---

#### Sourcing limitations

| Official site | Result | Fallback |
|---|---|---|
| `rtd-denver.com/app/facilities` | **Served** (200 after following a 308 redirect, 560 KB) | Not needed - Wikipedia line articles all carry Municipality columns |
| `rideuta.com` | **Served** (200). The specific `/Rider-Info/Frontrunner-Stations` path returns a **soft 404** ("Route 404. Missed your stop? This stop is discontinued...") | Wikipedia FrontRunner station table + Census geocoder |
| `valleymetro.org/maps-schedules/rail` | **BLOCKED - HTTP 403** with both a Chrome UA and `curl/8.0` | Wikipedia [Valley Metro Rail](https://en.wikipedia.org/wiki/Valley_Metro_Rail) route description + geocoder |
| `soundtransit.org/ride-with-us/stops-stations` | **Served** (200, 86 KB) | Wikipedia station list used as primary (it has a Location column) |
| `trimet.org/wes/` | **Served** - quoted directly above; **this was the decisive official source for WES** | - |
| `trimet.org/max/` | Served (200) | Wikipedia list + geocoding of all 86 stations (no city column anywhere) |
| `metrotransit.org/northstar` | **Served** - quoted directly; **this was the decisive official source for the Northstar shutdown** | - |
| `metrostlouis.org/metrolink/` | **Served, but partial.** Its station address list renders only ~34 of 38 stations - Skinker, Stadium, Sunnen and **Washington Park** are absent from the HTML, so it could not settle the Washington Park question | Wikipedia station list + Census coordinate and address geocoders |
| `riderta.com/rail` and `riderta.com/routes/red` | **404** | Wikipedia [RTA Rapid Transit](https://en.wikipedia.org/wiki/RTA_Rapid_Transit) - which has an explicit Jurisdiction column and a plain-language sentence naming all four cities |
| `rideprt.org/rider-guide/...` | **404** on both paths tried | Wikipedia Pittsburgh station list + geocoder |
| `metro.nfta.com` | Root served (200); `/Rail/` **404** | Wikipedia Buffalo Metro Rail |
| `riometro.org` | Root served (200); `/70/Stations` **404** | Wikipedia + `Category:Railway stations in New Mexico` + geocoder |
| `qlinedetroit.com`, `thehopmke.com`, `kcstreetcar.org` | Served (200) | Only needed for the exclusion calls, which the Wikipedia leads state plainly |

**Other limitations worth flagging:**

- The local `work/2024_Gaz_place_national.txt` gazetteer is **missing Mount Lebanon municipality PA** even though it is a real Census place (GEOID 4251794). I validated all 105 output names against that file; Mount Lebanon was the only miss, and I confirmed it independently via the geocoder's Incorporated Places layer with a control test on two genuine townships. Anyone else using that file should not treat absence as proof.
- `api.census.gov/data/.../acs5` returned non-JSON (needs a key) - not used.
- `validator`-style bulk address geocoding failed for two addresses ("8298 Bellerive Drive" and "9720 West Illinois Route 161" -> NO MATCH), which is why those two cases rest on coordinate probes plus article/official text instead.

---

## PART 3 - DELIBERATELY EXCLUDED

### 3.1 Sports - deliberately excluded

| Excluded | Why |
|---|---|
| **Oakland, CA** | Has no top-tier team in any of the seven leagues. The Athletics left for West Sacramento in 2025 (see 1.2), the Raiders left for Paradise NV in 2020, the Warriors left for San Francisco in 2019. Including Oakland would be the single most common stale-data error in this dataset. |
| **Fort Lauderdale, FL** | Lost Inter Miami CF when Nu Stadium opened in Miami in April 2026. https://en.wikipedia.org/wiki/Nu_Stadium |
| **Bridgeview, IL** | Lost the Chicago Stars when the SeatGeek Stadium lease expired; they moved to Evanston for 2026. https://en.wikipedia.org/wiki/Chicago_Stars_FC |
| **Dallas, TX - WNBA** | Verified but deliberately not recorded. The Dallas Wings' home is College Park Center in Arlington; in 2026 they also played a handful of home games at American Airlines Center in Dallas (the July 12 win over Chicago drew 13,236 there, and August 7 and August 20 are also scheduled at AAC). https://en.wikipedia.org/wiki/2026_Dallas_Wings_season - infobox *"arena = College Park Center / American Airlines Center"*. A three-game secondary venue does not make Dallas a WNBA host, so the Wings are keyed only to Arlington TX. Dallas still appears with the NBA Mavericks and NHL Stars. |
| **Pawtucket, RI - NWSL** | Same reasoning. Boston Legacy FC's inaugural home is Gillette Stadium, but https://en.wikipedia.org/wiki/Boston_Legacy_FC says *"Seven of the team's fifteen home matches will be played at Centreville Bank Stadium in Pawtucket, Rhode Island, due to scheduling conflicts at Gillette Stadium during the 2026 FIFA Men's World Cup."* That is a one-season World Cup artifact, not a home city, so it is logged here and left out of the JSON. Pawtucket **is** in the dataset for MBTA commuter rail. |
| **Boston, MA - NWSL** | Boston Legacy FC's permanent home will be a renovated White Stadium in Boston, but the club article says the renovations *"will not be completed in time for the first season"*. Boston is in the dataset for NBA/MLB/NHL only. Add NWSL when White Stadium opens. |
| **Houston, TX - WNBA** | The Connecticut Sun's intended relocation to revive the Houston Comets is 2027 at the earliest. No game has been played. Houston keeps NFL/NBA/MLB/MLS/NWSL = 5 leagues. |
| **Brook Park, OH** ; **Everett, MA** ; **Plano, TX** ; **Kansas City, KS (NFL)** ; **Queens, NY (Etihad Park)** | All future venues in the leagues' own "future stadiums / under construction" tables. Nothing built, nothing counted. |
| **Auburn Hills, MI** | The Pistons' old home. They have played in Detroit since 2017. |
| **Atlanta, GA - MLB** ; **Uniondale, NY - NHL** ; **Anaheim, CA - NFL** | Teams that used to be there and are not. |
| **NBA G League, AHL, MiLB, USL, MLR, PLL, NLL, indoor/arena football, CFL, PWHL, college** | Not in the seven requested leagues and not top-tier US majors. Adding any of them would change many `pro_league_count` values, so they are flagged rather than silently included. |
| **Toronto Blue Jays / Raptors / Tempo / FC, CF Montréal, Vancouver Whitecaps, and the seven Canadian NHL clubs** | Canadian. Already covered by `data/civic.json`; this file is US-only. |

### 3.2 Transit - excluded

Every regional log above carries its own
`Deliberately excluded` table (unopened extensions, BRT, people movers, heritage
streetcars, stations whose municipality could not be pinned down). Those tables are the
authoritative list and are not duplicated here. The cross-cutting calls were:

- **Bus rapid transit is never rail.** Excludes the MBTA Silver Line (which is why
  Chelsea MA is commuter rail only), and every BRT-only city.
- **Automated people movers and airport trams are not rapid transit.** Excludes
  Miami's Metromover and the Detroit People Mover.
- **Funiculars and cable cars are not rapid transit.** Excludes the Duquesne and
  Monongahela Inclines and the San Francisco cable cars.
- **Nothing that has not opened to passengers.** Each log names the specific projects.
- **Mixed-traffic downtown streetcars are not light rail.** See each log's judgement
  table for the individual calls and their sources.

---

## PART 4 - PLACE-NAMING RULES AND SOURCING LIMITATIONS, STATED PLAINLY

### 4.1 What counts as a "place"

`name` is a US Census **place** name with no state suffix. That layer includes both
incorporated municipalities and **Census Designated Places** (CDPs), which are
unincorporated communities the Census still names. CDPs are kept, because a
"where should I live" app that dropped Silver Spring, Bethesda, Paradise, Elmont, Cumberland
and Willowbrook would be worse, not purer. Where a record's place is unincorporated or its
municipality is non-obvious, the record carries a `cdp_notes` string saying so.

Consequences worth knowing before you join this file to anything:

- **New England**: the town, not the village, is the place. Brookline, Weston, Hingham,
  Cherry Hill, Upper Darby are towns/townships. Massachusetts' Census place layer alone
  would drop most station towns, so town names are used throughout.
- **New York City boroughs are not places.** Brooklyn, Queens, the Bronx and Staten Island
  all collapse to `"New York", "NY"`. That is why the Nets, Knicks, Mets, Yankees, Rangers,
  NYCFC and Liberty all land on one record with 7 teams.
- **Long Island** is mostly unincorporated hamlets recorded as CDPs. They are included as
  CDPs with the town in `cdp_notes`.
- **Ambiguous names are disambiguated by `state`, and both halves exist in this file:**
  Arlington **TX** (Cowboys, Rangers, Wings) vs Arlington **VA** (Washington Metro, VRE).
  Kansas City **MO** (Chiefs, Royals, KC Current) vs Kansas City **KS** (Sporting KC).
  Columbia **MD** vs nothing in SC. Aurora **IL** (Metra) vs Aurora **CO** (RTD).
  Springfield **MA** vs Springfield **VA**. Glendale **AZ** (Cardinals) vs Glendale **CA**.
- **Washington DC** uses `state: "DC"`.
- **Puerto Rico** uses `state: "PR"` with the municipio name.

Sports records that sit in an unincorporated or easily-mistaken place:

| Place | Status | Note |
|---|---|---|
| Paradise, NV | CDP, unincorporated Clark County | The Las Vegas Strip is not in the City of Las Vegas. Holds the Raiders, Golden Knights and Aces. |
| Cumberland, GA | CDP, unincorporated Cobb County | Truist Park / the Braves. |
| Landover, MD | CDP, unincorporated Prince George's County | Northwest Stadium / the Commanders. |
| Elmont, NY | CDP in the Town of Hempstead | UBS Arena / the Islanders. |
| Uncasville, CT | CDP in the Town of Montville | Mohegan Sun Arena / the Connecticut Sun. The arena itself is on the Mohegan Reservation; Wikipedia's venue infobox gives the postal place as Uncasville and the team article's location field as Montville. `Uncasville` was chosen because it is the venue's own address; if your place layer is CT towns, map it to Montville. |
| Orchard Park, NY | Town in Erie County | Highmark Stadium / the Bills. There is also an Orchard Park **village** inside the town; the stadium is in the town, outside the village. |
| Foxborough, MA | Town in Norfolk County | Gillette Stadium. Spelled "Foxborough" (the town); the MBTA station is spelled "Foxboro". |
| Centennial, CO | City, incorporated 2001 | Centennial Stadium / Denver Summit FC. |
| West Sacramento, CA | City in Yolo County | Sutter Health Park / the Athletics. Not Sacramento, which is across the river in Sacramento County. |
| College Park, GA | City in Fulton/Clayton | Gateway Center Arena / the Atlanta Dream. Distinct from College Park **MD**, which is in this file for the Washington Metro and MARC. |

### 4.2 Sourcing limitations

1. **Wikipedia is the backbone, and that is a deliberate, stated choice.** The brief allowed
   it, and it is the only source that publishes a station-to-municipality mapping for every
   system in one comparable format. Every quoted line was pulled as raw wikitext from the
   MediaWiki API during this build, not recalled.
2. **Some official agency sites did serve, and where they did they were used as a second
   independent source.** The clearest case is the **MBTA v3 API**
   (`https://api-v3.mbta.com/stops`), which returns a `municipality` field per stop; all 143
   active MBTA commuter-rail stations were re-derived from it and agreed with Wikipedia on
   every one. Other agency sites that served or blocked are named in their regional log.
3. **Venue `location =` fields are single-source for a handful of non-controversial cases.**
   Where a venue's city was not itself the interesting fact (e.g. Ball Arena in Denver), the
   league's stadium-list row was accepted on its own. Every *trap* case in 1.3 was resolved
   against the venue's own article as well as the league list.
4. **One venue's two sources disagree.** Michelob Ultra Arena's short description says
   "Las Vegas" while its `location` field and street address say Paradise. The location
   field and address won. Same underlying fact as Allegiant Stadium and T-Mobile Arena,
   both of which say Paradise unambiguously.
5. **Split-venue seasons are a real and awkward 2026 phenomenon** because of the FIFA World
   Cup. NYCFC split between Yankee Stadium and Citi Field (both New York NY, so no effect);
   the Dallas Wings split Arlington/Dallas; Boston Legacy split Foxborough/Pawtucket. The
   rule applied was **primary home venue only**, with the secondary venue logged in 3.1
   rather than silently included or silently dropped.
6. **`pro_league_count` counts distinct leagues, not teams.** Chicago has 7 teams across 6
   leagues (two MLB clubs), New York has 7 teams across 5 leagues, Los Angeles 6 across 6.
7. **This file does not attempt to be a complete list of US Census places.** Only places
   with at least one verified attribute are present. A place absent from this file should be
   read as "no verified top-tier team and no verified rail rapid transit", not as
   "does not exist".
8. **No Canadian data was read, written or modified.** `data/civic.json` and
   `research/civic-sources.md` were opened read-only to copy the schema.

### 4.3 The one place-name I am not confident about

**`"Morris", "NJ"`** - NJ Transit's Convent Station is in **Morris Township**, Morris
County. New Jersey townships are Census *minor civil divisions*, not places, and the
Census place layer has no CDP for Convent Station, so stripping "Township" per the naming
rule produced the bare word "Morris". That is very likely **not** a Census place name.
Treat it as Morris Township, Morris County, NJ, or drop the record; it is the single
weakest key in the file and it is flagged rather than quietly shipped.

The same NJ/PA township problem is handled cleanly everywhere else because a CDP exists
for the station's community (Iselin, Whippany, Ardmore, Bryn Mawr, Villanova, Wayne,
Cherry Hill, Upper Darby), and those CDP names are what the file uses.

### 4.4 The "postal city is not the municipality" problem, and four override candidates

Wikipedia's `{{Short description}}` and `address =` fields give a station's **postal** city,
which is not the same thing as the municipality whose boundary contains it. That difference
was caught during review by reverse-geocoding station coordinates through the
**US Census geocoder** (`geocoding.geo.census.gov/geocoder/geographies/coordinates`), which
returns the actual place polygon a point falls in. Two regional logs used that method as
their primary resolver (LIRR/Metro-North, and Texas/South/Florida), and it repeatedly
disagreed with the prose.

The clearest cases are four SunRail stations. All four are named for, and serve, a real
city, and all four sit in **unincorporated county land just outside** it:

| Station | Postal city per Wikipedia | Census geocoder result | Call |
|---|---|---|---|
| Sanford (SunRail) | "Rail station in Sanford, Florida" | no place at 28.813168,-81.298673; a downtown Sanford control address does return "Sanford city" | **excluded** |
| DeLand | "Passenger train station in DeLand, Florida" | no place at 29.017806,-81.35272; downtown DeLand control returns "DeLand city". Article also says "located west of the downtown area" | **excluded** |
| Poinciana | "in the community of Poinciana, Florida" | no place at 28.258829,-81.484368; a Poinciana residential control returns "Poinciana CDP" | **excluded** |
| Tupperware | "Commuter rail station in Hunter's Creek, Florida" | no place; and the article simultaneously calls it "the northernmost SunRail station in Osceola County" while Hunter's Creek CDP is in **Orange** County | **excluded** |

These are the four rows most likely to be wanted back. If the app's rule is "the city this
station is built to serve" rather than "the polygon the platform sits in", add
`Sanford FL`, `DeLand FL`, `Poinciana FL` and `Hunters Creek FL` as `commuter rail` /
`SunRail` and cite https://en.wikipedia.org/wiki/SunRail plus the station article. They are
flagged rather than silently dropped precisely because the call could reasonably go the
other way. The strict-boundary rule was applied for consistency with every other region.

### 4.5 Every name was checked against the official Census Gazetteer

After the merge, all 1,056 `name` + `state` pairs were checked programmatically against the
**US Census Bureau national place Gazetteer**, both the 2024 and the 2020 vintage
(`2024_Gaz_place_national.txt`, `2020_Gaz_place_national.txt`, 32,334 and 31,910 rows),
comparing against each row's `NAME` with its LSAD class word ("city", "town", "village",
"CDP", "zona urbana", ...) stripped.

**954 of 1,056 (90.3%) match a real Census place name exactly.** The 102 that do not break
down into two groups, and neither is an error of fact:

**(a) 98 rows are New England towns or Mid-Atlantic townships (expected).** These are real
municipalities that the Census classifies as *minor civil divisions*, not places, so they
cannot appear in the place Gazetteer no matter how correct they are:
MA 28, NJ 29, PA 18, CT 16, NY 6, RI 1. Examples: Weston MA, Westport CT, Upper Darby PA,
Cherry Hill NJ, Philipstown NY, North Kingstown RI. Dropping them would delete most of the
MBTA, Metro-North, SEPTA Regional Rail and NJ Transit suburb coverage, which is the whole
point of the dataset. They are kept, and every one has a `cdp_notes` entry in the appendix
naming the township or town.

**(b) 4 rows are genuine naming flags. Fix these first if the app hard-joins on Census names:**

| In this file | Census Gazetteer actually says | Comment |
|---|---|---|
| `Ventura`, CA | **`San Buenaventura (Ventura) city`** | Metrolink Ventura / Ventura-East stations. Everyone calls it Ventura; the Census does not. Rename if you join on the Gazetteer. |
| `Nashville`, TN | **`Nashville-Davidson metropolitan government (balance)`** | Consolidated city-county. `Nashville` is the usable name; the Gazetteer form is unusable in a UI. |
| `Cumberland`, GA | **no GA place by that name in either the 2020 or 2024 Gazetteer** | Truist Park / the Atlanta Braves. Wikipedia's venue infobox pins the location to "Cumberland, Georgia" with an explicit editor note not to change it, and Cumberland was a CDP in earlier vintages, but it is not in the current place layer - the ballpark sits in unincorporated Cobb County. Kept because the venue source is unambiguous, flagged because the key may not resolve. |
| `Rancho Dominguez`, CA | Gazetteer has only **`East Rancho Dominguez CDP`** and **`West Rancho Dominguez CDP`** | LA Metro A Line Del Amo station. The unincorporated community "Rancho Dominguez" exists but the Census splits it, and the station is in the industrial area between the two CDPs. The weakest transit key in the file. |

The checker is reproducible: it reads `data/us/civic.json` and the two Gazetteer files and
prints the unmatched rows with the system or leagues that put each one in the file.

---

## APPENDIX - unincorporated / non-obvious places

`data/us/civic.json` carries only the nine fields the Canadian file carries, so the
per-place municipality notes the research produced are recorded here instead. 520 places needed one.

| Place | State | Note |
|---|---|---|
| Acton | CA | Unincorporated Acton CDP; Vincent Grade/Acton station on the Antelope Valley Line. |
| Beverly Hills | CA | Wilshire/La Cienega station (D Line Extension Section 1) opened May 8, 2026 - Beverly Hills' first Metro Rail station. |
| Brisbane | CA | Bayshore station straddles the San Francisco/Brisbane line; the platform itself is in Brisbane (parking lot in San Francisco). |
| Castro Valley | CA | Unincorporated Castro Valley CDP, Alameda County; Castro Valley station. |
| Contra Costa Centre | CA | Pleasant Hill/Contra Costa Centre station is in the unincorporated Contra Costa Centre CDP, not in the city of Pleasant Hill. |
| East Los Angeles | CA | Unincorporated East Los Angeles CDP; E Line Atlantic, East LA Civic Center, Maravilla stations. |
| Florence-Graham | CA | Unincorporated Florence-Graham CDP (Firestone, Florence, Slauson A Line stations); the CDP covers the Florence, Firestone Park and Graham communities. |
| Glendora | CA | A Line Foothill Extension Phase 2B (Azusa-Pomona) opened September 19, 2025. |
| Gold River | CA | Unincorporated Gold River CDP, Sacramento County; Hazel station. |
| Industry | CA | Census place 'Industry' (City of Industry); Industry station on the San Bernardino Line. |
| La Riviera | CA | Unincorporated La Riviera CDP, Sacramento County; Butterfield and Tiber stations. |
| La Verne | CA | A Line Foothill Extension Phase 2B (Azusa-Pomona) opened September 19, 2025. |
| Laguna Niguel | CA | Laguna Niguel/Mission Viejo station; Wikipedia's station list locates it in Laguna Niguel. Mission Viejo itself is not separately sourced, so it is excluded. |
| North Highlands | CA | Unincorporated North Highlands CDP, Sacramento County; Watt/I-80 station. |
| Oceanside | CA | Oceanside Transit Center has SPRINTER (judged light rail), plus COASTER and two Metrolink lines; highest tier wins. |
| Pomona | CA | A Line Foothill Extension Phase 2B (Azusa-Pomona) opened September 19, 2025. |
| Rancho Dominguez | CA | Unincorporated Rancho Dominguez CDP; A Line Del Amo station is here, near but not inside the city of Carson. |
| Rosemont | CA | Unincorporated Rosemont CDP, Sacramento County; Starfire and Watt/Manlove stations. |
| San Dimas | CA | A Line Foothill Extension Phase 2B (Azusa-Pomona) opened September 19, 2025. |
| San Martin | CA | Unincorporated San Martin CDP, Santa Clara County. |
| Ventura | CA | Ventura-East station. The Census writes this place as 'San Buenaventura (Ventura)'. |
| Willowbrook | CA | Unincorporated Willowbrook CDP; Willowbrook/Rosa Parks station (A and C Lines). |
| Berkley | CO | Unincorporated CDP in Adams County; Clear Creek/Federal station geocodes to Berkley CDP. |
| Centennial | CO | Dry Creek station platform sits in the unannexed I-25 right-of-way; Centennial city surrounds it on three sides and both RTD line articles list the municipality as Centennial. |
| Commerce City | CO | Commerce City/72nd station platform sits in unannexed rail right-of-way immediately adjacent to Commerce City; the N Line article lists the municipality as Commerce City. |
| North Washington | CO | Unincorporated CDP in Adams County; Pecos Junction station geocodes to North Washington CDP. |
| Ansonia | CT | City coextensive with the town of Ansonia |
| Beacon Falls | CT | Connecticut town (Census county subdivision); no CDP at the station point |
| Berlin | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Kensington CDP inside the town |
| Bethel | CT | Connecticut town; the station is in the Bethel CDP |
| Branchville | CT | Unincorporated CDP in the town of Ridgefield |
| Branford | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Branford Center CDP |
| Bridgeport | CT | City in Fairfield County; New Haven Line, Waterbury Branch and Shore Line East |
| Cannondale | CT | Unincorporated CDP in the town of Wilton |
| Clinton | CT | Connecticut town; the station is in the Clinton CDP |
| Cos Cob | CT | Unincorporated CDP in the town of Greenwich |
| Danbury | CT | City in Fairfield County; Danbury Branch terminal |
| Darien | CT | Connecticut town (Census county subdivision); Census point-in-polygon of Darien station returns Darien Downtown CDP |
| Derby | CT | City coextensive with the town of Derby; the station is on the Derby side of the Housatonic from Shelton |
| Fairfield | CT | Connecticut town (Census county subdivision); no Fairfield CDP. Two stations: Fairfield and Fairfield-Black Rock (formerly Fairfield Metro, opened 2011) |
| Greens Farms | CT | Unincorporated CDP in the town of Westport; Census spells it Greens Farms (station sign: Green's Farms) |
| Greenwich | CT | Connecticut town (Census county subdivision); the station is in the Greenwich CDP within the town |
| Guilford | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Guilford Center CDP |
| Hartford | CT | City coextensive with the town of Hartford |
| Madison | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Madison Center CDP |
| Meriden | CT | City coextensive with the town of Meriden |
| Milford | CT | City coextensive with the town of Milford; Census records it as Milford city (balance) |
| Naugatuck | CT | Borough coextensive with the town of Naugatuck |
| New Canaan | CT | Connecticut town (Census county subdivision); station is in the New Canaan CDP. Talmadge Hill station is elsewhere in the town |
| New Haven | CT | City in New Haven County. Union Station and State Street: New Haven Line, Shore Line East and CTrail Hartford Line all terminate here |
| New London | CT | City coextensive with the town of New London; Shore Line East eastern terminal |
| Noroton Heights | CT | Unincorporated CDP in the town of Darien |
| Norwalk | CT | City in Fairfield County. Four open stations: South Norwalk, East Norwalk, Rowayton and Merritt 7 (Danbury Branch) |
| Old Greenwich | CT | Unincorporated CDP in the town of Greenwich |
| Old Saybrook | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Old Saybrook Center CDP |
| Riverside | CT | Unincorporated CDP in the town of Greenwich |
| Seymour | CT | Connecticut town (Census county subdivision); no CDP at the station point |
| Southport | CT | Unincorporated CDP in the town of Fairfield |
| Stamford | CT | City in Fairfield County. Stamford Transportation Center plus Glenbrook and Springdale on the New Canaan Branch |
| Stratford | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Stratford Downtown CDP |
| Wallingford | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Wallingford Center CDP. New station opened Nov 6 2017, Hartford Line service from June 16 2018 |
| Waterbury | CT | City in New Haven County; Waterbury Branch terminal |
| West Haven | CT | City in New Haven County; station opened Aug 18 2013 |
| Westbrook | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Westbrook Center CDP |
| Westport | CT | Connecticut town (Census county subdivision); Census point-in-polygon of Westport station returns Saugatuck CDP inside the town |
| Wilton | CT | Connecticut town (Census county subdivision); Census point-in-polygon returns Wilton Center CDP |
| Windsor | CT | Connecticut town (Census county subdivision); no CDP at the station point |
| Windsor Locks | CT | Connecticut town; the station is in the Windsor Locks CDP |
| Washington | DC | Also MARC Penn/Camden/Brunswick and VRE Fredericksburg/Manassas at Union Station |
| Claymont | DE | CDP, New Castle County DE |
| Newark | DE | City, New Castle County DE; Newark station (Wilmington/Newark Line terminus) and Churchmans Crossing, which the line article places in Newark (the station list says 'Christiana', which is not a 2020 Census place) |
| Wilmington | DE | City, New Castle County DE |
| Brownsville | FL | Unincorporated CDP. Brownsville and Earlington Heights stations. |
| Coral Gables | FL | University station. |
| Dania Beach | FL | Fort Lauderdale Airport station is inside Dania Beach city. |
| Fort Lauderdale | FL | Cypress Creek and Fort Lauderdale stations; Cypress Creek is in Fort Lauderdale, not Oakland Park. |
| Gladeview | FL | Unincorporated CDP. Northside and Dr. Martin Luther King Jr. Plaza stations. |
| Glenvar Heights | FL | Unincorporated CDP. Dadeland North station (postal address reads 'Miami'). |
| Golden Glades | FL | Unincorporated CDP (GEOID 1226375). Census renamed it 'Biscayne Gardens CDP' in 2023 (BAS23); the 2020 Census name is 'Golden Glades CDP'. |
| Hialeah | FL | Hialeah, Okeechobee and Tri-Rail Transfer Metrorail stations; also Tri-Rail commuter rail. |
| Hollywood | FL | Sheridan Street and Hollywood stations. |
| Kendall | FL | Unincorporated CDP. Dadeland South station (southern terminus). |
| Meadow Woods | FL | Unincorporated CDP. Meadow Woods station (postal address reads 'Orlando'). |
| Medley | FL | Palmetto station (northern terminus of the Green Line) is inside Medley town. |
| Orlando | FL | AdventHealth, LYNX Central, Church Street and Orlando Health/Amtrak stations. |
| Pine Castle | FL | Unincorporated CDP. Sand Lake Road station (postal address reads 'Orlando'). |
| Brookhaven | GA | City incorporated 2013; Brookhaven/Oglethorpe station verified inside Brookhaven city. |
| College Park | GA | Airport and College Park stations are both in College Park city (not Hapeville). |
| Decatur | GA | Decatur and Avondale stations. Avondale station is in Decatur, not Avondale Estates. |
| Dunwoody | GA | City incorporated 2008; Dunwoody station verified inside Dunwoody city. |
| East Point | GA | East Point station; Lakewood/Fort McPherson straddles Atlanta/East Point. |
| Sandy Springs | GA | City incorporated 2005; Medical Center, Sandy Springs and North Springs stations all inside. |
| Fairview Heights | IL | Station sits on the East St. Louis / Fairview Heights line; Metro's own station list gives the address as 9720 W. Route 161, Fairview Heights, IL 62208. |
| Golf | IL | Village of Golf IL (pop. under 500); Golf station is on the Milwaukee District North Line. |
| Long Lake | IL | Unincorporated Long Lake CDP, Lake County IL; Long Lake station is on the Milwaukee District North Line. |
| Hudson Lake | IN | Unincorporated Hudson Lake CDP, Hudson Township, LaPorte County IN. Not the city of La Porte. |
| Munster | IN | Town of Munster IN. Monon Corridor (West Lake) branch opened March 31, 2026. |
| Ogden Dunes | IN | Town of Ogden Dunes IN. Station is signed Portage/Ogden Dunes and serves Portage too, but sits in Ogden Dunes (infobox address 'U.S. Highway 12 and Hillcrest Road, Ogden Dunes'; the town article says 'The town is the site of the Portage / Ogden Dunes station'). |
| Andover | MA | Both Andover and Ballardvale stations are in the town of Andover. |
| Attleboro | MA | Both Attleboro and South Attleboro stations are in the city of Attleboro. |
| Beverly | MA | Beverly, North Beverly, Montserrat and Beverly Farms stations are all in the city of Beverly (Prides Crossing, also in Beverly, is indefinitely closed). |
| Billerica | MA | North Billerica station is in the North Billerica village of the town of Billerica. |
| Brookline | MA | Massachusetts town, not a city; Census carries it as Brookline CDP. |
| Chelsea | MA | Chelsea's only rail service is the Newburyport/Rockport Line commuter rail station. Silver Line SL3, which also serves Chelsea, is bus rapid transit and does not count. |
| Fall River | MA | Fall River Depot opened March 24, 2025 with South Coast Rail Phase 1. |
| Fitchburg | MA | Both Fitchburg and Wachusett stations are in the city of Fitchburg. |
| Foxborough | MA | Foxboro station (at Gillette Stadium) has permanent scheduled weekday service on the Franklin/Foxboro Line since October 2, 2023, not just event service. |
| Franklin | MA | Both Franklin and Forge Park/495 stations are in the town of Franklin. |
| Freetown | MA | Freetown station opened March 24, 2025 with South Coast Rail Phase 1. |
| Hamilton | MA | Hamilton/Wenham station straddles the Hamilton-Wenham town line; MBTA lists its municipality as Hamilton. |
| Haverhill | MA | Both Haverhill station and Bradford station (in the Bradford neighborhood) are in the city of Haverhill. |
| Hingham | MA | West Hingham and Nantasket Junction stations are both in the town of Hingham. |
| Leominster | MA | North Leominster station is in the city of Leominster. |
| Littleton | MA | Littleton/Route 495 station is in the town of Littleton. |
| Lynn | MA | Lynn's permanent station closed for reconstruction in 2022; interim platforms have been in service since December 18, 2023. River Works is also in Lynn. |
| Manchester-by-the-Sea | MA | Station is signed 'Manchester'; the town is Manchester-by-the-Sea. |
| Melrose | MA | Wyoming Hill, Melrose/Cedar Park and Melrose Highlands are all in Melrose. |
| Middleborough | MA | New Middleborough station opened March 24, 2025, replacing Middleborough/Lakeville station 0.7 mi south in the town of Lakeville. |
| Milton | MA | Mattapan trolley: 4 of its 8 stations (Milton, Central Avenue, Valley Road, Capen Street) are in the town of Milton; the rest are in Boston. |
| Natick | MA | Natick Center and West Natick stations are both in the town of Natick. |
| Needham | MA | Hersey, Needham Junction, Needham Center and Needham Heights are all in Needham. |
| New Bedford | MA | New Bedford and Church Street stations opened March 24, 2025 with South Coast Rail Phase 1. |
| Norwood | MA | Norwood Depot, Norwood Central and Windsor Gardens are all in the town of Norwood. |
| Randolph | MA | Holbrook/Randolph station is in the town of Randolph. |
| Scituate | MA | North Scituate and Greenbush stations are both in the town of Scituate. |
| Springfield | MA | City in Hampden County; northern terminal of the CTrail Hartford Line (may overlap another agent's Massachusetts scope) |
| Taunton | MA | East Taunton station, opened March 24, 2025, is in the East Taunton village of the city of Taunton. |
| Wakefield | MA | Greenwood and Wakefield stations are both in the town of Wakefield. |
| Walpole | MA | Walpole station is active; Plimptonville, also in Walpole, is indefinitely closed. |
| Waltham | MA | Waltham and Brandeis/Roberts stations are both in the city of Waltham. |
| Wellesley | MA | Wellesley Farms, Wellesley Hills and Wellesley Square are all in Wellesley. |
| Wenham | MA | Hamilton/Wenham station straddles the town line, with the southern end of the platform geographically in Wenham. |
| Weston | MA | Kendal Green and Silver Hill stations are in the town of Weston (Hastings, also in Weston, is indefinitely closed). |
| Westwood | MA | Route 128 station (Providence/Stoughton Line) and Islington station (Franklin/Foxboro Line) are both in the town of Westwood, not Boston. |
| Weymouth | MA | Weymouth Landing/East Braintree and East Weymouth (Greenbush) and South Weymouth (Kingston) are all in the town of Weymouth. |
| Wilmington | MA | Wilmington station (Lowell Line) and North Wilmington station (Haverhill Line) are both in the town of Wilmington. |
| Winchester | MA | Wedgemere and Winchester Center stations are both in the town of Winchester. |
| Woburn | MA | Anderson/Woburn station is in Woburn; Mishawum, also in Woburn, is indefinitely closed. |
| Aberdeen | MD | City, Harford County; Penn Line |
| Baltimore | MD | Also Baltimore Light RailLink and MARC Penn/Camden lines |
| Barnesville | MD | Town, Montgomery County; Brunswick Line |
| Beltsville | MD | CDP, Prince George's County; Muirkirk station on the Camden Line |
| Bethesda | MD | CDP, Montgomery County; Bethesda and Medical Center stations |
| Bowie | MD | City, Prince George's County; Bowie State station on the Penn Line |
| Brunswick | MD | City, Frederick County; Brunswick Line namesake terminus |
| Capitol Heights | MD | Town; Capitol Heights and Addison Road stations |
| Cheverly | MD | Town, Prince George's County |
| Cockeysville | MD | CDP, Baltimore County; Warren Road station |
| College Park | MD | City; College Park-University of Maryland station + MARC Camden Line |
| Edgewood | MD | CDP, Harford County; Penn Line |
| Forest Glen | MD | CDP, Montgomery County |
| Frederick | MD | City, Frederick County; Frederick and Monocacy stations on the Frederick Branch |
| Gaithersburg | MD | City, Montgomery County; Gaithersburg and Metropolitan Grove stations (the Brunswick Line article puts both in Gaithersburg) |
| Garrett Park | MD | Town, Montgomery County; Brunswick Line |
| Germantown | MD | CDP, Montgomery County; Brunswick Line |
| Glen Burnie | MD | CDP, Anne Arundel County; Ferndale and Glen Burnie stations - the source puts BOTH in Glen Burnie, so the separate Ferndale CDP is not claimed |
| Glenmont | MD | CDP, Montgomery County; Red Line terminus |
| Greenbelt | MD | City; Metro Green/Yellow terminus + MARC Camden Line |
| Hillcrest Heights | MD | CDP, Prince George's County; Naylor Road station |
| Hyattsville | MD | City; Hyattsville Crossing and West Hyattsville stations |
| Jessup | MD | CDP straddling Anne Arundel and Howard counties; Camden Line |
| Kensington | MD | Town, Montgomery County; Brunswick Line |
| Lake Arbor | MD | CDP, Prince George's County; Downtown Largo station (Largo postal address), NOT the Largo CDP |
| Landover | MD | CDP, Prince George's County |
| Laurel | MD | City, Prince George's County; Laurel and Laurel Race Track stations on the Camden Line |
| Linthicum | MD | CDP, Anne Arundel County (Wikipedia writes 'Linthicum Heights'); North Linthicum, Linthicum and BWI Business District stations |
| Lochearn | MD | CDP, Baltimore County; Old Court and Milford Mill stations |
| Lutherville | MD | CDP, Baltimore County; Lutherville station |
| Middle River | MD | CDP, Baltimore County; Martin State Airport station on the Penn Line |
| New Carrollton | MD | City; station sits just outside the city limits per Wikipedia, but MARC/WMATA name the place New Carrollton. Metro + MARC Penn + Amtrak |
| North Bethesda | MD | CDP, Montgomery County; North Bethesda and Grosvenor-Strathmore stations |
| Odenton | MD | CDP, Anne Arundel County; Penn Line |
| Owings Mills | MD | CDP, Baltimore County; western terminus |
| Perryville | MD | Town, Cecil County; Penn Line northern terminus |
| Point of Rocks | MD | CDP, Frederick County; Brunswick Line junction |
| Redland | MD | CDP, Montgomery County; Shady Grove station (Derwood postal address), NOT in Rockville city |
| Riverdale Park | MD | Town, Prince George's County; MARC 'Riverdale' station on the Camden Line |
| Rockville | MD | City; Rockville and Twinbrook stations. Also MARC Brunswick Line |
| Savage | MD | CDP, Howard County; Camden Line |
| Seabrook | MD | CDP, Prince George's County; Penn Line |
| Silver Spring | MD | CDP, Montgomery County; Metro Red Line + MARC Brunswick Line |
| Suitland | MD | CDP, Prince George's County; Suitland and Branch Avenue stations |
| Summerfield | MD | CDP, Prince George's County; Morgan Boulevard station (Landover postal address) |
| Temple Hills | MD | CDP, Prince George's County; Southern Avenue station |
| Timonium | MD | CDP, Baltimore County; Fairgrounds and Timonium stations (the 2010 'Lutherville-Timonium' CDP was split into Timonium and Lutherville CDPs for 2020) |
| Towson | MD | CDP, Baltimore County; Falls Road station ('Falls & Lake Roland Park entrance, Towson') |
| Washington Grove | MD | Town, Montgomery County; Brunswick Line |
| Wheaton | MD | CDP, Montgomery County |
| St. Paul | MN | Census writes the place name "St. Paul city". |
| Shrewsbury | MO | Shrewsbury–Lansdowne I-44 station straddles the Shrewsbury / St. Louis line; its street address (7201 Lansdowne Ave) geocodes to Shrewsbury city and the station article calls it a station 'in Shrewsbury and St. Louis, Missouri'. |
| Charlotte | NC | All 26 Blue Line stations are inside Charlotte; the southern terminus (I-485/South Boulevard) stops at the Pineville city limits, so Pineville has no station. |
| Aberdeen | NJ | Aberdeen Township (MCD); NJ townships are not Census places, township name used per spec. Station straddles Aberdeen Township and Matawan borough. |
| Annandale | NJ | Annandale CDP, Clinton Township |
| Ashland | NJ | CDP in Voorhees Township, Camden County NJ (PATCO Ashland station) |
| Atco | NJ | Atco CDP, Waterford Township |
| Avenel | NJ | Avenel CDP, Woodbridge Township |
| Basking Ridge | NJ | Basking Ridge CDP, Bernards Township |
| Belleville | NJ | Belleville Township (MCD); NJ townships are not Census places, township name used per spec |
| Berkeley Heights | NJ | Berkeley Heights Township (MCD); NJ townships are not Census places, township name used per spec |
| Beverly | NJ | Station is in Beverly city despite the name; Edgewater Park Township has no station |
| Bloomfield | NJ | Bloomfield Township (MCD); NJ townships are not Census places, township name used per spec |
| Branchburg | NJ | Branchburg Township (MCD); township name used per spec |
| Bridgewater | NJ | Bridgewater Township (MCD); township name used per spec |
| Budd Lake | NJ | Budd Lake CDP, Mount Olive Township |
| Cherry Hill | NJ | Cherry Hill Township (MCD); NJ townships are not Census places, township name used per spec NJ township, no incorporated village; PATCO Woodcrest station |
| Cinnaminson | NJ | Cinnaminson Township (MCD); NJ townships are not Census places, township name used per spec |
| Cranford | NJ | Cranford CDP, coextensive with Cranford Township |
| Delanco | NJ | Delanco Township (MCD); NJ townships are not Census places, township name used per spec |
| Denville | NJ | Denville Township (MCD); township name used per spec |
| Edison | NJ | Edison Township (MCD); NJ townships are not Census places, township name used per spec |
| Ewing | NJ | NJ township; West Trenton station. 'West Trenton' is not a 2020 Census place. May duplicate the New Jersey agent's output |
| Florence | NJ | Florence Township; Florence CDP is the village in it |
| Gillette | NJ | Gillette CDP, Long Hill Township |
| Hamilton | NJ | Hamilton Township, Mercer County (MCD); township name used per spec |
| Hazlet | NJ | Hazlet Township (MCD); NJ townships are not Census places, township name used per spec |
| Iselin | NJ | Iselin CDP, Woodbridge Township |
| Landing | NJ | Landing CDP, Roxbury Township |
| Little Falls | NJ | Little Falls Township (MCD); NJ townships are not Census places, township name used per spec |
| Lyndhurst | NJ | Lyndhurst Township (MCD); NJ townships are not Census places, township name used per spec |
| Mahwah | NJ | Mahwah Township (MCD); NJ townships are not Census places, township name used per spec |
| Maplewood | NJ | Maplewood Township (MCD); NJ townships are not Census places, township name used per spec |
| Middletown | NJ | Middletown Township (MCD); township name used per spec |
| Millburn | NJ | Millburn Township (MCD); NJ townships are not Census places, township name used per spec |
| Millington | NJ | Millington CDP, Long Hill Township |
| Montclair | NJ | Montclair Township (MCD); NJ townships are not Census places, township name used per spec |
| Morris | NJ | Morris Township (MCD); Convent Station is an unincorporated community in it, not a CDP |
| New Providence | NJ | Murray Hill is a section of New Providence borough; no Murray Hill CDP |
| North Bergen | NJ | North Bergen Township (MCD); NJ townships are not Census places, township name used per spec |
| Pennsauken | NJ | Pennsauken Township (MCD); NJ townships are not Census places, township name used per spec |
| Princeton Junction | NJ | Princeton Junction CDP, West Windsor Township |
| Riverside | NJ | Riverside Township (MCD); NJ townships are not Census places, township name used per spec |
| Roebling | NJ | Roebling CDP, Florence Township |
| Short Hills | NJ | Short Hills CDP, Millburn Township |
| Stirling | NJ | Stirling CDP, Long Hill Township |
| Towaco | NJ | Towaco CDP, Montville Township |
| Trenton | NJ | New Jersey city; Trenton Transit Center is the Trenton Line terminus. Also NJ Transit / Amtrak - may duplicate the New Jersey agent's output |
| Union | NJ | Union CDP, Union Township, Union County |
| Upper Montclair | NJ | Upper Montclair CDP, Montclair Township |
| Wayne | NJ | Wayne Township (MCD); township name used per spec |
| Weehawken | NJ | Weehawken Township (MCD); NJ townships are not Census places, township name used per spec |
| Westmont | NJ | CDP in Haddon Township, Camden County NJ (PATCO Westmont station) |
| White House Station | NJ | White House Station CDP (commonly 'Whitehouse Station'), Readington Township |
| Woodbridge | NJ | Woodbridge CDP, Woodbridge Township |
| Edith Enclave | NM | Unincorporated CDP in Bernalillo County; Sandia Pueblo station geocodes to Edith Enclave CDP (not to Pueblo of Sandia Village CDP). |
| North Valley | NM | Unincorporated CDP in Bernalillo County; both Montaño and Los Ranchos/Journal Center stations geocode to North Valley CDP, not to Los Ranchos de Albuquerque village. |
| South Valley | NM | Unincorporated CDP in Bernalillo County; the Bernalillo County/International Sunport station geocodes to South Valley CDP. |
| Albertson | NY | Unincorporated CDP, town of North Hempstead, Nassau County |
| Amagansett | NY | Unincorporated CDP, town of East Hampton |
| Amenia | NY | New York TOWN (Census county subdivision). Wassaic (Harlem Line northern terminal) and Tenmile River are in the town of Amenia; the Census point-in-polygon at both stations falls outside the Wassaic CDP and Amenia CDP boundaries |
| Amityville | NY | Incorporated village, town of Babylon |
| Babylon | NY | Incorporated village, town of Babylon; Babylon Branch terminal |
| Baldwin | NY | Unincorporated CDP, town of Hempstead, Nassau County |
| Bay Shore | NY | Unincorporated CDP, town of Islip |
| Baywood | NY | Unincorporated CDP, town of Islip. The station named Deer Park sits in Baywood |
| Beacon | NY | City in Dutchess County |
| Beaver Dam Lake | NY | Unincorporated CDP, town of Cornwall, Orange County. Article: the station is 'in the Beaver Dam Lake section of the town of Cornwall' |
| Bedford Hills | NY | Unincorporated CDP, town of Bedford |
| Bellerose | NY | Incorporated village, town of Hempstead. Station straddles Bellerose and Floral Park villages |
| Bellerose Terrace | NY | Unincorporated CDP, town of Hempstead. Elmont-UBS Arena station lies in Elmont and Bellerose Terrace |
| Bellmore | NY | Unincorporated CDP, town of Hempstead |
| Bethpage | NY | Unincorporated CDP, town of Oyster Bay |
| Brentwood | NY | Unincorporated CDP, town of Islip |
| Brewster | NY | Incorporated village, town of Southeast, Putnam County |
| Briarcliff Manor | NY | Incorporated village, towns of Ossining/Mount Pleasant. Article: Scarborough station is 'in the Scarborough area of Briarcliff Manor'; Census point-in-polygon of the listed coordinate returns Ossining village, so the two sit on the boundary |
| Bridgehampton | NY | Unincorporated CDP, town of Southampton |
| Bronxville | NY | Incorporated village, town of Eastchester |
| Carle Place | NY | Unincorporated CDP, town of North Hempstead |
| Cedarhurst | NY | Incorporated village, town of Hempstead |
| Central Islip | NY | Unincorporated CDP, town of Islip |
| Chappaqua | NY | Unincorporated CDP, town of New Castle |
| Cold Spring | NY | Incorporated village, town of Philipstown |
| Copiague | NY | Unincorporated CDP, town of Babylon |
| Croton-on-Hudson | NY | Incorporated village, town of Cortlandt. Croton-Harmon is a major Hudson Line hub |
| Dobbs Ferry | NY | Incorporated village, town of Greenburgh |
| Dover Plains | NY | Unincorporated CDP, town of Dover, Dutchess County |
| East Farmingdale | NY | Unincorporated CDP, town of Babylon. Pinelawn station (cemetery service, off-peak only) is in East Farmingdale |
| East Hampton | NY | Incorporated village, town of East Hampton |
| East Islip | NY | Unincorporated CDP, town of Islip. The station named Great River is in East Islip |
| East Northport | NY | Unincorporated CDP, town of Huntington. The station named Northport is in East Northport |
| East Rockaway | NY | Incorporated village, town of Hempstead. Two stations: East Rockaway and Centre Avenue |
| East Williston | NY | Incorporated village, town of North Hempstead. Station is on the East Williston / Williston Park border |
| Elmont | NY | Unincorporated CDP, town of Hempstead. Elmont-UBS Arena station opened Nov 2021, replacing the old Belmont Park-only stop |
| Farmingdale | NY | Incorporated village, town of Oyster Bay |
| Floral Park | NY | Incorporated village, town of Hempstead. Floral Park and Bellerose stations |
| Freeport | NY | Incorporated village, town of Hempstead |
| Garden City | NY | Incorporated village, town of Hempstead. Five stations in the village: Garden City, Country Life Press, Nassau Boulevard, Merillon Avenue, Stewart Manor |
| Garden City Park | NY | Unincorporated CDP, town of North Hempstead. Merillon Avenue station is in Garden City Park and Garden City |
| Glen Cove | NY | City in Nassau County. Glen Cove, Glen Street and Sea Cliff stations are all inside the city |
| Glen Head | NY | Unincorporated CDP, town of Oyster Bay |
| Golden's Bridge | NY | Unincorporated CDP, town of Lewisboro. Census spells the place Golden's Bridge; the station is Goldens Bridge |
| Great Neck Plaza | NY | Incorporated village, town of North Hempstead. The station named Great Neck is in the Village of Great Neck Plaza |
| Greenlawn | NY | Unincorporated CDP, town of Huntington |
| Greenport | NY | Incorporated village, town of Southold; Greenport Branch terminal |
| Hampton Bays | NY | Unincorporated CDP, town of Southampton |
| Hamptonburgh | NY | New York TOWN (Census county subdivision, not a Census place). Campbell Hall station is in unincorporated Hamptonburgh with no CDP at the point |
| Harrison | NY | Incorporated village coextensive with the town of Harrison |
| Hartsdale | NY | Unincorporated CDP, town of Greenburgh |
| Hastings-on-Hudson | NY | Incorporated village, town of Greenburgh |
| Hawthorne | NY | Unincorporated CDP, town of Mount Pleasant |
| Hempstead | NY | Incorporated village, town of Hempstead |
| Hewlett | NY | Unincorporated CDP, town of Hempstead |
| Hicksville | NY | Unincorporated CDP, town of Oyster Bay |
| Huntington Station | NY | Unincorporated CDP, town of Huntington |
| Inwood | NY | Unincorporated CDP, town of Hempstead. Census point-in-polygon puts the station in Inwood CDP; the Wikipedia article describes it as in the adjoining Village of Lawrence |
| Irvington | NY | Incorporated village, town of Greenburgh. Irvington and Ardsley-on-Hudson stations |
| Island Park | NY | Incorporated village, town of Hempstead |
| Islip | NY | Unincorporated CDP (hamlet), town of Islip |
| Katonah | NY | Unincorporated CDP, town of Bedford |
| Kings Park | NY | Unincorporated CDP, town of Smithtown |
| Larchmont | NY | Incorporated village, town of Mamaroneck. Article: 'located in Larchmont, New York' |
| Lawrence | NY | Incorporated village, town of Hempstead |
| Lindenhurst | NY | Incorporated village, town of Babylon |
| Locust Valley | NY | Unincorporated CDP, town of Oyster Bay |
| Long Beach | NY | City in Nassau County; Long Beach Branch terminal |
| Lynbrook | NY | Incorporated village, town of Hempstead |
| Malverne | NY | Incorporated village, town of Hempstead. Malverne and Westwood stations |
| Mamaroneck | NY | Incorporated village, town of Rye |
| Manhasset | NY | Unincorporated CDP, town of North Hempstead |
| Manorville | NY | Unincorporated CDP, town of Brookhaven. New Yaphank-BNL station opened July 17 2026; Census reverse geocode of its coordinates returns Manorville CDP (the article calls the community East Yaphank, which is not a Census place) |
| Massapequa | NY | Unincorporated CDP, town of Oyster Bay |
| Massapequa Park | NY | Incorporated village, town of Oyster Bay |
| Mattituck | NY | Unincorporated CDP, town of Southold |
| Medford | NY | Unincorporated CDP, town of Brookhaven |
| Merrick | NY | Unincorporated CDP, town of Hempstead |
| Mineola | NY | Incorporated village, town of North Hempstead |
| Montauk | NY | Unincorporated CDP, town of East Hampton; Montauk Branch terminal |
| Montrose | NY | Unincorporated CDP, town of Cortlandt. The station named Cortlandt sits in Montrose CDP |
| Mount Hope | NY | New York TOWN (Census county subdivision, not a Census place). Article: Otisville station is 'in the town of Mount Hope', outside Otisville village |
| Mount Kisco | NY | Incorporated village coextensive with the town of Mount Kisco |
| Mount Vernon | NY | City in Westchester County. Mount Vernon West and Fleetwood (Harlem Line) plus Mount Vernon East (New Haven Line) |
| Nanuet | NY | Unincorporated CDP, town of Clarkstown, Rockland County |
| New Hamburg | NY | Unincorporated CDP, town of Poughkeepsie |
| New Hyde Park | NY | Incorporated village, town of Hempstead |
| New Rochelle | NY | City in Westchester County |
| New York | NY | NYC boroughs are not Census places. LIRR terminals Penn Station and Grand Central Madison (Manhattan, opened Jan 25 2023) plus 25 Queens/Brooklyn stations (Jamaica, Woodside, Flushing-Main Street, Far Rockaway, Atlantic Terminal, Nostrand Avenue, East New York, Belmont Park etc). New York City also has subway service, which outranks commuter rail. |
| North Bellport | NY | Unincorporated CDP, town of Brookhaven. The station named Bellport is in North Bellport, not Bellport village |
| North Salem | NY | New York TOWN (Census county subdivision, not a Census place). Croton Falls and Purdy's stations are in unincorporated North Salem with no CDP at either point |
| Oakdale | NY | Unincorporated CDP, town of Islip |
| Oceanside | NY | Unincorporated CDP, town of Hempstead |
| Ossining | NY | Incorporated village, town of Ossining |
| Oyster Bay | NY | Unincorporated CDP (hamlet), town of Oyster Bay; Oyster Bay Branch terminal |
| Patchogue | NY | Incorporated village, town of Brookhaven |
| Patterson | NY | New York TOWN (Census county subdivision, not a Census place); no CDP at the station point |
| Pawling | NY | Incorporated village, town of Pawling, Dutchess County. The Appalachian Trail flag stop is elsewhere in the town |
| Pearl River | NY | Unincorporated CDP, town of Orangetown, Rockland County. Metro-North Pascack Valley Line (trains run by NJ Transit under contract) |
| Peekskill | NY | City in Westchester County |
| Pelham | NY | Incorporated village, town of Pelham |
| Philipstown | NY | New York TOWN (Census county subdivision, not a Census place). Garrison and Manitou stations are in unincorporated Philipstown with no CDP at either point |
| Plandome | NY | Incorporated village, town of North Hempstead |
| Pleasantville | NY | Incorporated village, town of Mount Pleasant |
| Port Chester | NY | Incorporated village, town of Rye |
| Port Jefferson | NY | Incorporated village, town of Brookhaven. Station sits on the village line with the hamlet of Port Jefferson Station |
| Port Jefferson Station | NY | Unincorporated CDP, town of Brookhaven. Wikipedia: the station 'is on the hamlet's northern border with the Incorporated Village of Port Jefferson' |
| Port Jervis | NY | City in Orange County; Port Jervis Line terminal |
| Port Washington | NY | Unincorporated CDP, town of North Hempstead; Port Washington Branch terminal |
| Poughkeepsie | NY | City in Dutchess County; Hudson Line northern terminal |
| Remsenburg-Speonk | NY | Unincorporated CDP, town of Southampton; Census name for the Speonk community |
| Riverhead | NY | Unincorporated CDP, town of Riverhead |
| Rockville Centre | NY | Incorporated village, town of Hempstead |
| Ronkonkoma | NY | Unincorporated CDP, town of Islip; Ronkonkoma Branch terminal and LI MacArthur Airport stop |
| Roslyn Harbor | NY | Incorporated village, town of Oyster Bay. Greenvale station is within the Village of Roslyn Harbor |
| Roslyn Heights | NY | Unincorporated CDP, town of North Hempstead. The station named Roslyn is in Roslyn Heights |
| Rye | NY | City in Westchester County |
| Sayville | NY | Unincorporated CDP, town of Islip |
| Scarsdale | NY | Incorporated village coextensive with the town of Scarsdale |
| Scotchtown | NY | Unincorporated CDP, town of Wallkill, Orange County. The station serving Middletown is outside the city, in the Town of Wallkill |
| Seaford | NY | Unincorporated CDP, town of Hempstead |
| Shirley | NY | Unincorporated CDP, town of Brookhaven |
| Sleepy Hollow | NY | Incorporated village, town of Mount Pleasant. Philipse Manor station is in Sleepy Hollow |
| Sloatsburg | NY | Incorporated village, town of Ramapo, Rockland County |
| Smithtown | NY | Unincorporated CDP, town of Smithtown |
| Southampton | NY | Incorporated village, town of Southampton |
| Southeast | NY | New York TOWN (Census county subdivision, not a Census place). Southeast station (formerly Brewster North) is in the town outside Brewster village |
| Southold | NY | Unincorporated CDP, town of Southold |
| Spring Valley | NY | Incorporated village, town of Ramapo, Rockland County; NY terminus of Pascack Valley Line service |
| St. James | NY | Unincorporated CDP, town of Smithtown |
| Stony Brook | NY | Unincorporated CDP, town of Brookhaven. Article: 'located in Stony Brook, New York, adjacent to the campus of Stony Brook University'; the Census point-in-polygon returns the adjacent Stony Brook University CDP |
| Suffern | NY | Incorporated village, town of Ramapo, Rockland County. Metro-North Port Jervis Line (trains run by NJ Transit under contract) |
| Syosset | NY | Unincorporated CDP, town of Oyster Bay |
| Tarrytown | NY | Incorporated village, town of Greenburgh |
| Tuckahoe | NY | Incorporated village, town of Eastchester. Tuckahoe and Crestwood stations |
| Tuxedo | NY | Incorporated village, Orange County; the Village of Tuxedo incorporated Dec 23 2019 and consolidated with the town Jan 1 2021, so it post-dates the 2020 Census place file but is in the current Census place layer (GEOID 3675779) |
| Valhalla | NY | Unincorporated CDP, town of Mount Pleasant |
| Valley Stream | NY | Incorporated village, town of Hempstead. Valley Stream and Gibson stations |
| Wantagh | NY | Unincorporated CDP, town of Hempstead |
| West Hempstead | NY | Unincorporated CDP, town of Hempstead. Three West Hempstead Branch stations: West Hempstead, Hempstead Gardens, Lakeview |
| West Hills | NY | Unincorporated CDP, town of Huntington. The station named Cold Spring Harbor is in West Hills |
| Westbury | NY | Incorporated village, town of North Hempstead |
| Westhampton Beach | NY | Incorporated village, town of Southampton. Census point-in-polygon puts the Westhampton station inside Westhampton Beach village; the article text says the hamlet of Westhampton |
| White Plains | NY | City in Westchester County. White Plains and North White Plains stations |
| Williston Park | NY | Incorporated village, town of North Hempstead. East Williston station straddles the Williston Park / East Williston line |
| Wingdale | NY | Unincorporated CDP, town of Dover, Dutchess County |
| Woodbury | NY | Incorporated village, town of Woodbury, Orange County. Article: Harriman station is 'in the town of Woodbury ... south of the eponymous hamlet'; Census point-in-polygon returns Woodbury village, not Harriman village |
| Woodmere | NY | Unincorporated CDP, town of Hempstead |
| Wyandanch | NY | Unincorporated CDP, town of Babylon |
| Yonkers | NY | City in Westchester County. Four Hudson Line stations: Yonkers, Ludlow, Glenwood, Greystone |
| Brook Park | OH | Brookpark station straddles the Cleveland / Brook Park line ('Cleveland / Brook Park' in the Jurisdiction column); Red Line (heavy rail) only. |
| East Cleveland | OH | Served only by the Red Line, which is heavy-rail rapid transit; typed 'light rail' for consistency with the brief's Cleveland classification. |
| Oak Grove | OR | Unincorporated CDP in Clackamas County; SE Park Avenue station (Orange Line terminus) geocodes to Oak Grove CDP. |
| Abington | PA | Abington Township, Montgomery County PA; Crestmont, Noble, Rydal, Meadowbrook and Ardsley stations - none of those five communities is a 2020 Census place |
| Aldan | PA | Delaware County borough; D2 street-running stops (Magnolia Ave, Woodlawn-Providence). Also Regional Rail Clifton-Aldan / Primos |
| Ambler | PA | Montgomery County borough |
| Ardmore | PA | CDP straddling Lower Merion Twp (Montgomery) and Haverford Twp (Delaware) |
| Bala Cynwyd | PA | CDP in Lower Merion Township, Montgomery County; Bala and Cynwyd stations (Cynwyd Line) |
| Bensalem | PA | Bensalem Township, Bucks County PA; Eddington station ('the Eddington section of Bensalem Township') and Neshaminy Falls station ('Bristol Road and Linden Street, Bensalem Township') |
| Berwyn | PA | CDP straddling Tredyffrin and Easttown townships, Chester County; Berwyn and Daylesford stations (Daylesford station is 'at Glenn Avenue and Lancaster Avenue in Berwyn') |
| Bridgeport | PA | Montgomery County borough; M stations Bridgeport and DeKalb Street |
| Bristol | PA | Bucks County borough |
| Bryn Mawr | PA | CDP straddling Lower Merion Twp (Montgomery) and Delaware County; Paoli/Thorndale Line station |
| Chalfont | PA | Bucks County borough; Chalfont station (Link Belt station has a Colmar address) |
| Cheltenham | PA | Cheltenham Township, Montgomery County PA; Cheltenham station (Fox Chase Line) and Melrose Park station. The 2020 Census place near the Cheltenham station is 'Cheltenham Village CDP'; the township is used because no source pins the platform inside that CDP |
| Chester | PA | Delaware County city; Chester Transit Center and Highland Avenue |
| Clifton Heights | PA | Delaware County borough; D2 stations. Also Regional Rail Clifton-Aldan |
| Collingdale | PA | Delaware County borough; 4 D2 stations |
| Conshohocken | PA | Montgomery County borough |
| Cornwells Heights | PA | CDP in Bensalem Township, Bucks County |
| Croydon | PA | CDP in Bristol Township, Bucks County |
| Darby | PA | Delaware County borough; Darby Transit Center = T4 (and limited T3) terminal. Also Regional Rail Darby station |
| Devon | PA | CDP, Chester County |
| Downingtown | PA | Chester County borough |
| Doylestown | PA | Bucks County borough; Doylestown station. The Delaware Valley University station is in Doylestown TOWNSHIP, a separate MCD with the same name |
| Drexel Hill | PA | CDP inside Upper Darby Township, Delaware County; 13 D1/D2 stations incl. Drexel Hill Junction |
| Eddystone | PA | Delaware County borough |
| Elkins Park | PA | CDP in Cheltenham Township, Montgomery County |
| Exton | PA | CDP in West Whiteland Township, Chester County; Exton and Whitford stations |
| Folcroft | PA | Delaware County borough |
| Fort Washington | PA | CDP in Upper Dublin Township, Montgomery County |
| Glenolden | PA | Delaware County borough |
| Glenside | PA | CDP straddling Abington and Cheltenham townships, Montgomery County |
| Hatboro | PA | Montgomery County borough |
| Hatfield | PA | Hatfield Township, Montgomery County PA; Fortuna station ('Hatfield Township'). The nearby Colmar and Link Belt stations are in the Colmar community, which straddles Hatfield and Montgomery townships |
| Haverford | PA | Haverford Township, Delaware County PA; 6 M (Norristown High Speed Line) stations. The Regional Rail 'Haverford' station is over the line in Lower Merion Township |
| Jenkintown | PA | Montgomery County borough; Jenkintown-Wyncote station |
| Langhorne Manor | PA | Bucks County borough; SEPTA's 'Langhorne' station (Langhorne postal address) |
| Lansdale | PA | Montgomery County borough; Lansdale, 9th Street and Pennbrook stations |
| Lansdowne | PA | Delaware County borough; Lansdowne and Gladstone stations |
| Lower Gwynedd | PA | Lower Gwynedd Township, Montgomery County PA; Gwynedd Valley and Penllyn stations (neither is a 2020 Census place) |
| Lower Merion | PA | Lower Merion Township, Montgomery County PA; M stations County Line, Matsonford, Roberts Road. Also Regional Rail Haverford and Wynnewood, neither of which is a 2020 Census place |
| Lower Moreland | PA | Lower Moreland Township, Montgomery County PA; Bethayres station and Philmont station (Huntingdon Valley). Neither community is a 2020 Census place |
| Malvern | PA | Chester County borough |
| Marcus Hook | PA | Delaware County borough |
| Media | PA | Delaware County borough; D1 street-running terminus at Orange St/State St. The Regional Rail 'Media' station is in Upper Providence Township |
| Merion Station | PA | CDP in Lower Merion Township, Montgomery County; SEPTA calls the station 'Merion' |
| Middletown | PA | Middletown Township, DELAWARE County PA; Elwyn and Wawa stations ('located adjacent to U.S. Route 1 in Middletown Township, Delaware County'). Neither Elwyn nor Wawa is a Census place |
| Millbourne | PA | Delaware County borough; Millbourne station on the Market-Frankford Line (L) |
| Morton | PA | Delaware County borough |
| Mount Lebanon | PA | Home-rule township that the Census treats as an incorporated place, "Mount Lebanon municipality" (place GEOID 4251794). |
| Narberth | PA | Montgomery County borough |
| Nether Providence | PA | Nether Providence Township, Delaware County PA; Wallingford and Moylan-Rose Valley stations (neither Wallingford nor Moylan is a 2020 Census place) |
| New Britain | PA | Bucks County borough |
| Norristown | PA | Montgomery County borough; Norristown Transit Center = M northern terminus. Also Regional Rail Norristown TC, Main Street, Elm Street |
| North Wales | PA | Montgomery County borough |
| Norwood | PA | Delaware County borough |
| Oreland | PA | CDP in Springfield Township, Montgomery County |
| Paoli | PA | CDP straddling Tredyffrin and Willistown townships, Chester County |
| Philadelphia | PA | Broad Street Line (B) + Market-Frankford Line (L) heavy rail; also PATCO, SEPTA T/G trolleys and 13 Regional Rail lines |
| Prospect Park | PA | Delaware County borough |
| Radnor | PA | Radnor Township, Delaware County PA (no Radnor CDP in the 2020 Census); M stations Bryn Mawr, Garrett Hill, Radnor, Stadium, Villanova. Also Regional Rail Radnor |
| Ridley | PA | Ridley Township, Delaware County PA; Crum Lynne and Secane stations (neither Crum Lynne nor Secane is a 2020 Census place; Secane straddles Ridley and Upper Darby townships) |
| Ridley Park | PA | Delaware County borough |
| Rosemont | PA | CDP straddling Lower Merion Twp (Montgomery) and Radnor Twp (Delaware) |
| Roslyn | PA | CDP in Abington Township, Montgomery County |
| Sharon Hill | PA | Delaware County borough; D2 western terminus. Also Regional Rail Sharon Hill and Curtis Park |
| Springfield | PA | Springfield Township, DELAWARE County PA (not the Montgomery County township); 7 D1 stations incl. Springfield Mall |
| St. Davids | PA | CDP in Radnor Township, Delaware County |
| Swarthmore | PA | Delaware County borough |
| Thorndale | PA | CDP in Caln Township, Chester County; western terminus of the Paoli/Thorndale Line |
| Tredyffrin | PA | Tredyffrin Township, Chester County PA; Strafford station (Strafford is not a 2020 Census place) |
| Trevose | PA | CDP in Bensalem Township, Bucks County |
| Tullytown | PA | Bucks County borough; SEPTA's 'Levittown' station is in Tullytown, not in the Levittown CDP |
| Upper Darby | PA | Pennsylvania township (Delaware County); 69th Street Transit Center = L terminus, plus M and D1/D2 stations |
| Upper Merion | PA | Upper Merion Township, Montgomery County PA; M stations Gulph Mills and Hughes Park |
| Upper Providence | PA | Upper Providence Township, Delaware County PA; the Media/Wawa Line 'Media' station. NOTE: the Media/Wawa Line article instead puts this station in Media borough - conflicting sources, Media borough is in this dataset anyway via the D1 trolley |
| Villanova | PA | CDP in Radnor Township, Delaware County; Paoli/Thorndale Line station. The SEPTA Metro M also has a Villanova station, which the SEPTA Metro list places in Radnor Township, so the light-rail tier is credited to Radnor rather than to this CDP |
| Warminster | PA | Warminster Township, Bucks County PA; Warminster station. The SEPTA station list instead names the Warminster Heights CDP, which lies inside the township - the township is the claim both sources support |
| Wayne | PA | CDP in Radnor Township, Delaware County |
| Whitemarsh | PA | Whitemarsh Township, Montgomery County PA; Miquon and Spring Mill stations (neither is a 2020 Census place) |
| Willow Grove | PA | CDP in Upper Moreland Township, Montgomery County |
| Woodbourne | PA | CDP in Middletown Township, Bucks County |
| Yardley | PA | Bucks County borough |
| Yeadon | PA | Delaware County borough; T3 outer terminal. Also SEPTA Regional Rail Fernwood-Yeadon (Media/Wawa Line) |
| Bayamón | PR | Municipio. Census place covering Bayamón, Deportivo and Jardines stations is 'Bayamón zona urbana'. |
| Guaynabo | PR | Municipio. Torrimar station is in 'Guaynabo zona urbana'. |
| San Juan | PR | Municipio. Puerto Rico municipios are county-equivalents; the Census place covering the station area is 'San Juan zona urbana' (Sagrado Corazon, Martínez Nadal, Las Lomas, San Francisco and others verified). |
| North Kingstown | RI | Wickford Junction station, the southern terminus of the Providence/Stoughton Line, is in the town of North Kingstown. |
| Pawtucket | RI | Pawtucket/Central Falls station (opened January 23, 2023) is in Pawtucket; the current station is not in Central Falls. |
| Warwick | RI | T.F. Green Airport station is in the city of Warwick. |
| Lebanon | TN | Lebanon, Hamilton Springs AND Martha stations: the Census geocoder puts Martha station (65 Martha Circle) inside Lebanon city limits. |
| Nashville | TN | Census place name is 'Nashville-Davidson metropolitan government (balance)'. Riverfront, Donelson and Hermitage stations are all in Nashville-Davidson. |
| Addison | TX | Addison station (DART Silver Line) opened Oct 25, 2025; Census geocoder places it in Addison town. |
| Austin | TX | Lakeline station is in the Williamson County portion of Austin city. |
| Fort Worth | TX | TRE: T&P, Fort Worth Central, Trinity Lakes, CentrePort/DFW and Bell stations. Bell and Trinity Lakes sit on the Fort Worth/Hurst line but are in Fort Worth per both station articles and the official TRE station list. Also TEXRail (North Side, Mercantile Center). |
| Grapevine | TX | Served by DART Silver Line (DFW Airport North, opened Oct 25 2025) and by Trinity Metro TEXRail (commuter rail) at DFW Airport North and Grapevine-Main Street. DFW Airport Terminal A/B stations also fall inside Grapevine city limits per the Census geocoder. |
| Houston | TX | All Red, Green and Purple Line stations are inside Houston city limits (termini spot-checked via the Census geocoder). |
| Lewisville | TX | Highland Village/Lewisville Lake, Old Town and Hebron stations are all inside Lewisville city limits. |
| American Fork | UT | American Fork station platform is in the unannexed rail corridor; American Fork city surrounds it and the station article gives borough = American Fork. |
| Alexandria | VA | Independent city; King Street-Old Town, Braddock Road, Van Dorn Street, Eisenhower Avenue, Potomac Yard (opened May 2023). Also VRE |
| Arlington | VA | Arlington VA (not Arlington TX). Arlington CDP is coextensive with Arlington County; 10 Metro stations incl. Rosslyn, Ballston-MU, Pentagon, Crystal City. Also VRE Crystal City |
| Ashburn | VA | CDP, Loudoun County; Silver Line western terminus, opened Nov 15 2022 |
| Burke | VA | CDP, Fairfax County; Rolling Road station (the VRE article also puts Burke Centre station in 'Burke') |
| Burke Centre | VA | CDP, Fairfax County; Burke Centre station |
| Fredericksburg | VA | Independent city; Fredericksburg Line |
| Herndon | VA | Town, Fairfax County; Herndon station opened Nov 15 2022. Wikipedia infobox gives the borough as Herndon; WMATA lists the jurisdiction only as Fairfax County and the platform is on Sunrise Valley Drive, effectively at the town edge |
| Huntington | VA | CDP, Fairfax County; 'the Huntington area of Fairfax County (though its mailing address says Alexandria)' |
| Idylwood | VA | CDP, Fairfax County; West Falls Church station is in Idylwood, NOT in Falls Church city |
| Lorton | VA | CDP, Fairfax County; Fredericksburg Line |
| Manassas | VA | Independent city; Manassas Line |
| Manassas Park | VA | Independent city; Manassas Line |
| McNair | VA | CDP, Fairfax County; Innovation Center station, at SR 267/SR 28 'in McNair, near the Fairfax/Loudoun county line' |
| Merrifield | VA | CDP, Fairfax County; Dunn Loring station ('The station is in Merrifield, with a Vienna mailing address') |
| Norfolk | VA | The whole 7.4 mi line was built inside Norfolk city limits; the eastern terminus (Newtown Road) is at the Norfolk/Virginia Beach boundary. |
| Quantico | VA | Town, Prince William County; Fredericksburg Line |
| Reston | VA | CDP, Fairfax County; Wiehle-Reston East (2014) and Reston Town Center (2022) stations |
| Springfield | VA | CDP, Fairfax County; Franconia-Springfield station (Metro Blue Line terminus + VRE) |
| Sterling | VA | CDP, Loudoun County; Loudoun Gateway station (infobox borough = Sterling), opened Nov 15 2022 |
| Tysons | VA | CDP, Fairfax County; McLean, Tysons, Greensboro and Spring Hill stations. McLean station is 'in the unincorporated community of Tysons, with a McLean postal address' |
| Woodbridge | VA | CDP, Prince William County; Fredericksburg Line |
| Kent | WA | Kent Des Moines and Star Lake stations (opened Dec 6 2025) are both inside Kent, not Des Moines. |
| Harpers Ferry | WV | Town, Jefferson County WV; Brunswick Line |
| Martinsburg | WV | City, Berkeley County WV; Brunswick Line western terminus |
