import pandas as pd

df = pd.read_csv("data/invoices.csv")


df["vendor_avg_amount"] = (
    df.groupby("vendor")["amount"]
    .transform("mean")
)

df["vendor_std_amount"] = (
    df.groupby("vendor")["amount"]
    .transform("std")
)

df["vendor_avg_quantity"] = (
    df.groupby("vendor")["quantity"]
    .transform("mean")
)

df["vendor_avg_unit_price"] = (
    df.groupby("vendor")["unit_price"]
    .transform("mean")
)

df["vendor_invoice_count"] = (
    df.groupby("vendor")["invoice_id"]
    .transform("count")
)



df["amount_deviation"] = (
    df["amount"] - df["vendor_avg_amount"]
).abs()

df["quantity_deviation"] = (
    df["quantity"] - df["vendor_avg_quantity"]
).abs()

df["unit_price_deviation"] = (
    df["unit_price"] - df["vendor_avg_unit_price"]
).abs()


print("\nAdvanced Features:")
print(
    df[
        [
            "invoice_id",
            "vendor",
            "amount",
            "quantity",
            "unit_price",
            "vendor_avg_amount",
            "vendor_avg_quantity",
            "vendor_avg_unit_price",
            "amount_deviation",
            "quantity_deviation",
            "unit_price_deviation",
            "vendor_invoice_count"
        ]
    ].head(10)
)

df.to_csv(
    "data/advanced_invoices.csv",
    index=False
)

print("\nAdvanced dataset saved successfully!")