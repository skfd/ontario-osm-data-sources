# ontario-osm-data-sources

One list of every open data source usable for OpenStreetMap in Ontario, with what each is
good for (import / conflate / validate / reference / no) and how far work on it has got.
It is generated here as one wiki page, `wiki/Canada_Open_data.wiki`, for
[Canada/Open data](https://wiki.openstreetmap.org/wiki/Canada/Open_data). Today that page is a
555-byte stub, but the Canada page already links to it as the list of municipal datasets.
Sections: national sources; then for Ontario, provincial sources, all tracked address-point
datasets, and every Guelph and Toronto layer.

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
