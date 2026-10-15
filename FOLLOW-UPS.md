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

- **Copies not provable.** `inventory.py --copies` marked 3,485 layers. Some likely copies it
  cannot prove remain at their own grade: Sault Ste. Marie's two address layers (33,316 and
  33,354), Simcoe's municipal address layers beside the county's, Middlesex's county address
  points on a second service. Mark them by hand (`Copy of <id>.`) if they are.
- **Themes.** Graders filed railways under `roads` and census layers under `planning` or
  `community`, unevenly. Add `rail` and `statistics` to `THEMES`, or settle on one existing
  theme for each.
- **Licence emails.** Layers of use with no open licence now have the status `No licence`;
  `report/SUMMARY.md` "Licences to ask for" lists the 813 graded 3 to 5 by jurisdiction.
- **OSM coverage.** No grade was checked against OSM; buildings in particular sit at 4
  whether OSM already has them or not.
