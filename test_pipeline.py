"""
Test script to verify data loading, health monitoring, and KPI calculations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_loader import load_campus_data, get_available_buildings, get_building_health, compute_resource_kpis, get_hourly_resampled

def test_loader():
    df = load_campus_data()
    print("Dataset loaded successfully.")
    print("Shape:", df.shape)
    
    bldgs = get_available_buildings(df)
    print("Buildings found:", bldgs)
    assert set(bldgs) == {"Academic Block", "Hostel", "Cafeteria"}, f"Unexpected buildings: {bldgs}"

    # Test All Buildings Health
    health_all = get_building_health(df, "All Buildings")
    print("\nCampus Health:", health_all)
    assert "Cafeteria" in health_all["offline_buildings"], "Cafeteria should be recognized as offline"
    assert health_all["total_missing"] > 0, "Missing readings should be counted"

    # Test Cafeteria (Offline edge case)
    health_cafe = get_building_health(df, "Cafeteria")
    print("\nCafeteria Health:", health_cafe)
    assert health_cafe["is_offline"] is True, "Cafeteria is_offline should be True"

    # Test Academic Block (Online with sporadic missing readings)
    health_acad = get_building_health(df, "Academic Block")
    print("\nAcademic Block Health:", health_acad)
    assert health_acad["is_offline"] is False, "Academic Block should be ONLINE"
    assert health_acad["missing_counts"]["electricity"] > 0, "Academic Block should have sporadic missing electricity readings"

    # Test KPIs computation
    kpis = compute_resource_kpis(df, "Hostel")
    print("\nHostel KPIs:", kpis)
    assert kpis["electricity"]["total"] > 0
    assert kpis["water"]["total"] > 0
    assert kpis["waste"]["total"] > 0

    # Test hourly resampled
    resampled_all = get_hourly_resampled(df, "All Buildings")
    assert len(resampled_all) > 0
    print("\nResampled length:", len(resampled_all))

    print("\nAll data loader tests PASSED successfully!")

if __name__ == "__main__":
    test_loader()
