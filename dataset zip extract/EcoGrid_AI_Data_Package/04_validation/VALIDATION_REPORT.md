# Validation Report

This report compares the package outputs to the original ZIP dataset files.

- **PASS — All seven source datasets found:** Found 7 source Excel datasets: buildings, calendar, daily_summary, hourly_streams, manual_logs, waste_events_test, waste_events_train.
- **PASS — buildings: row/column count retained:** Original 8 rows x 10 columns; canonical CSV 8 rows x 10 columns.
- **PASS — calendar: row/column count retained:** Original 120 rows x 7 columns; canonical CSV 120 rows x 7 columns.
- **PASS — daily_summary: row/column count retained:** Original 960 rows x 14 columns; canonical CSV 960 rows x 14 columns.
- **PASS — hourly_streams: row/column count retained:** Original 23192 rows x 7 columns; canonical CSV 23192 rows x 7 columns.
- **PASS — manual_logs: row/column count retained:** Original 415 rows x 8 columns; canonical CSV 415 rows x 10 columns.
- **PASS — waste_events_test: row/column count retained:** Original 1601 rows x 9 columns; canonical CSV 1601 rows x 9 columns.
- **PASS — waste_events_train: row/column count retained:** Original 6314 rows x 10 columns; canonical CSV 6314 rows x 10 columns.
- **PASS — Daily date-building key unique:** 0 duplicate date-building keys.
- **PASS — Building metadata join complete:** 0 daily rows without building metadata.
- **PASS — Calendar join complete:** 0 daily rows without calendar match.
- **PASS — Calendar date unique:** 0 duplicate calendar dates.
- **PASS — Train/test target separation:** Training data has category target; test data does not.
- **PASS — Manual log aliases documented:** 415 of 415 logs matched to building IDs; 0 remain unmatched/blank in normalized ID. Raw labels preserved.

## Missing values
See `missing_values_report.csv`. Missing source values were not filled or removed.

## Important limitation
A PASS on structural checks does not prove every field's domain meaning. Ambiguous units/scales are flagged in the data dictionary and must be confirmed from the original guide or dataset owner.