# Follow-ups

Work the portal sweeps (`inventory.py`, `catalogue/layers/`) left open. The first sweep
(2026-10-14) covered the municipalities; the second (2026-10-15) added the province, 21
ministries, agencies, school boards and health units, the 36 conservation authorities and
Conservation Ontario, Guelph's map server, Erin, and everything each Hub lists beyond its
`dataset` collection. The third (2026-10-16) read GRIN and RVCA's JKAN through new `custom`
readers, swept Essex County's imagery server, added OGSEarth's and Metrolinx's remaining
downloads as hand rows, and repaired the copy marks (below). The fourth (2026-10-30) listed the
54 ArcGIS Online org roots the Ontario Hubs sit on, and opened Nova Scotia. The fifth
(2026-11-02 and 03) opened New Brunswick.

## Graded on 2026-10-30 and 31

- **The org roots behind the Ontario Hubs (graded 2026-10-31).** 15,392 layers on 54 roots in
  51 jurisdictions, graded by eighteen agents told to look for each layer's counterpart in the
  catalogue first. Tiers: 1 at 5, 82 at 4, 559 at 3; 3,744 copies; 133 `Available` (rows with a
  Hub licence), the rest `No licence` or `Not usable`. Three quarters are tier 1: Survey123
  forms, staff and app layers, the province's forest-management-plan packages (about 2,100 of
  its 2,452), census tables. What the Hubs left out, in brief:
  - **Kingsville's 10,270 civic address points** on Essex County's org, the one tier 5, which
    the tracker does not follow: the second untracked town found this way, after Leamington.
  - **Dufferin's address-points-cityview-wgs84**, 32,318 points edited 2026-10, larger and newer
    than the 28,305 the tracker follows; the tracker's own note says a better layer exists.
    Re-pointing it is `../ontario-address-changes`' call.
  - **Buildings with heights:** Hamilton's 193,683 polygons with eave height and roof form,
    Sudbury's 128,651 rooflines (twice the Hub layer), Ottawa's 392,000 footprints, Cobourg's
    9,162 and Dufferin's 37,591 footprints with addresses, Essex's 19,096 with roll numbers.
  - **Trails:** Mississauga's pedestrian trail network (9,197 and 11,437 segments; the Hub has
    none), Cambridge's 2,119 named trails, Burlington's off-road trails, North Frontenac's ATV and
    hiking trails and campsites.
  - **Trees:** Peterborough's 51,585 (2026), Cornwall's 16,008, Cobourg's 11,780, Essex's 5,750.
    Peterborough's Hub layer has 29,455 (2023) and is also tier 4: decide which is the copy.
  - Heritage registers (Brantford, Kawartha Lakes, Peterborough, York, Rideau Lakes, PEC,
    Cornwall), stormwater ponds, park amenities, Brampton's sports-field rosters.

  Also found: Woolwich's org carries Wellesley's and Wilmot's own services, and neither township
  has a shared portal row. Prince Edward County's org shows only a 16,101-point address view
  against the tracked 27,602. Grey's, Frontenac's and Waterloo Region's orgs each hold a layer
  exported from OSM itself (tier 1). Several orgs carry Esri sample data or test layers.
