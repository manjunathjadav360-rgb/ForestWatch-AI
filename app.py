import streamlit as st

st.set_page_config(
    page_title="ForestWatch AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .stApp { background: #f7f8f5; }
      [data-testid="stSidebar"] { background: #eef2eb; }
      .block-container { padding-top: 2rem; max-width: 1180px; }
      .fw-muted { color: #647067; font-size: 0.92rem; }
      .fw-panel {
        background: #ffffff;
        border: 1px solid #e2e8df;
        border-radius: 12px;
        padding: 1rem 1.1rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ForestWatch AI")
st.caption("Satellite-informed forest disturbance screening · Western Ghats pilot")

with st.sidebar:
    st.subheader("Workspace")
    st.info("Prototype setup")
    st.markdown("**Pilot area**")
    st.write("Western Ghats, India")
    st.markdown("**Data sources planned**")
    st.write("Sentinel-2 optical · Sentinel-1 radar")
    st.caption("No live satellite analysis has been run yet.")

st.markdown(
    """
    This project is being built as an **evidence-first screening tool**.
    It aims to flag areas that may need human review—not to declare that
    illegal deforestation has occurred.
    """
)

left, middle, right = st.columns(3)
left.metric("Detection status", "Not run")
middle.metric("Candidate areas", "—")
right.metric("Evidence quality", "Awaiting data")

st.divider()
st.subheader("Investigation workspace")

tab_overview, tab_method, tab_limits = st.tabs(
    ["Overview", "Method", "Interpretation"]
)

with tab_overview:
    st.markdown(
        """
        <div class="fw-panel">
          <h4>What this prototype will do</h4>
          <ol>
            <li>Load comparable satellite observations for a selected area.</li>
            <li>Screen for persistent changes in vegetation signals.</li>
            <li>Compare optical observations with radar evidence where available.</li>
            <li>Present candidate locations with dates, indicators and limitations.</li>
          </ol>
          <p class="fw-muted">The dashboard will show real results only after the data pipeline is connected and tested.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_method:
    st.markdown("### Planned analysis")
    st.write(
        "- Sentinel-2: cloud-screened vegetation observations and NDVI change.\n"
        "- Sentinel-1: complementary radar observations, interpreted cautiously.\n"
        "- Temporal comparison: observations from comparable seasonal windows.\n"
        "- Review output: candidate disturbance polygons and supporting evidence."
    )
    st.latex(r"NDVI = \frac{NIR - Red}{NIR + Red}")

with tab_limits:
    st.warning(
        "A change in satellite imagery is not proof of illegal activity. "
        "Fire, storms, landslides, seasonal variation, harvesting and data-quality "
        "issues can produce similar signals."
    )
    st.write(
        "ForestWatch AI is intended to prioritize locations for expert review. "
        "Any future confidence or priority score will be explained and evaluated "
        "against reference data before being presented as meaningful."
    )

st.divider()
st.caption("ForestWatch AI · Neural Storm 2026 · Early development build")
