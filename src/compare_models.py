import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score
)

df = pd.read_csv("data/advanced_invoices.csv")

features = [
    "amount",
    "quantity",
    "unit_price",
    "vendor_avg_amount",
    "vendor_std_amount",
    "vendor_avg_quantity",
    "vendor_avg_unit_price",
    "vendor_invoice_count",
    "amount_deviation",
    "quantity_deviation",
    "unit_price_deviation"
]

X = df[features]

y_true = df["actual_anomaly"]



isolation_model = IsolationForest(
    contamination=0.02,
    random_state=42
)

isolation_prediction = isolation_model.fit_predict(X)

isolation_prediction = (
    isolation_prediction == -1
).astype(int)

if_precision = precision_score(
    y_true,
    isolation_prediction,
    zero_division=0
)

if_recall = recall_score(
    y_true,
    isolation_prediction,
    zero_division=0
)

if_f1 = f1_score(
    y_true,
    isolation_prediction,
    zero_division=0
)


lof_model = LocalOutlierFactor(
    n_neighbors=20,
    contamination=0.02
)

lof_prediction = lof_model.fit_predict(X)

lof_prediction = (
    lof_prediction == -1
).astype(int)

lof_precision = precision_score(
    y_true,
    lof_prediction,
    zero_division=0
)

lof_recall = recall_score(
    y_true,
    lof_prediction,
    zero_division=0
)

lof_f1 = f1_score(
    y_true,
    lof_prediction,
    zero_division=0
)



results = pd.DataFrame({
    "Model": [
        "Isolation Forest",
        "Local Outlier Factor"
    ],
    "Precision": [
        if_precision,
        lof_precision
    ],
    "Recall": [
        if_recall,
        lof_recall
    ],
    "F1 Score": [
        if_f1,
        lof_f1
    ]
})

print("\n==============================")
print("MODEL COMPARISON")
print("==============================")

print(
    results.to_string(index=False)
)

results.to_csv(
    "data/model_comparison.csv",
    index=False
)

print("\nModel comparison saved to:")
print("data/model_comparison.csv")