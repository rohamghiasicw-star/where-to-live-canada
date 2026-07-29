#!/usr/bin/env python3
"""
US wildfire smoke -> data/us/smoke_grid.json

Source: Childs et al. (2022), "Daily local-level estimates of ambient wildfire
smoke PM2.5 for the contiguous US", Environ. Sci. Technol. 56(19) 13607-13621,
doi:10.1021/acs.est.2c02934. Data: Harvard Dataverse doi:10.7910/DVN/DJVMTV
(CC BY-SA 4.0), version 1.0, published 2024-02-26.

This is the US analogue of ECCC FireWork Cumulative Effects, which is what the
Canadian side of the app uses. It is FIRE-ATTRIBUTED smoke PM2.5 in ug/m3, not
total PM2.5. Total PM2.5 (EPA AQS, AirNow, NAPS) is the trap: monitors measure
total mass and cannot separate fire smoke from traffic, industry and wood stoves,
so a total-PM2.5 surface ranks Los Angeles and the Ohio Valley smoky and Idaho
clean. See research/us/smoke-sources.md.

How Childs et al. isolate the smoke, verbatim from the paper (Figure 1a):
  "Non-smoke median PM2.5 ... is the station- and month-specific median of PM2.5
   on non-smoke days, and smoke PM2.5 ... is total PM2.5 above the non-smoke
   median on days with smoke overhead."
Smoke days come from NOAA HMS smoke plume polygons plus HYSPLIT trajectories.
A gradient-boosted model then predicts that anomaly everywhere on a 10 km grid.

What this script produces: a MULTI-YEAR MEAN ANNUAL surface, 2006-2020 (15 full
years, 5479 days). Mean = (sum of daily smoke PM2.5 over all 5479 days) / 5479,
so it is an annual-average concentration in ug/m3, the same construct as
FireWork CE's "yearly average of wildfire contribution: surface PM2.5", and one
extreme fire year (2020 in the US, 2023 in Canada) counts once, not once over.

Coverage: contiguous US only. The source dataset does not exist for Alaska,
Hawaii or Puerto Rico, so those are emitted as null. Alaska genuinely burns; a
null is honest and a zero would be a lie.

Requires: numpy, pandas. No GDAL/rasterio/geopandas - the shapefile is parsed
with struct. Downloads ~1.8 GB on first run into WORK (resumable via curl -C -).

Run:  python3 src/us/build_smoke.py
"""

import json, os, struct, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT  = os.path.join(ROOT, "data", "us", "smoke_grid.json")
WORK = os.environ.get("SMOKE_WORK", "/tmp/smoke_us")

DOI    = "doi:10.7910/DVN/DJVMTV"
ACCESS = "https://dataverse.harvard.edu/api/access/datafile/%d"
FILES  = {                      # Dataverse datafile id -> local name, bytes
    "grid.shp":   (8550317,   13621316),
    "grid.shx":   (8550318,     801348),
    "grid.dbf":   (8550315,    5809178),
    "grid.prj":   (8550314,        145),
    "README.txt": (8550346,      10743),
    "smokePM_10km_20060101-20201231.csv": (8550337, 1778985211),
}

Y0, Y1  = 2006, 2020
NDAYS   = 5479                  # 2006-01-01..2020-12-31 inclusive, 4 leap years
MAX_ID  = 221556                # 10 km raster index space (grid IDs run to 221555)

# Output grid. 0.1 deg ~ 11.1 km N-S and 8.5-10.3 km E-W across CONUS, i.e. the
# same order as the 10 km source, so resampling neither invents nor loses detail.
# The box deliberately spans Alaska, Hawaii and Puerto Rico even though all three
# are null, so that a nearest-neighbour sample for Anchorage, Honolulu or San Juan
# lands on a null cell instead of being clamped to the nearest CONUS value.
LAT0, LON0, DLAT, DLON = 18.0, -180.0, 0.1, 0.1
NLAT, NLON = 541, 1161          # 18.0..72.0 N, -180.0..-64.0 E