- **Nova Scotia is graded (2026-10-30):** 4,764 layers in 53 batches, graded by eleven agents
  the same day. Tiers: 39 at 5 (every municipal civic-address and building-footprint layer, the
  province's NSCAF civic points and 504,081 footprints), 82 at 4, 391 at 3; 911 marked copies.
  No municipal layer is licensed except Halifax's (Open Government Licence - Halifax) and some of
  Cumberland's (ODbL), so Nova Scotia's tier-5 layers are mostly `No licence`: the licence
  emails to write first. Graders flagged many layers with personal data (owner names on
  parcels, contact details on forms, historical vital records); they are tier 1 with the fact
  in the note. `--copies` was tightened after it marked two of Windsor's 311 request layers as
  copies of each other: a shared schema and count prove nothing under 50 rows or between
  sublayers of one service.
- **Records of children and of homeless people are kept out, not only pupils' (2026-10-31).**
  Eleven layers were dropped from listings and the catalogue: two Pictou County forms of pupil
  and parent records, a Conservation Ontario school ski registration (student names, birth
  dates), a Peterborough County student programme form, three Oakville Youth Advisory Council
  applications (minors' names, ages, schools, parental consent), a Mississauga youth challenge
  form (school, grade, email), West Parry Sound's Kids in the Biosphere registrations
  (children's names and ages) and a county's two layers of homeless encampment locations.
  Dropping the encampments widens the rule beyond children: undo it in `PERSONAL_FIELDS` if
  that is not wanted. The filter now matches contact fields of students and parents, children's
  names, homelessness duration, and a school-grade-email set; it no longer matches a school
  list's `Student_Trustee` or a survey's yes-or-no `parent_guardian_school_child`.

## New Brunswick (surveyed 2026-11-02)

Every one of the 77 local governments and the 12 regional service commissions (RSCs) has a portal
row: a top-down pass over GeoNB, Socrata, Hub and ArcGIS Online searches, then three agents
checking each unit's own site. The province publishes through a Socrata catalogue
(gnb.socrata.com, 676 of 700 assets under the New Brunswick Open Government Licence, which the
OSMF page lists as compatible since 2025-07-14) and GeoNB, whose items name a GeoNB OpenData
Licence (`geonb-odl_en.pdf`). Six departments serve layers from ArcGIS Online orgs or servers
with no licence stated. Edmundston's Hub is the only municipal portal naming a licence of its
own. The OSM wiki's New Brunswick page records CanVec imported province-wide, GeoNB addresses
used as a reference by hand, and the 2023 boundaries imported in 2025; no import is tracked in
`work.csv`. Open ends:

- **The province's layers (graded 2026-11-02):** 2,205 layers once the test server was dropped
  (3,034 swept). GeoNB's 373,903 NB 911 civic address points and 661,348 lidar building
  footprints are tier 5 and `Available`. Worth a look in review:
  - `geonb-snb-municipal-planning-civic-addresses-2` has 441,451 points with unit numbers against
    the DPS layer's 373,903: it may be the better import source. It is marked a copy of the DPS
    layer.
  - **Test servers are not catalogued (decided 2026-11-03).** GeoNB's test server
    (`geonb-t.snb.ca`, 825 layers, among them 15,869 named trail segments production does not
    serve) was swept and graded, then dropped with its portal row, along with the 4-layer `test`
    folder on GeoNB's production server, Haliburton's 19-layer `Testing` folder and MTO's two
    `intra.dev` apps. `inventory.py`'s `TEST` rule keeps such hosts and folders out of later
    sweeps; a service merely named `test` on a production server is still listed.
  - The org's `schools-update-2024-05-03` (295 schools) is newer than the two 2018 production
    school layers, but is marked their copy.
  - Natural Resources' own server (`gis-erd-der.gnb.ca`) has an older NBHN edition (88,242
    watercourses against GeoNB's 158,957), province-wide 10-30 cm orthos (NBORTHOS) and Crown
    forest roads with attributes, all with no licence: the department is the one to ask. Two of
    its OpenData layers (mineral claims, exploration drillholes) say "not to distribute".
  - The Socrata "Rural Districts" dataset holds the 77 local governments, and its "NBHN" holds
    wetlands; both are marked copies of the GeoNB layers they really are.
- **The municipalities' and RSCs' layers (graded 2026-11-03):** 6,639 layers on 32 portals in 24
  jurisdictions, 932 copies; 5,572 at tier 1, among them Moncton's 2,922 council documents on its
  Hub. Only Edmundston's Hub names an open licence, Moncton's says "Open Data Terms of Use", and
  Fredericton's 119 Hub rows say "GNB Open Data Policy": a policy, not a licence, though the grader
  took it as open (`Available`); worth a look. What the cities publish beyond GeoNB:
  - **Their own address registers**, all graded on their merits against the NB 911 points:
    Fredericton's 25,111 points with units, postcodes and wards (tier 5, edited 2026-10-30),
    Moncton's 49,730 Greater Moncton points with units and postcodes, Saint John's 25,580 (the
    city's source for NB 911), Dieppe's 12,273 with units, Rothesay's 4,510 with suites, Quispamsis'
    8,123 `CivicNumbersTest` (live despite the name). Bathurst's layer stops at exactly 8,000, which
    looks capped.
  - **Footprints newer than GeoNB's 2015-18 lidar:** Moncton's 41,916 with year built, floors and
    height, Saint John's 37,656 and Quispamsis' 13,570 (both edited 2026-04), Fredericton's 31,183,
    Edmundston's 15,369 (source unverified).
  - **Trails:** the Southeast RSC's 1,069 and 337 named segments, Bathurst's 10,297 by use,
    Fredericton's 524 with Wolastoqey (Maliseet) names, Dieppe's 368, Edmundston's mountain-bike and hiking
    trails. Also parks, sports fields, trees (Fredericton 21,186, Moncton 12,731), heritage
    registers (Fredericton's 781 evaluated buildings), Rothesay's 1,836 signs, Saint John's truck
    routes and bike routes, Moncton's 344 parking lots.
  - Fredericton's org holds about 40 layers of South African municipal asset registers (Port St
    Johns, Buffalo City) and a Newfoundland salmon-pool layer; two Southeast RSC layers are Esri's
    Los Angeles sample data; two Edmundston layers are exports of OSM. All tier 1.
- **The RSCs hold the small units' layers.** 52 shared rows give members their zoning, civic
  points and other layers on the RSC orgs, many under the names of villages and planning areas
  the 2023 reform merged (Maple Hills' zoning is the old Kent County and Beaubassin West plans on
  the Southeast org). Kings and Western Valley RSCs publish PDF maps only, so 11 of their members
  are none-found at reach 1. Kedgwick is a Restigouche member, not Northwest's.
- **Fredericton's org is half someone else's.** 288 of its 555 services belong to Greater
  Fredericton Social Innovation's accounts (social-indicator tables, story maps); they are listed
  under Fredericton with that non-profit as provider.
- **Token-only and unread.** Bathurst's server opens 11 of 53 folders anonymously (planning,
  property and road network need a token); Dieppe's 8 of 16. Two Northwest RSC Hubs are empty
  sites. arcadianb.ca, townofsaintandrews.ca and valleywaters.ca answer 403 to scripts,
  tantramar.ca fails certificate checks, campbellton.org, grand-sault.ca, valleedesrivieres.ca,
  maps.saintjohn.ca and gis.moncton.ca do not answer.
- **Personal data in public layers**, all tier 1 with the fact in the note: Restigouche RSC's
  `SNBData_Restigouche` (property owners' names and mailing addresses), Chaleur RSC's variance
  layer (applicants' names and addresses), Natural Resources' deer registration agents (home
  addresses and phones), GeoNB's early learning centres (operators' emails and phones) and
  pharmacies, and 142 home daycares under their operators' names in the Socrata childcare list.
  A Tourism layer that looks like a children's physical-literacy self-assessment holds scores
  only, so it was kept. Municipal parcels joined to owners' names and mailing addresses are
  common on the RSC orgs (Acadian Peninsula, Capital Region, Restigouche, Chaleur) and in Dieppe,
  Miramichi and Rothesay.
- **Records of children and of homeless people kept out (2026-11-03).** Four forms and a layer were
  dropped: a city's holiday-help form (parents' and children's names, school, allergies), another
  city's student application and student quiz forms with their tables, and a city's 219 parcels
  marked as encampments with occupancy. `PERSONAL_FIELDS` now matches the French field names
  (`nom_dedes_enfants`, `nom_de_l_tudiant`), a layer named for encampments is left out whatever its
  fields, and a form with one such layer is left out whole. A count-only query shows one student
  application still readable by anyone and its layer editable by anyone; the holiday form accepts
  submissions only, and the encampment layer is read-only. Which publishers and services these are
  is in the gitignored `cache/scratch/exposed-forms.md`, as for Ontario's.
- **No address tracker for New Brunswick**, as for Nova Scotia: the NB 911 points have no
  `/addresses` row and no measures. Onboarding them is `../ontario-address-changes`' call.

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

- **GeoNB's download catalogue.** Its `custom` row (gnb.ca's data-catalogue page, 74 zip
  downloads from `geonb.snb.ca/downloads`) has no `api_url`, so it is not swept. Most of the 74
  have twins among the services on `geonb.snb.ca`; as with OGSEarth's, hand rows in `sources.csv`
  are owed only for downloads that have none.
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

- **`--copies` is not idempotent (found 2026-11-03).** Run again on the committed catalogue, it
  marks 33 rows the first run left alone: 32 of the Fundy RSC's CMIP6 climate grids (one service
  per emissions scenario, same 18,271 cells and fields, different values) as copies of each other,
  and one of Fredericton's South African asset layers. All are tier 1, so no grade moves; the
  Fundy marks were reverted by hand and will come back on the next run until the rule learns that
  a shared schema and count across scenario services is not a copy, or why the first run differs.
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

- **The wiki view is over MediaWiki's 2 MB (5.2 MB with New Brunswick, 3.3 MB with Nova Scotia,
  2.3 MB before).** Nothing
  is pasted until the catalogue is reviewed, so it blocks nothing yet; the likely fix is one page
  per province under `Canada/Open data/<Province>`, with the national table and links on the
  parent page.
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
- **Form answers left readable by anyone (checked 2026-10-31).** Every layer of children's or
  homeless people's records the sweeps found is the hidden layer behind a Survey123 form. A
  public form must accept submissions from anyone; whether anyone can also read the answers is
  a separate sharing setting, so the sweep sees only the publishers who set it wrong. Other
  municipalities collect the same things (programme sign-ups, outreach logs) and keep them
  private. A count-only query, which returns no records, shows two still exposed:
  - **A county's homeless-outreach log:** 71 encampment locations with population, how long
    people have been homeless, services needed and housing plans. Anyone can read, download and
    edit it, and it was edited on 2026-05-29, so it is in use. The county should be told, and
    soon: an editable layer can be altered as well as read.
  - **A city's youth challenge form:** 6 entries with school, grade and email, readable and
    editable by anyone; last edited 2021.

  Two others accept submissions only, so their answers are hidden and only the field names show:
  a children's activity-kit registration (2019) and a youth advisory council application (2026).
  They were dropped from the listing anyway. Which publishers and services these are is kept out
  of this public file, so it does not point anyone at them: it is in the gitignored
  `cache/scratch/exposed-forms.md`.
- **Copy marks repaired (2026-10-16).** `copies()` took any first word after "Copy of" as
  the original, so prose ("Copy of the county's layer") and stray punctuation ("Copy of
  <id>;") counted as marks, and 50 originals were demoted to copies of themselves or of "the".
  Those 50 have their graded tier back; notes naming an id became marks and dropped to tier 2;
  139 naming none now read "A copy of" and keep their grade. 6,269 layers are marked copies.
  Worth a look in review: the rows whose tier moved in commit `5b29458`.
  **Marks the loose count rule may have made (counted 2026-10-30).** Until today `--copies`
  took a shared schema and record count as proof from 2 rows up, and between sublayers of one
  service; that marked two of Windsor's 311 request layers as copies of each other, so the rule
  now needs 50 rows and different services. Marks already made were left alone. Of Ontario's
  6,669 marks, 1,177 sit between sublayers of one service (Simcoe 352, Haliburton 290, York 63,
  Markham 53) and 2,534 share a record count under 50 with their original; some of each were
  proved another way (same URL, a grader's note), so these are upper bounds on what to review.
  A wrong mark hides a layer at tier 2.
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
