# Dufferin: Open Government Licence – The County of Dufferin, version 2

**Verdict: ELIGIBLE.** Every substantive difference from Ottawa 2.0 falls in categories 1–4. Five wording differences fall outside the categories, but they are editorial and have no legal effect (rows E1–E7 below). This verdict depends on treating them as editorial. Most come from the OGL-Ontario 1.0 template (LWG-approved 2024-03-04), which this text is built from.

- Reviewed 2026-10-11 against `_base/ottawa-2.0.txt`, using a word-level diff and then reading both texts clause by clause.
- **Exact title:** "Open Government Licence - The County of Dufferin". The PDF metadata title is the same.
- **Version:** "version 2 of the Open Government Licence for the County of Dufferin" (clause 13).
- **Sources** (all three copies have the same text, checked with `diff -w`):
  - County site, linked as "Dufferin County Open Data Terms of Use" from <https://www.dufferincounty.ca/mapping/open-data/>: <https://www.dufferincounty.ca/wp-content/uploads/2024/03/Dufferin-Open-Government-License.pdf>. PDF created 2016-12-09, modified 2024-02-29. **Cite this one.**
  - ArcGIS item `fbbfe060de804d44a4e39cd51a451e35` "Dufferin Open Government License" (PDF, 2017).
  - ArcGIS item `ef6ec37af55f493ba442835b10fc15e9` "Dufferin Open Government License 2021" (PDF).

## Which data this licence covers

- **Tracked layer today** (`Dufferin_County_Entrances`, item `0a7cdf8b0e74434c82eced47538bf4f1`): the item's licenseInfo links directly to the licence PDF (item `fbbfe060…`).
- **Better address layer** (`Address_Points_DufferinCounty_Open_Data`, item `2fca5d07a8bb432b8addb7d2131e9996`):
  - Its licenseInfo is empty.
  - It belongs to the ArcGIS group `238ba174204d424f9e98778e21fc5f64` "Dufferin County Open Data".
  - The county open-data page says: "By downloading and/or using the data, you are agreeing to the Dufferin County Open Data Terms of Use". That link goes to the PDF above.
  - So the licence covers this layer too, but only through the portal-wide statement, not through an item-level licence.

## Differences from Ottawa Open Data Licence 2.0

