# Barrie — Open Government Licence – Barrie

**Verdict: UNKNOWN.** The case for self-service is strong but not clean. The licence says it is based on OGL – Ontario 1.0. Measured against Ottawa 2.0, every difference except one fits the four OSMF categories or is non-operative wording. The exception is an added exemption: clause 6(b), "Information or Records not accessible under the Municipal Freedom of Information and Protection of Privacy Act (Ontario)". This is an extra exemption, which the procedure does not list as allowed. It could be read as part of category 4, the "records" definition, because the OSMF page cites Edmonton for that category and Edmonton's licence is reported to carry the same exemption. That reading rests on a secondary source: I could not fetch Edmonton's own text. Precedent points the same way. Oakville, self-listed in August 2026 and listed by the LWG on 2026-09-14, has the same kind of exemption ("information protected under Ontario's Municipal Freedom of Information and Protection of Privacy Act (MFIPPA)"). So does Toronto, which the LWG lists ("Information not accessible under the Ontario Municipal Freedom of Information and Protection of Privacy Act…"). Two further oddities: the definitions point to the provincial FIPPA while the exemption points to MFIPPA, and the preamble promises a PHIPA provision that the body does not contain.

**Recommendation:** email the LWG and wait. The Oakville and Toronto precedent is the argument to put in that email, not a reason to skip it. Do not treat this as a clean four-category diff.

**Second caveat: the licence is not attached to the layer in use.** The tracker pulls ArcGIS item `38b9faf0262e4ff9acf3e1d6720df7f8` (COB_ADDRESS_POINT, services3.arcgis.com). That item has **no `licenseInfo`** and is shared to **no groups**, so it is not in the opendata.barrie.ca catalogue. The catalogue's groups `a11c9689…` and `3ea69cc6…` hold a different item, "Address Points" `4902c7fd1aff42fb892a9d4e51428b95`, which serves `https://gispublic.barrie.ca/arcgis/rest/services/Open_Data/AddressVW/MapServer` and whose licenseInfo is only "© Copyright City of Barrie…". The portal-wide notice ("By downloading data from this site you are agreeing to the terms of the Open Data License") therefore covers the catalogued AddressVW layer, not COB_ADDRESS_POINT. Before any OSM use, either switch to the catalogued AddressVW service or get Barrie to confirm that COB_ADDRESS_POINT is released under this licence.

## Sources

- Licence PDF: <https://www.barrie.ca/Online%20Services/PublishingImages/OpenData_Images/COB_DataLicense.pdf> (fetched 2026-10-11, 19,214 bytes).
- The City's GIS portal <https://opendata.barrie.ca/> links this PDF from its home page: "By downloading data from this site you are agreeing to the terms of the Open Data License".
- The tracker's layer is ArcGIS item `38b9faf0262e4ff9acf3e1d6720df7f8` (COB_ADDRESS_POINT, owner BarrieGIS). Its `licenseInfo` is **empty** and it is not in the portal catalogue (see the second caveat above).
- Base: `../_base/ottawa-2.0.txt`.
- OSMF wiki listing: Barrie is **not** on the OSMF variants page, the Contributors page, or the wiki Canada Open Data table (all checked 2026-10-11). There is no prior decision either way.

## Identity

- Exact title: **Open Government Licence – Barrie**
- Version: **1.0** ("This is version 1.0 of the Open Government Licence – Barrie")
- Template: OGL – Ontario 1.0. The PDF's own preamble says "This licence is based on version 1.0 of the Open Government Licence – Ontario". Ottawa 2.0 is based on OGL – Canada 2.0.
- Required attribution: "Contains information licensed under the Open Government Licence – Barrie."

## Differences against Ottawa 2.0

Categories: **1** locality name · **2** legal venue · **3** PII definition (provincial law) · **4** "records" definition (provincial law) · **OTHER** anything else · *trivial* (punctuation or wording with no legal effect, listed for completeness).

