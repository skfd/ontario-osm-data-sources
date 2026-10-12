# lennox-addington — Open Government Licence - County of Lennox and Addington v2.0

**Verdict: UNKNOWN.** Not the self-service path: email legal-questions@osmfoundation.org and wait.

Verdict words in this folder: ELIGIBLE = every difference from Ottawa 2.0 falls in categories 1–4, so the
licence can be added to Contributors and the LWG emailed afterwards. NOT ELIGIBLE / UNKNOWN = not the
self-service path; email the LWG and wait for its answer. Neither is a claim that the licence is incompatible.

Main reason: two operative clauses are reworded in ways none of the four categories cover.

- **The grant** reads "licence to use the information for commercial purposes". Ottawa's word "including" is
  gone. Read literally, that narrows the grant. Clause 3 ("for any lawful purpose") pulls the other way.
- **"Information"** is redefined as "information or data protected by copyright that is expressly made available
  under the terms of this license on or through the Corporation of the County of Lennox and Addington". That
  changes what the licence covers: Ottawa's "or other information" is gone, and "expressly made available … on
  or through" the County is new.

The rest is categories 1–4 or cosmetic. I expect a favourable reading, but that is the LWG's call.

## Source

- Licence: <https://open-data-hub-lennoxaddington.hub.arcgis.com/pages/terms-of-use> (page "TERMS OF USE", County
  of Lennox & Addington Open Data Hub).
- Text taken from the Hub Page item
  <https://www.arcgis.com/sharing/rest/content/items/6445d96287b54472a993521a59a32ba8/data?f=json> (owner
  LA_County_RB, item modified 2023-11-22). Confirmed on the rendered live page on 2026-10-11: it contains "the information for commercial purposes", "expressly made available", "does not permit any right", "official marks of the Information Provider" and "version 2 of the Open Government".
- Exact title: "The Corporation of the County of Lennox and Addington Open Government Licence v.2.0". Versioning
  clause: "version 2 of the Open Government Licence - County of Lennox and Addington".
