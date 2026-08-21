"""
build_osm.py - real OpenStreetMap amenity counts for every place in data/climate.json.

WHAT IT COUNTS (all straight from OSM tags, nothing modelled or estimated)
  soccer_pitches   leisure=pitch  AND sport contains "soccer"
                   (semicolon multi-values count, e.g. sport=soccer;baseball)
  churches         amenity=place_of_worship  religion=christian
  mosques          amenity=place_of_worship  religion=muslim
  synagogues       amenity=place_of_worship  religion=jewish
  temples_hindu    amenity=place_of_worship  religion=hindu
  gurdwaras        amenity=place_of_worship  religion=sikh
  temples_buddhist amenity=place_of_worship  religion=buddhist
  worship_total    every amenity=place_of_worship, whatever the religion tag says
                   (many Canadian entries have no religion tag at all, so
                    worship_total is always >= the sum of the six buckets)
  ice_rinks        leisure=ice_rink, plus leisure=pitch / leisure=sports_centre
                   with sport containing "ice_hockey"

HOW THE DATA IS FETCHED
  13 Overpass queries, one per province/territory, each clipped to that
  province's OSM admin_level=4 relation area. One query pulls all three
  categories at once as a union. Nodes, ways and relations ("nwr") are all
  returned, with "out center;" so ways/relations carry a coordinate.
  Sequential, long server-side timeout, exponential backoff on 429/504.
  Raw responses are cached on disk so re-runs do not re-hit the API.

ASSIGNMENT RULE  (this is the whole meaning of the numbers - read it)

  THE MAIN FIELDS ARE A 15 KM RADIUS COUNT.
  soccer_pitches, churches, ... , ice_rinks count every matching OSM element
  whose coordinate is within RADIUS_KM (15 km) great-circle of the place's
  point in data/climate.json. Nothing else. An element within 15 km of three
  places is counted for all three - Burnaby's total and Vancouver's total
  legitimately overlap, because "is there a synagogue near me" does not care
  which municipality it is filed under. Every place therefore covers the SAME
  707 km2 of ground, which is the only way 712 counts are comparable to each
  other. 15 km is about the equivalent-circle radius of the City of Toronto
  (630 km2 -> 14.2 km) and is a normal short drive.
  DO NOT SUM THESE ACROSS PLACES. The overlaps mean the column does not add
  up to a national total.

  THE *_exclusive FIELDS ARE A PARTITION.
  Each element is also given to exactly ONE place - the nearest by great-circle
  distance, still capped at 15 km - and counted in soccer_pitches_exclusive,
  churches_exclusive and so on. No double counting, so these DO sum to a
  national total, and an element beyond 15 km of every place is in no place.

  WHY BOTH EXIST. A nearest-place-only rule was built first and it is badly
  misleading in this dataset, because the place list mixes huge amalgamated
  cities with tiny enclaves. Montreal's nearest listed neighbour is Westmount
  at 3.1 km, so its cell is a ~3 km blob and it scored 39 soccer pitches;
  Calgary's nearest neighbour is 16.4 km away so it kept a full 15 km disc and
  scored 426. That is a ~20x difference in catchment AREA masquerading as a
  difference in soccer pitches, and it put Town of Mount Royal above Montreal
  on places of worship. The radius fields are the honest headline number and
  the exclusive fields are kept for anyone who needs a true partition.

DEDUPE
  OSM sometimes carries the same real-world thing twice (a node inside its own
  building way, or a multipolygon relation plus its outer way). Two passes,
  both requiring a shared category:
    1. same non-empty name within 100 m  -> collapse to one.
    2. an UNNAMED element within 50 m of a NAMED one -> drop the unnamed.
  Pass 2 exists because the commonest real duplicate is a named worship node
  sitting inside its own unnamed building way - Gander's Evangel Pentecostal
  Church is node 1487667293 and way 982460796, 13 m apart, and pass 1 alone
  counts it twice. Measured on the Atlantic provinces this is ~1.1% of
  elements. Two unnamed elements are never merged with each other, so genuinely
  distinct unnamed pitches side by side both still count.

COORDINATE TWINS (affects the *_exclusive fields only)
  data/climate.json contains 8 pairs of places that carry the SAME point, so
  "nearest place" is a genuine tie and a strict winner-takes-all would hand one
  twin everything and report a fabricated 0 for the other:
    Yarmouth (Town)/(District) NS, Digby (Town)/(District) NS,
    Lunenburg (Town)/(District) NS, Antigonish (Town)/(Subd. A) NS,
    Langley (City)/(District) BC, North Vancouver (City)/(District) BC,
    Nanaimo/Nanaimo A BC, and Kitchener/Waterloo ON.
  Places within TIE_KM (1 km) of each other are treated as one tie-group, and
  when a group wins an element every member of the group is credited with it.
  So both twins report the same shared count and neither shows a fake zero.
  Those *_exclusive counts are the one case that is NOT additive - do not sum
  Kitchener and Waterloo. The radius fields need no special handling: two
  places at the same point simply have the same disc.

Reads data/climate.json. Writes data/osm.json. Nothing else is touched.

  python3 src/build_osm.py              # uses the cached Overpass responses
  python3 src/build_osm.py --refetch    # re-hits the API for every province
  python3 src/build_osm.py --prov=NS,PE # one or more provinces only
"""

