# Sarnia: City of Sarnia Open Data – Terms of Use (Open Government Licence – City of Sarnia)

**Verdict: NOT ELIGIBLE (for the self-service path).** This verdict means the licence has to be emailed to the LWG and we wait for their answer. It does not mean the licence is incompatible.

The licence says "The only substantive changes to the licence are references to the province of jurisdiction and the name of the public body". That is not accurate. Compared with Ottawa 2.0, the text has four changes outside categories 1–4:

- an **added exemption** (rows 6–7)
- an **added, garbled sentence** in the liability paragraph (row 8)
- the **whole Versioning section dropped** (row 9)
- "use **or access**" in the exemptions lead (row 6)

Reviewed 2026-10-11 against `_base/ottawa-2.0.txt`, using a word-level diff and then reading both texts clause by clause.

- **Exact title:** the document is headed "City of Sarnia Open Data - Terms of Use". Below the preamble it calls itself "Open Government Licence – City of Sarnia", and the attribution statement uses that name.
- **Version:** none stated, because there is no versioning clause.
- **Sources** (same text in both; the hub page adds only a contact line):
  - licenseInfo of ArcGIS item `2ed254db85d6442a8b040213c0c6b097` ("Addresses Open Data", service `Addresses_Open_Data_AGOL`), which is the tracked layer itself: <https://www.arcgis.com/home/item.html?id=2ed254db85d6442a8b040213c0c6b097>
  - hub page <https://city-of-sarnia.hub.arcgis.com/pages/terms-of-use> (Hub Page item `4acef04992034598a45181305786d2f3`, last modified 2024-08-09)
- **Stated basis:** "based on version 2.0 of the Open Government Licence - Canada".

## Differences from Ottawa Open Data Licence 2.0

| # | Ottawa 2.0 | Sarnia | Category |
|---|---|---|---|
| 1 | Attribution: "…Open Government Licence – City of Ottawa." | "\"Contains information licensed under the Open Government Licence – City of Sarnia\"" | 1 |
| 2 | "“Information Provider” means City of Ottawa." | "\"Information Provider\" means The Corporation of the City of Sarnia." | 1 |
| 3 | Title "Open Data licence version 2.0" / "Open Government Licence – City of Ottawa" | "City of Sarnia Open Data - Terms of Use" / "Open Government Licence – City of Sarnia" | 1 (name) |
| 4 | "governed by the laws of the Province of Ontario…"; "courts of Ontario" | "governed by the laws of Ontario…"; "courts of Ontario" | 2 / editorial (same law and venue) |
| 5 | "“Information” means information resources protected by copyright or other information that is offered…" | "…information resources **or records** protected by copyright or other information **or records** that are offered…" | 4. Note that Sarnia never defines "records". The word is used without a definition, which is harmless. |
| 6 | "This licence does not grant you any right to use:" | "This licence does not grant you any right to use **or access**:" | **OTHER.** The words are added to the exemptions lead. Probably harmless, since the licence never granted access, but it is not one of the categories. |
| 7 | Exemptions (four items) | **Added (b):** "Information not available under the Municipal Freedom of Information and Protection of Privacy Act, R.S.O. 1990, c. M. 56" | **OTHER: added exemption.** It has the same shape as the exemption in LWG-approved OGL-Ontario 1.0 ("Information or Records not accessible under [FIPPA]"), but Ottawa 2.0 has no such exemption and it is not a definition. |
| 8 | Liability paragraph ends "…even if specifically advised of the possibility of such loss, injury or damage." | Adds: "**Your copying, modification, publication, translation, adaptation, distribution and any other use of the Information shall be at your sole and exclusive rights.**" | **OTHER: added sentence.** As written, it doesn't say anything clear. It is most likely a typo for "sole and exclusive **risk**", which would make it an at-your-own-risk clause that Ottawa 2.0 does not have. The LWG has to read this one, and the City should be asked to fix the wording. |
| 9 | "Versioning — This is version 2.0 of the Open Government Licence – City of Ottawa. The Information Provider may make changes… Your use of the Information will be governed by the terms of the licence in force as of the date you accessed the information." | **absent** | **OTHER: dropped clause.** There is no version number, and no rule that the terms in force when you accessed the data govern your use. That is arguably neutral, but it means later edits to the terms page cannot be tied to a version. If the licence is cleared, archive a dated copy (for example on the Wayback Machine). |
| 10 | Exemption: "other official **symbols**"; "not authorized to license" | "other official **marks**"; "not authorized to licence" | OTHER, editorial ("marks" is the narrower term) |
| 11 | PI "as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act" | "has the meaning set out in 2(1) of the Municipal Freedom of Information and Protection of Privacy Act, R.S.O. 1990, c. M. 56" | Same statute and section. **Not a substantive difference.** |
| 12 | Introduction (based on OGL-Canada 2.0; lists the three changes Ottawa made) | "Preamble: … The only substantive changes to the licence are references to the province of jurisdiction and the name of the public body." | OTHER, editorial: non-operative, and its claim is inaccurate (see rows 6–9) |
| 13 | (absent); "Information Provider(s)"; "the rights granted you"; "your use of Information" | "You are encouraged to use the Information… with only a few conditions."; "Information Provider"; "granted to you"; "use of the Information" | OTHER, editorial |

