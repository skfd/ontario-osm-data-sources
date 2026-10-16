"""List every dataset and layer the open-data portals publish, so each can be graded once.

Reads   catalogue/portals.csv, catalogue/sources.csv, catalogue/jurisdictions.csv
Writes  cache/inventory/<code>.csv       one row per dataset or layer, with its metadata
        cache/inventory/chunks/<n>.csv   the rows not yet merged, in grading batches of at most CHUNK
        cache/inventory/chunks.json      the batches, for the grading agents
        catalogue/layers/<code>.csv      --merge: graded rows added, existing rows left alone

    python inventory.py [jurisdiction ...]   list the portals (network)
    python inventory.py --chunk              cut the batches again, no network
    python inventory.py --check <chunk>      validate cache/graded/<chunk>.csv
    python inventory.py --merge              graded batches -> catalogue/layers/
    python inventory.py --copies             mark layers that republish another source

Portals swept: every reach 2 to 4 row with an api_url, minus shared-portal rows (their layers
are listed under the owner). The goal is that no layer goes
unlisted; a grade can be argued later, a missing row cannot. A Hub item that names a whole service
becomes one row per layer. A server layer a Hub of the same jurisdiction already lists is
dropped, and so is any URL already in sources.csv. Ids are assigned here, in URL order, so the
graders never invent one; a layer already in catalogue/layers keeps the id it has there.
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

from common import (FEASIBILITY, HERE, JURISDICTIONS, LAYERS, MEASURES, PORTALS, SOURCE_COLS,
                    SOURCES, SYNCED, THEMES, read_csv, write_csv)
import survey
from survey import Secured, ServiceError, get_json, get_text, with_param

# Hundreds of servers, few requests each: more in flight than survey.py's count needs.
survey.SLOTS = threading.Semaphore(24)

CACHE = HERE / "cache" / "inventory"
GRADED = HERE / "cache" / "graded"
CHUNK = 120
SKIP: set[str] = set()  # jurisdictions left out of a sweep
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
    """One spelling per layer: MapServer and FeatureServer of the same service are one layer, and
    a CKAN package is one page in either language."""
    u = urllib.parse.unquote(url.strip().rstrip("/").lower().split("?", 1)[0])
    return (u.replace("/featureserver", "/mapserver").replace("http://", "https://")
            .replace("/en/dataset/", "/dataset/").replace("/fr/dataset/", "/dataset/"))


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
        "layer_name": text(layer.get("name"), 200),
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


# A Hub's own pages and site items are its navigation, not anything it publishes.
SITE_TYPES = {"Hub Page", "Hub Site Application", "Hub Initiative", "Site Page", "Site Application",
              "Solution", "Code Sample"}


def from_hub(p: dict) -> list[dict]:
    url = p["api_url"]
    items = sharing_items(url) if "/sharing/rest/search" in url else hub_items(url)
    rows = []
    for it in items:
        if it.get("type") in SITE_TYPES:
            continue
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
            # A ministry's catalogue names the ministry only as the package's organization, and
            # many of the province's packages only point at the same layer on GeoHub.
            org = (pk.get("organization") or {}).get("title") or ""
            hub = any("geohub" in (r.get("url") or "") for r in pk.get("resources") or [])
            notes = text(pk.get("notes"), 300)
            rows.append({
                "origin": "ckan",
                "dataset": text(pk.get("title") or pk.get("name"), 200),
                "item_type": "CKAN package: " + ", ".join(formats),
                "source_url": f"{site}/dataset/{pk['name']}",
                "edited": (pk.get("metadata_modified") or "")[:10],
                "licence": licence(text(pk.get("license_title"), 150), p["licence"]),
                "description": text(" ".join(filter(None, [f"{org}." if org else "",
                                                           "Links to GeoHub." if hub else "",
                                                           notes])), 300),
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


def from_grin(p: dict) -> list[dict]:
    """GRIN, Grand River's download catalogue: one zip per layer, each under its own licence."""
    return [{"origin": "grin", "dataset": text(d.get("Download_Alias"), 200),
             "item_type": "GRIN download (zip)", "source_url": d.get("Download_URL") or "",
             "edited": d.get("MaxDate") or "",
             "licence": text(d.get("AccessConstraint"), 150) or p["licence"],
             "description": text(d.get("AbstractShort"), 300)}
            for d in get_json(p["api_url"])["results"]]