import json, math, os, sys, tempfile, time
import urllib.request, urllib.parse, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Raw Overpass responses are cached here so a re-run costs the API nothing.
# Delete this directory (or pass --refetch) to pull fresh data.
CACHE = os.environ.get("OSM_CACHE",
                       os.path.join(tempfile.gettempdir(), "livable_osm_cache"))
os.makedirs(CACHE, exist_ok=True)

RADIUS_KM = 15.0
DEDUPE_M = 100.0     # same-name collapse radius
DEDUPE_UNNAMED_M = 50.0  # unnamed-into-named collapse radius
TIE_KM = 1.0  # places this close share a catchment (see COORDINATE TWINS above)
UA = "livable-city-ranking/1.0 (one-off research build; rohamghiasicw@gmail.com)"

# Global-coverage mirrors ONLY. overpass.osm.ch was tried and removed: it is a
# Switzerland-only extract, so a Canadian area id resolves to nothing there and
# it answers 200 OK with zero elements. That is worse than an error - it would
# have cached a silent fake zero for a whole province. See sane() below, which
# now refuses any response that is empty or lands outside Canada.
# Rotated on every attempt, because the main instance answers
# "Dispatcher_Client::request_read_and_idx::timeout - server is probably too
# busy" under load. All four were probed with the same Canadian query
# (ice rinks in the Nova Scotia area); the two that answered returned an
# identical 64 elements at identical coordinates, which is the cross-check
# that they hold real global planet data and not a regional extract.
ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

# OSM admin_level=4 relation ids, confirmed live by querying
# rel["ISO3166-2"~"^CA-"][admin_level=4] before this script was written.
PROV_REL = {
    "NL": 391196, "PE": 391115, "NS": 390558, "NB": 68942, "QC": 61549,
    "ON": 68841, "MB": 390841, "SK": 391178, "AB": 391186, "BC": 390867,
    "YT": 391455, "NT": 391220, "NU": 390840,
}

