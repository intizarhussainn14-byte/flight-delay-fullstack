# FlightInsight — Flight Delay Prediction

A full-stack machine learning teaching application that predicts whether a flight will arrive at least 15 minutes late.

## Links

- Repository: https://github.com/intizarhussainn14-byte/flight-delay-fullstack
- Static demo: https://intizarhussainn14-byte.github.io/flight-delay-fullstack/
- CI runs: https://github.com/intizarhussainn14-byte/flight-delay-fullstack/actions

## Deployment scope

GitHub Pages hosts only the static Angular interface. Prediction is intentionally disabled on the public site.

Live predictions require Angular and the Flask API running locally. GitHub Pages does not execute Python or the saved model.

## Dataset and research reference

Dataset: Flight Delay Dataset (2018–2022), published on Kaggle by robikscube:
https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022

This project uses `Combined_Flights_2022.csv`. The dataset preparation script:

- Excludes cancelled and diverted flights.
- Removes records with a missing target.
- Samples 25% of the remaining records within each processing chunk, using seed 42.
- Adds five engineered features.
- Exports `flights_sample.csv`.

Large datasets are excluded from Git. Obtain the source data from Kaggle and review its usage terms before redistribution.

Research reference:

AlBassam, S. A. A., & AlShahrani, S. D. N. (2025).
Flight delay prediction: Evaluating machine learning algorithms for enhanced accuracy.
PLOS ONE, 20(12), e0335141.
https://doi.org/10.1371/journal.pone.0335141

This student implementation uses its own training configuration and evaluation results. It does not reproduce the paper’s complete experimental methodology.

## Models and recorded evaluation

Decision Tree and Random Forest classifiers were trained using an 80/20 stratified split with random seed 42. Both use balanced class weights.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Decision Tree | 0.6608 | 0.3366 | 0.5849 | 0.4273 | 0.6843 |
| Random Forest | 0.6848 | 0.3602 | 0.5891 | 0.4471 | 0.7074 |

These are recorded hold-out results from `models/results.csv`.
Precision, recall, and F1 describe the delayed class.

Random Forest was selected because it had the higher F1 score on this split. The application serves this selected model, rather than combining both models.

Because model selection used the same hold-out results shown above, these scores are not an independent final evaluation of the selected model.

## Target and input schema

Target: `ArrDel15`

- `0`: arrival delay below 15 minutes.
- `1`: arrival delay of at least 15 minutes.

The model predicts a class and class probabilities; it does not predict delay duration.

The input contains 41 features: 27 numeric and 14 categorical.

Exact names, order, and feature types are recorded in:
`models/model_metadata.json`

### Numeric features

Quarter, Month, DayofMonth, DayOfWeek, CRSDepTime, CRSArrTime,
CRSElapsedTime, Distance, DistanceGroup,
Flight_Number_Marketing_Airline, Flight_Number_Operating_Airline,
DOT_ID_Marketing_Airline, DOT_ID_Operating_Airline,
OriginAirportID, OriginAirportSeqID, OriginCityMarketID,
OriginStateFips, OriginWac, DestAirportID, DestAirportSeqID,
DestCityMarketID, DestStateFips, DestWac,
DepHour, ArrHour, DayOfYear, IsWeekend.

### Categorical features

Airline, Origin, Dest, OriginState, DestState,
Marketing_Airline_Network, Operated_or_Branded_Code_Share_Partners,
DepTimeBlk, ArrTimeBlk, Operating_Airline,
IATA_Code_Marketing_Airline, IATA_Code_Operating_Airline,
Tail_Number, Route.

### Engineered features

- DepHour: `(CRSDepTime // 100) % 24`
- ArrHour: `(CRSArrTime // 100) % 24`
- DayOfYear: day number derived from FlightDate.
- IsWeekend: 1 when DayOfWeek is 6 or 7; otherwise 0.
- Route: Origin + "_" + Dest.

Feature engineering occurs in the dataset preparation script, outside the saved preprocessing pipeline. The current form supplies all 41 features explicitly. Related fields must remain consistent.

Never include the target in prediction requests.

## Saved preprocessing and model

`backend/models/model_bundle.joblib` contains:

