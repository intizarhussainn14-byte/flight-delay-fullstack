import json
import joblib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix,
                             classification_report, roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier

DATA = "data/flights_sample.csv"
TARGET = "ArrDel15"
SEED = 42

df = pd.read_csv(DATA)
X = df.drop(columns=[TARGET])
y = df[TARGET]

cat_cols = X.select_dtypes(exclude="number").columns.tolist()
num_cols = X.select_dtypes(include="number").columns.tolist()
print(f"Features: {len(cat_cols) + len(num_cols)} "
      f"({len(num_cols)} numeric, {len(cat_cols)} text)")

# 80/20 split, same for both models; stratify keeps the 78/22 ratio in both parts
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y)
print(f"Train: {len(X_train):,} rows | Test: {len(X_test):,} rows")

def make_pipeline(model):
    prep = ColumnTransformer([
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value",
                               unknown_value=-1), cat_cols),
        ("num", "passthrough", num_cols),
    ])
    return Pipeline([("prep", prep), ("model", model)])

models = {
    "Decision Tree": make_pipeline(DecisionTreeClassifier(
        max_depth=12, min_samples_split=100, min_samples_leaf=50,
        class_weight="balanced", random_state=SEED)),
    "Random Forest": make_pipeline(RandomForestClassifier(
        n_estimators=100, max_depth=15, min_samples_leaf=50,
        class_weight="balanced", n_jobs=2, random_state=SEED)),
}

results, fitted, probs = [], {}, {}
for name, pipe in models.items():
    print(f"\nTraining {name} ...")
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    proba = pipe.predict_proba(X_test)[:, 1]
    fitted[name], probs[name] = pipe, proba

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred),
        "Recall": recall_score(y_test, pred),
        "F1": f1_score(y_test, pred),
        "AUC-ROC": roc_auc_score(y_test, proba),
    })
    print(f"\n=== {name} ===")
    print("Confusion matrix [[TN FP] [FN TP]]:")
    print(confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred,
          target_names=["Not delayed", "Delayed"]))

    fig, ax = plt.subplots(figsize=(4, 4))
    cm = confusion_matrix(y_test, pred)
    ax.imshow(cm, cmap="Blues")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{cm[i, j]:,}", ha="center", va="center")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["Not delayed", "Delayed"])
    ax.set_yticklabels(["Not delayed", "Delayed"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title(f"{name} - confusion matrix")
    fig.tight_layout()
    fig.savefig(f"models/confusion_{name.replace(' ', '_')}.png", dpi=120)
    plt.close(fig)

table = pd.DataFrame(results).set_index("Model").round(4)
print("\n=== COMPARISON TABLE ===")
print(table.to_string())
table.to_csv("models/results.csv")

fig, ax = plt.subplots(figsize=(5, 5))
for name, p in probs.items():
    fpr, tpr, _ = roc_curve(y_test, p)
    ax.plot(fpr, tpr, label=f"{name} (AUC={table.loc[name, 'AUC-ROC']:.3f})")
ax.plot([0, 1], [0, 1], "k--", label="Random guess")
ax.set_xlabel("False positive rate"); ax.set_ylabel("True positive rate")
ax.set_title("ROC curves"); ax.legend()
fig.tight_layout(); fig.savefig("models/roc_curves.png", dpi=120)

# Pick the better model by F1 (balances precision and recall on the delayed class)
best_name = table["F1"].idxmax()
print(f"\nBest model by F1: {best_name}")
joblib.dump(fitted[best_name], "models/flight_delay_model.pkl", compress=3)

meta = {
    "best_model": best_name,
    "target": "ArrDel15 = 1 if arrival delay >= 15 minutes, else 0",
    "features": list(X.columns),
    "categorical_features": cat_cols,
    "numeric_features": num_cols,
    "test_size": 0.2, "random_state": SEED,
    "metrics": table.loc[best_name].to_dict(),
}
with open("models/model_metadata.json", "w") as f:
    json.dump(meta, f, indent=2)
print("Saved models/flight_delay_model.pkl and model_metadata.json")