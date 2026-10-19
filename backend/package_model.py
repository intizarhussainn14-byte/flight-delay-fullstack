import json
from pathlib import Path

import joblib

ROOT = Path(__file__).resolve().parents[1]

model_path = ROOT / "models" / "flight_delay_model.pkl"
metadata_path = ROOT / "models" / "model_metadata.json"

pipeline = joblib.load(model_path)
metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

features = metadata["features"]

if list(pipeline.feature_names_in_) != features:
    raise ValueError("Metadata feature order differs from the saved model.")

bundle = {
    "pipeline": pipeline,
    "features": features,
    "task": "classification",
    "model_version": "1.0",
    "classes": pipeline.classes_.tolist(),
    "target": metadata["target"],
    "categorical_features": metadata["categorical_features"],
    "numeric_features": metadata["numeric_features"],
}

output = ROOT / "backend" / "models" / "model_bundle.joblib"
output.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(bundle, output, compress=3)

print("Saved:", output)
print("Model:", metadata["best_model"])
print("Features:", len(features))
print("Classes:", bundle["classes"])
print("PASS: model packaged")