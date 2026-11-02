# ForestWatch AI — judge Q&A

Use these short answers as a guide. Keep claims tied to the recorded pilot run and show the notebook output if a judge asks for a value that is not listed here.

## 1. What problem are you solving?

Forest disturbance is difficult to review over large areas. ForestWatch creates a satellite-based shortlist of locations where persistent vegetation decline is visible, so analysts can prioritize human inspection.

## 2. What is the AI contribution?

The current prototype is an automated, multi-source geospatial screening pipeline. It uses explicit change-detection and evidence-ranking rules rather than a trained machine-learning classifier. We are describing that honestly. A next research step is to build a labelled dataset from verified examples and evaluate a supervised model against held-out locations.

## 3. Which programming language did you use?

Python is the primary language in the Google Colab notebook, using the Google Earth Engine Python API. Jupyter is the notebook environment; it is not a separate programming language. The dashboard is a Streamlit Python app.

## 4. Which satellite and reference datasets are used?

- Sentinel-2 Surface Reflectance Harmonized for optical observations and NDVI.
- Sentinel-1 GRD VV/VH for complementary radar context.
- ESA WorldCover 2021 class 10 as a historical tree-cover reference.
- Hansen Global Forest Change 2025 v1.13 as a separate, coarser tree-cover-loss cross-check.

## 5. What did the pilot produce?

The recorded pilot run reported approximately 485.92 ha of persistent optical candidate pixels. Approximately 413.12 ha overlapped ESA WorldCover 2021 tree-cover class 10 (about 85.02%). The connected-region review contained 790 regions of at least 0.1 ha, from which the 20 largest were shortlisted.

These are screening outputs, not confirmed deforestation measurements.

## 6. Does 485.92 ha mean 485.92 ha of deforestation?

No. It is the approximate area flagged by the persistent vegetation-decline screen. Some flagged areas may reflect seasonal variation, plantations, harvesting, fire, storms, landslides or other land changes. Independent verification is required.

## 7. Why combine optical and radar data?

Optical NDVI provides a vegetation-condition signal but can be affected by clouds and atmosphere. Sentinel-1 radar provides a complementary observation source that can work through cloud cover. Radar change is also ambiguous, so it is supporting context—not proof.

## 8. What does radar coverage mean, and how is it different from radar support?

Coverage indicates the share of a region with usable radar observations. Support indicates the share of radar-observed pixels meeting the pipeline's exploratory radar-support condition; pixels without observations are excluded from the support denominator. A region can have full coverage but only a small share of observed pixels showing supporting change.

## 9. Why use ESA WorldCover and Hansen Global Forest Change?

WorldCover provides a historical tree-cover class reference to help focus review on areas mapped as tree cover. Hansen provides a separate, coarser loss-year reference. Section 12 sums the mapped Hansen pixel area intersecting candidate geometries and reports per-region loss-pixel fractions. These are approximate cross-check measures, not verified deforested area. Neither dataset proves natural-forest status, the cause of change or illegality.

## 10. What are the model's accuracy, precision and recall?

We do not claim these metrics. The prototype has not yet been evaluated against an independently verified ground-truth dataset. A defensible evaluation needs labelled examples, a held-out test set and a clear definition of the event being detected.

## 11. Can it identify illegal activity or who caused it?

No. Satellite imagery cannot establish legality, intent or responsibility by itself. ForestWatch only prioritizes locations for review. Any legal or enforcement decision belongs to competent authorities after independent investigation.

## 12. What happens after a region is flagged?

A reviewer checks dated imagery, local land-use context, known plantations and management activity, fire or storm history, and authoritative reference information. The CSV and GeoJSON exports are intended to support that review.

## 13. What is the current limitation?

The pilot covers a limited study area and uses exploratory thresholds. It has no ground-truth validation, and small polygons may contain few pixels in the coarser Hansen dataset. It is a prototype, not an operational alerting service.

## 14. What would you improve next?

1. Expand the pilot to a clearly defined monitoring boundary.
2. Build a verified reference dataset with domain experts.
3. Tune thresholds and evaluate on geographically separate test areas.
4. Add time-series and land-use context to reduce false positives.
5. Test the workflow with forest researchers or local authorities.

## Presentation reminders

- Say “candidate region” or “screening flag,” not “confirmed illegal deforestation.”
- Say “automated geospatial screening pipeline,” not “trained AI model.”
- Do not invent Hansen cross-check values; show the actual Section 12 notebook output if asked.
- Do not claim accuracy, precision, recall or real-time monitoring.
- Keep each answer brief, then point to the map, table or notebook evidence.