R_EARTH  = 6371.0088            # km
MAX_KM   = 7.1                  # half-diagonal of a 10 km cell = 7.07 km.
                                # A target cell whose nearest source centroid is
                                # farther than this is outside the source domain
                                # -> null. This is a resample, never an
                                # extrapolation beyond ~2 km of the real edge.
DECIMALS = 3


def fetch():
    os.makedirs(WORK, exist_ok=True)
    for name, (fid, size) in FILES.items():
        p = os.path.join(WORK, name)
        if os.path.exists(p) and os.path.getsize(p) == size:
            continue
        print("downloading %s (%.1f MB)" % (name, size / 1e6), flush=True)
        subprocess.run(["curl", "-sS", "-L", "-C", "-", "--retry", "8",
                        "--retry-delay", "5", "--retry-all-errors",
                        ACCESS % fid, "-o", p], check=True)
        got = os.path.getsize(p)
        if got != size:
            sys.exit("%s: got %d bytes, expected %d" % (name, got, size))
    return {k: os.path.join(WORK, k) for k in FILES}


def read_grid(shp, dbf):
    """10 km grid cell IDs and WGS84 centroids. Cells are 10 km squares in the
    source projection, so in lat/lon they are slightly rotated quadrilaterals;
    the mean of the four corners is the centroid."""
    f = open(shp, "rb")
    hdr = f.read(100)
    assert struct.unpack(">i", hdr[0:4])[0] == 9994, "not a shapefile"
    assert struct.unpack("<i", hdr[32:36])[0] == 5, "not polygons"
    lon, lat = [], []
    while True:
        rh = f.read(8)
        if len(rh) < 8:
            break
        _rn, clen = struct.unpack(">ii", rh)
        c = f.read(clen * 2)
        nparts, npts = struct.unpack("<ii", c[36:44])
        pts = np.frombuffer(c, dtype="<f8", count=2 * npts,
                            offset=44 + 4 * nparts).reshape(npts, 2)
        q = pts[:-1]                      # drop the repeated closing vertex
        lon.append(q[:, 0].mean()); lat.append(q[:, 1].mean())
    f.close()

    g = open(dbf, "rb"); h = g.read(32)
    nrec = struct.unpack("<i", h[4:8])[0]
    hlen = struct.unpack("<h", h[8:10])[0]
    rlen = struct.unpack("<h", h[10:12])[0]
    g.seek(hlen); buf = g.read(nrec * rlen); g.close()
    ids = np.array([int(buf[i * rlen + 1:i * rlen + 10]) for i in range(nrec)],
                   dtype=np.int64)
    assert len(ids) == len(lon), "shp/dbf record count mismatch"
    return ids, np.array(lon), np.array(lat)


def aggregate(csv):
    """Sum daily smoke PM2.5 per grid cell over 2006-2020.

    The CSV holds SMOKE DAYS ONLY. README.txt, verbatim: "Predictions on
    non-smoke days are by construction 0 ug/m^3 and not included in this file."
    So the missing cell-days contribute exactly zero to the sum, and the
    denominator is the full 5479 days.
    """
    import pandas as pd
    tot = np.zeros(MAX_ID, dtype=np.float64)
    per_year = {y: np.zeros(MAX_ID, dtype=np.float64) for y in range(Y0, Y1 + 1)}
    nrows = 0
    for ch in pd.read_csv(csv, usecols=["grid_id_10km", "date", "smokePM_pred"],
                          dtype={"grid_id_10km": "int32", "date": "int32",
                                 "smokePM_pred": "float32"},
                          chunksize=8_000_000):
        gid = ch["grid_id_10km"].to_numpy()
        val = ch["smokePM_pred"].to_numpy().astype(np.float64)
        yr  = ch["date"].to_numpy() // 10000
        tot += np.bincount(gid, weights=val, minlength=MAX_ID)[:MAX_ID]
        for y in np.unique(yr):
            m = yr == y
            per_year[int(y)] += np.bincount(gid[m], weights=val[m],
                                            minlength=MAX_ID)[:MAX_ID]
        nrows += len(gid)
        print("  %d rows" % nrows, flush=True)
    return tot, per_year, nrows


