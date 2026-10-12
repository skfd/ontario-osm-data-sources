# Lambton — Open Government Licence – County of Lambton

**Verdict: NOT ELIGIBLE.** The self-service route is closed; email the LWG and wait. This verdict is about the self-service route only, not a finding that the licence is incompatible. The text is OGL – Canada 2.0 with Ontario references, the same family as Ottawa, but it has changes outside the four categories:

1. An **added sentence** at the end of the liability clause: "Your copying, modification, publication, translation, adaptation, distribution and any other use of the Information shall be at your sole and exclusive rights." It reads garbled and was probably meant to say "risk".
2. The **Versioning clause is dropped** entirely, even though the page is titled "2.0".
3. An extra exemption for "Information not available under the Municipal Freedom of Information and Protection of Privacy Act", with **no "Records" definition** to anchor it in category 4.
4. The exemption lead-in widens to "use **or access**".
5. "official **marks**" replaces Ottawa's "official symbols".

The page states that "The only substantive changes to the licence are references to the province of jurisdiction and the name of the public body". That statement is not accurate, and the tracker's `green-ogl` tier was based on it.

## Sources

- Licence page: <https://county-lambton.opendata.arcgis.com/pages/open-data-license>. This is an ArcGIS Hub page rendered by JavaScript. The text was read from its backing item: <https://www.arcgis.com/sharing/rest/content/items/c7c87d629f604ecab2ace7115bce6780/data?f=json> (item "Open Data License", owner jhannigan, last modified 2019-04-17), fetched 2026-10-11.
- The tracker's layer is ArcGIS item `81b3b0b051fa4b528802a51ce87c6b3f` (Address Points, owner opendata_lambton, url = `https://www.lambtongis.ca/arcgis_adaptor/rest/services/OpenData/AddressPoints/MapServer/0`). Its `licenseInfo` links "License" to the page above. The MapServer layer's `copyrightText` is empty.
- Base: `../_base/ottawa-2.0.txt`.
- OSM wiki Canada Open Data table row (checked 2026-10-11): "Open Government License 2.0 - County of Lambton", notes empty, date checked 2026-02-14. Lambton is not on the OSMF variants page or the Contributors page.

## Identity

- Exact title: page heading "**Open Government License 2.0 - County of Lambton**", licence title line "**Open Government Licence - County of Lambton**".
- Version: "2.0" appears only in the heading. There is no versioning clause.
- Template: OGL – Canada 2.0 (own preamble).
- Required attribution: "Contains information licensed under the Open Government Licence - County of Lambton".
- © 2019 The Corporation of the County of Lambton.

## Differences against Ottawa 2.0

Categories: **1** locality name · **2** legal venue · **3** PII definition (provincial law) · **4** "records" definition (provincial law) · **OTHER** · *trivial*.

