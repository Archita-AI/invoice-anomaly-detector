import pandas as pd


anomaly_df = pd.read_csv(
    "data/anomaly_results.csv"
)

duplicate_df = pd.read_csv(
    "data/invoices_with_duplicates.csv"
)

time_df = pd.read_csv(
    "data/time_features.csv"
)

risk_df = pd.read_csv(
    "data/risk_scored_invoices.csv"
)

explanation_df = pd.read_csv(
    "data/explained_invoices.csv"
)



final_df = anomaly_df.copy()



if "is_duplicate" in duplicate_df.columns:

    final_df = final_df.merge(
        duplicate_df[
            [
                "invoice_id",
                "is_duplicate"
            ]
        ],
        on="invoice_id",
        how="left"
    )

else:

    final_df["is_duplicate"] = False



time_columns = [
    "invoice_id",
    "invoice_date",
    "invoice_month",
    "invoice_day",
    "invoice_day_of_week",
    "invoice_week",
    "is_weekend"
]

available_time_columns = [
    column
    for column in time_columns
    if column in time_df.columns
]

final_df = final_df.merge(
    time_df[available_time_columns],
    on="invoice_id",
    how="left"
)


risk_columns = [
    "invoice_id",
    "normalized_anomaly_score",
    "risk_score",
    "risk_level"
]

available_risk_columns = [
    column
    for column in risk_columns
    if column in risk_df.columns
]

final_df = final_df.merge(
    risk_df[available_risk_columns],
    on="invoice_id",
    how="left"
)



if "explanation" in explanation_df.columns:

    final_df = final_df.merge(
        explanation_df[
            [
                "invoice_id",
                "explanation"
            ]
        ],
        on="invoice_id",
        how="left"
    )


final_df = final_df.loc[
    :,
    ~final_df.columns.duplicated()
]

final_df["is_duplicate"] = (
    final_df["is_duplicate"]
    .fillna(False)
    .astype(bool)
)

final_df.to_csv(
    "data/final_invoices.csv",
    index=False
)


print("\n========================================")
print("FINAL INVOICE DATASET")
print("========================================")

print(
    f"\nTotal invoices: {len(final_df)}"
)

print(
    f"Total columns: {len(final_df.columns)}"
)

print("\nColumns:")

for column in final_df.columns:
    print(f"- {column}")


print("\nFirst 5 invoices:")

print(
    final_df.head().to_string(index=False)
)


print(
    "\nFinal dataset saved to:"
)

print(
    "data/final_invoices.csv"
)