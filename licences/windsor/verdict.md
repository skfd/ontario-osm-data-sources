# Windsor — Open Government Licence - The Corporation of the City of Windsor (v1.0)

**Verdict: UNKNOWN.** Not the self-service path: email legal-questions@osmfoundation.org and wait.

Verdict words in this folder: ELIGIBLE = every difference from Ottawa 2.0 falls in categories 1–4, so the
licence can be added to Contributors and the LWG emailed afterwards. NOT ELIGIBLE / UNKNOWN = not the
self-service path; email the LWG and wait for its answer. Neither is a claim that the licence is incompatible.

**Why UNKNOWN.** The text is the OGL – Ontario 1.0 template with Windsor's name in it. The template is OGL – Canada 2.0
in structure, with numbered clauses, Definitions and Versioning. Measured against Ottawa 2.0, every difference
but one is a category 1–4 change or has no legal effect. **The exception is an added exemption:** 6(b) "Information or Records not accessible
under the Municipal Freedom of Information and Protection of Privacy Act (Ontario)". It comes paired with a
category-4 "Records" definition. The four categories cover the *definition* of records, not an added
exemption, so this falls outside the literal procedure. The precedent for it is strong:

- Niagara Region OGL 2.0 (LWG 2024-06-10) has "b. Information not accessible under the Municipal Freedom of
  Information and Protection of Privacy Act."
- Toronto (LWG 2024-04-08) and Oakville (LWG-listed 2026-09-14) have equivalent MFIPPA exemptions. This
  comes from sibling verdicts in this folder (`barrie/verdict.md`); I did not re-check it here.