def unit_xyz(lon, lat):
    la = np.radians(lat); lo = np.radians(lon)
    c = np.cos(la)
    return np.stack([c * np.cos(lo), c * np.sin(lo), np.sin(la)], axis=-1)


def resample(src_lon, src_lat, src_val):
    """Nearest source cell centroid per output cell, null beyond MAX_KM.

    Pure numpy: source centroids are bucketed on a 0.25 deg hash, and each
    output cell only searches its own bucket plus the eight around it. At this
    latitude range a 0.25 deg bucket is >=20 km, so a 3x3 neighbourhood always
    contains anything within 7.1 km.
    """
    B = 0.25
    key_of = lambda lo, la: (np.floor(la / B).astype(np.int64) * 100000 +
                             np.floor(lo / B).astype(np.int64))
    keys = key_of(src_lon, src_lat)
    order = np.argsort(keys, kind="stable")
    keys_s = keys[order]
    uniq, start = np.unique(keys_s, return_index=True)
    end = np.append(start[1:], len(keys_s))
    bucket = {int(k): (int(s), int(e)) for k, s, e in zip(uniq, start, end)}
    src_xyz = unit_xyz(src_lon, src_lat)[order]
    src_v   = src_val[order]

    chord = 2.0 * R_EARTH * np.sin(MAX_KM / (2.0 * R_EARTH))   # km -> chord
    lim2 = chord ** 2

    lats = LAT0 + DLAT * np.arange(NLAT)
    lons = LON0 + DLON * np.arange(NLON)
    out = np.full((NLAT, NLON), np.nan)

    # only rows/cols that can possibly touch the source domain
    r_lo = max(0, int(np.floor((src_lat.min() - 0.2 - LAT0) / DLAT)))
    r_hi = min(NLAT, int(np.ceil((src_lat.max() + 0.2 - LAT0) / DLAT)) + 1)
    c_lo = max(0, int(np.floor((src_lon.min() - 0.2 - LON0) / DLON)))
    c_hi = min(NLON, int(np.ceil((src_lon.max() + 0.2 - LON0) / DLON)) + 1)

    for i in range(r_lo, r_hi):
        la = lats[i]
        row_lons = lons[c_lo:c_hi]
        txyz = unit_xyz(row_lons, np.full(len(row_lons), la))
        ib = int(np.floor(la / B))
        for k, lo in enumerate(row_lons):
            jb = int(np.floor(lo / B))
            best2 = lim2; bestv = np.nan
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    b = bucket.get((ib + di) * 100000 + (jb + dj))
                    if b is None:
                        continue
                    s, e = b
                    d = src_xyz[s:e] - txyz[k]
                    d2 = np.einsum("ij,ij->i", d, d)
                    m = int(np.argmin(d2))
                    if d2[m] < best2:
                        best2 = float(d2[m]); bestv = float(src_v[s + m])
            out[i, c_lo + k] = bestv
    return out


def pct(a, q):
    return float(np.percentile(a, q))


