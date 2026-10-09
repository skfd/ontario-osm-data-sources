"""Generate the OSM wiki data-source tree for Canada / Ontario.

Reads
  - ../ontario-address-changes/datasets/*.toml        address datasets + licence tier
  - ../address-importer-friend/future-work/multi-city/ survey JSON + onboarding queue
  - ../<slug>-address-import                         checkout remotes (tool links)
  - the OSMF "OGL Canada and local variants" page      licence evidence (cached)
  - data/*.csv                                         curated rows (see data/SCHEMA.md)
Writes
  - wiki/*.wiki                                        one file per wiki page
  - wiki/CHECKS.md                                     disagreements to resolve before publishing

    python generate.py [--refresh]
"""

import csv
import json
import re
import subprocess
import sys
import tomllib
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
TRACKER = CODE / "ontario-address-changes" / "datasets"
MULTI = CODE / "address-importer-friend" / "future-work" / "multi-city"
SURVEY = MULTI / "08-survey-results-2026-08-12.json"
SURVEY_DATE = "2026-08-12"
QUEUE = MULTI / "onboarding-queue.md"
CACHE = HERE / "cache" / "osmf-ogl-variants.wikitext"
OSMF_API = ("https://osmfoundation.org/w/api.php?action=parse&prop=wikitext&format=json"
            "&formatversion=2&page=OGL_Canada_and_local_variants")
OSMF_PAGE = "https://osmfoundation.org/wiki/OGL_Canada_and_local_variants"
OUT = HERE / "wiki"

FEASIBILITY = {
    "import": "Import",
    "conflate": "Conflate",
    "validate": "Validate",
    "reference": "Reference",
    "no": "No",
}
STATUS_STYLE = {
    "Completed": "background:#d4f4d4",
    "Ongoing": "background:#e6f6d0",
    "Planned": "background:#fdf6c8",
    "Onboarding": "background:#fdf6c8",
    "Available": "background:#e8eef8",
    "Parked": "background:#f4e0d0",
    "Not usable": "background:#eeeeee",
}

# Where the licence holder on the OSMF page is not the dataset's provider.
OSMF_NAME = {
    "niagara-falls": "Niagara Region",
    "durham": "Oshawa",
    "york": "York Region",
    "peel-region": "Peel",
    "toronto": "Toronto",
}


# ---------------------------------------------------------------- sources

def osmf_wikitext(refresh: bool) -> str:
    if refresh or not CACHE.exists():
        with urllib.request.urlopen(OSMF_API, timeout=60) as r:
            text = json.load(r)["parse"]["wikitext"]
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(text, encoding="utf-8")
    return CACHE.read_text(encoding="utf-8")


def osmf_approvals(text: str) -> list[tuple[str, str]]:
    """(entry text, LWG minutes date) for every 'compatible' bullet."""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("*") and "compatible" in line:
            m = re.search(r"LWG\s+minutes (\d{4}-\d{1,2}-\d{1,2})", line)
            if m:
                out.append((line, m.group(1)))
    return out


def core_name(provider: str) -> str:
    name = re.sub(r"^(The Corporation of the |City of |Town of |County of |United Counties of "
                  r"|Municipality of |Regional Municipality of |District Municipality of )",
                  "", provider)
    return re.sub(r" (County|Region)$", "", name)


def lwg_date(slug: str, provider: str, approvals) -> str | None:
    name = OSMF_NAME.get(slug, core_name(provider))
    pat = re.compile(rf"\b{re.escape(name)}\b(?!ford)")
    for line, when in approvals:
        # match the licence title only, not the URL
        title = re.sub(r"\[\S+", "", line)
        if pat.search(title):
            return when
    return None


def entry_states() -> dict[str, str]:
    """slug -> entry-state cell from the onboarding queue's Done table."""
    states = {}
    in_done = False
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_done = line.strip() == "## Done"
        if in_done and line.startswith("| ") and not line.startswith("| city") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            states[cells[0]] = cells[2]
    return states


def checkout_url(slug: str) -> str | None:
    repo = CODE / f"{slug}-address-import"
    if slug == "toronto":
        repo = CODE / "toronto-2-address-import"
    if not repo.is_dir():
        return None
    r = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"],
                       capture_output=True, text=True)
    url = r.stdout.strip().removesuffix(".git")
    return url or None


def read_curated() -> list[dict]:
    rows = []
    for path in sorted((HERE / "data").glob("*.csv")):
        with path.open(encoding="utf-8", newline="") as f:
            rows.extend(csv.DictReader(f))
    return rows


# ---------------------------------------------------------------- address rows

