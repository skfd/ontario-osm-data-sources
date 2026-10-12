# haldimand — Open Government Licence - Haldimand County v1.0

**Verdict: UNKNOWN.** Not the self-service path: email legal-questions@osmfoundation.org and wait.

Verdict words in this folder: ELIGIBLE = every difference from Ottawa 2.0 falls in categories 1–4, so the
licence can be added to Contributors and the LWG emailed afterwards. NOT ELIGIBLE / UNKNOWN = not the
self-service path; email the LWG and wait for its answer. Neither is a claim that the licence is incompatible.

Main reason: against Ottawa 2.0 the licence adds an exemption for "Information not accessible under the Ontario
Municipal Freedom of Information and Protection of Privacy Act or the Ontario Personal Health Information
Protection Act, 2004". The PHIPA part is not one of the four categories. Everything else is categories 1–4 or
cosmetic.

**Strong second argument: this is OGL 1.0 Toronto (LWG-approved 2024-04-08) with the locality changed.** The
exemption, the venue clause and the "Information" definition are word for word Toronto's. Apart from the
locality and cosmetic changes, the only differences from Toronto are:

- Haldimand defines "Records" under FIPPA, where Toronto uses MFIPPA (category 4);
- Haldimand's Personal Information citation adds "R.S.O. 1990" (category 3);
- the preamble is shorter.

The OSMF email step asks why the licence "is substantially the same as an already-approved license", and
Toronto answers that directly. Still, the procedure's test is the diff against Ottawa 2.0, and that diff
contains a non-category exemption. So the honest verdict is UNKNOWN: email first, with the Toronto comparison
up front. The LWG is very likely to approve it.

## Source

- Licence: Haldimand County Open Data hub home page, <https://opendata-haldimand.hub.arcgis.com/>. The licence is
  a markdown card on the home page, heading id `open-government-licence-haldimand-county`, and is rendered
  client-side.
- Text taken from the hub site item config:
  <https://www.arcgis.com/sharing/rest/content/items/d16c768293b74ab29ca691487dfc68fa/data?f=json>
  (`values.layout.sections[6]`; site item owner MDhald, modified 2026-04-15). The same markdown is embedded,
  URL-encoded, in the live home page HTML. In a rendered browser on 2026-10-11 the home page showed the licence, including the PHIPA exemption and the "brought against the Information Provider" venue.
- Exact title: "Open Government Licence - Haldimand County"; Versioning: "version 1.0 of the Open Government
  Licence – Haldimand County".
- Fetched 2026-10-11. Text: [licence.txt](licence.txt).
- **Metadata to explain in the email:**
  - The hub *site application* item's licenseInfo field reads "CC-BY-SA". That is metadata on the website item,
    not a data licence, but someone checking may trip over it.
  - Per-dataset licence fields are blank.
  - The tracked layer sits on the County's own ArcGIS Server
    (`gis.haldimandcounty.ca/server/rest/services/Topo/AddressPoints`), which has no item metadata.
  - So the site-wide licence on the hub home page is the only licence text that applies.

## Structure

The text is OGL-Canada 2.0 / Ottawa 2.0 in form (unnumbered headings, same clauses), with:

- an MFIPPA+PHIPA exemption added,
- a FIPPA "Records" definition,
- the Information definition widened to include Records,
- an Ontario venue clause.

**Against OGL 1.0 Toronto (LWG 2024-04-08):** the live open.toronto.ca page returned 404 on 2026-10-11, so I
compared the Wayback capture
<https://web.archive.org/web/20241223193002/https://open.toronto.ca/open-data-license/>. Haldimand is the Toronto
text with these changes:

| Toronto 1.0 | Haldimand 1.0 | Category |
|---|---|---|
| Preamble: "This licence is based on version 1.0 of the Open Government Licence – Ontario … The only substantive changes in this licence are to replace direct references to the Province of Ontario with the City of Toronto and the inclusion of a provision for the Ontario Personal Health Information Protection Act, 2004. You are encouraged to use the Information … with only a few conditions." | "You are encouraged to use the Information that is available under this licence with the following conditions." | non-operative |
| "Information Provider" means the City of Toronto; attribution "…– Toronto"; "version 1.0 of the Open Government Licence – Toronto. The Information Provider may make changes…" | "the Corporation of Haldimand County"; "…– Haldimand County"; "…– Haldimand County. The Corporation of Haldimand County may make changes…" | 1 |
| "Personal Information" … "subsection 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | same + ", R.S.O. 1990." | 3 (citation only) |
| "Records" means "Records" as defined in subsection 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act. | "Records" has the meaning of "record" as set out in the Freedom of Information and Protection of Privacy Act, R.S.O. 1990 (Ontario). | 4 (provincial statute changed MFIPPA → FIPPA) |
| "non-exclusive"; "specified by the Information Provider"; "trade-marks" | "nonexclusive"; "Information Provider(s)"; "trademarks" | cosmetic |

Word for word identical to Toronto: the MFIPPA+PHIPA exemption, "authorized to licence", the venue "brought
against the Information Provider in the courts of the Province of Ontario", and the "Information" definition
with Records.

**Against OGL 1.0 Ontario (LWG 2024-03-04):** not a match. OGL-Ontario's exemption names FIPPA only, with no
PHIPA, it defines Personal Information under FIPPA, and its venue is "in the courts of Ontario".

Other approved texts with a PHIPA exemption, checked 2026-10-11 at the URLs on the OSMF list:

- Hamilton (LWG 2024-11-18): "any information or records which are not accessible under the Municipal Freedom
  of Information and Protection of Privacy Act (Ontario) or Personal Health Information Protection Act
  (Ontario)"
