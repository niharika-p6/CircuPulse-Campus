# SRUJANA 2026: Official Prompt Workbook & Engineering Log
**Project Title:** CircuPulse Campus — Predictive Circular-Resource Grid for a Multi-Building Campus  
**Team:** Revert (SRUJANA 2026 Hackathon)  
**AI Mentorship Platform:** Google Antigravity / Gemini 3.8  
**Date of Development:** 24 October 2026 
**Team Members:** 1. Niharika Naik P 
                  2. Khushi Ojha 
                  3. Divija D
                  4. Sujal Singh Rathore

---

## 1. Executive Summary & AI Tool Role Disclosure

In accordance with official SRUJANA 2026 constraints:
* **Role of Generative AI:** Generative AI served as an interactive engineering mentor, data analyst, architectural thinking partner, and code scaffolding assistant. It helped discover latent patterns across 7 heterogeneous datasets, formulate mathematical formulas for zero-dependency edge inference, and generate unit tests for edge-case validation.
* **Human Engineering Leadership:** All product decisions, milestone approvals, dataset interpretations, architecture choices, model evaluations, and failure-mode analyses were actively reviewed, guided, and validated by the student engineering team.
* **Authenticity Assurance:** No complete GitHub repositories or pre-built applications were copied. Every line of code was built from scratch within the competition environment. All accuracy metrics, latencies, and financial savings reflect genuine benchmark evaluations on the supplied competition datasets without fabrication.

---

## 2. Chronological Prompt Evolution Log

### Entry 1: Stage 1 — Dataset & Environment Discovery
* **Milestone:** Stage 1 — Discovery & Integrity Inspection
* **Date & Timestamp:** 2026-10-24 12:14:33
* **AI Tool Used:** Antigravity / Gemini 3.8
* **Prompt Submitted:**  
  *Master Project Instructions requesting recursive workspace discovery, dataset inspection across 7 relational tables, capability-support matrix, join cardinality validation, and risk analysis without altering data or starting implementation.*
* **AI Output Summary:**  
  Identified Python 3.14.7 runtime. Located canonical dataset package in `02_csv_for_antigravity`. Inspected all 7 relational tables: `buildings.csv` (8 rows), `calendar.csv` (120 rows), `daily_summary.csv` (960 rows), `hourly_streams.csv` (23,192 rows), `manual_logs.csv` (415 rows), `waste_events_train.csv` (6,314 rows), `waste_events_test.csv` (1,601 rows). Identified 368 duplicate network retries, 1.01–12.08 hour ingestion delays, and 6 waste categories.
* **Human Evaluation & Decisions:**  
  *Accepted:* Recognized that sandbox mode lacks internet access and `scikit-learn` is absent, prompting the decision to build native, zero-dependency NumPy/pandas algorithms.  
  *Rejected:* Rejected any cloud API or external package downloads.  
  *Human Action:* Directed the AI to proceed to Stage 2 directions based strictly on these empirical findings.
* **Files Changed:** Created `STAGE_1_AND_2_DISCOVERY_REPORT.md` (Artifact).
* **Tests Performed:** Diagnostic schema check scripts via PowerShell.
* **Known Limitations:** Domain units in `manual_logs` required explicit normalization rules (`kL -> L`, `bags -> kg`).

---

### Entry 2: Stage 2 — Product Direction Selection
* **Milestone:** Stage 2 — Propose Three Product Directions
* **Date & Timestamp:** 2026-10-24 12:19:14
* **AI Tool Used:** Antigravity / Gemini 3.8
* **Prompt Submitted:**  
  *Request for three distinct, grounded product directions with 15-point breakdowns, hardware budgets, failure modes, and comparison tables.*
* **AI Output Summary:**  
  Formulated 3 directions:
  1. *EcoGrid EdgeCore:* Focus on smart-bin sorting and gateway buffering.
  2. *CircuPulse Campus:* Closed-loop circular grid, 12-hr demand forecasting, organic waste composting balance, and behavioral incentives.
  3. *TerraSense Audit & Action:* Forensic maintenance telemetry engine.  
  Recommended Direction 2 for 100% problem statement coverage.
* **Human Evaluation & Decisions:**  
  *Accepted:* The team selected and formally approved **Direction 2: CircuPulse Campus** because it uniquely covers all 8 problem requirements and utilizes all 7 datasets.
* **Files Changed:** Updated `STAGE_1_AND_2_DISCOVERY_REPORT.md`.
* **Human Approval Given:** Document approved by team at 12:25:42.

---

### Entry 3: Milestone 1 — Data Ingestion & Multi-Source Fusion
* **Milestone:** Implementation Milestone 1
* **Date & Timestamp:** 2026-10-24 12:27:42
* **Prompt Submitted:**  
  *Team approved Milestone 1: Build robust data pipeline, unit harmonization, and relational loaders.*
* **AI Output Summary:**  
  Created `modules/data_loader.py` and `tests/test_data_loader.py`. Implemented exact conversion formulas (`1 kL = 1000 L`, `1 bag = 8.0 kg`, `1 unit = 1 kWh`) and KPI aggregators.
* **Human Evaluation & Decisions:**  
  Verified that zero rows were dropped during join operations. Confirmed arrival delay was properly captured in `ingestion_delay_hours`.
* **Files Changed:** `modules/data_loader.py`, `tests/test_data_loader.py`.
* **Tests Performed:** `python tests/test_data_loader.py` — 7/7 tests passed.
* **Results:** Verified 8 buildings, 120 calendar days, 960 daily summaries, 23,192 hourly records, 415 manual logs, 6,314 train events, and 1,601 test events.

---

