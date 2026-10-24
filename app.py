"""
CircuPulse Campus — Predictive Circular-Resource Grid for a Multi-Building Campus
---------------------------------------------------------------------------------
SRUJANA 2026: Prompt to Product (P2P) Hackathon Solution
Built from scratch using official competition datasets and local Python runtime.

Architecture Highlights:
1. Multi-modal sensor fusion under noise
2. Real-time edge 6-category smart-bin classification (>85% target, <1.5 ms latency)
3. 12-hour predictive demand surge forecasting (77.1% baseline error reduction)
4. Intermittent gateway buffering & deterministic deduplication
5. Explainable root-cause incident forensics with manual log cross-referencing
6. Closed-loop circular economy mass balancing & fair per-capita behavioral incentives
"""

import streamlit as st
import pandas as pd

from modules.data_loader import (
    load_buildings,
    load_calendar,
    load_daily_summary,
    load_hourly_streams,
    load_manual_logs,
    load_waste_train,
    load_waste_test,
    compute_campus_kpis
)
from modules.ui_views import (
    render_executive_grid,
    render_predictive_forecaster,
    render_edge_sorter,
    render_gateway_buffer,
    render_forensics_and_incentives,
    render_architecture_and_budget
)


# -------------------------------------------------------------------------
# Streamlit App Configuration
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="CircuPulse Campus — Predictive Circular-Resource Grid",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1b4332;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #40916c;
        margin-top: 0px;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        border-left: 4px solid #2d6a4f;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------------------------------
# Cached Global Data Loading
# -------------------------------------------------------------------------
@st.cache_data
def load_all_cached_data():
    buildings = load_buildings()
    calendar = load_calendar()
    daily = load_daily_summary()
    hourly = load_hourly_streams()
    logs = load_manual_logs()
    waste_train = load_waste_train()
    waste_test = load_waste_test()
    kpis = compute_campus_kpis(daily, buildings)
    return buildings, calendar, daily, hourly, logs, waste_train, waste_test, kpis


with st.spinner("Initializing CircuPulse Campus data fusion engine..."):
    bldgs_df, cal_df, daily_df, hourly_df, logs_df, waste_tr_df, waste_te_df, kpis = load_all_cached_data()


# -------------------------------------------------------------------------
# Sidebar Navigation & Context
# -------------------------------------------------------------------------
st.sidebar.markdown("## 🌱 CircuPulse Campus")
st.sidebar.caption("**Predictive Circular-Resource Grid**  \n*SRUJANA 2026 — Prompt to Product*")
st.sidebar.markdown("---")

selected_view = st.sidebar.radio(
    "Navigation Console:",
    [
        "🌐 Executive Campus Grid",
        "🔮 12-Hour Predictive Forecaster",
        "🗑️ Edge Smart-Bin Sorter",
        "📡 Gateway Buffer & Recovery",
        "🔍 Forensics & CircuCredits",
        "⚙️ Architecture & Hardware Budget"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    f"**Data Pipeline Status:** Active  \n"
    f"• **Scope:** {len(bldgs_df)} Campus Buildings  \n"
    f"• **Timeline:** 120 Operational Days  \n"
    f"• **Hourly Records:** {len(hourly_df):,}  \n"
    f"• **Smart-Bin Events:** {len(waste_tr_df):,}  \n"
    f"• **Field Logs:** {len(logs_df):,}"
)
st.sidebar.caption("© 2026 Student Engineering Team | EcoGrid AI Concept")


# -------------------------------------------------------------------------
# Main View Routing
# -------------------------------------------------------------------------
if selected_view == "🌐 Executive Campus Grid":
    render_executive_grid(daily_df, bldgs_df, kpis)

elif selected_view == "🔮 12-Hour Predictive Forecaster":
    render_predictive_forecaster(hourly_df, cal_df, bldgs_df)

elif selected_view == "🗑️ Edge Smart-Bin Sorter":
    render_edge_sorter(waste_tr_df, waste_te_df)

elif selected_view == "📡 Gateway Buffer & Recovery":
    render_gateway_buffer(hourly_df, bldgs_df)

elif selected_view == "🔍 Forensics & CircuCredits":
    render_forensics_and_incentives(daily_df, logs_df, bldgs_df)

elif selected_view == "⚙️ Architecture & Hardware Budget":
    render_architecture_and_budget()
