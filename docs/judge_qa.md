# ForestWatch AI — judge Q&A

Use these short answers as a guide. Keep claims tied to the recorded pilot run and show the notebook output if a judge asks for a value that is not listed here.

## 1. What problem are you solving?

Forest disturbance is difficult to review over large areas. ForestWatch creates a satellite-based shortlist of locations where persistent vegetation decline is visible, so analysts can prioritize human inspection.

## 2. What is the AI contribution?

The prototype combines explicit satellite change screening with an unsupervised machine-learning stage. A StandardScaler + Isolation Forest model is fitted to a reproducible random sample of non-candidate 2021 tree-cover pixels in the pilot AOI using seven features: NDVI drops in 2024 and 2025, 2025-vs-2024 NDVI change, Sentinel-1 VV and VH change, a radar-support flag, and a radar-availability flag. It scores pixels across all sampleable connected candidate regions and orders those regions by median anomaly percentile before selecting the final 20 priorities. This is relative anomaly ranking, not a supervised forest-loss classification or a probability of illegal activity.

## 3. How was the ML model trained, and what does its score mean?

The model is unsupervised: it learns the feature distribution from up to 8,000 randomly sampled valid 2021 tree-cover pixels outside the persistent-candidate mask. The sample is split into model-fit and held-out calibration subsets. Candidate pixels are compared with the held-out calibration score distribution. A higher percentile means a more unusual multi-sensor feature pattern relative to the sample. No human labels are used, and the percentile is not a probability of deforestation.

## 4. Which programming language did you use?

Python is the primary language in the Google Colab notebook, using the Google Earth Engine Python API. Jupyter is the notebook environment; it is not a separate programming language. The dashboard is a Streamlit Python app.

## 5. Which satellite and reference datasets are used?

- Sentinel-2 Surface Reflectance Harmonized for optical observations and NDVI.
- Sentinel-1 GRD VV/VH for complementary radar context.
- ESA WorldCover 2021 class 10 as a historical tree-cover reference.
- Hansen Global Forest Change 2025 v1.13 as a separate, coarser tree-cover-loss cross-check.

## 6. What did the pilot produce?

The recorded pilot run reported approximately 485.92 ha of persistent optical candidate pixels. Approximately 413.12 ha overlapped ESA WorldCover 2021 tree-cover class 10 (about 85.02%). The connected-region review contained 790 regions of at least 0.1 ha, from which the 20 largest were shortlisted.

These are screening outputs, not confirmed deforestation measurements.

## 7. Does 485.92 ha mean 485.92 ha of deforestation?

No. It is the approximate area flagged by the persistent vegetation-decline screen. Some flagged areas may reflect seasonal variation, plantations, harvesting, fire, storms, landslides or other land changes. Independent verification is required.

## 8. Why combine optical and radar data?

Optical NDVI provides a vegetation-condition signal but can be affected by clouds and atmosphere. Sentinel-1 radar provides a complementary observation source that can work through cloud cover. Radar change is also ambiguous, so it is supporting context—not proof.

## 9. What does radar coverage mean, and how is it different from radar support?

Coverage indicates the share of a region with usable radar observations. Support indicates the share of radar-observed pixels meeting the pipeline's exploratory radar-support condition; pixels without observations are excluded from the support denominator. A region can have full coverage but only a small share of observed pixels showing supporting change.

## 10. Why use ESA WorldCover and Hansen Global Forest Change?

WorldCover provides a historical tree-cover class reference to help focus review on areas mapped as tree cover. Hansen provides a separate, coarser loss-year reference. Section 13 sums the mapped Hansen pixel area intersecting candidate geometries and reports per-region loss-pixel fractions. These are approximate cross-check measures, not verified deforested area. Neither dataset proves natural-forest status, the cause of change or illegality.

## 11. What are the model's accuracy, precision and recall?

We do not claim these metrics. The Isolation Forest is unsupervised and has not been evaluated against an independently verified ground-truth dataset. A defensible supervised evaluation needs labelled examples, a geographically held-out test set and a clear definition of the event being detected.

## 12. Can it identify illegal activity or who caused it?

No. Satellite imagery cannot establish legality, intent or responsibility by itself. ForestWatch only prioritizes locations for review. Any legal or enforcement decision belongs to competent authorities after independent investigation.

## 13. What happens after a region is flagged?

A reviewer checks dated imagery, local land-use context, known plantations and management activity, fire or storm history, and authoritative reference information. The CSV and GeoJSON exports are intended to support that review.

## 14. What is the current limitation?

The pilot covers a limited study area and uses exploratory thresholds. It has no ground-truth validation, and small polygons may contain few pixels in the coarser Hansen dataset. It is a prototype, not an operational alerting service.

## 15. What would you improve next?

1. Expand the pilot to a clearly defined monitoring boundary.
2. Build a verified reference dataset with domain experts.
3. Tune thresholds and evaluate on geographically separate test areas.
4. Add time-series and land-use context to reduce false positives.
5. Test the workflow with forest researchers or local authorities.

## Presentation reminders

- Say “candidate region” or “screening flag,” not “confirmed illegal deforestation.”
- Say “unsupervised Isolation Forest anomaly ranking,” not “trained classifier” or “deforestation probability.”
- The model ranks all Section 11 candidate regions for which valid pixel samples are returned; the run output reports how many regions were successfully scored.
- Do not invent ML scores or Hansen values; show the actual Section 12 (ML) and Section 13 (Hansen) notebook outputs if asked.
- Do not claim accuracy, precision, recall or real-time monitoring.
- Keep each answer brief, then point to the map, table or notebook evidence.
