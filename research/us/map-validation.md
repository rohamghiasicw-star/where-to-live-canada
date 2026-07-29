# US map geometry: independent validation

The rings in `data/us/us_rings.json` were built with pyproj by `src/us/build_map.py`.
`src/us/albers.py` reimplements the identical transform in pure Python, because
`build_app.py` must project a few thousand place coordinates on every build and the
Canadian side deliberately has no third-party dependency. pyproj was only ever
present in a session-scratch venv, so depending on it would have rotted.

## Pure Python vs pyproj 3.7.2

| plane | agreement |
|---|---|
| CONUS (EPSG:5070) | 0.000 cm over 7 test points |
| Alaska (EPSG:3338 + inset) | 0.000 cm over 2 test points |
| Hawaii (ESRI 102007 + inset) | 73 cm |

The Hawaii gap is a datum-handling difference in the proj4 string, not an error in
the formulas. The sheet renders at about 4.6 km per pixel, so 73 cm is 1/6000th of
a pixel. Recorded rather than chased.

## Do the dots land inside their state?

Point-in-polygon against the simplified rings, using the pure-Python transform:

Inland places: all inside, comfortably.

Coastal and island places sit *on* the boundary by definition, so simplification
puts some marginally to seaward. Measured distance outside:

| place | km outside |
|---|---|
| Utqiagvik AK | 0.02 |
| Nome AK | 0.10 |
| Provincetown MA | 0.25 |
| Lihue HI | 0.27 |
| Juneau AK | 0.50 |
| Astoria OR | 0.84 |
| Kodiak AK | 1.85 |
| Sitka AK | 1.88 |
| **Key West FL** | **15.6** |

Everything except Key West is under half a pixel and invisible. Key West is the one
real casualty: the Florida Keys chain is below the island-retention threshold, so
its dot draws in open water south of the mainland, which is approximately where Key
West is. Left as is, and noted here rather than silently.

## Scope

50 states plus DC. Puerto Rico, the USVI, Guam, American Samoa and the Northern
Marianas are absent: Natural Earth files them as separate admin-0 units, not in the
admin-1 states layer, and each would need its own ocean-crossing inset. If any
inhabited place in those territories ends up in the place list it will have no
state ring to sit in, so the place list must exclude them too.