- Quinte West 1.0 (LWG 2025-09-08): the same, plus "or any other act or by-law"

## Differences from Ottawa 2.0

| # | Ottawa 2.0 | Haldimand v1.0 | Category |
|---|---|---|---|
| 1 | Introduction: "This licence is based on version 2.0 of the Open Government Licence – Canada … The only substantive changes …" | "You are encouraged to use the Information that is available under this licence with the following conditions." | OTHER (non-operative preamble; drops Ottawa's statement of what was changed) |
| 2 | Exemptions: Personal Information; Third party rights …; names, crests, logos …; other IP rights. | Adds: "**Information not accessible under the Ontario Municipal Freedom of Information and Protection of Privacy Act or the Ontario Personal Health Information Protection Act, 2004;**" | **OTHER / borderline 4: added exemption.** The MFIPPA part is the usual Ontario "records not accessible" exemption (OGL-Ontario 1.0; the Oakville self-service precedent). The PHIPA part is not covered by any of the four categories; it has LWG precedent only through full review (Hamilton, Quinte West). In practice it excludes nothing that is published as open data. Address points are neither. |
| 3 | "Legal proceedings related to this licence may only be brought in the courts of Ontario." | "Legal proceedings related to this licence may only be brought against the Information Provider in the courts of the Province of Ontario." | 2 (venue). Still Ontario. "against the Information Provider" narrows which suits the clause covers and adds no obligation for users. |
| 4 | "Information" means information resources protected by copyright or other information that is offered for use under the terms of this licence. | "means information resources or Records protected by copyright or other information resources or Records that are offered for use under the terms of this licence." | 4 (records). It widens what the licence covers. |
| 5 | (no definition) | "Records" has the meaning of "record" as set out in the Freedom of Information and Protection of Privacy Act, R.S.O. 1990 (Ontario). | 4 (records, provincial law). Inconsistency: Records points at **FIPPA** (provincial government) while Personal Information and the exemption point at **MFIPPA** (municipal). Both are provincial statutes. |
| 6 | "Personal Information" means "personal information" as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act. | "“Personal Information” means “personal information” as defined in subsection 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act, R.S.O. 1990." | 3 (PII). Same statute and section as Ottawa; only the citation is longer. |
| 7 | "Information Provider" means City of Ottawa. / attribution "…City of Ottawa." / "version 2.0 of the Open Government Licence – City of Ottawa. The Information Provider may make changes …" | "means the Corporation of Haldimand County." / "…Open Government Licence – Haldimand County" / "version 1.0 of the Open Government Licence – Haldimand County. The Corporation of Haldimand County may make changes …" | 1 (locality). The version label 1.0 vs 2.0 is only a label. |
| 8 | "non-exclusive"; "authorized to license"; "trade-marks"; "the Province of Ontario" (governing law); "your use of Information"; "obligations and liabilities" | "nonexclusive"; "authorized to licence"; "trademarks"; "the province of Ontario"; "your use of the Information"; "obligations, and liabilities" | Cosmetic, no change in meaning |

Grant (including commercial use), freedoms, attribution mechanism, termination, non-endorsement, no-warranty,
governing law, "You" and the rest of Versioning otherwise match Ottawa 2.0 word for word.

**More permissive than Ottawa:** the "Information" definition also covers "Records". That widens what the
licence covers, but only because of the Records category; I would not claim "more permissive" on it.

## Contributors entry (add once the LWG confirms)

```
===== Haldimand County =====
OpenStreetMap data may include data provided by Haldimand County under the [https://opendata-haldimand.hub.arcgis.com/#open-government-licence-haldimand-county Open Government Licence – Haldimand County].
```

(The licence is a section of the hub home page. On 2026-10-11, in a rendered browser, the page showed the full
licence text and contained an element with id `open-government-licence-haldimand-county`.)

## Email paragraph

Short version (paste-ready): Haldimand County (Ontario) publishes its open data, including address points, under
the "Open Government Licence – Haldimand County" v1.0
(https://opendata-haldimand.hub.arcgis.com/#open-government-licence-haldimand-county). The text is the
LWG-approved OGL 1.0 Toronto word for word, except for the locality, a "Records" definition citing Ontario FIPPA
instead of MFIPPA, and a shorter preamble. Measured against the Ottawa 2.0 base, it keeps Toronto's extra
exemption for information not accessible under MFIPPA or the Personal Health Information Protection Act, 2004.
That exemption is outside the four self-service categories, so we ask the LWG to confirm before we add it to
Contributors.

Long version:

Haldimand County (Ontario) publishes its open data, including NG911 address points, under the "Open Government
Licence – Haldimand County" v1.0, shown on its hub home page
https://opendata-haldimand.hub.arcgis.com/#open-government-licence-haldimand-county. The text is the
LWG-approved OGL 1.0 Toronto (2024-04-08) word for word, apart from:

- locality substitutions;
- a "Records" definition that cites Ontario FIPPA instead of MFIPPA;
- a fuller citation ("R.S.O. 1990") for the MFIPPA Personal Information definition;
- a shorter preamble.

Against the Ottawa 2.0 base, though, it carries Toronto's extra exemption for "Information not accessible under
the Ontario Municipal Freedom of Information and Protection of Privacy Act or the Ontario Personal Health
Information Protection Act, 2004". That exemption is not one of the four self-service categories, although it
also appears in the approved Hamilton and Quinte West licences. We therefore ask the LWG to confirm before we
add the licence to Contributors. Please ignore the "CC-BY-SA" in the hub website item's metadata: it is not the
data licence. Per-dataset licence fields are blank, so the home-page licence governs.
