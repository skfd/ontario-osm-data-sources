# Follow-ups

Work the portal sweeps (`inventory.py`, `catalogue/layers/`) left open. The first sweep
(2026-10-14) covered the municipalities; the second (2026-10-15) added the province, 21
ministries, agencies, school boards and health units, the 36 conservation authorities and
Conservation Ontario, Guelph's map server, Erin, and everything each Hub lists beyond its
`dataset` collection. The third (2026-10-16) read GRIN and RVCA's JKAN through new `custom`
readers, swept Essex County's imagery server, added OGSEarth's and Metrolinx's remaining
downloads as hand rows, and repaired the copy marks (below). The fourth (2026-10-30) listed the
54 ArcGIS Online org roots the Ontario Hubs sit on, and opened Nova Scotia.

## Ungraded

- **The org roots behind the Hubs (listed 2026-10-30).** 15,399 layers on 54 roots in 51
  jurisdictions wait in 156 batches (`cache/inventory/chunks/`), none graded: a third carry
  view, public or dashboard in their names and about 1,000 report zero records, so many will be
  copies or empty. Grading was held for a go-ahead because of the size. Mississauga (1,757),
  the province's two orgs (2,452), Dufferin, Oakville and Brampton are the largest.
- **Nova Scotia (swept 2026-10-30).** Its batches are cut with the above; grade them first,
  they are the smaller set.

## Nova Scotia (surveyed 2026-10-30)

Every one of the 49 municipal units has a portal row; three agents checked each unit's site
bottom-up after a top-down pass over the Socrata, Hub and ArcGIS Online search APIs. The
province publishes through a Socrata catalogue (every asset under the Nova Scotia Open
Government Licence) and NSGI's two map servers; four departments and the Government of Nova
Scotia org serve layers from ArcGIS Online with no licence stated. Only Halifax (Open
Government Licence - Halifax) and Cumberland (ODbL-1.0 on some items) name a licence
municipally. Open ends:

- **Two shared GIS bodies are associations:** the Eastern District Planning Commission (six
  members, 55 services) and the Annapolis Valley Local Information Utility (Annapolis Royal,
  Middleton, Berwick). Argyle owns the org it shares with the District of Yarmouth, run by one
  technician under the key `yabdpc`; a Yarmouth-Argyle-Barrington planning commission may be the
  real owner. Chester's server carries members' layers by suffix (_TOMB, _MODL, _TOB, _TOL) and
  17 layers suffixed _LC, probably Lunenburg County, with no body found.
- **Boundary-only layers.** The five Pictou-area towns appear on the county's org only in the
  county's `Town_Boundary` layer, so they got none-found rows (the Ganaraska rule). Lunenburg,
  Bridgewater and Amherst kept thin shared rows because the host names the layer for the town
  (`_TOL`, `_TOB`, `Amherst_Water`), as Adelaide Metcalfe's did.
- **Empty Hubs at reach 4.** Truro's Hub lists six PDFs and Pictou County's one page; both got
  the platform's reach, and their layers sit on the org roots. Barrington's Hub has 0 items
  and no row.
