import pandas as pd
from sklearn.ensemble import IsolationForest

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

model = IsolationForest(
    contamination=0.02,
    random_state=42
)

model.fit(X)

df["prediction"] = model.predict(X)

df["anomaly_score"] = model.decision_function(X)

df["model_result"] = df["prediction"].apply(
    lambda x: "Anomaly" if x == -1 else "Normal"
)


print("\n==============================")
print("MODEL RESULTS")
print("==============================")

print(
    df["model_result"].value_counts()
)

print("\nActual anomalies:")
print(df["actual_anomaly"].sum())

print("\nModel detected:")
print(
    (df["model_result"] == "Anomaly").sum()
)

correctly_detected = (
    (df["actual_anomaly"] == 1) &
    (df["model_result"] == "Anomaly")
).sum()

print("\nActual anomalies correctly detected:")
print(correctly_detected)


print("\n==============================")
print("MOST SUSPICIOUS INVOICES")
print("==============================")

suspicious = (
    df[
        [
            "invoice_id",
            "vendor",
            "amount",
            "vendor_avg_amount",
            "amount_deviation",
            "anomaly_score",
            "model_result"
        ]
    ]
    .sort_values("anomaly_score")
    .head(10)
)

print(suspicious.to_string(index=False))

df.to_csv(
    "data/anomaly_results.csv",
    index=False
)

print("\nResults saved to data/anomaly_results.csv")