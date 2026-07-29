"""
src/us/build_osm.py - real OpenStreetMap amenity counts for every US place in
data/us/places.json.  US sibling of src/build_osm.py (Canada).  Writes
data/us/osm.json and touches nothing else.

WHY THIS FILE EXISTS AT ALL
  The app's originator asked for two things by name: "number of soccer pitches"
  as a fun, non-boring ranking category, and places of worship, because "a
  Jewish person would want a synagogue within driving distance".  Both are real
  OSM tags.  In the US version they matter MORE than in Canada: the US census
  does not ask about religion at all, so there is no US equivalent of the
  Canadian census religion table.  Counting the actual buildings in OSM is the
  only honest way to answer "is there a synagogue near me" for a US place.

WHAT IT COUNTS (all straight from OSM tags, nothing modelled or estimated)
  soccer_pitches   leisure=pitch  AND sport contains "soccer"
                   (semicolon multi-values count, e.g. sport=soccer;baseball)
  churches         amenity=place_of_worship  religion=christian
  mosques          amenity=place_of_worship  religion=muslim
  synagogues       amenity=place_of_worship  religion=jewish
  temples_hindu    amenity=place_of_worship  religion=hindu
  gurdwaras        amenity=place_of_worship  religion=sikh
  temples_buddhist amenity=place_of_worship  religion=buddhist
  worship_total    every amenity=place_of_worship, whatever the religion tag
                   says (plenty of US entries have no religion tag at all, so
                   worship_total is always >= the sum of the six buckets)
  ice_rinks        leisure=ice_rink, plus leisure=pitch / leisure=sports_centre
                   with sport containing "ice_hockey"

  Exactly the nine fields the Canadian file carries, same names, same tag
  tests, so the two countries are directly comparable.

HOW THE DATA IS FETCHED  (efficiency is the whole problem here)
  4,197 separate per-place Overpass "around" queries would be ~4,197 calls and
  would be throttled off the API long before finishing, so this does NOT do
  that.  Instead: 51 large queries, one per state + DC, each clipped to that
  state's OSM admin_level=4 relation area, plus 7 cross-border band queries
  (below).  One query pulls all three categories at once as a union.  Nodes,
  ways and relations ("nwr") are all returned, with "out center;" so ways and
  relations carry a coordinate.  Everything is then assigned to places locally
  by great-circle distance.  58 calls total instead of 4,197.

  Sequential, never parallel.  600 s server-side timeout, 700 s socket
  timeout, exponential backoff on 429/504, endpoint rotation, 4 s pause
  between states.  Raw responses are cached on disk keyed by region, so a
  restart or a re-run costs the API nothing.

  A GEOFABRIK EXTRACT WAS CONSIDERED AND REJECTED.  us-latest.osm.pbf is
  ~12 GB and needs osmium/pyosmium to read; neither was installed on this
  machine and only 33 GB of disk was free, so the download plus a node-location
  index would have been tighter on disk than on patience.  Overpass with
  51 state-clipped queries returns only the ~0.5 M elements actually wanted
  instead of ~10^9 nodes, and the state areas make the coverage auditable
  region by region.  If this ever needs to be re-run monthly, switch to the
  extract; for a one-off build Overpass is the cheaper and more reliable path.

  STATE RELATION IDS were not typed from memory.  They were resolved live by
  querying rel["ISO3166-2"~"^US-"][admin_level=4] before this script was
  written: 56 relations, 56 distinct ISO codes, no duplicates and no misses.
  The five territory codes (PR VI GU AS MP) are deliberately dropped, which
  also drops the 29 Puerto Rico places in data/us/places.json.

CROSS-BORDER BANDS
  A state-clipped query stops at the international border, which would quietly
  understate every border metro: half of El Paso's 15 km disc is Ciudad
  Juarez, half of Detroit's is Windsor, half of San Diego's is Tijuana.  So
  seven extra queries fetch the same three categories from the Canadian and
  Mexican side, clipped to the country area intersected with a bounding band
  that follows the border.  Over-fetching is harmless: an element is only ever
  used if it lands within 15 km of a US place, and everything else is thrown
  away.  Under-fetching is the honest limit - the bands reach roughly 150-250 km
  inland, far more than the 15 km that can matter, but a US place whose disc
  somehow reached foreign ground outside a band would be US-side only.  No
  such place exists in this input.

ASSIGNMENT RULE  (this is the whole meaning of the numbers - read it)

  THE MAIN FIELDS ARE A 15 KM RADIUS COUNT.  Same 15 km as the Canadian build.
  soccer_pitches, churches, ... , ice_rinks count every matching OSM element
  whose coordinate is within RADIUS_KM (15 km) great-circle of the place's
  point in data/us/places.json.  Nothing else.  An element within 15 km of
  three places is counted for all three - Cambridge, Somerville and Boston
  legitimately overlap, because "is there a synagogue near me" does not care
  which municipality it is filed under.  Every place therefore covers the SAME
  707 km2 of ground, which is the only way 4,197 counts are comparable to each
  other.  15 km is a normal short drive, and it is about the equivalent-circle
  radius of the City of Toronto (630 km2 -> 14.2 km) or of Denver
  (397 km2 -> 11.2 km).
  DO NOT SUM THESE ACROSS PLACES.  The overlaps mean the column does not add
  up to a national total.

  THE *_exclusive FIELDS ARE A PARTITION.
  Each element is also given to exactly ONE place - the nearest by great-circle
  distance, still capped at 15 km - and counted in soccer_pitches_exclusive,
  churches_exclusive and so on.  No double counting, so these DO sum to a
  national total, and an element beyond 15 km of every place is in no place.

  WHY BOTH EXIST.  Carried over verbatim from the Canadian build, where a
  nearest-place-only rule was tried first and proved badly misleading, because
  the place list mixes huge amalgamated cities with tiny enclaves: Montreal's
  nearest listed neighbour is 3.1 km away so its cell was a ~3 km blob (39
  soccer pitches) while Calgary kept a full 15 km disc (426), a ~20x
  difference in catchment AREA masquerading as a difference in soccer pitches.
  The US place list is far worse in this respect - it has 498 California
  places, and Los Angeles is ringed by West Hollywood, Beverly Hills, Culver
  City and Inglewood at 3-12 km - so the radius fields are the honest headline
  number for "within driving distance" and the exclusive fields are kept only
  for anyone who needs a true partition.

DEDUPE
  OSM sometimes carries the same real-world thing twice (a node inside its own
  building way, or a multipolygon relation plus its outer way).  Two passes,
  both requiring a shared category:
    1. same non-empty name within 100 m  -> collapse to one.
    2. an UNNAMED element within 50 m of a NAMED one -> drop the unnamed.
  Pass 2 exists because the commonest real duplicate is a named worship node
  sitting inside its own unnamed building way, and pass 1 alone counts it
  twice.  Identical rule to the Canadian build; the only difference is that
  both passes are run through a 0.01 deg (~1.1 km) grid instead of a flat
  scan, because at US scale a name like "first baptist church" appears
  thousands of times nationally and an all-pairs scan inside one name bucket
  would be quadratic.  The grid restricts comparisons to the 3x3 cell
  neighbourhood, which is strictly larger than the 100 m test radius, so the
  answer is the same and the run is not O(n^2).

COORDINATE TWINS (affects the *_exclusive fields only)
  If two places in the input sit within TIE_KM (1 km) of each other, "nearest
  place" is a coin flip and a strict winner-takes-all would hand one twin
  everything and report a fabricated 0 for the other.  Places that close are
  treated as one tie-group and every member is credited with whatever the
  group wins, so neither shows a fake zero.  Those particular *_exclusive
  counts are the one case that is NOT additive.  The radius fields need no
  special handling: two places at nearly the same point simply have nearly the
  same disc.  The groups found in this input are printed at build time.

HONEST ZEROS
  Zero is a real answer and is never filled in.  A small town with no mosque
  inside 15 km gets mosques = 0, because OSM says there is none.  The only
  nulls written are for a region whose Overpass query failed permanently - all
  nine fields go null for every place in it and the region is named in the
  build log, so a missing region can never be mistaken for a real zero.

Reads data/us/places.json.  Writes data/us/osm.json.  Nothing else is touched -
not the Canadian data, not the app code, not data/us/places.json.

  python3 src/us/build_osm.py               # uses the cached Overpass responses
  python3 src/us/build_osm.py --refetch     # re-hits the API for every region
  python3 src/us/build_osm.py --state=RI,MA # one or more regions only
  python3 src/us/build_osm.py --check       # rebuild + print the check table
"""

