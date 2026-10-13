"""Render the catalogue into its views. Reads only this repository.

Reads   catalogue/*.csv, catalogue/synced/*.csv  (see catalogue/SCHEMA.md)
Writes  index.html                               the catalogue as tables, for GitHub Pages
        wiki/Canada_Open_data.wiki               the OSM wiki page
        report/SUMMARY.md                        counts, freshness, gaps and coverage, for review

    python build.py
"""

from collections import Counter, defaultdict
from datetime import date
from html import escape as esc

from common import (FEASIBILITY, HERE, PLATFORMS, REACH, STATUSES, THEMES, jurisdiction,
                    latest, load, measure_text, tool_pairs)

WIKI = HERE / "wiki"
REPORT = HERE / "report"
REPO_URL = "https://github.com/skfd/ontario-osm-data-sources"
OSMF_PAGE = "https://osmfoundation.org/wiki/OGL_Canada_and_local_variants"
SURVEY_DATE = "2026-08-12"

STATUS_STYLE = {
    "Completed": "background:#d4f4d4",
    "Ongoing": "background:#e6f6d0",
    "Planned": "background:#fdf6c8",
    "Onboarding": "background:#fdf6c8",
    "Available": "background:#e8eef8",
    "Parked": "background:#f4e0d0",
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
    for code, rs in sorted(by_muni.items(), key=lambda kv: -len(kv[1])):
        scored = any(r["tier"] for r in rs)
        intro = (f"{len(rs)} layers ({summarize(rs)}). ''Value'' is a 1–5 score of what OSM "
                 "would gain.\n\n" if scored else "")
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


def select(name: str, label: str, values: list[str]) -> str:
    opts = "".join(f'<option value="{esc(v)}">{esc(v)}</option>' for v in values)
    return (f'<label>{label} <select name="{name}" data-f="{name.split("-", 1)[1]}">'
            f'<option value="">all</option>{opts}</select></label>')


def bar(prefix: str, selects: str, more: bool = False) -> str:
    toggle = (f'<label class="check"><input type="checkbox" name="{prefix}-more"> more columns</label>'
              if more else "")
    return (f'<div class="bar"><input type="search" name="{prefix}-q" placeholder="Search…" '
            f'aria-label="Search">{selects}{toggle}<span class="count"></span></div>')


def source_rows(sources, measures, juris, last) -> str:
    history = defaultdict(list)
    for m in measures:
        history[m["source_id"]].append(m)
    order = {s: i for i, s in enumerate(STATUSES)}
    uses = list(FEASIBILITY)
    rows = sorted(sources, key=lambda r: (order[r["status"]], jurisdiction(r["id"]).count("/"),
                                          juris[jurisdiction(r["id"])]["name"], r["dataset"]))
    out = []
    for r in rows:
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

        out.append(
            f'<tr data-where="{esc(where)}" data-theme="{r["theme"]}" data-use="{use}" '
            f'data-status="{r["status"]}">'
            f'<td class="name">{a(r["source_url"], name)}{notes}</td>'
            f"<td>{esc(where)}</td><td>{r['theme']}</td>"
            f'<td data-sort="{uses.index(r["feasibility"])}">{use}</td>'
            f'<td data-sort="{order[r["status"]]}"><span class="badge" '
            f'style="{STATUS_STYLE[r["status"]]}">{r["status"]}</span></td>'
            f'<td class="osm" data-sort="{"" if share is None else f"{share:.4f}"}">{osm}</td>'
            f'<td class="tools">{tools}</td><td>{leads}</td>'
            f'<td class="more">{licence}</td>'
            f'<td class="more nowrap">{r["last_verified"]}</td>'
            f'<td class="more"><code>{esc(r["id"])}</code></td></tr>')
    return "\n".join(out)


def portal_rows(portals, juris) -> str:
    rows = sorted(portals, key=lambda p: (-int(p["reach"]), -int(p["layers_seen"] or -1),
                                          juris[p["jurisdiction"]]["name"]))
    out = []
    for p in rows:
        j = juris[p["jurisdiction"]]
        tier = TIER_LABEL.get(j["tier"], j["level"])
        reach = int(p["reach"])
        host = p["portal_url"].split("//", 1)[-1].split("/", 1)[0]
        layers = f"{int(p['layers_seen']):,}" if p["layers_seen"] else ""
        out.append(
            f'<tr data-tier="{tier}" data-reach="{reach} {p["reach_label"]}" '
            f'data-platform="{p["platform"]}">'
            f'<td class="name">{esc(j["name"])}</td><td class="nowrap">{tier}</td>'
            f'<td data-sort="{reach}"><span class="badge" style="{REACH_STYLE[reach]}">'
            f'{reach} {p["reach_label"]}</span></td>'
            f'<td>{p["platform"]}</td><td>{a(p["portal_url"], host)}</td>'
            f'<td class="num" data-sort="{p["layers_seen"]}">{layers}</td>'
            f'<td class="licence">{esc(p["licence"])}</td><td class="nowrap">{p["surveyed_on"]}</td>'
            f'<td><div class="clamp muted">{esc(p["notes"])}</div></td></tr>')
    return "\n".join(out)


def th(*cols: tuple[str, str]) -> str:
    return "".join(f'<th{" " + attrs if attrs else ""}><button>{label}</button></th>'
                   for label, attrs in cols)


def html_page(sources, measures, juris, portals, last) -> str:
    by_name = lambda codes: sorted({juris[c]["name"] for c in codes})
    present = lambda vocab, key: [v for v in vocab if any(r[key] == v for r in sources)]
    live = [p for p in portals if p["platform"] != "none-found"]
    munis = {c for c, j in juris.items() if j["tier"]}
    with_portal = {p["jurisdiction"] for p in live} & munis
    src_bar = bar("s", select("s-where", "Where", by_name({jurisdiction(r["id"]) for r in sources}))
                  + select("s-theme", "Theme", present(THEMES, "theme"))
                  + select("s-use", "Use", [FEASIBILITY[f] for f in present(FEASIBILITY, "feasibility")])
                  + select("s-status", "Status", present(STATUSES, "status")), more=True)
    portal_bar = bar("p", select("p-tier", "Tier", ["province"] + list(TIER_LABEL.values()))
                     + select("p-reach", "Reach", [f"{g} {REACH[g]}" for g in sorted(REACH, reverse=True)])
                     + select("p-platform", "Platform", PLATFORMS))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ontario open data for OpenStreetMap</title>
<style>{CSS}</style>
</head>
<body>
<header>
<h1>Ontario open data for OpenStreetMap</h1>
<p>Every open data source we know of that could feed OSM in Ontario: what it is good for, and
how much of it is already in OSM. <b>{len(sources)} sources</b> ({summarize(sources)});
{len(measures)} measures. Generated {date.today()} from the
<a href="{REPO_URL}/tree/main/catalogue">catalogue CSVs</a>;
<a href="{REPO_URL}/blob/main/report/SUMMARY.md">summary</a> ·
<a href="{REPO_URL}/blob/main/wiki/Canada_Open_data.wiki">wiki view</a> ·
<a href="#portals">portals</a>.</p>
<p class="muted">A row here is not permission to import. Licence verdicts live on
<a href="https://wiki.openstreetmap.org/wiki/Canada#Open_Data">Canada#Open Data</a> and the OSMF
<a href="{OSMF_PAGE}">OGL Canada and local variants</a> page.</p>
</header>

<section id="sources" data-table>
{src_bar}
<table>
<thead><tr>{th(("Dataset", ""), ("Where", ""), ("Theme", ""), ("Use", 'data-type="num"'),
              ("Status", 'data-type="num"'), ("In OSM", 'data-type="num" class="osm"'),
              ("Tools", ""), ("Lead", ""), ("Licence", 'class="more"'),
              ("Verified", 'class="more"'), ("Id", 'class="more"'))}</tr></thead>
<tbody>
{source_rows(sources, measures, juris, last)}
</tbody>
</table>
</section>

<section id="portals" data-table>
<h2>Portals</h2>
<p class="muted">Where Ontario publishes open data: the denominator the catalogue grows towards.
{len(with_portal)} of {len(munis)} municipalities have data reachable on a portal or map server.
<i>Reach</i> grades how good the data is likely to be, by how it is published: 4 its own
catalogue, 3 listed in a county catalogue, 2 layers on a map server no catalogue lists, 1 a
viewer only, 0 nothing found.</p>
{portal_bar}
<table>
<thead><tr>{th(("Jurisdiction", ""), ("Tier", ""), ("Reach", 'data-type="num"'), ("Platform", ""),
              ("Portal", ""), ("Layers", 'data-type="num" class="num"'), ("Licence", ""),
              ("Surveyed", ""), ("Notes", ""))}</tr></thead>
<tbody>
{portal_rows(portals, juris)}
</tbody>
</table>
</section>
<script>{JS}</script>
</body>
</html>
"""


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
h1{font-size:1.4rem;margin:0}
h2{font-size:1.15rem;margin:2.5rem 1.25rem .25rem}
section>p{margin:.25rem 1.25rem .5rem;max-width:72rem}
.muted{color:var(--muted)}
.bar{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:center;
padding:.6rem 1.25rem;background:var(--bg);border-bottom:1px solid var(--line)}
.bar input[type=search]{min-width:14rem;flex:0 1 20rem}
.bar input[type=search],.bar select{font:inherit;padding:.3rem .5rem;border:1px solid var(--line);
border-radius:6px;background:var(--bg);color:var(--fg)}
.bar label{color:var(--muted);white-space:nowrap}
.bar .count{margin-left:auto;color:var(--muted);font-variant-numeric:tabular-nums}
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
td.licence{min-width:12rem}
code{font-size:.8rem}
.more{display:none}
table.show-more .more{display:table-cell}
"""

JS = """
const params = new URLSearchParams(location.hash.slice(1));
for (const sec of document.querySelectorAll("section[data-table]")) {
  const table = sec.querySelector("table"), tbody = table.tBodies[0], rows = [...tbody.rows];
  const controls = [...sec.querySelectorAll(".bar [name]")], count = sec.querySelector(".count");
  const barEl = sec.querySelector(".bar");
  new ResizeObserver(() => sec.style.setProperty("--bar-h", barEl.offsetHeight + "px")).observe(barEl);

  const apply = () => {
    const words = sec.querySelector("[type=search]").value.toLowerCase().split(/\\s+/).filter(Boolean);
    const picks = controls.filter(c => c.dataset.f && c.value);
    let n = 0;
    for (const tr of rows) {
      let ok = picks.every(c => tr.dataset[c.dataset.f] === c.value);
      if (ok && words.length) {
        const text = tr.textContent.toLowerCase();
        ok = words.every(w => text.includes(w));
      }
      tr.hidden = !ok;
      if (ok) tr.classList.toggle("odd", n % 2 === 1);
      n += ok;
    }
    count.textContent = n === rows.length ? `${n} rows` : `${n} of ${rows.length} rows`;
    const more = sec.querySelector("[type=checkbox]");
    if (more) table.classList.toggle("show-more", more.checked);
  };
  const save = () => {
    const all = new URLSearchParams(location.hash.slice(1));
    for (const c of controls) {
      const v = c.type === "checkbox" ? (c.checked ? "1" : "") : c.value;
      v ? all.set(c.name, v) : all.delete(c.name);
    }
    history.replaceState(null, "", all.size ? "#" + all : location.pathname);
  };
  for (const c of controls) {
    if (params.has(c.name)) c.type === "checkbox" ? (c.checked = true) : (c.value = params.get(c.name));
    c.addEventListener("input", () => { apply(); save(); });
  }
  apply();

  table.tHead.addEventListener("click", ev => {
    const th = ev.target.closest("th");
    if (!th) return;
    const i = th.cellIndex, num = th.dataset.type === "num";
    const dir = th.getAttribute("aria-sort") === "ascending" ? -1 : 1;
    for (const h of table.tHead.rows[0].cells) h.removeAttribute("aria-sort");
    th.setAttribute("aria-sort", dir === 1 ? "ascending" : "descending");
    const key = tr => {
      const td = tr.cells[i], v = td.dataset.sort ?? td.textContent.trim();
      return v === "" ? null : num ? +v : v;
    };
    rows.sort((a, b) => {
      const x = key(a), y = key(b);
      if (x === null || y === null) return (x === null) - (y === null);
      return dir * (num ? x - y : x.localeCompare(y));
    });
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

    (HERE / "index.html").write_text(html_page([with_work(r) for r in sources], measures, juris,
                                               portals, last), encoding="utf-8")
    WIKI.mkdir(exist_ok=True)
    (WIKI / "Canada_Open_data.wiki").write_text(wiki_page([with_work(r) for r in sources], juris),
                                                encoding="utf-8")
    REPORT.mkdir(exist_ok=True)
    (REPORT / "SUMMARY.md").write_text(summary(sources, measures, juris, last) + "\n"
                                       + coverage(sources, juris, portals), encoding="utf-8")
    print(f"{len(sources)} sources ({summarize(sources)}); {len(measures)} measures")


if __name__ == "__main__":
    main()
