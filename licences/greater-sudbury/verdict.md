# Greater Sudbury — City of Greater Sudbury Open Data Licence

**Verdict: NOT ELIGIBLE.** The self-service route is closed; email the LWG and wait. This verdict is about the self-service route only, not a finding that the licence is incompatible. The text is a reworked OGL – Ontario 1.0, and its differences from Ottawa 2.0 go well past the four categories:

- The exemption is open-ended: anything "not accessible under … MFIPPA …, [PHIPA] or **any other act or by-law**".
- The governing-law clause adds "**City of Greater Sudbury by-laws**". The City can change its own by-laws, so this lets it change what governs the licence on its own.
- Personal Information is widened to include personal health information under PHIPA.
- A new definition says "Use" includes downloading.

The exemptions and the Information Provider clause are also restructured.

## Sources

- Licence page: <https://www.greatersudbury.ca/city-hall/open-government/open-data/licence/> (HTML, fetched 2026-10-11, page dated "April 14, 2015").
- The tracker's layer is ArcGIS item `d3b94bd7d0a14b4b97b3757d1a383dd4` (Address and Building Roofline, owner Greater.Sudbury). Its `licenseInfo` links "Open Data License" to `https://www.greatersudbury.ca/inside-city-hall/open-data/policy/`, which redirects to the Open Data **Policy** page in the same section. That policy refers to "Open Data Licence v. 1.0", which is the licence page above.
- Base: `../_base/ottawa-2.0.txt`.
- OSM wiki Canada Open Data table row (checked 2026-10-11): licence "OGL-CA v1.0 City of Greater Sudbury", note "Not accepted for import into OSM due to name and licence text being different.", date checked 2025-11-28. The same boilerplate note sits on the Town of Oakville row, and the LWG has since listed Oakville. So the note is a wiki editor's flag, not an LWG decision. Sudbury is not on the OSMF variants page or the Contributors page.

## Identity

- Exact title: **City of Greater Sudbury Open Data Licence**. The required attribution names it "Open Data Licence – City of Greater Sudbury".
- Version: **1.0** ("This is version 1.0 of the City of Greater Sudbury Open Data Licence"), dated April 14, 2015.
- Template: OGL – Ontario 1.0, "adapted for municipal use and jurisdiction" (own preamble). It is **not** OGL-Canada-based; the wiki's "OGL-CA v1.0" label is inaccurate.

## Differences against Ottawa 2.0

Categories: **1** locality name · **2** legal venue · **3** PII definition (provincial law) · **4** "records" definition (provincial law) · **OTHER** · *trivial*.

