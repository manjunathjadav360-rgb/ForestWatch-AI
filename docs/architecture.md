# ForestWatch AI — system architecture

## Processing flow

```mermaid
flowchart TD
    A[Google Earth Engine authentication] --> B[Study area: Western Ghats pilot AOI]
    B --> C[Sentinel-2 surface reflectance]
    B --> D[Sentinel-1 GRD radar]
    C --> E[Cloud and scene-quality screening]
    E --> F[Seasonally comparable NDVI composites]
    F --> G[Persistent decline screen: 2023, 2024, 2025]
    D --> H[VV and VH change context]
    G --> I[ESA WorldCover 2021 tree-cover reference]
    I --> J[Connected candidate regions]
    H --> K[Regional radar evidence]
    J --> L[Region-level evidence shortlist]
    K --> L
    L --> M[Retain original area rank for every region]
    M --> N[Non-candidate 2021 tree-cover reference sample]
    N --> O[StandardScaler + Isolation Forest]
    O --> P[Score every sampleable candidate region]
    P --> Q[Top 20 ML anomaly priorities]
    Q --> R[Hansen Global Forest Change cross-check]
    R --> S[CSV and GeoJSON exports to Google Drive]
    S --> T[Human review and independent verification]
```

## Components and responsibilities

| Component | Role | Interpretation |
|---|---|---|
| Sentinel-2 SR Harmonized | NDVI observations from optical bands | Vegetation-condition indicator; sensitive to clouds and seasonal effects |
| Quality screening | Masks poor-quality observations and requires repeat observations | Reduces, but does not eliminate, observation artefacts |
| Multi-year comparison | Compares corresponding seasonal windows across 2023–2025 | Persistent decline is a screening signal, not a forest-loss label |
| Sentinel-1 GRD | VV/VH radar change context | Complementary evidence; backscatter changes are not uniquely attributable |
| ESA WorldCover 2021 | Historical tree-cover reference (class 10) | Helps screen to areas mapped as tree cover; does not prove natural forest |
| Connected regions | Groups adjacent candidate pixels and filters tiny fragments | Creates reviewable geographic units |
| Unsupervised ML stage | StandardScaler + Isolation Forest over seven optical/radar features, fitted to a reproducible random sample of valid 2021 tree-cover pixels outside the persistent-candidate mask, with held-out score calibration | Produces relative anomaly percentiles and per-region optical/radar feature summaries for all candidate regions with usable data; selects 20 priorities for cross-checking, not a probability or supervised forest-loss class |
| Hansen Global Forest Change | Independent, coarser loss-year cross-check | Indicates mapped stand-replacement loss, not its cause or legality |
| CSV / GeoJSON export | Makes shortlist reusable in analysis and mapping tools | Exports candidates for human review |

## Evidence logic

ForestWatch separates three concepts:

1. **Candidate generation:** persistent optical vegetation decline in the selected seasonal windows.
2. **Evidence context:** radar support and historical tree-cover / forest-loss references.
3. **Area baseline:** every connected region retains its original mapped-area rank for comparison.
4. **ML review priority:** an unsupervised Isolation Forest scores sampled pixels across all regions with usable data, aggregates anomaly percentiles per region and selects the 20 highest anomaly priorities. This is a relative anomaly ranking only.
5. **Independent cross-check:** Hansen loss-year values are shown separately and do not train the anomaly model.

These are not a calibrated probability model. A high-ranked region is not necessarily illegal deforestation, and a low-ranked or unflagged region is not guaranteed to be unchanged.

## Human review

Before a candidate is described as forest loss, a reviewer should inspect dated imagery, local land-cover context, known plantations and land management, fire or storm history, and authoritative ground/reference information. Any enforcement decision requires competent authorities and independent verification.