- **Not read:** Stewiacke's `Stewiacke_OpenDataLicence` PDF on its Hub (recorded as `None
  published`); clarksharbour.com answers 403 to scripts; Queens may have a viewer behind a
  login; middleton.ca does not answer. Guysborough and St. Mary's are not on the EDPC org,
  though the top-down pass assumed they were. Six of CBRM's 14 server folders want a token.
- **The address tracker is Ontario-only**, so Nova Scotia's civic address layers (the province's
  NSCAF on Socrata and NSGI, EDPC's and Argyle's county points) have no `/addresses` synced
  rows and no measures. Onboarding them is `../ontario-address-changes`' call.

## Not swept

- **GeologyOntario.** Both Hubs still list 0 datasets (the French one lists 10 site pages);
  the search app behind `www.geologyontario.mines.gov.on.ca` queries a keyed Elasticsearch API.
  OGSEarth's 38 downloads all have rows: 25 were swept already (13 of them under `ca/on`, from
  the province's CKAN, not under `ontario-geological-survey`), and 13 are new hand rows in
  `sources.csv`.
- **School boards and health units (swept 2026-10-24).** Every one of the province's 72 boards
  and 29 units (the 2025 mergers brought 34 down) has a portal row. Boards: 19 publish layers of
  their own, 14 only on another body's server (Watson & Associates Economists' org, coded as an
  `association`, or a busing consortium's), 35 have a school locator only, 4 nothing. Units: 6
  on their own org, 8 through their municipality's portal, Renfrew only on Southeast's org, 1
  viewer, 13 nothing. No board or unit licenses any layer; 43 of the 1,148 new layers reach
  tier 3 (school rosters, approved wards, HDSB's surveyed school grounds), none higher.
  Not reachable: the Sudbury Student Services Consortium (`oY8XdPA3KnPpc0c8`) and
  Windsor-Essex's health unit list public items whose services all need a token;
  Hamilton-Wentworth Catholic's and five units' orgs are private. Classroom orgs (student story maps)
  are named in each board's notes and not swept. Layers of pupil records turned up on public
  servers; they are kept out by `PERSONAL_FIELDS` in `inventory.py` and listed nowhere here.
  Worth a look in review: Watson's ward-review layers, where the existing wards of six
  municipalities are tier 3 on the assumption that no new wards were adopted for 2026.
- **Conservation authorities with only viewers.** Kawartha, St. Clair, Lower Trent, Mississippi
  Valley, South Nation, Raisin Region and Crowe Valley have layers on Conservation Ontario's org
  but no portal of their own. Long Point, Catfish Creek, Kettle
  Creek, Mattagami and Sault Ste. Marie Region publish nothing but viewers or PDFs. Their
  layers on the shared org are credited to the right authority by service-name prefix. Essex
  Region's vector folder on the county server needs a token.
- **Server folders named for a municipality, left without a row.** On Ganaraska's
  `maps2.grca.on.ca`, the Durham, Northumberland_County and PTBO_City folders hold only the
  authorities' own floodplain and SWP layers, so those municipalities get no shared row;
  Clarington's folder has building footprints whose authorship nothing states, and gave
  Clarington a shared row (reach 2, up from viewer) on that alone. On Essex's imagery server
  the seven municipal folders are the county's orthophotos clipped to each town (same 10 cm
  pixels, inside the county extent): no municipal rows.
- **Grading cut short, then redone.** A usage limit stopped the second sweep's grading after
  43 of 148 batches. The rest were graded in a second run with the same prompt, and every batch
  passes `--check`.

## Decisions pending

- **Hub portals are swept through their catalogue only (measured 2026-10-22).** `from_hub`
  reads the Hub's search, so a service the org publishes without cataloguing it is never seen.
  Essex County's org (`services6.arcgis.com/baycHE2iKJaT7Upn`) lists 288 services at its REST
  root against about 209 Hub items, and the missing ones include Leamington's live civic
  address points (`SDEAddressPts/FeatureServer/3`, 11,424 points) and `Parcels_CIVIC` (edited
  2026-08). It was found through a note in OpenAddresses' `lasalle.json`, not by the sweep.
  Measured for every org: 97 AGOL org roots appear in `catalogue/layers/`, 57 of them never
  listed as an `arcgis-rest` portal. Their roots hold 11,300 services. Filtering the names for
  address words and dropping what the catalogue or the tracker already has leaves Leamington as
  the only new jurisdiction; the rest are alternate views of tracked layers (Whitby's five
  `For_Apps` versions, Frontenac's `NF_View`), census household layers, and Survey123 forms.
  An ArcGIS Online search by name for the tracker's 165 gap municipalities (under 5% of the
  National Address Register's locations) found nothing else Ontarian: the hits were US
  namesakes (Brighton MI, Marathon WI) or tracked county layers.
  **Decision:** whether the catalogue should hold REST-only services at all. For: they are
  publicly served and sometimes the only copy (Leamington). Against: no item, so no
  `licenseInfo`, and the Hub is the publisher's own statement of what it releases; 11,300 names
  of mostly staff and survey layers would swamp the grading. A middle path is a cheap
  name-only pass over each Hub's org roots, run with the quarterly re-probe, that reports
  uncatalogued services matching a theme's words here rather than adding rows. Probe script
  used for the measurement: list each root and its folders, keyword-match service names,
  subtract catalogued and tracked service paths: `rootcheck.py`. Another case from the board
  and unit sweep: Peel's Hub sits on `services6.arcgis.com/ONZht79c8QWuX759` (321 services),
  whose six public `PHDZ_*` health data-zone services the Hub does not list.
  **Decided 2026-10-30: yes, the catalogue holds them.** A publicly served layer is a candidate
  source whether or not its publisher catalogued it. Work to follow: give each of the 57 org
  roots an `arcgis-rest` row of its own (reach 2, under the Hub's jurisdiction), sweep them with
  `inventory.py`, let `--copies` take the alternate views, and grade the rest.

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
- **Copy marks repaired (2026-10-16).** `copies()` took any first word after "Copy of" as
  the original, so prose ("Copy of the county's layer") and stray punctuation ("Copy of
  <id>;") counted as marks, and 50 originals were demoted to copies of themselves or of "the".
  Those 50 have their graded tier back; notes naming an id became marks and dropped to tier 2;
  139 naming none now read "A copy of" and keep their grade. 6,269 layers are marked copies.
  Worth a look in review: the rows whose tier moved in commit `5b29458`.
- **Copies still not provable.** Left at their own grade:
  - Simcoe: New Tecumseth's public address points (15% fewer than the county's, 4 fields) and
    Orillia's (`addresses-sc-addresspoints`, county field names but empty ADDRESSID)
  - Halton Catholic DSB's 193,636 Halton addresses: Halton Region has no portal row to name
    (`maps.halton.ca` still answers 503)
  - municipal-boundary layers of Simcoe County DSB (22), Simcoe Muskoka health unit (35) and
    Dufferin-Peel CDSB (4), which match no layer's count
  
  Proved not to be copies: the ORN road-net-element (no names; the composite joins them),
  TDSB's ward-attributed schools, and three merged address layers of TVDSB and WDG Public
  Health that were wrongly marked.
- **Middlesex's tracker URL is stale.** `ca/on/middlesex/addresses` follows
  MiddlesexCountyAddressPoints, a 2023 snapshot (31,571 points); the live county layer is
  `middlesex/middlesex-county-address-points` (34,308), marked as its copy here. The fix
  belongs in `../ontario-address-changes`, whose TODO §2 has it (2026-10-16) along with West
  Parry Sound's dead endpoint, Elgin's frozen layer, Tecumseh and Grey.
- **The tracker took in the sweep's address layers (2026-10-16); synced 2026-10-17.**
  `../ontario-address-changes` onboarded 24 of them as datasets (licence now gates only
  publishing) and re-pointed waterloo and dufferin. `sync.py` now maps the slugs that are not
  `<code>/addresses` (`SOURCE_ID`): `blue-mountains` -> `the-blue-mountains/addresses`, and the
  second layers `vaughan-ng911`, `grey-assigned-addresses` and LRCA's `gorham-ware` take the id
  the sweep already gave the layer, so the synced row adds to that row. `--copies` then marked
  19 swept rows as copies of the newly tracked sources; it now skips tracked rows and treats
  another sublayer of the same service as another layer (Grey's ParcelLabels 2/3/4).
  Blue Mountains' row sits under grey, so it was marked by hand.
- **L&A's township address views skip the county's redaction (2026-10-16).** The county's
  `L_and_A_County_Civic_Address_Point_(Public)` view filters out `SUBUNITTYPE = 'Public Redact'`
  and `'Unknown Address'` rows (26,613). GN_Civics, Loyalist civics (public), Addington Highlands
  civics, Stone Mills Civic Address (View) and Civic Addresses (Public View) carry no such filter
  (27,383 together), so they expose ~37 points the county redacts plus 733 unknowns. GN_Civics and
  Loyalist are graded 5/import here; an import should take the filtered county view instead, and
  the county may want to know.
- **Provincial tenure downloads.** The province's mining claims, alienations and disposition
  areas are not downloadable from data.ontario.ca, but OGSEarth serves a viewing copy
  (`mlas_operational_gis_data.zip`, 206 MB). They stay tier 1.
- **Themes left fuzzy.** The list grew to 42 (2026-10-15). Graders still found no clean home
  for these:
  - fences and barriers (topography or amenities)
  - source-water protection zones (environment)
  - cartographic masks and label layers (maps)
  - Survey123 forms and staff records (statistics or community)
- **Letters not sent.** The two drafts of 2026-10-11 in `wiki/edits/`, the follow-up to the OSMF
  Licensing Working Group and the West Parry Sound scope question, were never sent, and there is
  no plan yet to send them (2026-10-30).
- **Licence emails.** Layers of use with no open licence have the status `No licence`;
  `report/SUMMARY.md` "Licences to ask for" lists those graded 3 to 5 by jurisdiction. The
  provincial bodies add some good ones: the Heritage Trust's plaques (terms forbid
  redistribution), AGCO's cannabis stores, and MTO's carpool lots and rest areas on its AGOL
  server. Essex County's 2026 10 cm orthophotos are on a server that names no licence; the
  county's Hub has one, and asking whether it covers the imagery could be worth more than any
  single layer.
- **OSM coverage.** No grade was checked against OSM. In particular:
  - buildings sit at 4 whether OSM already has them or not
  - CanVec imports may already carry much of the province's water, wooded areas and
    geographic names
  - Trans Canada Trail syncs with OSM (`push_to_osm_flag`), so its gain may be smaller than
    its grade
