# ForestWatch AI

**Neural Storm 2026 · GP-04 — Illegal Deforestation Detection**  
**Pilot geography:** Western Ghats, India

ForestWatch AI is an evidence-first, unsupervised-ML-enabled satellite screening prototype. It combines seasonally comparable Sentinel-2 vegetation observations, Sentinel-1 radar context, a historical tree-cover reference and a separate forest-loss cross-check to produce a shortlist of locations for human review.

> **Important:** A candidate flag is not confirmation of deforestation, natural-forest loss or illegal activity. Satellite change can result from harvesting, fire, storms, landslides, disease, seasonal effects or other land management. The system does not identify a responsible party or make legal conclusions.

## What is implemented

The main working workflow is in [`notebooks/forestwatch_pipeline_v2.ipynb`](notebooks/forestwatch_pipeline_v2.ipynb), designed to run in Google Colab with Google Earth Engine access.

1. Authenticate to Earth Engine and check Sentinel-2 data access.
2. Create seasonally comparable optical composites and calculate NDVI change.
3. Screen for persistent vegetation decline across 2023, 2024 and 2025.
4. Add Sentinel-1 VV/VH radar observations as complementary context.
5. Intersect persistent candidates with ESA WorldCover 2021 tree-cover class 10.
6. Group connected pixels into regions (minimum mapped area 0.1 ha) and measure regional optical/radar evidence.
7. Rank the 20 largest tree-cover-overlap regions for review.
8. Fit a StandardScaler + Isolation Forest model on up to 8,000 random valid 2021 tree-cover pixels outside the persistent-candidate mask, using a held-out calibration split using seven optical/radar features; score candidate pixels across all sampleable connected regions and create a separate ML priority order.
9. Cross-check the ML-ranked shortlist with Hansen Global Forest Change 2025 v1.13.
10. Export the top 20 regions, ML scores and Hansen fields as CSV and GeoJSON to Google Drive.

## Pilot run: observed outputs

The following values are from the pilot notebook execution outputs recorded during development. They describe screening results, not independently verified forest loss.

| Indicator | Observed pilot output |
|---|---:|
| Persistent candidate area (2023–2025 optical screen) | approximately 485.92 ha |
| Candidate area overlapping ESA WorldCover 2021 tree-cover class | approximately 413.12 ha |
| Persistent candidate area overlapping that tree-cover class | approximately 85.02% |
| Connected tree-cover-overlap regions of at least 0.1 ha | 790 |
| Largest region in the Section 11 shortlist | approximately 21.45 ha |
| Regions examined in the top-ranked shortlist | 20 |

For the top 20 regions, radar coverage was reported separately from radar support; coverage was 100% in the recorded Section 11 output, while radar support varied by region. Radar support is calculated among pixels with valid radar observations; radar coverage is reported separately. These indicators are not an accuracy score. Section 12 generates relative unsupervised ML anomaly percentiles; Section 13 reports Hansen loss-pixel fractions and approximate pixel-area sums within the shortlist geometries. Read values from the actual run rather than inferring unrecorded values.

## Data sources

