Prompt to Product (P2P 2026): Synthetic / Hypothetical Campus Telemetry & Resource Dataset Guide
=================================================================================================

**Problem Statement:** Predictive Circular-Resource Grid for a Multi-Building Campus  
**Dataset Type:** Synthetic / Hypothetical Operational Benchmark  
**Monitoring Period:** 20 June 2026 to 17 October 2026 (120 Days)  
**Campus Scope:** 8 Buildings (Academic Blocks, Hostels, Central Mess, Lab Complex)  

--------------------------------------------------------------------------------
Operational Context & Overview
--------------------------------------------------------------------------------

This benchmark dataset represents a **synthetic / hypothetical operational telemetry and facilities collection**, specifically constructed to simulate an 8-building academic and residential campus for the problem statement *"Predictive Circular-Resource Grid for a Multi-Building Campus"*.

Modeled after real-world institutional micro-grids and smart facility infrastructure, the dataset reflects authentic operational field conditions—including asynchronous telemetry sampling, intermittent gateway dropouts, sensor calibration variances, meteorological influences, and departmental manual field logs. Engineering resilient pipelines that handle real-world data noise and close circular resource loops (energy, water, and waste) is a core technical objective of this competition.

--------------------------------------------------------------------------------
1. File Manifest
--------------------------------------------------------------------------------

The dataset package consists of the following 7 core relational tables:

| File | Rows | Description |
|---|---|---|
| `buildings.csv` | 8 | Structural metadata: building type, floors, built area ($m^2$), design capacity, solar array presence, on-site composting units |
| `calendar.csv` | 120 | Academic schedule (working days, weekends, holidays, exam windows, fests) joined with ambient meteorological feeds (mean temp, precipitation, humidity) |
| `daily_summary.csv` | 960 | Building-level daily aggregate logs: occupancy estimates, grid electricity, water draw, solar generation, segregated waste categories, diverted mass, and residual landfill |
| `hourly_streams.csv` | 23,192 | Time-series telemetry across all 8 buildings: active power load (kWh), water flow (L), solar output (kWh), and turnstile footfall counts (delivered as an asynchronous stream) |
| `manual_logs.csv` | 415 | Field operations records entered by hostel wardens, mess supervisors, and facility technicians (field observations, meter checks, variable units) |
| `waste_events_train.csv` | 6,314 | Smart-bin multi-sensor event records with verified ground-truth classification labels |
| `waste_events_test.csv` | 1,601 | Unlabelled smart-bin test events reserved for model evaluation and leaderboard scoring |

> **Format Note:** All datasets are provided in standard `.csv` format (for Python, Pandas, and ML pipelines) as well as pre-formatted `.xlsx` format inside the `excel_format/` subfolder for spreadsheet inspection.

--------------------------------------------------------------------------------
2. Schema & Measurement Units
--------------------------------------------------------------------------------

### Primary Identifiers & Joins
- `building_id`: Primary key (`B01` to `B08`), mapping to `buildings.csv`.
- Relational joins across tables use `building_id` along with `date` (YYYY-MM-DD) for daily records, or `timestamp` (YYYY-MM-DD HH:MM) for hourly streams.

### Campus Activity & Footfall
- `occupancy_avg`: Estimated daily building occupant count.
- `footfall`: Hourly entrance turnstile passage count. Cumulative hourly footfall approximates dynamic occupancy patterns.

### Energy & Water Utilities
- `electricity_kwh`: Active grid power draw (kilowatt-hours).
- `solar_generation_kwh`: Distributed rooftop photovoltaic generation (kilowatt-hours).
- `water_litres`: Potable and utility water consumption (litres).

### Segregated Waste & Circular Resource Streams
- `wet_organic_kg`, `dry_recyclable_kg`, `ewaste_kg`, `hazardous_kg`: Daily segregated mass by category.
- `composted_kg`: Mass diverted to decentralized campus composting units (`0` if building lacks a composting facility).
- `recycled_kg`: Mass diverted to certified recycling off-takers.
- `landfill_kg`: Residual non-diverted mass destined for municipal landfill.
- `contamination_pct`: Measured contamination percentage in segregated recycling streams.

### Meteorological & Event Drivers
- `avg_temp_c`, `rainfall_mm`, `humidity_pct`: Ambient weather metrics influencing HVAC and solar yields (from `calendar.csv`).
- `event`: Scheduled campus events (hackathons, recruitment drives, examinations, cultural fests) driving localized consumption surges.

--------------------------------------------------------------------------------
3. Telemetry Stream Dynamics & Edge Gateway Behaviour
--------------------------------------------------------------------------------

The time-series telemetry feed (`hourly_streams.csv`) simulates realistic IoT network behavior:

- **Sampling vs. Ingestion Timestamps:**  
  - `timestamp`: Time the measurement was captured by edge sensors.  
  - `received_at`: Server-side ingestion timestamp. Records arrive in order of `received_at`, which may not match chronological sampling order.
- **Gateway Dropouts & Local Buffering:** Sub-station communication links periodically experience interruptions. During dropouts, edge micro-controllers buffer readings locally and transmit them in burst batches upon reconnection. Unbuffered intervals represent packet loss and can be identified via sampling interval deltas.
- **Duplicate Retransmissions:** Network retries occasionally produce duplicate readings with minor jitter. Ingestion architectures must perform deterministic deduplication.

--------------------------------------------------------------------------------
4. Smart-Bin Edge Multi-Modal Sensor Specifications
--------------------------------------------------------------------------------

Each sorting event recorded in `waste_events_train.csv` and `waste_events_test.csv` captures physical sensor responses from an edge-deployed smart disposal receptacle:

