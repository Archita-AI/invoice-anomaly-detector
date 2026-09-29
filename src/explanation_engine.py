import pandas as pd

df = pd.read_csv(
    "data/risk_scored_invoices.csv"
)

def generate_explanation(row):

    reasons = []

    # Amount deviation
    if row["amount_deviation"] > (
        row["vendor_avg_amount"] * 1.5
    ):
        reasons.append(
            "Invoice amount is significantly "
            "higher than the vendor average."
        )

    # Quantity deviation
    if row["quantity_deviation"] > (
        row["vendor_avg_quantity"] * 1.5
    ):
        reasons.append(
            "Invoice quantity is significantly "
            "higher than the vendor average."
        )

    # Unit price deviation
    if row["unit_price_deviation"] > (
        row["vendor_avg_unit_price"] * 1.5
    ):
        reasons.append(
            "Unit price is significantly different "
            "from the vendor average."
        )

    # ML anomaly
    if row["model_result"] == "Anomaly":
        reasons.append(
            "Machine learning model identified "
            "this invoice as unusual."
        )

    # Duplicate
    if (
        "is_duplicate" in row
        and row["is_duplicate"]
    ):
        reasons.append(
            "Invoice has characteristics matching "
            "another invoice."
        )

    
    if len(reasons) == 0:
        reasons.append(
            "No major individual anomaly reason "
            "was identified."
        )

    return " ".join(reasons)



df["explanation"] = df.apply(
    generate_explanation,
    axis=1
)


print("\n==============================")
print("ANOMALY EXPLANATIONS")
print("==============================")

print(
    df[
        [
            "invoice_id",
            "vendor",
            "risk_score",
            "risk_level",
            "explanation"
        ]
    ]
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(15)
    .to_string(index=False)
)

df.to_csv(
    "data/explained_invoices.csv",
    index=False
)

print(
    "\nExplained invoice dataset saved!"
)