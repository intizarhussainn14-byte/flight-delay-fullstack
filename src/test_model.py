import joblib
import pandas as pd

model = joblib.load("models/flight_delay_model.pkl")
sample = pd.read_csv("data/flights_sample.csv", nrows=5)
X = sample.drop(columns=["ArrDel15"])

print("Predictions:", model.predict(X))
print("Delay probabilities:", model.predict_proba(X)[:, 1].round(3))
print("Actual values:", sample["ArrDel15"].tolist())