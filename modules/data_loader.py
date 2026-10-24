"""
CircuPulse Campus — Data Ingestion & Multi-Source Fusion Pipeline
-----------------------------------------------------------------
Robust, deterministic data loader for all 7 relational campus datasets.
Handles unit harmonization, temporal alignment, and multi-source fusion.
"""

import os
from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np

# Resolve base dataset directory
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(
    WORKSPACE_DIR,
    "dataset zip extract",
    "EcoGrid_AI_Data_Package",
    "02_csv_for_antigravity"
)

# Standard Campus Engineering Constants (from Problem Statement & Competition Guide)
GRID_CARBON_FACTOR_KG_PER_KWH = 0.70    # 0.70 kg CO2 / kWh
COMMERCIAL_TARIFF_INR_PER_KWH = 8.00     # Rs. 8.00 / kWh
WATER_ENERGY_KWH_PER_KL = 0.85          # 0.85 kWh / 1,000 L pumping intensity
COMPOST_CONVERSION_RATIO = 0.25         # 4:1 conversion ratio by mass (1 kg organic -> 0.25 kg compost)
CUSTODIAL_BAG_MASS_KG = 8.0             # ~8 kg per standard institutional custodial bag


def get_data_dir() -> str:
    """Returns the verified directory path for canonical CSV files."""
    if os.path.exists(DATA_DIR):
        return DATA_DIR
    # Fallback to local data dir if moved
    alt_dir = os.path.join(WORKSPACE_DIR, "data")
    if os.path.exists(alt_dir):
        return alt_dir
    raise FileNotFoundError(f"Canonical dataset folder not found at: {DATA_DIR}")


def load_buildings() -> pd.DataFrame:
    """
    Loads structural metadata for the 8 campus buildings.
    Grain: 1 row per building.
    """
    path = os.path.join(get_data_dir(), "buildings.csv")
    df = pd.read_csv(path)
    df["building_id"] = df["building_id"].astype(str)
    return df


def load_calendar() -> pd.DataFrame:
    """
    Loads 120-day academic calendar and ambient weather telemetry.
    Grain: 1 row per calendar day.
    """
    path = os.path.join(get_data_dir(), "calendar.csv")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    return df


def load_daily_summary() -> pd.DataFrame:
    """
    Loads daily aggregate resource consumption, waste streams, and occupancy.
    Grain: 1 row per building per date (960 rows = 8 buildings x 120 days).
    """
    path = os.path.join(get_data_dir(), "daily_summary.csv")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["building_id"] = df["building_id"].astype(str)
    return df


def load_daily_master() -> pd.DataFrame:
    """
    Loads the pre-joined daily convenience table (daily_summary + buildings + calendar).
    Grain: 1 row per building per date.
    """
    path = os.path.join(get_data_dir(), "daily_master.csv")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["building_id"] = df["building_id"].astype(str)
    return df


def load_hourly_streams() -> pd.DataFrame:
    """
    Loads hourly telemetry streams across all 8 buildings (23,192 records).
    Preserves both 'timestamp' (sensor event time) and 'received_at' (gateway arrival time).
    Calculates ingestion delay in hours.
    """
    path = os.path.join(get_data_dir(), "hourly_streams.csv")
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["received_at"] = pd.to_datetime(df["received_at"])
    df["building_id"] = df["building_id"].astype(str)
    
    # Calculate arrival delay in hours
    df["ingestion_delay_hours"] = (
        (df["received_at"] - df["timestamp"]).dt.total_seconds() / 3600.0
    ).round(2)
    return df


