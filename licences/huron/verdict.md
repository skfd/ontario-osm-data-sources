# Huron: Open Government Licence – The County of Huron, version 2.0

**Verdict: NOT ELIGIBLE (for the self-service path).** This verdict means the licence has to be emailed to the LWG and we wait for their answer. It does not mean the licence is incompatible.

- **Why:** the licence adds an exemption that Ottawa 2.0 does not have. Exemption 6(b) excludes "Information or records that are not accessible pursuant to" MFIPPA **and the Personal Health Information Protection Act**. It also adds a PHIPA-based "Personal Health Information" definition. Neither fits categories 1–4.
- **Why the case is strong anyway:** the same kind of exemption, paired with a "Records" definition, is in **OGL-Ontario 1.0**, which the LWG approved on 2024-03-04 ("Information or Records not accessible under the Freedom of Information and Protection of Privacy Act (Ontario)", checked on ontario.ca on 2026-10-11). It is also reportedly in the Edmonton licence that OSMF cites as its example for category 4. The PHIPA reference is the part that is new.
- Reviewed 2026-10-11 against `_base/ottawa-2.0.txt`, using a word-level diff and then reading both texts clause by clause.
- **Exact title:** "Open Government Licence - The County of Huron".
- **Version:** "version 2.0 of the Open Government Licence –The County of Huron" (clause 13).
- **Source:** licenseInfo of ArcGIS item `55ae362c840344cdb3422d496db10d64` (`Municipal_911_Address`, owner `Huron_County`), which is the tracked layer itself. Item page: <https://www.arcgis.com/home/item.html?id=55ae362c840344cdb3422d496db10d64>. No standalone licence page was found: the hub site `data-huron.opendata.arcgis.com` has no pages.
- **Stated basis:** "This licence is based on version 1.0 of the Open Government Licence – Ontario". It is **not** based on OGL-Canada 2.0 or Ottawa 2.0.

## Which data this licence covers (confirmed)

The restrictive terms on <https://www.huroncounty.ca/gis-services/> do not apply to the address layer:

- Those terms are a "Limited Licence Grant" (copies "within the Licensee's organization only", no commercial use, "must not be used or posted on an external website").
- They sit under the **"Data Requests"** heading. That heading covers consultants working under contract who ask for data in writing.
- The same page separately says "Data is now available through our Open Data Portal".

The address item is part of that open portal:

- It belongs to the ArcGIS group `b262543361b34739ba2001f644ea29fc` "Huron County - Open Data".
- That group is the catalog group of the hub site `data-huron.opendata.arcgis.com` (site item `b3f44808a42941a2b5c6474ea16d0d18`).

So the item-level open licence governs this layer.

## Differences from Ottawa Open Data Licence 2.0

