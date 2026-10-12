# Catalogue schema

UTF-8 CSV, RFC 4180 quoting. `build.py` validates all of it and refuses to run on a bad row.

| file | written by | one row per |
|---|---|---|
| `sources.csv` | hand | data source: a dataset as its publisher publishes it |
| `work.csv` | hand | stream of work bringing one source into OSM |
| `synced/addresses.csv` | `sync.py` — never edit | address dataset in `../ontario-address-changes` |
| `measures.csv` | hand, and `sync.py` appends | measurement of one source or stream on one day |
| `jurisdictions.csv` | hand | country, province or municipality an id can sit under |

## Ids

Every source has a lowercase path id: jurisdiction code, then a slug for the dataset.

    ca/odb                          national
    ca/on/geohub                    provincial
    ca/on/guelph/hydrants           municipal
    ca/on/guelph/addresses          a municipality's address-point dataset

A stream of work hangs off its source: `ca/on/toronto/addresses/import`.

`<municipality>/addresses` is the address dataset the tracker follows; the jurisdiction code
is the tracker slug. Ids never change once given, because measures point at them.

## `sources.csv`

    id,theme,dataset,provider,source_url,licence,tier,feasibility,status,tools,lead,last_verified,notes

| column | meaning |
|---|---|
| `id` | See above. Its jurisdiction must be in `jurisdictions.csv` |
| `theme` | One of the themes below |
| `dataset` | Name of the layer as the publisher calls it |
| `provider` | Publisher (City of Guelph, Statistics Canada, …) |
| `source_url` | The live endpoint or dataset page: what a mapper would open |
| `licence` | Licence name as published. Never a verdict; the verdict lives on the wiki's `Canada#Open_Data` table and the OSMF variants page |
| `tier` | Optional 1–5 score of what OSM would gain (Guelph audit rubric) |
| `feasibility` | `import`, `conflate`, `validate`, `reference` or `no` |
| `status` | `Completed`, `Ongoing`, `Planned`, `Onboarding`, `Available`, `Parked` or `Not usable` |
| `tools` | `label\|url` pairs separated by `; `: tile layer, gaps page, MapRoulette, import page |
| `lead` | OSM username leading the work, blank if none. Once a source has rows in `work.csv`, leads go there |
| `last_verified` | `YYYY-MM-DD` the row's facts were last checked |
| `notes` | One short sentence, no wiki markup |

**Adding to a synced row.** A hand row whose id is in `synced/addresses.csv` does not make a
second source. Its non-empty cells replace the synced ones and its tools go after the synced
tools. Fill only what the tracker cannot know: `lead`, extra `tools`, `notes`.

**A source is the dataset, not the work.** An import, a later gap-fill and a MapRoulette queue
on the same layer are one source with three rows in `work.csv`, not three sources. A source
with a single unnamed stream may keep its `lead` and work tools on its own row until a second
stream appears.

**Themes:** addresses, buildings, roads, traffic, parking, cycling, pedestrian, trails,
transit, parks, recreation, trees, water, amenities, emergency, health, education, community,
poi, heritage, boundaries, planning, elections, waste, environment, topography, imagery,
catalogue. Add one here and in `common.py` together.

## `work.csv`

    id,source_id,kind,status,lead,started,ended,tools,notes

| column | meaning |
|---|---|
| `id` | `<source_id>/<slug>` |
| `source_id` | The source being worked on |
| `kind` | `import`, `gap-fill`, `maintenance`, `conflation`, `task-queue` or `survey` |
| `status` | `Completed`, `Ongoing`, `Planned` or `Parked` |
| `lead` | OSM username |
| `started`, `ended` | `YYYY-MM-DD`, blank if unknown |
| `tools` | As in `sources.csv`: import page, change tracker, MapRoulette challenge |
| `notes` | One short sentence |

The wiki folds a source's streams into its row: tools after the source's, leads of the active
streams, and a short "import completed 2026-05-28, maintenance ongoing" in the notes.

## `measures.csv`

    source_id,measured_on,measure,value,of,unit,method,text

Append only: a new measurement is a new line. Never edit an old one, because the history is
the point. The wiki shows each source's latest line.

| column | meaning |
|---|---|
| `source_id` | A source id, or a work id for what the work itself did |
| `measured_on` | `YYYY-MM-DD` of the OSM data measured (the extract date, not the day you ran it) |
| `measure` | `missing`: `value` of `of` source features have no OSM match. `matched`: `value` of `of` are in OSM. `added`: `value` features a stream of work added. `observation`: a fact with no numbers to track yet. `note`: why there is no measure (out of scope, not compared) |
| `value`, `of` | Numbers, no commas. Blank for `observation` and `note` |
| `unit` | What is counted: addresses, parks, km, … |
| `method` | How it was measured. Next month's number is only comparable to this one if this matches. `audit` = a hand audit; `portfolio-survey` = the 2026-08-12 address survey |
| `text` | The measurement as a sentence, shown on the wiki |

## `portals.csv`

    jurisdiction,portal_url,platform,reach,reach_label,api_url,licence,layers_seen,surveyed_on,notes

