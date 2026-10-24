"""
CircuPulse Campus — Predictive Circular-Resource Grid for a Multi-Building Campus
---------------------------------------------------------------------------------
SRUJANA 2026: Prompt to Product (P2P) Hackathon Solution
Intuitive, clear, dedicated 6-view navigation with modern clean styling.
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
    page_title="CircuPulse Campus — Predictive Circular Grid",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Modern CSS Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.1;
    }
    .metric-sub {
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 6px;
    }

    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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


with st.spinner("Connecting to campus resource grid telemetry..."):
    bldgs_df, cal_df, daily_df, hourly_df, logs_df, waste_tr_df, waste_te_df, kpis = load_all_cached_data()


# -------------------------------------------------------------------------
# Sidebar Navigation (Dedicated 6 Consoles)
# -------------------------------------------------------------------------
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
        <span style="font-size: 2rem;">🌱</span>
        <div>
            <h2 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #065f46;">CircuPulse</h2>
            <div style="font-size: 0.75rem; color: #059669; font-weight: 600;">PREDICTIVE CIRCULAR GRID</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

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

st.sidebar.markdown(
    """
    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; font-size: 0.8rem; color: #475569;">
        <strong style="color: #0f172a;">SRUJANA 2026 Submission</strong><br>
        • <strong>8 Buildings</strong> Monitored<br>
        • <strong>120 Days</strong> Historical Telemetry<br>
        • <strong>6-Class</strong> Edge Sorter (&lt;1.5 ms)<br>
        • <strong>12-Hr</strong> Surge Forecaster (77% ↑)<br>
        • <strong>100% Lossless</strong> Ingestion
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.caption("Prompt to Product (P2P) • EcoGrid AI Architecture")


# -------------------------------------------------------------------------
# View Routing
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