def load_manual_logs() -> pd.DataFrame:
    """
    Loads operator field logs (415 records) and harmonizes heterogeneous units.
    Standard conversions:
      - electricity: 'units' -> 'kWh' (1 unit = 1 kWh)
      - water: 'kL' -> 'L' (1 kL = 1000 L)
      - waste: 'bags' -> 'kg' (1 bag = 8.0 kg)
    Creates 'normalized_value' and 'standard_unit'.
    """
    path = os.path.join(get_data_dir(), "manual_logs.csv")
    df = pd.read_csv(path)
    df["logged_at"] = pd.to_datetime(df["logged_at"])
    df["building_id_normalized"] = df["building_id_normalized"].astype(str)

    def harmonize_row(row):
        val = row["value"]
        unit = str(row["unit"]).strip().lower() if pd.notnull(row["unit"]) else ""
        stream = str(row["stream"]).strip().lower()

        if pd.isna(val):
            return np.nan, "none"
        
        # Electricity harmonization
        if stream == "electricity":
            if unit in ["kwh", "units"]:
                return float(val), "kWh"
            return float(val), "kWh"

        # Water harmonization
        if stream == "water":
            if unit == "kl":
                return float(val) * 1000.0, "L"
            elif unit == "l":
                return float(val), "L"
            return float(val), "L"

        # Waste harmonization
        if stream == "waste":
            if unit == "bags":
                return float(val) * CUSTODIAL_BAG_MASS_KG, "kg"
            elif unit == "kg":
                return float(val), "kg"
            return float(val), "kg"

        return float(val), unit

    harmonized = df.apply(harmonize_row, axis=1)
    df["normalized_value"] = [h[0] for h in harmonized]
    df["standard_unit"] = [h[1] for h in harmonized]
    return df


def load_waste_train() -> pd.DataFrame:
    """
    Loads labeled multi-modal smart-bin events for supervised classification.
    Target column: 'category' (6 classes).
    Sensor columns: weight_g, moisture_pct, metal_signal, transparency, acoustic_hardness.
    """
    path = os.path.join(get_data_dir(), "waste_events_train.csv")
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["building_id"] = df["building_id"].astype(str)
    return df


def load_waste_test() -> pd.DataFrame:
    """
    Loads unlabelled active field disposal events (1,601 records) for inference.
    Contains sensor readings with no ground truth category.
    """
    path = os.path.join(get_data_dir(), "waste_events_test.csv")
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["building_id"] = df["building_id"].astype(str)
    return df


def compute_campus_kpis(daily_df: pd.DataFrame, buildings_df: pd.DataFrame) -> Dict[str, float]:
    """
    Computes high-level campus sustainability KPIs across the 120-day benchmark.
    """
    total_grid_kwh = float(daily_df["electricity_kwh"].sum(skipna=True))
    total_solar_kwh = float(daily_df["solar_generation_kwh"].sum(skipna=True))
    total_water_litres = float(daily_df["water_litres"].sum(skipna=True))

    # Waste streams
    total_wet_organic_kg = float(daily_df["wet_organic_kg"].sum(skipna=True))
    total_dry_recyclable_kg = float(daily_df["dry_recyclable_kg"].sum(skipna=True))
    total_ewaste_kg = float(daily_df["ewaste_kg"].sum(skipna=True))
    total_hazardous_kg = float(daily_df["hazardous_kg"].sum(skipna=True))
    total_waste_kg = (
        total_wet_organic_kg + total_dry_recyclable_kg + total_ewaste_kg + total_hazardous_kg
    )

    total_composted_kg = float(daily_df["composted_kg"].sum(skipna=True))
    total_recycled_kg = float(daily_df["recycled_kg"].sum(skipna=True))
    total_diverted_kg = total_composted_kg + total_recycled_kg
    total_landfill_kg = float(daily_df["landfill_kg"].sum(skipna=True))

    diversion_rate_pct = (
        (total_diverted_kg / total_waste_kg * 100.0) if total_waste_kg > 0 else 0.0
    )

    # Ecological & Financial offsets
    avoided_co2_kg = total_solar_kwh * GRID_CARBON_FACTOR_KG_PER_KWH
    solar_cost_savings_inr = total_solar_kwh * COMMERCIAL_TARIFF_INR_PER_KWH
    compost_yield_kg = total_composted_kg * COMPOST_CONVERSION_RATIO

    return {
        "total_grid_kwh": round(total_grid_kwh, 1),
        "total_solar_kwh": round(total_solar_kwh, 1),
        "total_water_litres": round(total_water_litres, 1),
        "total_waste_kg": round(total_waste_kg, 1),
        "total_composted_kg": round(total_composted_kg, 1),
        "total_recycled_kg": round(total_recycled_kg, 1),
        "total_diverted_kg": round(total_diverted_kg, 1),
        "total_landfill_kg": round(total_landfill_kg, 1),
        "diversion_rate_pct": round(diversion_rate_pct, 2),
        "avoided_co2_kg": round(avoided_co2_kg, 1),
        "solar_cost_savings_inr": round(solar_cost_savings_inr, 2),
        "compost_yield_kg": round(compost_yield_kg, 1),
        "num_buildings": len(buildings_df),
        "num_days": daily_df["date"].nunique(),
    }
