"""
EcoGrid AI - UI Components Module
---------------------------------
Reusable Streamlit UI components for rendering:
- Header & Synthetic Data Disclaimers
- Health Status & Offline Alert Banners
- Resource KPI Metric Cards (Electricity, Water, Waste)
- Interactive Plotly Visualizations
- Missing Reading Inspector
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional

def inject_custom_css():
    """Injects modern, clean, sustainable-themed CSS styles."""
    st.markdown("""
        <style>
        /* Main background & typography tweaks */
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #105652;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #4B6584;
            margin-bottom: 1.2rem;
        }
        
        /* Synthetic data disclaimer pill */
        .synthetic-badge {
            background-color: #FEF3C7;
            color: #92400E;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            border: 1px solid #FCD34D;
            display: inline-block;
            margin-bottom: 12px;
        }

        /* Status Badges */
        .badge-online {
            background-color: #DEF7EC;
            color: #03543F;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid #BCF0DA;
        }
        .badge-offline {
            background-color: #FDE8E8;
            color: #9B1C1C;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid #FBD5D5;
        }
        .badge-warning {
            background-color: #FEECDC;
            color: #B43403;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid #FCD9BD;
        }

        /* Metric cards */
        .metric-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }
        .metric-card:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.08);
            border-color: #CBD5E1;
        }
        .metric-title {
            font-size: 0.85rem;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .metric-value {
            font-size: 1.65rem;
            font-weight: 700;
            color: #0F172A;
        }
        .metric-subtitle {
            font-size: 0.78rem;
            color: #64748B;
            margin-top: 4px;
        }

        /* Callout alert box */
        .offline-callout {
            background-color: #FFF5F5;
            border-left: 4px solid #E53E3E;
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: #742A2A;
            font-size: 0.95rem;
        }
        .warning-callout {
            background-color: #FFFDF0;
            border-left: 4px solid #DD6B20;
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: #7B341E;
            font-size: 0.92rem;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    """Renders the top branding, navigation summary, and synthetic data label."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="main-header">🌱 EcoGrid AI — Campus Sustainability Hub</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sub-header">Unified monitoring & telemetry for electricity, water, and waste resources.</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div style="text-align: right;">'
            '<span class="synthetic-badge">⚠️ SYNTHETIC DEMO DATA</span><br>'
            '<small style="color: #64748B;">Proof-of-Concept v1.0</small>'
            '</div>',
            unsafe_allow_html=True
        )


def render_health_banner(health_info: Dict[str, Any]):
    """
    Renders clear status indicators and warnings for offline buildings
    and missing telemetry readings.
    """
    if health_info["is_offline"]:
        if health_info["building"] == "All Buildings" or health_info["building"] == "Campus Total":
            offline_list = ", ".join(health_info["offline_buildings"])
            st.markdown(
                f'<div class="offline-callout">'
                f'🚨 <strong>Telemetry Alert:</strong> {len(health_info["offline_buildings"])} building(s) currently offline: '
                f'<strong>{offline_list}</strong>. Telemetry gateway connection lost; metrics reflect only active periods.'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="offline-callout">'
                f'🚨 <strong>Building Offline:</strong> <strong>{health_info["building"]}</strong> sensor gateway is disconnected! '
                f'No live telemetry received in the past 14 hours. Please inspect gateway power and LoRa/Wi-Fi uplink.'
                f'</div>',
                unsafe_allow_html=True
            )

    if health_info["total_missing"] > 0:
        missing_details = []
        if health_info["missing_counts"]["electricity"] > 0:
            missing_details.append(f"{health_info['missing_counts']['electricity']} electricity")
        if health_info["missing_counts"]["water"] > 0:
            missing_details.append(f"{health_info['missing_counts']['water']} water")
        if health_info["missing_counts"]["waste"] > 0:
            missing_details.append(f"{health_info['missing_counts']['waste']} waste")
            
        details_str = ", ".join(missing_details)
        st.markdown(
            f'<div class="warning-callout">'
            f'⚠️ <strong>Data Quality Notice:</strong> {health_info["total_missing"]} missing readings detected '
            f'({health_info["missing_pct"]}% of expected window: {details_str}). '
            f'Calculations automatically omit missing timestamps to prevent biased totals.'
            f'</div>',
            unsafe_allow_html=True
        )


def render_summary_cards(kpis: Dict[str, Dict[str, Any]], resource_filter: str):
    """
    Renders professional KPI summary cards for Electricity, Water, and Waste.
    Respects resource filter if a specific resource is chosen.
    """
    cols_to_show = []
    if resource_filter in ("All Resources", "⚡ Electricity (kWh)"):
        cols_to_show.append(("electricity", "⚡ Electricity", "kWh", "#F59E0B"))
    if resource_filter in ("All Resources", "💧 Water (Liters)"):
        cols_to_show.append(("water", "💧 Water", "Liters", "#3B82F6"))
    if resource_filter in ("All Resources", "♻️ Waste (kg)"):
        cols_to_show.append(("waste", "♻️ Waste", "kg", "#10B981"))

    cols = st.columns(len(cols_to_show))

    for idx, (res_key, res_name, unit_label, accent_color) in enumerate(cols_to_show):
        data = kpis[res_key]
        with cols[idx]:
            # Format numbers cleanly
            if data["total"] >= 10000:
                tot_str = f"{data['total']:,.0f}"
            else:
                tot_str = f"{data['total']:,.1f}"

            daily_avg_str = f"{data['daily_avg']:,.1f}"
            peak_str = f"{data['peak']:,.1f}"
            missing_badge = f'<span style="color:#DC2626;">({data["missing_readings"]} missing)</span>' if data["missing_readings"] > 0 else '<span style="color:#059669;">(100% valid)</span>'

            st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid {accent_color};">
                    <div class="metric-title">{res_name}</div>
                    <div class="metric-value">{tot_str} <span style="font-size: 0.9rem; font-weight: 500; color: #64748B;">{unit_label}</span></div>
                    <div class="metric-subtitle">
                        📅 Daily Avg: <strong>{daily_avg_str} {unit_label}/day</strong><br>
                        ⚡ Peak Load: <strong>{peak_str} {unit_label}/hr</strong><br>
                        📊 Telemetry: {missing_badge}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


def render_resource_trend_chart(
    df: pd.DataFrame,
    resource: str,
    building: str
):
    """
    Renders an interactive Plotly line/area chart showing consumption over time.
    """
    resource_config = {
        "⚡ Electricity (kWh)": ("electricity_kwh", "Electricity Consumption (kWh)", "#F59E0B"),
        "💧 Water (Liters)": ("water_liters", "Water Consumption (Liters)", "#3B82F6"),
        "♻️ Waste (kg)": ("waste_kg", "Waste Generation (kg)", "#10B981"),
    }

    if resource not in resource_config:
        # Default fallback to electricity
        col, title, color = resource_config["⚡ Electricity (kWh)"]
    else:
        col, title, color = resource_config[resource]

    if building == "All Buildings":
        # Grouped by building for comparison
        fig = px.line(
            df,
            x="timestamp",
            y=col,
            color="building",
            title=f"📈 {title} — Multi-Building Comparison",
            labels={"timestamp": "Date & Time", col: f"{title}", "building": "Building"},
            color_discrete_map={
                "Academic Block": "#3B82F6",
                "Hostel": "#8B5CF6",
                "Cafeteria": "#EC4899"
            }
        )
    else:
        bldg_data = df[df['building'] == building] if 'building' in df.columns else df
        fig = px.area(
            bldg_data,
            x="timestamp",
            y=col,
            title=f"📈 {title} — {building} Trend Over Time",
            labels={"timestamp": "Date & Time", col: f"{title}"},
            color_discrete_sequence=[color]
        )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, width='stretch')


def render_building_comparison(df: pd.DataFrame, resource: str):
    """
    Renders a bar chart comparing total consumption across all buildings.
    """
    resource_config = {
        "⚡ Electricity (kWh)": ("electricity_kwh", "Total Electricity (kWh)", "#F59E0B"),
        "💧 Water (Liters)": ("water_liters", "Total Water (Liters)", "#3B82F6"),
        "♻️ Waste (kg)": ("waste_kg", "Total Waste (kg)", "#10B981"),
        "All Resources": ("electricity_kwh", "Electricity (kWh) by Building", "#F59E0B")
    }

    col, label, color = resource_config.get(resource, ("electricity_kwh", "Electricity (kWh)", "#F59E0B"))

    summary = df.groupby('building')[col].sum().reset_index()

    fig = px.bar(
        summary,
        x="building",
        y=col,
        title=f"🏢 Campus Breakdown: {label}",
        labels={"building": "Campus Building", col: label},
        text_auto=".1f",
        color="building",
        color_discrete_sequence=["#10B981", "#3B82F6", "#F59E0B"]
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False
    )
    st.plotly_chart(fig, width='stretch')


def render_missing_data_inspector(df: pd.DataFrame, selected_building: str):
    """
    Inspects and visualizes missing data occurrences and sensor status.
    """
    with st.expander("🔍 Telemetry Diagnostics & Missing Reading Inspector"):
        data = df if selected_building == "All Buildings" else df[df['building'] == selected_building]
        
        # Filter rows where at least one reading is missing or status is OFFLINE
        flagged_rows = data[(data['electricity_kwh'].isna()) | 
                            (data['water_liters'].isna()) | 
                            (data['waste_kg'].isna()) | 
                            (data['status'] == 'OFFLINE')]

        st.markdown(
            f"**Total Telemetry Dropouts Detected:** `{len(flagged_rows)}` out of `{len(data)}` hours logged."
        )

        if not flagged_rows.empty:
            display_cols = ['timestamp', 'building', 'electricity_kwh', 'water_liters', 'waste_kg', 'status']
            st.dataframe(
                flagged_rows[display_cols].style.highlight_null(color='#FED7D7'),
                width='stretch'
            )
            st.caption("Highlighted red cells represent missing sensor readings (NaN). EcoGrid automatically isolates these periods.")
        else:
            st.success("✅ All sensor readings are 100% complete with no dropouts in this view.")
