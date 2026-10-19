from pathlib import Path
import math

import joblib
import pandas as pd
from flask import Flask, jsonify, request

BASE = Path(__file__).resolve().parent
BUNDLE = joblib.load(BASE / "models/model_bundle.joblib")

MODEL = BUNDLE["pipeline"]
FEATURES = BUNDLE["features"]
NUMERIC = set(BUNDLE["numeric_features"])
CATEGORICAL = set(BUNDLE["categorical_features"])

LABELS = {
    0: "Not delayed by 15 minutes or more",
    1: "Delayed by 15 minutes or more",
}

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(
        status="ok",
        features=len(FEATURES),
        task=BUNDLE["task"],
        model_version=BUNDLE["model_version"],
    )


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object"), 400

    missing = [name for name in FEATURES if name not in data]
    extra = [name for name in data if name not in FEATURES]

    if missing or extra:
        return jsonify(
            error="Input schema mismatch",
            missing=missing,
            extra=extra,
        ), 400

    # Validate input types before calling the model.
    for name in FEATURES:
        value = data[name]

        if name in NUMERIC:
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                return jsonify(
                    error=f"{name} must be a finite number"
                ), 400

        elif name in CATEGORICAL:
            if not isinstance(value, str) or not value.strip():
                return jsonify(
                    error=f"{name} must be a non-empty string"
                ), 400

    frame = pd.DataFrame(
        [[data[name] for name in FEATURES]],
        columns=FEATURES,
    )

    try:
        prediction = int(MODEL.predict(frame)[0])
        probabilities = MODEL.predict_proba(frame)[0]
        classes = MODEL.classes_.tolist()

        return jsonify(
            prediction=prediction,
            label=LABELS[prediction],
            task=BUNDLE["task"],
            classes=classes,
            probabilities=probabilities.tolist(),
            delay_probability=float(probabilities[classes.index(1)]),
            model_version=BUNDLE["model_version"],
            disclaimer="Teaching prototype; not a guarantee of flight status.",
        )

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify(error="Prediction processing failed"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)