# ForestWatch AI

**Neural Storm 2026 · GP-04 — Illegal Deforestation Detection**  
**Pilot geography:** Western Ghats, India

ForestWatch AI is an evidence-first satellite screening prototype. It combines seasonally comparable Sentinel-2 vegetation observations, Sentinel-1 radar context, a historical tree-cover reference and a separate forest-loss cross-check to produce a shortlist of locations for human review.

> **Important:** A candidate flag is not confirmation of deforestation, natural-forest loss or illegal activity. Satellite change can result from harvesting, fire, storms, landslides, disease, seasonal effects or other land management. The system does not identify a responsible party or make legal conclusions.

## What is implemented

The main working workflow is in [`notebooks/forestwatch_pipeline_v2.ipynb`](notebooks/forestwatch_pipeline_v2.ipynb), designed to run in Google Colab with Google Earth Engine access.

1. Authenticate to Earth Engine and check Sentinel-2 data access.
2. Create seasonally comparable optical composites and calculate NDVI change.
3. Screen for persistent vegetation decline across 2023, 2024 and 2025.
4. Add Sentinel-1 VV/VH radar observations as complementary context.
5. Intersect persistent candidates with ESA WorldCover 2021 tree-cover class 10.
6. Group connected pixels into regions (minimum mapped area 0.1 ha) and measure regional optical/radar evidence.
7. Cross-check the 20 highest-ranked regions with Hansen Global Forest Change 2025 v1.13.
8. Export the top 20 regions as CSV and GeoJSON to Google Drive.

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

For the top 20 regions, radar coverage was reported separately from radar support; coverage was 100% in the recorded Section 11 output, while radar support varied by region. These indicators are not an accuracy score. Hansen cross-check results should be read from the notebook's Section 12 output for the exact run; this README does not infer values that are not recorded here.

## Data sources

- **Sentinel-2 Surface Reflectance Harmonized** — optical observations and NDVI.
- **Sentinel-1 GRD** — VV/VH radar observations used as supporting context.
- **ESA WorldCover 2021 v200** — class 10 (tree cover) used as a historical land-cover reference.
- **Hansen/UMD Global Forest Change 2025 v1.13** — independent, approximately 30 m tree-cover-loss cross-check for 2021–2025.

Dataset definitions, resolutions and limitations are described in the notebook and in [the reproducibility guide](docs/reproducibility.md).

## Run the workflow

1. Open the [ForestWatch pipeline notebook](notebooks/forestwatch_pipeline_v2.ipynb) in Google Colab.
2. Use a Google account with access to Google Earth Engine.
3. In Section 2, confirm that `PROJECT_ID` matches your registered Earth Engine Cloud project (the development project is `forestwatch-ai-2026`).
4. Run the notebook sections in order in one runtime. In particular, Section 11 creates `ranked_regions`, which Sections 12 and 13 use.
5. Complete the Earth Engine authentication prompts when asked.
6. Run Section 13 and monitor both export tasks in the Earth Engine Tasks panel. The CSV and GeoJSON files are written to the `ForestWatchAI` folder in Google Drive.

See [docs/reproducibility.md](docs/reproducibility.md) for the detailed run order and troubleshooting notes.

## Judge-facing results dashboard

The Streamlit dashboard opens with a recorded snapshot of the 20-region Section 11 pilot shortlist (`data/forestwatch_top20_snapshot.csv`). This lets the judge-facing view load without requiring Earth Engine authentication. Upload the latest CSV exported by Section 13 in the sidebar to replace that snapshot. The map displays candidate centroids, not polygon boundaries.

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

To use the latest run, upload `forestwatch_top20_candidates.csv` from the `ForestWatchAI` Google Drive folder using the dashboard sidebar. The top-20 area metric is the sum of the shortlisted regions only, not the total pilot candidate area. The GeoJSON export can be used separately in a GIS viewer for polygon inspection.

## Judge demo

A concise 90–120 second presentation flow is in [docs/demo_script.md](docs/demo_script.md).

## Architecture

See [docs/architecture.md](docs/architecture.md) for the processing flow and the role of each evidence source.

## Evaluation status

This prototype has produced candidate regions and supporting indicators, but it has **not** been evaluated against a verified ground-truth dataset. No precision, recall, F1-score, accuracy, false-positive rate or confirmed-illegal-event count is claimed. A proper evaluation requires independent reference labels and a geographically and temporally representative test set.

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

Python, Google Colab, Google Earth Engine, Sentinel-2, Sentinel-1, ESA WorldCover and Hansen Global Forest Change are used in the current notebook workflow. ChatGPT assisted with planning, code development, debugging and documentation; reported outputs are taken from the development run rather than presented as independently audited results.

## Repository layout

```text
ForestWatch-AI/
├── notebooks/
│   └── forestwatch_pipeline_v2.ipynb
├── docs/
│   ├── architecture.md
│   └── reproducibility.md
└── README.md
```
