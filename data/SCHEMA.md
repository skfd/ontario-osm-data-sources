# Curated row schema (`data/*.csv`)

UTF-8, comma-separated, RFC 4180 quoting, header row exactly:

    area,dataset,provider,source_url,licence,tier,coverage,feasibility,status,tools,lead,last_verified,notes

| column | meaning |
|---|---|
| `area` | Page the row lands on: `Canada`, `Ontario`, `Guelph`, `Toronto`, `Oakville`, … |
| `dataset` | Human name of the layer, as the publisher calls it |
| `provider` | Publisher (City of Guelph, Statistics Canada, …) |
| `source_url` | The live endpoint or dataset page — the thing a mapper would open |
| `licence` | Licence name as published. Never a verdict — the verdict lives on the wiki's `Canada#Open_Data` table / OSMF variants page |
| `tier` | Optional 1–5 value-to-OSM score (Guelph audit rubric). Blank elsewhere |
| `coverage` | What OSM already has, with a number and the date measured, e.g. `3,384 of 3,524 missing (2026-10-09)` |
| `feasibility` | One of `import`, `conflate`, `validate`, `reference`, `no` |
| `status` | One of `Completed`, `Ongoing`, `Planned`, `Onboarding`, `Parked`, `Available`, `Not usable` |
| `tools` | `label|url` pairs separated by `; ` — tile layer, gaps page, beholder, MapRoulette, Osmose, import page |
| `lead` | OSM username leading work on it, blank if none |
| `last_verified` | `YYYY-MM-DD` the row's facts were last checked |
| `notes` | One short sentence; no wiki markup |

Feasibility meanings: **import** = bulk upload after a proposal; **conflate** = merge
attributes/geometry into existing OSM features; **validate** = gap list / task queue
(MapRoulette, gaps page) for hand edits; **reference** = tile layer only; **no** = not useful
or not licensed.
