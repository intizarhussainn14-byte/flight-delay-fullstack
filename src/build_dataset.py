import pandas as pd

CSV_PATH = "data/Combined_Flights_2022.csv"
OUT_PATH = "data/flights_sample.csv"
SAMPLE_FRACTION = 0.25
SEED = 42

# Raw columns known BEFORE departure
NUMERIC_RAW = [
    "Quarter", "Month", "DayofMonth", "DayOfWeek",
    "CRSDepTime", "CRSArrTime", "CRSElapsedTime",
    "Distance", "DistanceGroup",
    "Flight_Number_Marketing_Airline", "Flight_Number_Operating_Airline",
    "DOT_ID_Marketing_Airline", "DOT_ID_Operating_Airline",
    "OriginAirportID", "OriginAirportSeqID", "OriginCityMarketID",
    "OriginStateFips", "OriginWac",
    "DestAirportID", "DestAirportSeqID", "DestCityMarketID",
    "DestStateFips", "DestWac",
]
TEXT_RAW = [
    "Airline", "Origin", "Dest", "OriginState", "DestState",
    "Marketing_Airline_Network", "Operated_or_Branded_Code_Share_Partners",
    "DepTimeBlk", "ArrTimeBlk", "Operating_Airline",
    "IATA_Code_Marketing_Airline", "IATA_Code_Operating_Airline",
    "Tail_Number",
]
ENGINEERED = ["DepHour", "ArrHour", "DayOfYear", "IsWeekend", "Route"]
TARGET = "ArrDel15"

usecols = NUMERIC_RAW + TEXT_RAW + ["FlightDate", TARGET, "Cancelled", "Diverted"]
final_cols = NUMERIC_RAW + TEXT_RAW + ENGINEERED + [TARGET]

first = True
kept_total = 0
rows_read = 0

for chunk in pd.read_csv(CSV_PATH, usecols=usecols, chunksize=500_000):
    rows_read += len(chunk)

    # keep only completed flights (they have a target)
    chunk = chunk[~chunk["Cancelled"] & ~chunk["Diverted"]]
    chunk = chunk.dropna(subset=[TARGET])
    chunk = chunk.sample(frac=SAMPLE_FRACTION, random_state=SEED).copy()

    # engineered features (all known before departure)
    chunk["DepHour"] = (chunk["CRSDepTime"] // 100) % 24
    chunk["ArrHour"] = (chunk["CRSArrTime"] // 100) % 24
    chunk["DayOfYear"] = pd.to_datetime(chunk["FlightDate"]).dt.dayofyear
    chunk["IsWeekend"] = chunk["DayOfWeek"].isin([6, 7]).astype("int8")
    chunk["Route"] = chunk["Origin"] + "_" + chunk["Dest"]

    chunk["Tail_Number"] = chunk["Tail_Number"].fillna("UNKNOWN")
    chunk[TARGET] = chunk[TARGET].astype("int8")
    chunk = chunk[final_cols]

    chunk.to_csv(OUT_PATH, mode="w" if first else "a", header=first, index=False)
    first = False
    kept_total += len(chunk)
    print(f"read {rows_read:,} rows | kept so far {kept_total:,}", end="\r")

print(f"\nSaved {OUT_PATH} with {kept_total:,} rows")

df = pd.read_csv(OUT_PATH)
print("Shape:", df.shape)
print("Number of features (excluding target):", df.shape[1] - 1)
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))
print("\nClass distribution:")
print(df[TARGET].value_counts())
print((df[TARGET].value_counts(normalize=True) * 100).round(2))