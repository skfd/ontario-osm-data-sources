"""Render the catalogue into its views. Reads only this repository.

Reads   catalogue/*.csv, catalogue/synced/*.csv  (see catalogue/SCHEMA.md)
Writes  index.html, portals.html                 the catalogue as tables, for GitHub Pages
        rows-d.js, rows-f.js                     index.html's D and F rows, loaded on request
        wiki/Canada_Open_data.wiki               the OSM wiki page
        report/SUMMARY.md                        counts, freshness, gaps and coverage, for review

    python build.py
"""

import json
import re
from collections import Counter, defaultdict
from datetime import date
from html import escape as esc
from urllib.parse import quote

from common import (FEASIBILITY, HERE, PLATFORMS, REACH, STATUSES, THEMES, jurisdiction,
                    latest, load, measure_text, tool_pairs)

WIKI = HERE / "wiki"
REPORT = HERE / "report"
REPO_URL = "https://github.com/skfd/ontario-osm-data-sources"
OSMF_PAGE = "https://osmfoundation.org/wiki/OGL_Canada_and_local_variants"
SURVEY_DATE = "2026-08-12"
PAGES_URL = "https://skfd.github.io/ontario-osm-data-sources/"
WIKI_MIN_TIER = 3  # swept layers below this stay off the wiki page

STATUS_STYLE = {
    "Completed": "background:#d4f4d4",
    "Ongoing": "background:#e6f6d0",
    "Planned": "background:#fdf6c8",
    "Onboarding": "background:#fdf6c8",
    "Available": "background:#e8eef8",
    "Parked": "background:#f4e0d0",
    "No licence": "background:#f8e4e4",
    "Not usable": "background:#eeeeee",
}


def is_address_dataset(r: dict) -> bool:
    """The one address-point dataset of a municipality; other address rows are work on it."""
    return r["id"].count("/") == 3 and r["id"].endswith("/addresses")


def with_work(r: dict) -> dict:
    """The row as the wiki shows it: its work streams' tools, leads and states folded in."""
    if not r["work"]:
        return r
    tools, urls = [], set()
    for label, url in tool_pairs(r["tools"]) + [p for w in r["work"] for p in tool_pairs(w["tools"])]:
        if url not in urls:
            urls.add(url)
            tools.append(f"{label}|{url}")
    active = [w for w in r["work"] if w["status"] in ("Ongoing", "Planned")] or r["work"]
    leads = list(dict.fromkeys([r["lead"]] * bool(r["lead"]) + [w["lead"] for w in active if w["lead"]]))
    states = []
    for w in r["work"]:
        state = f"{w['kind'].replace('-', ' ')} {w['status'].lower()}"
        if w["status"] == "Completed" and w["ended"]:
            state += f" {w['ended']}"
        elif w["status"] == "Ongoing" and w["started"]:
            state += f" since {w['started']}"
        states.append(state)
    notes = "; ".join(x for x in (r["notes"], ", ".join(states)) if x)
    return r | {"tools": "; ".join(tools), "lead": ", ".join(leads), "notes": notes}


# ---------------------------------------------------------------- wikitext

def ext(url: str, label: str) -> str:
    return f"[{url} {label}]" if url else label


def table(rows: list[dict], first_col: str, cols: list[str]) -> str:
    head = {
        "dataset": "Dataset", "provider": "Municipality", "licence": "Licence",
        "lwg": "LWG", "tier": "Value", "coverage": "In OSM", "feasibility": "Use",
        "status": "Status", "tools": "Tools", "lead": "Lead",
        "last_verified": "Verified", "notes": "Notes",
    }
    out = ['{| class="wikitable sortable" style="font-size:90%"', "|-"]
    out.append("! " + " !! ".join(head[c] for c in [first_col] + cols))
    for r in rows:
        out.append("|-")
        cells = []
        for c in [first_col] + cols:
            v = r.get(c, "") or ""
            if c == first_col:
                v = ext(r.get("source_url", ""), v)
            elif c == "feasibility":
                v = FEASIBILITY.get(v, v)
            elif c == "status":
                style = STATUS_STYLE.get(v)
                v = f'style="{style}" | {v}' if style else v
            elif c == "tools":
                v = "<br>".join(ext(url, label) for label, url in tool_pairs(v))
            elif c == "lead":
                v = "<br>".join(f"{{{{User|{u}}}}}" for u in v.split(", ") if u)
            elif c == "lwg":
                v = ("[[Contributors#Ontario|self-listed]]" if v == "self-listed"
                     else ext(r.get("lwg_url", ""), v))
            elif c == "tier":
                v = f"{v}/5" if v else ""
            cells.append(v)
        out.append("| " + " || ".join(cells))
    out.append("|}")
    return "\n".join(out)


LEGEND = """{| class="wikitable" style="font-size:90%"
! Use !! means
|-
| Import || bulk upload after an import proposal ([[Import/Guidelines]])
|-
| Conflate || merge names, attributes or missing features into what OSM already has
|-
| Validate || a gap list or task queue (gaps page, MapRoulette, Osmose) worked by hand
|-
| Reference || a tile layer to trace or check against; nothing is uploaded
|-
| No || not useful for OSM, or not licensed
|}"""

PREAMBLE = (
    f"This page is generated from [{REPO_URL} ontario-osm-data-sources]. Fix a row there. "
    "Edit here if you like, and say so on the talk page.\n\n"
    "'''A row here is not permission to import.''' The licence verdict for every portal lives "
    "in [[Canada#Open Data]] and on the OSMF "
    f"[{OSMF_PAGE} OGL Canada and local variants] page; the LWG column only cites it. Every "
    "import still needs a proposal, a community discussion and an [[Import/Catalogue]] entry."
)


def summarize(rows) -> str:
    c = Counter(r["status"] for r in rows)
    return ", ".join(f"{n} {s.lower()}" for s, n in c.most_common())