- Fetched 2026-10-11. Text: [licence.txt](licence.txt).
- **Binding:** the tracked address item `5dab3ac751e34eedbaf4660a957de53a` ("L&A County Civic Address Point
  (Public View)") has licenseInfo `<a href='https://open-data-hub-lennoxaddington.hub.arcgis.com/pages/terms-of-use'>Lennox and Addington Open Data Policy</a>`.
  It links this page under the name "Open Data Policy". That reconciles the two earlier notes (one said it names
  an "Open Data Policy", the other that it links the terms page).

## Structure

The text follows OGL-Canada 2.0 / Ottawa 2.0 clause order, numbered 1–13. It has no Records exemption or Records
definition. The opening sentence ("use and re-use … freely and flexibly") is UK-OGL-style wording rather than
OGL-Canada's. It matches neither OGL 1.0 Ontario nor OGL 1.0 Toronto apart from the locality (Toronto compared via the Wayback capture of 2024-12-23, https://web.archive.org/web/20241223193002/https://open.toronto.ca/open-data-license/ ; the live page returned 404 on 2026-10-11. Toronto adds an MFIPPA+PHIPA exemption and an MFIPPA "Records" definition.) So the only base
is Ottawa 2.0 itself.

## Differences from Ottawa 2.0

| # | Ottawa 2.0 | Lennox and Addington v2.0 | Category |
|---|---|---|---|
| 1 | Introduction: "This licence is based on version 2.0 of the Open Government Licence – Canada … The only substantive changes …" | "You are encouraged to use and re-use the Information that is available under this licence, freely and flexibly, with only a few conditions." | OTHER (non-operative preamble) |
| 2 | "The Information Provider grants you a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information **including** for commercial purposes subject to the terms below." | "2. The information provider grants you a worldwide, royalty-free, perpetual, non-exclusive licence to use the information for commercial purposes, subject to the terms below." | **OTHER: grant wording.** Without "including", the grant clause literally covers commercial purposes only. Clause 3 still says "for any lawful purpose", so the overall effect is probably unchanged, but this is not a category 1–4 edit. |
| 3 | Clauses 1–4 capitalise the defined terms "Information" / "Information Provider(s)" | Clauses 1–4 use lower-case "information" / "information provider", and "specified by the information provider" drops "(s)". Capitalised from clause 4's second paragraph on. | OTHER (defined terms used inconsistently; drafting, not substance) |
| 4 | "This licence does not grant you any right to use:" … "the names, crests, logos, or other official **symbols** of the Information Provider" | "6. This licence does not **permit** any right to use:" … "the names, crests, logos, or other official **marks** of the Information Provider" | OTHER (wording; same effect. Item d already excludes "official marks") |
| 5 | "Legal proceedings related to this licence may only be brought in the courts of Ontario." | "11. Legal proceedings related to this licence may only be brought in the courts of Province of Ontario." | 2 (venue; same place) |
| 6 | "Information" means information resources protected by copyright **or other information** that is offered for use under the terms of this licence. | "‘Information’: means information or data protected by copyright that is **expressly made available under the terms of this license on or through the Corporation of the County of Lennox and Addington**." | **OTHER: scope of "Information" redefined.** Narrower in one way: only copyright-protected material, and only what is "expressly made available … on or through" the County. Facts not under copyright fall outside the licence. In Canada, with no database right, they would be unrestricted anyway, but the change is outside categories 1–4. |
| 7 | "Personal Information" means "personal information" as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act. | "‘Personal Information’: has the meaning set out in section 2 of Municipal Freedom of Information and Protection of Privacy Act of Ontario;" | 3 (PII; same statute, cites s. 2 rather than s. 2(1)) |
| 8 | "Information Provider" means City of Ottawa. / attribution "…City of Ottawa." / "version 2.0 of the Open Government Licence – City of Ottawa" | "means the Corporation of the County of Lennox and Addington;" / "…Open Government Licence – County of Lennox and Addington." / "version 2 of the Open Government Licence - County of Lennox and Addington" | 1 (locality) |
| 9 | "You" means the natural or legal person, or body of persons corporate or incorporate, acquiring rights under this licence. | "‘you’ or ‘your’: means the natural or legal person, or body of persons corporate or incorporate, acquiring rights under this licence." | Cosmetic (adds "your") |
| 10 | Unnumbered headings | Numbered 1–13; "Use of any information" lower-case; "license"/"licence" mixed | Cosmetic |

These match Ottawa 2.0 word for word apart from case and numbering: freedoms (clause 3), the attribution
mechanism, termination, the other three exemptions, non-endorsement, the "as is" disclaimer and liability
exclusion, governing law, and the change-of-terms sentence in Versioning.

**More permissive than Ottawa:** nothing I am confident about. The narrower "Information" definition could be
argued either way.

## Contributors entry (add once the LWG confirms)

```
===== Lennox and Addington County =====
OpenStreetMap data may include data provided by the County of Lennox and Addington under the [https://open-data-hub-lennoxaddington.hub.arcgis.com/pages/terms-of-use Open Government Licence – County of Lennox and Addington].
```

## Email paragraph

Short version (paste-ready): The County of Lennox and Addington (Ontario) publishes civic address points under
its "Open Government Licence v.2.0" (https://open-data-hub-lennoxaddington.hub.arcgis.com/pages/terms-of-use),
which the address item's metadata links to. It follows the Ottawa 2.0 clauses, with the locality substituted,
Ontario venue, and Personal Information under MFIPPA s. 2. Two operative changes fall outside the four
self-service categories. The grant reads "licence to use the information for commercial purposes", without
"including", although clause 3 still allows "any lawful purpose". And "Information" is redefined as
copyright-protected "information or data … expressly made available under the terms of this license on or
through" the County. We read these as drafting variations with no added restriction, and ask the LWG to confirm
before we add it to Contributors.

Long version:

The County of Lennox and Addington (Ontario) publishes civic address points under "The Corporation of the County
of Lennox and Addington Open Government Licence v.2.0", at
https://open-data-hub-lennoxaddington.hub.arcgis.com/pages/terms-of-use. The address item's metadata links to
this page. The text follows the Ottawa 2.0 / OGL-Canada 2.0 clauses: same freedoms, attribution statement,
exemptions, disclaimer, Ontario law and venue, and Personal Information under MFIPPA s. 2. Two operative
clauses are reworded beyond the self-service categories:

- the grant reads "licence to use the information for commercial purposes", without "including", while
  clause 3 still allows use "for any lawful purpose";
- "Information" is redefined as "information or data protected by copyright that is expressly made available
  under the terms of this license on or through the Corporation of the County of Lennox and Addington".

There are also minor wording changes: "does not permit any right", "official marks", and lower-case defined
terms. We read these as drafting variations with no added restriction, and ask the LWG to confirm before we
add the licence to Contributors.
