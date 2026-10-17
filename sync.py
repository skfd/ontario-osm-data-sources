"""Bring in what other repos and pages know. Needs the sibling checkouts and, with --refresh,
the network; build.py needs neither.

Reads
  - ../ontario-address-changes/datasets/*.toml        address datasets + licence tier
  - ../address-importer-friend/future-work/multi-city/ survey JSON + onboarding queue
  - ../<slug>-address-import                         checkout remotes (tool links)
  - the OSMF "OGL Canada and local variants" page      licence evidence (cached)
Writes
  - catalogue/synced/addresses.csv                     one row per tracked address dataset
  - catalogue/measures.csv                             appends survey measures not yet logged
  - wiki/CHECKS.md                                     tracker vs OSMF disagreements

    python sync.py [--refresh]
"""

import json
import re
import subprocess
import sys
import tomllib
import urllib.request

from common import (CODE_DIR, HERE, MEASURE_COLS, MEASURES, SYNCED, SYNCED_COLS, read_csv,
                    write_csv)

TRACKER = CODE_DIR / "ontario-address-changes" / "datasets"
MULTI = CODE_DIR / "address-importer-friend" / "future-work" / "multi-city"
SURVEY = MULTI / "08-survey-results-2026-08-12.json"
SURVEY_DATE = "2026-08-12"
QUEUE = MULTI / "onboarding-queue.md"
CACHE = HERE / "cache" / "osmf-ogl-variants.wikitext"
OSMF_API = ("https://osmfoundation.org/w/api.php?action=parse&prop=wikitext&format=json"
            "&formatversion=2&page=OGL_Canada_and_local_variants")
CHECKS = HERE / "wiki" / "CHECKS.md"

# Where the licence holder on the OSMF page is not the dataset's provider.
OSMF_NAME = {
    "york": "York Region",
    "peel-region": "Peel",
    "toronto": "Toronto",
}

# Tracker datasets that are not a municipality's one address-point layer at <code>/addresses: a
# second layer beside it, a slug that is not the jurisdiction's code, or a place with no code.
# A layer the portal sweep already listed keeps its id there, so the synced row adds to that row
# rather than listing the layer twice, and no slug becomes a jurisdiction.
SOURCE_ID = {
    "blue-mountains": "ca/on/the-blue-mountains/addresses",
    "vaughan-ng911": "ca/on/vaughan/address-cov-address-cov",
    "grey-assigned-addresses": "ca/on/grey/service-parcellabels-assigned-address-points",
    # Gorham and Ware are unorganized townships; LRCA publishes them on NVCA's server.
    "gorham-ware": "ca/on/nottawasaga-valley-conservation-authority/"
                   "lrca-municipal-gorham-ware-house-numbers",
}

# Municipalities that granted OSM explicit permission, recorded on the wiki Contributors page.
AUTHORIZED = {
    "kitchener": "https://wiki.openstreetmap.org/wiki/Waterloo_region/Kitchener_authorization",
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
    repo = CODE_DIR / f"{slug}-address-import"
    if slug == "toronto":
        repo = CODE_DIR / "toronto-2-address-import"
    if not repo.is_dir():
        return None
    r = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"],
                       capture_output=True, text=True)
    url = r.stdout.strip().removesuffix(".git")
    return url or None


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


