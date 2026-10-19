import pandas as pd

CSV_PATH = "data/Combined_Flights_2022.csv"
cols = ["Cancelled", "Diverted", "ArrDelay", "ArrDel15",
        "Airline", "Origin", "Dest", "Tail_Number"]

total = cancelled = diverted = 0
miss_target = miss_and_canc = miss_and_div = miss_neither = 0
on_time = delayed = 0
mismatch_ge15 = mismatch_gt15 = 0
uniq = {c: set() for c in ["Airline", "Origin", "Dest", "Tail_Number"]}

for chunk in pd.read_csv(CSV_PATH, usecols=cols, chunksize=500_000):
    total += len(chunk)
    cancelled += int(chunk["Cancelled"].sum())
    diverted += int(chunk["Diverted"].sum())

    miss = chunk["ArrDel15"].isna()
    miss_target += int(miss.sum())
    miss_and_canc += int((miss & chunk["Cancelled"]).sum())
    miss_and_div += int((miss & chunk["Diverted"]).sum())
    miss_neither += int((miss & ~chunk["Cancelled"] & ~chunk["Diverted"]).sum())

    valid = chunk[~miss]
    vc = valid["ArrDel15"].value_counts()
    on_time += int(vc.get(0.0, 0))
    delayed += int(vc.get(1.0, 0))

    # Which rule does ArrDel15 follow: ArrDelay >= 15 or ArrDelay > 15?
    mismatch_ge15 += int((valid["ArrDel15"] != (valid["ArrDelay"] >= 15).astype(float)).sum())
    mismatch_gt15 += int((valid["ArrDel15"] != (valid["ArrDelay"] > 15).astype(float)).sum())

    for c in uniq:
        uniq[c].update(chunk[c].dropna().unique())

print(f"Total rows:           {total:,}")
print(f"Cancelled flights:    {cancelled:,}")
print(f"Diverted flights:     {diverted:,}")

print("\n--- Rows where ArrDel15 is missing ---")
print(f"Total missing:              {miss_target:,}")
print(f"  ...that are Cancelled:    {miss_and_canc:,}")
print(f"  ...that are Diverted:     {miss_and_div:,}")
print(f"  ...neither (unexplained): {miss_neither:,}")

n = on_time + delayed
print("\n--- ArrDel15 class distribution (non-missing rows) ---")
print(f"0 (not delayed): {on_time:,} ({on_time / n * 100:.2f}%)")
print(f"1 (delayed):     {delayed:,} ({delayed / n * 100:.2f}%)")

print("\n--- Which rule does ArrDel15 follow? (fewer mismatches = the rule) ---")
print(f"Mismatches if rule is ArrDelay >= 15: {mismatch_ge15:,}")
print(f"Mismatches if rule is ArrDelay >  15: {mismatch_gt15:,}")

print("\n--- Unique values ---")
for c, s in uniq.items():
    print(f"{c}: {len(s):,}")