JKAN_LINK = re.compile(r'href="([^"]+)"[^>]*property=.dcat:accessURL.', re.I)
JKAN_LICENCE = re.compile(r'property="dct:license"[^>]*>\s*(?:<[^>]+>\s*)*([^<]+)', re.I)


def from_jkan(p: dict) -> list[dict]:
    """A JKAN site: datasets.json lists the datasets, each page its links and licence. A dataset
    that links a layer on a map server is that layer, as with a Hub item."""
    site = urllib.parse.urlsplit(p["api_url"])
    rows = []
    for d in get_json(p["api_url"]):
        if "Licence Agreements" in (d.get("category") or []):  # the licence texts themselves
            continue
        page = f"{site.scheme}://{site.netloc}{d['url']}"
        body = get_text(page)
        links = JKAN_LINK.findall(body)
        name = JKAN_LICENCE.search(body)
        updated = re.search(r"(\d\d)-(\d\d)-(\d{4})", d.get("lastUpdate") or "")
        base = {"origin": "jkan", "dataset": text(d.get("title"), 200),
                "item_type": "JKAN dataset: " + ", ".join(d.get("category") or []),
                "source_url": page,
                "edited": f"{updated[3]}-{updated[1]}-{updated[2]}" if updated else "",
                "licence": text(name[1], 150) if name else p["licence"],
                "description": text(re.sub(r"^Last Update \(mm-dd-yyyy\):\s*[\d-]*\s*", "",
                                           text(d.get("notes"), 400)), 300)}
        service = next((u for u in links if SERVICE.match(u)), None)
        layers = expand(service) if service else []
        if not layers:
            rows.append(base)
        for l in layers:
            rows.append(base | {k: v for k, v in l.items() if k in COLS and v}
                        | {"dataset": base["dataset"] if len(layers) == 1
                           else f"{base['dataset']} — {l['layer_name']}"})
    return rows


def from_custom(p: dict) -> list[dict]:
    """A download page with a JSON list behind it; one without has no api_url and is not swept."""
    if "/metadata-api/" in p["api_url"]:
        return from_grin(p)
    if p["api_url"].endswith("/datasets.json"):
        return from_jkan(p)
    raise ValueError(f"no reader for the custom catalogue {p['api_url']}")


PLATFORM = {"arcgis-hub": from_hub, "ckan": from_ckan, "arcgis-rest": from_rest,
            "custom": from_custom}


# ---------------------------------------------------------------- inventory

def swept(p: dict) -> bool:
    return (p["reach"] in ("2", "3", "4") and p["api_url"] and p["platform"] in PLATFORM
            and p["jurisdiction"] not in SKIP and "shared portal of" not in p["notes"])


