# Where To Live / Canada

Answer what you actually want out of a place. It re-ranks all 129 Canadian cities and towns against it, on a map, and tells you what each one costs you.

**Live: https://rohamghiasicw-star.github.io/where-to-live-canada/**

Or just open `index.html` in any browser. The whole thing is one self-contained file. Fonts, data, and the map of Canada are all inlined, so it works offline, off a USB stick, or emailed to someone. No server, no build, no dependencies.

---

## Why

This started in a gym change room. Two guys were talking about the weather, wildfire smoke was blowing in from up north, and the conversation turned into what kind of place you would actually want to live in year round.

> "I liked the climate in Vancouver, but the city was too big. Some people might like Alberta, but not the politics. Some might like Halifax, except too much traffic. Goderich, the town is nice, but there are major snowstorms and London is a bit of a drive."

Every "Canada's Most Livable Cities" list answers that by picking the weights for you. This asks you instead.

The Goderich line checks out, by the way. Routed on real roads it is 98.6km and 101 minutes to London.

## What is in it

129 places, from Toronto down to Bayfield, Ontario (population 1,100). Real towns, not just metros.

| Dimension | Source |
|---|---|
| Temperature, snow, rain, sun | Environment and Climate Change Canada, Canadian Climate Normals 1981-2010 |
| Wildfire smoke | ECCC FireWork RAQDPS-FW Cumulative Effects, 2013-2024 |
| Population, income, home values, rent | Statistics Canada, 2021 Census Profile |
| Political lean | Elections Canada, 45th General Election, April 2025 |
| Growth, age, commute, car dependence, jobs, diversity, French | Statistics Canada, 2021 Census Profile |
| Drive to the nearest real city | OSRM routed on OpenStreetMap roads |
| What residents say | Reddit, local news, forums, personal blogs (59 places so far) |

## How it decides

Each question sets a target and how much it matters. A place scores 0 to 1 per dimension, then a weighted mean gives the fit.

Temperature, size, and drive time use distance to your ideal, so wanting a `-5°C` January does not mean colder is always worse. Cost is one-sided: under budget is good and cheaper is better, over budget falls away fast. Two questions can rule a place out completely rather than let a high score elsewhere paper over it, because "too expensive" and "the air is full of smoke" are not things a nice main street compensates for.

Where a place has no data for a dimension, it is dropped from that place's average instead of being scored as average. Missing is not the same as mediocre.

## Things that would have been wrong

Worth stating, because the whole point is that the numbers are real.

**The smoke data is not the obvious smoke data.** ECCC's climate normals include "days with smoke or haze," which looks perfect and is actively backwards: it correlates *negatively* with real wildfire smoke (Pearson −0.22). It counts any visibility obstruction, mostly summer humidity haze, so it gives Goderich 92 days a year and Kamloops 3.5. Shipping it would have told Kelowna families their air is clean. What is used instead is FireWork Cumulative Effects, which is ECCC's air quality model run *with* fires differenced against the run *without*, so it isolates smoke from fire from traffic and wood stoves. Kamloops 2.82 µg/m³, St. John's 0.05. Yellowknife hit 11.8 in 2023, the year it was evacuated. It is a 12-year mean so that 2023, which was roughly 3x a normal year and moves some towns up to 82 rank places on its own, counts once out of twelve.

**Weather stations are not where you live.** Revelstoke's nearest station with published normals is Mount Fidelity, 43km away and 1,431m higher up, reporting 1,388cm of snow. That is the alpine snowpack, not the town. Stations are matched on elevation as well as distance, and Revelstoke now reads 424.6cm from its own airport station 4km away at the right elevation. Every place shows which station its climate came from and how far off it is. Goderich's is Blyth, 26km inland in the snowbelt, which is why its snow number runs high for a lakeside town.

**Nine places had no published normals nearby.** Their figures are computed from raw ECCC monthly observations and labelled as computed, with the year count. Iqaluit has no published normals at all; it uses 13 years of its own station's observations.

**Two of 129 geocodes were wrong.** Kenora resolved to Kenora *District* (54.0°N, hundreds of km off) and Perth to Perth *County*. Both silently poison every distance and climate lookup downstream. Caught by checking each result against its province.

**Statistics Canada ships that file as latin-1.** Read as UTF-8 with error replacement, "Montréal" quietly becomes `montral` and every accented Quebec place fails to match while the script reports no error.

## Honesty

Resident research covers 59 of 129 places, and is missing Quebec and Atlantic Canada. The rest are scored on measured data only and say so. Every quote links to the page it came from, so you can check it.

Small towns have thin data. Where a number is missing it is left blank rather than guessed at.

Sydney is reported as Cape Breton Regional Municipality, which is the census subdivision, so its population is the whole municipality. Same for Halifax.

The political axis is a judgement call, not a measurement. Party positions are set in `src/build_politics.py` and the vote-weighted math is right there to argue with.

Nothing here is a recommendation. It is a way to argue with a list.

## Rebuilding

```bash
python3 src/build_app.py     # reassemble index.html from data/
```

The other scripts in `src/` regenerate each dataset from its source. They document the exact endpoints. Some need large downloads (the census profile is a 2.6GB CSV).

## The design

It is built as a field guide, not a dashboard. Seventeen dimensions across 129 places is the problem Peterson and Sibley solved for birds: here are many similar things, help me tell mine apart.

The rule everything is checked against: **a graphical move is convincing when it is a function of the data, and costume when it is a layer over the data.** Test any mark by asking whether its value could have come out different. A compass rose always points north, so it carries no information. A magnetic declination diagram looks like its cousin but carries a real angle stamped with an epoch, because it decays.

What that produced:

- **Positional constancy.** The column order never changes, so the eye can detect difference. Read down a column to compare one thing across the country, across a row to read one place.
- **Missing values keep their slot** and read `..`, which is StatCan's own published symbol for "not available". An MLS card leaves `Taxes` blank rather than deleting the cell. The empty slot is information.
- **Provenance has its own ink.** USGS and NRCan each spend a scarce plate saying how much of the sheet was field checked. 59 of 129 places have resident research and the rest do not, and they must not render identically.
- **One arrow, rationed.** It marks the single dimension that separates a place from the ones it ties with. It points at what *distinguishes*, not at what is good.
- **No dark mode.** There is no dark-mode paper.
- **No monospace.** The 1985 MLS book was a proportional grotesque. The inheritance from that tradition is tabular figures, not typewriter cosplay.

Type is **Radio Canada** by Coppers and Brasses of Montréal, commissioned for CBC/Radio-Canada, OFL. Chosen for fit rather than novelty, and because it ships real tabular figures. The previous stack declared `font-variant-numeric: tabular-nums` while shipping no font that had the feature, so the incantation did nothing. Its width axis carries data: a big city sets wide, a village narrow.

Map geometry from Natural Earth, projected to Statistics Canada Lambert (EPSG:3347), the projection Canada is actually drawn in.

Idea by a guy in a change room who was right.
