# Follow-ups

Work the portal sweeps (`inventory.py`, `catalogue/layers/`) left open. The first sweep
(2026-10-14) covered the municipalities; the second (2026-10-15) added the province, 21
ministries, agencies, school boards and health units, the 36 conservation authorities and
Conservation Ontario, Guelph's map server, Erin, and everything each Hub lists beyond its
`dataset` collection.

## Not swept

- **Download catalogues with no API.** These are `custom` rows, so `inventory.py` cannot read
  them; grade them by hand into `catalogue/layers/<code>.csv`:
  - Grand River's GRIN, 62 layers (`data.grandriver.ca/metadata-api/v2/downloads` is JSON)
  - RVCA's JKAN, 22 datasets (`rvcagis.github.io/jkan/datasets.json`); most are also layers
    on `gis.rvca.ca`, which was swept
  - the Geological Survey's GeologyOntario site, whose Hub answers with 0 items
  - Metrolinx's open-data page beyond the four GTFS and shapefile rows in `sources.csv`
- **School boards and health units.** Only 9 of 72 boards and 2 of 34 units were found, by
  searching ArcGIS Online by name. Left out on purpose: Watson & Associates' org
  (`f8lLPHShq1QkdT5J`, hosting layers for five boards), an org mixing three health units
  (`IrGlfUdWCDMTtRnk`), and BWDSB's classroom org.
- **Conservation authorities with only viewers.** Kawartha, St. Clair, Lower Trent, Mississippi
  Valley, South Nation, Raisin Region and Crowe Valley have layers on Conservation Ontario's org
  but no portal of their own. Long Point, Catfish Creek, Kettle
  Creek, Mattagami and Sault Ste. Marie Region publish nothing but viewers or PDFs. Essex
  Region's vector folder on the county server needs a token, and its imagery folder
  (`gisimagery.countyofessex.ca/arcgis/rest/services/ERCA`) has no row.
- **Servers shared with municipalities.** Ganaraska's `maps2.grca.on.ca` also holds folders for
  Clarington, Durham, Northumberland, and Peterborough city and county. Their layers were swept
  under Ganaraska. Those municipalities may want `shared portal of
  ca/on/ganaraska-region-conservation-authority` rows.
- **Grading cut short, then redone.** A usage limit stopped the second sweep's grading after
  43 of 148 batches. The rest were graded in a second run with the same prompt, and every batch
  passes `--check`.

## Decisions pending

- **Conservation authorities consolidate on 2027-02-01.** The 36 authorities become 9
  regional ones; Long Point, Grand River, Catfish Creek and Kettle Creek become the Eastern
  Lake Erie Regional Conservation Authority. The CA codes in `jurisdictions.csv`, and the ids
  under them, will need new parents or redirects.
- **Ministries as agencies.** The four ministries sit at level `agency`. Mines (under
  `ontario-geological-survey`) and Energy (`ministry-of-energy-and-mines`) have been one
  ministry since 2025 but have two codes. Trans Canada Trail is a national charity coded under
  `ca/on`.
- **Providers guessed.** Most data.ontario.ca packages name no organization, so graders
  inferred the ministry from the content. In Conservation Ontario's shared org, the authority
  was read from service names, owners or map extents; where none fitted, the provider is
  `Conservation Ontario`.
- **Staff layers in public.** NVCA's shared server exposes `*_Staff` services for its tenants,
  including a layer named "CONFIDENTIAL DO NOT PRINT - MPAC Parcel 2009" (North Bay-Mattawa)
  and "Parcels (Owners)" (Conservation Sudbury). They are graded 1; the authorities may want to
  know.
- **Copies not provable.** 6,279 layers are marked copies in all, by `inventory.py --copies`
  or by the graders. Some likely copies nobody could prove remain at their own grade:
  - Sault Ste. Marie's two address layers (33,316 and 33,354)
  - Simcoe's municipal address layers beside the county's
  - Middlesex's county address points on a second service
  - school boards' and health units' republished municipal address points, boundaries and
    school points, whose notes often name the original without an id
  - the ORN road-net-element beside the ORN composite
  
  Mark them by hand (`Copy of <id>.`) if they are copies.
- **Themes left fuzzy.** The list grew to 42 (2026-10-15). Graders still found no clean home
  for these:
  - fences and barriers (topography or amenities)
  - source-water protection zones (environment)
  - cartographic masks and label layers (maps)
  - Survey123 forms and staff records (statistics or community)
- **Licence emails.** Layers of use with no open licence have the status `No licence`;
  `report/SUMMARY.md` "Licences to ask for" lists those graded 3 to 5 by jurisdiction. The
  provincial bodies add some good ones: the Heritage Trust's plaques (terms forbid
  redistribution), AGCO's cannabis stores, and MTO's carpool lots and rest areas on its AGOL
  server.
- **OSM coverage.** No grade was checked against OSM. In particular:
  - buildings sit at 4 whether OSM already has them or not
  - CanVec imports may already carry much of the province's water, wooded areas and
    geographic names
  - Trans Canada Trail syncs with OSM (`push_to_osm_flag`), so its gain may be smaller than
    its grade