import json, math, os, sys, tempfile, time
import urllib.request, urllib.parse, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Raw Overpass responses are cached here so a re-run costs the API nothing.
# Delete this directory (or pass --refetch) to pull fresh data.
CACHE = os.environ.get("US_OSM_CACHE",
                       os.path.join(tempfile.gettempdir(), "livable_us_osm_cache"))
os.makedirs(CACHE, exist_ok=True)

RADIUS_KM = 15.0
DEDUPE_M = 100.0          # same-name collapse radius
DEDUPE_UNNAMED_M = 50.0   # unnamed-into-named collapse radius
TIE_KM = 1.0              # places this close share a catchment (see COORDINATE TWINS)
UA = "livable-city-ranking/1.0 (one-off research build; rohamghiasicw@gmail.com)"

# Global-coverage mirrors ONLY, rotated on every attempt because the main
# instance answers "Dispatcher_Client::request_read_and_idx::timeout - server is
# probably too busy" under load.  A regional-extract mirror (overpass.osm.ch is
# Switzerland-only) answers 200 OK with zero elements for a US area id, which is
# worse than an error because it would cache a silent fake zero for a whole
# state.  sane() below refuses any response that is empty or lands outside the
# expected box, so such a mirror can never poison the cache.
ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

# OSM admin_level=4 relation ids, resolved live by querying
# rel["ISO3166-2"~"^US-"][admin_level=4] before this script was written.
# Territories (PR VI GU AS MP) are intentionally absent.
STATE_REL = {
    'AK': 1116270, 'AL': 161950, 'AR': 161646, 'AZ': 162018, 'CA': 165475, 'CO': 161961,
    'CT': 165794, 'DC': 162069, 'DE': 162110, 'FL': 162050, 'GA': 161957, 'HI': 166563,
    'IA': 161650, 'ID': 162116, 'IL': 122586, 'IN': 161816, 'KS': 161644, 'KY': 161655,
    'LA': 224922, 'MA': 61315, 'MD': 162112, 'ME': 63512, 'MI': 165789, 'MN': 165471,
    'MO': 161638, 'MS': 161943, 'MT': 162115, 'NC': 224045, 'ND': 161653, 'NE': 161648,
    'NH': 67213, 'NJ': 224951, 'NM': 162014, 'NV': 165473, 'NY': 61320, 'OH': 162061,
    'OK': 161645, 'OR': 165476, 'PA': 162109, 'RI': 392915, 'SC': 224040, 'SD': 161652,
    'TN': 161838, 'TX': 114690, 'UT': 161993, 'VA': 224042, 'VT': 60759, 'WA': 165479,
    'WI': 165466, 'WV': 162068, 'WY': 161991,
}
TERRITORIES = {"PR", "VI", "GU", "AS", "MP"}