# Overpass returns 504 on the full sixteen-line query for a province the size of
# Newfoundland: too much work for one request. The tag list is split into batches
# that each fit inside the endpoint's budget and the elements are merged. Batch 0
# is the original four lines, which completed for every province before this.
TAG_BATCHES = [
    ['nwr["leisure"="pitch"]["sport"~"(^|;)soccer(;|$)"](area.a);',
     'nwr["amenity"="place_of_worship"](area.a);',
     'nwr["leisure"="ice_rink"](area.a);',
     'nwr["leisure"~"^(pitch|sports_centre)$"]["sport"~"(^|;)ice_hockey(;|$)"](area.a);'],
    ['nwr["leisure"="dog_park"](area.a);',
     'nwr["amenity"="veterinary"](area.a);',
     'nwr["amenity"="arts_centre"](area.a);',
     'nwr["amenity"="studio"](area.a);',
     'nwr["tourism"="gallery"](area.a);',
     'nwr["tourism"="museum"](area.a);'],
    ['nwr["leisure"="hackerspace"](area.a);',
     'nwr["craft"](area.a);',
     'nwr["amenity"="marketplace"](area.a);',
     'nwr["shop"="farm"](area.a);',
     'nwr["shop"="greengrocer"](area.a);',
     'nwr["amenity"="library"](area.a);'],
    ['nwr["amenity"="college"](area.a);',
     'nwr["amenity"="university"](area.a);',
     'nwr["amenity"="hospital"](area.a);',
     'nwr["amenity"="clinic"](area.a);',
     'nwr["amenity"="community_centre"](area.a);',
     'nwr["amenity"="animal_shelter"](area.a);'],
    ['nwr["office"="ngo"](area.a);',
     'nwr["office"="charity"](area.a);'],
]


def query_for(area_id, batch):
    return ("[out:json][timeout:600];\narea(%d)->.a;\n(\n  " % area_id
            + "\n  ".join(TAG_BATCHES[batch]) + "\n);\nout center;")


# Rough Canada bounding box, used only to prove a mirror actually served us
# Canadian data rather than an empty answer from a regional extract.
CA_BOX = (41.0, -142.0, 84.0, -51.0)


def sane(prov, d, require_nonempty=True):
    """Refuse a response that cannot be a real answer for this province.

    Guards against a mirror that holds only a regional extract: it resolves the
    Canadian area id to nothing and returns 200 OK with zero elements, which
    would be cached as a fabricated zero for every place in the province.
    """
    els = d.get("elements")
    if els is None:
        return "no elements key"
    if len(els) == 0:
        return ("zero elements - no Canadian province has zero churches/pitches/rinks"
                if require_nonempty else None)
    inbox = 0
    for el in els:
        c = coord(el)
        if c and CA_BOX[0] <= c[0] <= CA_BOX[2] and CA_BOX[1] <= c[1] <= CA_BOX[3]:
            inbox += 1
    if inbox < 0.9 * len(els):
        return "only %d/%d elements inside Canada - wrong database?" % (inbox, len(els))
    return None


def fetch(prov, batch, force=False):
    """One Overpass call for one province and one tag batch. Cached, retried."""
    tag = "%s_b%d" % (prov, batch)
    need = (batch == 0)
    path = os.path.join(CACHE, "osm_%s.json" % tag)
    if os.path.exists(path) and not force:
        with open(path) as f:
            d = json.load(f)
        bad = sane(prov, d, need)
        if bad:
            print("  %s cached file REJECTED (%s), refetching" % (tag, bad))
        else:
            print("  %s cached: %d elements" % (tag, len(d["elements"])))
            return d
    q = query_for(3600000000 + PROV_REL[prov], batch)
    body = urllib.parse.urlencode({"data": q}).encode()
    delay = 30
    for attempt in range(10):
        ep = ENDPOINTS[attempt % len(ENDPOINTS)]
        try:
            t0 = time.time()
            req = urllib.request.Request(ep, data=body, headers={"User-Agent": UA})
            raw = urllib.request.urlopen(req, timeout=700).read()
            d = json.loads(raw)
            bad = sane(prov, d, need)
            if bad:
                raise ValueError("bad response from %s: %s" % (ep.split("/")[2], bad))
            print("  %s ok: %d elements in %.0fs (%s)"
                  % (tag, len(d["elements"]), time.time() - t0, ep.split("/")[2]))
            with open(path, "w") as f:
                json.dump(d, f)
            time.sleep(4)  # be polite between calls
            return d
        except Exception as e:
            code = getattr(e, "code", "")
            print("  %s attempt %d failed (%s %s), sleeping %ds"
                  % (tag, attempt + 1, code, str(e)[:120], delay))
            time.sleep(delay)
            delay = min(int(delay * 1.7), 300)
    raise RuntimeError("Overpass failed for %s after 10 attempts" % tag)


