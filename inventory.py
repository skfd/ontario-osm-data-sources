"""List every dataset and layer the open-data portals publish, so each can be graded once.

Reads   catalogue/portals.csv, catalogue/sources.csv, catalogue/jurisdictions.csv
Writes  cache/inventory/<code>.csv       one row per dataset or layer, with its metadata
        cache/inventory/chunks/<n>.csv   the same rows in grading batches of at most CHUNK
        cache/inventory/chunks.json      the batches, for the grading agents
        catalogue/layers/<code>.csv      --merge: graded rows added, existing rows left alone

    python inventory.py [jurisdiction ...]   list the portals (network)
    python inventory.py --chunk              cut the batches again, no network
    python inventory.py --check <chunk>      validate cache/graded/<chunk>.csv
    python inventory.py --merge              graded batches -> catalogue/layers/

Portals swept: every reach 2 to 4 row with an api_url, minus shared-portal rows (their layers
are listed under the owner) and the provincial catalogues. The goal is that no layer goes
unlisted; a grade can be argued later, a missing row cannot. A Hub item that names a whole service
becomes one row per layer. A server layer a Hub of the same jurisdiction already lists is
dropped, and so is any URL already in sources.csv. Ids are assigned here, in URL order, so the
graders never invent one.
"""

import csv
import html
import json
import re
import sys
import threading
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone

from common import (FEASIBILITY, HERE, JURISDICTIONS, LAYERS, PORTALS, SOURCE_COLS, SOURCES,
                    THEMES, read_csv, write_csv)
import survey
from survey import Secured, ServiceError, get_json, with_param

# Hundreds of servers, few requests each: more in flight than survey.py's count needs.
survey.SLOTS = threading.Semaphore(24)

CACHE = HERE / "cache" / "inventory"
GRADED = HERE / "cache" / "graded"
CHUNK = 120
SKIP = {"ca/on"}  # the provincial catalogues are not a municipality's
COLS = ["id", "jurisdiction", "portal_url", "origin", "dataset", "item_type", "source_url",
        "geometry", "records", "fields", "edited", "licence", "description"]
GRADE_COLS = ["id", "theme", "provider", "tier", "feasibility", "status", "notes"]
BORING_FIELDS = re.compile(r"^(objectid|fid|shape|shape_.*|shape__.*|globalid|st_area.*|"
                           r"st_length.*|created_.*|last_edited_.*)$", re.I)


def text(s, limit: int) -> str:
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = " ".join(s.split()).replace("|", "/")  # a pipe separates tools in the catalogue
    return s if len(s) <= limit else s[:limit - 1].rstrip() + "…"


def slug(s: str) -> str:
    s = re.sub(r"[’'`]", "", s.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60].strip("-") or "layer"


def key(url: str) -> str:
    """One spelling per layer: MapServer and FeatureServer of the same service are one layer."""
    u = url.strip().rstrip("/").lower().split("?", 1)[0]
    return u.replace("/featureserver", "/mapserver").replace("http://", "https://")


def licence(item_text: str, portal: str) -> str:
    """The item's own licence when it names one; many Hubs put a disclaimer in that field."""
    if re.search(r"licen[cs]e|OGL|creative commons|public domain", item_text, re.I):
        return item_text
    return portal


def day(ms) -> str:
    try:
        return datetime.fromtimestamp(ms / 1000, timezone.utc).date().isoformat() if ms else ""
    except (TypeError, ValueError, OSError):
        return ""


# ---------------------------------------------------------------- ArcGIS services

SERVICE = re.compile(r"^(.*/(?:FeatureServer|MapServer))(?:/(\d+))?/?$", re.I)
_services: dict[str, list[dict]] = {}


def service_layers(service: str) -> list[dict]:
    """The layers and tables of one service, with fields, from its /layers resource."""
    if service not in _services:
        try:
            d = get_json(f"{service}/layers?f=json")
            _services[service] = (d.get("layers") or []) + (d.get("tables") or [])
        except (Secured, ServiceError, OSError, ValueError):
            _services[service] = []
    return _services[service]


def count(layer_url: str) -> str:
    try:
        d = get_json(f"{layer_url}/query?where=1%3D1&returnCountOnly=true&f=json")
        return str(d.get("count", ""))
    except (Secured, ServiceError, OSError, ValueError, KeyError):
        return ""