| # | Clause | Ottawa 2.0 | Greater Sudbury 1.0 | Class |
|---|---|---|---|---|
| 1 | Preamble | "based on version 2.0 of the Open Government Licence – Canada…" | "based on version 1.0 of the Open Government Licence – Ontario. This licence has been adapted for municipal use and jurisdiction. The only significant changes from the Ontario licence are the replacement of references to [FIPPA] with references to the Personal Health Information Protection Act, 2004 … and the Municipal Freedom of Information and Protection of Privacy Act" | OTHER (non-operative). A different base template is declared. |
| 2 | Lead-in | (none) | "You are encouraged to use the information that is available under this licence as described below." | OTHER (non-operative) |
| 3 | Grant | "The Information Provider grants you a … licence to use the Information including for commercial purposes…" | "The Information Provider, the City of Greater Sudbury, grants you a … licence to use the information provided **for any purpose**, including for commercial purposes…" | 1 (the name). "for any purpose" adds nothing over "Copy, modify … for any lawful purpose"; *trivial*. |
| 4 | Attribution | "any attribution statement specified by the Information Provider(s)" / "If the Information Provider does not provide … or if you are using Information from several information providers…" | "…specified by the City of Greater Sudbury" / "If the City does not provide … or if you are using information from other Information Providers as well as the City…" | 1 (reworded around the City's name). The meaning is unchanged. |
| 5 | Attribution statement | "…Open Government Licence – City of Ottawa." | "Contains information licensed under the Open Data Licence – City of Greater Sudbury." | 1 (the licence name also changes from "Open Government Licence" to "Open Data Licence") |
| 6 | Termination | "the rights granted you … any similar licence granted by the Information Provider" | "the rights granted to you … any similar licence granted by the City of Greater Sudbury" | 1 / *trivial* |
| 7 | Exemptions, structure | "This licence does not grant you any right to use: [4 items]" | "This licence: Does not grant you any right to use Personal Information; Does not grant you any right to use … [5 items]" | *trivial* (restructured; same effect for the shared items) |
| 8 | Exemption, **added** | (none) | "Does not grant you any right to use information or records that are not accessible under the Municipal Freedom of Information and Protection of Privacy Act, R.S.O. 1990, c. M. 56, the Personal Health Information Protection Act, 2004, S.O. 2004, c. 3, Sched. A **or any other act or by-law**;" | **OTHER (extra exemption, open-ended).** "any other act or by-law" has no limit and lets the City exempt material by passing its own by-law. This goes well past a "records" definition. |
| 9 | Exemptions (shared items) | "Third party rights the Information Provider…", "official symbols of the Information Provider" | "third party rights the City of Greater Sudbury…", "official symbols of the City of Greater Sudbury" | 1 |
| 10 | Non-endorsement | "…the Information Provider endorses you…" | "…the City of Greater Sudbury endorses you…" | 1 |
| 11 | No warranty / liability | "the Information Provider excludes … The Information Provider is not liable…" | "the City of Greater Sudbury excludes … The City of Greater Sudbury is not liable…" | 1. Otherwise identical apart from the comma in "obligations, and liabilities". |
| 12 | Governing law | "governed by the laws of the Province of Ontario and the applicable laws of Canada." | "governed by the laws of the Province of Ontario, the applicable laws of Canada **and City of Greater Sudbury by-laws**." | **OTHER.** This is not a venue change (category 2 covers the forum, not the body of law). Making the licensor's own by-laws part of the governing law is a substantive addition. |
| 13 | Venue | "may only be brought in the courts of Ontario." | Identical | — |
| 14 | Def. "Information" | "information resources protected by copyright or other information that is offered…" | "information resources or Records protected by copyright or other information, resources or Records that are offered…" | 4 |
| 15 | Def. "Information Provider" | "means City of Ottawa." | **Dropped as a definition**; the capitalised term "Information Providers" still appears in clause 4 with no definition. | 1 (the City's name is written directly into the grant). The dangling undefined term is *trivial*. |
| 16 | Def. "Personal Information" | "as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | "as defined in section 2 of the Municipal Freedom of Information and Protection of Privacy Act … **and includes "personal health information" as defined in section 4 of the Personal Health Information Protection Act, 2004**" | 3 for the MFIPPA part. Adding PHIPA health information widens the exclusion; the procedure does contemplate a definition aligned to provincial law, so this is arguably still 3, but it is a second statute and is flagged. |
| 17 | Def. "Records", **added** | (none) | "means "record" as defined in section 2 of [MFIPPA] and section 2 of [PHIPA];" | 4 |
| 18 | Def. "Use", **added** | (none) | "“Use” includes downloading; and" | **OTHER (added definition).** Harmless in practice, but outside the four categories. |
| 19 | Def. "You" | "…acquiring rights under this licence." | "…, as applicable, acquiring rights under this licence, and “Your” is the possessive tense of you." | OTHER (minor wording, no practical effect) |
| 20 | Versioning | "This is version 2.0 of the Open Government Licence – City of Ottawa. The Information Provider may make changes…" | "This is version 1.0 of the City of Greater Sudbury Open Data Licence. The City of Greater Sudbury may make changes…" | 1 |

**Clauses dropped:** the "Information Provider" definition (see row 15).
**Clauses more permissive than Ottawa:** none of substance.
**Clauses with effects outside the four categories:** rows 8, 12 and 18, plus the PHIPA extension in row 16.

## Contributors entry (do NOT paste until the LWG confirms)

```
===== Greater Sudbury =====
OpenStreetMap data may include data provided by the City of Greater Sudbury under the [https://www.greatersudbury.ca/city-hall/open-government/open-data/licence/ Open Data Licence – City of Greater Sudbury].
```

## Email paragraph (a question for the LWG, not a self-service notice)

The City of Greater Sudbury Open Data Licence v1.0 (<https://www.greatersudbury.ca/city-hall/open-government/open-data/licence/>, dated 2015-04-14) is an adaptation of OGL – Ontario 1.0. Its grant, attribution, non-endorsement, warranty and liability clauses match the Ottawa Open Data Licence 2.0 once the City's name replaces "Information Provider". It does not meet the self-service test, for three reasons. Its exemption covers information "not accessible under [MFIPPA], [PHIPA] or any other act or by-law". Its governing-law clause adds "City of Greater Sudbury by-laws". Its Personal Information definition adds PHIPA health information, and a new definition says "Use" includes downloading. We would be grateful for the LWG's view on whether the open-ended "any other act or by-law" exemption and the by-law governing-law clause affect compatibility for the City's civic address points.