| Sensor Attribute | Sensor Hardware Type | Measurement Description |
|---|---|---|
| `weight_g` | Precision load cell | Disposed item mass (grams) |
| `moisture_pct` | Dielectric moisture probe | Surface & internal moisture content (0.0% – 100.0%) |
| `metal_signal` | Inductive proximity sensor | Binary / analog electromagnetic induction response |
| `transparency` | Optical transmission photodiode | Optical transmission coefficient (0.0 = opaque, 1.0 = clear) |
| `acoustic_hardness` | Impact vibration / piezo sensor | Material impact resonant frequency coefficient |

**Target Classification Classes (6):**
1. `food_organic` (Mess/cafeteria waste, peels, wet compostable matter)
2. `paper_cardboard` (Exam papers, cartons, dry packaging)
3. `plastic` (Bottles, wrappers, disposable containers)
4. `glass` (Laboratory glassware, beverage bottles)
5. `metal` (Beverage cans, foil, hardware scraps)
6. `ewaste` (Cables, battery cells, broken peripherals)

--------------------------------------------------------------------------------
5. Field Log Conventions & Operator Data Variances
--------------------------------------------------------------------------------

Field operational logs (`manual_logs.csv`) reflect varied record-keeping practices across shift staff:
- **Building Alias Aliasing:** Hostels and academic halls may be recorded under informal names (e.g., `"BH"`, `"Boys Hostle"`, and `"B05"` all denote Building B05).
- **Unit Heterogeneity:** Electricity may be logged in `kWh` or `units` (1 unit = 1 kWh); water in `L` or `kL` (1 kL = 1,000 L); waste in `kg` or standard `bags` (~8 kg per standard custodial bag).
- **Narrative Notes:** Records where `stream = "note"` contain qualitative observations (e.g., pump maintenance, leak reports, fest prep).

--------------------------------------------------------------------------------
6. Engineering Baselines & Assumptions
--------------------------------------------------------------------------------

Unless alternative parameters are justified in your system design report, the following campus constants apply:
- **Grid Carbon Emission Factor:** 0.70 kg $CO_2$ per kWh.
- **Commercial Utility Electricity Tariff:** Rs. 8.00 per kWh.
- **Water Pumping & Treatment Energy Intensity:** 0.85 kWh per 1,000 L.
- **Composting Diversion Potential:** Diverted wet organic waste yields high-grade compost at an average 4:1 conversion ratio by mass.

--------------------------------------------------------------------------------
7. Technical Evaluation Mapping
--------------------------------------------------------------------------------

Solutions are evaluated on how effectively their prompted systems address the technical challenges embedded within this benchmark:

| Technical Challenge | Relevant Data Sources |
|---|---|
| Multi-modal sensor fusion under noise | `hourly_streams`, `daily_summary`, `manual_logs`, `waste_events_train` |
| Real-time edge classification (>85% target) | `waste_events_train` & `waste_events_test` |
| Short-horizon demand forecasting (6–12 hr) | `hourly_streams` combined with `calendar` (events and weather) |
| Intermittent telemetry & buffer recovery | `hourly_streams` (sampling lag, buffering intervals, retransmissions) |
| Root-cause anomaly attribution | Telemetry trends cross-referenced with `manual_logs` and `calendar` |
| Circular allocation & facility dashboard UX | `daily_summary`, `buildings`, and smart-bin routing |

--------------------------------------------------------------------------------
8. Sensor Telemetry & Field Testing Data
--------------------------------------------------------------------------------

### Overview of Smart-Bin Sensor Records
The smart-bin event logs capture real-world physical measurements taken at the point of disposal across campus bins:
- Physical sensor telemetry comprises 5 continuous indicators: `weight_g`, `moisture_pct`, `metal_signal`, `transparency`, and `acoustic_hardness`.
- Because these reflect hardware deployed in busy campus environments, readings naturally contain physical sensor noise, environmental moisture variances, and material edge cases.

### Dataset Structure: Historical Reference vs. Live Field Streams
The smart-bin data is structured into two complementary files:

1. **`waste_events_train.csv` (Historical Annotated Logs &mdash; 6,314 Events):**  
   Contains complete sensor readings alongside verified historical category labels (`waste_class`). This dataset serves as reference data for understanding sensor distributions, feature correlations, and material response patterns across the 6 waste categories.

2. **`waste_events_test.csv` (Active Field Stream &mdash; 1,601 Events):**  
   Contains sensor readings from 1,601 unlabelled active disposal events.  
   - This dataset represents real-world operational arrivals where the material type is unknown at the moment of disposal.
   - Teams may leverage this unlabelled stream to demonstrate how their product architecture handles live sensor feeds, automated categorization, and real-time facility alerts.
   - If your solution pipeline generates automated classifications for these test records, you may optionally include a predictions file (`waste_events_test_predictions.csv` with `event_id` and `predicted_class`) with your submission for benchmark verification.

--------------------------------------------------------------------------------
9. Submission Deliverables Summary
--------------------------------------------------------------------------------

Teams submit their final solution package via the official submission portal:

1. **Prompt Workbook:** Step-by-step prompt evolution log documenting tools used, prompt iterations, and verified public chat share links.
2. **Standardized 3-Page Report (PDF):** System architecture, data handling strategy, and UI screenshots.
3. **2.5-Minute Video Walkthrough:** Continuous screen recording demonstrating live UI dynamic recalculations across campus buildings and prompt tool execution.
4. **UI Screenshots Package:** High-resolution captures of the operational telemetry dashboard, circular waste allocations, and facility alerts.
*(Optional: `waste_events_test_predictions.csv` if your system outputs automated test stream predictions).*
