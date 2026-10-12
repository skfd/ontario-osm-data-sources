# Milton — Open Government Licence – Milton (v2.0)

**Verdict: NOT ELIGIBLE (for the self-service path).** Email legal-questions@osmfoundation.org and wait. The
licence follows Ottawa 2.0 closely, but it **rewrites one of Ottawa's exemptions**. That change is outside the
four categories, and no approved licence has the same wording.

Verdict words in this folder: ELIGIBLE = every difference from Ottawa 2.0 falls in categories 1–4, so the
licence can be added to Contributors and the LWG emailed afterwards. NOT ELIGIBLE / UNKNOWN = not the
self-service path; email the LWG and wait for its answer. Neither is a claim that the licence is incompatible.

- **The rewritten exemption.** Ottawa's exemption reads "Third party rights the Information Provider is not
  authorized to license". In Milton's 6(b) it becomes "third party information the Information Provider is not
  authorized to disclose according to Section 10(1) of the Municipal Freedom of Information and Protection of
  Privacy Act (MFIPPA), R.S.O. 1990, c.M.56".
  - MFIPPA s.10(1) covers third-party trade secrets and scientific, technical, commercial, financial or labour-relations
    information supplied in confidence. Ottawa's carve-out is about third-party *rights*, such as copyright the City
    cannot license.
  - Milton's text therefore drops the express carve-out for third-party IP and adds an access-law carve-out
    in its place.
  - This is **not confidently "more permissive"**. A licensor cannot grant rights it does not hold, so dropping the
    carve-out moves risk onto users rather than granting them more. Classified OTHER.
- **Everything else** is a category 1 or 3 change, or has no legal effect. Milton's lead-in and the web page
  around the licence (Disclaimer, Copyright) add no restriction.

**Coverage caveat.** The licence is demonstrably attached to the open-data **Address Points** item, which serves
`api.milton.ca/arcgis/rest/services/Datasets/Address_Pts/MapServer`. **The tracked layer,
`WebMaps/MGIS/MapServer/63`, is not shown to be covered.** See "What the licence covers".

## Sources (fetched 2026-10-11)

- Licence page: <https://discover-milton.hub.arcgis.com/pages/disclaimer-and-terms-of-use>.
  - The hub page is rendered by JavaScript. Its text was read from the page's content item:
    <https://www.arcgis.com/sharing/rest/content/items/66bc793c2cfa4b03874beed76f12080d/data?f=json>
    (Hub Page "Disclaimer and Terms of Use", org `FAgEZRLybpkpIX4O`, site "Discover the Town of Milton").
  - The page says "Date Modified: 2020-11-03", and the item was modified 2020-11-04.
- Base: `../_base/ottawa-2.0.txt`.
- Prior status: Milton is not on the OSMF variants list, Contributors or the wiki Canada table.

## Identity

- Exact title: **Open Government Licence – Milton**
- Version: **2.0** ("This is version 2.0 of the Open Government Licence – Milton"). The structure is OGL – Canada 2.0, like Ottawa's.
- Required attribution: "Contains information licensed under the Open Government Licence – Milton."
- Scope statement on the page: "Unless otherwise specified, all material on the Discover Milton Open Data webpage
  is made available under the Open Government Licence – Milton."

## Differences against Ottawa 2.0

Categories: **1** locality name · **2** legal venue · **3** PII definition (provincial law) · **4** "records"
definition (provincial law) · **OTHER** anything else · *trivial* (no legal effect).

| # | Clause | Ottawa 2.0 | Milton 2.0 | Class |
|---|---|---|---|---|
| 1 | Introduction | "This licence is based on version 2.0 of the Open Government Licence – Canada … The only substantive changes …" | (none) | OTHER (non-operative). The explanatory note is dropped. |
| 2 | Page wrapper (outside the licence) | — | Disclaimer: "…the Town of Milton cannot guarantee all information's completeness, accuracy, reliability, suitability or availability. Therefore any reliance you place on such information is at your own risk." Copyright: "The Town of Milton is the owner of copyright in all information found on the Discover Milton GeoHub unless otherwise stated." | OTHER (context, not licence terms). Consistent with the no-warranty clause; adds no restriction. |
| 3 | Title line | (none) | "Open Government Licence – Milton" | 1 |
| 4 | Lead-in | (none) | "The use of Discover Milton Open GeoHub is subject to the following Terms and Conditions and constitutes the user's agreement to those terms and conditions. You are encouraged to use the Information that is available under this licence with only a few conditions." | OTHER (non-operative). Acceptance-by-use wording that repeats clause 1, plus OGL boilerplate. |
| 5 | Numbering | unnumbered | 1–12 (versioning unnumbered) | *trivial* |
| 6 | Grant | "…licence to use the Information including for commercial purposes subject to the terms below." | "…licence to use the Information, including for commercial purposes, subject to the terms below." | *trivial* |
| 7 | Attribution | "If the Information Provider does not provide…" / "several information providers" | "If the information provider does not provide…" / "several Information Providers" | *trivial* (case) |
| 8 | Attribution statement | "…Open Government Licence – City of Ottawa." | "Contains information licensed under the Open Government Licence – Milton." | 1 |
| 9 | Termination | "the rights granted you" | "the rights granted to you" | *trivial* |
| 10 | Exemptions lead-in | "This licence does not grant you any right to use:" | "This licence does not permit any right to use:" | *trivial* (same effect, awkward wording) |
| 11 | Exemption (a) | "Personal Information;" | "Personal Information;" | — |
| 12 | Exemption (b), **rewritten** | "Third party rights the Information Provider is not authorized to license;" | "third party information the Information Provider is not authorized to disclose according to Section 10(1) of the Municipal Freedom of Information and Protection of Privacy Act (MFIPPA), R.S.O. 1990, c.M.56;" | **OTHER (substituted exemption).** It changes from a rights-based carve-out to an access-law carve-out (s.10(1) third-party confidential information). Third-party IP is no longer expressly excluded. It is not clearly more or less permissive. No LWG-approved twin is known. |
| 13 | Exemption (c) | "The names, crests, logos, or other official symbols of the Information Provider; and" | "the names, crests, logos, or other official symbols of the Information Provider; and" | *trivial* (case). Unlike Windsor and Niagara, Milton keeps "official symbols". |
| 14 | Exemption (d) | "Information subject to other intellectual property rights, including patents, trade-marks and official marks." | identical apart from case | *trivial* |
| 15 | Non-endorsement | "your use of Information." | "your use of the Information." | *trivial* |
| 16 | No warranty | "obligations and liabilities" | "obligations, and liabilities" | *trivial*. The liability paragraph is word-for-word identical. |
| 17 | Governing law and venue | "the laws of the Province of Ontario…" / "may only be brought in the courts of Ontario." | "the laws of the province of Ontario…" / identical | *trivial* |
| 18 | Def. "Information" | identical | identical | — |
| 19 | Def. "Information Provider" | "means City of Ottawa." | "means Town of Milton." | 1 |
| 20 | Def. "Personal Information" | "means "personal information" as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | "means "personal information" as defined in section 2 of the MFIPPA, R.S.O. 1990, c.M.56." | 3. Same statute; the definition is in s.2(1). |
| 21 | Def. "You" | identical | identical | — |
| 22 | Versioning | "This is version 2.0 of the Open Government Licence – City of Ottawa. …" | "This is version 2.0 of the Open Government Licence – Milton. …" | 1. The rest is identical. |
| 23 | Footer | — | "Date Modified: 2020-11-03" | *trivial* |