def layer_row(service: str, layer: dict) -> dict:
    fields = [f["name"] for f in layer.get("fields") or [] if not BORING_FIELDS.match(f["name"])]
    geometry = (layer.get("geometryType") or "").replace("esriGeometry", "").lower()
    return {
        "source_url": f"{service}/{layer['id']}",
        "item_type": layer.get("type", ""),
        "geometry": geometry or ("table" if layer.get("type") == "Table" else ""),
        "fields": text(" ".join(fields), 300),
        "edited": day((layer.get("editingInfo") or {}).get("lastEditDate")),
        "layer_name": layer.get("name", ""),
        "layer_description": text(layer.get("description"), 300),
    }


def expand(url: str) -> list[dict]:
    """A service or layer URL as one entry per (non-group) layer it names."""
    m = SERVICE.match(url or "")
    if not m:
        return []
    service, index = m.group(1), m.group(2)
    layers = [l for l in service_layers(service) if not l.get("subLayerIds")]
    if index is not None:
        layers = [l for l in layers if str(l.get("id")) == index] or [{"id": int(index)}]
    return [layer_row(service, l) for l in layers]


# ---------------------------------------------------------------- platforms

def hub_items(api_url: str) -> list[dict]:
    items, start = [], 1
    while True:
        d = get_json(with_param(api_url, f"limit=100&startindex={start}"))
        feats = d.get("features") or []
        items += [f["properties"] for f in feats]
        start += len(feats)
        if not feats or start > int(d.get("numberMatched") or 0):
            return items


def sharing_items(api_url: str) -> list[dict]:
    items, start = [], 1
    while start > 0:
        d = get_json(with_param(api_url, f"num=100&start={start}&f=json"))
        items += d.get("results") or []
        start = int(d.get("nextStart") or -1)
    return items


def from_hub(p: dict) -> list[dict]:
    url = p["api_url"]
    items = sharing_items(url) if "/sharing/rest/search" in url else hub_items(url)
    rows = []
    for it in items:
        base = {
            "origin": "hub",
            "dataset": text(it.get("title"), 200),
            "item_type": it.get("type", ""),
            "source_url": it.get("url") or "",
            "edited": day(it.get("modified")),
            "licence": licence(text(it.get("licenseInfo"), 150), p["licence"]),
            "description": text(it.get("snippet") or it.get("description"), 300),
        }
        layers = expand(base["source_url"])
        if not layers:
            if not base["source_url"] and it.get("id"):
                base["source_url"] = f"{p['portal_url'].rstrip('/')}/datasets/{it['id']}"
            rows.append(base)
            continue
        for l in layers:
            name = base["dataset"]
            if len(layers) > 1 and l["layer_name"]:
                name = f"{name} — {l['layer_name']}"
            rows.append(base | {k: v for k, v in l.items() if k in COLS and v}
                        | {"dataset": name, "edited": l["edited"] or base["edited"]})
    return rows


def from_ckan(p: dict) -> list[dict]:
    rows, start = [], 0
    while True:
        d = get_json(with_param(p["api_url"], f"rows=500&start={start}"))["result"]
        for pk in d["results"]:
            formats = sorted({(r.get("format") or "").upper() for r in pk.get("resources") or []} - {""})
            site = p["portal_url"].rstrip("/")
            rows.append({
                "origin": "ckan",
                "dataset": text(pk.get("title") or pk.get("name"), 200),
                "item_type": "CKAN package: " + ", ".join(formats),
                "source_url": f"{site}/dataset/{pk['name']}",
                "edited": (pk.get("metadata_modified") or "")[:10],
                "licence": licence(text(pk.get("license_title"), 150), p["licence"]),
                "description": text(pk.get("notes"), 300),
            })
        start += len(d["results"])
        if not d["results"] or start >= d["count"]:
            return rows


