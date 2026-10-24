"""
Test Suite for Machine Learning & Predictive Analytics Engine (Milestone 2)
---------------------------------------------------------------------------
Validates:
1. EdgeWasteClassifier achieves >85% accuracy on stratified test split.
2. Single-sample inference latency is strictly <2.0 seconds (benchmark target is <1.0 ms).
3. Test stream batch inference produces exactly 1,601 rows with event_id, predicted_class, and confidence.
4. DemandForecaster achieves >50% MAE improvement over naive diurnal persistence.
5. 12-hour future forecast bounds are consistent (lower <= predicted <= upper).
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.data_loader import load_waste_train, load_waste_test, load_hourly_streams
from modules.ml_models import EdgeWasteClassifier, DemandForecaster


def test_edge_waste_classifier():
    train_raw = load_waste_train()
    
    # 80/20 train/test split with fixed seed for reproducibility
    np.random.seed(42)
    shuffled_idx = np.random.permutation(len(train_raw))
    split_point = int(len(train_raw) * 0.8)
    tr_df = train_raw.iloc[shuffled_idx[:split_point]]
    te_df = train_raw.iloc[shuffled_idx[split_point:]]

    clf = EdgeWasteClassifier(var_smoothing=1e-4)
    clf.fit(tr_df)
    results = clf.evaluate(te_df)

    acc = results["accuracy"]
    print(f"Verified Classifier Accuracy: {acc * 100:.2f}%")
    assert acc >= 0.85, f"Expected accuracy >= 85%, got {acc * 100:.2f}%"

    # Test single-event inference speed (<2 seconds required by problem statement)
    sample_sensor = {
        "weight_g": 350.0,
        "moisture_pct": 72.0,
        "metal_signal": 5.0,
        "transparency": 0.12,
        "acoustic_hardness": 0.15,
    }
    pred_res = clf.predict_single(sample_sensor)
    latency = pred_res["latency_ms"]
    print(f"Verified Single-Event Inference Latency: {latency:.3f} ms")
    assert latency < 100.0, f"Inference too slow: {latency} ms"
    assert pred_res["predicted_class"] == "food_organic"

    # Test batch predictions on held-out test stream
    test_stream = load_waste_test()
    preds_df = clf.predict_test_stream(test_stream)
    assert len(preds_df) == 1601, f"Expected 1,601 predictions, got {len(preds_df)}"
    assert set(preds_df.columns) == set(["event_id", "predicted_class", "confidence_pct"])
    print("PASS: test_edge_waste_classifier")


def test_demand_forecaster():
    hourly_df = load_hourly_streams()
    forecaster = DemandForecaster(l2_reg=10.0)

    # Fit 12-hour ahead electricity forecast for B01
    forecaster.fit(hourly_df, building_id="B01", utility="electricity_kwh", horizon=12)
    metrics = forecaster.metrics

    print(f"Forecaster MAE: {metrics['mae']} kWh vs Baseline: {metrics['baseline_mae']} kWh")
    print(f"Improvement over Baseline: {metrics['improvement_pct']}%")
    assert metrics["mae"] < metrics["baseline_mae"], "Forecaster failed to beat baseline"
    assert metrics["improvement_pct"] > 50.0, f"Expected >50% improvement, got {metrics['improvement_pct']}%"

    # Test 12-hour lookahead forecast generation
    future_df = forecaster.predict_future(hourly_df, building_id="B01", utility="electricity_kwh", num_hours=12)
    assert len(future_df) == 12, f"Expected 12 future steps, got {len(future_df)}"
    for _, r in future_df.iterrows():
        assert r["lower_bound_95"] <= r["predicted"] <= r["upper_bound_95"]
        assert r["predicted"] >= 0.0

    print("PASS: test_demand_forecaster")


if __name__ == "__main__":
    test_edge_waste_classifier()
    test_demand_forecaster()
    print("\nALL MILESTONE 2 TESTS PASSED SUCCESSFULLY!")
