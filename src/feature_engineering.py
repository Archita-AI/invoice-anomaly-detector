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

df["amount_deviation"] = (
    df["amount"] - df["vendor_avg_amount"]
).abs()

df["vendor_avg_quantity"] = (
    df.groupby("vendor")["quantity"]
    .transform("mean")
)

df["quantity_deviation"] = (
    df["quantity"] - df["vendor_avg_quantity"]
).abs()




df["vendor_avg_unit_price"] = (
    df.groupby("vendor")["unit_price"]
    .transform("mean")
)

df["unit_price_deviation"] = (
    df["unit_price"] -  df["vendor_avg_unit_price"]
).abs()

df["vendor_invoice_count"] = (
    df.groupby("vendor")["invoice_id"]
    .transform("count")
)




print("\nEnhanced Features:")

print(
    df[
        [
            "invoice_id",
            "vendor",
            "amount",
            "vendor_avg_amount",
            "amount_deviation",
            "quantity",
            "vendor_avg_quantity",
            "quantity_deviation",
            "unit_price",
            "vendor_avg_unit_price",
            "unit_price_deviation",
            "vendor_invoice_count"
        ]
    ].head(10)
)


df.to_csv(
    "data/enhanced_invoices.csv",
    index=False
)

print("\nEnhanced dataset saved successfully!")