def address_rows(approvals, checks: list[str], measures: list[dict]) -> list[dict]:
    survey = {s["slug"]: s for s in json.loads(SURVEY.read_text(encoding="utf-8"))}
    states = entry_states()
    rows = []
    for path in sorted(TRACKER.glob("*.toml")):
        slug = path.stem
        sid = SOURCE_ID.get(slug, f"ca/on/{slug}/addresses")
        t = tomllib.loads(path.read_text(encoding="utf-8"))
        tier = t.get("osm_compatible", "")
        provider = t.get("provider", slug)
        lwg = lwg_date(slug, provider, approvals)
        indirect = bool(lwg) and slug in OSMF_NAME and slug not in ("toronto", "york")
        cleared = (bool(lwg) and not indirect) or tier in ("green-cc0", "green-self") or slug in AUTHORIZED

        if tier.startswith("green") and not cleared and not indirect:  # green-self is cleared
            checks.append(f"- **{slug}**: tracker says `{tier}`, but `{provider}` is not on the "
                          f"OSMF variants page. Listed as *licence unverified*.")
        if slug in OSMF_NAME and lwg and slug not in ("toronto", "york"):
            checks.append(f"- **{slug}**: matched on the OSMF page as `{OSMF_NAME[slug]}`, not as "
                          f"`{provider}` — confirm the dataset is published under that licence.")
        if lwg and not tier.startswith("green"):
            checks.append(f"- **{slug}**: OSMF lists it compatible (LWG {lwg}), tracker still "
                          f"says `{tier}`.")

        s = survey.get(slug)
        missing = s["missing_pct"] if s else None
        if s:
            measures.append({
                "source_id": sid, "measured_on": SURVEY_DATE, "measure": "missing",
                "value": str(round(s["missing_pct"] / 100 * s["active_rows"])),
                "of": str(s["active_rows"]), "unit": "addresses", "method": "portfolio-survey",
                "text": f"{s['missing_pct']:.0f}% of {s['active_rows']:,} missing",
            })

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
        elif slug in AUTHORIZED and not lwg:
            licence_note = "explicit OSM permission from the municipality"
        elif cleared:
            licence_note = ""
        elif tier == "orange-ccby-waiver":
            licence_note = "CC BY: needs an OSMF waiver"
        elif tier == "yellow-ogl":
            licence_note = "OGL variant: LWG review pending"
        elif indirect:
            licence_note = f"licence matched via {OSMF_NAME[slug]}; confirm it covers this dataset"
        elif tier.startswith("green"):
            licence_note = "licence unverified (not on OSMF list)"
        elif tier == "yellow-review":
            licence_note = "custom licence: needs LWG review"
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
        if slug == "guelph":
            tools.append(("import page", "https://wiki.openstreetmap.org/wiki/Guelph/Address_Import"))

        rows.append({
            "id": sid,
            "theme": "addresses",
            "dataset": provider,
            "provider": provider,
            "source_url": t.get("data_url", ""),
            "licence": t.get("license_name", ""),
            "tracker_tier": tier,
            "lwg": lwg or ("CC0" if tier == "green-cc0" else "")
                   or ("self-listed" if tier == "green-self" else "")
                   or ("permission" if slug in AUTHORIZED else ""),
            "lwg_url": "" if lwg else AUTHORIZED.get(slug, ""),
            "feasibility": feas,
            "status": status,
            "tools": "; ".join(f"{a}|{b}" for a, b in tools),
            "last_verified": SURVEY_DATE if s else "",
            "notes": notes,
        })
    return rows


def main():
    refresh = "--refresh" in sys.argv
    approvals = osmf_approvals(osmf_wikitext(refresh))
    checks: list[str] = []
    found: list[dict] = []
    rows = address_rows(approvals, checks, found)
    write_csv(SYNCED, SYNCED_COLS, rows)

    logged = read_csv(MEASURES)
    key = lambda m: (m["source_id"], m["measured_on"], m["measure"], m["method"])
    have = {key(m) for m in logged}
    new = [m for m in found if key(m) not in have]
    write_csv(MEASURES, MEASURE_COLS, logged + new)

    CHECKS.parent.mkdir(exist_ok=True)
    CHECKS.write_text(
        "# Resolve before publishing\n\n"
        "Disagreements between the address tracker and the OSMF variants page.\n\n"
        + ("\n".join(checks) or "None.") + "\n", encoding="utf-8")
    print(f"synced {len(rows)} address datasets; {len(new)} new measures; checks: {len(checks)}")


if __name__ == "__main__":
    main()