# Cross-border bands: country relation id + (south, west, north, east) box that
# follows the international border.  Only elements landing within 15 km of a US
# place are ever used, so the generous inland reach costs nothing but bytes.
CANADA_REL = 1428125
MEXICO_REL = 114686
BORDER_BANDS = {
    # name            country rel   south   west     north   east
    "CA_west":       (CANADA_REL,  (48.0, -139.5,  50.5,  -95.0)),   # BC AB SK MB
    "CA_ontario_nw": (CANADA_REL,  (47.0,  -95.0,  50.5,  -84.0)),   # Superior / MN
    "CA_ontario_s":  (CANADA_REL,  (41.5,  -84.0,  46.5,  -74.0)),   # Windsor Sarnia Niagara
    "CA_quebec_s":   (CANADA_REL,  (44.5,  -78.0,  46.8,  -66.5)),   # NY VT NH border
    "CA_maritimes":  (CANADA_REL,  (44.5,  -69.5,  48.5,  -63.5)),   # NB / Maine
    "CA_yukon_bc":   (CANADA_REL,  (54.0, -141.5,  70.0, -122.0)),   # AK panhandle + north
    "MX_border":     (MEXICO_REL,  (25.5, -117.5,  33.0,  -97.0)),   # CA AZ NM TX
}