**Clauses dropped compared with Ottawa:** the non-operative introduction. In substance, the "third party rights
… not authorized to license" carve-out is gone, replaced by row 12.
**Clauses more permissive than Ottawa:** none I can state with confidence. Row 12 could be read as licensing
more third-party material, but that is an exposure for users, not a clearer grant.
**Liability, indemnity, non-commercial or voluntary-attribution changes:** none. No "Records" definition and no
MFIPPA access exemption of the Windsor/Niagara kind.

## What the licence covers

- ArcGIS item **"Address Points"** `7b543a0d714a4930a90e771db838594b` (owner Milton_Maps) has url
  `https://api.milton.ca/arcgis/rest/services/Datasets/Address_Pts/MapServer`. Its licenseInfo is a link,
  "Town of Milton Disclaimer & Terms of Use", to the page above. **This layer is demonstrably covered.**
- **Tracked layer:** `https://api.milton.ca/arcgis/rest/services/WebMaps/MGIS/MapServer/63`. It belongs to a
  web-map service, and **no catalogue item or licence statement that points at it was found**. Same host and same
  publisher, but not shown to be covered.
  - The hub's "all material on the Discover Milton Open Data webpage" covers what that page publishes. MGIS/63 is
    not among the open-data items.
  - On 2026-10-11 MGIS timed out twice ("Wait time of the request to the service 'WebMaps/MGIS.MapServer' has
    expired"), so its copyrightText could not be re-read.
- The two layers are **not drop-in twins.** `Datasets/Address_Pts/MapServer/0` (ADDRESS_PTS) has these fields:
  OBJECTID, Shape, ADDRESS_NUM, GEOSTNAME, STREET_TYPE, ST_DIR_SUFFIX, UNIT_NUMBER, BLOCK, LOT, DISPLAY_NAME,
  Address_ID, ADU, ADU_UNIT_NO.
  - It **lacks** STREET_NAME, FULL_ADDRESS, STATUS, WARD, PROP_RSN, LABEL_ANGLE, ASSIGNED_BY and HISTORY, which
    `milton.toml` maps or ignores from MGIS/63.
  - It does carry the same identity key, `Address_ID`, and ADDRESS_NUM/UNIT_NUMBER.
  - Re-pointing would need a `street` built from GEOSTNAME + STREET_TYPE + ST_DIR_SUFFIX, and the status/ward
    classes would be lost.
  - A row count could not be taken: the query returned "Error performing query operation" twice.
- **Recommendation:** for OSM use, either take the data from `Datasets/Address_Pts`, the licensed item, or get the
  Town to confirm that MGIS/63 is released under the OGL – Milton.

## Contributors entry (do NOT paste until the LWG confirms)

```
===== Milton =====
OpenStreetMap data may include data provided by the Town of Milton under the [https://discover-milton.hub.arcgis.com/pages/disclaimer-and-terms-of-use Open Government Licence – Milton].
```

## Email paragraph (to legal-questions@osmfoundation.org)

> Town of Milton, Ontario: "Open Government Licence – Milton", version 2.0, published on the Discover Milton
> open-data hub (https://discover-milton.hub.arcgis.com/pages/disclaimer-and-terms-of-use) and attached to its
> Address Points item. Diffed against the Ottawa Open Data Licence 2.0, it differs in the locality name, an
> MFIPPA-based PII definition and editorial wording. There is one substantive change outside the self-service
> categories. Ottawa's exemption for "Third party rights the Information Provider is not authorized to license"
> is replaced by "third party information the Information Provider is not authorized to disclose according to
> Section 10(1) of the Municipal Freedom of Information and Protection of Privacy Act". That swaps a carve-out
> for third-party intellectual property for an access-to-information carve-out. Could you advise whether this
> variant is compatible? All other clauses, including attribution, warranty, liability and governing law, match
> Ottawa 2.0.
