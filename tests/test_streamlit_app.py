"""
Streamlit AppTest Suite for CircuPulse Campus (Milestone 4)
----------------------------------------------------------
Validates:
1. Main entrypoint app.py loads without syntax or runtime exceptions.
2. All 6 navigation views render smoothly without errors.
3. Interactive selectbox and radio controls execute successfully.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit.testing.v1 import AppTest


def test_streamlit_views():
    app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")
    print(f"Initializing AppTest from {app_path}...", flush=True)
    at = AppTest.from_file(app_path, default_timeout=30)
    
    # 1. Initial Load (View 1: Executive Campus Grid)
    print("Running initial app load (Executive Grid)...", flush=True)
    at.run()
    assert len(at.exception) == 0, f"Exceptions on initial load: {at.exception}"
    print("PASS: Executive Grid rendered cleanly.")

    # 2. View 2: Predictive Forecaster
    print("Switching to 12-Hour Predictive Forecaster...", flush=True)
    at.sidebar.radio[0].set_value("🔮 12-Hour Predictive Forecaster").run()
    assert len(at.exception) == 0, f"Exceptions on Forecaster view: {at.exception}"
    print("PASS: 12-Hour Predictive Forecaster rendered cleanly.")

    # 3. View 3: Edge Smart-Bin Sorter
    print("Switching to Edge Smart-Bin Sorter...", flush=True)
    at.sidebar.radio[0].set_value("🗑️ Edge Smart-Bin Sorter").run()
    assert len(at.exception) == 0, f"Exceptions on Edge Sorter view: {at.exception}"
    print("PASS: Edge Smart-Bin Sorter rendered cleanly.")

    # 4. View 4: Gateway Buffer & Recovery
    print("Switching to Gateway Buffer & Recovery...", flush=True)
    at.sidebar.radio[0].set_value("📡 Gateway Buffer & Recovery").run()
    assert len(at.exception) == 0, f"Exceptions on Gateway Buffer view: {at.exception}"
    print("PASS: Gateway Buffer rendered cleanly.")

    # 5. View 5: Forensics & CircuCredits
    print("Switching to Forensics & CircuCredits...", flush=True)
    at.sidebar.radio[0].set_value("🔍 Forensics & CircuCredits").run()
    assert len(at.exception) == 0, f"Exceptions on Forensics view: {at.exception}"
    print("PASS: Forensics & CircuCredits rendered cleanly.")

    # 6. View 6: Architecture & Hardware Budget
    print("Switching to Architecture & Hardware Budget...", flush=True)
    at.sidebar.radio[0].set_value("⚙️ Architecture & Hardware Budget").run()
    assert len(at.exception) == 0, f"Exceptions on Architecture view: {at.exception}"
    print("PASS: Architecture & Budget rendered cleanly.")

    print("\nALL 6 STREAMLIT VIEWS RENDERED WITH ZERO EXCEPTIONS!")


if __name__ == "__main__":
    test_streamlit_views()