| # | Clause | Ottawa 2.0 | Barrie 1.0 | Class |
|---|---|---|---|---|
| 1 | Preamble | "based on version 2.0 of the Open Government Licence – Canada … replace direct references to the Government of Canada with the City of Ottawa, replace a reference to the Federal Privacy Act with … MFIPPA, and remove a reference to the Federal Court of Canada." | "based on version 1.0 of the Open Government Licence – Ontario … The only substantive changes in this licence are to replace direct references to the Province of Ontario with the City of Barrie and the inclusion of a provision for the Ontario Personal Health Information Protection Act, 2004." | OTHER (non-operative). A different base template is declared. The PHIPA provision it promises **does not appear anywhere in the body**, so the preamble does not describe the licence accurately. |
| 2 | Title line | (none) | "Open Government Licence – Barrie" | 1 |
| 3 | Lead-in | (none) | "You are encouraged to use the Information that is available under this licence with only a few conditions." | OTHER (non-operative). OGL template boilerplate with no legal effect. |
| 4 | Numbering | Unnumbered paragraphs | Numbered clauses 1–13, exemptions a–e | *trivial* (structure) |
| 5 | Grant | "…non-exclusive licence to use the Information including for commercial purposes subject to the terms below." | "…non-exclusive licence to use the Information, including for commercial purposes, subject to the terms below." | *trivial* (commas) |
| 6 | Attribution | "several information providers" | "several Information Providers" | *trivial* (capitalisation) |
| 7 | Attribution statement | "Contains information licensed under the Open Government Licence – City of Ottawa." | "Contains information licensed under the Open Government Licence – Barrie." | 1 |
| 8 | Termination | "the rights granted you under this licence" | "the rights granted to you under this licence" | *trivial* |
| 9 | Exemption (b), **added** | (no such clause; Ottawa lists four exemptions) | "b. Information or Records not accessible under the Municipal Freedom of Information and Protection of Privacy Act (Ontario);" | **OTHER (extra exemption).** It could be counted as category 4 only by reading that category as covering an MFIPPA access exemption tied to a "Records" definition. The Edmonton example on the OSMF page is reported (secondary source; primary text not retrieved) to carry the same pairing, and LWG-listed Oakville and Toronto have equivalent MFIPPA exemptions. It is still an added restriction. In practice it withholds nothing that appears in a published address layer. |
| 10 | Exemptions (c)/(d) | "Third party rights…", "The names, crests, logos, or other official symbols…" | "third party rights…", "the names, crests, logos, or other official symbols…" | *trivial* (case). Note that "official symbols" matches Ottawa. |
| 11 | Non-endorsement | "endorses you or your use of Information." | "endorses you or your use of the Information." | *trivial* |
| 12 | No warranty | "obligations and liabilities" | "obligations, and liabilities" | *trivial* |
| 13 | Governing law and venue | "governed by the laws of the Province of Ontario and the applicable laws of Canada." / "may only be brought in the courts of Ontario." | Identical | — (no difference) |
| 14 | Def. "Information" | "information resources protected by copyright or other information that is offered…" | "information resources or Records protected by copyright or other information or Records that are offered…" | 4 (follows from adding a "Records" definition) |
| 15 | Def. "Information Provider" | "City of Ottawa." | "The Corporation of the City of Barrie" | 1 |
| 16 | Def. "Personal Information" | "as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | "has the meaning set out in section 2(1) of Freedom of Information and Protection of Privacy Act (Ontario)." | 3. Note that it cites the **provincial** FIPPA, not the municipal MFIPPA, so it is inconsistent with exemption 6(b), which cites MFIPPA. It is still a provincial-law PII definition. |
| 17 | Def. "Records", **added** | (none) | "has the meaning of "record" as set out in the Freedom of Information and Protection of Privacy Act (Ontario)." | 4 (also cites FIPPA rather than MFIPPA) |
| 18 | Versioning | "This is version 2.0 of the Open Government Licence – City of Ottawa." | "This is version 1.0 of the Open Government Licence – Barrie." | 1 (number and name). The rest of the clause is identical. |

**Clauses dropped compared with Ottawa:** none.
**Clauses more permissive than Ottawa:** none.
**Liability, indemnity, non-commercial, or voluntary-attribution changes:** none. The warranty, liability and attribution clauses match Ottawa word for word, apart from commas.

## Contributors entry (do NOT paste until the LWG confirms)

```
===== Barrie =====
OpenStreetMap data may include data provided by the City of Barrie under the [https://www.barrie.ca/Online%20Services/PublishingImages/OpenData_Images/COB_DataLicense.pdf Open Government Licence – Barrie].
```

## Email paragraph (to legal-questions@osmfoundation.org)

The Open Government Licence – Barrie (v1.0, <https://www.barrie.ca/Online%20Services/PublishingImages/OpenData_Images/COB_DataLicense.pdf>) is, by its own preamble, based on OGL – Ontario 1.0, which the LWG lists as compatible. Diffed against the Ottawa Open Data Licence 2.0, its grant, attribution, termination, non-endorsement, warranty, liability and governing-law clauses are word-for-word the same apart from punctuation. The differences are the locality name ("The Corporation of the City of Barrie") and a Personal Information definition and a new "Records" definition that both point to Ontario's Freedom of Information and Protection of Privacy Act. There is one difference outside the four listed categories: an added exemption for "Information or Records not accessible under the Municipal Freedom of Information and Protection of Privacy Act (Ontario)". Oakville (listed 2026-09-14) and Toronto carry the same kind of exemption, and we ask you to confirm that it does not affect compatibility. We would like to list Barrie on the Contributors page with the attribution "Contains information licensed under the Open Government Licence – Barrie."