| # | Ottawa 2.0 | Huron v2.0 | Category |
|---|---|---|---|
| 1 | Attribution: "…Open Government Licence – City of Ottawa." | "Contains information licensed under the Open Government Licence – The County of Huron." | 1 |
| 2 | "“Information Provider” means City of Ottawa." | "\"Information Provider\" means The County of Huron." | 1 |
| 3 | "This is version 2.0 of the Open Government Licence – City of Ottawa." | "This is version 2.0 of the Open Government Licence –The County of Huron." | 1 |
| 4 | "“Information” means information resources protected by copyright or other information that is offered…" | "\"Information\" means information resources **or records** protected by copyright or other information **or records** that are offered…" | 4 |
| 5 | (no "Records" definition) | "\"Records\" has the meaning of \"record\" as set out in section 2 of the Municipal Freedom of Information and Protection of Privacy Act (Ontario) and section 2 of the Personal Health Information Protection Act 2004 (Ontario)." | 4 (records defined by provincial law). This one cites two provincial statutes. |
| 6 | PI "as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act" | "has the meaning set out in section 2 of Municipal Freedom of Information and Protection of Privacy Act (Ontario)" | Same statute; at most category 3. **Not a substantive difference.** |
| 7 | Exemptions (four items) | **Added 6(b):** "Information or records that are not accessible pursuant to the Municipal Freedom of Information and Protection of Privacy Act (Ontario) and the Personal Health Information Protection Act (Ontario);" | **OTHER: added exemption.** This is not a definition, so it is not category 3 or 4. Precedent: OGL-Ontario 1.0 (LWG-approved) has the FIPPA version. The PHIPA part is new. In practice the exemption carves out information that could not be released under an access request, which covers nothing a county would publish as open address data. It is still a textual addition that only the LWG can clear. |
| 8 | (none) | "“Personal Health Information” has the meaning set out in section 4 of the Personal Health Information Protection Act 2004 (Ontario)." | **OTHER: added definition.** The term is never used in the operative text (exemption 6(a) says "Personal information"), so the definition has no effect. It is not an alignment of the PII definition (category 3). |
| 9 | (none) | "“Licence” means this County of Huron Open Government Licence." | OTHER, editorial: a definition with no effect |
| 10 | "“You” means the natural or legal person…" | "\"You\" or “your” means the natural or legal person…, **as applicable**, acquiring rights…" | OTHER, editorial |
| 11 | Introduction: "based on version 2.0 of the Open Government Licence – Canada… replace a reference to the Federal Privacy Act… remove a reference to the Federal Court of Canada." | "based on version 1.0 of the Open Government Licence – Ontario… the inclusion of a provision for the Ontario Personal Health Information Protection Act, 2004 and the referencing of [MFIPPA] instead of [FIPPA]." | OTHER, editorial: a non-operative preamble. It does disclose the different lineage and the PHIPA addition. |
| 12 | (absent) | "You are encouraged to use the information… with only a few conditions. Using information under this licence means:" | OTHER, editorial: a non-operative opener |
| 13 | Unnumbered; "non-exclusive"; "the rights granted you"; "your use of Information" | Numbered 1–13; "nonexclusive"; "the rights granted to you"; "your use of the information" | OTHER, editorial |

**Checked and unchanged from Ottawa 2.0:**
- the grant: worldwide, royalty-free, perpetual, commercial use allowed
- the freedoms
- the attribution mechanism, including "Information Provider(s)"
- termination only on breach
- the other four exemptions, including "official symbols"
- non-endorsement
- both no-warranty paragraphs
- governing law, and venue in "the courts of Ontario"
- the versioning mechanism

**Not present in Huron's text:** no indemnity, no waiver of claims, no revocation at will, no non-commercial limit, no dropped operative clauses.

## Contributors entry (do not add until the LWG replies)

Place it under `==== Ontario ====`, between Hamilton and Kingston:

```
===== Huron County =====
OpenStreetMap data may include data provided by the County of Huron under the [https://www.arcgis.com/home/item.html?id=55ae362c840344cdb3422d496db10d64 Open Government Licence – The County of Huron].
```

The only URL that carries the text is the ArcGIS item page. Consider asking the county for a stable licence page.

## Email paragraph (legal-questions@osmfoundation.org)

> The County of Huron publishes its 911 address points under the "Open Government Licence – The County of Huron" (version 2.0, carried in the item licence of https://www.arcgis.com/home/item.html?id=55ae362c840344cdb3422d496db10d64). The licence states that it is based on OGL-Ontario 1.0, which the LWG approved on 2024-03-04, rather than on OGL-Canada 2.0. Against the Ottawa Open Data Licence 2.0, most differences fall within the accepted categories: the locality name, the Personal Information definition (MFIPPA, the same statute Ottawa cites), and a "Records" definition (with "or records" added to the Information definition). One difference does not. Exemption 6(b) excludes "Information or records that are not accessible pursuant to" MFIPPA and the Personal Health Information Protection Act, and there is an added, unused "Personal Health Information" definition. The exemption has the same shape as OGL-Ontario 1.0's FIPPA exemption, but the PHIPA reference is new. Because this falls outside the self-service categories, we are asking the LWG to confirm compatibility and have not added Huron to the Contributors page. The grant, attribution, termination, warranty, governing-law and venue terms are otherwise identical to Ottawa 2.0. The address layer is in the county's Open Data Portal catalogue group, so the county's separate restricted licence for contracted GIS data requests does not apply to it.
