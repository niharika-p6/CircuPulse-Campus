# Antigravity: mandatory dataset inspection instructions

Before coding, inspect `DATASET_GUIDE.md`, the original README/problem statement, `03_documentation/DATASET_CATALOG.csv`, and `03_documentation/DATA_DICTIONARY.csv`.

Then:
1. List all available datasets and report row counts, columns, missing values, target columns, date/time columns, and join keys.
2. Explain which dataset will power each planned feature and why.
3. Do not alter files in `01_original_files/`.
4. Use `daily_master.csv` only as the pre-joined daily convenience table; do not merge its source tables into it again.
5. Use hourly_streams for hourly analysis and preserve both event timestamp and received_at.
6. Use waste_events_train for model training with category as the target; do not use category as an input feature. Keep waste_events_test separate.
7. Treat manual_logs building aliases and units carefully. Do not guess unmatched aliases or convert unlike units without an explicit rule.
8. Report the validation checks and unresolved data-quality issues before implementing the application.
9. If any relationship or unit is unclear, state the uncertainty and ask rather than infer.
10. Only after the inspection report is complete, begin implementation.
