"""
Test Suite for Buffer Resilience, Circular Balance & Forensics (Milestone 3)
----------------------------------------------------------------------------
Validates:
1. GatewayBufferManager eliminates the 368 network retries and maintains 100% lossless reconciliation.
2. Building outage simulation computes buffered packets, energy kWh, and recovery metrics.
3. Circular mass balance computes finished compost and solar CO2 offsets.
4. Forensic incident detector identifies all 4 documented operational anomalies with corroborated notes.
5. CircuCredit leaderboard computes normalized per-capita metrics and ranks all 8 buildings.
"""

import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.data_loader import (
    load_buildings,
    load_daily_summary,
    load_hourly_streams,
    load_manual_logs
)
from modules.buffer_engine import GatewayBufferManager
from modules.circular_logic import (
    compute_circular_mass_balance,
    detect_forensic_incidents,
    compute_circucredit_leaderboard
)


def test_buffer_reconciliation():
    hourly_df = load_hourly_streams()
    mgr = GatewayBufferManager()
    reconciled_df, metrics = mgr.reconcile_stream(hourly_df)

    assert metrics["raw_total"] == 23192
    assert metrics["duplicates_detected"] == 368
    assert metrics["redundant_packets_pruned"] == 184
    assert len(reconciled_df) == 23008
    assert metrics["integrity_status"] == "VERIFIED_100_PERCENT_LOSSLESS"

    # Test outage simulation
    outage = mgr.simulate_building_outage(hourly_df, building_id="B05", duration_hours=6)
    assert outage["duration_hours"] == 6
    assert outage["buffered_packets_count"] > 0
    assert outage["buffered_energy_kwh"] > 0
    print("PASS: test_buffer_reconciliation")


def test_circular_mass_balance():
    daily_df = load_daily_summary()
    bldgs_df = load_buildings()
    balance = compute_circular_mass_balance(daily_df, bldgs_df)

    assert balance["food_court_organic_kg"] > 0
    assert balance["finished_compost_kg"] > 0
    assert balance["total_solar_kwh"] > 0
    assert balance["avoided_co2_kg"] > 0
    assert balance["compost_economic_value_inr"] > 0
    print("PASS: test_circular_mass_balance")


def test_forensic_incidents():
    daily_df = load_daily_summary()
    logs_df = load_manual_logs()
    bldgs_df = load_buildings()
    incidents = detect_forensic_incidents(daily_df, logs_df, bldgs_df)

    assert len(incidents) == 4
    incident_ids = [inc["incident_id"] for inc in incidents]
    assert incident_ids == ["INC-01", "INC-02", "INC-03", "INC-04"]

    # Verify corroborating notes exist
    for inc in incidents:
        assert len(inc["corroborating_log"]) > 0
        assert inc["confidence_score"] > 90.0
        assert "action_recommendation" in inc
    print("PASS: test_forensic_incidents")


def test_circucredit_leaderboard():
    daily_df = load_daily_summary()
    bldgs_df = load_buildings()
    leaderboard = compute_circucredit_leaderboard(daily_df, bldgs_df)

    assert len(leaderboard) == 8
    assert "circupulse_score" in leaderboard.columns
    assert "tier_badge" in leaderboard.columns
    assert (leaderboard["circupulse_score"] >= 0).all()
    assert (leaderboard["circupulse_score"] <= 100).all()
    # Check ranking order is monotonically decreasing
    assert list(leaderboard["circupulse_score"]) == sorted(list(leaderboard["circupulse_score"]), reverse=True)
    print("PASS: test_circucredit_leaderboard")


if __name__ == "__main__":
    test_buffer_reconciliation()
    test_circular_mass_balance()
    test_forensic_incidents()
    test_circucredit_leaderboard()
    print("\nALL MILESTONE 3 TESTS PASSED SUCCESSFULLY!")
