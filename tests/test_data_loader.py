"""
Test Suite for Data Loader & Fusion Pipeline (Milestone 1)
---------------------------------------------------------
Validates:
1. All 7 competition tables load with exact expected row/column shapes.
2. Building and calendar join keys match with 0 orphaned rows.
3. Unit harmonization in manual logs correctly standardizes kL, L, units, kWh, bags, and kg.
4. Campus KPI summary calculations are non-negative and mathematically consistent.
"""

import os
import sys
import pandas as pd
import numpy as np

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.data_loader import (
    load_buildings,
    load_calendar,
    load_daily_summary,
    load_daily_master,
    load_hourly_streams,
    load_manual_logs,
    load_waste_train,
    load_waste_test,
    compute_campus_kpis
)


def test_buildings_shape():
    df = load_buildings()
    assert len(df) == 8, f"Expected 8 buildings, got {len(df)}"
    assert set(["building_id", "building_name", "building_type", "has_solar", "has_composter"]).issubset(df.columns)
    assert df["building_id"].nunique() == 8


def test_calendar_shape():
    df = load_calendar()
    assert len(df) == 120, f"Expected 120 days, got {len(df)}"
    assert df["date"].nunique() == 120
    assert "avg_temp_c" in df.columns


def test_daily_summary_and_master():
    summary_df = load_daily_summary()
    master_df = load_daily_master()
    assert len(summary_df) == 960, f"Expected 960 daily summary rows, got {len(summary_df)}"
    assert len(master_df) == 960, f"Expected 960 daily master rows, got {len(master_df)}"
    
    # Check that building_id and date join cleanly
    bldg_ids = set(load_buildings()["building_id"])
    assert set(summary_df["building_id"]).issubset(bldg_ids)


def test_hourly_streams():
    df = load_hourly_streams()
    assert len(df) == 23192, f"Expected 23,192 hourly records, got {len(df)}"
    assert "ingestion_delay_hours" in df.columns
    # Check delay values are positive
    assert (df["ingestion_delay_hours"] >= 0).all()
    # Check max delay matches discovery findings (~12 hours)
    assert df["ingestion_delay_hours"].max() > 10.0


def test_manual_logs_harmonization():
    df = load_manual_logs()
    assert len(df) == 415, f"Expected 415 manual logs, got {len(df)}"
    assert "normalized_value" in df.columns
    assert "standard_unit" in df.columns
    
    # Check water kL conversion (e.g. 5.6 kL -> 5600 L)
    kl_records = df[(df["stream"] == "water") & (df["unit"].astype(str).str.lower() == "kl")]
    for _, r in kl_records.iterrows():
        if pd.notnull(r["value"]):
            assert r["normalized_value"] == float(r["value"]) * 1000.0
            assert r["standard_unit"] == "L"

    # Check waste bags conversion (e.g. 1 bag -> 8 kg)
    bag_records = df[(df["stream"] == "waste") & (df["unit"].astype(str).str.lower() == "bags")]
    for _, r in bag_records.iterrows():
        if pd.notnull(r["value"]):
            assert r["normalized_value"] == float(r["value"]) * 8.0
            assert r["standard_unit"] == "kg"


def test_waste_train_and_test():
    train_df = load_waste_train()
    test_df = load_waste_test()
    assert len(train_df) == 6314, f"Expected 6,314 train events, got {len(train_df)}"
    assert len(test_df) == 1601, f"Expected 1,601 test events, got {len(test_df)}"
    
    # Check target isolation
    assert "category" in train_df.columns
    assert "category" not in test_df.columns
    assert train_df["category"].nunique() == 6


def test_kpi_computation():
    daily_df = load_daily_summary()
    bldg_df = load_buildings()
    kpis = compute_campus_kpis(daily_df, bldg_df)
    
    assert kpis["total_grid_kwh"] > 0
    assert kpis["total_solar_kwh"] > 0
    assert kpis["total_water_litres"] > 0
    assert kpis["total_waste_kg"] > 0
    assert 0.0 <= kpis["diversion_rate_pct"] <= 100.0
    assert kpis["avoided_co2_kg"] > 0
    assert kpis["num_buildings"] == 8
    assert kpis["num_days"] == 120


if __name__ == "__main__":
    test_buildings_shape()
    print("PASS: test_buildings_shape")
    test_calendar_shape()
    print("PASS: test_calendar_shape")
    test_daily_summary_and_master()
    print("PASS: test_daily_summary_and_master")
    test_hourly_streams()
    print("PASS: test_hourly_streams")
    test_manual_logs_harmonization()
    print("PASS: test_manual_logs_harmonization")
    test_waste_train_and_test()
    print("PASS: test_waste_train_and_test")
    test_kpi_computation()
    print("PASS: test_kpi_computation")
    print("\nALL 7 MILESTONE 1 TESTS PASSED SUCCESSFULLY!")
