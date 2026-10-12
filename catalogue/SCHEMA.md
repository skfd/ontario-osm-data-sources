# Catalogue schema

UTF-8 CSV, RFC 4180 quoting. `build.py` validates all of it and refuses to run on a bad row.

| file | written by | one row per |
|---|---|---|
| `sources.csv` | hand | data source (or a stream of work on one) |
| `synced/addresses.csv` | `sync.py` — never edit | address dataset in `../ontario-address-changes` |
| `measures.csv` | hand, and `sync.py` appends | measurement of one source on one day |
| `jurisdictions.csv` | hand | country, province or municipality an id can sit under |

## Ids

Every source has a lowercase path id: jurisdiction code, then a slug for the dataset.

    ca/odb                          national
    ca/on/geohub                    provincial
    ca/on/guelph/hydrants           municipal
    ca/on/guelph/addresses          a municipality's address-point dataset

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
| `lead` | OSM username leading the work, blank if none |
| `last_verified` | `YYYY-MM-DD` the row's facts were last checked |
| `notes` | One short sentence, no wiki markup |

**Adding to a synced row.** A hand row whose id is in `synced/addresses.csv` does not make a
second source. Its non-empty cells replace the synced ones and its tools go after the synced
tools. Fill only what the tracker cannot know: `lead`, extra `tools`, `notes`.

**Themes:** addresses, buildings, roads, traffic, parking, cycling, pedestrian, trails,
transit, parks, recreation, trees, water, amenities, emergency, health, education, community,
poi, heritage, boundaries, planning, elections, waste, environment, topography, imagery,
catalogue. Add one here and in `common.py` together.

## `measures.csv`

    source_id,measured_on,measure,value,of,unit,method,text

Append only: a new measurement is a new line. Never edit an old one, because the history is
the point. The wiki shows each source's latest line.

| column | meaning |
|---|---|
| `source_id` | A source id |
| `measured_on` | `YYYY-MM-DD` of the OSM data measured (the extract date, not the day you ran it) |
| `measure` | `missing`: `value` of `of` source features have no OSM match. `matched`: `value` of `of` are in OSM. `observation`: a fact with no numbers to track yet. `note`: why there is no measure (out of scope, not compared) |
| `value`, `of` | Numbers, no commas. Blank for `observation` and `note` |
| `unit` | What is counted: addresses, parks, km, … |
| `method` | How it was measured. Next month's number is only comparable to this one if this matches. `audit` = a hand audit; `portfolio-survey` = the 2026-08-12 address survey |
| `text` | The measurement as a sentence, shown on the wiki |

## `jurisdictions.csv`

    code,name,level

`level` is `country`, `province` or `municipal`. The name is used as a wiki section heading.