def inventory(only: set[str]):
    portals = [p for p in read_csv(PORTALS) if swept(p) and (not only or p["jurisdiction"] in only)]
    existing = read_csv(SOURCES) + read_csv(SYNCED)
    known = {key(r["source_url"]) for r in existing if r["source_url"]}
    taken_ids = {r["id"] for r in existing}
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
            u = r["source_url"]
            k = key(u) if SERVICE.match(u) or key(u) in known else u
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
        # A layer already merged keeps its id, so a new portal or a rerun cannot shift the
        # suffixes and hand an old grade to another layer.
        # A Hub item and a server row for one layer are the same layer under two spellings.
        spell = lambda u: key(u) if SERVICE.match(u) else u
        merged = {spell(r["source_url"]): r["id"] for r in read_csv(LAYERS / f"{code.split('/')[-1]}.csv")}
        # The tracker's address points are left free: the same dataset found here is dropped below.
        used = set(merged.values()) | {i for i in taken_ids if not i.endswith("/addresses")}
        for r in sorted(rows, key=lambda r: key(r["source_url"]) or r["dataset"]):
            if spell(r["source_url"]) in merged:
                r["id"] = merged[spell(r["source_url"])]
                continue
            base, n = f"{code}/{slug(r['dataset'])}", 1
            while (i := base if n == 1 else f"{base}-{n}") in used:
                n += 1
            used.add(i)
            r["id"] = i
        # The tracker follows each municipality's address points under <code>/addresses, often
        # at another URL; the same dataset found on a portal is that source, not a new one.
        rows[:] = [r for r in rows if r["id"] not in taken_ids or not r["id"].endswith("/addresses")]
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
        merged = {r["id"] for r in read_csv(LAYERS / f.name)}
        rows = [r for r in read_csv(f) if r["id"] not in merged]
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
    known = (set(want) | {r["id"] for f in LAYERS.glob("*.csv") for r in read_csv(f)}
             | {r["id"] for r in read_csv(SOURCES) + read_csv(SYNCED)})
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
        if r["status"] not in ("Available", "No licence", "Not usable"):
            bad.append(f"status {r['status']!r}")
        if not r["provider"].strip():
            bad.append("empty provider")
        if not r["notes"].strip() or "\n" in r["notes"] or len(r["notes"]) > 300:
            bad.append("notes must be one line of 1-300 characters")
        if r["notes"].startswith(COPY) and marked(r) not in known:
            bad.append("a note starting 'Copy of ' must go on 'Copy of <known id>. '")
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

COPY = "Copy of "
MARK = re.compile(r"^Copy of (ca/on/[a-z0-9/-]*[a-z0-9])\.(?: |$)")
SAID = re.compile(r"(?:same (?:data|endpoint|layer|dataset|service) as|layer behind|tracked as|"
                  r"copy of|copies|copying|duplicates?|the source is|the live layer is) "
                  r"(ca/on/[a-z0-9/-]*[a-z0-9])", re.I)


def marked(r: dict) -> str:
    """The id a row's note names as its original, or "" when the note does not start with one.
    "Copy of the county's layer" is a grader's sentence, not a mark."""
    m = MARK.match(r["notes"])
    return m.group(1) if m and m.group(1) != r["id"] else ""


