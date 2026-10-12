# leeds-grenville — Open Government Licence - United Counties of Leeds and Grenville v1.0

**Verdict: UNKNOWN.** Not the self-service path: email legal-questions@osmfoundation.org and wait.

Verdict words in this folder: ELIGIBLE = every difference from Ottawa 2.0 falls in categories 1–4, so the
licence can be added to Contributors and the LWG emailed afterwards. NOT ELIGIBLE / UNKNOWN = not the
self-service path; email the LWG and wait for its answer. Neither is a claim that the licence is incompatible.

Main reason: clause for clause this is the Ottawa 2.0 text with the locality swapped. It has the same
exemptions, the same governing-law and venue clause, and the same MFIPPA s. 2(1) reference. But it contains
drafting defects that are not locality, venue, PII or records edits:

- Personal Information is defined as "**perfect** information";
- "You" drops "or incorporate";
- the liability exclusion reads "caused by its **user**";
- "Information" drops "resources".

They look like typos and I expect the LWG to wave them through. The procedure's test is still "only these four
kinds of difference", and a defect in a definition is a difference, so this goes to the LWG first.

## Source

- Licence: <https://geohub-uclg.hub.arcgis.com/pages/terms-of-use> (page heading "Terms of Use", Leeds Grenville
  GIS Hub; dated on the page "January 3, 2024").
- Text taken from the Hub Page item
  <https://www.arcgis.com/sharing/rest/content/items/d2102e8a679d439a8ebcfeff8c2b9f83/data?f=json> (owner
  UCLG_Admin, item modified 2026-01-20). Confirmed on the rendered live page on 2026-10-11: it contains "perfect information", "persons corporate, acquiring", "caused by its user", "any right use" and "January 3, 2024".
- Exact title: there is no title line. The page is headed "Terms of Use"; the name comes from the Versioning
  clause, "version 1.0 of the Open Government Licence - United Counties of Leeds and Grenville", and the
  attribution "Contains information licensed under the Open Government Licence – United Counties of Leeds and
  Grenville."
- Fetched 2026-10-11. Text: [licence.txt](licence.txt).
- **Binding:**
  - The counties' open-data item `3587c7019a7142e7aee6fd970b79b4fc` ("LG_CivicAddress_OpenData", service
    `LG_CivicAddress_OpenData/FeatureServer`) has licenseInfo "Before using this data you must read and understand
    the United Counties of Leeds and Grenville's Open Data Terms of Use. Link:
    https://geohub-uclg.hub.arcgis.com/pages/terms-of-use".
  - The layer the tracker actually pulls, `CivicAddress/FeatureServer` (item `5b8385254ee94401ba03df02369e8aef`),
    has an **empty** licenseInfo.
  - Either name the open-data item as the source in the email, or switch the tracker to it.

## Structure

