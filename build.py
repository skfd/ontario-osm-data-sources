"""Render the catalogue into its views. Reads only this repository.

Reads   catalogue/*.csv, catalogue/synced/*.csv  (see catalogue/SCHEMA.md)
Writes  wiki/Canada_Open_data.wiki               the OSM wiki page
        report/SUMMARY.md                        counts, freshness and gaps, for review

    python build.py
"""

from collections import Counter, defaultdict
from datetime import date

from common import (FEASIBILITY, HERE, STATUSES, THEMES, jurisdiction, latest, load,
                    measure_text, tool_pairs)

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
                v = f"{{{{User|{v}}}}}" if v else ""
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
    active = [r for r in sources if r["status"] in ("Ongoing", "Planned", "Onboarding")]
    a_rows = [[r["id"], r["status"], r["lead"] or "", measure_text(last.get(r["id"]))]
              for r in sorted(active, key=lambda r: r["id"])]

    unparsed = [m for m in measures if m["measure"] == "observation"]
    return f"""# Catalogue summary

Generated by `build.py` on {today}. {len(sources)} sources in {len(by_j)} jurisdictions;
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


def main():
    sources, measures, juris = load()
    last = latest(measures)
    for r in sources:
        r["coverage"] = measure_text(last.get(r["id"]))

    WIKI.mkdir(exist_ok=True)
    (WIKI / "Canada_Open_data.wiki").write_text(wiki_page(sources, juris), encoding="utf-8")
    REPORT.mkdir(exist_ok=True)
    (REPORT / "SUMMARY.md").write_text(summary(sources, measures, juris, last), encoding="utf-8")
    print(f"{len(sources)} sources ({summarize(sources)}); {len(measures)} measures")


if __name__ == "__main__":
    main()