def wiki_page(sources, juris) -> str:
    national = [r for r in sources if jurisdiction(r["id"]) == "ca"]
    prov = [r for r in sources if jurisdiction(r["id"]) == "ca/on"]
    addresses = [r for r in sources if is_address_dataset(r)]
    local = [r for r in sources if jurisdiction(r["id"]).count("/") == 2 and not is_address_dataset(r)]
    by_muni = defaultdict(list)
    for r in local:
        by_muni[jurisdiction(r["id"])].append(r)
    cols = ["licence", "coverage", "feasibility", "status", "tools", "lead", "last_verified",
            "notes"]
    sections = []
    for code, every in sorted(by_muni.items(), key=lambda kv: -len(kv[1])):
        # The sweep lists every layer; the wiki shows the ones worth a mapper's time and
        # index.html all of them. A page over 2 MB will not save.
        rs = [r for r in every if not r["swept"] or int(r["tier"] or 0) >= WIKI_MIN_TIER]
        hidden = len(every) - len(rs)
        scored = any(r["tier"] for r in rs)
        intro = (f"{len(rs)} layers ({summarize(rs)}). ''Value'' is a 1–5 score of what OSM "
                 "would gain." if scored else "")
        if hidden:
            intro += (f" {hidden} more swept layers scored below {WIKI_MIN_TIER}; they are in "
                      f"the [{PAGES_URL} catalogue].")
        intro += "\n\n" if intro else ""
        sections.append(f"=== {juris[code]['name']} ===\n{intro}"
                        + table(rs, "dataset", cols[:1] + (["tier"] if scored else []) + cols[1:]))
    munis_text = "\n\n".join(sections)
    wide = ["provider", "licence", "feasibility", "status", "tools", "last_verified", "notes"]
    return f"""{{{{Languages|Canada/Open data}}}}
Open data that can be used for OpenStreetMap in Canada: what each source is good for, and how
far work on it has got. Only Ontario is filled in so far; other provinces are welcome.

{PREAMBLE}

== Use ==
{LEGEND}

== National sources ==
{table(national, "dataset", wide)}

== Ontario ==
=== Provincial sources ===
{table(prov, "dataset", wide)}

=== Address points ===
{len(addresses)} municipal and county address-point datasets ({summarize(addresses)}).
''In OSM'' is the share of source addresses with no matching OSM address, measured from a
Geofabrik extract on {SURVEY_DATE} unless the row says otherwise.

{table(addresses, "provider", ["licence", "lwg", "coverage", "feasibility", "status", "tools", "lead", "notes"])}

{munis_text}

== Other provinces ==
Licence status per portal: [[Canada#Open Data]]. Add a section here when you have
dataset-level detail.

[[Category:Canada]]
[[Category:Data sources from Canada]]
"""


# ---------------------------------------------------------------- summary

