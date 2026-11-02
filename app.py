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
      .stApp { background: #f5f7f2; }
      .block-container { max-width: 1200px; padding-top: 1.8rem; }
      [data-testid="stMetric"] { background: white; padding: 14px 16px; border: 1px solid #e1e8dc; border-radius: 10px; }
      .fw-note { background: #eef3e9; padding: 12px 16px; border-left: 4px solid #56734f; border-radius: 6px; }
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
    st.header("Load pilot results")
    uploaded = st.file_uploader("Upload Section 13 CSV", type=["csv"])
    st.caption("In Colab, download forestwatch_top20_candidates.csv from Drive, then upload it here.")

if uploaded is None:
    st.info("Upload the CSV exported by notebook Section 13 to display the real candidate map and evidence. No sample or fabricated detections are shown.")
    st.subheader("How to get the results file")
    st.markdown(
        "1. Open the ForestWatch notebook in Colab.\n"
        "2. Run Section 13 and wait for the CSV export task to complete.\n"
        "3. In Google Drive, open the **ForestWatchAI** folder.\n"
        "4. Download **forestwatch_top20_candidates.csv** and upload it using the sidebar."
    )
    st.markdown("**Pipeline:** Sentinel-2 change → persistence screen → Sentinel-1 context → ESA WorldCover reference → regional shortlist → Hansen cross-check.")
    st.stop()

try:
    df = pd.read_csv(uploaded)
except Exception as exc:
    st.error(f"Could not read this CSV: {exc}")
    st.stop()

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
st.caption("ForestWatch AI · Evidence-first prototype · Results shown only from the CSV uploaded in this session")
