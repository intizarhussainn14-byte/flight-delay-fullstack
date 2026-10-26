# FlightInsight — Flight Delay Prediction

A full-stack machine learning teaching application that predicts whether a flight will arrive at least 15 minutes late. The Angular interface is hosted on GitHub Pages and sends prediction requests to a Flask API deployed on Vercel.

## Links

- [Live application](https://intizarhussainn14-byte.github.io/flight-delay-fullstack/)
- [Backend health endpoint](https://flight-delay-fullstack.vercel.app/health)
- [Repository](https://github.com/intizarhussainn14-byte/flight-delay-fullstack)
- [CI and deployment runs](https://github.com/intizarhussainn14-byte/flight-delay-fullstack/actions)

## Deployment and demonstration

GitHub Pages serves the static Angular files. The Flask API on Vercel loads the packaged Random Forest pipeline, validates requests, and returns predictions. CORS allows requests from the GitHub Pages origin.

Live predictions are enabled on the public website. No local Python server is required to use it.

1. Open the live application.
2. Select **Load sample**.
3. Select **Analyze Flight**.
4. The included sample returns class **0**, displayed as **No 15-minute delay predicted**, with approximately **39.5%** estimated probability of a delay of at least 15 minutes.

This public sample prediction was demonstrated successfully. It verifies the deployed request flow for that sample, not overall predictive accuracy or service availability.

## Dataset and research reference

Dataset: [Flight Delay Dataset (2018–2022)](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022), published on Kaggle by robikscube.

This project uses `Combined_Flights_2022.csv`. The preparation script:

- Excludes cancelled and diverted flights.
- Removes records with a missing target.
- Samples 25% of the remaining records within each processing chunk, using seed 42.
- Adds five engineered features.
- Exports `flights_sample.csv`.

Large datasets are excluded from Git. Obtain the source data from Kaggle and review its usage terms before redistribution.

Research reference:

AlBassam, S. A. A., & AlShahrani, S. D. N. (2025). Flight delay prediction: Evaluating machine learning algorithms for enhanced accuracy. *PLOS ONE, 20*(12), e0335141. https://doi.org/10.1371/journal.pone.0335141

This student implementation uses its own training configuration and evaluation results. It does not reproduce the paper’s complete experimental methodology.

## Models and recorded evaluation

Decision Tree and Random Forest classifiers were trained using an 80/20 stratified split with random seed 42. Both use balanced class weights.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| Decision Tree | 0.6608 | 0.3366 | 0.5849 | 0.4273 | 0.6843 |
| Random Forest | 0.6848 | 0.3602 | 0.5891 | 0.4471 | 0.7074 |

These are recorded hold-out results from `models/results.csv`. Precision, recall, and F1 describe the delayed class.

Random Forest was selected because it had the higher F1 score on this split. The application serves this selected model; it does not combine both classifiers.

Because model selection used the same hold-out results shown above, these scores are not an independent final evaluation of the selected model.

## Target and input schema

Target: `ArrDel15`.

- `0`: arrival delay below 15 minutes.
- `1`: arrival delay of at least 15 minutes.

The model predicts a class and class probabilities; it does not predict delay duration.

The input contains **41 features: 27 numeric and 14 categorical**. Exact names, order, and types are recorded in `models/model_metadata.json`.

### Numeric features

`Quarter`, `Month`, `DayofMonth`, `DayOfWeek`, `CRSDepTime`, `CRSArrTime`, `CRSElapsedTime`, `Distance`, `DistanceGroup`, `Flight_Number_Marketing_Airline`, `Flight_Number_Operating_Airline`, `DOT_ID_Marketing_Airline`, `DOT_ID_Operating_Airline`, `OriginAirportID`, `OriginAirportSeqID`, `OriginCityMarketID`, `OriginStateFips`, `OriginWac`, `DestAirportID`, `DestAirportSeqID`, `DestCityMarketID`, `DestStateFips`, `DestWac`, `DepHour`, `ArrHour`, `DayOfYear`, `IsWeekend`.

### Categorical features

`Airline`, `Origin`, `Dest`, `OriginState`, `DestState`, `Marketing_Airline_Network`, `Operated_or_Branded_Code_Share_Partners`, `DepTimeBlk`, `ArrTimeBlk`, `Operating_Airline`, `IATA_Code_Marketing_Airline`, `IATA_Code_Operating_Airline`, `Tail_Number`, `Route`.

### Engineered features

| Feature | Calculation |
| --- | --- |
| `DepHour` | `(CRSDepTime // 100) % 24` |
| `ArrHour` | `(CRSArrTime // 100) % 24` |
| `DayOfYear` | Day number derived from `FlightDate` |
| `IsWeekend` | `1` when `DayOfWeek` is 6 or 7; otherwise `0` |
| `Route` | `Origin + "_" + Dest` |

Feature engineering occurs in the dataset preparation script, outside the saved preprocessing pipeline. The current form supplies all 41 features explicitly. Related fields must remain consistent. Never include the target in prediction requests.

## Saved preprocessing and model

`backend/models/model_bundle.joblib` contains:

- A fitted pipeline containing a `ColumnTransformer` and Random Forest classifier.
- An `OrdinalEncoder` for categorical features and numeric passthrough.
- Feature names, task, class labels, and model version.

Unknown categories are encoded as `-1` by the fitted encoder. Supply meaningful values consistent with the training schema. Load only trusted model artifacts. No retraining is required to run the application.

## Environment

Verified development environment:

| Component | Version |
| --- | --- |
| Python | 3.12.10 |
| scikit-learn | 1.9.1 |
| pandas | 3.0.6 |
| NumPy | 2.5.3 |
| SciPy | 1.18.1 |
| joblib | 1.6.0 |
| Node.js | 24.22.0 |
| npm | 11.19.1 |
| Angular | 22 |

Backend dependencies are declared in `backend/requirements.txt`. Frontend dependencies are recorded in `frontend/package-lock.json`. The backend Python version is configured in `backend/.python-version`.

## Installation on Windows

Run in Command Prompt:

```bat
git clone https://github.com/intizarhussainn14-byte/flight-delay-fullstack.git
cd flight-delay-fullstack
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r backend\requirements.txt
cd frontend
npm ci
cd ..
```

In PowerShell, activate the environment using `.\.venv\Scripts\Activate.ps1`.

## Run locally

### Current frontend configuration: hosted backend

`frontend/src/app/prediction.service.ts` currently sends requests directly to:

```text
https://flight-delay-fullstack.vercel.app/predict
```

To run the Angular interface locally using that hosted backend:

```bat
cd frontend
npx ng serve --open
```

Open `http://localhost:4200`, select **Load sample**, then **Analyze Flight**. Internet access and availability of the hosted API are required. The backend CORS configuration includes the local Angular origins.

### Run both frontend and backend locally

For a fully local setup, first change the request URL in `frontend/src/app/prediction.service.ts` from the hosted URL to `/api/predict`. This is a local development change; restore the hosted URL before publishing the frontend to GitHub Pages.

Terminal 1, from the repository root:

```bat
.venv\Scripts\activate.bat
python backend\app.py
```

Health endpoint: `http://127.0.0.1:5000/health`. Keep this terminal running.

Terminal 2, from the repository root:

```bat
cd frontend
npx ng serve --open --proxy-config proxy.conf.cjs
```

The development proxy forwards `/api/predict` to Flask `/predict`. It is used only when the frontend service calls the relative `/api/predict` URL.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Service status, feature count, task, and model version |
| POST | `/predict` | Prediction from a JSON object containing all 41 features |

Hosted base URL: `https://flight-delay-fullstack.vercel.app`.

The API rejects malformed JSON, missing or extra fields, invalid numeric types, and empty categorical values. Current validation does not enforce every feature’s domain range or cross-field consistency. A successful response is not proof that an arbitrary flight profile is realistic.

Example hosted request from the repository root:

```bat
curl.exe -i -X POST "https://flight-delay-fullstack.vercel.app/predict" -H "Content-Type: application/json" --data-binary "@backend/test_payload.json"
```

Example local request while Flask is running:

```bat
curl.exe --noproxy "*" -i -X POST "http://127.0.0.1:5000/predict" -H "Content-Type: application/json" --data-binary "@backend/test_payload.json"
```

Example sample response:

```json
{
  "classes": [0, 1],
  "delay_probability": 0.39497275308848623,
  "disclaimer": "Teaching prototype; not a guarantee of flight status.",
  "label": "Not delayed by 15 minutes or more",
  "model_version": "1.0",
  "prediction": 0,
  "probabilities": [0.6050272469115138, 0.39497275308848623],
  "task": "classification"
}
```

The backend has no root-page route. A `404` at its base URL is expected; use `/health` to check it.

## Automated tests

From the repository root with the Python environment activated:

```bat
python -m pytest -q backend\tests
```

Eight tests cover the health response, a valid prediction and expected probability, a missing feature, invalid JSON, an extra feature, and three invalid numeric input cases.

These tests use Flask’s test client and require no running Flask server. They verify API behavior and a known sample, not overall predictive performance. The recorded local result is **8 passed**.

## Production build

```bat
cd frontend
npm run build
```

Browser output: `frontend/dist/frontend/browser`.

## CI and deployment

### GitHub Actions CI

`.github/workflows/ci.yml` installs Python dependencies, checks dependency compatibility, runs the eight model-backed API tests on Linux, installs frontend dependencies with `npm ci`, builds Angular, and uploads the `angular-build` artifact.

### GitHub Pages frontend

`.github/workflows/pages.yml` builds Angular with base href `/flight-delay-fullstack/`, uploads the browser output, and deploys it to GitHub Pages.

The Pages workflow runs separately from CI; it is not gated on CI success. Check both workflows after changes.

### Vercel backend

The Vercel project uses the `backend` root directory and serves the Flask application from `app.py`. The packaged model is included under `backend/models/`. Backend deployments are managed separately from the GitHub Pages workflow.

The frontend uses the hosted `/predict` endpoint. If the backend domain changes, update `prediction.service.ts` and redeploy the frontend. If the frontend origin changes, update the backend CORS allowlist and redeploy the backend.

## Training and preparation scripts

`src/` contains dataset inspection, preparation, training, and original model-testing scripts. Re-running training requires the source dataset under `data/` and an existing `models/` output folder.

Some development utilities require files intentionally excluded from the repository:

| Utility | Required excluded files |
| --- | --- |
| `backend/package_model.py` | Original `models/flight_delay_model.pkl` |
| `backend/make_payload.py` | `data/flights_sample.csv` |
| `backend/test_pipeline.py` | Original `models/flight_delay_model.pkl` |
| `src/test_model.py` | Original model and sample CSV |

These files remain in the original training workspace. They are not needed to run Flask, the Angular form, or the eight backend API tests because the packaged bundle and sample JSON are included.

## Limitations

- Research and teaching prototype, not an operational flight-status service.
- Trained using historical 2022 flight data; performance on future flights may differ.
- Probabilities have not been independently calibrated.
- Cancelled and diverted flights were excluded during preparation.
- No live airline, weather, or airport feed is connected.
- The form requires 41 mutually consistent features; validation does not enforce all domain rules.
- Model comparison used one stratified random split, rather than an independent chronological final evaluation.
- Public predictions depend on the hosted API’s availability and hosting resource limits.

