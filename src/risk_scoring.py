import pandas as pd
import numpy as np

df = pd.read_csv(
    "data/anomaly_results.csv"
)


score_min = df["anomaly_score"].min()
score_max = df["anomaly_score"].max()

df["normalized_anomaly_score"] = (
    (score_max - df["anomaly_score"])
    /
    (score_max - score_min)
)

df["risk_score"] = (
    df["normalized_anomaly_score"] * 100
)


def classify_risk(score):

    if score >= 75:
        return "High"

    elif score >= 50:
        return "Medium"

    else:
        return "Low"


df["risk_level"] = (
    df["risk_score"]
    .apply(classify_risk)
)

df["risk_score"] = (
    df["risk_score"].round(2)
)


print("\n==============================")
print("RISK SCORING")
print("==============================")

print(
    df[
        [
            "invoice_id",
            "vendor",
            "amount",
            "risk_score",
            "risk_level"
        ]
    ]
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(20)
    .to_string(index=False)
)

df.to_csv(
    "data/risk_scored_invoices.csv",
    index=False
)

print(
    "\nRisk-scored dataset saved!"
)