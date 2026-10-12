# frontenac — County of Frontenac - Open Government Licence v1.0

**Verdict: NOT ELIGIBLE** for the OSMF self-service path. Email legal-questions@osmfoundation.org and wait.

Verdict words in this folder: ELIGIBLE = every difference from Ottawa 2.0 falls in categories 1–4, so the
licence can be added to Contributors and the LWG emailed afterwards. NOT ELIGIBLE / UNKNOWN = not the
self-service path; email the LWG and wait for its answer. Neither is a claim that the licence is incompatible.

Main reason: clause 5 adds a use restriction found in neither Ottawa 2.0 nor OGL-Ontario 1.0:
"Ensure that you do not misrepresent the information, rely on it for navigation, decision making or advising, …".
OSM data is used for navigation, so this is a substantive condition, not a locality edit.

## Source

- Licence PDF: <https://frontenac.maps.arcgis.com/sharing/rest/content/items/b8d2d338adc240c9b7d78e5f615e0652/data>
  (AGOL item `b8d2d338adc240c9b7d78e5f615e0652`, "County of Frontenac Open Data Licence", file
  `Frontenac_Open_Data_Licence.pdf`, owner FrontenacGIS, created 2024-08-21, unlisted)
- Linked as "Open Data Licence" from the Frontenac GIS hub's "Open-Data" page (Hub Page item
  `39da191d03454899a3cd02a61c7606c2`).
- Exact title: "County of Frontenac - Open Government Licence"; clause 14: "version 1.0 of the Open Government
  Licence - County of Frontenac". Preamble: "based on version 1.0 of the Open Government Licence - Ontario".
- Fetched 2026-10-11. Text: [licence.txt](licence.txt).

