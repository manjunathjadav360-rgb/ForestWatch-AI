# ForestWatch AI — judge demo script

**Target length: 90–120 seconds**

## 1. Problem and purpose (15 seconds)

"Forest disturbance can be difficult to review across large landscapes. ForestWatch AI is a satellite-informed screening prototype for the Western Ghats. It prioritizes locations for human inspection; it does not automatically declare illegal deforestation."

## 2. Show the dashboard (25 seconds)

Open the deployed Streamlit dashboard.

"After loading the Section 14 export, these are the candidate regions ordered by an unsupervised multi-sensor anomaly model. The map shows centroid locations. The table shows the model's relative anomaly percentile alongside area, optical change and radar evidence. These percentiles are calibrated against a separate held-out sample of non-candidate 2021 tree-cover pixels; they are not probabilities."

Point to the map and the top-five table. Explain that the markers are centroids, not mapped polygon boundaries.

## 3. Explain the pilot evidence (30 seconds)

"Our optical workflow compared seasonally aligned Sentinel-2 observations across 2023, 2024 and 2025. The persistence screen identified approximately 485.92 hectares of candidate pixels. About 413.12 hectares overlapped ESA WorldCover 2021 tree-cover class 10, or approximately 85.02% of the candidate area."

"After connected-region grouping and the minimum-area filter, the tree-cover-overlap candidate set contained 790 regions of at least 0.1 hectares. The ML stage scores regions with usable pixel samples and selects 20 anomaly priorities; their original area ranks remain visible for comparison."

"The updated Section 12 output shows each ML priority beside its original area rank, candidate area, sampled-pixel count and anomaly percentile. I quote only values visible in the current run."

## 4. Independent cross-check and limitations (20 seconds)

"We also fit an Isolation Forest to a random pilot-area sample using seven optical and radar features, then scored sampled pixels across the connected candidate regions. Its percentile ranks are relative anomaly measures, not event probabilities. A separate Hansen Global Forest Change cross-check provides an independent source of context. I report only values from the actual notebook run."

"These are screening candidates, not confirmed forest loss. Seasonal effects, fire, harvesting, storms and other disturbances can produce similar signals. Ground verification and reference labels are still needed."

## 5. Close (10 seconds)

"Our contribution is an evidence-first workflow that combines optical change, radar context, unsupervised multi-sensor anomaly ranking, historical tree-cover reference and an independent loss-data cross-check to help experts decide where to investigate first."

---

## Demo checklist

- Open the deployed dashboard before the presentation.
- Confirm the map and table load; keep the latest CSV export available.
- Run Sections 12–14 and keep the Colab notebook ready to show the actual ML and Section 13 Hansen outputs.
- If asked, show the architecture and reproducibility guides in the repository.
- Do not call the 485.92 ha or 413.12 ha figures confirmed deforestation.
- Do not claim accuracy, precision, recall or illegal-event detection rates; no ground-truth evaluation has been completed.
- If a judge asks about model scoring, explain that the Isolation Forest is unsupervised and its percentiles are not probabilities.
- If a judge asks about the Hansen results, show the actual Section 13 output for the run. Do not estimate or make up missing values.
