import json
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
bundle = joblib.load(ROOT / "backend/models/model_bundle.joblib")
features = bundle["features"]

sample = pd.read_csv(ROOT / "data/flights_sample.csv", nrows=1)

missing = [name for name in features if name not in sample.columns]
if missing:
    raise ValueError(f"Missing features: {missing}")

# Convert through pandas JSON to produce standard JSON values.
payload = json.loads(
    sample.loc[:, features].to_json(orient="records")
)[0]

output = ROOT / "backend/test_payload.json"
output.write_text(json.dumps(payload, indent=2), encoding="utf-8")

print("Saved:", output)
print("Features:", len(payload))
print("PASS: sample payload created")