PLAIN = [
    ("brownfield-complete", "already imported; gap-fill only"),
    ("brownfield-active-community", "local community maps from City data; coordinate first"),
    ("brownfield-active-informal", "a local mapper adds addresses by hand; coordinate first"),
    ("brownfield-active", "local mappers active; coordinate first"),
    ("brownfield-active (organic)", "local mappers active; coordinate first"),
    ("greenfield", "few addresses in OSM yet"),
    ("tracker ingests the wrong layer", "a better address layer exists on the same portal"),
    ("better sibling layer", "a better address layer exists on the same portal"),
]


def plain_state(state: str) -> str:
    s = re.sub(r"\*\*|`|PARKED: ", "", state).strip()
    for key, words in PLAIN:
        if s.startswith(key):
            return words
    return ""


def address_rows(approvals, checks: list[str]) -> list[dict]:
    survey = {s["slug"]: s for s in json.loads(SURVEY.read_text(encoding="utf-8"))}
    states = entry_states()
    rows = []
    for path in sorted(TRACKER.glob("*.toml")):
        slug = path.stem
        t = tomllib.loads(path.read_text(encoding="utf-8"))
        tier = t.get("osm_compatible", "")
        provider = t.get("provider", slug)
        lwg = lwg_date(slug, provider, approvals)
        cleared = bool(lwg) or tier == "green-cc0"

        if tier.startswith("green") and not cleared:
            checks.append(f"- **{slug}**: tracker says `{tier}`, but `{provider}` is not on the "
                          f"OSMF variants page. Listed as *licence unverified*.")
        if slug in OSMF_NAME and lwg and slug not in ("toronto", "york"):
            checks.append(f"- **{slug}**: matched on the OSMF page as `{OSMF_NAME[slug]}`, not as "
                          f"`{provider}` — confirm the dataset is published under that licence.")
        if lwg and not tier.startswith("green"):
            checks.append(f"- **{slug}**: OSMF lists it compatible (LWG {lwg}), tracker still "
                          f"says `{tier}`.")

        s = survey.get(slug)
        if s:
            coverage = f"{s['missing_pct']:.0f}% of {s['active_rows']:,} missing ({SURVEY_DATE})"
            missing = s["missing_pct"]
        else:
            coverage, missing = "", None

        if missing is None:
            feas = "import"
        elif missing < 15:
            feas = "validate"
        elif missing < 50:
            feas = "conflate"
        else:
            feas = "import"

        state = states.get(slug, "")
        if slug == "toronto" or state.startswith("imported"):
            status = "Completed"
        elif "PARKED" in state:
            status = "Parked"
        elif "brownfield" in state:
            status = "Ongoing" if slug == "guelph" else "Onboarding"
        elif state:
            status = "Onboarding"
        elif tier.startswith("red"):
            status = "Not usable"
        elif cleared:
            status = "Available"
        else:
            status = "Parked"

        if tier.startswith("red"):
            licence_note = "licence incompatible"
        elif cleared:
            licence_note = ""
        elif tier == "orange-ccby-waiver":
            licence_note = "CC BY: needs an OSMF waiver"
        elif tier == "yellow-ogl":
            licence_note = "OGL variant: LWG review pending"
        elif tier.startswith("green"):
            licence_note = "licence unverified (not on OSMF list)"
        else:
            licence_note = "no licence review yet"

        note = plain_state(state)
        if status == "Parked" and not state:
            note = ""
        notes = "; ".join(x for x in (licence_note, note) if x)

        tools = []
        url = checkout_url(slug)
        if url:
            tools.append(("import checkout", url))
        if slug == "toronto":
            tools.append(("import page", "https://wiki.openstreetmap.org/wiki/Toronto/Address_Import"))
        if slug == "guelph":
            tools.append(("import page", "https://wiki.openstreetmap.org/wiki/Guelph/Address_Import"))

        rows.append({
            "area": "Ontario",
            "dataset": provider,
            "provider": provider,
            "source_url": t.get("data_url", ""),
            "licence": t.get("license_name", ""),
            "lwg": lwg or ("CC0" if tier == "green-cc0" else ""),
            "tier": "",
            "coverage": coverage,
            "feasibility": feas,
            "status": status,
            "tools": "; ".join(f"{a}|{b}" for a, b in tools),
            "lead": "",
            "last_verified": SURVEY_DATE if s else "",
            "notes": notes,
        })
    return rows


# ---------------------------------------------------------------- wikitext

def ext(url: str, label: str) -> str:
    return f"[{url} {label}]" if url else label


def tools_cell(tools: str) -> str:
    parts = []
    for pair in filter(None, (p.strip() for p in tools.split(";"))):
        label, _, url = pair.partition("|")
        parts.append(ext(url.strip(), label.strip()))
    return "<br>".join(parts)


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
                v = tools_cell(v)
            elif c == "lead":
                v = f"{{{{User|{v}}}}}" if v else ""
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
    "This page is generated from [https://github.com/skfd/ontario-osm-data-sources "
    "ontario-osm-data-sources]. Fix a row there, or edit here and say so on the talk page.\n\n"
    "'''A row here is not permission to import.''' The licence verdict for every portal lives "
    "in [[Canada#Open Data]] and on the OSMF "
    f"[{OSMF_PAGE} OGL Canada and local variants] page; the LWG column only cites it. Every "
    "import still needs a proposal, a community discussion and an [[Import/Catalogue]] entry."
)


