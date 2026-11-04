# Reproducibility guide

## Requirements

- Google account with Google Earth Engine access.
- A registered Google Cloud / Earth Engine project.
- Google Colab.
- Access to the public Earth Engine datasets referenced in the notebook.
- Google Drive access for Section 13 exports.

The development project ID used in the notebook is `forestwatch-ai-2026`. If running under another account, replace `PROJECT_ID` in Section 2 with a project that the account is authorized to use.

## Notebook

Open [`notebooks/forestwatch_pipeline_v2.ipynb`](../notebooks/forestwatch_pipeline_v2.ipynb) in Google Colab. Run code cells from top to bottom in the same runtime; later sections depend on variables created earlier.

## Run order

| Section | Purpose | Key dependency/output |
|---|---|---|
| 1–2 | Install Earth Engine API; authenticate and initialize | Earth Engine session and AOI |
| 3–5 | Initial optical screening and map preview | NDVI-change candidates and visual preview |
| 6 | Sentinel-1 radar comparison | VV/VH change and radar context |
| 7 | Quality-screened optical composites | Valid-observation counts and candidate layer |
| 8 | Multi-year persistence screen | `persistent_candidates` |
| 9 | Region-level evidence view | Regional evidence table |
| 10 | ESA WorldCover tree-cover reference screen | `tree_cover_persistent_candidates` |
| 11 | Connected-region shortlist and regional metrics | `ranked_regions`; radar support is calculated among valid radar-observed pixels, with coverage reported separately |
| 12 | Unsupervised ML anomaly ranking | `ml_review_regions`; StandardScaler + Isolation Forest trained on up to 8,000 random AOI samples and used to reorder the 20 largest regions |
| 13 | Hansen Global Forest Change cross-check | Per-region historical canopy and 2021–2025 loss fractions, plus approximate Hansen pixel-area sums inside ML-ranked shortlist geometries |
| 14 | CSV and GeoJSON exports | Two Earth Engine Drive export tasks containing ML and Hansen fields |

**Important dependencies:** Section 11 requires the variables produced by earlier optical/radar sections and Section 10. Section 12 requires Section 11 and the Section 6/8 optical/radar layers. Sections 13 and 14 require the ML-ranked regions and Hansen results from the current runtime.

## Export procedure

1. Run Section 13 once.
2. Open the Earth Engine Tasks panel in Colab.
3. Start or monitor the CSV and GeoJSON tasks if the interface requests it.
4. Wait until both tasks report completion.
5. Open Google Drive and locate the `ForestWatchAI` folder.
6. Confirm that the CSV and GeoJSON files exist before using them in a presentation or external map.

The CSV contains the top 20 regions ordered by Section 12 ML priority, including area rank, ML median anomaly percentile, the fraction of sampled pixels at or above the 95th anomaly percentile, pixel sample count, Hansen tree-cover mean, annual and combined loss-pixel shares, and Hansen loss-pixel area sums for 2021–2025. Radar support is the fraction among observed radar pixels; radar coverage is the fraction of the region with radar observations. Hansen loss-pixel area is a coarse-grid estimate intersected with candidate polygons, not confirmed deforested area. The GeoJSON contains the corresponding region geometries and properties. The exported data is a review shortlist, not a set of confirmed deforestation events.

## Reproducibility notes

- The notebook uses Google Earth Engine datasets; results can change as source collections are updated or as data availability changes.
- The anomaly model is unsupervised. Its percentiles are relative to the sampled AOI reference distribution and are not calibrated event probabilities.
- The ML stage only reorders the 20 largest regions selected by area in Section 11; it does not score all 790 connected regions.
- The pilot AOI and seasonal windows are defined in notebook code. Record any changes to them when comparing runs.
- Run all dependent sections in one runtime to avoid missing variables or stale server objects.
- If a runtime disconnects, rerun the notebook from Section 1 onward.
- Preserve the notebook output and record the run date, AOI, dates, dataset IDs and export completion status alongside any submitted results.
- For a fair comparison, do not silently change cloud masks, thresholds, minimum region size or date windows between runs.

## Troubleshooting

- **Earth Engine authentication or permission error:** complete the authentication prompt and confirm that the project ID is correct and Earth Engine is enabled for that project.
- **Missing variable error:** rerun the required earlier sections in the same runtime, especially Sections 8, 10 and 11.
- **No or incomplete export files:** inspect the Earth Engine Tasks panel for task status and error details; confirm Drive permissions and the destination folder.
- **Dataset or band error:** check the dataset ID and band names in the current Earth Engine Data Catalog before changing the notebook.

## Scientific and operational limits

This workflow has not been validated against an independent ground-truth sample. It does not produce a calibrated probability, accuracy score or legal conclusion. Optical decline, radar change and forest-loss layers each have their own omissions and ambiguities. The final shortlist must be treated as a set of locations for human inspection.
