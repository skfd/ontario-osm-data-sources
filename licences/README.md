# Licence diffs

Evidence for the OSMF self-service procedure on
<https://osmfoundation.org/wiki/OGL_Canada_and_local_variants> ("Evaluating Canadian Open Data
Licenses"): diff a municipal licence against the **Ottawa Open Data Licence 2.0**; if the only
differences are

1. references to the name of the locality,
2. the legal venue for disputes,
3. the definition of personally identifiable information (provincial law reference),
4. the definition of "records" (provincial law reference),

add the licence to the wiki Contributors page and email the explanation to the LWG
(legal-questions@osmfoundation.org). Any other difference means: email and wait.

One folder per tracker slug:

- `licence.txt` — the licence text as fetched, with source URL and fetch date on the first lines
- `verdict.md` — `ELIGIBLE` / `NOT ELIGIBLE` / `UNKNOWN`, every difference classified against
  the four categories, the Contributors entry to add, and the email paragraph

`_base/ottawa-2.0.txt` is the comparison base.

## The rule we apply (2026-10-11)

The OSMF page gives two tests. The numbered procedure lists four categories; the sentence
above it says changes "of the types the License Working Group (LWG) has previously evaluated"
are usable too. Oakville is the worked example: its licence adds an exemption for
"information protected under Ontario's [MFIPPA]" — outside the four categories — and after
it was self-listed on Contributors (2026-08-31) the LWG listed it (minutes 2026-09-14).

So: **self-service when every difference is in the four categories, or is a clause found in
a licence already on the OSMF list — and we name that licence.** Precedent clauses, checked
first-hand 2026-10-11:

| clause | already in (LWG minutes) |
|---|---|
| exemption for information not accessible under MFIPPA | Oakville (2026-09-14), Niagara Region (2024-06-10), Toronto (2024-04-08) |
| … and under PHIPA | Toronto (2024-04-08), Hamilton (2024-11-18), Quinte West (2025-09-08) |
| … "or any other act or by-law" | Quinte West (2025-09-08) |
| personal information includes PHIPA personal health information | Quinte West |
| governing law adds the municipality's by-laws | Quinte West |
| "Use" includes downloading; "Your" possessive | Quinte West |
| "official marks" for the crest/logo exemption; "use or access" | Niagara Region |
| "Records" defined by provincial FIPPA/MFIPPA | Toronto, Niagara Region (category 4) |
| cancel/suspend access without notice | Hamilton (2024-11-18) — noted, not relied on alone |

## Summary

| slug | route | why |
|---|---|---|
| dufferin | **self-service** | four categories only |
| barrie | **self-service by precedent** | + MFIPPA exemption (Oakville, Niagara Region, Toronto) |
| windsor | **self-service by precedent** | + MFIPPA exemption, "official marks" (Niagara Region) |
| haldimand | **self-service by precedent** | Toronto's approved text word for word apart from locality and law citations |
| huron | **self-service by precedent** | + MFIPPA/PHIPA exemption (Toronto, Hamilton); unused PHI definition |
| greater-sudbury | **self-service by precedent** | Quinte West's approved text: open-ended exemption, PHI, by-laws, "Use" |
| niagara-falls | covered | the layer is Niagara Region's, under the approved Niagara Region licence |
| sarnia | LWG | added "sole and exclusive rights" sentence; no Versioning clause |
| lambton | LWG | same two as Sarnia |
| frontenac | LWG | "don't rely on it for navigation, decision making or advising" |
| leeds-grenville | LWG | typos inside definitions ("perfect information") |
| lennox-addington | LWG | commercial-use grant and "Information" reworded |
| milton | LWG | third-party-rights exemption replaced by an MFIPPA s.10(1) one |
| brantford | LWG | rewritten licence: cancel without notice, claims waiver, entire agreement |
| durham | LWG | Region of Durham Open Data Licence v1.0 — a different licence family |
| west-parry-sound | LWG + WPSGN | Niagara text with template residue; one township's licence on a 13-community layer |

Layer caveats, whatever the licence: the tracker reads a layer the licence is not attached to
for **barrie** (use `Open_Data/AddressVW`), **windsor** (use `OpenDataServices/PropertyParcels`),
**milton** (`Datasets/Address_Pts`) and **leeds-grenville** (`LG_CivicAddress_OpenData`).
