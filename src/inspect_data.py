import os
import numpy as np
import pandas as pd

CSV_PATH = "data/Combined_Flights_2022.csv"
CHUNK = 200_000   # rows read at a time (small = safe for 8 GB RAM)

print(f"File size: {os.path.getsize(CSV_PATH) / 1024**3:.2f} GB")

# ---- Part 1: columns and data types from a small sample ----
sample = pd.read_csv(CSV_PATH, nrows=50_000)
print("\n--- COLUMNS ---")
print("Number of columns:", sample.shape[1])
print(list(sample.columns))
print("\n--- DATA TYPES (from first 50,000 rows) ---")
print(sample.dtypes.to_string())
print("\n--- FIRST 2 ROWS ---")
print(sample.head(2).T.to_string())
del sample

# ---- Part 2: rows, missing values, duplicates, in chunks ----
total_rows = 0
missing_total = None
hash_list = []

for i, chunk in enumerate(pd.read_csv(CSV_PATH, chunksize=CHUNK)):
    total_rows += len(chunk)
    m = chunk.isna().sum()
    missing_total = m if missing_total is None else missing_total + m
    hash_list.append(pd.util.hash_pandas_object(chunk, index=False).values)
    print(f"  processed {total_rows:,} rows...", end="\r")

print(f"\n\n--- TOTAL ROWS ---\n{total_rows:,}")

print("\n--- MISSING VALUES (columns with any) ---")
miss = missing_total[missing_total > 0].sort_values(ascending=False)
report = pd.DataFrame({
    "missing_count": miss,
    "missing_pct": (miss / total_rows * 100).round(2),
})
print(report.to_string() if len(report) else "No missing values.")

all_hashes = np.concatenate(hash_list)
dupes = total_rows - len(np.unique(all_hashes))
print(f"\n--- DUPLICATE ROWS (approx, by row fingerprint) ---\n{dupes:,}")

print("\n--- REQUIREMENT CHECK ---")
n_cols = len(missing_total)
print(f"Rows >= 100,000?               {total_rows >= 100_000}  ({total_rows:,})")
print(f"Total columns:                 {n_cols}")
print(f"Columns >= 35 (incl. target)?  {n_cols >= 35}")
print(f"Predictors >= 35 (excl. target)? {n_cols - 1 >= 35}")