import pandas as pd

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

df = pd.read_csv("data/anomaly_results.csv")

df["predicted_anomaly"] = (
    df["model_result"] == "Anomaly"
).astype(int)

y_true = df["actual_anomaly"]

y_pred = df["predicted_anomaly"]


cm = confusion_matrix(
    y_true,
    y_pred
)

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")

print(cm)

precision = precision_score(
    y_true,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    zero_division=0
)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"Precision: {precision:.3f}")
print(f"Recall:    {recall:.3f}")
print(f"F1 Score:  {f1:.3f}")

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")

print(
    classification_report(
        y_true,
        y_pred,
        zero_division=0
    )
)