QUERY_AREA = """[out:json][timeout:600];
area(%d)->.a;
(
  nwr["leisure"="pitch"]["sport"~"(^|;)soccer(;|$)"](area.a);
  nwr["amenity"="place_of_worship"](area.a);
  nwr["leisure"="ice_rink"](area.a);
  nwr["leisure"~"^(pitch|sports_centre)$"]["sport"~"(^|;)ice_hockey(;|$)"](area.a);
);
out center;"""

QUERY_BAND = """[out:json][timeout:600];
area(%d)->.a;
(
  nwr["leisure"="pitch"]["sport"~"(^|;)soccer(;|$)"](area.a)(%f,%f,%f,%f);
  nwr["amenity"="place_of_worship"](area.a)(%f,%f,%f,%f);
  nwr["leisure"="ice_rink"](area.a)(%f,%f,%f,%f);
  nwr["leisure"~"^(pitch|sports_centre)$"]["sport"~"(^|;)ice_hockey(;|$)"](area.a)(%f,%f,%f,%f);
);
out center;"""

# Per-region sanity box (south, west, north, east).  A response is refused if it
# is empty or if fewer than 90% of its elements fall inside the box, which is
# what catches a mirror serving the wrong database.  States get a generous
# continental/AK/HI box; bands get their own band box.
US_BOX = (17.0, -180.0, 72.0, -64.0)
AK_BOX = (51.0, -180.0, 72.0, -129.0)
HI_BOX = (18.0, -161.0, 23.0, -154.0)


def region_box(region):
    if region in BORDER_BANDS:
        s, w, n, e = BORDER_BANDS[region][1]
        return (s - 0.5, w - 0.5, n + 0.5, e + 0.5)
    if region == "AK":
        return AK_BOX
    if region == "HI":
        return HI_BOX
    return US_BOX


def coord(el):
    if "lat" in el and "lon" in el:
        return el["lat"], el["lon"]
    c = el.get("center")
    if c:
        return c["lat"], c["lon"]
    return None


def sane(region, d):
    """Refuse a response that cannot be a real answer for this region.

    Guards against a mirror that holds only a regional extract: it resolves the
    US area id to nothing and returns 200 OK with zero elements, which would be
    cached as a fabricated zero for every place in the state.
    """
    els = d.get("elements")
    if els is None:
        return "no elements key"
    if len(els) == 0:
        return "zero elements - no US state has zero churches/pitches/rinks"
    box = region_box(region)
    inbox = 0
    for el in els:
        c = coord(el)
        if c and box[0] <= c[0] <= box[2] and box[1] <= c[1] <= box[3]:
            inbox += 1
    if inbox < 0.9 * len(els):
        return "only %d/%d elements inside the %s box - wrong database?" % (
            inbox, len(els), region)
    return None


