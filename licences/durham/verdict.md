# Durham — which licence governs the layer, and the diff

**Verdict: NOT ELIGIBLE.** The self-service route is closed; email the LWG and wait. This verdict is about the self-service route only, not a finding that the licence is incompatible. The layer the tracker pulls is governed by the **Region of Durham Open Data Licence v.1.0**, not by the City of Oshawa licence that `durham.toml` names. The Durham licence is a different licence family: its "free to" list and lead-in follow the UK Open Government Licence v1.0 wording, not OGL – Canada 2.0. Almost every clause differs from Ottawa 2.0:

- **Attribution is voluntary.**
- The Region can make you **remove its credit statement** on request.
- There are added conduct conditions: "complies with all applicable laws and is **not harmful to others**", and "do not misrepresent the Information or its source".
- An availability disclaimer is added.
- **There is no legal-venue clause.**
- "Information" is limited to material made available "through The Regional Municipality of Durham website".

**`durham.toml` names the wrong licence for the layer.** `license_name = "Open Government Licence – City of Oshawa"` and the `green-lwg` tier both rest on the Oshawa licence. The Region's own item for the exact service URL cites the Durham licence. The tracker's comment, "the region-wide licence is unconfirmed", can now be answered: a Region licence exists, it is the one that applies, and it is not OSM-cleared.

