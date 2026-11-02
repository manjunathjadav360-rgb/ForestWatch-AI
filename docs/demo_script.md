# ForestWatch AI — judge demo script

**Target length: 90–120 seconds**

## 1. Problem and purpose (15 seconds)

"Forest disturbance can be difficult to review across large landscapes. ForestWatch AI is a satellite-informed screening prototype for the Western Ghats. It prioritizes locations for human inspection; it does not automatically declare illegal deforestation."

## 2. Show the dashboard (25 seconds)

Open the deployed Streamlit dashboard.

"These are the 20 largest regions from our recorded pilot shortlist. The map shows their centroid locations. The table lets a reviewer compare region area, vegetation-index change and radar evidence."

Point to the map and the top-five table. Explain that the markers are centroids, not mapped polygon boundaries.

## 3. Explain the pilot evidence (30 seconds)

"Our optical workflow compared seasonally aligned Sentinel-2 observations across 2023, 2024 and 2025. The persistence screen identified approximately 485.92 hectares of candidate pixels. About 413.12 hectares overlapped ESA WorldCover 2021 tree-cover class 10, or approximately 85.02% of the candidate area."

"After connected-region grouping and the minimum-area filter, the tree-cover-overlap shortlist contained 790 regions of at least 0.1 hectares. We ranked them for review and exported the top 20."

"The largest shortlisted region is approximately 21.45 hectares. Its mean NDVI drop indicators were 0.538 for 2024 and 0.545 for 2025. Radar support was 20.9%, while radar coverage was 100%—coverage and support are different measures."

## 4. Independent cross-check and limitations (20 seconds)

"We also added a separate Hansen Global Forest Change cross-check for the top 20 regions. We report its observed table values from the actual notebook run rather than inventing a summary score."

"These are screening candidates, not confirmed forest loss. Seasonal effects, fire, harvesting, storms and other disturbances can produce similar signals. Ground verification and reference labels are still needed."

## 5. Close (10 seconds)

"Our contribution is an evidence-first workflow that combines optical change, radar context, historical tree-cover reference and an independent loss-data cross-check to help experts decide where to investigate first."

---

## Demo checklist

- Open the deployed dashboard before the presentation.
- Confirm the map and table load; keep the latest CSV export available.
- Keep the Colab notebook ready in another tab for the Section 12 Hansen cross-check.
- If asked, show the architecture and reproducibility guides in the repository.
- Do not call the 485.92 ha or 413.12 ha figures confirmed deforestation.
- Do not claim accuracy, precision, recall or illegal-event detection rates; no ground-truth evaluation has been completed.
- If a judge asks about the Hansen results, show the actual Section 12 output for the run. Do not estimate or make up missing values.