def main():
    f = fetch()
    print("reading 10 km grid ...", flush=True)
    ids, glon, glat = read_grid(f["grid.shp"], f["grid.dbf"])
    print("  %d cells, lon %.3f..%.3f lat %.3f..%.3f"
          % (len(ids), glon.min(), glon.max(), glat.min(), glat.max()))

    print("aggregating daily smoke days %d-%d ..." % (Y0, Y1), flush=True)
    tot, per_year, nrows = aggregate(f["smokePM_10km_20060101-20201231.csv"])

    unseen = int((tot[ids] == 0).sum())
    mean = tot[ids] / NDAYS
    print("  %d rows, %d/%d grid cells never appear (0 smoke-day rows -> 0.0)"
          % (nrows, unseen, len(ids)))
    orphan = tot.sum() - tot[ids].sum()
    print("  smoke mass on grid ids absent from the shapefile: %.6g of %.6g"
          % (orphan, tot.sum()))
    print("  national annual mean by year (mean over cells, ug/m3):")
    for y in range(Y0, Y1 + 1):
        d = 366 if y % 4 == 0 else 365
        print("    %d %.3f" % (y, (per_year[y][ids] / d).mean()))

    print("resampling to %.2f deg lat/lon ..." % DLAT, flush=True)
    grid = resample(glon, glat, mean)
    n_ok = int(np.isfinite(grid).sum())
    print("  %d/%d output cells with data (%.1f%%)"
          % (n_ok, NLAT * NLON, 100.0 * n_ok / (NLAT * NLON)))

    vals = [[None if not np.isfinite(v) else round(float(v), DECIMALS)
             for v in row] for row in grid]
    doc = {
        "units": "ug/m3",
        "years": "%d-%d" % (Y0, Y1),
        "source": ("Childs et al. 2022, daily 10 km wildfire smoke PM2.5 for the "
                   "contiguous US (Environ. Sci. Technol. 56:13607, "
                   "doi:10.1021/acs.est.2c02934); data Harvard Dataverse "
                   "doi:10.7910/DVN/DJVMTV v1.0, CC BY-SA 4.0"),
        "note": ("Fire-attributed smoke PM2.5 only, NOT total PM2.5. Daily "
                 "smoke PM2.5 is total PM2.5 above each monitor's station- and "
                 "month-specific non-smoke median on days with a NOAA HMS smoke "
                 "plume overhead, modelled onto a 10 km grid. Value is the "
                 "%d-%d mean annual concentration: sum of daily smoke PM2.5 over "
                 "all %d days divided by %d, so one extreme fire year counts "
                 "once. Directly comparable to the Canadian ECCC FireWork "
                 "Cumulative Effects values in data/smoke.json. "
                 "values[i][j] is at lat = lat0 + i*dlat, lon = lon0 + j*dlon; "
                 "row 0 is the southernmost. null = no data. The source is "
                 "contiguous-US only, so ALASKA, HAWAII AND PUERTO RICO ARE "
                 "null, not zero, and so is everything outside the CONUS "
                 "land/coastal domain. Do not fill them; Alaska burns and a zero "
                 "there would be wrong. The grid box spans AK, HI and PR on "
                 "purpose so a nearest-neighbour lookup there returns null "
                 "instead of being clamped to a CONUS value. Modelled, not "
                 "measured: spatial out-of-sample R2 = 0.67."
                 % (Y0, Y1, NDAYS, NDAYS)),
        "lat0": LAT0, "lon0": LON0, "dlat": DLAT, "dlon": DLON,
        "nlat": NLAT, "nlon": NLON,
        "values": vals,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(doc, fh, separators=(",", ":"))
    print("wrote %s  %.2f MB" % (OUT, os.path.getsize(OUT) / 1e6))

    # ---------------- validation ----------------
    def sample(lat, lon):
        i = int(round((lat - LAT0) / DLAT)); j = int(round((lon - LON0) / DLON))
        if not (0 <= i < NLAT and 0 <= j < NLON):
            return None
        v = grid[i, j]
        return None if not np.isfinite(v) else float(v)

    print("\n--- validation: reported cities ---")
    cities = [("Chico CA", 39.7285, -121.8375), ("Medford OR", 42.3265, -122.8756),
              ("Boise ID", 43.6150, -116.2023), ("Missoula MT", 46.8721, -113.9940),
              ("Spokane WA", 47.6588, -117.4260), ("Denver CO", 39.7392, -104.9903),
              ("Phoenix AZ", 33.4484, -112.0740), ("Chicago IL", 41.8781, -87.6298),
              ("Miami FL", 25.7617, -80.1918), ("Portland ME", 43.6591, -70.2568)]
    for n, la, lo in cities:
        v = sample(la, lo)
        print("  %-12s %s" % (n, "null" if v is None else "%.3f" % v))

    print("\n--- validation: regional means (should be West high, East low) ---")
    regions = [("N California", 38.5, 42.0, -124.4, -120.0),
               ("Oregon",       42.0, 46.2, -124.6, -117.0),
               ("Idaho",        42.0, 49.0, -117.2, -111.0),
               ("Montana W",    44.4, 49.0, -116.1, -111.5),
               ("Washington E", 45.6, 49.0, -120.9, -117.0),
               ("Florida",      25.0, 31.0,  -87.6,  -80.0),
               ("Maine coast",  43.0, 45.2,  -70.9,  -67.0),
               ("Michigan UP",  45.8, 47.5,  -90.4,  -84.0)]
    rows = []
    for n, a, b, c, d in regions:
        i0 = int(round((a - LAT0) / DLAT)); i1 = int(round((b - LAT0) / DLAT))
        j0 = int(round((c - LON0) / DLON)); j1 = int(round((d - LON0) / DLON))
        w = grid[i0:i1 + 1, j0:j1 + 1]
        w = w[np.isfinite(w)]
        rows.append((n, float(w.mean()), int(w.size)))
    for n, m, k in sorted(rows, key=lambda t: -t[1]):
        print("  %-13s %.3f   (%d cells)" % (n, m, k))

    print("\n--- validation: national distribution (CONUS cells) ---")
    a = grid[np.isfinite(grid)]
    print("  n=%d  min %.3f  p10 %.3f  p50 %.3f  mean %.3f  p90 %.3f  max %.3f"
          % (a.size, a.min(), pct(a, 10), pct(a, 50), a.mean(), pct(a, 90), a.max()))
    print("  Canada FireWork CE span for comparison: 0.04 (Iqaluit) - 2.82 (Kamloops)")

    print("\n--- validation: AK / HI must be null ---")
    for n, la, lo in [("Anchorage AK", 61.2181, -149.9003),
                      ("Fairbanks AK", 64.8378, -147.7164),
                      ("Honolulu HI", 21.3069, -157.8583)]:
        print("  %-13s %s" % (n, "null (no source coverage)"
                              if sample(la, lo) is None else "*** LEAK ***"))

    pl = os.path.join(ROOT, "data", "us", "places.json")
    if os.path.exists(pl):
        places = json.load(open(pl))
        miss = [p for p in places if sample(p["lat"], p["lon"]) is None]
        states = sorted({p["state"] for p in miss})
        print("\n--- validation: data/us/places.json coverage ---")
        print("  %d/%d places resolve; %d null, states: %s"
              % (len(places) - len(miss), len(places), len(miss), ",".join(states)))
        bad = [p for p in miss if p["state"] not in ("AK", "HI", "PR")]
        for p in bad[:20]:
            print("    unexpected null: %s, %s (%.4f, %.4f)"
                  % (p["name"], p["state"], p["lat"], p["lon"]))
        hi_ak = [p for p in places if p["state"] in ("AK", "HI", "PR")
                 and sample(p["lat"], p["lon"]) is not None]
        print("  AK/HI/PR places with a non-null value (must be 0): %d" % len(hi_ak))

        by_state = {}
        for p in places:
            v = sample(p["lat"], p["lon"])
            if v is not None:
                by_state.setdefault(p["state"], []).append(v)
        rank = sorted(((s, float(np.mean(v)), len(v)) for s, v in by_state.items()
                       if len(v) >= 5), key=lambda t: -t[1])
        print("\n--- validation: state means at real places (>=5 places) ---")
        print("  smokiest 10:")
        for s, m, k in rank[:10]:
            print("    %-4s %.3f  (n=%d)" % (s, m, k))
        print("  cleanest 10:")
        for s, m, k in rank[-10:]:
            print("    %-4s %.3f  (n=%d)" % (s, m, k))
        top = sorted(((sample(p["lat"], p["lon"]) or -1, p) for p in places),
                     key=lambda t: -t[0])[:12]
        print("  smokiest 12 individual places:")
        for v, p in top:
            print("    %-22s %-3s %.3f" % (p["name"][:22], p["state"], v))

    i, j = np.unravel_index(np.nanargmax(grid), grid.shape)
    print("\n--- validation: grid maximum ---")
    print("  %.3f ug/m3 at lat %.2f lon %.2f" % (grid[i, j], LAT0 + i * DLAT,
                                                 LON0 + j * DLON))


if __name__ == "__main__":
    main()
