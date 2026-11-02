# ForestWatch AI — pilot run record

Copy this file for every new Earth Engine run. Fill in values from the actual notebook session; do not estimate missing values.

## Run identity

- Run date and time (UTC):
- Operator:
- Git commit:
- Earth Engine project ID:
- Notebook version / commit:
- AOI name and geometry source:
- AOI coordinates or asset ID:

## Data and processing configuration

- Sentinel-2 collection ID:
- Sentinel-1 collection ID:
- ESA WorldCover collection/version:
- Hansen Global Forest Change collection/version:
- Analysis start and end dates:
- Seasonal/comparison windows:
- Cloud and quality-screening settings:
- Persistence criteria:
- Minimum connected-region area:
- Radar-support definition / threshold:
- Any manual parameter changes:

## Results — copy from notebook output

- Valid observation counts:
- Persistent candidate pixels:
- Persistent candidate area (ha):
- WorldCover tree-cover overlap area (ha):
- WorldCover overlap share (%):
- Connected regions above minimum area:
- Number of regions exported:
- Hansen top-20 regions evaluated:
- Hansen regions with at least one loss-year pixel:
- Hansen loss-pixel area / candidate polygon area share (%), if computed:
- Hansen loss-pixel area intersecting shortlist polygons (ha), if computed:
- Other annual Hansen summaries:

## Export verification

- CSV export task ID and final status:
- GeoJSON export task ID and final status:
- CSV filename and Drive location:
- GeoJSON filename and Drive location:
- Confirmed CSV row count:
- Confirmed GeoJSON feature count:
- Snapshot updated in repository? yes / no

## Interpretation and review

- Candidate regions inspected manually:
- Known plantations / harvesting / fire / storm context checked:
- Independent reference source used:
- Findings that support candidate disturbance:
- Findings that contradict candidate disturbance:
- Unresolved uncertainties:

## Mandatory reporting caveats

- Candidate area is not confirmed deforested area.
- Hansen loss pixels are a coarse cross-check, not ground truth.
- A Hansen loss flag does not identify cause, natural-forest status or illegality.
- No accuracy, precision, recall or F1 score may be reported without independent labels and a defined evaluation protocol.
- Record any missing or failed data rather than silently treating it as zero.