**Checked and unchanged from Ottawa 2.0:**
- the grant: worldwide, royalty-free, perpetual, non-exclusive, commercial use allowed
- the freedoms
- attribution
- termination only on breach
- the other four exemptions
- non-endorsement
- the "as is" paragraph
- governing law and venue
- the "You" definition

**Not present in Sarnia's text:** no indemnity, no revocation at will, no non-commercial limit.

## About the OSM wiki note: "Not accepted for import into OSM due to name and licence text being different" (2026-02-24)

**Where the note came from:**
- User **Jarek** added the whole Sarnia row to the [Canada](https://wiki.openstreetmap.org/wiki/Canada#Open_Data) table in revision 2957778, 2026-02-25 01:58 UTC (2026-02-24 local time), with the summary "add link to Sarnia open data portal". The Sarnia row is not in revision 2955216, just before it.
- The status text is **the same boilerplate used on seven rows**: Saint John, Niagara Falls, Oakville, Sarnia, Greater Sudbury, Welland and Windsor.
- It is still on **Oakville's** row even though the LWG listed Oakville as compatible on 2026-09-14, so it is clearly not kept up to date with LWG decisions.
- No LWG minutes are cited for Sarnia, and Sarnia does not appear on the OSMF variants page.

**What the note means:** it is a wiki editor's shorthand for "this licence's name and text differ from the approved variants, so it is not covered by an existing approval". It is **not a recorded LWG rejection**.

**Is it right?**
- **Substantively yes:** this review confirms the text differs from Ottawa 2.0 beyond the four self-service categories (rows 6–9). So Sarnia cannot be self-cleared and needs the LWG.
- **But it overstates:** "Not accepted" reads like a decision, and none has been made. Once the LWG answers, the row should be updated to cite their decision.

## Contributors entry (do not add until the LWG replies)

Place it under `==== Ontario ====`, between Quinte West and Thunder Bay:

```
===== Sarnia =====
OpenStreetMap data may include data provided by the City of Sarnia under the [https://city-of-sarnia.hub.arcgis.com/pages/terms-of-use Open Government Licence – City of Sarnia].
```

## Email paragraph (legal-questions@osmfoundation.org)

> The City of Sarnia publishes its address points under "City of Sarnia Open Data – Terms of Use", which calls itself the "Open Government Licence – City of Sarnia" (https://city-of-sarnia.hub.arcgis.com/pages/terms-of-use; the same text is in the item licence of the address layer). It states that it is based on OGL-Canada 2.0 with only locality and province changes. Against the Ottawa Open Data Licence 2.0, the grant, attribution, termination, non-endorsement, governing-law and venue terms match, and the Personal Information definition cites the same MFIPPA s.2(1). However, there are four differences outside the self-service categories, so we are not self-clearing it:
>
> - an added exemption for "Information not available under the Municipal Freedom of Information and Protection of Privacy Act" (the same shape as OGL-Ontario 1.0's FIPPA exemption)
> - the exemptions lead reads "use or access"
> - the liability paragraph adds "Your copying, modification, publication, translation, adaptation, distribution and any other use of the Information shall be at your sole and exclusive rights", which we read as a typo for "risk"
> - the Versioning section is omitted entirely
>
> We would be grateful for the LWG's view on whether these differences affect compatibility. We also note that the Canada wiki row's "Not accepted… name and licence text being different" appears to be an editor's note rather than an LWG decision.
