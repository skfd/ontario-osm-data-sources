# West Parry Sound — Open Government License - Township of The Archipelago (v2)

**Verdict: UNKNOWN.** Not the self-service path: email legal-questions@osmfoundation.org and wait. Two
problems lead here, and they are independent. **Either one alone would keep this off the Contributors
page.**

Verdict words in this folder: ELIGIBLE = every difference from Ottawa 2.0 falls in categories 1–4, so the
licence can be added to Contributors and the LWG emailed afterwards. NOT ELIGIBLE / UNKNOWN = not the
self-service path; email the LWG and wait for its answer. Neither is a claim that the licence is incompatible.

1. **Text.** This is the Ontario OGL template, OGL – Canada 2.0 with an MFIPPA exemption. It is almost word for word
   the **Niagara Region OGL 2.0** (LWG-approved 2024-06-10) with the Township's name swapped in. Against Ottawa 2.0 it adds
   exemption 6(b), "Information not accessible under Ontario Municipal Freedom of Information and Protection of
   Privacy Act". That is an extra exemption, outside the four categories. The precedent for it is strong:
   - Niagara Region has the identical clause.
   - The OGL – Alberta family behind the procedure's Edmonton "records" example pairs a Records definition with
     the same kind of exemption.

   The published PDF also contains a template drafting note inside the "Records" definition (row 19), and its
   preamble says the only changes are names and jurisdiction, which is not accurate (row 1).
2. **Scope.** The licence's Information Provider is "Township of The Archipelago", one of the
   members of the West Parry Sound Geography Network (WPSGN). The tracked layer is the WPSGN-wide civic-address
   layer, with 13 `Municipality` values including Seguin, Parry Sound, McDougall, Carling, McKellar, Whitestone and
   Wasauksing. Each member maintains its own rows. A licence from the Township can only license what the Township
   holds rights in. **Nothing shows that the other members' addresses are released under it.** The licence
   is attached to **nothing** on the data side: not the service, not the ArcGIS item, not the WPSGN hub. The
   only link is the WPSGN's re3data entry.

## Sources (fetched 2026-10-11)

- Licence PDF: <https://wpsgn.ca/OpenGovernmentLicense%E2%80%93TownshipofTheArchipelago.pdf>. 3 pages, 278,446
  bytes. PDF metadata: Author Chris Mahon, Word 2010, created 2014-12-01.
- How it is linked to the data: re3data API `r3d100013016` (repository "West Parry Sound Geography Network",
  institution WPSGN) lists `dataLicenseName` "OGLC" and `dataLicenseURL`
  "http://wpsgn.ca/OpenGovernmentLicense%E2%80%93TownshipofTheArchipelago.pdf". The re3data entry was created
  2019-03-28 and last updated 2023-04-28.
- The tracked layer is `https://www.wpsgn.ca/s22/rest/services/wpsgnPublic/wpsgn_opendata/FeatureServer/0`.
  - ArcGIS item `c9053cbee22e47ceac167971a9963ed7` ("West Parry Sound Civic Addresses", owner `wpsgnet`):
    `licenseInfo` null, `accessInformation` null.
  - The service's `copyrightText` was empty when the tracker checked it on 2026-08-20.
  - On 2026-10-11 the service itself answered "Service wpsgnPublic/wpsgn_opendata/MapServer not started" (HTTP-200
    JSON error 500). That is worth knowing for the tracker, but it is unrelated to the licence.
- The wpsgn.ca home page has no licence or terms link.
- Base: `../_base/ottawa-2.0.txt`.
- Comparison twin: `../niagara-falls/licence.txt` (Niagara Region OGL 2.0, LWG-approved).
- Prior status: the licence is not on the OSMF variants list, Contributors or the wiki Canada table.

## Identity

- Exact title: **Open Government License - Township of The Archipelago**. It uses the "License" spelling throughout.
- Version: **2** ("This is version 2 of the Open Government License for Township of The Archipelago").
- Declared base: "version 2.0 of the Open Government License - Canada".
- Required attribution: "Contains information licensed under the Open Government License - Township of The
  Archipelago."

