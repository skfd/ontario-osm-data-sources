"""The catalogue's files, vocabularies and loaders, shared by sync.py and build.py."""

import csv
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE_DIR = HERE.parent
CATALOGUE = HERE / "catalogue"
SOURCES = CATALOGUE / "sources.csv"
SYNCED = CATALOGUE / "synced" / "addresses.csv"
MEASURES = CATALOGUE / "measures.csv"
JURISDICTIONS = CATALOGUE / "jurisdictions.csv"
WORK = CATALOGUE / "work.csv"
PORTALS = CATALOGUE / "portals.csv"

SOURCE_COLS = ["id", "theme", "dataset", "provider", "source_url", "licence", "tier",
               "feasibility", "status", "tools", "lead", "last_verified", "notes"]
SYNCED_COLS = ["id", "theme", "dataset", "provider", "source_url", "licence", "tracker_tier",
               "lwg", "lwg_url", "feasibility", "status", "tools", "last_verified", "notes"]
WORK_COLS = ["id", "source_id", "kind", "status", "lead", "started", "ended", "tools", "notes"]
MEASURE_COLS = ["source_id", "measured_on", "measure", "value", "of", "unit", "method", "text"]
PORTAL_COLS = ["jurisdiction", "portal_url", "platform", "api_url", "licence", "layers_seen",
               "surveyed_on", "notes"]

FEASIBILITY = {
    "import": "Import",
    "conflate": "Conflate",
    "validate": "Validate",
    "reference": "Reference",
    "no": "No",
}
STATUSES = ["Completed", "Ongoing", "Planned", "Onboarding", "Available", "Parked", "Not usable"]
THEMES = [
    "addresses", "buildings", "roads", "traffic", "parking", "cycling", "pedestrian", "trails",
    "transit", "parks", "recreation", "trees", "water", "amenities", "emergency", "health",
    "education", "community", "poi", "heritage", "boundaries", "planning", "elections",
    "waste", "environment", "topography", "imagery", "catalogue",
]
MEASURES_VOCAB = ["missing", "matched", "added", "observation", "note"]
WORK_KINDS = ["import", "gap-fill", "maintenance", "conflation", "task-queue", "survey"]
WORK_STATUSES = ["Completed", "Ongoing", "Planned", "Parked"]
PLATFORMS = ["arcgis-hub", "arcgis-rest", "ckan", "socrata", "opendatasoft", "custom",
             "none-found"]
TIERS = ["upper", "single", "lower"]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, cols: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, cols, lineterminator="\n")
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in cols} for r in rows)


def jurisdiction(source_id: str) -> str:
    return source_id.rsplit("/", 1)[0]


def is_date(s: str) -> bool:
    try:
        date.fromisoformat(s)
        return True
    except ValueError:
        return False


def tool_pairs(tools: str) -> list[tuple[str, str]]:
    out = []
    for pair in filter(None, (p.strip() for p in tools.split(";"))):
        label, _, url = pair.partition("|")
        out.append((label.strip(), url.strip()))
    return out