def build_query(region):
    if region in BORDER_BANDS:
        rel, b = BORDER_BANDS[region]
        return QUERY_BAND % ((3600000000 + rel,) + b * 4)
    return QUERY_AREA % (3600000000 + STATE_REL[region])


def fetch(region, force=False):
    """One Overpass call for one region. Cached. Retries with backoff."""
    path = os.path.join(CACHE, "osm_%s.json" % region)
    if os.path.exists(path) and not force:
        with open(path) as f:
            d = json.load(f)
        bad = sane(region, d)
        if bad:
            print("  %s cached file REJECTED (%s), refetching" % (region, bad))
        else:
            print("  %-14s cached: %6d elements" % (region, len(d["elements"])))
            return d
    body = urllib.parse.urlencode({"data": build_query(region)}).encode()
    delay = 30
    for attempt in range(10):
        ep = ENDPOINTS[attempt % len(ENDPOINTS)]
        try:
            t0 = time.time()
            req = urllib.request.Request(ep, data=body, headers={"User-Agent": UA})
            raw = urllib.request.urlopen(req, timeout=700).read()
            d = json.loads(raw)
            bad = sane(region, d)
            if bad:
                raise ValueError("bad response from %s: %s" % (ep.split("/")[2], bad))
            print("  %-14s ok: %6d elements in %5.0fs (%s)"
                  % (region, len(d["elements"]), time.time() - t0, ep.split("/")[2]))
            tmp = path + ".part"
            with open(tmp, "w") as f:
                json.dump(d, f)
            os.replace(tmp, path)
            time.sleep(4)  # be polite between regions
            return d
        except Exception as e:
            code = getattr(e, "code", "")
            print("  %-14s attempt %d failed (%s %s), sleeping %ds"
                  % (region, attempt + 1, code, str(e)[:110].replace("\n", " "), delay),
                  flush=True)
            time.sleep(delay)
            delay = min(int(delay * 1.7), 300)
    raise RuntimeError("Overpass failed for %s after 10 attempts" % region)


