# ontario-osm-data-sources

One tree of every open data source usable for OpenStreetMap in Ontario, with what each is
good for (import / conflate / validate / reference / no) and how far work on it has got.
It is generated here and pasted into the OSM wiki:

| file | wiki page |
|---|---|
| `wiki/Canada_Open_data.wiki` | [Canada/Open data](https://wiki.openstreetmap.org/wiki/Canada/Open_data) — the root; today a 555-byte stub the Canada page already calls "a list of them" |
| `wiki/Ontario_Data_sources.wiki` | `Ontario/Data sources` — provincial sources, all 53 tracked address-point datasets, other layers per municipality |
| `wiki/Guelph_Data_sources.wiki` | `Guelph/Data sources` — every Guelph layer, from the [audit](../guelph-osm-import-audit) |

A municipality gets its own page once it has more than 12 rows; until then its rows sit on
the Ontario page.

**Licence verdicts are not made here.** The wiki's `Canada#Open_Data` table and the OSMF
[OGL Canada and local variants](https://osmfoundation.org/wiki/OGL_Canada_and_local_variants)
page own them; the LWG column cites the OSMF page. `wiki/CHECKS.md` lists every dataset where
our address tracker disagrees with that page. Resolve it before pasting.

## Inputs

- `../ontario-address-changes/datasets/*.toml` — address datasets, licence name, tracker tier
- `../address-importer-friend/future-work/multi-city/` — coverage survey (2026-08-12) and
  onboarding queue (entry state per city)
- `../<slug>-address-import` — checkout remotes, for tool links
- `data/*.csv` — curated rows for everything else; format in `data/SCHEMA.md`
- the OSMF variants page, cached in `cache/` (`--refresh` refetches it)

## Run

```bash
python generate.py --refresh
```

Needs Python 3.11+ and nothing else. The sibling repos above must be checked out next to
this one.