def load() -> tuple[list[dict], list[dict], dict[str, dict], list[dict]]:
    """(sources, measures, jurisdictions, portals), validated. A hand row whose id is a synced
    row adds to it: its non-empty cells win, and its tools follow the synced ones. Each source
    carries its streams of work as r["work"]."""
    synced = read_csv(SYNCED)
    hand = read_csv(SOURCES)
    measures = read_csv(MEASURES)
    juris = {j["code"]: j for j in read_csv(JURISDICTIONS)}
    portals = read_csv(PORTALS)
    errors = []

    names = Counter(j["name"] for j in juris.values())
    for j in juris.values():
        if names[j["name"]] > 1:
            errors.append(f"jurisdictions.csv {j['code']}: name {j['name']!r} used twice")
        if j["tier"] not in TIERS + [""]:
            errors.append(f"jurisdictions.csv {j['code']}: tier {j['tier']!r}")

    blank = dict.fromkeys(SOURCE_COLS + SYNCED_COLS, "")
    by_id = {r["id"]: blank | r for r in synced}
    sources = list(by_id.values())
    seen = set()
    for n, r in enumerate(hand, start=2):
        where = f"sources.csv:{n} {r['id']}"
        if r["id"] in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(r["id"])
        base = by_id.get(r["id"])
        if base:
            tools = "; ".join(x for x in (base["tools"], r["tools"]) if x)
            base.update({k: v for k, v in r.items() if v})
            base["tools"] = tools
            continue
        for k in ("dataset", "feasibility", "status"):
            if not r[k]:
                errors.append(f"{where}: no {k} (and no synced row to add to)")
        sources.append(blank | r)

    for r in sources:
        where = r["id"]
        if not re.fullmatch(r"[a-z]+(/[a-z0-9-]+)+", r["id"]):
            errors.append(f"{where}: id is not a lowercase path")
        if jurisdiction(r["id"]) not in juris:
            errors.append(f"{where}: jurisdiction {jurisdiction(r['id'])!r} not in jurisdictions.csv")
        if r["theme"] not in THEMES:
            errors.append(f"{where}: theme {r['theme']!r}")
        if r["feasibility"] not in FEASIBILITY:
            errors.append(f"{where}: feasibility {r['feasibility']!r}")
        if r["status"] not in STATUSES:
            errors.append(f"{where}: status {r['status']!r}")
        if r.get("last_verified") and not is_date(r["last_verified"]):
            errors.append(f"{where}: last_verified {r['last_verified']!r}")
        for label, url in tool_pairs(r["tools"]):
            if not url.startswith("http"):
                errors.append(f"{where}: tool {label!r} has no URL")
        for k, v in r.items():
            if k != "tools" and "|" in (v or ""):
                errors.append(f"{where}: pipe in {k}")

    ids = {r["id"] for r in sources}
    for r in sources:
        r["work"] = []
    by_src = {r["id"]: r for r in sources}
    work_ids = set()
    for n, w in enumerate(read_csv(WORK), start=2):
        where = f"work.csv:{n} {w['id']}"
        if w["id"] in work_ids or w["id"] in ids:
            errors.append(f"{where}: duplicate id")
        work_ids.add(w["id"])
        if w["source_id"] not in by_src:
            errors.append(f"{where}: no such source {w['source_id']!r}")
            continue
        if not w["id"].startswith(w["source_id"] + "/") or w["id"].count("/") != w["source_id"].count("/") + 1:
            errors.append(f"{where}: id must be <source_id>/<slug>")
        if w["kind"] not in WORK_KINDS:
            errors.append(f"{where}: kind {w['kind']!r}")
        if w["status"] not in WORK_STATUSES:
            errors.append(f"{where}: status {w['status']!r}")
        for k in ("started", "ended"):
            if w[k] and not is_date(w[k]):
                errors.append(f"{where}: {k} {w[k]!r}")
        for label, url in tool_pairs(w["tools"]):
            if not url.startswith("http"):
                errors.append(f"{where}: tool {label!r} has no URL")
        by_src[w["source_id"]]["work"].append(w)
    ids |= work_ids
    for n, m in enumerate(measures, start=2):
        where = f"measures.csv:{n} {m['source_id']}"
        if m["source_id"] not in ids:
            errors.append(f"{where}: no such source or work")
        if not is_date(m["measured_on"]):
            errors.append(f"{where}: measured_on {m['measured_on']!r}")
        if m["measure"] not in MEASURES_VOCAB:
            errors.append(f"{where}: measure {m['measure']!r}")
        for k in ("value", "of"):
            if m[k] and not re.fullmatch(r"\d+(\.\d+)?", m[k]):
                errors.append(f"{where}: {k} {m[k]!r} is not a number")

    seen, found = set(), defaultdict(set)
    for n, p in enumerate(portals, start=2):
        where = f"portals.csv:{n} {p['jurisdiction']}"
        if (p["jurisdiction"], p["portal_url"]) in seen:
            errors.append(f"{where}: duplicate portal {p['portal_url']!r}")
        seen.add((p["jurisdiction"], p["portal_url"]))
        found[p["jurisdiction"]].add(p["platform"] != "none-found")
        if p["jurisdiction"] not in juris:
            errors.append(f"{where}: jurisdiction not in jurisdictions.csv")
        if p["platform"] not in PLATFORMS:
            errors.append(f"{where}: platform {p['platform']!r}")
        if not is_date(p["surveyed_on"]):
            errors.append(f"{where}: surveyed_on {p['surveyed_on']!r}")
        if p["layers_seen"] and not p["layers_seen"].isdigit():
            errors.append(f"{where}: layers_seen {p['layers_seen']!r} is not a count")
        for k in ("portal_url", "api_url"):
            if p[k] and not p[k].startswith("http"):
                errors.append(f"{where}: {k} is not a URL")
        if p["platform"] == "none-found":
            if any(p[k] for k in ("portal_url", "api_url", "licence", "layers_seen")):
                errors.append(f"{where}: none-found with a portal, API, licence or count")
            if not p["notes"]:
                errors.append(f"{where}: none-found without a note of what was checked")
        elif not p["portal_url"]:
            errors.append(f"{where}: no portal_url")
        for k, v in p.items():
            if "|" in (v or ""):
                errors.append(f"{where}: pipe in {k}")
    for code, kinds in found.items():
        if len(kinds) == 2:
            errors.append(f"portals.csv {code}: both a portal and a none-found row")

    if errors:
        sys.exit("catalogue failed validation:\n  " + "\n  ".join(errors))
    return sources, measures, juris, portals


def latest(measures: list[dict]) -> dict[str, dict]:
    """source id -> its most recent measure; on a tie the later line wins."""
    out = {}
    for m in measures:
        cur = out.get(m["source_id"])
        if not cur or m["measured_on"] >= cur["measured_on"]:
            out[m["source_id"]] = m
    return out


def measure_text(m: dict | None) -> str:
    if not m:
        return ""
    return m["text"] if m["measured_on"] in m["text"] else f"{m['text']} ({m['measured_on']})"