| # | Ottawa 2.0 | Dufferin v2 | Category |
|---|---|---|---|
| 1 | Attribution: "Contains information licensed under the Open Government Licence – City of Ottawa." | "Contains information licensed under the Open Government Licence - County of Dufferin" | 1 (locality name) |
| 2 | "“Information Provider” means City of Ottawa." | "\"Information Provider\" means County of Dufferin." | 1 |
| 3 | "This is version 2.0 of the Open Government Licence – City of Ottawa." | "This is version 2 of the Open Government Licence for the County of Dufferin." | 1 (name; the version number is the licence's own) |
| 4 | "Legal proceedings related to this licence may only be brought in the courts of Ontario." | "…may only be brought in the courts of the Province of Ontario." | 2 (venue; same courts) |
| 5 | "“Personal Information” means “personal information” as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | "\"Personal Information\" has the meaning set out in section 2(1) of Freedom of Information and Protection of Privacy Act (Ontario)." | 3 (PII defined by provincial law). Note: FIPPA and MFIPPA are both Ontario statutes. FIPPA covers provincial institutions, and MFIPPA covers municipalities, so MFIPPA would have been the natural reference for a county. The wording is carried over from OGL-Ontario 1.0. Both acts define "personal information" in s.2(1) as "recorded information about an identifiable individual" followed by the same list of examples. The Ontario IPC treats the two as one definition (Interpretation Bulletin "Personal information", <https://www.ipc.on.ca/sites/default/files/documents/IB0003E-2026-08-personal-information.pdf>). I did not get the statute text from e-Laws, because the site is JS-rendered. |
| 6 | (no "Records" definition) | "\"Records\" has the meaning of \"record\" as set out in the Freedom of Information and Protection of Privacy Act (Ontario)." | 4 (records defined by provincial law) |
| 7 | "“Information” means information resources protected by copyright or other information that is offered…" | "\"Information\" means information resources **or records** protected by copyright or other information **or records** that are offered…" | 4 (this is where the records definition gets used) |
| E1 | Introduction: "This licence is based on version 2.0 of the Open Government Licence – Canada… The only substantive changes in this licence are…" | absent | OTHER, editorial: a non-operative explanatory preamble is dropped |
| E2 | (absent) | "You are encouraged to use the information that is available under this licence with only a few conditions." | OTHER, editorial: a non-operative opener. The sentence appears in both OGL-Canada 2.0 and OGL-Ontario 1.0. |
| E3 | Unnumbered paragraphs | Clauses numbered 1–13 | OTHER, editorial |
| E4 | "Exemptions — This licence does not grant you any right to use:" | "Exemptions — 6. This licence does not **permit** any right to use:" | OTHER, editorial: the meaning is unchanged (the listed items are carved out of the grant) |
| E5 | Exemption 3: "The names, crests, logos, or other official **symbols** of the Information Provider" | "the names, crests, logos, or other official **marks** of the Information Provider" | OTHER, editorial. "Official marks" is the narrower term (Trademarks Act), so if anything this exemption is narrower. It is immaterial for address data. I did not claim "more permissive". |
| E6 | "attribution statement specified by the Information Provider(s)" | "…specified by the information provider" | OTHER, editorial (singular instead of plural) |
| E7 | "the rights granted you"; "your use of Information"; "obligations and liabilities" | "the rights granted to you"; "your use of the Information"; "obligations, and liabilities" | OTHER, editorial (grammar and punctuation) |

**Checked and unchanged from Ottawa 2.0:**
- the grant: worldwide, royalty-free, perpetual, non-exclusive, commercial use allowed
- the freedoms list
- automatic termination only on breach
- **the exemption list.** It has exactly Ottawa's four items: Personal Information, third-party rights, names/crests/logos, other IP. It does **not** add OGL-Ontario's "records not accessible under FIPPA" exemption.
- non-endorsement
- both no-warranty paragraphs
- governing law
- the "You" definition
- the versioning mechanism

**Not present in Dufferin's text:**
- no added exemptions
- no added restrictions
- no indemnity or waiver
- no non-commercial limit
- no revocation-at-will clause
- no clauses dropped beyond the non-operative preamble

**Correction to the earlier desk note.** LICENSING.md says this text "omits the not-accessible-records exemption (more permissive)". That comparison is against OGL-Ontario 1.0. Against Ottawa 2.0, which is the procedure's base, the exemption lists are the same, so it is **not** more permissive than Ottawa.

## Contributors entry

Place it under `==== Ontario ====`, between Cornwall and Guelph:

```
===== Dufferin County =====
OpenStreetMap data may include data provided by the County of Dufferin under the [https://www.dufferincounty.ca/wp-content/uploads/2024/03/Dufferin-Open-Government-License.pdf Open Government Licence – The County of Dufferin].
```

## Email paragraph (legal-questions@osmfoundation.org)

Dufferin was already in the LWG email the user sent, which has had no reply. Send this paragraph as a follow-up to that email, and only **after** making the Contributors edit, because it says the entry has been added.

> The County of Dufferin's "Open Government Licence – The County of Dufferin" (version 2, https://www.dufferincounty.ca/wp-content/uploads/2024/03/Dufferin-Open-Government-License.pdf) is substantially the same as the Ottawa Open Data Licence 2.0. A clause-by-clause diff shows the same grant (worldwide, royalty-free, perpetual, non-exclusive, commercial use permitted), the same attribution and termination terms, the same four exemptions, and the same non-endorsement, warranty and governing-law clauses. The substantive differences are the locality name (County of Dufferin), the venue wording ("courts of the Province of Ontario"), Personal Information defined by reference to s.2(1) of Ontario's Freedom of Information and Protection of Privacy Act, and an added "Records" definition from the same Act (with "or records" added to the Information definition). These all fall within the categories listed on the OGL Canada and local variants page. The remaining differences are editorial: no explanatory preamble, numbered clauses, the OGL-Ontario 1.0 opener "You are encouraged to use…", "does not permit any right" instead of "does not grant you any right", and "official marks" instead of "official symbols". We have therefore added it to the Contributors page and would be grateful if the Canada page could be updated.