This is OGL-Canada 2.0 / Ottawa 2.0 in structure and wording. The "v1.0" is only the counties' own version
number, not an OGL-Ontario 1.0 or OGL-Canada 1.0 base. It has none of the Ontario variants' Records exemption or
Records definition. It matches neither OGL 1.0 Ontario nor OGL 1.0 Toronto except for the locality (Toronto compared via the Wayback capture of 2024-12-23, https://web.archive.org/web/20241223193002/https://open.toronto.ca/open-data-license/ ; the live page returned 404 on 2026-10-11. Toronto adds an MFIPPA+PHIPA exemption and an MFIPPA "Records" definition.) The useful
second argument is that it is Ottawa 2.0 itself, apart from the locality and the defects below.

## Differences from Ottawa 2.0

| # | Ottawa 2.0 | Leeds and Grenville v1.0 | Category |
|---|---|---|---|
| 1 | Introduction: "This licence is based on version 2.0 of the Open Government Licence – Canada … The only substantive changes …" | Dropped. The page starts "Terms of Use" / "Using Information under this licence:" | OTHER (non-operative preamble dropped; no effect on terms) |
| 2 | "This licence does not grant you any right to use:" | "This licence does not grant you any right use:" | OTHER (typo: missing "to"; meaning unchanged) |
| 3 | "Third party rights the Information Provider is not authorized to license;" / "licensed “as is”" | "…authorized to licence;" / "licenced "as is"" | Cosmetic spelling |
| 4 | "…loss, injury or damage caused by its use or otherwise arising in connection with this licence…" | "…loss, injury or damage caused by its **user** or otherwise arising in connection with this licence…" | OTHER (typo). Read literally it changes the liability-exclusion wording, but only the Provider's own protection; nothing new for users. |
| 5 | "Information" means information **resources** protected by copyright or other information that is offered for use under the terms of this licence. | "Information" means information protected by copyright or other information that is offered for use under the terms of this licence. | OTHER (drops "resources"; the scope is the same in practice, since "or other information" still catches everything offered) |
| 6 | "Personal Information" means "**personal information**" as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act. | "Personal Information" means "**perfect information**" as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act. | **OTHER: defective PII definition.** Same statute and section as Ottawa, so the intended meaning is clear, but MFIPPA defines no "perfect information". Read literally, the Personal Information exemption has no content, which if anything is more permissive. It is still a typo in a definition, not a category-3 alignment. |
| 7 | "You" means the natural or legal person, or body of persons corporate **or incorporate**, acquiring rights under this licence. | "You" means the natural or legal person, or body of persons corporate, acquiring rights under this licence. | **OTHER: narrower licensee definition** on paper. It drops unincorporated groups; natural persons (mappers) and legal persons (OSMF) are still covered. |
| 8 | "Information Provider" means City of Ottawa. / attribution "…City of Ottawa." / "version 2.0 of the Open Government Licence – City of Ottawa" | "means United Counties of Leeds and Grenville." / "…United Counties of Leeds and Grenville." / "version 1.0 of the Open Government Licence - United Counties of Leeds and Grenville" | 1 (locality). Version label 1.0 vs 2.0 is only a label. |
| 9 | Headings without colons ("Exemptions", "Governing law") | Headings with colons; "Non-Endorsement"; "Information Providers" capitalised | Cosmetic |

These match Ottawa 2.0 word for word: grant (including commercial use), freedoms, attribution mechanism,
termination, the four exemptions, non-endorsement, "as is" disclaimer, governing law **and venue** ("Legal
proceedings related to this licence may only be brought in the courts of Ontario."), and Versioning.

**More permissive than Ottawa:** possibly #6, since a literal reading voids the Personal Information exemption.
I am not confident that counts, and it is plainly a typo, so I make no "more permissive" claim.

## Contributors entry (add once the LWG confirms)

```
===== Leeds and Grenville =====
OpenStreetMap data may include data provided by the United Counties of Leeds and Grenville under the [https://geohub-uclg.hub.arcgis.com/pages/terms-of-use Open Government Licence – United Counties of Leeds and Grenville].
```

## Email paragraph

Short version (paste-ready): The United Counties of Leeds and Grenville (Ontario) publish civic address points
under the "Open Government Licence – United Counties of Leeds and Grenville" v1.0
(https://geohub-uclg.hub.arcgis.com/pages/terms-of-use). Despite the "v1.0" label, it is the Ottawa Open Data
Licence 2.0 clause for clause, with the locality substituted and the same Ontario venue and MFIPPA s. 2(1)
reference. It also has drafting errors that are not among the four self-service categories: Personal
Information is defined as "perfect information", "You" omits "or incorporate", the liability exclusion reads
"caused by its user", and "any right use" is missing "to". We read these as typos with no effect on users, but
they touch definitions, so we ask the LWG to confirm before we add it to Contributors.

Long version:

The United Counties of Leeds and Grenville (Ontario) publish civic address points under the "Open Government
Licence – United Counties of Leeds and Grenville" v1.0, at https://geohub-uclg.hub.arcgis.com/pages/terms-of-use.
The address dataset's metadata names this page. Despite its "v1.0" label, the text is the Ottawa Open Data
Licence 2.0 clause for clause, with the locality substituted. It has the same exemptions, the same Ontario
venue, and Personal Information tied to MFIPPA s. 2(1). It also has drafting errors that are not among the four
self-service categories:

- Personal Information is defined as "perfect information" as defined in MFIPPA s. 2(1);
- "You" omits "or incorporate";
- the liability exclusion says "caused by its user";
- "Information" omits "resources";
- "any right use" is missing "to".

We read these as typos with no effect on users. Since they touch definitions, we are asking the LWG to confirm
before we add the licence to Contributors.