## Differences against Ottawa 2.0

Categories: **1** locality name · **2** legal venue · **3** PII definition (provincial law) · **4** "records"
definition (provincial law) · **OTHER** anything else · *trivial* (no legal effect). The last column notes
whether Niagara Region's approved text matches.

| # | Clause | Ottawa 2.0 | Archipelago v2 | Class | Same in Niagara Region (approved)? |
|---|---|---|---|---|---|
| 1 | Preamble | "This licence is based on version 2.0 of the Open Government Licence – Canada … The only substantive changes in this licence are to replace direct references to the Government of Canada with the City of Ottawa, replace a reference to the Federal Privacy Act with … MFIPPA, and remove a reference to the Federal Court of Canada." | "…is based on version 2.0 of the Open Government License - Canada … The only substantive changes to the license are references to the province of jurisdiction and the name of the public body." | OTHER (non-operative). The claim is **inaccurate**, because 6(b) and the Records definition are also substantive changes. | yes, word for word |
| 2 | Title line | (none) | "Open Government License - Township of The Archipelago" | 1 | yes (name) |
| 3 | Lead-in | (none) | "You are encouraged to use the Information that is available under this license with only a few conditions." | OTHER (non-operative) | yes |
| 4 | Spelling and numbering | "licence"; unnumbered | "license" throughout; clauses 1–13 | *trivial* | — |
| 5 | Grant | "…licence to use the Information including for commercial purposes subject to the terms below." | "…license to use the Information, including for commercial purposes, subject to the terms below." | *trivial* | yes |
| 6 | Attribution | "specified by the Information Provider(s)" / "several information providers" | "specified by the Information Provider" / "several information providers" | *trivial* | yes |
| 7 | Attribution statement | "…Open Government Licence – City of Ottawa." | "Contains information licensed under the Open Government License - Township of The Archipelago." | 1 | yes (name) |
| 8 | Termination | "the rights granted you" | "the rights granted to you" | *trivial* | yes |
| 9 | Exemptions lead-in | "This licence does not grant you any right to use:" | "This license does not grant you any right to use:" | — | Niagara says "use or access" |
| 10 | Exemption (b), **added** | (none) | "b) Information not accessible under Ontario Municipal Freedom of Information and Protection of Privacy Act." | **OTHER (extra exemption).** It cannot rest on category 4, because the clause says "Information", not "Records". In practice it withholds nothing that appears in a published address layer. | **yes, identical** ("b.Information not accessible under the Municipal Freedom of Information and Protection of Privacy Act.") |
| 11 | Exemption (c) | "Third party rights the Information Provider is not authorized to license;" | "third party rights the Information Provider is not authorized to license;" | *trivial* | yes |
| 12 | Exemption (d) | "…or other official symbols of the Information Provider" | "…or other official marks of the Information Provider" | OTHER (minor). "Official marks" is a Trademarks Act term, arguably narrower; no effect on address data. | yes |
| 13 | Non-endorsement | "your use of Information." | "your use of the Information." | *trivial* | yes |
| 14 | No warranty | "obligations and liabilities" | "obligations, and liabilities" | *trivial*. The liability paragraph is otherwise identical. | yes |
| 15 | Governing law | "governed by the laws of the Province of Ontario and the applicable laws of Canada." | "governed by the laws of Ontario and the applicable laws of Canada." | *trivial* (same jurisdiction) | yes, identical |
| 16 | Venue | "may only be brought in the courts of Ontario." | "may only be brought in the courts of Ontario" (no full stop) | — (no difference) | yes |
| 17 | Def. "Information" | "information resources protected by copyright or other information that is offered…" | "information resources or Records protected by copyright or other information or Records that are offered…" | 4 | yes |
| 18 | Def. "Personal Information" | "as defined in section 2(1) of the Ontario Municipal Freedom of Information and Protection of Privacy Act." | "has the meaning set out in Ontario Municipal Freedom of Information and Protection of Privacy Act." (no section) | 3 | Niagara cites "2(1) of Freedom of Information and Protection of Privacy Act (Ontario)", i.e. FIPPA |
| 19 | Def. "Records", **added** | (none) | ""Records" (this definition is not necessary if "Records" is omitted from clause 6B) has the meaning set out in Ontario Municipal Freedom of Information and Protection of Privacy Act." | 4 for the definition. **OTHER (drafting defect)** for the bracketed note, which is template text left in the published licence. Its condition is actually met, since 6(b) says "Information" not "Records". So the definition matters only through the "Information" definition (row 17). The note has no legal effect, but it shows the text was not finalised. | Niagara has no Records definition |
| 20 | Def. "Information Provider" | "means City of Ottawa." | "means Township of The Archipelago." | 1 | yes (name) |
| 21 | Def. "You" | identical | identical | — | yes |
| 22 | Versioning | "This is version 2.0 of the Open Government Licence – City of Ottawa." | "This is version 2 of the Open Government License for Township of The Archipelago." | 1. The rest is identical. | yes (same wording) |