def from_rest(p: dict) -> list[dict]:
    root = p["api_url"].rstrip("/")
    top = get_json(with_param(root, "f=json"))
    services = list(top.get("services", []))
    for folder in top.get("folders", []):
        try:
            services += get_json(f"{root}/{urllib.parse.quote(folder)}?f=json").get("services", [])
        except (Secured, ServiceError, OSError, ValueError):
            pass
    kinds: dict[str, set] = {}
    for s in services:
        kinds.setdefault(s["name"], set()).add(s["type"])
    rows = []
    for name in sorted(kinds):
        kind = next((t for t in ("FeatureServer", "MapServer") if t in kinds[name]), None)
        if kind is None:
            if "ImageServer" in kinds[name]:
                rows.append({"origin": "rest", "dataset": name.split("/")[-1].replace("_", " "),
                             "item_type": "ImageServer", "geometry": "raster",
                             "source_url": f"{root}/{urllib.parse.quote(name)}/ImageServer",
                             "licence": p["licence"]})
            continue
        service = f"{root}/{urllib.parse.quote(name)}/{kind}"
        for l in expand(service):
            rows.append({"origin": "rest", "licence": p["licence"],
                         "dataset": f"{name.split('/')[-1].replace('_', ' ')} — {l['layer_name']}",
                         "description": l["layer_description"]}
                        | {k: v for k, v in l.items() if k in COLS})
    return rows


PLATFORM = {"arcgis-hub": from_hub, "ckan": from_ckan, "arcgis-rest": from_rest}


# ---------------------------------------------------------------- inventory

def swept(p: dict) -> bool:
    return (p["reach"] in ("2", "3", "4") and p["api_url"] and p["platform"] in PLATFORM
            and p["jurisdiction"] not in SKIP and "shared portal of" not in p["notes"])


def inventory(only: set[str]):
    portals = [p for p in read_csv(PORTALS) if swept(p) and (not only or p["jurisdiction"] in only)]
    known = {key(r["source_url"]) for r in read_csv(SOURCES) if r["source_url"]}
    CACHE.mkdir(parents=True, exist_ok=True)

    def fetch(p):
        try:
            return p, PLATFORM[p["platform"]](p), None
        except (OSError, ServiceError, ValueError, KeyError, TypeError) as e:
            return p, [], e

    by_juris: dict[str, list[dict]] = {}
    with ThreadPoolExecutor(12) as pool:
        for p, rows, err in pool.map(fetch, portals):
            print(f"  {'FAIL' if err else 'ok  '} {len(rows):>5}  {p['jurisdiction']} {p['portal_url']}"
                  + (f": {err}" if err else ""), flush=True)
            for r in rows:
                r |= {"jurisdiction": p["jurisdiction"], "portal_url": p["portal_url"],
                      "reach": p["reach"]}
            by_juris.setdefault(p["jurisdiction"], []).extend(rows)

    # Record counts last, in one pool, once the rows are deduplicated.
    for code, rows in by_juris.items():
        rows.sort(key=lambda r: (-int(r["reach"]), r["origin"] != "hub", key(r["source_url"])))
        seen, kept = set(known), []
        for r in rows:
            k = key(r["source_url"]) if SERVICE.match(r["source_url"]) else r["source_url"]
            if k and k in seen:
                continue
            seen.add(k)
            kept.append(r)
        by_juris[code] = kept
    todo = [r for rows in by_juris.values() for r in rows
            if SERVICE.match(r["source_url"]) and r.get("geometry") != "raster"]
    print(f"counting records in {len(todo)} layers", flush=True)
    with ThreadPoolExecutor(24) as pool:
        for i, (r, n) in enumerate(zip(todo, pool.map(lambda r: count(r["source_url"]), todo)), 1):
            r["records"] = n
            if i % 500 == 0:
                print(f"  {i} counted", flush=True)

    for code, rows in by_juris.items():
        taken = {}
        for r in sorted(rows, key=lambda r: key(r["source_url"]) or r["dataset"]):
            base = f"{code}/{slug(r['dataset'])}"
            n = taken.get(base, 0) + 1
            taken[base] = n
            r["id"] = base if n == 1 else f"{base}-{n}"
        write_csv(CACHE / f"{code.split('/')[-1]}.csv", COLS, rows)
    print(f"{sum(map(len, by_juris.values()))} rows in {len(by_juris)} jurisdictions")


