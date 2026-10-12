# Brantford: Open Government Licence – Brantford, version 1.0

**Verdict: NOT ELIGIBLE.** This licence is not an OGL clone. It is a rewritten licence that adds several substantive clauses Ottawa 2.0 does not have:

- **revocation at will** (clause 8, row 9). This one alone defeats the "perpetual" grant.
- **a waiver of all claims** (clause 7, row 8)
- **user acknowledgements**, including "solely at your own risk" (clause 2, row 5)
- **an expanded disclaimer** that covers title and third-party IP (clause 6, row 7)
- **an express prohibition** in place of the non-endorsement carve-out (clause 5, row 6)
- **an added exemption** for records not accessible under MFIPPA or PHIPA (clause 4(b), row 4)
- **entire-agreement and non-waiver clauses** (clauses 12–13, row 12)
- **a broadened "Information Provider"** that includes the mayor, councillors and employees (row 10)

The self-service path is closed. Clause 8 is the kind of term the LWG has treated as a compatibility problem, not a formality, so this needs an LWG ruling. A realistic route is probably an explicit OSM permission from the City, like Kitchener's authorization on the wiki.

**The earlier desk note was wrong.** LICENSING.md and the 2026-08-16 memory note describe it as "clone; adds PHIPA to exemptions; venue drops Federal Court". That note came from a fetched page summary, not the text. It also matters for the LWG email the user already sent: if that email described Brantford as a clone, it should be corrected.

Reviewed 2026-10-11 against `_base/ottawa-2.0.txt`. The clauses are restructured, so this was a clause-by-clause read.

- **Exact title:** "Open Government Licence – Brantford". The heading on the hub page uses the same name; the website page heading is "Open Data Licence".
- **Version:** "This is version 1.0 of the Open Government Licence – Brantford" (clause 10).
- **Sources** (same text in both, checked word by word):
  - City website: <https://www.brantford.ca/your-government/open-data/open-data-licence/>. The URL brantford.ca/en/your-government/open-data-licence.aspx redirects here.
  - ArcGIS Hub page item `8f31590acfa3499cb8bbb0523ac40996` "Licence" (owner CoBOpenData, created 2017-05-25).
- **Link to the tracked layer:** the tracked layer `OP_Site_Addresses2` (item `8fa270cb0c174bd99b52a11260f60f15`) has licenseInfo "See Licence". The alternative layer `SiteAddress_pub` (item `15e6b987c0bc43cebaac8c15c6697fb9`) has empty licenseInfo.

## Differences from Ottawa Open Data Licence 2.0

