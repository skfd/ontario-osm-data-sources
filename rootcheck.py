#!/usr/bin/env python
"""List what Hub sweeps cannot see: services on an ArcGIS Online org root that no Hub catalogues.

    python rootcheck.py                 # address words (the default theme)
    python rootcheck.py --words "hydrant|valve"

Finds every services*.arcgis.com/<org>/arcgis/rest/services root that rows in
catalogue/layers/ point at but portals.csv does not sweep as an arcgis-rest portal,
lists each root and its folders, keeps service names matching --words, and drops the
ones the catalogue (or ../ontario-address-changes, when it is next door) already has.
Reports only; adds no rows. See FOLLOW-UPS.md, "Hub portals are swept through their
catalogue only".
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
TRACKER = os.path.join(os.path.dirname(HERE), "ontario-address-changes", "datasets")
UA = {"User-Agent": "ontario-osm-data-sources rootcheck"}
ROOT = re.compile(r"(https://services\d*\.arcgis\.com/[A-Za-z0-9]+/arcgis/rest/services)", re.I)
SVC = re.compile(r"/rest/services/(.+?)/(featureserver|mapserver)", re.I)


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def unswept_roots():
    with open(os.path.join(HERE, "catalogue", "portals.csv"), encoding="utf-8") as fh:
        swept = {p["api_url"].rstrip("/").lower() for p in csv.DictReader(fh) if p["platform"] == "arcgis-rest"}
    roots, known = defaultdict(set), set()
    for f in glob.glob(os.path.join(HERE, "catalogue", "layers", "*.csv")):
        with open(f, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                url = r.get("source_url") or ""
                m = ROOT.search(url)
                if m:
                    roots[m.group(1)].add(os.path.basename(f)[:-4])
                s = SVC.search(url)
                if s:
                    known.add(s.group(1).lower())
    for f in glob.glob(os.path.join(TRACKER, "*.toml")):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if line.lstrip().startswith("data_url"):
                    s = SVC.search(line)
                    if s:
                        known.add(s.group(1).lower())
    return {r: sorted(j) for r, j in roots.items() if r.lower() not in swept}, known


def services(root):
    top = get(root + "?f=json")
    names = {s["name"] for s in top.get("services", [])}
    for folder in top.get("folders", []):
        try:
            names |= {s["name"] for s in get(f"{root}/{urllib.parse.quote(folder)}?f=json").get("services", [])}
        except Exception:  # noqa: BLE001 - a secured folder is simply skipped
            pass
    return sorted(names)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--words", default=r"addr|civic|911|siteadd|site_add|address",
                    help="regex matched against service names (default: address words)")
    args = ap.parse_args()
    words = re.compile(args.words, re.I)
    roots, known = unswept_roots()

    def probe(root):
        try:
            return root, services(root), None
        except Exception as exc:  # noqa: BLE001
            return root, [], str(exc)[:60]

    total = 0
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(probe, roots))
    for root, names, err in sorted(results, key=lambda r: r[0]):
        total += len(names)
        new = [n for n in names if words.search(n) and n.lower() not in known]
        if err:
            print(f"{','.join(roots[root])[:40]:40} ERR {err}")
        elif new:
            print(f"{','.join(roots[root])[:40]:40} {len(names):>5}  {root}\n    " + "\n    ".join(new))
    print(f"\n{len(roots)} unswept org roots, {total} services listed")


if __name__ == "__main__":
    main()
