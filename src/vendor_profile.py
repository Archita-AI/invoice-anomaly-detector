import pandas as pd

df = pd.read_csv(
    "data/invoices_with_duplicates.csv"
)

vendor_profile = (
    df.groupby("vendor")
    .agg(
        invoice_count=("invoice_id", "count"),
        average_amount=("amount", "mean"),
        median_amount=("amount", "median"),
        minimum_amount=("amount", "min"),
        maximum_amount=("amount", "max"),
        average_quantity=("quantity", "mean"),
        average_unit_price=("unit_price", "mean")
    )
    .reset_index()
)

numeric_columns = [
    "average_amount",
    "median_amount",
    "minimum_amount",
    "maximum_amount",
    "average_quantity",
    "average_unit_price"
]

vendor_profile[numeric_columns] = (
    vendor_profile[numeric_columns].round(2)
)

print("\n==============================")
print("VENDOR PROFILES")
print("==============================")

print(
    vendor_profile.to_string(index=False)
)

vendor_profile.to_csv(
    "data/vendor_profiles.csv",
    index=False
)

print(
    "\nVendor profiles saved to "
    "data/vendor_profiles.csv"
)