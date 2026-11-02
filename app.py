import streamlit as st
import pandas as pd
from pathlib import Path

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
st.caption("Satellite-informed forest disturbance screening · Western Ghats pilot · Neural Storm 2026")

st.markdown(
    '<div class="fw-note"><b>Review tool, not an enforcement verdict.</b> '
    'Candidate regions indicate places for human inspection. Satellite signals alone cannot confirm '
    'deforestation, natural-forest loss or illegal activity.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Pilot results")
    uploaded = st.file_uploader("Replace with latest Section 13 CSV (optional)", type=["csv"])
    st.caption("The dashboard opens with the recorded Section 11 pilot shortlist. Upload the latest Section 13 export to replace it.")

default_csv = Path(__file__).parent / "data" / "forestwatch_top20_snapshot.csv"
source_label = "Recorded Section 11 pilot output snapshot"
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

st.caption(f"Data source: {source_label}. Upload the latest export when available.")

required = [
    "area_ha", "latitude", "longitude", "ndvi_drop_2024",
    "ndvi_drop_2025", "ndvi_change_2025_vs_2024",
    "radar_support_share", "radar_coverage_share"
]
missing = [column for column in required if column not in df.columns]
if missing:
    st.error("This file is missing expected Section 13 columns: " + ", ".join(missing))
    st.stop()

for column in required:
    df[column] = pd.to_numeric(df[column], errors="coerce")
df = df.dropna(subset=["latitude", "longitude", "area_ha"]).copy()
df = df.sort_values("area_ha", ascending=False).reset_index(drop=True)
df.insert(0, "review_rank", range(1, len(df) + 1))

if df.empty:
    st.warning("The uploaded file contains no mappable candidate rows.")
    st.stop()

total_area = df["area_ha"].sum()
mean_support = df["radar_support_share"].mean()
mean_drop = df["ndvi_drop_2025"].mean()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Regions in file", f"{len(df)}")
m2.metric("Combined mapped area", f"{total_area:.2f} ha")
m3.metric("Mean 2025 NDVI drop", "—" if pd.isna(mean_drop) else f"{mean_drop:.3f}")
m4.metric("Mean radar support", "—" if pd.isna(mean_support) else f"{mean_support * 100:.1f}%")

st.divider()
left, right = st.columns([1.25, 1])
with left:
    st.subheader("Candidate region map")
    st.caption("Points mark region centroids; they are not polygon boundaries.")
    map_df = df[["latitude", "longitude"]].rename(columns={"latitude": "lat", "longitude": "lon"})
    st.map(map_df, zoom=8, use_container_width=True)

with right:
    st.subheader("Largest review candidates")
    display = df.head(5)[[
        "review_rank", "area_ha", "ndvi_drop_2024", "ndvi_drop_2025",
        "radar_support_share", "radar_coverage_share"
    ]].copy()
    display.columns = ["Rank", "Area (ha)", "NDVI drop 2024", "NDVI drop 2025", "Radar support", "Radar coverage"]
    st.dataframe(display, hide_index=True, use_container_width=True)

st.divider()
st.subheader("Candidate evidence table")
st.caption("Values are exploratory indicators from the exported shortlist, not calibrated probabilities or accuracy scores.")
table_columns = [
    "review_rank", "area_ha", "latitude", "longitude",
    "ndvi_drop_2024", "ndvi_drop_2025", "ndvi_change_2025_vs_2024",
    "radar_support_share", "radar_coverage_share"
]
st.dataframe(df[table_columns], hide_index=True, use_container_width=True)

st.subheader("How to interpret")
st.markdown(
    "- **NDVI drop:** vegetation-index difference relative to the notebook's 2023 baseline.\n"
    "- **Radar support:** share of regional pixels meeting the exploratory radar-support condition.\n"
    "- **Radar coverage:** share of regional pixels with radar observations. Coverage is not support.\n"
    "- **Area:** mapped candidate-region area, not confirmed deforested area."
)
st.warning("A high-ranked region is a priority for review, not proof of illegal deforestation. Inspect dated imagery and local context, then verify with authoritative reference information.")
st.caption("ForestWatch AI · Evidence-first prototype · Recorded pilot snapshot or latest uploaded export")
