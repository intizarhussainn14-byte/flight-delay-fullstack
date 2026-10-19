import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

bundle = joblib.load(ROOT / "backend/models/model_bundle.joblib")
original = joblib.load(ROOT / "models/flight_delay_model.pkl")

payload = json.loads(
    (ROOT / "backend/test_payload.json").read_text(encoding="utf-8")
)

features = bundle["features"]
assert set(payload) == set(features), "Payload features do not match."

frame = pd.DataFrame(
    [[payload[name] for name in features]],
    columns=features,
)

prediction = bundle["pipeline"].predict(frame)
probabilities = bundle["pipeline"].predict_proba(frame)

np.testing.assert_array_equal(prediction, original.predict(frame))
np.testing.assert_allclose(
    probabilities,
    original.predict_proba(frame),
)

print("Prediction:", prediction.tolist())
print("Classes:", bundle["pipeline"].classes_.tolist())
print("Probabilities:", probabilities.round(3).tolist())
print("PASS: packaged model matches original")