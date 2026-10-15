# Follow-ups

Work the 2026-10-14 portal sweep (`inventory.py`, `catalogue/layers/`) left open.

## Not swept

- **Provincial catalogues.** `data.ontario.ca` (CKAN, ~2,960 datasets) and Ontario GeoHub
  (~244) were left out as not municipal. `inventory.py` skips `ca/on`; drop it from `SKIP`
  to list them.
- **Erin.** Its open-data page is a list of downloads with no API (`platform` `custom`), so
  `inventory.py` cannot read it. Grade it by hand.
- **Guelph's map server.** Only the Hub (`explore.guelph.ca`) was swept; the 74 hand-audited
  layers came from `gismaps.guelph.ca/hosting/rest/services` too, but `portals.csv` has no
  reach-2 row for it. Add the row and run `python inventory.py ca/on/guelph`.

## Decisions pending

- **Address duplicates.** 57 of the 78 tier-5 address rows are in municipalities whose
  address points the tracker already follows (`synced/addresses.csv`), at another URL, and
  several batches hold two copies of one layer (Lennox and Addington 26,613 twice, Simcoe
  190,432 twice, Niagara `address-points` and `address-points-2`). Mark them as copies at
  tier 2 under GRADING.md's duplicate rule, or add a column saying which source they copy.
- **Themes.** Graders filed railways under `roads` and census layers under `planning` or
  `community`, unevenly. Add `rail` and `statistics` to `THEMES`, or settle on one existing
  theme for each.
- **Licence emails.** 179 layers graded 4 or 5 are `Not usable` only for want of a licence.
- **OSM coverage.** No grade was checked against OSM; buildings in particular sit at 4
  whether OSM already has them or not.