- The OSMF page cites Edmonton as its example for category 4, and Edmonton descends from OGL – Alberta. OGL – Alberta pairs a
  "Record" definition with the exemption "Information or Records that are not accessible under applicable laws"
  (checked at <https://open.alberta.ca/licence>, 2026-10-11). Edmonton's own page did not render, so I could not
  quote it directly.

A second, smaller non-category change is "official marks" in place of Ottawa's "official symbols" in 6(d).
Niagara Region's approved text has the same wording.

**Coverage caveat.** The licence is demonstrably attached to the City's open-data items "Address Point" and
"Address Polygon" on `mappmycity.ca/.../OpenDataServices/PropertyParcels/MapServer/0` and `/1`. The tracker
reads a different service on the same host, `MappMyCity/AllUniqueAddresses_Parcels/MapServer/0`, which has
no licence statement. See "What the licence covers" below.

## Sources (fetched 2026-10-11)

- Licence PDF: <https://opendata.citywindsor.ca/Documents/OpenDataTermsofUse.pdf>. 2 pages, 65,324 bytes.
  PDF metadata: Title "CAO APPROVAL ONLY", Author Harry Turnbull, created 2023-01-02. The metadata title looks
  like a leftover from internal drafting; the body is a complete licence.
- The wiki Canada table links the older URL `http://www.citywindsor.ca/opendata/Documents/OpenDataTermsofUse.pdf`.
- Base: `../_base/ottawa-2.0.txt`.
- Prior status: Windsor is not on the OSMF variants list and not on Contributors. The wiki Canada Open Data table
  says "Not accepted for import into OSM due to name and licence text being different" (see below).

## Identity

- Exact title: **Open Government Licence - The Corporation of the City of Windsor**
- Version: **1.0** ("This is version 1.0 of the Open Government Licence - The Corporation of the City of Windsor").
  This is Windsor's own version counter. Ottawa's "2.0" is likewise Ottawa's own counter, which happens to match
  its OGL – Canada 2.0 base. The "1.0" does **not** mean the licence is built on OGL – Canada 1.0, which was
  structurally different. Windsor has every OGL – Canada 2.0 section: grant, free-to, attribution, termination,
  exemptions, non-endorsement, no warranty, governing law, definitions and versioning.
- Required attribution: "Contains information licensed under the Open Government Licence - The Corporation of the
  City of Windsor."

## What the wiki's "name and licence text being different" amounts to

The wiki row uses the same boilerplate sentence as several other rows, including City of Niagara Falls and Welland.
It records no LWG decision. Diffed clause by clause, the actual differences are:

- the locality name (category 1);
- the 6(b) MFIPPA exemption and the "Records" definition (OTHER and category 4);
- "official marks" (OTHER, minor);
- non-operative or editorial wording.

There is no liability, indemnity, non-commercial or attribution change.

## Differences against Ottawa 2.0

Categories: **1** locality name · **2** legal venue · **3** PII definition (provincial law) · **4** "records"
definition (provincial law) · **OTHER** anything else · *trivial* (punctuation or wording with no legal effect).

| # | Clause | Ottawa 2.0 | Windsor 1.0 | Class |
|---|---|---|---|---|
| 1 | Introduction | "This licence is based on version 2.0 of the Open Government Licence – Canada … The only substantive changes … replace direct references to the Government of Canada with the City of Ottawa …" | (no introduction) | OTHER (non-operative). An explanatory note has been dropped; no operative term is lost. |
| 2 | Title line | (none in the body) | "Open Government Licence - The Corporation of the City of Windsor" | 1 |
| 3 | Lead-in | (none) | "You are encouraged to use the Information that is available under this licence with only a few conditions." | OTHER (non-operative). OGL – Canada 2.0 boilerplate. |
| 4 | Numbering | unnumbered | clauses 1–13, exemptions a)–e) | *trivial* |
| 5 | Grant | "licence to use the Information including for commercial purposes subject to the terms below." | "licence to use the Information, including for commercial purposes, subject to the terms below." | *trivial* (commas) |
| 6 | Attribution | "several information providers" | "several Information Providers" | *trivial* (case) |
| 7 | Attribution statement | "Contains information licensed under the Open Government Licence – City of Ottawa." | "Contains information licensed under the Open Government Licence - The Corporation of the City of Windsor." | 1 |
| 8 | Termination | "the rights granted you" | "the rights granted to you" | *trivial* |
| 9 | Exemption (b), **added** | (none; Ottawa has four exemptions) | "b) Information or Records not accessible under the Municipal Freedom of Information and Protection of Privacy Act (Ontario);" | **OTHER (extra exemption).** It ties to the category-4 "Records" definition (row 17). The same clause is in LWG-approved Niagara Region 2.0 and the OGL – Alberta family. It withholds nothing that appears in a published address layer, but it is still an added exemption. |
| 10 | Exemption (c) | "Third party rights the Information Provider is not authorized to license;" | "third party rights the Information Provider is not authorized to licence;" | *trivial* (case; verb spelt "licence") |
| 11 | Exemption (d) | "The names, crests, logos, or other official symbols of the Information Provider; and" | "the names, crests, logos, or other official marks of the Information Provider; and" | OTHER (minor). "Official marks" is a term of art in the Trademarks Act and is arguably narrower than "official symbols". There is no practical effect on address data, and the same wording is in LWG-approved Niagara Region 2.0. |
| 12 | Exemption (e) | "Information subject to other intellectual property rights, including patents, trade-marks and official marks." | identical apart from case | *trivial* |
| 13 | Non-endorsement | "endorses you or your use of Information." | "endorses you or your use of the Information." | *trivial* |
| 14 | No warranty | "obligations and liabilities" | "obligations, and liabilities" | *trivial*. The liability paragraph is word-for-word identical. |
| 15 | Governing law and venue | "governed by the laws of the Province of Ontario and the applicable laws of Canada." / "may only be brought in the courts of Ontario." | "governed by the laws of the province of Ontario and the applicable laws of Canada." / identical venue sentence | *trivial* (case); no category-2 change needed |
| 16 | Def. "Information" | "information resources protected by copyright or other information that is offered for use…" | "information resources or Records protected by copyright or other information or Records that are offered for use…" | 4 (follows from adding "Records") |
| 17 | Def. "Records", **added** | (none) | ""Records" has the meaning of "record" as set out in the Municipal Freedom of Information and Protection of Privacy Act (Ontario)." | 4 |
| 18 | Def. "Information Provider" | "means City of Ottawa." | "means The Corporation of the City of Windsor." | 1 |
| 19 | Def. "Personal Information" | "means "personal information" as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | "has the meaning set out in section 2(1) of Municipal Freedom of Information and Protection of Privacy Act (Ontario)." | 3. Same statute and section, so substantively identical. |
| 20 | Def. "You" | identical | identical | — |
| 21 | Versioning | "This is version 2.0 of the Open Government Licence – City of Ottawa." | "This is version 1.0 of the Open Government Licence - The Corporation of the City of Windsor." | 1 (name and version number). The rest is identical. |