def chunk():
    names = {j["code"]: j["name"] for j in read_csv(JURISDICTIONS)}
    out = CACHE / "chunks"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.csv"):
        f.unlink()
    chunks = []
    for f in sorted(CACHE.glob("*.csv")):
        rows = read_csv(f)
        if not rows:
            continue
        code = rows[0]["jurisdiction"]
        parts = -(-len(rows) // CHUNK)
        size = -(-len(rows) // parts)
        for i in range(parts):
            name = f"{f.stem}-{i + 1}"
            part = rows[i * size:(i + 1) * size]
            write_csv(out / f"{name}.csv", COLS, part)
            chunks.append({"chunk": name, "jurisdiction": code, "name": names.get(code, code),
                           "rows": len(part), "part": f"{i + 1} of {parts}"})
    (CACHE / "chunks.json").write_text(json.dumps(chunks, indent=1), encoding="utf-8")
    print(f"{len(chunks)} chunks, {sum(c['rows'] for c in chunks)} rows")


# ---------------------------------------------------------------- grading

def check(name: str) -> list[str]:
    want = [r["id"] for r in read_csv(CACHE / "chunks" / f"{name}.csv")]
    path = GRADED / f"{name}.csv"
    if not path.exists():
        return [f"{path} does not exist"]
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != GRADE_COLS:
            return [f"header must be {','.join(GRADE_COLS)}, is {','.join(reader.fieldnames or [])}"]
        got = list(reader)
    errors = []
    ids = [r["id"] for r in got]
    if missing := [i for i in want if i not in ids]:
        errors.append(f"{len(missing)} ids missing, e.g. {missing[:3]}")
    if extra := [i for i in ids if i not in want]:
        errors.append(f"{len(extra)} ids not in the chunk, e.g. {extra[:3]}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids")
    for r in got:
        bad = []
        if r["theme"] not in THEMES:
            bad.append(f"theme {r['theme']!r}")
        if r["tier"] not in ("1", "2", "3", "4", "5"):
            bad.append(f"tier {r['tier']!r}")
        if r["feasibility"] not in FEASIBILITY:
            bad.append(f"feasibility {r['feasibility']!r}")
        if r["status"] not in ("Available", "Not usable"):
            bad.append(f"status {r['status']!r}")
        if not r["provider"].strip():
            bad.append("empty provider")
        if not r["notes"].strip() or "\n" in r["notes"] or len(r["notes"]) > 300:
            bad.append("notes must be one line of 1-300 characters")
        if bad:
            errors.append(f"{r['id']}: {', '.join(bad)}")
    return errors


def merge():
    today = date.today().isoformat()
    LAYERS.mkdir(parents=True, exist_ok=True)
    done, pending = 0, []
    for f in sorted(CACHE.glob("*.csv")):
        rows = read_csv(f)
        graded = {}
        for g in sorted(GRADED.glob(f"{f.stem}-*.csv")):
            if re.fullmatch(rf"{re.escape(f.stem)}-\d+", g.stem):
                graded |= {r["id"]: r for r in read_csv(g)}
        # A row already in catalogue/layers may have been edited by hand since: it stays.
        kept = {r["id"]: r for r in read_csv(LAYERS / f.name)}
        out = []
        for r in rows:
            if r["id"] in kept:
                out.append(kept.pop(r["id"]))
                continue
            g = graded.get(r["id"])
            if g is None:
                pending.append(r["id"])
                continue
            out.append({"id": r["id"], "theme": g["theme"], "dataset": r["dataset"],
                        "provider": g["provider"], "source_url": r["source_url"],
                        "licence": r["licence"], "tier": g["tier"],
                        "feasibility": g["feasibility"], "status": g["status"], "tools": "",
                        "lead": "", "last_verified": today, "notes": g["notes"]})
        out += kept.values()  # gone from the portal since; dropping them is a decision for a person
        if out:
            write_csv(LAYERS / f.name, SOURCE_COLS, out)
            done += len(out)
    print(f"{done} rows merged into {LAYERS}; {len(pending)} still ungraded")


def main():
    args = sys.argv[1:]
    if args[:1] == ["--chunk"]:
        chunk()
    elif args[:1] == ["--check"] and len(args) == 2:
        errors = check(args[1])
        print("\n".join(errors) if errors else f"OK {args[1]}")
        sys.exit(1 if errors else 0)
    elif args[:1] == ["--merge"]:
        merge()
    elif any(a.startswith("-") for a in args):
        sys.exit(__doc__)
    else:
        inventory(set(args))
        chunk()


if __name__ == "__main__":
    main()
