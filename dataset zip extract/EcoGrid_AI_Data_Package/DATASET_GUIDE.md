# EcoGrid AI — Dataset Guide (read this first)

## Purpose
This package organizes the provided campus sustainability datasets so a developer or AI coding agent can identify each dataset, understand its grain, and avoid accidental joins or training/test leakage.

## Start here
1. Read this guide and `03_documentation/DATA_DICTIONARY.csv`.
2. Read the original `README_data_guide.md` and `PROBLEM_STATEMENT_AND_CONSTRAINTS.md` in `01_original_files/`.
3. Use `02_csv_for_antigravity/` for easy programmatic loading. UTF-8 CSVs are provided.
4. Use `EcoGrid_AI_Data_Workbook.xlsx` for human inspection.
5. Read `04_validation/validation_checks.csv` and `missing_values_report.csv` before modeling.

## Dataset map
- `buildings.csv`: one row per building; lookup table for building metadata.
- `calendar.csv`: one row per date; calendar and weather context.
- `daily_summary.csv`: one row per building and date; daily resource use, occupancy, and waste measures.
- `daily_master.csv`: derived join of `daily_summary` + `buildings` on `building_id` + `calendar` on `date`. This is a convenience table, not a new raw source.
- `hourly_streams.csv`: hourly resource/footfall records. Keep `timestamp` (event time) distinct from `received_at` (arrival time); late arrivals are meaningful.
- `manual_logs.csv`: manual operational logs. Includes two additive helper columns: `building_id_normalized` and `building_match_status`. Original `building` label, value, unit, note, and all original rows are retained. Empty normalized IDs mean the alias did not match the explicit mapping; do not guess.
- `waste_events_train.csv`: labeled waste sensor events. `category` is the prediction target. Do not include it among model input features.
- `waste_events_test.csv`: test/inference events with no `category` target in the provided source. Keep it separate from training.

## Raw originals vs normalized files
`01_original_files/` contains the original input files extracted from the supplied ZIP without editing their contents.
`02_csv_for_antigravity/` contains CSV copies with date/time fields formatted consistently for easier parsing. The manual-log CSV adds normalized building-ID helper columns; no source columns are removed.
`EcoGrid_AI_Data_Workbook.xlsx` contains clearly named raw sheets, a derived master join, a normalized manual-log view, a dataset catalog, and a data dictionary.

## Join rules
- Daily summary -> buildings: many-to-one on `building_id`.
- Daily summary -> calendar: many-to-one on `date`.
- Do not join daily summary to hourly streams unless a specific analysis requires it. Their grains differ.
- Do not join manual logs by building name without first using/validating the alias mapping and units.
- Waste event tables can join to buildings on `building_id` if building metadata is needed; do not join waste events to daily rows unless a date/time aggregation is deliberately designed.
- Validate row counts before and after every merge. Use explicit merge validation and check unmatched keys.

## Data handling rules
- Never overwrite the original source files.
- Do not silently fill missing values with zero. A blank is not the same as zero.
- Do not assume all missing values mean the same thing; inspect context and the original data guide.
- Do not sum values across incompatible units. `manual_logs.unit` must be respected.
- Treat `received_at` as arrival time, not event time.
- For time-based train/test evaluation, split chronologically where appropriate to prevent leakage.
- For waste classification, train only on `waste_events_train.csv`; keep `waste_events_test.csv` separate.
- Check class imbalance before training and report metrics appropriate for multiclass classification.
- Do not claim that data represents live sensors or a live campus feed unless the application actually connects to such a source. These are provided datasets.
- Do not invent missing labels, sensor readings, units, or records.

## Known cautions
- `design_capacity`, `occupancy_avg`, sensor `metal_signal`, `transparency`, and `acoustic_hardness` require the original data guide or domain confirmation for exact semantics/scales. The dictionary flags these.
- Manual building aliases are inconsistent. The normalized column maps only explicitly listed aliases. Unmatched entries remain blank and are listed in validation.
- Date/time formatting is normalized in the CSV convenience files; original Excel files are preserved separately.