**Binding gap:** the tracked address layer (item `019c879661b44075b2b3f1cecbad2407`, "Civic Address Points
(Open Data View)") has an **empty** licenseInfo. The only link between the data and this licence is that the
hub's Open-Data page links the PDF. Say this in the email.

## Structure

The text is OGL-Ontario 1.0 (itself OGL-Canada 2.0 with Ontario edits), numbered 1–14, with Frontenac's
name substituted **and** clause 5 added. I compared it with the live OGL-Ontario 1.0 text at
<https://www.ontario.ca/page/open-government-licence-ontario> (fetched 2026-10-11). Apart from clause 5, the venue
wording, and the opening sentence, it matches OGL-Ontario 1.0 except for the locality. So the "matches the
LWG-approved OGL 1.0 Ontario (2024-03-04)" argument **does not work**: clause 5 is not in it. Nor is it in OGL 1.0
Toronto (2024-04-08; Wayback capture of 2024-12-23, since the live page returned 404) or in the Oakville text.

## Differences from Ottawa 2.0

| # | Ottawa 2.0 | Frontenac v1.0 | Category |
|---|---|---|---|
| 1 | Introduction: "This licence is based on version 2.0 of the Open Government Licence – Canada … The only substantive changes in this licence are to replace direct references to the Government of Canada with the City of Ottawa, …" | "This licence is based on version 1.0 of the Open Government Licence - Ontario, which was developed through public consultation and a collaborative effort by the provincial and federal government. You are encouraged to use the Information that is available under this licence with only a few conditions." | OTHER (non-operative preamble; names a different base) |
| 2 | (no equivalent) | Clause 5: "**Ensure that you do not misrepresent the information, rely on it for navigation, decision making or advising, or use it in such a way that implies any official status or endorsement from the Information Provider.**" | **OTHER: added use restriction.** The "official status or endorsement" part repeats the Non-endorsement clause; "do not misrepresent" is a new obligation; "rely on it for navigation, decision making or advising" is a new prohibition on reliance. Not in Ottawa 2.0 or OGL-Ontario 1.0. Blocks self-service. |
| 3 | Exemptions: Personal Information; Third party rights …; names, crests, logos …; other IP rights. | Adds a second bullet: "Information or Records not accessible under the Freedom of Information and Protection of Privacy Act (Ontario);" | 4 (records), with a caveat. This is the clause that uses the "Records" definition; it is word for word OGL-Ontario 1.0 (LWG-approved), and the Oakville precedent (self-service, LWG-listed 2026-09-14) carried a similar extra bullet ("information protected under Ontario's Municipal Freedom of Information and Protection of Privacy Act (MFIPPA)"). Strictly it is an added exemption, not just a definition; flag it in the email. |
| 4 | "Legal proceedings related to this licence may only be brought in the courts of Ontario." | "Legal proceedings related to this licence may only be brought against the Information Provider in the courts of the Province of Ontario." | 2 (venue). Still Ontario courts. "against the Information Provider" is not in OGL-Ontario 1.0 either (it says "brought in the courts of Ontario"). It narrows which suits the clause covers and adds no obligation for users. |
| 5 | "Information" means information resources protected by copyright or other information that is offered for use under the terms of this licence. | "means information resources or Records protected by copyright or other information resources or Records that are offered for use under the terms of this licence." | 4 (follows from adding "Records") |
| 6 | "Personal Information" means "personal information" as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act. | "has the meaning set out in section 2(1) of Freedom of Information and Protection of Privacy Act (Ontario)." | 3 (PII, provincial law). Oddity: a county is a municipal institution under **MFIPPA**, yet this cites the provincial-government **FIPPA**, copied unchanged from OGL-Ontario 1.0. |
| 7 | (no definition) | "Records" has the meaning of "record" as set out in the Freedom of Information and Protection of Privacy Act (Ontario). | 4 (records, provincial law); same FIPPA vs MFIPPA oddity |
| 8 | "Information Provider" means City of Ottawa. / attribution "…City of Ottawa." / "version 2.0 of the Open Government Licence – City of Ottawa" | "means the County of Frontenac." / "…Open Government Licence - County of Frontenac." / "version 1.0 of the Open Government Licence - County of Frontenac" | 1 (locality); version number 1.0 vs 2.0 is only the label |
| 9 | Clause headings unnumbered; "the laws of the Province of Ontario"; "warranties, obligations and liabilities"; "you or your use of Information" | Numbered 1–14; "the province of Ontario"; "warranties, obligations, and liabilities"; "your use of the Information"; "Information Providers" capitalised | Cosmetic, no change in meaning |

Grant, freedoms, attribution, termination, non-endorsement, no-warranty, governing law, "You" and versioning
otherwise match Ottawa 2.0 word for word.

**More permissive than Ottawa:** nothing.

## Contributors entry (only if the LWG confirms; do not add on self-service)

```
===== Frontenac County =====
OpenStreetMap data may include data provided by the County of Frontenac under the [https://frontenac.maps.arcgis.com/sharing/rest/content/items/b8d2d338adc240c9b7d78e5f615e0652/data Open Government Licence – County of Frontenac].
```

## Email paragraph

The County of Frontenac (Ontario) publishes civic address points under the "County of Frontenac - Open
Government Licence" v1.0 (PDF:
https://frontenac.maps.arcgis.com/sharing/rest/content/items/b8d2d338adc240c9b7d78e5f615e0652/data), which
states that it is based on OGL-Ontario 1.0 and otherwise follows it closely, including the "Information or
Records not accessible under FIPPA" exemption, the FIPPA definitions of Personal Information and Records, and
the Ontario venue clause. It adds one clause found in neither OGL-Ontario 1.0 nor the Ottawa 2.0 licence. Clause 5
requires users to "Ensure that you do not misrepresent the information, rely on it for navigation, decision making
or advising, or use it in such a way that implies any official status or endorsement". We read this as a
reliance disclaimer, but on its face it limits use, so we are asking the LWG before adding it to Contributors.
Note also that the address layer's own metadata carries no licence; the PDF is linked from the County's GIS hub
Open-Data page.