def md_table(head: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def summary(sources, measures, juris, last) -> str:
    today = date.today()
    numeric = {m["source_id"] for m in measures if m["of"]}
    age = lambda m: (today - date.fromisoformat(m["measured_on"])).days

    # by jurisdiction
    by_j = defaultdict(list)
    for r in sources:
        by_j[jurisdiction(r["id"])].append(r)
    j_rows, only_addr = [], []
    for code, rs in sorted(by_j.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(rs) == 1 and is_address_dataset(rs[0]):
            only_addr += rs
            continue
        dates = [last[r["id"]]["measured_on"] for r in rs if r["id"] in last]
        j_rows.append([juris[code]["name"], len(rs), sum(r["id"] in numeric for r in rs),
                       max(dates) if dates else "—"])
    dates = [last[r["id"]]["measured_on"] for r in only_addr if r["id"] in last]
    j_rows.append([f"{len(only_addr)} more municipalities, address dataset only", len(only_addr),
                   sum(r["id"] in numeric for r in only_addr), max(dates) if dates else "—"])

    # theme x status
    ts = Counter((r["theme"], r["status"]) for r in sources)
    themes = [t for t in THEMES if any(r["theme"] == t for r in sources)]
    statuses = [s for s in STATUSES if any(r["status"] == s for r in sources)]
    t_rows = [[t] + [ts[(t, s)] or "" for s in statuses] + [sum(ts[(t, s)] for s in statuses)]
              for t in themes]

    # freshness
    buckets = Counter()
    for r in sources:
        m = last.get(r["id"])
        if not m or m["measure"] == "note":
            buckets["no measure"] += 1
        elif age(m) <= 30:
            buckets["≤ 30 days"] += 1
        elif age(m) <= 90:
            buckets["31–90 days"] += 1
        else:
            buckets["> 90 days"] += 1
    f_rows = [[k, buckets[k]] for k in ("≤ 30 days", "31–90 days", "> 90 days", "no measure")]

    # work in progress: what to watch
    a_rows = []
    for r in sorted(sources, key=lambda r: r["id"]):
        for w in r["work"]:
            if w["status"] in ("Ongoing", "Planned"):
                m = last.get(w["id"]) or last.get(r["id"])
                a_rows.append([w["id"], f"{w['kind']}, {w['status']}", w["lead"], measure_text(m)])
        if not r["work"] and r["status"] in ("Ongoing", "Planned", "Onboarding"):
            a_rows.append([r["id"], r["status"], r["lead"], measure_text(last.get(r["id"]))])

    # Layers worth asking for: of use, graded 3 or more, no open licence, not a copy.
    asks = defaultdict(list)
    for r in sources:
        if (r["status"] == "No licence" and int(r["tier"] or 0) >= 3
                and not r["notes"].startswith("Copy of ")):
            asks[jurisdiction(r["id"])].append(r)
    ask_rows = []
    for code, rs in sorted(asks.items(), key=lambda kv: (-max(int(r["tier"]) for r in kv[1]),
                                                         -len(kv[1]), juris[kv[0]]["name"])):
        rs.sort(key=lambda r: (-int(r["tier"]), r["dataset"]))
        best = "; ".join(f"{r['dataset']} ({r['tier']})" for r in rs[:4])
        ask_rows.append([juris[code]["name"], len(rs), rs[0]["tier"], best.replace("|", "/")])

    unparsed = [m for m in measures if m["measure"] == "observation"]
    return f"""# Catalogue summary

Generated by `build.py` on {today}. {len(sources)} sources in {len(by_j)} jurisdictions;
{sum(len(r["work"]) for r in sources)} streams of work on them;
{len(measures)} measures, {len(numeric)} sources with a numeric one.

## By jurisdiction

{md_table(["jurisdiction", "sources", "with a number", "latest measure"], j_rows)}

## Theme × status

{md_table(["theme"] + statuses + ["total"], t_rows)}

## Freshness of the latest measure

{md_table(["age", "sources"], f_rows)}

## Licences to ask for

{sum(len(rs) for rs in asks.values())} layers graded 3 to 5 are of use but carry no open
licence, in {len(asks)} jurisdictions. Each is a line in an email to the publisher. Copies are
left out; the original is the one to ask about.

{md_table(["jurisdiction", "layers", "best", "the best of them (value)"], ask_rows)}

## Being worked on

{md_table(["id", "status", "lead", "latest measure"], a_rows)}

## Measures still free text

{len(unparsed)} measures have no `value`/`of`. Each needs a defined measure before it can be
tracked over time:

""" + "\n".join(f"- `{m['source_id']}` — {m['text']}" for m in unparsed) + "\n"


def coverage(sources, juris, portals) -> str:
    """How much of what Ontario publishes the catalogue has looked at: the portal inventory is
    the denominator, catalogued sources the numerator."""
    catalogued = Counter(jurisdiction(r["id"]) for r in sources)
    by_j = defaultdict(list)
    for p in portals:
        by_j[p["jurisdiction"]].append(p)
    live = [p for p in portals if p["platform"] != "none-found"]
    counted = {p["portal_url"]: int(p["layers_seen"]) for p in live if p["layers_seen"]}
    seen = sum(counted.values())
    in_counted = sum(catalogued[j] for j in {p["jurisdiction"] for p in live if p["layers_seen"]})

    shared = lambda p: "shared portal of" in p["notes"]
    # each municipality at the best reach any of its rows has
    best = {c: max(int(p["reach"]) for p in ps) for c, ps in by_j.items()}
    grades = sorted(REACH, reverse=True)
    tiers = [("upper", "upper-tier"), ("single", "single-tier"), ("lower", "lower-tier")]
    t_rows = []
    for tier, label in tiers:
        codes = [c for c, j in juris.items() if j["tier"] == tier]
        n = Counter(best[c] for c in codes if c in best)
        t_rows.append([label, len(codes)] + [n[g] for g in grades] + [len(codes) - n.total()])
    t_rows.append(["**all**"] + [sum(r[i] for r in t_rows) for i in range(1, len(grades) + 3)])

    p_rows = []
    for plat in PLATFORMS[:-1]:
        urls = {p["portal_url"] for p in live if p["platform"] == plat}
        if urls:
            n = [counted[u] for u in urls if u in counted]
            p_rows.append([plat, len(urls), sum(n) if n else "—"])

    j_rows = []
    owners = {p["jurisdiction"] for p in live if not shared(p)}
    for code in owners:
        ps = [p for p in by_j[code] if p in live and not shared(p)]
        n = [int(p["layers_seen"]) for p in ps if p["layers_seen"]]
        j_rows.append([juris[code]["name"], ", ".join(sorted({p["platform"] for p in ps})),
                       sum(n) if n else "—", catalogued[code] or "",
                       f"{catalogued[code] / sum(n):.1%}" if n and catalogued[code] else ""])
    j_rows.sort(key=lambda r: (-(r[2] if r[2] != "—" else -1), r[0]))
    via_only = len({p["jurisdiction"] for p in live} - owners)

    return f"""## Coverage of the catalogue

`catalogue/portals.csv` lists every open-data portal found in Ontario and a `none-found` row
for each municipality that has none. {len(set(p["portal_url"] for p in live))} portals are known,
{len(counted)} of them counted through their API: **{seen} layers seen, against {in_counted}
sources catalogued in those jurisdictions.** A layer seen is a candidate source; a shared
county or consortium portal is counted once, under its owner.

Each municipality at its best *reach*: how good its data is likely to be, judged only by how it
is published (licence plays no part). 4 its own open-data catalogue; 3 its own datasets in a
county or consortium catalogue; 2 queryable layers on a public map server, its own or the
county's, that no catalogue lists; 1 a map viewer only; 0 nothing found.

{md_table(["municipalities", "total"] + [f"{g} {REACH[g]}" for g in grades] + ["not surveyed"],
          t_rows)}

An `arcgis-rest` count includes every layer on the server, viewer backends too, so it runs
higher than a Hub's count of curated datasets.

{md_table(["platform", "portals", "layers seen"], p_rows)}

Jurisdictions with a portal of their own. *Share* is sources catalogued over layers seen; over
100% means the catalogue holds layers the portal's own catalogue does not list (Guelph's audit
worked from the server behind its Hub). The {via_only} municipalities found only on a county or
consortium portal are in `portals.csv`.

{md_table(["jurisdiction", "platform", "layers seen", "sources catalogued", "share"], j_rows)}
"""


# ---------------------------------------------------------------- html

REACH_STYLE = {4: "background:#c6ebd0", 3: "background:#dcf1d2", 2: "background:#eef3c9",
               1: "background:#f6e6d2", 0: "background:#ececec"}
TIER_LABEL = {"upper": "upper-tier", "single": "single-tier", "lower": "lower-tier"}
# The page shows the 1–5 tier as a school grade; the CSVs, the wiki and SUMMARY.md keep 1–5.
GRADE = {"5": "A", "4": "B", "3": "C", "2": "D", "1": "F"}
UNGRADED = "ungraded"
GRADE_MEANS = {"A": "a large gap filled", "B": "features OSM lacks in bulk",
               "C": "a gaps list or reference", "D": "small, or OSM has it",
               "F": "not something OSM maps", UNGRADED: "hand-catalogued, not graded"}
DEFERRED = ("D", "F")  # rows-d.js and rows-f.js: loaded when the Value filter asks for them
GRADE_STYLE = {"A": "background:#8fd19e", "B": "background:#c8ebb4", "C": "background:#f7e79a",
               "D": "background:#f8c99a", "F": "background:#f1cfcf"}
SHARED_ARCGIS = re.compile(r"^services\d*\.arcgis\.com$|^utility\.arcgis\.com$")


def host(url: str) -> str:
    return url.split("//", 1)[-1].split("/", 1)[0].lower() if url else ""


def portal_label(url: str) -> str:
    """The host, and on ArcGIS Online's shared hosts the organisation too."""
    h = host(url)
    if SHARED_ARCGIS.match(h):
        return "/".join(url.split("//", 1)[-1].split("/")[:2])
    return h


def portal_finder(portals):
    """Which portal a source was found on. Of the jurisdiction's portals: one whose licence the
    row carries (a server's layers always carry the server's), then one on the source's host,
    then the best reach. A source with none, the host's portal anywhere. Checked against the
    sweep's own record: every swept layer comes out on the portal it was listed from."""
    live = [p for p in portals if p["platform"] != "none-found"]
    by_j = defaultdict(list)
    for p in live:
        by_j[p["jurisdiction"]].append(p)

    def find(r: dict) -> dict | None:
        h = portal_label(r["source_url"]).lower()
        on_host = lambda p: h in (portal_label(p["portal_url"]).lower(),
                                  portal_label(p["api_url"]).lower())
        mine = by_j[jurisdiction(r["id"])]
        own = [p for p in mine if p["platform"] != "arcgis-rest" or p["licence"] == r["licence"]]
        if own:
            return max(own, key=lambda p: (p["licence"] == r["licence"], on_host(p),
                                           int(p["reach"]), int(p["layers_seen"] or 0)))
        return next((p for p in mine + live if on_host(p)), None)
    return find


def share_in_osm(m: dict | None) -> float | None:
    """The share of the source that is in OSM, from a numeric missing or matched measure."""
    if not m or not m["of"] or not float(m["of"]) or m["measure"] not in ("missing", "matched"):
        return None
    v, of = float(m["value"]), float(m["of"])
    return (of - v) / of if m["measure"] == "missing" else v / of


def pct(share: float) -> str:
    """A whole percent, but never rounded up to 100% or down to 0%."""
    return f"{share:.1%}" if 0 < share < 0.005 or 0.995 <= share < 1 else f"{share:.0%}"


def a(url: str, label: str) -> str:
    return f'<a href="{esc(url)}">{esc(label)}</a>' if url else esc(label)


def facet(name: str, label: str, values: list[tuple[str, str]], find: bool = False,
          default: list[str] | None = None, totals: dict | None = None) -> str:
    """A filter that picks several values: a button opening a list of checkboxes with counts.
    `default` is what it holds when the URL says nothing; `totals` count rows not yet loaded."""
    attrs = f' data-default="{esc("|".join(default))}"' if default else ""
    box = '<input type="search" class="find" placeholder="Find…" aria-label="Find">' if find else ""
    opts = "".join(
        f'<label><input type="checkbox" value="{esc(v)}"'
        + (f' data-total="{totals[v]}"' if totals and v in totals else "")
        + f'><span>{shown}</span><i></i></label>' for v, shown in values)
    return (f'<details class="facet" data-name="{name}" data-f="{name.split("-", 1)[1]}"{attrs}>'
            f'<summary>{label}<b></b></summary><div class="opts">{box}{opts}</div></details>')


def plain(values) -> list[tuple[str, str]]:
    return [(v, esc(v)) for v in values]


def bar(prefix: str, facets: str, checks: list[tuple[str, str]] = ()) -> str:
    boxes = "".join(f'<label class="check"><input type="checkbox" name="{prefix}-{n}"> {label}</label>'
                    for n, label in checks)
    # On a phone the filters fold behind the Filters button, so the bar stays one line.
    return (f'<div class="bar"><input type="search" name="{prefix}-q" placeholder="Search…" '
            f'aria-label="Search"><button type="button" class="filters" aria-expanded="false">'
            f'Filters</button><span class="count"></span><div class="picks">{facets}{boxes}</div>'
            f'<div class="active"></div><div class="hint" hidden></div></div>')


def grade(tier: str) -> str:
    g = GRADE.get(tier)
    return f'<b class="grade {g}">{g}</b>' if g else ""


def slug_class(v: str) -> str:
    return "s-" + v.lower().replace(" ", "-")


def badge_css() -> str:
    """Badge colours as classes: an inline style on 15,000 rows is half a megabyte."""
    rules = [f".{slug_class(s)}{{{style}}}" for s, style in STATUS_STYLE.items()]
    rules += [f".r{n}{{{style}}}" for n, style in REACH_STYLE.items()]
    rules += [f".grade.{g}{{{style}}}" for g, style in GRADE_STYLE.items()]
    return "\n".join(rules)


def source_rows(sources, measures, juris, portals, last) -> dict[str, list[str]]:
    """Each row's HTML, by the grade letter that decides which file it ships in."""
    find = portal_finder(portals)
    history = defaultdict(list)
    for m in measures:
        history[m["source_id"]].append(m)
    order = {s: i for i, s in enumerate(STATUSES)}
    uses = list(FEASIBILITY)
    rows = sorted(sources, key=lambda r: (order[r["status"]], jurisdiction(r["id"]).count("/"),
                                          juris[jurisdiction(r["id"])]["name"], r["dataset"]))
    out = defaultdict(list)
    for i, r in enumerate(rows):
        where = juris[jurisdiction(r["id"])]["name"]
        use = FEASIBILITY[r["feasibility"]]
        name = "Address points" if is_address_dataset(r) else r["dataset"]
        notes = f'<div class="notes clamp">{esc(r["notes"])}</div>' if r["notes"] else ""

        m = last.get(r["id"])
        share = share_in_osm(m)
        osm = ""
        if share is not None:
            osm = (f'<div class="meter" title="{pct(share)} in OSM"><span style="width:{share:.1%}">'
                   f'</span></div><b>{pct(share)}</b> ')
        osm += f'<span class="muted">{esc(r["coverage"])}</span>' if r["coverage"] else ""
        past = sorted((x for i in [r["id"]] + [w["id"] for w in r["work"]] for x in history[i]),
                      key=lambda x: x["measured_on"], reverse=True)
        if len(past) > 1:
            items = "".join(f'<li><time>{x["measured_on"]}</time> {esc(x["text"])}</li>' for x in past)
            osm += f'<details><summary>{len(past)} measures</summary><ul>{items}</ul></details>'

        tools = "".join(f'<a class="chip" href="{esc(u)}">{esc(l)}</a>' for l, u in tool_pairs(r["tools"]))
        leads = ", ".join(a(f"https://www.openstreetmap.org/user/{u}", u)
                          for u in r["lead"].split(", ") if u)
        licence = esc(r["licence"])
        if r["lwg"] == "self-listed":
            licence += ' <span class="muted">· self-listed on the wiki</span>'
        elif r["lwg"]:
            licence += f' <span class="muted">· LWG {a(r.get("lwg_url", ""), r["lwg"])}</span>'
        p = find(r)
        portal = a(p["portal_url"], portal_label(p["portal_url"])) if p else ""
        g = GRADE.get(r["tier"], UNGRADED)
        copy = ' data-copy="1"' if r["notes"].startswith("Copy of ") else ""

        out[g].append(
            f'<tr data-i="{i}" data-where="{esc(where)}" data-theme="{r["theme"]}" data-use="{use}" '
            f'data-status="{r["status"]}" data-value="{g}"{copy}>'
            f'<td class="name">{a(r["source_url"], name)}{notes}</td>'
            f"<td>{esc(where)}</td><td>{r['theme']}</td>"
            f'<td class="value">{grade(r["tier"])}</td>'
            f'<td data-sort="{uses.index(r["feasibility"])}">{use}</td>'
            f'<td data-sort="{order[r["status"]]}"><span class="badge {slug_class(r["status"])}">'
            f'{r["status"]}</span></td>'
            f'<td class="licence"><div class="clamp">{licence}</div></td>'
            + cell("portal", portal)
            + cell("osm", osm, "" if share is None else f"{share:.4f}")
            + cell("tools", tools) + cell("lead", leads)
            + f'<td class="more nowrap">{r["last_verified"]}</td>'
            f'<td class="more"><code>{esc(r["id"])}</code></td></tr>')
    return out


def cell(cls: str, html: str, sort: str | None = None) -> str:
    """A cell, bare when empty: a third of the rows' cells are, and the bytes add up."""
    if not html:
        return "<td></td>"
    return f'<td class="{cls}"' + (f' data-sort="{sort}"' if sort is not None else "") + f">{html}</td>"


def portal_rows(sources, portals, juris) -> str:
    find = portal_finder(portals)
    catalogued = Counter()
    for r in sources:
        p = find(r)
        if p:
            catalogued[(p["jurisdiction"], p["portal_url"])] += 1
    rows = sorted(portals, key=lambda p: (-int(p["reach"]), -int(p["layers_seen"] or -1),
                                          juris[p["jurisdiction"]]["name"]))
    out = []
    for p in rows:
        j = juris[p["jurisdiction"]]
        tier = TIER_LABEL.get(j["tier"], j["level"])
        reach = int(p["reach"])
        label = portal_label(p["portal_url"])
        layers = f"{int(p['layers_seen']):,}" if p["layers_seen"] else ""
        n = catalogued[(p["jurisdiction"], p["portal_url"])]
        # The datasets page finds a portal's rows by searching its label within the jurisdiction.
        listed = (f'<a href="index.html#s-q={quote(label)}&amp;s-where={quote(j["name"])}'
                  f'&amp;s-value=all">{n:,}</a>'
                  if n else "")
        out.append(
            f'<tr data-tier="{tier}" data-reach="{reach} {p["reach_label"]}" '
            f'data-platform="{p["platform"]}">'
            f'<td class="name">{esc(j["name"])}</td><td class="nowrap">{tier}</td>'
            f'<td data-sort="{reach}"><span class="badge r{reach}">'
            f'{reach} {p["reach_label"]}</span></td>'
            f'<td>{p["platform"]}</td><td class="portal">{a(p["portal_url"], label)}</td>'
            f'<td class="num layers" data-sort="{p["layers_seen"]}">{layers}</td>'
            f'<td class="num listed" data-sort="{n or ""}">{listed}</td>'
            f'<td class="licence"><div class="clamp">{esc(p["licence"])}</div></td>'
            f'<td class="nowrap surveyed">{p["surveyed_on"]}</td>'
            f'<td class="notes-cell"><div class="clamp muted">{esc(p["notes"])}</div></td></tr>')
    return "\n".join(out)


def th(*cols: tuple[str, str]) -> str:
    return "".join(f'<th{" " + attrs if attrs else ""}><button>{label}</button></th>'
                   for label, attrs in cols)


def shell(title: str, here: str, intro: str, body: str) -> str:
    """One page of the site: the shared header with its navigation, then the body."""
    pages = [("index.html", "Datasets"), ("portals.html", "Portals")]
    nav = " · ".join(f'<b aria-current="page">{label}</b>' if href == here else a(href, label)
                     for href, label in pages)
    nav += (f' · <a href="{REPO_URL}/blob/main/report/SUMMARY.md">Summary</a>'
            f' · <a href="{REPO_URL}/blob/main/wiki/Canada_Open_data.wiki">Wiki view</a>'
            f' · <a href="{REPO_URL}/tree/main/catalogue">CSVs</a>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{CSS}{badge_css()}</style>
</head>
<body>
<header>
<h1>Ontario open data for OpenStreetMap</h1>
<nav>{nav}</nav>
{intro}
</header>
{body}
<script>{JS}</script>
</body>
</html>
"""


def html_page(sources, measures, juris, rows) -> str:
    """The datasets page. Its rows are A to C and the ungraded; D and F wait in their files."""
    by_name = lambda codes: sorted({juris[c]["name"] for c in codes})
    present = lambda vocab, key: [v for v in vocab if any(r[key] == v for r in sources)]
    grades = [g for g in list(GRADE.values()) + [UNGRADED] if rows[g]]
    src_bar = bar("s", facet("s-where", "Where", plain(by_name({jurisdiction(r["id"]) for r in sources})),
                             find=True)
                  + facet("s-theme", "Theme", plain(present(THEMES, "theme")), find=True)
                  + facet("s-value", "Value",
                          [(g, (f'<b class="grade {g}">{g}</b> ' if g != UNGRADED else "")
                            + GRADE_MEANS[g]) for g in grades],
                          default=[g for g in grades if g not in DEFERRED],
                          totals={g: len(rows[g]) for g in DEFERRED})
                  + facet("s-use", "Use", plain(FEASIBILITY[f] for f in present(FEASIBILITY, "feasibility")))
                  + facet("s-status", "Status", plain(present(STATUSES, "status"))),
                  [("nocopy", "hide copies"), ("more", "more columns")])
    legend = " ".join(f'{grade(t)} {GRADE_MEANS[g]}' for t, g in GRADE.items())
    deferred = " ".join(f"{g}:rows-{g.lower()}.js" for g in DEFERRED)
    shown = sum(len(rows[g]) for g in grades if g not in DEFERRED)
    intro = f"""<p>Every open data source we know of that could feed OSM in Ontario: what it is good
for, and how much of it is already in OSM. <b>{len(sources)} sources</b> ({summarize(sources)});
{len(measures)} measures. Generated {date.today()}.</p>
<p class="muted grades"><i>Value</i> is what OSM would gain (<a href="{REPO_URL}/blob/main/catalogue/GRADING.md">how it is graded</a>):
{legend}. The page opens on the {shown:,} rows graded A to C or not graded; D and F load when
you pick them. Grades are a first pass and unreviewed.</p>
<p class="muted">A row here is not permission to import. Licence verdicts live on
<a href="https://wiki.openstreetmap.org/wiki/Canada#Open_Data">Canada#Open Data</a> and the OSMF
<a href="{OSMF_PAGE}">OGL Canada and local variants</a> page.</p>"""
    body = f"""<section id="sources" data-table data-total="{len(sources)}" data-deferred="{deferred}">
{src_bar}
<table>
<thead><tr>{th(("Dataset", ""), ("Where", ""), ("Theme", ""), ("Value", ""),
              ("Use", 'data-type="num"'),
              ("Status", 'data-type="num"'), ("Licence", ""), ("Portal", ""),
              ("In OSM", 'data-type="num" class="osm"'),
              ("Tools", ""), ("Lead", ""),
              ("Verified", 'class="more"'), ("Id", 'class="more"'))}</tr></thead>
<tbody>
{chr(10).join(tr for g in grades if g not in DEFERRED for tr in rows[g])}
</tbody>
</table>
</section>"""
    return shell("Ontario open data for OpenStreetMap", "index.html", intro, body)


def deferred_rows(g: str, rows: list[str]) -> str:
    """A script, not JSON for fetch(): a script loads from file:// too."""
    return f"window.ROWS_{g} = {json.dumps(chr(10).join(rows), ensure_ascii=False)};\n"


def portals_page(sources, juris, portals) -> str:
    live = [p for p in portals if p["platform"] != "none-found"]
    munis = {c for c, j in juris.items() if j["tier"]}
    with_portal = {p["jurisdiction"] for p in live} & munis
    portal_bar = bar("p", facet("p-tier", "Tier", plain(["province"] + list(TIER_LABEL.values())))
                     + facet("p-reach", "Reach", plain(f"{g} {REACH[g]}" for g in sorted(REACH, reverse=True)))
                     + facet("p-platform", "Platform", plain(PLATFORMS)))
    intro = f"""<p>Where Ontario publishes open data: the denominator the catalogue grows towards.
{len(with_portal)} of {len(munis)} municipalities have data reachable on a portal or map server.
<i>Reach</i> grades how good the data is likely to be, by how it is published: 4 its own
catalogue, 3 listed in a county catalogue, 2 layers on a map server no catalogue lists, 1 a
viewer only, 0 nothing found. <i>Catalogued</i> counts the datasets taken from each portal;
follow the number to see them.</p>"""
    body = f"""<section id="portals" data-table>
{portal_bar}
<table>
<thead><tr>{th(("Jurisdiction", ""), ("Tier", ""), ("Reach", 'data-type="num"'), ("Platform", ""),
              ("Portal", ""), ("Layers", 'data-type="num" class="num"'),
              ("Catalogued", 'data-type="num" class="num"'), ("Licence", ""),
              ("Surveyed", ""), ("Notes", ""))}</tr></thead>
<tbody>
{portal_rows(sources, portals, juris)}
</tbody>
</table>
</section>"""
    return shell("Portals · Ontario open data for OpenStreetMap", "portals.html", intro, body)


CSS = """
:root{--bg:#fff;--fg:#1d2329;--muted:#5f6b76;--line:#e3e7eb;--zebra:#f8fafb;--head:#eef2f5;
--link:#0b5cad;--hover:#fff8dc;--meter:#3d9a6a;--track:#e3e7eb}
@media (prefers-color-scheme:dark){:root{--bg:#14181c;--fg:#e2e6e9;--muted:#98a3ad;--line:#2b3238;
--zebra:#181d22;--head:#1f252b;--link:#80b8ff;--hover:#2a2a1e;--meter:#5cbf8a;--track:#2b3238}}
*{box-sizing:border-box}
body{margin:0;font:14px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
background:var(--bg);color:var(--fg)}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
header{padding:1.25rem 1.25rem .25rem;max-width:72rem}
header p{margin:.35rem 0}
nav{margin:.35rem 0 .5rem}
h1{font-size:1.4rem;margin:0}
.muted{color:var(--muted)}
.grades .grade{margin-left:.3rem;width:1.3rem;line-height:1.3rem;font-size:.8rem}
.bar{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:center;
padding:.6rem 1.25rem;background:var(--bg);border-bottom:1px solid var(--line)}
.bar .picks{display:contents}
.bar .filters{display:none}
.bar>input[type=search]{min-width:14rem;flex:0 1 20rem}
.bar input[type=search],.bar>button{font:inherit;padding:.3rem .5rem;
border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
.facet{position:relative}
.facet summary{list-style:none;cursor:pointer;padding:.3rem .6rem;border:1px solid var(--line);
border-radius:6px;color:var(--fg);white-space:nowrap;user-select:none}
.facet summary::-webkit-details-marker{display:none}
.facet summary::after{content:" ▾";color:var(--muted)}
.facet summary b{font-weight:600;margin-left:.4rem;color:var(--link)}
.facet[open] summary{background:var(--head)}
.facet .opts{position:absolute;top:calc(100% + .3rem);left:0;z-index:5;min-width:16rem;
max-height:60vh;overflow:auto;padding:.35rem;background:var(--bg);border:1px solid var(--line);
border-radius:8px;box-shadow:0 8px 28px rgba(0,0,0,.18)}
.facet .opts label{display:flex;align-items:center;gap:.5rem;padding:.3rem .45rem;border-radius:5px;
color:var(--fg);white-space:nowrap;cursor:pointer}
.facet .opts label[hidden]{display:none}
.facet .opts label:hover{background:var(--hover)}
.facet .opts label span{flex:1}
.facet .opts label.zero{opacity:.45}
.facet .opts i{font-style:normal;color:var(--muted);font-size:.8rem;font-variant-numeric:tabular-nums}
.facet .opts i.away::after{content:" to load"}
.facet .find{width:100%;margin-bottom:.3rem}
.bar .active{order:10;flex:1 1 100%;display:flex;flex-wrap:wrap;gap:.35rem}
.bar .active:empty{display:none}
.active button{font:inherit;font-size:.8rem;padding:.1rem .55rem;border:1px solid var(--line);
border-radius:999px;background:var(--head);color:var(--fg);cursor:pointer}
.active button:not(.reset)::after{content:" ×";color:var(--muted)}
.active button.reset{background:none;border-color:transparent;color:var(--link)}
.bar .hint{order:11;flex:1 1 100%;font-size:.85rem;color:var(--muted)}
.bar .hint[hidden]{display:none}
.hint button{font:inherit;padding:0;border:0;background:none;color:var(--link);cursor:pointer;
text-decoration:underline}
.bar label{color:var(--muted);white-space:nowrap}
.bar .count{order:9;margin-left:auto;color:var(--muted);font-variant-numeric:tabular-nums}
table{border-collapse:collapse;width:100%}
th,td{padding:.45rem .6rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th:first-child,td:first-child{padding-left:1.25rem}
thead th{position:sticky;top:var(--bar-h,3rem);z-index:1;background:var(--head);
font-size:.8rem;text-transform:uppercase;letter-spacing:.03em;white-space:nowrap}
th button{all:unset;cursor:pointer;color:var(--muted);font-weight:600}
th[aria-sort] button{color:var(--fg)}
th[aria-sort=ascending] button::after{content:" ▲"}
th[aria-sort=descending] button::after{content:" ▼"}
tbody tr.odd{background:var(--zebra)}
tbody tr:hover{background:var(--hover)}
td.name{min-width:14rem;max-width:28rem}
td.name>a{font-weight:600}
.notes{font-size:.85rem;color:var(--muted);margin-top:.15rem}
.clamp{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer}
.clamp.open{display:block}
td .clamp.muted{font-size:.85rem;min-width:20rem;max-width:32rem;overflow-wrap:anywhere}
.badge{display:inline-block;padding:.05rem .5rem;border-radius:999px;color:#1d2329;font-size:.8rem;
white-space:nowrap}
.grade{display:inline-block;width:1.6rem;line-height:1.6rem;border-radius:5px;text-align:center;
font-weight:700;color:#1d2329}
td.value{text-align:center}
td.licence{min-width:10rem;max-width:16rem;font-size:.85rem;overflow-wrap:anywhere}
td.portal{font-size:.85rem;max-width:14rem;overflow-wrap:break-word}
td.osm{min-width:13rem;max-width:22rem;font-size:.85rem}
.meter{display:inline-block;width:4.5rem;height:.5rem;margin-right:.35rem;border-radius:3px;
background:var(--track);vertical-align:middle;overflow:hidden}
.meter span{display:block;height:100%;background:var(--meter)}
details{margin-top:.2rem}summary{cursor:pointer;color:var(--link)}
details ul{margin:.25rem 0;padding-left:1rem}details time{color:var(--muted);font-variant-numeric:tabular-nums}
td.tools{min-width:15rem;max-width:18rem}
.chip{display:inline-block;margin:0 .25rem .25rem 0;padding:.05rem .45rem;border:1px solid var(--line);
border-radius:4px;font-size:.8rem}
.num{text-align:right;font-variant-numeric:tabular-nums}
.nowrap{white-space:nowrap;font-variant-numeric:tabular-nums}
code{font-size:.8rem}
.more{display:none}
table.show-more .more{display:table-cell}

/* A phone gets one card per row: the bar folds to a line, the headings become a strip of
   sort buttons, and each row's cells flow under its name. */
@media (max-width:760px){
header{padding:1rem 1rem .25rem}
.bar{padding:.5rem 1rem;gap:.5rem}
.bar input[type=search]{flex:1 1 8rem;min-width:0;padding:.45rem .6rem}
.bar .filters{display:inline-block;padding:.45rem .7rem}
.bar .filters[aria-expanded=true]{background:var(--head)}
.bar .count{order:0;margin:0;font-size:.85rem}
.bar .picks{display:none;flex:1 1 100%;grid-template-columns:1fr 1fr;gap:.5rem}
.bar.open .picks{display:grid}
.bar .picks .facet[open]{grid-column:1/-1}
.facet summary{display:flex;padding:.45rem .6rem}
.facet summary b{flex:1;overflow:hidden;text-overflow:ellipsis}
.facet .opts{position:static;box-shadow:none;max-height:55vh;margin-top:.3rem;min-width:0}
.facet .opts label{padding:.45rem .45rem;white-space:normal}
.bar .picks label.check{flex-direction:row;align-items:center;gap:.4rem}
table,thead,tbody{display:block}
thead{position:sticky;top:var(--bar-h,3rem);z-index:1;background:var(--head)}
thead tr{display:flex;overflow-x:auto;gap:.35rem;padding:.4rem 1rem;scrollbar-width:none}
thead th,thead th:first-child{position:static;padding:0;border:0;background:none}
thead th.more{display:none}
th button{padding:.3rem .6rem;border:1px solid var(--line);border-radius:999px;background:var(--bg)}
tbody tr{display:block;padding:.65rem 1rem;border-bottom:1px solid var(--line);
content-visibility:auto;contain-intrinsic-size:auto 7rem}
tbody tr[hidden]{display:none}
tbody tr:hover{background:inherit}
td,td:first-child{display:inline-block;padding:0;border:0;margin:.3rem .7rem 0 0;
min-width:0!important;max-width:none!important;vertical-align:middle}
td:empty{display:none}
td.name{display:block;margin:0}
td.name>a{font-size:1rem}
td.licence,td.portal,td.osm,td.tools,td.notes-cell{display:block}
td.licence::before{content:"Licence: "}
td.portal::before{content:"Portal: "}
td.lead::before{content:"Lead: "}
td.layers::before{content:"Layers seen: "}
td.listed::before{content:"Catalogued: "}
td.surveyed::before{content:"Surveyed "}
td::before{color:var(--muted)}
#portals td.name{font-weight:600}
td.licence{display:flex;gap:.3rem}td.licence::before{flex:none}
td .clamp.muted{min-width:0;max-width:none}
table.show-more td.more{display:inline-block}
td .grade{width:1.8rem;line-height:1.8rem}
.chip{padding:.2rem .55rem}
}
"""

JS = """
const params = new URLSearchParams(location.hash.slice(1));
const same = (a, b) => a.length === b.length && a.every(x => b.includes(x));
const fmt = n => n.toLocaleString();
for (const sec of document.querySelectorAll("section[data-table]")) {
  const table = sec.querySelector("table"), tbody = table.tBodies[0];
  const rows = [...tbody.rows];
  const barEl = sec.querySelector(".bar"), search = sec.querySelector(".bar > [type=search]");
  const count = sec.querySelector(".count"), toggle = sec.querySelector(".filters");
  const active = sec.querySelector(".active"), hint = sec.querySelector(".hint");
  const checks = [...sec.querySelectorAll(".picks > label > [type=checkbox]")];
  const more = checks.find(c => c.name.endsWith("-more"));
  const nocopy = checks.find(c => c.name.endsWith("-nocopy"));
  const total = +sec.dataset.total || rows.length;
  // Grades whose rows ship in their own file, and what has arrived.
  const deferred = Object.fromEntries((sec.dataset.deferred || "").split(" ").filter(Boolean)
    .map(s => s.split(":")));
  const loading = {}, done = {};
  const facets = [...sec.querySelectorAll(".facet")].map(el => ({
    el, f: el.dataset.f, name: el.dataset.name,
    label: el.querySelector("summary").firstChild.textContent,
    boxes: [...el.querySelectorAll(".opts label > input")],
    def: el.dataset.default ? el.dataset.default.split("|") : [],
  }));
  const valueFacet = facets.find(fc => fc.f === "value");
  const chosen = fc => fc.boxes.filter(b => b.checked).map(b => b.value);
  new ResizeObserver(() => sec.style.setProperty("--bar-h", barEl.offsetHeight + "px")).observe(barEl);
  // Reading 15,000 rows' text on every keystroke is what made typing lag; read each once.
  const text = new Map();
  const textOf = tr => {
    let t = text.get(tr);
    if (t === undefined) text.set(tr, t = tr.textContent.toLowerCase());
    return t;
  };

  // The URL holds what differs from the defaults: a facet is repeated once per value.
  for (const fc of facets) {
    const vals = !params.has(fc.name) ? fc.def
      : params.getAll(fc.name).includes("all") ? [] : params.getAll(fc.name);
    for (const b of fc.boxes) b.checked = vals.includes(b.value);
  }
  for (const c of checks) c.checked = params.has(c.name);
  if (params.has(search.name)) search.value = params.get(search.name);

  const wanted = () => {
    const vals = valueFacet ? chosen(valueFacet) : [];
    return Object.keys(deferred).filter(g => !vals.length || vals.includes(g));
  };
  const load = g => loading[g] || (loading[g] = new Promise((ok, fail) => {
    const s = document.createElement("script");
    s.src = deferred[g];
    s.onerror = () => { delete loading[g]; fail(new Error(deferred[g])); };
    s.onload = () => {
      const t = document.createElement("tbody");
      t.innerHTML = window["ROWS_" + g];
      delete window["ROWS_" + g];
      rows.push(...t.rows);
      done[g] = true;
      order();
      tbody.append(...rows);
      ok();
    };
    document.head.append(s);
  }));

  let sorting = null;
  const order = () => {
    if (!sorting) return rows.sort((a, b) => a.dataset.i - b.dataset.i);
    const {i, num, dir} = sorting;
    const key = tr => {
      const td = tr.cells[i], v = td.dataset.sort ?? td.textContent.trim();
      return v === "" ? null : num ? +v : v;
    };
    const keys = new Map(rows.map(tr => [tr, key(tr)]));
    rows.sort((a, b) => {
      const x = keys.get(a), y = keys.get(b);
      if (x === null || y === null) return (x === null) - (y === null);
      return dir * (num ? x - y : x.localeCompare(y));
    });
  };

  const apply = () => {
    const words = search.value.toLowerCase().split(/\\s+/).filter(Boolean);
    const sel = facets.map(fc => new Set(chosen(fc)));
    // A row failing only facet k still counts towards k's options: that is what picking one
    // of them would add.
    const tally = facets.map(() => new Map());
    const add = (k, tr) => {
      const v = tr.dataset[facets[k].f];
      tally[k].set(v, (tally[k].get(v) || 0) + 1);
    };
    const hideCopies = nocopy && nocopy.checked;
    let n = 0;
    for (const tr of rows) {
      let fails = 0, miss = -1;
      if (hideCopies && tr.dataset.copy) fails = 9;
      else if (words.length) {
        const t = textOf(tr);
        if (!words.every(w => t.includes(w))) fails = 9;
      }
      for (let k = 0; k < facets.length && fails < 2; k++) {
        if (sel[k].size && !sel[k].has(tr.dataset[facets[k].f])) { fails++; miss = k; }
      }
      if (fails === 0) for (let k = 0; k < facets.length; k++) add(k, tr);
      else if (fails === 1) add(miss, tr);
      const ok = fails === 0;
      if (tr.hidden === ok) tr.hidden = !ok;
      if (ok) tr.classList.toggle("odd", n % 2 === 1);
      n += ok;
    }

    facets.forEach((fc, k) => {
      for (const b of fc.boxes) {
        const label = b.parentElement, i = label.querySelector("i");
        // Not loaded yet: the whole grade's size, before any other filter.
        const away = b.dataset.total && !done[b.value];
        const c = away ? +b.dataset.total : tally[k].get(b.value) || 0;
        i.textContent = fmt(c);
        i.classList.toggle("away", !!away);
        label.classList.toggle("zero", !c);
      }
      const v = chosen(fc);
      fc.el.querySelector("summary b").textContent =
        !v.length ? "" : v.length <= 2 ? v.join(", ") : `${v.slice(0, 2).join(", ")} +${v.length - 2}`;
    });

    const pending = Object.keys(deferred).filter(g => loading[g] && !done[g]);
    count.textContent = pending.length ? `${fmt(n)} … loading ${pending.join(", ")}`
      : n === total ? `${fmt(n)} rows` : `${fmt(n)} of ${fmt(total)}`;

    const changed = facets.filter(fc => !same(chosen(fc), fc.def));
    toggle.textContent = changed.length ? `Filters (${changed.length})` : "Filters";
    active.replaceChildren();
    for (const fc of changed) {
      // A facet with a default is one chip that puts the default back; others, one per value.
      const v = chosen(fc);
      const chips = fc.def.length ? [v.length ? v.join(", ") : "all"] : v;
      for (const x of chips) {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.textContent = `${fc.label}: ${x}`;
        chip.title = fc.def.length ? "Back to the default" : "Remove";
        chip.onclick = () => {
          if (fc.def.length) fc.boxes.forEach(b => (b.checked = fc.def.includes(b.value)));
          else fc.boxes.find(b => b.value === x).checked = false;
          update();
        };
        active.append(chip);
      }
    }
    if (changed.length) {
      const reset = document.createElement("button");
      reset.type = "button";
      reset.className = "reset";
      reset.textContent = "Reset filters";
      reset.onclick = () => {
        for (const fc of facets) fc.boxes.forEach(b => (b.checked = fc.def.includes(b.value)));
        update();
      };
      active.append(reset);
    }

    // Say what the default leaves out, so a search never silently misses a D or F row.
    const out = Object.keys(deferred).filter(g => !wanted().includes(g));
    hint.hidden = !out.length;
    if (out.length) {
      const away = out.reduce((s, g) => s + +valueFacet.boxes.find(b => b.value === g).dataset.total, 0);
      hint.replaceChildren(`${fmt(away)} rows graded ${out.join(" or ")} ${
        words.length ? "not searched" : "hidden"} · `);
      const show = document.createElement("button");
      show.type = "button";
      show.textContent = "show them";
      show.onclick = () => {
        for (const b of valueFacet.boxes) if (out.includes(b.value)) b.checked = true;
        update();
      };
      hint.append(show);
    }
    if (more) table.classList.toggle("show-more", more.checked);
  };

  const save = () => {
    const all = new URLSearchParams(location.hash.slice(1));
    search.value ? all.set(search.name, search.value) : all.delete(search.name);
    for (const c of checks) c.checked ? all.set(c.name, "1") : all.delete(c.name);
    for (const fc of facets) {
      all.delete(fc.name);
      const v = chosen(fc);
      if (same(v, fc.def)) continue;
      if (!v.length) all.set(fc.name, "all");
      else for (const x of v) all.append(fc.name, x);
    }
    history.replaceState(null, "", all.size ? "#" + all : location.pathname);
  };

  let timer;
  const update = () => {
    clearTimeout(timer);
    const need = wanted().filter(g => !done[g]);
    apply();
    save();
    if (need.length) Promise.all(need.map(load)).then(apply, err => {
      count.textContent = `Could not load ${err.message}`;
    });
  };
  search.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(update, 200); });
  search.addEventListener("change", update);
  for (const c of checks) c.addEventListener("change", update);
  for (const fc of facets) {
    for (const b of fc.boxes) b.addEventListener("change", update);
    const find = fc.el.querySelector(".find");
    if (find) find.addEventListener("input", () => {
      const q = find.value.toLowerCase();
      for (const b of fc.boxes) b.parentElement.hidden = !b.value.toLowerCase().includes(q);
    });
    fc.el.addEventListener("toggle", () => {
      if (!fc.el.open) return;
      for (const o of facets) if (o !== fc) o.el.open = false;
      if (find && matchMedia("(hover:hover)").matches) find.focus();
    });
  }
  document.addEventListener("click", ev => {
    for (const fc of facets) if (fc.el.open && !fc.el.contains(ev.target)) fc.el.open = false;
  });
  document.addEventListener("keydown", ev => {
    if (ev.key === "Escape") for (const fc of facets) fc.el.open = false;
  });
  toggle.addEventListener("click", () => {
    toggle.setAttribute("aria-expanded", barEl.classList.toggle("open"));
  });
  update();

  table.tHead.addEventListener("click", ev => {
    const th = ev.target.closest("th");
    if (!th) return;
    const dir = th.getAttribute("aria-sort") === "ascending" ? -1 : 1;
    for (const h of table.tHead.rows[0].cells) h.removeAttribute("aria-sort");
    th.setAttribute("aria-sort", dir === 1 ? "ascending" : "descending");
    sorting = {i: th.cellIndex, num: th.dataset.type === "num", dir};
    order();
    tbody.append(...rows);
    apply();
  });
  tbody.addEventListener("click", ev => {
    const c = ev.target.closest(".clamp");
    if (c && !ev.target.closest("a")) c.classList.toggle("open");
  });
}
"""


def main():
    sources, measures, juris, portals = load()
    last = latest(measures)
    for r in sources:
        r["coverage"] = measure_text(last.get(r["id"]))

    shown = [with_work(r) for r in sources]
    rows = source_rows(shown, measures, juris, portals, last)
    (HERE / "index.html").write_text(html_page(shown, measures, juris, rows), encoding="utf-8")
    for g in DEFERRED:
        (HERE / f"rows-{g.lower()}.js").write_text(deferred_rows(g, rows[g]), encoding="utf-8")
    (HERE / "portals.html").write_text(portals_page(shown, juris, portals), encoding="utf-8")
    WIKI.mkdir(exist_ok=True)
    (WIKI / "Canada_Open_data.wiki").write_text(wiki_page([with_work(r) for r in sources], juris),
                                                encoding="utf-8")
    REPORT.mkdir(exist_ok=True)
    (REPORT / "SUMMARY.md").write_text(summary(sources, measures, juris, last) + "\n"
                                       + coverage(sources, juris, portals), encoding="utf-8")
    print(f"{len(sources)} sources ({summarize(sources)}); {len(measures)} measures")


if __name__ == "__main__":
    main()