def summarize(rows) -> str:
    c = Counter(r["status"] for r in rows)
    return ", ".join(f"{n} {s.lower()}" for s, n in c.most_common())


def page_canada(curated) -> str:
    national = [r for r in curated if r["area"] == "Canada"]
    return f"""{{{{Languages|Canada/Open data}}}}
Open data that can be used for OpenStreetMap in Canada, as a tree: national sources here,
then one page per province, then one page per municipality where there is layer-by-layer detail.

{PREAMBLE}

== Licences ==
Which municipal and provincial licences are compatible is tracked in [[Canada#Open Data]],
backed by the OSMF [{OSMF_PAGE} OGL Canada and local variants] page and
[[Contributors#Canada]] for attribution.

== National sources ==
{table(national, "dataset", ["provider", "licence", "feasibility", "status", "tools", "last_verified", "notes"])}

== By province ==
* '''Ontario''' — [[Ontario/Data sources]]
* Alberta, British Columbia, Manitoba, New Brunswick, Nova Scotia, Québec, Saskatchewan, Yukon —
  no data-source page yet; see the per-province licence tables in [[Canada#Open Data]].

== Use ==
{LEGEND}

[[Category:Canada]]
[[Category:Data sources from Canada]]
"""


def page_ontario(curated, addresses) -> str:
    prov = [r for r in curated if r["area"] == "Ontario"]
    munis = sorted({r["area"] for r in curated} - {"Canada", "Ontario"})
    sections = []
    for m in munis:
        rs = [r for r in curated if r["area"] == m]
        if len(rs) > 12:
            sections.append(f"=== {m} ===\n{len(rs)} layers ({summarize(rs)}) — see "
                            f"'''[[{m}/Data sources]]'''.")
        else:
            sections.append(f"=== {m} ===\n" + table(
                rs, "dataset", ["licence", "coverage", "feasibility", "status", "tools", "lead",
                                "last_verified", "notes"]))
    munis_text = "\n\n".join(sections)
    return f"""Open data that can be used for OpenStreetMap in Ontario. Part of [[Canada/Open data]].

{PREAMBLE}

== Use ==
{LEGEND}

== Provincial sources ==
{table(prov, "dataset", ["provider", "licence", "feasibility", "status", "tools", "last_verified", "notes"])}

== Address points ==
{len(addresses)} municipal and county address-point datasets ({summarize(addresses)}).
''In OSM'' is the share of source addresses with no matching OSM address, measured from a
Geofabrik extract on {SURVEY_DATE}.

{table(addresses, "provider", ["licence", "lwg", "coverage", "feasibility", "status", "tools", "notes"])}

== Other layers, by municipality ==
{munis_text}

[[Category:Ontario]]
[[Category:Data sources from Canada]]
"""


def page_city(area, rows) -> str:
    return f"""Open data from {area} and what it is worth to OpenStreetMap, layer by layer.
Part of [[Ontario/Data sources]].

{PREAMBLE}

''Value'' is a 1–5 score of what OSM would gain.

== Use ==
{LEGEND}

== Layers ==
{table(rows, "dataset", ["licence", "tier", "coverage", "feasibility", "status", "tools", "lead", "last_verified", "notes"])}

[[Category:{area}]]
[[Category:Data sources from Canada]]
"""


def main():
    refresh = "--refresh" in sys.argv
    approvals = osmf_approvals(osmf_wikitext(refresh))
    checks: list[str] = []
    addresses = address_rows(approvals, checks)
    curated = read_curated()

    OUT.mkdir(exist_ok=True)
    (OUT / "Canada_Open_data.wiki").write_text(page_canada(curated), encoding="utf-8")
    (OUT / "Ontario_Data_sources.wiki").write_text(page_ontario(curated, addresses), encoding="utf-8")
    for area in sorted({r["area"] for r in curated} - {"Canada", "Ontario"}):
        rows = [r for r in curated if r["area"] == area]
        if len(rows) > 12:
            (OUT / f"{area}_Data_sources.wiki").write_text(page_city(area, rows), encoding="utf-8")

    (OUT / "CHECKS.md").write_text(
        f"# Resolve before publishing ({date.today()})\n\n"
        "Disagreements between the address tracker and the OSMF variants page.\n\n"
        + ("\n".join(checks) or "None.") + "\n", encoding="utf-8")
    print(f"addresses: {len(addresses)} ({summarize(addresses)}); curated: {len(curated)}; "
          f"checks: {len(checks)}")


if __name__ == "__main__":
    main()
