import math
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="ForestWatch AI | Review dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      :root { color-scheme: light; }
      html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #f5f7f2 !important;
        color: #26352a !important;
      }
      .block-container { max-width: 1200px; padding-top: 1.8rem; }
      h1, h2, h3, h4, h5, h6, p, span, label, li, strong, small,
      [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"],
      [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
      [data-testid="stMetricDelta"], [data-testid="stFileUploader"] {
        color: #26352a !important;
      }
      [data-testid="stSidebar"] { background: #edf2e9 !important; }
      [data-testid="stMetric"] {
        background: #ffffff !important;
        padding: 14px 16px;
        border: 1px solid #dce5d8;
        border-radius: 10px;
      }
      [data-testid="stDataFrame"], [data-testid="stTable"] {
        background: #ffffff !important;
      }
      .fw-note {
        background: #e8f0e4;
        color: #26352a !important;
        padding: 12px 16px;
        border-left: 4px solid #56734f;
        border-radius: 6px;
      }
      .fw-note b { color: #203b27 !important; }
      [data-testid="stAlert"] p { color: #26352a !important; }
      @media (max-width: 640px) {
        .block-container { padding: 1rem 0.8rem 3rem; }
        h1 { font-size: 1.8rem !important; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌿 ForestWatch AI")
st.caption(
    "Satellite-informed forest disturbance screening · Western Ghats pilot · Neural Storm 2026"
)
st.markdown(
    '<div class="fw-note"><b>Review tool, not an enforcement verdict.</b> '
    "Candidate regions indicate places for human inspection. Satellite signals alone cannot confirm "
    "deforestation, natural-forest loss or illegal activity.</div>",
    unsafe_allow_html=True,
)

required_columns = ["area_ha", "latitude", "longitude"]
evidence_columns = [
    "ndvi_drop_2024",
    "ndvi_drop_2025",
    "ndvi_change_2025_vs_2024",
    "radar_support_share",
    "radar_coverage_share",
    "area_rank",
    "ml_anomaly_percentile_median",
    "ml_anomaly_p95_share",
    "ml_sample_count",
    "treecover2000_pct_mean",
    "loss_2021_2025_share_mean",
    "loss_area_2021_2025_ha_sum",
    "ml_anomaly_percentile_median",
    "ml_anomaly_p95_share",
    "ml_sample_count",
    "ml_priority_rank",
    "area_rank",
    *[f"loss_{year}_share_mean" for year in range(2021, 2026)],
    *[f"loss_area_{year}_ha_sum" for year in range(2021, 2026)],
]

with st.sidebar:
    st.header("Review data")
    uploaded = st.file_uploader(
        "Upload Section 14 CSV with ML + Hansen results (optional)", type=["csv"]
    )
    st.caption(
        "Without an upload, the dashboard uses the committed Section 11 pilot snapshot."
    )

default_csv = Path(__file__).parent / "data" / "forestwatch_top20_snapshot.csv"
source_label = "Recorded Section 11 pilot snapshot"
try:
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        source_label = "User-uploaded Section 13 export"
    elif default_csv.exists():
        df = pd.read_csv(default_csv)
    else:
        st.error("Pilot results file is missing.")
        st.stop()
except Exception as exc:
    st.error(f"Could not read the candidate data: {exc}")
    st.stop()

missing = [column for column in required_columns if column not in df.columns]
if missing:
    st.error("This file is missing required columns: " + ", ".join(missing))
    st.stop()

hansen_required = {
    "treecover2000_pct_mean",
    "loss_2021_2025_share_mean",
    "loss_area_2021_2025_ha_sum",
}
has_hansen = hansen_required.issubset(df.columns)
ml_required = {
    "ml_priority_rank",
    "ml_anomaly_percentile_median",
    "ml_anomaly_p95_share",
    "ml_sample_count",
}
has_ml = ml_required.issubset(df.columns)
if uploaded is not None:
    if has_ml and has_hansen:
        source_label = "User-uploaded Section 14 export with ML ranking and Hansen cross-check"
    elif has_ml:
        source_label = "User-uploaded CSV with unsupervised ML ranking"
    elif has_hansen:
        source_label = "User-uploaded CSV with Hansen cross-check fields"
    else:
        source_label = "User-uploaded CSV without ML or Hansen fields"

original_rows = len(df)
numeric_columns = required_columns + [
    column for column in evidence_columns if column in df.columns
]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Keep only records with usable coordinates and a positive mapped area.
valid_coordinates = (
    df["latitude"].between(-90, 90)
    & df["longitude"].between(-180, 180)
)
valid_area = df["area_ha"].gt(0)
df = df.loc[
    valid_coordinates & valid_area,
    :
].dropna(subset=required_columns).copy()

# Evidence shares are fractions, so values outside [0, 1] are invalid.
share_columns = [
    "radar_support_share",
    "radar_coverage_share",
    "ml_anomaly_p95_share",
    "loss_2021_2025_share_mean",
    *[f"loss_{year}_share_mean" for year in range(2021, 2026)],
]
invalid_share_counts = {}
for column in share_columns:
    if column in df.columns:
        invalid = df[column].notna() & ~df[column].between(0, 1)
        invalid_share_counts[column] = int(invalid.sum())
        df.loc[invalid, column] = float("nan")

if "ml_anomaly_percentile_median" in df.columns:
    invalid = (
        df["ml_anomaly_percentile_median"].notna()
        & ~df["ml_anomaly_percentile_median"].between(0, 100)
    )
    if invalid.any():
        df.loc[invalid, "ml_anomaly_percentile_median"] = float("nan")
        st.warning("Invalid ML anomaly percentiles were omitted.")

if "ml_sample_count" in df.columns:
    invalid = df["ml_sample_count"].notna() & df["ml_sample_count"].lt(0)
    if invalid.any():
        df.loc[invalid, "ml_sample_count"] = float("nan")
        st.warning("Negative ML sample counts were omitted.")

if "ml_priority_rank" in df.columns:
    invalid = df["ml_priority_rank"].notna() & df["ml_priority_rank"].lt(1)
    if invalid.any():
        df.loc[invalid, "ml_priority_rank"] = float("nan")
        st.warning("Invalid ML priority ranks were omitted.")

if "treecover2000_pct_mean" in df.columns:
    invalid = df["treecover2000_pct_mean"].notna() & ~df["treecover2000_pct_mean"].between(0, 100)
    if invalid.any():
        df.loc[invalid, "treecover2000_pct_mean"] = float("nan")
        st.warning("Invalid Hansen year-2000 canopy percentages were omitted.")

for column in [
    "loss_area_2021_2025_ha_sum",
    *[f"loss_area_{year}_ha_sum" for year in range(2021, 2026)],
]:
    if column in df.columns:
        invalid = df[column].notna() & df[column].lt(0)
        if invalid.any():
            df.loc[invalid, column] = float("nan")
            st.warning(f"Negative values in {column} were omitted.")

removed_rows = original_rows - len(df)
if df.empty:
    st.warning("No valid candidate rows remain after checking coordinates and area.")
    st.stop()

# Use the model priority order when an enriched export is uploaded; otherwise
# retain the recorded Section 11 area order for the fallback snapshot.
if has_ml:
    df = df.sort_values(
        ["ml_priority_rank", "area_ha"],
        ascending=[True, False],
        na_position="last",
    ).reset_index(drop=True)
else:
    df = df.sort_values("area_ha", ascending=False).reset_index(drop=True)
df.insert(0, "review_rank", range(1, len(df) + 1))

if uploaded is not None:
    st.caption(f"Data source: {source_label}.")
else:
    st.caption(f"Data source: {source_label}. Upload a newer Section 13 CSV to refresh the shortlist.")

if removed_rows:
    st.warning(
        f"{removed_rows} of {original_rows} rows were excluded because their coordinates or mapped area were invalid."
    )

invalid_share_total = sum(invalid_share_counts.values())
if invalid_share_total:
    st.warning(
        f"{invalid_share_total} evidence-share value(s) were outside the valid 0–1 range "
        "and are omitted from the corresponding summaries."
    )

with st.sidebar:
    st.divider()
    st.subheader("Shortlist filter")
    top_n = st.slider(
        "Review priorities to display" if has_ml else "Largest regions to display",
        min_value=1,
        max_value=len(df),
        value=min(20, len(df)),
        step=1,
    )

view_df = df.head(top_n).copy()

# Metrics are calculated only from the rows currently shown.
mean_drop = (
    view_df["ndvi_drop_2025"].mean()
    if "ndvi_drop_2025" in view_df.columns
    else float("nan")
)
mean_support = (
    view_df["radar_support_share"].mean()
    if "radar_support_share" in view_df.columns
    else float("nan")
)
mean_coverage = (
    view_df["radar_coverage_share"].mean()
    if "radar_coverage_share" in view_df.columns
    else float("nan")
)
candidate_area = view_df["area_ha"].sum()

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Regions shown", f"{len(view_df)}")
m2.metric("Candidate area shown", f"{candidate_area:.2f} ha")
m3.metric(
    "Mean 2025 NDVI drop",
    "—" if pd.isna(mean_drop) else f"{mean_drop:.3f}",
)
m4.metric(
    "Mean radar support",
    "—" if pd.isna(mean_support) else f"{mean_support * 100:.1f}%",
)
m5.metric(
    "Mean radar coverage",
    "—" if pd.isna(mean_coverage) else f"{mean_coverage * 100:.1f}%",
)
st.caption(
    "Area is the sum of displayed candidate-region polygons, not confirmed deforested area. "
    "Radar coverage is reported separately from radar support."
)

if has_ml:
    st.subheader("Unsupervised ML anomaly analysis")
    st.caption(
        "StandardScaler + Isolation Forest scores multi-sensor feature patterns. "
        "Percentiles compare candidate pixels with the sampled pilot-AOI reference distribution; "
        "they are not probabilities or accuracy scores."
    )
    ml_median = view_df["ml_anomaly_percentile_median"].median()
    ml_priority_count = int(
        view_df["ml_anomaly_percentile_median"].ge(95).sum()
    )
    ml_pixels = int(view_df["ml_sample_count"].fillna(0).sum())
    ml1, ml2, ml3 = st.columns(3)
    ml1.metric(
        "Median regional anomaly percentile",
        "—" if pd.isna(ml_median) else f"{ml_median:.1f}",
    )
    ml2.metric("Regions with median ≥95th percentile", f"{ml_priority_count}/{len(view_df)}")
    ml3.metric("Candidate pixels scored", f"{ml_pixels:,}")

with st.expander("Independent Hansen cross-check", expanded=has_hansen):
    if has_hansen:
        hansen_area = view_df["loss_area_2021_2025_ha_sum"].sum(min_count=1)
        hansen_share = view_df["loss_2021_2025_share_mean"].mean()
        regions_with_signal = int(
            view_df["loss_2021_2025_share_mean"].fillna(0).gt(0).sum()
        )
        h1, h2, h3 = st.columns(3)
        h1.metric(
            "Hansen loss-pixel area",
            "—" if pd.isna(hansen_area) else f"{hansen_area:.3f} ha",
        )
        h2.metric(
            "Mean regional loss-pixel share",
            "—" if pd.isna(hansen_share) else f"{hansen_share * 100:.2f}%",
        )
        h3.metric(
            "Regions with a loss signal",
            f"{regions_with_signal}/{len(view_df)}",
        )
        st.warning(
            "These are approximate intersections of roughly 30 m Hansen loss pixels "
            "with candidate polygons. They are not confirmed deforested hectares, "
            "ground truth, or evidence of illegal activity."
        )
    else:
        st.info(
            "The committed pilot snapshot contains Section 11 fields only. "
            "To display ML and Hansen results here, run notebook Sections 12–14, "
            "then upload forestwatch_top20_candidates_with_hansen.csv from Google Drive."
        )

st.divider()
st.subheader("Candidate region map")
st.caption(
    "Each marker is a region centroid, not its boundary. Larger markers represent larger candidate regions."
)
map_df = view_df[["latitude", "longitude", "area_ha"]].copy()
max_area = max(float(map_df["area_ha"].max()), 0.01)
# st.map interprets the size column in metres. Use the equivalent-circle
# diameter for each region so marker area remains proportional to candidate area.
map_df["marker_diameter_m"] = map_df["area_ha"].apply(
    lambda value: 2 * math.sqrt(max(float(value), 0) * 10000 / math.pi)
)
st.map(
    map_df,
    latitude="latitude",
    longitude="longitude",
    size="marker_diameter_m",
    zoom=8,
    width="stretch",
)

st.subheader("Largest review candidates")
display_columns = [
    "review_rank",
    "region_id",
    "area_ha",
    "latitude",
    "longitude",
    "ndvi_drop_2024",
    "ndvi_drop_2025",
    "ndvi_change_2025_vs_2024",
    "radar_support_share",
    "radar_coverage_share",
    "treecover2000_pct_mean",
    "loss_2021_2025_share_mean",
    "loss_area_2021_2025_ha_sum",
    *[f"loss_{year}_share_mean" for year in range(2021, 2026)],
]
available_display_columns = [
    column for column in display_columns if column in view_df.columns
]
display = view_df[available_display_columns].copy()
display = display.rename(
    columns={
        "review_rank": "ML priority rank" if has_ml else "Area review rank",
        "area_rank": "Original area rank",
        "region_id": "Region ID (this run)",
        "area_ha": "Area (ha)",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "ndvi_drop_2024": "NDVI drop 2024",
        "ndvi_drop_2025": "NDVI drop 2025",
        "ndvi_change_2025_vs_2024": "NDVI change 2025 vs 2024",
        "radar_support_share": "Radar support (%)",
        "radar_coverage_share": "Radar coverage (%)",
        "ml_anomaly_percentile_median": "Median ML anomaly percentile",
        "ml_anomaly_p95_share": "Pixels ≥95th anomaly percentile (%)",
        "ml_sample_count": "ML pixels scored",
        "treecover2000_pct_mean": "Hansen tree cover 2000 mean (%)",
        "loss_2021_2025_share_mean": "Hansen loss share 2021–25 (%)",
        "loss_area_2021_2025_ha_sum": "Hansen loss-pixel area (ha)",
        **{
            f"loss_{year}_share_mean": f"Hansen loss share {year} (%)"
            for year in range(2021, 2026)
        },
    }
)
for column in [
    "Radar support (%)",
    "Radar coverage (%)",
    "Pixels ≥95th anomaly percentile (%)",
    "Hansen loss share 2021–25 (%)",
    *[f"Hansen loss share {year} (%)" for year in range(2021, 2026)],
]:
    if column in display.columns:
        display[column] = display[column] * 100
st.dataframe(display, hide_index=True, width="stretch")

st.download_button(
    "Download displayed shortlist (CSV)",
    data=view_df.to_csv(index=False).encode("utf-8"),
    file_name="forestwatch_review_shortlist.csv",
    mime="text/csv",
    width="stretch",
)

with st.expander("Evidence definitions and limitations"):
    st.markdown(
        """
        - **NDVI drop:** vegetation-index difference relative to the notebook's 2023 baseline.
        - **Radar support:** share of radar-observed pixels meeting the exploratory radar-support condition. Pixels without radar observations are excluded from this share.
        - **Radar coverage:** share of regional pixels with radar observations. Coverage is not support.
        - **Candidate area:** mapped area of a region flagged by the screening workflow; it is not confirmed forest-loss area.
        - **ML anomaly percentile:** relative rank against the sampled pilot-AOI reference distribution; it is not a probability or supervised class.
        - **ML ≥95th-percentile share:** fraction of sampled pixels in a region whose anomaly percentile is at least 95.
        - **Map markers:** centroid points only. Use the notebook's GeoJSON export to inspect candidate-region geometries.
        """
    )
    if has_hansen:
        st.caption(
            "Hansen fields were loaded from the Section 13 export. "
            "Treecover2000 is historical canopy cover; loss-pixel area is an approximate "
            "intersection at Hansen's coarser grid resolution."
        )
    else:
        st.info(
            "The committed pilot snapshot contains Section 11 fields only. "
            "Run the updated notebook Sections 12–14, then upload "
            "forestwatch_top20_candidates_with_hansen.csv to show ML ranking and the independent cross-check."
        )
    st.warning(
        "The workflow has not been validated against ground-truth labels. It does not produce a calibrated "
        "probability, accuracy score, or conclusion about the cause or legality of disturbance."
    )

st.caption(
    "ForestWatch AI · Evidence-first prototype · Human verification required"
)