def copies():
    """Mark each layer that republishes another: the address points the tracker already follows
    (same service, or a record count within 1% of the tracker's); the same URL listed by two
    jurisdictions; a copy the grader named in the note; or, within a jurisdiction, the same
    geometry and record count with the same fields, or with the same theme when the count is
    1,000 or more. The copy keeps its row, so nothing goes unlisted, but drops to
    tier 2 at most, becomes reference, and its note starts with the id of the one it copies.
    The kept layer is the best graded, then the Hub's, then the latest edited. Rows already
    marked are left alone, so this can run after every --merge."""
    meta = {r["id"]: r for f in CACHE.glob("*.csv") for r in read_csv(f)}
    files = {f: read_csv(f) for f in sorted(LAYERS.glob("*.csv"))}
    rows = [r for rs in files.values() for r in rs]
    tracked = {}
    for r in read_csv(SYNCED):
        tracked[r["id"].rsplit("/", 1)[0]] = r
    tracked_ids = {r["id"] for r in tracked.values()}
    sizes = {}
    for m in read_csv(MEASURES):
        if m["of"] and m["source_id"].endswith("/addresses"):
            sizes[m["source_id"]] = int(m["of"])  # measures.csv is in date order: the last wins

    def service(url: str) -> str:
        m = SERVICE.match(url or "")
        return key(m.group(1)) if m else ""

    def base(url: str) -> str:
        """The service's name without the view suffixes AGOL adds: X_Public_View is X."""
        name = service(url).rsplit("/", 2)[-2] if service(url) else ""
        return re.sub(r"(_public)?(_view)?$", "", name)

    ids = {r["id"] for r in rows} | set(tracked_ids) | {r["id"] for r in read_csv(SOURCES)}
    # Copies marked on an earlier run, by hand or by this, still point a group outside itself.
    original = {r["id"]: marked(r) for r in rows if marked(r) in ids}
    for r in rows:
        if r["theme"] != "addresses" or marked(r):
            continue
        t = tracked.get(r["id"].rsplit("/", 1)[0])
        if not t:
            continue
        n, size = meta.get(r["id"], {}).get("records"), sizes.get(t["id"])
        same_service = base(r["source_url"]) and base(r["source_url"]) == base(t["source_url"])
        if same_service or (n and size and abs(int(n) - size) <= size / 100):
            original[r["id"]] = t["id"]

    # A layer listed by two jurisdictions (a Hub that shows its region's items) belongs to the
    # upper tier. Between equals it belongs to a member before an association that gathers its
    # members' layers (Conservation Ontario's shared org), then to the one whose Hub lists it,
    # then to the first by code.
    rank = {j["code"]: (("upper", "single", "lower", "").index(j["tier"]), j["level"] == "association")
            for j in read_csv(JURISDICTIONS)}
    by_url = {}
    for r in rows:
        if service(r["source_url"]):
            by_url.setdefault(key(r["source_url"]), []).append(r)
    for g in by_url.values():
        if len({r["id"].rsplit("/", 1)[0] for r in g}) > 1:
            # One already marked stays the copy, so an earlier run's choice is not reversed.
            g.sort(key=lambda r: (r["id"] in original, rank.get(r["id"].rsplit("/", 1)[0], (3, False)),
                                  meta.get(r["id"], {}).get("origin") != "hub", r["id"]))
            for r in g[1:]:
                original.setdefault(r["id"], g[0]["id"])

    # What the graders said in so many words: "a copy of <id>", "the same layer as <id>".
    said = {}
    for r in rows:
        m = SAID.search(r["notes"])
        if m and m.group(1) in ids and m.group(1) != r["id"] and not marked(r):
            said[r["id"]] = m.group(1)
    for a, b in said.items():
        if said.get(b) != a:
            original.setdefault(a, b)

    groups = {}
    for r in rows:
        m = meta.get(r["id"])
        if m and m["records"] and int(m["records"]) >= 2 and m["fields"]:
            k = (m["jurisdiction"], m["geometry"], m["records"], m["fields"].lower())
            groups.setdefault(k, []).append(r)
        if m and m["records"] and int(m["records"]) >= 1000:  # a big exact count is a fingerprint
            k = (m["jurisdiction"], m["geometry"], m["records"], r["theme"])
            groups.setdefault(k, []).append(r)
    for g in groups.values():
        if len(g) < 2:
            continue
        outside = next((original[r["id"]] for r in g if r["id"] in original), None)
        g.sort(key=lambda r: (-int(r["tier"] or 0), meta[r["id"]]["origin"] != "hub",
                              -int(meta[r["id"]]["edited"].replace("-", "") or 0),
                              len(r["id"])))
        for r in g if outside else g[1:]:
            original.setdefault(r["id"], outside or g[0]["id"])

    def root(i: str) -> str:
        seen = {i}
        while original.get(i) and original[i] not in seen:
            i = original[i]
            seen.add(i)
        return i

    marked = 0
    for r in rows:
        of = original.get(r["id"]) and root(r["id"])
        if of == r["id"]:
            continue
        if not of or marked(r):
            continue
        r["tier"] = str(min(int(r["tier"] or 2), 2))
        if r["feasibility"] != "no":
            r["feasibility"] = "reference"
        note = f"{COPY}{of}. {r['notes']}"
        r["notes"] = note if len(note) <= 300 else note[:299].rstrip() + "…"
        marked += 1
    for f, rs in files.items():
        write_csv(f, SOURCE_COLS, rs)
    print(f"{marked} layers marked as copies")


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
    elif args[:1] == ["--copies"]:
        copies()
    elif any(a.startswith("-") for a in args):
        sys.exit(__doc__)
    else:
        inventory(set(args))
        chunk()


if __name__ == "__main__":
    main()
