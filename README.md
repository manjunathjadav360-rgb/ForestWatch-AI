# ForestWatch AI

**Neural Storm 2026 · Green Planet · GP-04: Illegal Deforestation Detection**

ForestWatch AI is an evidence-first prototype for screening satellite observations for possible forest disturbance. The intended pilot region is the Western Ghats, India.

> **Important:** A satellite-observed change is not proof of illegal deforestation. ForestWatch is designed to identify candidate areas for human review and show the evidence and uncertainty behind each flag.

## Problem

Forest landscapes can change for many reasons, including land clearing, fire, storms, landslides, disease, seasonal vegetation cycles and normal land management. A useful monitoring workflow must do more than compare two images: it should account for observation quality, seasonality and alternative explanations.

## Proposed approach

1. Use Sentinel-2 optical observations to examine vegetation change.
2. Apply cloud and scene-quality screening before comparison.
3. Compare observations from seasonally comparable periods.
4. Add Sentinel-1 radar observations as complementary evidence where practical.
5. Group notable changes into candidate areas for review.
6. Present dates, location, indicators, data quality and known limitations alongside each candidate.

The project will distinguish **evidence quality** from **investigation priority**. Any scoring method will be documented and evaluated; it will not be presented as a legal determination.

## Technology

- Python
- Google Earth Engine
- Streamlit
- NumPy and Pandas
- Matplotlib

Additional geospatial or machine-learning libraries will be added only when the implementation needs them.

## Current status

This repository currently contains the initial dashboard shell and project documentation. The satellite processing pipeline, candidate detection, validation and live map are **not implemented yet**. No detection results or model-accuracy claims are being reported at this stage.

## Run locally

1. Install Python 3.10 or newer.
2. Clone this repository.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

The initial dashboard shell can be opened without Earth Engine credentials. Satellite analysis will require a separately authenticated Earth Engine account and project.

## Evaluation plan

When suitable reference labels are available, the project will report relevant measures such as precision, recall and F1-score, and will document the geographic and temporal limits of the evaluation. Results will not be invented or estimated without running the evaluation.

## AI tools used

ChatGPT is being used for planning, code assistance, debugging and documentation. The implementation and results will be checked against the actual data and execution output.

## Limitations

- Optical imagery can be affected by clouds, haze and shadows.
- Radar data provides complementary information but requires careful interpretation.
- Seasonal differences can look like disturbance if comparison periods are poorly chosen.
- A detected change does not establish its cause, legality or responsible party.
- Human review and reliable reference data are necessary.

## Project structure

```text
ForestWatch-AI/
├── app.py
├── requirements.txt
└── README.md
```

More modules will be added as working components are implemented and tested.