### Entry 4: Milestone 2 — Machine Learning & Predictive Engines
* **Milestone:** Implementation Milestone 2
* **Date & Timestamp:** 2026-10-24 12:29:58
* **Prompt Submitted:**  
  *Team approved Milestone 2: Build closed-form Ridge forecaster and real-time edge classifier in pure NumPy.*
* **AI Output Summary:**  
  Created `modules/ml_models.py` and `tests/test_ml_models.py`:
  - `EdgeWasteClassifier`: Gaussian Naive Bayes modeling 5 sensor dimensions across 6 waste categories.
  - `DemandForecaster`: Autoregressive Ridge Regression with cyclical $24\text{-hr}$ sine/cosine encodings, multi-day lags, and $95\%$ confidence bounds.
* **Human Evaluation & Decisions:**  
  *Accepted:* Model achieved **85.11% accuracy** (exceeding $>85\%$ target) and **1.46 ms latency** (vastly beating $<2.0\text{ s}$ target). Forecaster achieved **6.05 kWh MAE** vs **26.42 kWh baseline** (**77.1% error reduction**).
* **Files Changed:** `modules/ml_models.py`, `tests/test_ml_models.py`.
* **Tests Performed:** `python tests/test_ml_models.py` — All tests passed.

---

### Entry 5: Milestone 3 — Buffer Resilience, Circular Balance & Forensics
* **Milestone:** Implementation Milestone 3
* **Date & Timestamp:** 2026-10-24 12:33:18
* **Prompt Submitted:**  
  *Team approved Milestone 3: Implement gateway buffer deduplication, circular mass balance, forensic incident detector, and CircuCredit leaderboard.*
* **AI Output Summary:**  
  Created `modules/buffer_engine.py`, `modules/circular_logic.py`, and `tests/test_circular_logic.py`. Deduplicated 368 network retries down to 23,008 unique records. Identified 4 corroborated real-world incidents from `manual_logs.csv`. Created fair per-capita normalized dorm scoring.
* **Human Evaluation & Decisions:**  
  *Accepted:* Confirmed that per-capita normalization prevents large hostels (600+ students) from being unfairly penalized.
* **Files Changed:** `modules/buffer_engine.py`, `modules/circular_logic.py`, `tests/test_circular_logic.py`.
* **Tests Performed:** `python tests/test_circular_logic.py` — 4/4 tests passed.

---

### Entry 6: Milestone 4 — Interactive Streamlit Dashboard & End-to-End Testing
* **Milestone:** Implementation Milestone 4
* **Date & Timestamp:** 2026-10-24 12:34:59
* **Prompt Submitted:**  
  *Team approved Milestone 4: Build multi-view Streamlit UI and execute full integration testing.*
* **AI Output Summary:**  
  Built `modules/ui_views.py` and `app.py`. Created end-to-end integration test `tests/test_full_system.py`. Resolved Windows CP1252 terminal Unicode output formatting.
* **Human Evaluation & Decisions:**  
  *Accepted:* Verified that all 6 views load seamlessly and the entire end-to-end data pipeline executes in **0.23 seconds**.
* **Files Changed:** `app.py`, `modules/ui_views.py`, `tests/test_full_system.py`.
* **Tests Performed:** `python tests/test_full_system.py` — Passed in 0.23s.

---

### Entry 7: Milestone 5 — Final Submission Deliverables
* **Milestone:** Final Deliverables & Pitch Preparation
* **Date & Timestamp:** 2026-10-24 12:39:37
* **Prompt Submitted:**  
  *Team approved Milestone 5: Generate test predictions, prompt workbook, and 2.5-minute pitch video script.*
* **AI Output Summary:**  
  Generated `waste_events_test_predictions.csv` (1,601 records classified). Created `PROMPT_WORKBOOK.md` and `DEMO_SCRIPT.md`.
* **Human Evaluation & Decisions:**  
  Final review of all documentation, code integrity, and submission guidelines.
* **Files Changed:** `waste_events_test_predictions.csv`, `PROMPT_WORKBOOK.md`, `DEMO_SCRIPT.md`.

---

## 3. Human Engineering Principles & Decisions Applied

1. **Grounded in Reality, Not Hallucinations:** We refused to use synthetic placeholders when the authentic 120-day competition benchmark package was available. Every metric displayed in the dashboard is calculated from the true dataset.
2. **Zero-Dependency Resilience:** Operating in an isolated local sandbox with no internet required strict adherence to foundational mathematics. Building Ridge Regression and Gaussian Naive Bayes directly in NumPy proved that elegant, interpretable ML models outperform bloated black-box frameworks on edge devices.
3. **Equitable Gamification:** By normalizing energy and water consumption by occupant-days ($kWh/\text{person}\cdot\text{day}$), we established a fair gamification standard that rewards genuine behavioral conservation rather than structural building size.
4. **Actionable Explainability:** Rather than generating isolated anomaly scores, our system ties spikes directly to human evidence in custodial logs, providing facilities teams with actionable work orders.

---

## 4. Known System Limitations & Future Roadmap

* **Continuous Model Retraining:** The current classifier uses fixed prior distributions computed from the initial 6,314 events. In a multi-semester deployment, an automated drift-detection mechanism should trigger continuous Bayesian parameter updates as packaging materials change.
* **Physical Hardware Actuation:** While the edge classifier outputs motor routing signals in <1.5 ms, physical motorized diverter gates and automated greywater valves remain simulated in software.
* **Natural Language Extraction:** Manual log notes are currently matched via keyword and time-window heuristics; future iterations could incorporate an embedded edge LLM for conversational maintenance work-order generation.