**Clauses dropped compared with Ottawa:** none.
**Clauses more permissive than Ottawa:** none.
**Liability, indemnity, non-commercial or voluntary-attribution changes:** none.

The text alone would get the same verdict as Windsor and Barrie: UNKNOWN, with very strong precedent. It is closer
to an approved licence than either, because it is the Niagara Region text with the name changed and a Records
definition added.

## Scope: one township's licence on a district-wide layer

- The layer holds civic addresses for all WPSGN members (13 `Municipality` values). The licence grants rights from
  "Township of The Archipelago" only.
- The only document tying this licence to the WPSGN repository is the third-party re3data record. No WPSGN page,
  service, ArcGIS item or hub page states it.
- The likely history is that the Township drafted the licence (2014) and WPSGN adopted it as a template without
  renaming it. That is plausible, but it is not evidence.
- **Needed before any OSM use**, whatever the LWG says about the text: written confirmation from WPSGN
  (info@wpsgn.ca) that the West Parry Sound Civic Addresses layer, for all member communities, is released under this
  licence. Ideally WPSGN would publish its own licence and attach it to item c9053cbe….

## Contributors entry (do NOT paste until the LWG confirms the text AND WPSGN confirms scope)

```
===== West Parry Sound =====
OpenStreetMap data may include data provided by the West Parry Sound Geography Network under the [https://wpsgn.ca/OpenGovernmentLicense%E2%80%93TownshipofTheArchipelago.pdf Open Government License – Township of The Archipelago].
```

If WPSGN says the licence covers only the Township's own rows, the entry should instead read "…data provided by
the Township of The Archipelago under…". In that case the layer would need filtering to `Municipality =
Archipelago`.

## Email paragraph (to legal-questions@osmfoundation.org)

> West Parry Sound Geography Network (WPSGN), Ontario: the district civic-address layer is listed on re3data
> under the "Open Government License - Township of The Archipelago", version 2
> (https://wpsgn.ca/OpenGovernmentLicense%E2%80%93TownshipofTheArchipelago.pdf). Diffed against the Ottawa Open Data Licence 2.0,
> it is essentially the Niagara Region OGL 2.0 you approved on 2024-06-10, with the Township's name substituted. The differences are:
> - an added exemption 6(b), "Information not accessible under Ontario Municipal Freedom of Information and
>   Protection of Privacy Act", identical to Niagara's;
> - "official marks" for "official symbols";
> - an added MFIPPA "Records" definition, which still carries a template drafting note;
> - a PII definition by reference to MFIPPA.
>
> Could you confirm whether the MFIPPA exemption is acceptable under the "records" category? We are also asking WPSGN
> separately to confirm that a licence issued in one member township's name covers the other member communities'
> addresses in the shared layer. We will not import until both points are settled.