def hav(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p = math.radians
    dla = p(lat2 - lat1)
    dlo = p(lon2 - lon1)
    x = math.sin(dla / 2) ** 2 + math.cos(p(lat1)) * math.cos(p(lat2)) * math.sin(dlo / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


SOCCER = "soccer"
HOCKEY = "ice_hockey"


def has_sport(tags, want):
    s = tags.get("sport", "")
    return want in [x.strip() for x in s.split(";")]


def categorise(el):
    """Return the set of category keys this element counts toward."""
    t = el.get("tags", {})
    out = set()
    if t.get("leisure") == "pitch" and has_sport(t, SOCCER):
        out.add("soccer_pitches")
    if t.get("amenity") == "place_of_worship":
        out.add("worship_total")
        rel = (t.get("religion") or "").strip().lower()
        rmap = {"christian": "churches", "muslim": "mosques", "jewish": "synagogues",
                "hindu": "temples_hindu", "sikh": "gurdwaras", "buddhist": "temples_buddhist"}
        if rel in rmap:
            out.add(rmap[rel])
    if t.get("leisure") == "ice_rink" or (
        t.get("leisure") in ("pitch", "sports_centre") and has_sport(t, HOCKEY)
    ):
        out.add("ice_rinks")
    return out


FIELDS = ["soccer_pitches", "churches", "mosques", "synagogues", "temples_hindu",
          "gurdwaras", "temples_buddhist", "worship_total", "ice_rinks"]

METHOD = ("count within radius_km great-circle of the place point; overlaps between "
          "neighbouring places are real, do not sum this column")
METHOD_EXCL = ("same elements partitioned to the single nearest place within radius_km; "
               "this column does sum")

CELL = 0.01  # ~1.1 km lat; comfortably larger than the 100 m dedupe test radius
PCELL = 0.25  # place index cell, degrees


def dedupe(tagged):
    """Two-pass near-duplicate collapse, identical rule to the Canadian build."""
    # pass 1: same non-empty name within 100 m and sharing a category.
    keep = []
    dropped_dupe = 0
    buckets = {}
    for r in tagged:
        nm = r[3]
        if not nm:
            keep.append(r)
            continue
        gx, gy = int(r[0] / CELL), int(r[1] / CELL)
        dup = False
        for ax in (gx - 1, gx, gx + 1):
            for ay in (gy - 1, gy, gy + 1):
                for prev in buckets.get((nm, ax, ay), ()):
                    if prev[2] & r[2] and hav(prev[0], prev[1], r[0], r[1]) * 1000 <= DEDUPE_M:
                        dup = True
                        break
                if dup:
                    break
            if dup:
                break
        if dup:
            dropped_dupe += 1
            continue
        buckets.setdefault((nm, gx, gy), []).append(r)
        keep.append(r)
    tagged = keep
    print("after same-name/100m dedupe: %d  (collapsed %d)" % (len(tagged), dropped_dupe))

    # pass 2: an unnamed element sitting on top of a named one, same category,
    # is the same building mapped twice. Drop the unnamed one.
    grid = {}
    for p in tagged:
        if p[3]:
            grid.setdefault((int(p[0] / CELL), int(p[1] / CELL)), []).append(p)
    keep2 = []
    dropped_un = 0
    for r in tagged:
        if r[3]:
            keep2.append(r)
            continue
        gx, gy = int(r[0] / CELL), int(r[1] / CELL)
        dup = False
        for ax in (gx - 1, gx, gx + 1):
            for ay in (gy - 1, gy, gy + 1):
                for p in grid.get((ax, ay), ()):
                    if p[2] & r[2] and hav(p[0], p[1], r[0], r[1]) * 1000 <= DEDUPE_UNNAMED_M:
                        dup = True
                        break
                if dup:
                    break
            if dup:
                break
        if dup:
            dropped_un += 1
        else:
            keep2.append(r)
    print("after unnamed-on-named/50m dedupe: %d  (collapsed %d)" % (len(keep2), dropped_un))
    return keep2


def tie_groups(plat, plon, pkey):
    """Union places within TIE_KM into shared-catchment groups."""
    n = len(plat)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    grid = {}
    for i in range(n):
        grid.setdefault((int(plat[i] / PCELL), int(plon[i] / PCELL)), []).append(i)
    for i in range(n):
        gx, gy = int(plat[i] / PCELL), int(plon[i] / PCELL)
        for ax in (gx - 1, gx, gx + 1):
            for ay in (gy - 1, gy, gy + 1):
                for j in grid.get((ax, ay), ()):
                    if j <= i:
                        continue
                    if hav(plat[i], plon[i], plat[j], plon[j]) <= TIE_KM:
                        parent[find(i)] = find(j)
    group = {}
    for i in range(n):
        group.setdefault(find(i), []).append(i)
    twins = [g for g in group.values() if len(g) > 1]
    print("coordinate tie-groups (shared catchment): %d groups, %d places"
          % (len(twins), sum(len(g) for g in twins)))
    for g in sorted(twins, key=lambda g: pkey[g[0]]):
        print("    " + " == ".join("%s, %s" % pkey[i] for i in g))
    return find, group


def main():
    force = "--refetch" in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--state="):
            only = a.split("=", 1)[1].split(",")

    raw = json.load(open(os.path.join(ROOT, "data", "us", "places.json")))
    skipped = [p for p in raw if p["state"] in TERRITORIES]
    places = [{"name": p["name"], "state": p["state"], "lat": p["lat"], "lon": p["lon"]}
              for p in raw if p["state"] not in TERRITORIES]
    print("places: %d  (skipped %d territory places: %s)"
          % (len(places), len(skipped),
             ",".join(sorted({p["state"] for p in skipped})) or "none"))

    regions = only or (list(STATE_REL) + list(BORDER_BANDS))
    print("fetching %d regions from Overpass (%d states+DC, %d cross-border bands)"
          % (len(regions), sum(1 for r in regions if r in STATE_REL),
             sum(1 for r in regions if r in BORDER_BANDS)))
    elements = []
    failed = []
    for rg in regions:
        try:
            d = fetch(rg, force=force)
        except Exception as e:
            print("  !! %s FAILED PERMANENTLY: %s" % (rg, e))
            failed.append(rg)
            continue
        for el in d["elements"]:
            elements.append(el)
    print("total raw elements fetched: %d" % len(elements))
    if failed:
        print("FAILED REGIONS (their places get nulls, not zeros): %s" % ",".join(failed))

    # one element can be returned by two region queries if it straddles a
    # border or sits in a band overlap; dedupe on (type, id) first.
    seen = {}
    for el in elements:
        seen[(el["type"], el["id"])] = el
    elements = list(seen.values())
    print("after id dedupe: %d" % len(elements))

    # classify + coordinate
    tagged = []
    nocoord = 0
    for el in elements:
        cats = categorise(el)
        if not cats:
            continue
        c = coord(el)
        if c is None:
            nocoord += 1
            continue
        tagged.append((c[0], c[1], cats,
                       (el.get("tags", {}).get("name") or "").strip().lower(),
                       el["type"], el["id"]))
    print("classified elements: %d  (dropped %d with no coordinate)" % (len(tagged), nocoord))
    tagged.sort(key=lambda r: (r[3], r[0], r[1]))
    tagged = dedupe(tagged)

    # ---- assignment ------------------------------------------------------
    counts = {(p["name"], p["state"]): {f: 0 for f in FIELDS} for p in places}
    excl = {(p["name"], p["state"]): {f: 0 for f in FIELDS} for p in places}
    plat = [p["lat"] for p in places]
    plon = [p["lon"] for p in places]
    pkey = [(p["name"], p["state"]) for p in places]
    if len(counts) != len(places):
        print("WARNING: %d places collapse to %d name+state keys"
              % (len(places), len(counts)))
    find, group = tie_groups(plat, plon, pkey)

    # place index so each element only tests nearby places, not all 4,197.
    pgrid = {}
    for i in range(len(places)):
        pgrid.setdefault((int(plat[i] / PCELL), int(plon[i] / PCELL)), []).append(i)

    dlat = RADIUS_KM / 110.574 + 1e-9
    assigned = 0
    unassigned = 0
    inradius = 0
    for la, lo, cats, nm, ty, oid in tagged:
        dlon = RADIUS_KM / (111.320 * max(math.cos(math.radians(la)), 1e-6)) + 1e-9
        rx = int(dlat / PCELL) + 1
        ry = int(dlon / PCELL) + 1
        gx, gy = int(la / PCELL), int(lo / PCELL)
        best = None
        bestd = 1e18
        near = []
        for ax in range(gx - rx, gx + rx + 1):
            for ay in range(gy - ry, gy + ry + 1):
                for i in pgrid.get((ax, ay), ()):
                    if abs(plat[i] - la) > dlat or abs(plon[i] - lo) > dlon:
                        continue
                    d = hav(la, lo, plat[i], plon[i])
                    if d <= RADIUS_KM:
                        near.append(i)
                    if d < bestd:
                        bestd = d
                        best = i

        # main fields: every place whose 15 km disc contains this element
        for i in near:
            c = counts[pkey[i]]
            for k in cats:
                c[k] += 1
        if near:
            inradius += 1

        # *_exclusive fields: the nearest place only (tie-groups share)
        if best is None or bestd > RADIUS_KM:
            unassigned += 1
            continue
        assigned += 1
        for i in group[find(best)]:
            c = excl[pkey[i]]
            for k in cats:
                c[k] += 1
    print("within 15 km of at least one place: %d   (radius fields)" % inradius)
    print("assigned to a nearest place: %d   beyond %.0f km of every place: %d"
          "   (exclusive fields)" % (assigned, RADIUS_KM, unassigned))

    out = []
    for p in places:
        k = (p["name"], p["state"])
        dead = p["state"] in failed
        rec = {"name": p["name"], "state": p["state"]}
        for f in FIELDS:
            rec[f] = None if dead else counts[k][f]
        rec["radius_km"] = RADIUS_KM
        rec["method"] = METHOD
        for f in FIELDS:
            rec[f + "_exclusive"] = None if dead else excl[k][f]
        rec["method_exclusive"] = METHOD_EXCL
        out.append(rec)

    path = os.path.join(ROOT, "data", "us", "osm.json")
    tmp = path + ".part"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=0)
    os.replace(tmp, path)
    print("wrote %s (%d places, %.1f MB)"
          % (path, len(out), os.path.getsize(path) / 1e6))
    if "--check" in sys.argv:
        check(out)
    return out


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------

BIG = [("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX")]
SIGNALS = [("Lakewood", "NJ"), ("Brookline", "MA"), ("Dearborn", "MI"), ("Paterson", "NJ"),
           ("Salt Lake City", "UT"), ("Minneapolis", "MN"), ("Boston", "MA"),
           ("Phoenix", "AZ"), ("Miami", "FL")]
SMALL = [("Lost Springs", "WY"), ("Monowi", "NE")]


def check(out):
    ix = {(r["name"], r["state"]): r for r in out}
    cols = ["soccer_pitches", "worship_total", "churches", "synagogues", "mosques",
            "temples_hindu", "gurdwaras", "temples_buddhist", "ice_rinks"]
    hdr = "%-26s" % "place" + "".join("%9s" % c[:8] for c in cols)

    def row(k):
        r = ix.get(k)
        if r is None:
            return "%-26s  NOT IN OUTPUT" % ("%s, %s" % k)
        return "%-26s" % ("%s, %s" % k) + "".join(
            "%9s" % ("null" if r[c] is None else r[c]) for c in cols)

    print("\n=== CHECK TABLE (15 km radius counts) ===")
    print(hdr)
    print("-" * len(hdr))
    print("-- the four biggest metros: expect the most pitches and worship --")
    for k in BIG:
        print(row(k))
    print("-- named signal places: a zero here means the query or assignment is wrong --")
    for k in SIGNALS:
        print(row(k))
    print("-- top 10 by soccer_pitches --")
    for r in sorted([r for r in out if r["soccer_pitches"] is not None],
                    key=lambda r: -r["soccer_pitches"])[:10]:
        print(row((r["name"], r["state"])))
    print("-- top 10 by worship_total --")
    for r in sorted([r for r in out if r["worship_total"] is not None],
                    key=lambda r: -r["worship_total"])[:10]:
        print(row((r["name"], r["state"])))
    print("-- top 10 by synagogues --")
    for r in sorted([r for r in out if r["synagogues"] is not None],
                    key=lambda r: -r["synagogues"])[:10]:
        print(row((r["name"], r["state"])))
    print("-- top 10 by mosques --")
    for r in sorted([r for r in out if r["mosques"] is not None],
                    key=lambda r: -r["mosques"])[:10]:
        print(row((r["name"], r["state"])))
    print("-- top 10 by ice_rinks --")
    for r in sorted([r for r in out if r["ice_rinks"] is not None],
                    key=lambda r: -r["ice_rinks"])[:10]:
        print(row((r["name"], r["state"])))

    live = [r for r in out if r["worship_total"] is not None]
    print("\ncoverage: %d/%d places have real counts, %d null (failed region)"
          % (len(live), len(out), len(out) - len(live)))
    for f in FIELDS:
        nz = sum(1 for r in live if r[f])
        tot = sum(r[f + "_exclusive"] for r in live)
        print("  %-17s nonzero in %5d/%d places   exclusive national total %d"
              % (f, nz, len(live), tot))


if __name__ == "__main__":
    main()
