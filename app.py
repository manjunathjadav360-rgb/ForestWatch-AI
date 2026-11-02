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
]

with st.sidebar:
    st.header("Review data")
    uploaded = st.file_uploader(
        "Upload latest Section 13 CSV (optional)", type=["csv"]
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

removed_rows = original_rows - len(df)
if df.empty:
    st.warning("No valid candidate rows remain after checking coordinates and area.")
    st.stop()

# Rank consistently by mapped candidate-region area, largest first.
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

with st.sidebar:
    st.divider()
    st.subheader("Shortlist filter")
    top_n = st.slider(
        "Largest regions to display",
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

st.divider()
st.subheader("Candidate region map")
st.caption(
    "Each marker is a region centroid, not its boundary. Larger markers represent larger candidate regions."
)
map_df = view_df[["latitude", "longitude", "area_ha"]].copy()
max_area = max(float(map_df["area_ha"].max()), 0.01)
map_df["marker_size_m"] = map_df["area_ha"].apply(
    lambda value: 350 + 1650 * math.sqrt(max(float(value), 0) / max_area)
)
st.map(
    map_df,
    latitude="latitude",
    longitude="longitude",
    size="marker_size_m",
    zoom=8,
    use_container_width=True,
)

st.subheader("Largest review candidates")
display_columns = [
    "review_rank",
    "area_ha",
    "latitude",
    "longitude",
    "ndvi_drop_2024",
    "ndvi_drop_2025",
    "ndvi_change_2025_vs_2024",
    "radar_support_share",
    "radar_coverage_share",
]
available_display_columns = [
    column for column in display_columns if column in view_df.columns
]
display = view_df[available_display_columns].copy()
display = display.rename(
    columns={
        "review_rank": "Rank",
        "area_ha": "Area (ha)",
        "ndvi_drop_2024": "NDVI drop 2024",
        "ndvi_drop_2025": "NDVI drop 2025",
        "ndvi_change_2025_vs_2024": "NDVI change 2025 vs 2024",
        "radar_support_share": "Radar support (%)",
        "radar_coverage_share": "Radar coverage (%)",
    }
)
for column in ["Radar support (%)", "Radar coverage (%)"]:
    if column in display.columns:
        display[column] = display[column] * 100
st.dataframe(display, hide_index=True, use_container_width=True)

st.download_button(
    "Download displayed shortlist (CSV)",
    data=view_df.to_csv(index=False).encode("utf-8"),
    file_name="forestwatch_review_shortlist.csv",
    mime="text/csv",
    use_container_width=True,
)

with st.expander("Evidence definitions and limitations"):
    st.markdown(
        """
        - **NDVI drop:** vegetation-index difference relative to the notebook's 2023 baseline.
        - **Radar support:** share of regional pixels meeting the exploratory radar-support condition.
        - **Radar coverage:** share of regional pixels with radar observations. Coverage is not support.
        - **Candidate area:** mapped area of a region flagged by the screening workflow; it is not confirmed forest-loss area.
        - **Map markers:** centroid points only. Use the notebook's GeoJSON export to inspect candidate-region geometries.
        """
    )
    st.info(
        "The dashboard's committed snapshot contains Section 11 shortlist fields. "
        "The independent Hansen Global Forest Change cross-check is calculated in notebook Section 12 "
        "and is not merged into this dashboard dataset."
    )
    st.warning(
        "The workflow has not been validated against ground-truth labels. It does not produce a calibrated "
        "probability, accuracy score, or conclusion about the cause or legality of disturbance."
    )

st.caption(
    "ForestWatch AI · Evidence-first prototype · Human verification required"
)