| # | Clause | Ottawa 2.0 | Lambton | Class |
|---|---|---|---|---|
| 1 | Preamble | "This licence is based on version 2.0 of the Open Government Licence – Canada … replace direct references to the Government of Canada with the City of Ottawa…" | "This Open Government Licence is based on version 2.0 of the Open Government Licence - Canada, which was developed through public consultation and collaborative efforts by provincial and federal governments. The only substantive changes to the licence are references to the province of jurisdiction and the name of the public body." | OTHER (non-operative). The claim is inaccurate; see rows 7, 8, 11 and 17. |
| 2 | Title and lead-in | (none) | "Open Government Licence - County of Lambton" / "You are encouraged to use the Information that is available under this licence with only a few conditions." | 1 / OTHER (non-operative boilerplate) |
| 3 | Grant | "…licence to use the Information including for commercial purposes subject to the terms below." | "…licence to use the Information, including for commercial purposes, subject to the terms below." | *trivial* |
| 4 | Attribution | "specified by the Information Provider(s)" | "specified by the Information Provider" | *trivial* |
| 5 | Attribution statement | "…Open Government Licence – City of Ottawa." | ""Contains information licensed under the Open Government Licence - County of Lambton"" | 1 |
| 6 | Termination | Identical text | Identical text | — |
| 7 | Exemptions lead-in | "This licence does not grant you any right to use:" | "This licence does not grant you any right to use **or access**:" | **OTHER.** A wording change outside the categories. In practice it is harmless, since a licence that withholds a right also withholds access to the thing it withholds. |
| 8 | Exemption (b), **added** | (none) | "b) Information not available under the Municipal Freedom of Information and Protection of Privacy Act." | **OTHER (extra exemption).** Unlike Barrie, Oshawa and Edmonton, there is no "Records" definition, so it cannot be tied to category 4. LWG-listed Oakville and Toronto carry a similar MFIPPA exemption, which is a relevant precedent but does not make it self-service. |
| 9 | Exemption (c) | "Third party rights the Information Provider is not authorized to license;" | "third party rights the Information Provider is not authorized to licence;" | *trivial* (spelling) |
| 10 | Exemption (d) | "The names, crests, logos, or other official **symbols** of the Information Provider; and" | "the names, crests, logos, or other official **marks** of the Information Provider; and" | **OTHER** (wording). Probably no practical difference, since exemption (e) already excludes "official marks", but it is outside the four categories. |
| 11 | Liability, **sentence added** | "…even if specifically advised of the possibility of such loss, injury or damage." (end of clause) | "…even if specifically advised of the possibility of such loss, injury or damage. **Your copying, modification, publication, translation, adaptation, distribution and any other use of the Information shall be at your sole and exclusive rights.**" | **OTHER (added liability-type clause).** As written, "at your sole and exclusive rights" has no clear legal meaning. If it means "risk", it is an assumption-of-risk clause, close to the existing disclaimer. If it is read literally, "exclusive rights" contradicts the non-exclusive grant. Either way only the LWG can rule on it. |
| 12 | No warranty | "obligations and liabilities" | "obligations, and liabilities" | *trivial* |
| 13 | Governing law | "governed by the laws of the Province of Ontario and the applicable laws of Canada." | "governed by the laws of Ontario and the applicable laws of Canada." | *trivial* (same jurisdiction) |
| 14 | Venue | "may only be brought in the courts of Ontario." | Identical | — |
| 15 | Def. "Information" | "information resources protected by copyright or other information that is offered…" | "information resources or records protected by copyright or other information or records that are offered…" | OTHER / 4-adjacent. "records" (lower case) appears here but is **never defined**. |
| 16 | Def. "Information Provider" | "City of Ottawa." | "The Corporation of the County of Lambton." | 1 |
| 17 | Def. "Personal Information" | "as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | "has the meaning set out in 2(1) of the Muncipal Freedom of Information and Protection of Privacy Act (Ontario)." | 3. The statute and section are the same as Ottawa's; "Muncipal" is a typo and the word "section" is missing. *trivial* beyond that. |
| 18 | Def. "Records" | (none) | (none) | — (no "Records" definition to classify) |
| 19 | Versioning, **dropped** | "This is version 2.0 of the Open Government Licence – City of Ottawa. The Information Provider may make changes to the terms of this licence from time to time and issue a new version of the licence. Your use of the Information will be governed by the terms of the licence in force as of the date you accessed the information." | **Absent.** The page ends after the "You" definition and the copyright footer. | **OTHER (dropped clause).** Without it there is no statement that the licence in force at access time governs, so the County's ability to change terms later is undefined. Arguably that is more favourable to the user, but it is not certain. |

**Clauses dropped:** Versioning (row 19).
**Clauses more permissive than Ottawa:** possibly row 19, since nothing reserves the right to issue new terms, but it is ambiguous and not relied on.
**Liability, indemnity, non-commercial or voluntary-attribution changes:** row 11 adds an unclear sentence to the liability clause. There is no indemnity clause, no non-commercial limit, and attribution is still mandatory.

## Contributors entry (do NOT paste until the LWG confirms)

```
===== Lambton County =====
OpenStreetMap data may include data provided by the County of Lambton under the [https://county-lambton.opendata.arcgis.com/pages/open-data-license Open Government Licence – County of Lambton].
```

## Email paragraph (a question for the LWG, not a self-service notice)

The Open Government Licence – County of Lambton (<https://county-lambton.opendata.arcgis.com/pages/open-data-license>, titled "2.0") is OGL – Canada 2.0 localised to Ontario, the same base as the Ottawa Open Data Licence 2.0. Its grant, attribution, termination, non-endorsement, warranty, governing-law and venue clauses match Ottawa apart from the County's name, and its Personal Information definition points to the same MFIPPA s.2(1). It falls outside the self-service test for several reasons. It adds an exemption for "Information not available under the Municipal Freedom of Information and Protection of Privacy Act" (with no "Records" definition) and changes "official symbols" to "official marks". It drops the versioning clause. It also appends a sentence to the liability clause, "any other use of the Information shall be at your sole and exclusive rights", which we read as a drafting error for "risk". We would be grateful for the LWG's view on whether these differences, especially the appended liability sentence, affect compatibility for the County's civic address points.