- A fitted ColumnTransformer and Random Forest pipeline.
- An OrdinalEncoder for categorical features.
- Numeric passthrough.
- Feature names, task, class labels, and model version.

Unknown categories are encoded as -1 by the fitted encoder. Users should nevertheless supply meaningful values consistent with the training schema.

Load only trusted model artifacts. No retraining is required to run the application.

## Environment

Verified development environment:

| Component | Version |
|---|---|
| Python | 3.12.10 |
| scikit-learn | 1.9.1 |
| pandas | 3.0.6 |
| NumPy | 2.5.3 |
| SciPy | 1.18.1 |
| joblib | 1.6.0 |
| Node.js | 24.22.0 |
| npm | 11.19.1 |
| Angular | 22 |

Backend versions are pinned in `backend/requirements.txt`.
Frontend dependencies are recorded in `frontend/package-lock.json`.

## Installation on Windows

Clone and enter the repository:

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

The commands above use Command Prompt. In PowerShell, activate using:
`.\.venv\Scripts\Activate.ps1`

## Run locally

Open two terminals from the cloned project.

### Terminal 1 — Flask

```bat
.venv\Scripts\activate.bat
python backend\app.py
```

Health endpoint: http://127.0.0.1:5000/health

Keep this terminal running.

### Terminal 2 — Angular

```bat
cd frontend
npx ng serve --open --proxy-config proxy.conf.cjs
```

Open http://localhost:4200

Select Load sample, then Analyze flight. The supplied sample produces class 0 and an estimated delay probability of approximately 39.5%.

The Angular development proxy forwards `/api/predict` to Flask `/predict`.

## API

- `GET /health`: service status and model information.
- `POST /predict`: prediction from a JSON object containing all 41 features.

The API rejects malformed JSON, missing or extra fields, invalid numeric types, and empty categorical values.

Current validation does not enforce every feature’s domain range or cross-field consistency. A successful response is not proof that an arbitrary flight profile is realistic.

Example request from the project root, while Flask is running:

```bat
curl.exe --noproxy "*" -i -X POST "http://127.0.0.1:5000/predict" -H "Content-Type: application/json" --data-binary "@backend/test_payload.json"
```

## Automated tests

From the project root with the Python environment activated:

```bat
python -m pytest -q backend\tests
```

Eight tests cover:

- Health response.
- Valid prediction and expected probability.
- Missing feature.
- Invalid JSON.
- Extra feature.
- Three invalid numeric input cases.

These tests use Flask’s test client and do not require a running Flask server. They verify API behavior and a known sample, not overall predictive performance.

## Production build

```bat
cd frontend
npm run build
```

Website output:
`frontend/dist/frontend/browser`

## CI and deployment

`.github/workflows/ci.yml`:

- Installs pinned Python dependencies and checks compatibility.
- Runs the eight model-backed API tests on Linux.
- Installs frontend dependencies using npm ci.
- Builds Angular and uploads the angular-build artifact.

`.github/workflows/pages.yml`:

- Builds Angular with base href `/flight-delay-fullstack/`.
- Uploads the static browser output.
- Deploys it to GitHub Pages.

The deployment workflow runs separately from CI; it is not gated on CI success.

## Training and preparation scripts

`src/` contains dataset inspection, preparation, training, and original model-testing scripts.

Re-running training requires the source dataset under `data/` and an existing `models/` output folder.

Some development utilities also require files intentionally excluded from this repository:

- `backend/package_model.py`: original `models/flight_delay_model.pkl`.
- `backend/make_payload.py`: `data/flights_sample.csv`.
- `backend/test_pipeline.py`: original `models/flight_delay_model.pkl`.
- `src/test_model.py`: original model and sample CSV.

These files remain in the original training workspace. They are not needed to run Flask, the Angular form, or the eight backend API tests, because the packaged bundle and sample JSON are included.

## Limitations

- Research and teaching prototype, not an operational flight-status service.
- Trained using historical 2022 flight data.
- Performance on future flights may differ.
- Probabilities have not been independently calibrated.
- Cancelled and diverted flights were excluded during preparation.
- No live airline, weather, or airport feed is connected.
- Public GitHub Pages hosting provides a static interface only.
