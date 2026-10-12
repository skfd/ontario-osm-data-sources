# Niagara Falls (tracker slug) — governed by Open Government License 2.0 (Niagara Region)

**Verdict: COVERED by Niagara Region.** No new licence needs to be diffed. The tracked layer is the
Regional Municipality of Niagara's own address-points service. Niagara Region's open-data catalogue
lists that exact FeatureServer URL under the **Open Government License 2.0 (Niagara Region)**. The
LWG has already approved that licence (minutes 2024-06-10), and it already has an entry on the OSM wiki
Contributors page (`===== Niagara Region =====`). No Contributors edit and no LWG email are needed
for this layer.

Verdict words in this folder: ELIGIBLE = every difference from Ottawa 2.0 falls in categories 1–4.
NOT ELIGIBLE / UNKNOWN = not the self-service path; email the LWG and wait. COVERED = the data
is governed by a licence the LWG has already approved, so there is nothing to diff.

## Evidence chain (all fetched 2026-10-11)

1. The tracked `data_url` is
   `https://services1.arcgis.com/WxiLK82TWf8W3O3f/arcgis/rest/services/OpenData_Address_Points/FeatureServer/43`.
   The service JSON gives `serviceItemId` `574a111cfe26426a90f1266cb5803d53` and an empty `copyrightText`. The
   service description says the points come from "the Region's address repository … updates completed by the
   Region of Niagara GIS Services staff … The dataset extent corresponds to the Region of Niagara."
2. ArcGIS item `574a111cfe26426a90f1266cb5803d53` ("Address Points"): its **owner is `niagararegion`** and its
   `orgId` is `WxiLK82TWf8W3O3f`. Its `licenseInfo` is **empty** (the hub API reports
   `structuredLicense: {type: none}`). The item is shared to the group "Niagara Region Open Data Content",
   which feeds the Region's hub site <https://open.niagararegion.ca>. The hub itself declares no terms. Its site
   item (`97c1867eea3544c8b77126413befd8cb`) has a null licenseInfo, and its header's "Terms of Use" link is a
   template placeholder (`href="#"`).
3. Portal `WxiLK82TWf8W3O3f` (`/sharing/rest/portals/WxiLK82TWf8W3O3f`): its name is **"Niagara Region"**, its
   urlKey is `NiagaraRegion` and its contact is gis@niagararegion.ca. **It is not a City of Niagara Falls
   organisation.** The task brief and the tracker's `provider = "City of Niagara Falls"` both assumed it was.
4. The ArcGIS item carries no licence, so the binding comes from Niagara Region's CKAN catalogue
   <https://niagaraopendata.ca> (API `package_search?q=address points`). Dataset **`address-points`**, organisation
   **Niagara Region**, `license_id` `open-government-license-2-0-niagara-region`, license title "Open Government
   License 2.0 (Niagara Region)", license URL
   <https://niagaraopendata.ca/pages/open-government-license-2-0-niagara-region>. Its resources include
   **exactly the tracked URL**: "ArcGIS GeoServices REST API
   https://services1.arcgis.com/WxiLK82TWf8W3O3f/arcgis/rest/services/OpenData_Address_Points/FeatureServer/43".
   The dataset metadata was modified 2026-10-07.
5. The licence text is saved in `licence.txt`. It is the same "Open Government License 2.0 (Niagara Region)" that
   the OSMF variants page lists as compatible ("Open Government License 2.0 (Niagara Region), compatible (LWG
   minutes 2024-06-10)"). The Contributors page links the same URL.

## Do not confuse with the City of Niagara Falls' own licence

The City of Niagara Falls publishes its **own** "Open Government License 2.0 (Niagara Falls)". Its licence
page is at niagara.oggtestbed.com/pages/open-government-license-2-0-niagara-falls, and the wiki Canada table
links open.niagarafalls.ca/pages/terms-of-use and marks it "Not accepted for import into OSM due to name and
licence text being different". The City has its own address layer under that licence:
`services9.arcgis.com/oMFQlUUrLd1Uh1bd/.../Niagara_Falls_Address_Points/FeatureServer/0` (CKAN
`niagara-falls-address-points`). **The tracker does not read that layer.** The City licence would need its own
diff only if someone switched to the City layer. I did not diff it here.

## Housekeeping flags (not edited)

- `ontario-address-changes/datasets/niagara-falls.toml` says `provider = "City of Niagara Falls"`, but the data
  belongs to Niagara Region (all 12 local municipalities). The slug is historical. The provider field and any
  attribution generated from it should name **Niagara Region**.
- The OSM attribution to use is the existing Niagara Region one: "Contains information licensed under the Open
  Government Licence - Niagara Region".

## Contributors entry

None needed. The existing entry covers this data:

```
===== Niagara Region =====
OpenStreetMap data may include data provided by the Niagara Region under the [https://niagaraopendata.ca/pages/open-government-license-2-0-niagara-region Open Government License 2.0 – Niagara Region].
```

## Email paragraph

Not needed, because the licence is already approved. If a note to the LWG is wanted for completeness:

> For the record: the region-wide address-points layer we use
> (services1.arcgis.com/WxiLK82TWf8W3O3f/…/OpenData_Address_Points/FeatureServer/43, ArcGIS item 574a111c…) is
> owned by Niagara Region's ArcGIS organisation. Niagara Region's open-data catalogue (niagaraopendata.ca
> dataset "address-points") lists it under the Open Government License 2.0 (Niagara Region), which you
> approved on 2024-06-10. It is already on the Contributors page. No new licence is involved. The separate
> City of Niagara Falls licence is not in play for this layer.