| # | Ottawa 2.0 | Brantford v1.0 | Category |
|---|---|---|---|
| 1 | Attribution "…Open Government Licence – City of Ottawa."; "“Information Provider” means City of Ottawa." | "“Contains information licensed under the Open Government Licence – Brantford.”"; "\"Information Provider\" means The Corporation of the City of Brantford…" | 1 |
| 2 | "Legal proceedings related to this licence may only be brought in the courts of Ontario." | Cl. 11: "…all legal proceedings related to this licence may only be brought **against the Information Provider** in the courts of the Province of Ontario." | 2 (venue). The added words limit the venue rule to suits *against* the City. |
| 3 | (no "Records" definition; Information = "information resources protected by copyright or other information…") | "\"Records\" means \"Records\" as defined in subsection 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act."; Information = "information resources or Records…" | 4 |
| 4 | Exemptions: four items | Cl. 4 **adds (b):** "Information not accessible under the Ontario Municipal Freedom of Information and Protection of Privacy Act or the Ontario Personal Health Information Protection Act, 2004;" | **OTHER: added exemption.** On the PHIPA question: this is an exemption clause, not a PII definition, so it is **not category 3**. Ottawa 2.0 has no records exemption at all. |
| 5 | (none) | Cl. 2 Acknowledgement: "(a) You have capacity and authority to accept…; (b) This licence does not constitute a partnership, joint venture, or relationship of principal/agent or employer/employee…; (c) You have no authority to bind the Information Provider…; (d) **Use of the Information is solely at your own risk.**" | **OTHER: added clauses** |
| 6 | "This licence does not grant you any right to use the Information in a way that suggests any official status…" | Cl. 5: "This Licence does not permit, **and expressly prohibits** Use of the Information in a way that suggests any official status…" | **OTHER.** What was a carve-out from the grant becomes an affirmative prohibition. |
| 7 | "The Information is licensed “as is”… to the maximum extent permitted by law." | Cl. 6 adds: "**including without limitation any representations or warranties as to completeness, accuracy, currency, title, fitness for a particular use, or that the Information is free from any third party intellectual property rights.**" | **OTHER: expanded disclaimer.** It expressly disclaims title and IP non-infringement. |
| 8 | Liability paragraph ends "…even if specifically advised of the possibility of such loss, injury or damage." | Cl. 7 adds: "**You waive your right to any and all claims against the Information Provider arising either directly or indirectly from Use of the Information.**" | **OTHER: waiver of claims** (a liability clause) |
| 9 | "…if you fail to comply with any of them, the rights granted you… will end automatically." | Cl. 8 adds: "**Furthermore, the Information Provider may, in its sole discretion, cancel or suspend this license without notice and for any reason whatsoever, and in such case, You must immediately stop any Use of the Information.**" | **OTHER: revocation at will.** This contradicts the "perpetual" grant in cl. 1. It is incompatible in principle with contributing to ODbL-licensed OSM, where contributed data cannot be withdrawn on demand. **This is the critical difference.** |
| 10 | "“Information Provider” means City of Ottawa." | "…The Corporation of the City of Brantford **and includes its mayor, councillors, employees, successors and assigns.**" | **OTHER.** It widens the parties protected by the waiver (row 8) and the prohibition (row 6). |
| 11 | "“Information” means information resources protected by copyright or other information that is offered for use…" | "…offered for Use under the terms of this licence, **and which may be altered, amended, deleted, or updated at any time and from time to time, without prior notice to You.**" | **OTHER: added text.** It imposes nothing on the user, but it is not a category. |
| 12 | (none) | Cl. 12: "This licence is the entire agreement… and replaces all prior agreements…"; Cl. 13: "Failure to enforce any provisions… does not constitute a waiver…" | **OTHER: added clauses** (entire agreement, non-waiver) |
| 13 | Introduction paragraph; "You are free to: Copy, modify, publish…"; separate headings | No preamble; the grant restructured into cl. 1 with "Use" defined in cl. 9 as "to copy, modify, publish, translate, adapt, distribute or otherwise use the Information"; sections re-titled (Acknowledgement / Requirements / Warranty, Limitation of Liability, Indemnity / Termination / General) | OTHER, editorial: a structural rewrite. The scope of the grant is equivalent: worldwide, royalty-free, perpetual (in cl. 1), non-exclusive, commercial use allowed. The section is headed "Indemnity", but I found no indemnity obligation in its text. |
| 14 | PI "as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act" | "as defined in subsection 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act" | Same. **Not a difference.** |
| 15 | Versioning | Cl. 10: same mechanism, "version 1.0" | 1 |

**Unchanged from Ottawa 2.0:** the attribution requirement and default statement, the other four exemptions, the core "as is" and no-liability wording, governing law, and the "You" definition.

## Contributors entry (do NOT add: not eligible; only if the LWG or the City clears it)

Place it under `==== Ontario ====`, before Cambridge:

```
===== Brantford =====
OpenStreetMap data may include data provided by the City of Brantford under the [https://www.brantford.ca/your-government/open-data/open-data-licence/ Open Government Licence – Brantford].
```

## Email paragraph (legal-questions@osmfoundation.org)

This paragraph corrects or expands the earlier email:

> On closer reading, the City of Brantford's "Open Government Licence – Brantford" (version 1.0, https://www.brantford.ca/your-government/open-data/open-data-licence/) is not a straightforward OGL variant, and we are not treating it as self-service compatible. It keeps the OGL grant (worldwide, royalty-free, perpetual, non-exclusive, commercial use) and the attribution wording, but adds several terms not found in the Ottawa Open Data Licence 2.0:
>
> - clause 8 lets the City "in its sole discretion, cancel or suspend this license without notice and for any reason whatsoever", after which the user "must immediately stop any Use of the Information"
> - clause 7 adds a waiver of "any and all claims" against the City, which is defined to include its mayor, councillors and employees
> - an acknowledgement that use is "solely at your own risk", and an expanded warranty disclaimer covering title and third-party IP
> - an express prohibition on use implying endorsement
> - an exemption for information not accessible under MFIPPA or PHIPA
> - entire-agreement and non-waiver clauses
>
> We believe the revocation clause in particular needs the LWG's assessment, and we will not use Brantford data unless the LWG finds the licence compatible or the City grants explicit permission.