- **Sentinel-2 Surface Reflectance Harmonized** — optical observations and NDVI.
- **Sentinel-1 GRD** — VV/VH radar observations used as supporting context.
- **ESA WorldCover 2021 v200** — class 10 (tree cover) used as a historical land-cover reference.
- **Hansen/UMD Global Forest Change 2025 v1.13** — independent, approximately 30 m tree-cover-loss cross-check for 2021–2025 ([official Earth Engine catalog](https://developers.google.com/earth-engine/datasets/catalog/UMD_hansen_global_forest_change_2025_v1_13)).

Dataset definitions, resolutions and limitations are described in the notebook and in [the reproducibility guide](docs/reproducibility.md).

## Run the workflow

1. Open the [ForestWatch pipeline notebook](notebooks/forestwatch_pipeline_v2.ipynb) in Google Colab.
2. Use a Google account with access to Google Earth Engine.
3. In Section 2, confirm that `PROJECT_ID` matches your registered Earth Engine Cloud project (the development project is `forestwatch-ai-2026`).
4. Run the notebook sections in order in one runtime. In particular, Section 11 creates `ranked_regions`; Sections 12–14 build the ML-ranked shortlist, Hansen cross-check and exports.
5. Complete the Earth Engine authentication prompts when asked.
6. Run Section 14 and monitor both export tasks in the Earth Engine Tasks panel. The CSV and GeoJSON files are written to the `ForestWatchAI` folder in Google Drive.

See [docs/reproducibility.md](docs/reproducibility.md) for the detailed run order and troubleshooting notes.

## Judge-facing results dashboard

The Streamlit dashboard opens with a recorded snapshot of the 20-region Section 11 pilot shortlist (`data/forestwatch_top20_snapshot.csv`). This lets the judge-facing view load without requiring Earth Engine authentication. Upload the latest CSV exported by Section 14 in the sidebar to replace that snapshot.

The dashboard supports a shortlist-size filter, scales centroid markers by candidate-region area, validates uploaded coordinates, positive area values and evidence-share ranges, and provides a CSV download of the currently displayed shortlist. When the enriched Section 14 file is uploaded, it orders the 20-region shortlist by the unsupervised ML priority rank and displays median anomaly percentiles, high-anomaly pixel shares and Hansen cross-check fields. Marker locations are centroids, not polygon boundaries. The committed fallback snapshot remains the original Section 11 area-ranked data and does not contain ML scores.

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

To use the latest run, execute notebook Sections 12–14, then upload `forestwatch_top20_candidates_with_hansen.csv` from the `ForestWatchAI` Google Drive folder using the dashboard sidebar. Section 12 adds ML anomaly fields; Section 13 adds Hansen cross-check fields; Section 14 exports both. The candidate-area metric is the sum of the displayed shortlist regions only, not the total pilot candidate area or confirmed deforested area. Use the GeoJSON export separately in a GIS viewer to inspect polygon geometries.

**ML and Hansen status:** The committed dashboard snapshot is a recorded Section 11 shortlist and does not contain ML or Hansen values. The updated Section 14 export includes Section 12 ML anomaly scores and Section 13 Hansen fields; upload `forestwatch_top20_candidates_with_hansen.csv` to display both. Anomaly percentiles are relative rankings, not probabilities. Hansen loss-pixel intersections are approximate cross-checks, not confirmed forest loss.

## Judge demo

A concise 90–120 second presentation flow is in [docs/demo_script.md](docs/demo_script.md).

## Architecture

See [docs/architecture.md](docs/architecture.md) for the processing flow and the role of each evidence source.

## Reproducible run records

Use [`docs/run_record_template.md`](docs/run_record_template.md) to record each Earth Engine run, dataset versions, thresholds, export completion and independent review notes. Fill it only with values observed in the actual run.

## Automated repository checks

A GitHub Actions workflow runs dashboard startup tests and ML unit tests, checks dashboard and ML-module Python syntax, parses every notebook Python code cell, and validates the committed 20-row pilot CSV structure, required fields, numeric values, coordinates, descending area order and radar-share ranges.

## Evaluation status

The prototype now includes an **unsupervised Isolation Forest anomaly-ranking stage**. It is fitted to a reproducible random sample of valid 2021 tree-cover optical/radar feature vectors outside the persistent-candidate mask and scores candidate pixels across all sampleable connected regions. The displayed anomaly percentile is relative to that sampled AOI reference distribution; it is not a probability, supervised class or proof of disturbance. The model has **not** been evaluated against verified ground-truth labels. No precision, recall, F1-score, accuracy, false-positive rate or confirmed-illegal-event count is claimed. A supervised evaluation requires independent reference labels and a geographically and temporally representative held-out test set.

## Limitations and responsible interpretation

- The pilot AOI is a screening area, not a complete Western Ghats monitoring boundary.
- Optical composites can be affected by clouds, haze, shadows, phenology and seasonal variation.
- Radar backscatter changes are ambiguous and are treated as supporting context, not proof.
- ESA WorldCover 2021 is a historical land-cover reference; its tree-cover class does not establish natural-forest status.
- Hansen Global Forest Change is a coarser product and its loss flag does not explain the cause of disturbance.
- Small candidate polygons may contain very few 30 m Hansen pixels, making regional percentages approximate.
- Candidate area is not equivalent to confirmed deforested area.
- Human review, local context and authoritative reference data are required before any operational or enforcement decision.

## Tools and assistance

Python, scikit-learn, Google Colab, Google Earth Engine, Sentinel-2, Sentinel-1, ESA WorldCover and Hansen Global Forest Change are used in the current workflow. ChatGPT assisted with planning, code development, debugging and documentation; reported outputs are taken from the development run rather than presented as independently audited results.

## Repository layout

```text
ForestWatch-AI/
├── data/
│   └── forestwatch_top20_snapshot.csv
├── docs/
│   ├── architecture.md
│   ├── demo_script.md
│   ├── judge_qa.md
│   ├── reproducibility.md
│   └── run_record_template.md
├── notebooks/
│   └── forestwatch_pipeline_v2.ipynb
├── app.py
├── forestwatch_ml.py
├── requirements.txt
├── tests/
│   ├── test_dashboard.py
│   └── test_forestwatch_ml.py
└── README.md
```
