# ontario-osm-data-sources

A catalogue of every open data source usable for OpenStreetMap in Ontario. It records what
each source is, what it is good for (import / conflate / validate / reference / no), and how
far it has been brought into OSM, as dated measurements that build up a history. It grows
until it covers every source and every measure we track.

Views are generated from it. Today there are three:

- [`index.html`](index.html), served at
  [skfd.github.io/ontario-osm-data-sources](https://skfd.github.io/ontario-osm-data-sources/):
  every source as a table you can search, filter and sort, with its licence, the portal it
  was found on, its value as a grade (A–F for tiers 5–1) and its measure history. It opens on
  the rows graded A to C and the ungraded hand-catalogued ones; the D and F rows wait in
  `rows-d.js` and `rows-f.js` until the Value filter asks for them. On a phone each row
  becomes a card. [`portals.html`](portals.html) lists every portal, with how many
  sources the catalogue has taken from each.
- [`wiki/Canada_Open_data.wiki`](wiki/Canada_Open_data.wiki), for
  [Canada/Open data](https://wiki.openstreetmap.org/wiki/Canada/Open_data). The live page is
  still a stub; nothing is pasted until the catalogue has been reviewed.
- [`report/SUMMARY.md`](report/SUMMARY.md): counts by jurisdiction and theme, how fresh the
  measures are, what is being worked on, which measures are still free text, and how much of
  what the portals publish the catalogue has covered.

**Licence verdicts are not made here.** The wiki's `Canada#Open_Data` table and the OSMF
[OGL Canada and local variants](https://osmfoundation.org/wiki/OGL_Canada_and_local_variants)
page own them; the LWG column cites the OSMF page. `wiki/CHECKS.md` lists every dataset where
our address tracker disagrees with that page.

## The catalogue

All of it is in [`catalogue/`](catalogue/); the format is in
[`catalogue/SCHEMA.md`](catalogue/SCHEMA.md).

- `sources.csv`: hand-curated sources, one row each, with a stable id like
  `ca/on/guelph/hydrants`
- `layers/<code>.csv`: every layer the portals publish, graded 1–5 by `GRADING.md` and
  written by `inventory.py --merge`; open ends of that sweep are in
  [`FOLLOW-UPS.md`](FOLLOW-UPS.md)
- `work.csv`: streams of work on a source (an import, a gap-fill, a MapRoulette queue)
- `synced/addresses.csv`: the address datasets the tracker follows, written by `sync.py`
- `measures.csv`: dated measurements, append only
- `portals.csv`: every open-data portal in Ontario, and a `none-found` row for each
  municipality without one: the denominator the catalogue grows towards
- `jurisdictions.csv`: the places an id can sit under, including all 444 municipalities

## Run

```bash
python sync.py --refresh
```

```bash
python survey.py --count
```

```bash
python build.py
```

`sync.py` brings in what the sibling repos know (`../ontario-address-changes`,
`../address-importer-friend`, `../<slug>-address-import`) and the OSMF page. `survey.py
--count` asks every portal in `catalogue/portals.csv` how many datasets it lists and rewrites
`layers_seen` (name jurisdiction codes after it to recount only those). `build.py` reads only
this repo. All need Python 3.11+ and nothing else.