The denominator: every place Ontario publishes open data, so the catalogue can say how much of
it has been looked at. Every municipality in `jurisdictions.csv` gets at least one row, a
`none-found` row when the survey found nothing. A portal's datasets are candidates for new
sources. One row per `(jurisdiction, portal_url)`.

| column | meaning |
|---|---|
| `jurisdiction` | Code from `jurisdictions.csv` |
| `portal_url` | The portal's home page. Blank for `none-found` |
| `platform` | `arcgis-hub`, `arcgis-rest`, `ckan`, `socrata`, `opendatasoft`, `custom` or `none-found` |
| `reach`, `reach_label` | How good the data is likely to be, from how it is published (below): a number and its label |
| `api_url` | The catalogue API (below). Blank for `custom` without one, and for `none-found` |
| `licence` | Licence name as the portal publishes it, `None published`, or blank for `none-found`. Never a verdict |
| `layers_seen` | Datasets the API listed on `surveyed_on`, by the method below. Blank if not counted |
| `surveyed_on` | `YYYY-MM-DD` the row was last checked by hand |
| `notes` | A sentence or two. For `none-found`, what was checked |

**Reach.** How good a municipality's data is likely to be, judged only by how it is published.
The licence plays no part; it has its own column.

| reach | label | the row is | platform |
|---|---|---|---|
| 4 | `own` | the jurisdiction's own open-data catalogue | a catalogue platform |
| 3 | `catalogued` | its own datasets listed in a county or consortium catalogue | a catalogue platform |
| 2 | `on-server` | queryable layers on a public map server, its own or the county's, that no catalogue lists | `arcgis-rest` |
| 1 | `viewer` | a map viewer only: it can be looked at, not downloaded | `none-found` |
| 0 | `none` | nothing found | `none-found` |

A catalogue is a site whose purpose is publishing datasets: a Hub, CKAN, Socrata, OpenDataSoft,
or a page listing downloads (`custom`). A dashboard or story-map hub is not one. A Hub and the
ArcGIS server behind it are one row (the Hub); a server holding much more than its Hub lists
gets a reach-2 row of its own. A CKAN site and a Hub run side by side are two rows. A
municipality is graded by its best row.

**Shared portals.** A county or consortium catalogue or server that holds a member's own layers
gives the member a row too, with the same URL, blank `layers_seen` and `shared portal of <code>`
in notes, so its layers are counted once, under the owner.

**`api_url` and `layers_seen` by platform.** Next survey's count is comparable only if it is
taken the same way.

| platform | `api_url` | `layers_seen` |
|---|---|---|
| `arcgis-hub` | `<site>/api/search/v1/collections/dataset/items` | `numberMatched` of `?limit=1` |
| `ckan` | `<base>/api/3/action/package_search` | `result.count` of `?rows=0` (all datasets, not only spatial) |
| `opendatasoft` | `<base>/api/explore/v2.1/catalog/datasets` | `total_count` of `?limit=0` |
| `socrata` | `https://api.us.socrata.com/api/catalog/v1?domains=<domain>` | `resultSetSize` of `&limit=0` |
| `arcgis-rest` | the services root, ending `/rest/services` | layers in every service, folders walked one level |
| `custom` | blank, or its JSON API | blank unless an API gives a count |

A Hub site with no `dataset` collection uses `collections/all` (or its own datasets
collection). A Hub that shows other organisations' items too (the four Waterloo-region hubs
share one catalogue) adds `?orgid=<its org>`, so each item is counted once. An ArcGIS
Enterprise Sites page has no Hub API; its `api_url` is the portal's `sharing/rest/search` over
the site's group, and the count is `total`. An `arcgis-rest` count includes the layers behind
map viewers, so it runs higher than a Hub's count of curated datasets: compare within a platform.

`python survey.py --count` takes these counts again and rewrites `layers_seen` only, never
`surveyed_on`. It skips rows with no `api_url`, `shared portal of` rows, and rows whose notes
say `not counted`. An `arcgis-rest` service is counted once by name: its FeatureServer if it
has one, else its MapServer, counting layers without `subLayerIds`; an ImageServer alone counts
1, other service types and secured folders or services count 0. A row whose request fails
keeps its old count.

## `jurisdictions.csv`

    code,name,level,tier

`level` is `country`, `province` or `municipal`. `tier` is `upper`, `single` or `lower` for the
444 municipalities of the Ontario list, blank otherwise (`west-parry-sound` is a GIS
consortium, not a municipality). The name is used as a wiki section heading, so no two rows
share one.

A new code is the slug of the name: lowercase, accents and punctuation dropped, spaces and
slashes as hyphens (`St. Catharines` → `st-catharines`, `Admaston/Bromley` →
`admaston-bromley`). Codes that came from the address tracker keep its slug even where it
reads oddly: `niagara-falls` is Niagara Region, `waterloo` the City of Waterloo. When a slug is
taken, the newcomer gets a qualifier: `niagara-falls-city`, `waterloo-region`, `renfrew-town`,
`hamilton-township`, `essex-county`.
