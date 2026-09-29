import pandas as pd

df = pd.read_csv(
    "data/advanced_invoices.csv"
)

df["invoice_date"] = pd.to_datetime(
    df["invoice_date"]
)


df["invoice_month"] = (
    df["invoice_date"].dt.month
)

df["invoice_day"] = (
    df["invoice_date"].dt.day
)

df["invoice_day_of_week"] = (
    df["invoice_date"].dt.dayofweek
)

df["invoice_week"] = (
    df["invoice_date"].dt.isocalendar().week
)

df["is_weekend"] = (
    df["invoice_day_of_week"] >= 5
).astype(int)


print("\n==============================")
print("TIME FEATURES")
print("==============================")

print(
    df[
        [
            "invoice_id",
            "invoice_date",
            "invoice_month",
            "invoice_day_of_week",
            "is_weekend"
        ]
    ].head(10)
)

df.to_csv(
    "data/time_features.csv",
    index=False
)

print(
    "\nTime-feature dataset saved!"
)