**Clauses dropped compared with Ottawa:** only the non-operative introduction (row 1).
**Clauses more permissive than Ottawa:** none.
**Liability, indemnity, non-commercial or voluntary-attribution changes:** none.

## What the licence covers

- ArcGIS org `HhXPJoZ6FLKHdvrH` is the City's new hub, <https://open-data-portal-citywindsor.hub.arcgis.com>. The
  old opendata.citywindsor.ca catalogue now says "This site is no longer being updated" and points to the hub.
  The Terms PDF still lives on the old host, and the new items link to it.
- Item **"Address Point"** `b6e438e857c74685af9ba793c5f19ead` →
  `https://mappmycity.ca/arcgis/rest/services/OpenDataServices/PropertyParcels/MapServer/0` (point layer, 133,331
  rows on 2026-10-11).
- Item **"Address Polygon"** `6793ba072d1b4103bf2a7b296ab8961c` → `…/OpenDataServices/PropertyParcels/MapServer/1`
  (polygon layer, 133,333 rows).
- Both items have the same licenseInfo: "Copyright 2025. City of Windsor (ArcGIS Online). Please be aware that by
  downloading or accessing this data, you agree to be bound by the City of Windsor's Open Data Terms of Use",
  linked to the PDF above.
- **Tracked layer:** `https://mappmycity.ca/arcgis/rest/services/MappMyCity/AllUniqueAddresses_Parcels/MapServer/0`.
  This is a polygon layer with 133,331 rows and an empty copyrightText. No catalogue item points at it, so **no
  licence statement demonstrably covers it**. It is the same host and publisher, has the same row count as the
  Address Point layer, and has the same attribute set. Its extras are the spatial-join columns
  Join_Count/TARGET_FID/JOIN_FID, plus RollNumber/created_*.
- **Recommendation:** before any OSM use, re-point the tracker to `OpenDataServices/PropertyParcels/MapServer/1`
  (Address Polygon) or `/0` (Address Point), or get the City to confirm the MappMyCity service is released
  under the same terms.

## Contributors entry (do NOT paste until the LWG confirms)

```
===== Windsor =====
OpenStreetMap data may include data provided by the City of Windsor under the [https://opendata.citywindsor.ca/Documents/OpenDataTermsofUse.pdf Open Government Licence – The Corporation of the City of Windsor].
```

## Email paragraph (to legal-questions@osmfoundation.org)

> City of Windsor, Ontario: "Open Government Licence - The Corporation of the City of Windsor", version 1.0
> (https://opendata.citywindsor.ca/Documents/OpenDataTermsofUse.pdf). It is attached to the City's ArcGIS
> "Address Point" and "Address Polygon" open-data items. We diffed it against the Ottawa Open Data Licence 2.0.
> Apart from the locality name, a provincial-law PII definition (MFIPPA s.2(1), the same as Ottawa) and an added
> MFIPPA "Records" definition, the only operative differences are these. First, an added exemption 6(b), "Information or Records not
> accessible under the Municipal Freedom of Information and Protection of Privacy Act (Ontario)". Second,
> "official marks" instead of "official symbols" in the names/crests/logos exemption. Both appear in the Niagara
> Region OGL 2.0 you approved on 2024-06-10. Niagara's exemption reads "Information not accessible under
> MFIPPA", without "or Records", but is otherwise the same. The exemption also matches the OGL – Alberta pattern behind the
> Edmonton example on your procedure page. Could you confirm whether that exemption-plus-Records pairing falls
> within the "records" category, so Windsor can be listed? The wiki Canada table's "Not accepted … name and
> licence text being different" note does not appear to reflect an LWG decision.