def coord(el):
    if "lat" in el and "lon" in el:
        return el["lat"], el["lon"]
    c = el.get("center")
    if c:
        return c["lat"], c["lon"]
    return None


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




# craft=* was pulled whole, but in North America the tag is overwhelmingly
# trades: measured across the Canadian pull it is electrician, builder, hvac,
# plumber, roofer, floorer, insulation. A plumber is not an arts scene, and
# counting one would put population-correlated noise into the single
# dimension that is meant not to be population. Keep the makers only.
CRAFT_ARTS = {"pottery", "atelier", "glassblower", "jeweller", "goldsmith",
              "bookbinder", "sculptor", "artist", "photographer", "printmaker",
              "engraver", "musical_instrument", "luthier", "weaver",
              "basket_maker", "restoration", "stonemason", "clockmaker"}


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

    # Doug's "alternative reasons" list, 2026-08-14. Each of these is a thing a
    # person actually moves for and none of them appear on a best-places list.
    am = t.get("amenity")
    if t.get("leisure") == "dog_park":
        out.add("dog_parks")
    if am == "veterinary":
        out.add("vets")
    # subculture: where a scene physically happens. craft=* is any workshop -
    # a bookbinder, a brewery, a luthier - which is the maker end of it.
    if (am in ("arts_centre", "studio") or t.get("tourism") in ("gallery", "museum")
            or t.get("leisure") == "hackerspace" or t.get("craft") in CRAFT_ARTS):
        out.add("arts_venues")
    if am == "marketplace" or t.get("shop") in ("farm", "greengrocer"):
        out.add("local_food")
    if am in ("library", "college", "university"):
        out.add("learning")
    if am in ("hospital", "clinic"):
        out.add("health_facilities")
    if am in ("community_centre", "animal_shelter") or t.get("office") in ("ngo", "charity"):
        out.add("volunteer_orgs")
    return out


FIELDS = ["soccer_pitches", "churches", "mosques", "synagogues", "temples_hindu",
          "gurdwaras", "temples_buddhist", "worship_total", "ice_rinks",
          "dog_parks", "vets", "arts_venues", "local_food", "learning",
          "health_facilities", "volunteer_orgs"]


