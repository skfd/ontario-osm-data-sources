# Grading a layer

How a layer from `inventory.py` gets its `theme`, `tier`, `feasibility`, `status` and `notes`.

The sweep's goal is completeness: every layer every portal publishes gets a row, so nothing
worth having goes unseen. A grade is a first sort for a person to review, not a verdict, and a
low grade is never a reason to leave a row out. The examples below come from the Guelph audit,
only so that the scale means the same everywhere.

## Tier: what OSM would gain, 1 to 5

Score the gain to OSM, not the quality of the data. A clean, complete layer of something OSM
does not map scores 1; a messy layer of something OSM lacks can score 4.

| tier | means | Guelph examples |
|---|---|---|
| 5 | A large, mappable gap that a whole community would want filled, ready to use: address points, building footprints for an area OSM lacks. Rare; most municipalities have none | |
| 4 | Physical, mappable features or attributes OSM is usually missing in bulk: official names, signed networks, facility rosters with good positions | Bike Facilities, Park Boundary (official names), Sports Fields, Community Gardens, Stormwater Ponds, AED Locations, Truck Routes, Trees, Heritage Register, Stop Signs, Veteran Street Names, Park Parking Lots, neighbourhood areas |
| 3 | Useful for a gaps list or a one-off conflation, or a real gain on part of the layer; or a reference OSM mappers would actually check against | Trails (surface, winter service), Restrooms, Child Care, Hydrants, Bus Stops, GTFS, Wards, Watercourse names, Schools, Fire Stations, aerial imagery, school crossings, crossovers |
| 2 | Small, or OSM usually has it already, or the authority for it is elsewhere | Sidewalks (OSM traces them), Laneways, Street Intersections, Bus Routes (GTFS is the authority), Golf Course points, City Facilities, City Boundary, Neighbourhood Groups already in OSM, directories that churn |
| 1 | Not something OSM maps: legal, administrative, operational or statistical | Parcels, Registered Plans, Zoning, Building Permits, Polling Subdivisions, Polling Stations, collection-day zones, mowing routes, contours, groundwater readings, enforcement deployments, planned (not built) works |

Rules of thumb from the audit:

- **Legal and administrative areas score 1**, except boundaries OSM does carry: municipal,
  ward (`boundary=political`), and named neighbourhoods or communities (`place=*` areas), 3–4.
- **Planned, proposed, candidate or temporary** features score 1: OSM maps what is on the ground.
- **Operational records** (inspections, work orders, maintenance zones, schedules, service
  requests, counts and statistics) score 1, even when they carry geometry.
- **Engineering networks** (water mains, sewers, storm pipes, valves, manholes) score 1–2:
  underground, and OSM rarely wants them. Above-ground utility objects people see (hydrants,
  street lights, poles) score 2–3.
- **Directories of services** that churn (social services, health programmes) score 2.
- **Duplicates**: a layer that republishes another in the same jurisdiction (a "view", a
  "public" copy, a yearly snapshot) gets the lower tier and says which layer it copies.
  Historic yearly copies score 1 unless the history itself is the value.
- **Tables with no geometry** score 1 unless they can be joined to a mappable layer by an id
  the note names.
- **Imagery** (ImageServer, orthophoto) scores 3 when it is recent and licensed, else 2.
- **Names are the usual gain.** Official names of parks, trails, creeks, facilities and
  streets are why most tier-4 rows are tier 4. Say so in the note when that is the case.

## Feasibility

| value | when |
|---|---|
| `import` | Bulk upload after an import proposal is the right route (boundaries, address points, footprints where OSM is empty) |
| `conflate` | Merge names, attributes or missing features into what OSM already has |
| `validate` | A gap list or task queue worked by hand: OSM has most of it, or positions need survey |
| `reference` | Something to look at or check against; nothing is uploaded |
| `no` | Not useful for OSM. Every tier-1 row is `no`; a tier-2 row can be |

## Status

Only two values come out of a sweep:

- `Not usable` when feasibility is `no`, or when the licence column is blank, `None published`,
  `none published`, or plainly not an open licence (a copyright notice, "all rights reserved",
  "for information only"). A layer that has value but no licence keeps its tier and says
  "but no licence" in the note, as Guelph's Stop Signs does.
- `Available` otherwise.

The licence column is the publisher's words, never a verdict on OSM compatibility. Whether a
licence is LWG-cleared is not the grader's call and does not change the status.

## Theme

One of the themes in `SCHEMA.md`. Pick by what the features are, not by the department that
publishes them: a park's washroom is `amenities`, its sports field `recreation`, the park
itself `parks`.

## Provider

The publisher as they name themselves: `City of Barrie`, `Town of Oakville`, `County of
Simcoe`. When a municipal portal republishes someone else's layer (a conservation authority's
floodplain, the province's wetlands, a school board's schools), the provider is that body.

## Notes

One short sentence, under 200 characters, no wiki markup, no line breaks. Say why the layer
scores what it scores, with the fact that decides it: what the gain is, or why there is none.

- Good: "Official names for 140 parks, which OSM mostly has as unnamed leisure=park areas."
- Good: "Zoning is a legal designation, not ground truth."
- Good: "A 2019 snapshot of Trails; the live layer is ca/on/barrie/trails."
- Bad: "Parks layer." (says what it is, not what it is worth)
- Bad: "56% missing from OSM." (unless you measured it; never invent a number)

Use the record count, the field names and the edit date. A layer last edited ten years ago, or
with 0 records, says so in the note. Do not claim what OSM has unless you checked; "OSM
usually has these" is a fair judgement, "OSM has 41 of them" is a measurement.
