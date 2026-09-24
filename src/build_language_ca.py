"""build_language_ca.py - language spoken at home per Canadian CSD.

The US got this from ACS C16001, which publishes twelve coarse groups. Canada
publishes far more: Mandarin and Cantonese split apart, plus Punjabi, Urdu,
Hindi, Gujarati, Tamil, Portuguese, Russian and Persian each on their own. None
of those are separable in the US data, so the two countries deliberately offer
different lists rather than a forced common denominator.

Source: StatCan 98-401-X2021005, Census Profile 2021 at census subdivision
level. Same file extract_census.py already uses; this reads a different block.

Two traps, both from the source verification:
  - The file is cp1252, not UTF-8. Read it as UTF-8 and Montreal silently
    becomes "montral" while the script reports success.
  - For Farsi use characteristic 974, the "Persian languages" parent. The leaf
    976 is only the residual and reads implausibly low in Persian-heavy CSDs.

Writes data/language_ca.json keyed by name+prov.
"""
import csv, json, os, re, sys, unicodedata, zipfile

csv.field_size_limit(sys.maxsize)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get("WUB_SCRATCH", "/tmp")
ZIP = os.path.join(SCRATCH, "statcan_csd.zip")
INNER = "98-401-X2021005_English_CSV_data.csv"

# "Language spoken most often at home" block. The mother-tongue ids are these
# minus 342; home language is the better question for "will I hear it here".
TOTAL = "735"
LANGS = {
    "mandarin": "1028", "cantonese": "1032", "punjabi": "963", "spanish": "985",
    "arabic": "849", "tagalog": "879", "urdu": "967", "hindi": "954",
    "gujarati": "953", "tamil": "893", "portuguese": "983", "russian": "912",
    "italian": "982", "german": "931", "korean": "989", "vietnamese": "861",
    "polish": "911", "ukrainian": "921", "greek": "948", "persian": "974",
}
WANT = set(LANGS.values()) | {TOTAL}
PROV = {"10": "NL", "11": "PE", "12": "NS", "13": "NB", "24": "QC", "35": "ON",
        "46": "MB", "47": "SK", "48": "AB", "59": "BC", "60": "YT", "61": "NT",
        "62": "NU"}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\s*\(.*?\)\s*", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    if not os.path.exists(ZIP):
        raise SystemExit("missing %s - download GEONO=005 first" % ZIP)
    raw = {}
    with zipfile.ZipFile(ZIP) as z:
        name = next(n for n in z.namelist() if n.endswith(".csv") and "data" in n.lower())
        print("reading", name)
        with z.open(name) as fh:
            r = csv.reader(l.decode("cp1252", "replace") for l in fh)
            next(r)
            for row in r:
                if row[8] not in WANT:
                    continue
                if "subdivision" not in row[3].lower():
                    continue
                prov = PROV.get(str(row[2])[:2])
                if not prov:
                    continue
                try:
                    val = float(row[11])
                except (ValueError, IndexError):
                    continue
                # key on the 7-digit CSD code, never the name: the census writes
                # "Trepassey, Town (T)" and the app writes "Trepassey", and a
                # name match across 5,161 CSDs is a guess wearing a join.
                raw.setdefault(str(row[2]), {})[row[8]] = val
    print("CSDs with any language row: %d" % len(raw))

    # census.json already maps every CSD code to the name the app uses.
    code2place = {r["code"]: (r["name"], r["prov"])
                  for r in json.load(open(os.path.join(ROOT, "data", "census.json")))}
    out = []
    for code, vals in raw.items():
        tot = vals.get(TOTAL)
        if not tot or code not in code2place:
            continue
        nm, prov = code2place[code]
        out.append({"name": nm, "prov": prov, "code": code,
                    "lang": {k: round(vals[i] / tot * 100, 1)
                             for k, i in LANGS.items() if vals.get(i) is not None}})

    dest = os.path.join(ROOT, "data", "language_ca.json")
    with open(dest, "w") as f:
        json.dump(out, f)
    print("wrote %s (%d CSDs)" % (dest, len(out)))

    # join report against the app's own list, rather than assuming it
    places = json.load(open(os.path.join(ROOT, "data", "climate.json")))
    have = {(r["name"], r["prov"]) for r in out}
    hit = sum(1 for p in places if (p["name"], p["prov"]) in have)
    print("joins %d/%d of the app's places (%.1f%%)" % (hit, len(places), 100 * hit / len(places)))
    by = {(r["name"], r["prov"]): r for r in out}
    for nm, pv, lg in [("Surrey", "BC", "punjabi"), ("Richmond", "BC", "cantonese"),
                       ("Markham", "ON", "mandarin"), ("Laval", "QC", "arabic")]:
        r = by.get((nm, pv))
        if r:
            print("   %-10s %s  %-10s %4.1f%%" % (nm, pv, lg, r["lang"].get(lg, 0)))


if __name__ == "__main__":
    main()