def main():
    force = "--refetch" in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--prov="):
            only = a.split("=", 1)[1].split(",")

    places = json.load(open(os.path.join(ROOT, "data", "climate.json")))
    places = [{"name": p["name"], "prov": p["prov"], "lat": p["lat"], "lon": p["lon"]}
              for p in places]
    print("places: %d" % len(places))

    provs = only or list(PROV_REL)
    print("fetching %d provinces from Overpass" % len(provs))
    elements = []
    failed = []
    for pv in provs:
        for bi in range(len(TAG_BATCHES)):
            try:
                d = fetch(pv, bi, force=force)
            except Exception as e:
                print("  !! %s batch %d FAILED PERMANENTLY: %s" % (pv, bi, e))
                failed.append("%s_b%d" % (pv, bi))
                continue
            for el in d["elements"]:
                el["_src"] = pv
                elements.append(el)
    print("total raw elements fetched: %d" % len(elements))

    # one element can be returned by two province queries only if it straddles a
    # border; dedupe on (type, id) first.
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
        tagged.append((c[0], c[1], cats, (el.get("tags", {}).get("name") or "").strip().lower(),
                       el["type"], el["id"]))
    print("classified elements: %d  (dropped %d with no coordinate)" % (len(tagged), nocoord))

    # near-duplicate collapse: same category set membership + same name within 100 m
    tagged.sort(key=lambda r: (r[3], r[0], r[1]))
    keep = []
    dropped_dupe = 0
    by_name = {}
    for r in tagged:
        nm = r[3]
        if not nm:
            keep.append(r)
            continue
        dup = False
        for prev in by_name.get(nm, []):
            if prev[2] & r[2] and hav(prev[0], prev[1], r[0], r[1]) * 1000 <= DEDUPE_M:
                dup = True
                break
        if dup:
            dropped_dupe += 1
            continue
        by_name.setdefault(nm, []).append(r)
        keep.append(r)
    tagged = keep
    print("after same-name/100m dedupe: %d  (collapsed %d)" % (len(tagged), dropped_dupe))

    # pass 2: an unnamed element sitting on top of a named one, same category,
    # is the same building mapped twice. Drop the unnamed one.
    CELL = 0.01  # ~1.1 km lat; comfortably larger than the 50 m test radius
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
    tagged = keep2
    print("after unnamed-on-named/50m dedupe: %d  (collapsed %d)" % (len(tagged), dropped_un))

    # ---- assignment: nearest place, capped at RADIUS_KM -------------------
    counts = {(p["name"], p["prov"]): {f: 0 for f in FIELDS} for p in places}
    excl = {(p["name"], p["prov"]): {f: 0 for f in FIELDS} for p in places}
    plat = [p["lat"] for p in places]
    plon = [p["lon"] for p in places]
    pkey = [(p["name"], p["prov"]) for p in places]
    # tie-groups: places sharing the same point cannot be told apart, so they
    # share whatever their point wins (see COORDINATE TWINS in the docstring).
    parent = list(range(len(places)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(places)):
        for j in range(i + 1, len(places)):
            if abs(plat[i] - plat[j]) > 0.02 or abs(plon[i] - plon[j]) > 0.05:
                continue
            if hav(plat[i], plon[i], plat[j], plon[j]) <= TIE_KM:
                parent[find(i)] = find(j)
    group = {}
    for i in range(len(places)):
        group.setdefault(find(i), []).append(i)
    twins = [g for g in group.values() if len(g) > 1]
    print("coordinate tie-groups (shared catchment): %d groups, %d places"
          % (len(twins), sum(len(g) for g in twins)))
    for g in twins:
        print("    " + " == ".join("%s,%s" % pkey[i] for i in g))

    # crude lat/lon prefilter box: 15 km is at most 0.135 deg lat, and
    # 15/(111.32*cos(lat)) deg lon.
    dlat = RADIUS_KM / 110.574 + 1e-9
    assigned = 0
    unassigned = 0
    inradius = 0
    for la, lo, cats, nm, ty, oid in tagged:
        dlon = RADIUS_KM / (111.320 * max(math.cos(math.radians(la)), 1e-6)) + 1e-9
        best = None
        bestd = 1e18
        near = []
        for i in range(len(places)):
            if abs(plat[i] - la) > dlat:
                continue
            if abs(plon[i] - lo) > dlon:
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
    print("assigned to a nearest place: %d   beyond %.0f km of every place: %d   (exclusive fields)"
          % (assigned, RADIUS_KM, unassigned))

    out = []
    for p in places:
        k = (p["name"], p["prov"])
        dead = p["prov"] in failed
        rec = {"name": p["name"], "prov": p["prov"]}
        for f in FIELDS:
            rec[f] = None if dead else counts[k][f]
        rec["radius_km"] = RADIUS_KM
        rec["method"] = "count within radius_km great-circle of the place point; overlaps between neighbouring places are real, do not sum this column"
        for f in FIELDS:
            rec[f + "_exclusive"] = None if dead else excl[k][f]
        rec["method_exclusive"] = "same elements partitioned to the single nearest place within radius_km; this column does sum"
        out.append(rec)

    path = os.path.join(ROOT, "data", "osm.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=0)
    print("wrote %s (%d places)" % (path, len(out)))
    return out


if __name__ == "__main__":
    main()