**Secondary verdict, City of Oshawa licence (applies to Oshawa's own data, not to this layer): UNKNOWN.** It is OGL – Canada 2.0 with the same added MFIPPA "Records" exemption as Barrie, plus "official marks" in place of "official symbols". The diff is below.

## Which licence governs the layer

- The tracker's `data_url` is `https://maps.durham.ca/arcgis/rest/services/Open_Data/Durham_OpenData/MapServer/0`.
- That service is registered on ArcGIS Online as item `8dcfee4f8c904ef29248b2c82ef33175`: "Civic Addresses", owner **GIS_DurhamRegion**, accessInformation "Region of Durham", last modified 2025-02-19. Its `licenseInfo` is `<a href='https://www.durham.ca/en/regional-government/resources/Documents/OpenDataLicenceAgreement.pdf'>Open Data License</a>`.
- The Oshawa Hub URL in the vault note (`city-oshawa.opendata.arcgis.com/datasets/DurhamRegion::civic-addresses`) carries the `DurhamRegion::` prefix. It is the Region's item re-surfaced in the City's catalogue, so the City's licence does not attach to it.
- The City of Oshawa's own address item is different: `528210b2e00c4607b8c971f4ed9389ff` "Oshawa Addresses", owner City.of.Oshawa, `https://map.oshawa.ca/arcgis/rest/services/Operational/Parcels_AddPts/MapServer/0`. That one carries the Oshawa OGL 2.0.
- The Region's open data page (<https://www.durham.ca/regional-government/access-to-information/open-data/>) publishes the licence text inline and says: "By downloading and/or using the data on this site, you are agreeing to the above Open Data Licence."

## Sources

- Governing licence text (`licence.txt`): live HTML at <https://www.durham.ca/regional-government/access-to-information/open-data/>, fetched 2026-10-11. The PDF linked from the item now returns 404. The Wayback capture <https://web.archive.org/web/20250914143117/https://www.durham.ca/en/regional-government/resources/Documents/OpenDataLicenceAgreement.pdf> has the same wording, and the CDX digest was unchanged from 2020-10-21 to 2026-04-16.
- Oshawa licence (`licence-oshawa.txt`): <https://map.oshawa.ca/OpenData/Open%20Government%20Licence%20version%202.0%20-%20Oshawa.pdf>, fetched 2026-10-11.
- Base: `../_base/ottawa-2.0.txt`.
- Prior decisions: neither Durham nor Oshawa is on the OSMF variants page, the Contributors page, or the wiki Canada Open Data table (checked 2026-10-11). In a 2018 talk-ca thread, a Durham staff member asked whether to adopt OGL-Canada, and a reply said the Region's licence was likely not LWG-approved: <https://lists.openstreetmap.org/pipermail/talk-ca/2018-March/008545.html>.

## A. Region of Durham – Open Data Licence v.1.0 against Ottawa 2.0

- Exact title: **Region of Durham - Open Data Licence v.1.0** ("version 1.0 of the Open Data Licence for The Regional Municipality of Durham").
- Suggested (optional) credit: "Contains public sector information made available under The Regional Municipality of Durham's Open Data Licence".

| # | Clause | Ottawa 2.0 | Durham 1.0 | Class |
|---|---|---|---|---|
| 1 | Preamble | "based on version 2.0 of the Open Government Licence – Canada…" | (none; lead-in only) "You are encouraged to use and re-use the information that is available under this licence, freely and flexibly, with only a few conditions." | OTHER. A different licence family; no OGL-Canada base is declared. |
| 2 | Grant | "…non-exclusive licence to use the Information including for commercial purposes subject to the terms below." | "Durham Region grants you a worldwide, royalty-free, perpetual, non-exclusive licence to use the information subject to the conditions below." | 1, but commercial use moves to the "free to" list |
| 3 | Copyright exceptions, **added** | (none) | "This licence does not affect any copyright exceptions or limitations available under the Copyright Act (Canada)." | OTHER (more permissive or neutral) |
| 4 | Freedoms | "Copy, modify, publish, translate, adapt, distribute or otherwise use the Information in any medium, mode or format for any lawful purpose." | "Copy, publish, distribute and transmit the information." / "Adapt the information." / "Use the information commercially, for example…" | OTHER (different enumeration). There is no "translate", "any medium, mode or format" or "otherwise use"; these are partly covered by the "Use" definition (row 16). |
| 5 | Attribution | "**You must** … Acknowledge the source of the Information by including any attribution statement specified … you must use the following attribution statement: Contains information licensed under the Open Government Licence – City of Ottawa." | "[You are free to] Provide credit to Durham Region when using information under this licence, **but are not required to**. If you choose to provide credit, please acknowledge … "Contains public sector information made available under The Regional Municipality of Durham's Open Data Licence"." | **OTHER (voluntary attribution).** More permissive than Ottawa, but outside the four categories. |
| 6 | Credit removal, **added** | (none) | "Upon the request of Durham Region, remove any Durham Region credit statement should Durham Region, in its sole discretion, decide that such credit is not in the public interest." | **OTHER (added obligation).** OSM attributes through the Contributors page and changeset `source` tags; an on-demand removal duty conflicts with how that attribution persists. |
| 7 | Non-endorsement | "This licence does not grant you any right to use the Information in a way that suggests any official status or that the Information Provider endorses you…" | "Ensure that you do not use the information in a way that suggests any official status or that Durham Region endorses you…" | 1 (recast as a condition; same effect) |
| 8 | Misrepresentation, **added** | (none) | "Ensure that you do not misrepresent the information or its source." | **OTHER (added condition)** |
| 9 | Lawful and harmless use, **added** | ("for any lawful purpose" in the freedoms) | "Ensure that your use of the information complies with all applicable laws and is **not harmful to others**." | **OTHER (added restriction).** "not harmful to others" is vague, open-ended and new. |
| 10 | Termination | "if you fail to comply with any of them, the rights granted you under this licence, or any similar licence granted by the Information Provider, will end automatically." | "if you fail to comply with them, the rights granted to you under this licence will end automatically." | OTHER (narrower: no cross-licence termination; more permissive) |
| 11 | Exemptions | Personal Information; third party rights; "names, crests, logos, or other official symbols"; "Information subject to other intellectual property rights, including patents, trade-marks and official marks." | Personal information; "Information or records that are not accessible pursuant to the Municipal Freedom of Information and Protection of Privacy Act (MFIPPA)."; third-party rights "if any"; "**Public sector organization** logos, trademarks, slogans or crests." | OTHER. The MFIPPA exemption is added, with "records" undefined. The logo exemption is extended to any public-sector organisation. The general "other intellectual property rights, including patents" exemption is dropped. |
| 12 | No warranty | "excludes all representations, warranties, obligations and liabilities, whether express or implied, **to the maximum extent permitted by law**." | "excludes all representations, warranties, obligations and liabilities, whether express or implied, **in relation to the information**." | OTHER (reworded) |
| 13 | Availability disclaimer, **added** | (none) | "Durham Region does not guarantee that the information will be available in any particular format, nor that the information will continue to be available." | OTHER (added disclaimer, harmless) |
| 14 | Liability | "…caused by its use **or otherwise arising in connection with this licence or the Information**, even if…" | "…caused by its use, even if…" | OTHER (narrower) |
| 15 | Governing law and venue | "governed by the laws of the Province of Ontario and the applicable laws of Canada." / "Legal proceedings related to this licence may only be brought in the courts of Ontario." | "This licence is governed by the laws of the Province of Ontario." (**no venue clause**) | **OTHER (dropped clause).** The venue clause is dropped entirely, and "applicable laws of Canada" is omitted. |
| 16 | Def. "Information" | "information resources protected by copyright or other information that is offered for use under the terms of this licence." | "information protected by copyright that is made available under the terms of this licence **through The Regional Municipality of Durham website**." | **OTHER (scope limited to website-delivered material).** It is arguable whether data pulled from `maps.durham.ca` REST counts as "through the website". |
| 17 | Def. "Information Provider" | "City of Ottawa." | (replaced by) ""Durham Region" means The Regional Municipality of Durham." | 1 |
| 18 | Def. "Personal Information" | "section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | "has the meaning set out in the Municipal Freedom of Information and Protection of Privacy Act (MFIPPA)." | 3 |
| 19 | Def. "Use", **added** | (none) | "means doing any act that is restricted by copyright … includes without limitation distributing, copying, adapting, modifying as may be technically necessary to use it in a different mode or format." | OTHER |
| 20 | Versioning | "Your use of the Information will be governed by the terms of the licence in force as of the date you accessed the information." | "…may, from time to time, issue new versions … You may continue to use information licensed under this version should you wish to do so. Notices of new versions … will be posted at the Region's website." | OTHER (different mechanism; arguably more permissive) |

**Summary for Durham:** rows 5, 6, 8, 9, 11, 15 and 16 are each enough on their own to take this licence out of the self-service route. Voluntary attribution (row 5), the narrower termination (row 10) and the copyright-exceptions clause (row 3) are more permissive. The credit-removal duty, the "not harmful to others" condition and the website scope are added restrictions.

### Contributors entry for Durham (do NOT paste; the licence is not cleared)

```
===== Durham Region =====
OpenStreetMap data may include data provided by The Regional Municipality of Durham under the [https://www.durham.ca/regional-government/access-to-information/open-data/ Region of Durham Open Data Licence v1.0].
```

### Email paragraph for Durham (a question for the LWG)

The Region of Durham Open Data Licence v1.0 (<https://www.durham.ca/regional-government/access-to-information/open-data/>) governs the Region's civic address layer (`maps.durham.ca` Open_Data/Durham_OpenData MapServer/0). It is not an OGL – Canada 2.0 derivative and is not substantially the same as the Ottawa Open Data Licence 2.0. It grants a worldwide, royalty-free, perpetual, non-exclusive licence that includes commercial use and adaptation, and attribution is optional. However, it obliges users to remove the Region's credit statement on request, to keep their use "not harmful to others", and not to misrepresent the information. It also limits "Information" to material made available "through The Regional Municipality of Durham website", and it has no venue clause. We would be grateful for the LWG's view on whether this licence is compatible with the ODbL and OSM's contributor terms, and in particular on the credit-removal and "not harmful to others" conditions.

## B. City of Oshawa – Open Government Licence 2.0 against Ottawa 2.0 (not the layer's licence; for reference)

- Exact title: **Open Government Licence – The Corporation of the City of Oshawa**. Version: "version 2 of the Open Government Licence for The Corporation of the City of Oshawa" (the PDF file name says "version 2.0").
- Template: OGL – Canada 2.0 (own preamble).

| # | Clause | Ottawa 2.0 | Oshawa 2.0 | Class |
|---|---|---|---|---|
| 1 | Preamble | "…replace direct references to the Government of Canada with the City of Ottawa…" | "…The only substantive changes to the licence are references to the province of jurisdiction and the name of the public body." | OTHER (non-operative). The claim is inaccurate; see rows 6 and 7. |
| 2 | Lead-in | (none) | "You are encouraged to use the Information that is available under this licence with only a few conditions." | OTHER (non-operative) |
| 3 | Grant and freedoms | as Ottawa | identical apart from commas; numbered 1–13 | *trivial* |
| 4 | Attribution | "specified by the Information Provider(s)" | "specified by the Information Provider" | *trivial* |
| 5 | Attribution statement | "…Open Government Licence – City of Ottawa." | "Contains information licensed under the Open Government Licence – The Corporation of the City of Oshawa" | 1 |
| 6 | Exemption (b), **added** | (none) | "b) Records not accessible under the Municipal Freedom of Information and Protection of Privacy Act, RSO 1990, c M.56, as amended;" | **OTHER (extra exemption)**, paired with a "Records" definition (row 12). The reasoning is the same as Barrie row 9: arguably category 4 by the Edmonton example (secondary source only), and Oakville and Toronto carry equivalents. |
| 7 | Exemption (d) | "official **symbols** of the Information Provider" | "official **marks** of the Information Provider" | **OTHER** (wording; probably no practical effect, since exemption (e) already covers official marks) |
| 8 | Termination | "rights granted you" | "rights granted to you" | *trivial* |
| 9 | Warranty, liability, governing law | as Ottawa | identical apart from commas | — |
| 10 | Venue | "in the courts of Ontario." | "in the courts of the Province of Ontario." | 2 / *trivial* |
| 11 | Def. "Information" | "information resources protected by copyright or other information that is offered…" | "information resources or Records protected by copyright or other information or Records that are offered…" | 4 |
| 12 | Defs. "Personal Information" and "Records" | PI: "section 2(1) of the Ontario [MFIPPA]"; no Records definition | PI: "section 2 of the Municipal Freedom of Information and Protection of Privacy Act, RSO 1990, c M.56, as amended"; Records: "has the meaning set out in section 2 of [MFIPPA]" | 3 / 4 |
| 13 | Def. "Information Provider" | "City of Ottawa." | "The Corporation of the City of Oshawa." | 1 |
| 14 | Versioning | "This is version 2.0 of the Open Government Licence – City of Ottawa…" | "This is version 2 of the Open Government Licence for The Corporation of the City of Oshawa…" (rest identical; "Information" is capitalised at the end) | 1 |

**Oshawa verdict: UNKNOWN.** Everything fits the four categories except the added MFIPPA "Records" exemption (row 6) and "official marks" (row 7). Use this only for the City of Oshawa's own `map.oshawa.ca` data, and only after the LWG replies. The Oakville and Toronto precedent is the argument to put in the email, not a substitute for sending it.

Contributors entry, if Oshawa data is ever used:

```
===== Oshawa =====
OpenStreetMap data may include data provided by The Corporation of the City of Oshawa under the [https://map.oshawa.ca/OpenData/Open%20Government%20Licence%20version%202.0%20-%20Oshawa.pdf Open Government Licence – The Corporation of the City of Oshawa].
```

Email paragraph for Oshawa: The Open Government Licence – The Corporation of the City of Oshawa (version 2, <https://map.oshawa.ca/OpenData/Open%20Government%20Licence%20version%202.0%20-%20Oshawa.pdf>) is OGL – Canada 2.0 localised to Ontario, the same base as the Ottawa Open Data Licence 2.0. Its grant, attribution, termination, non-endorsement, warranty, liability and governing-law clauses are word-for-word the same apart from punctuation and the City's name. Its venue is the courts of the Province of Ontario, and its Personal Information and "Records" definitions point to MFIPPA s.2. There are two differences outside the four listed categories. One is an added exemption for "Records not accessible under the Municipal Freedom of Information and Protection of Privacy Act", of the same kind found in the listed Oakville and Toronto licences. The other is "official marks" in place of "official symbols" in the logo exemption. We ask the LWG to confirm that neither affects compatibility.
