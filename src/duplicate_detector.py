import pandas as pd

df = pd.read_csv("data/advanced_invoices.csv")


duplicate_columns = [
    "vendor",
    "quantity",
    "unit_price"
]

df["is_duplicate"] = df.duplicated(
    subset=duplicate_columns,
    keep=False
)

print("\n==============================")
print("DUPLICATE INVOICE DETECTION")
print("==============================")

duplicate_count = df["is_duplicate"].sum()

print(f"\nPotential duplicate invoices: {duplicate_count}")

if duplicate_count > 0:

    duplicates = df[
        df["is_duplicate"] == True
    ][
        [
            "invoice_id",
            "vendor",
            "quantity",
            "unit_price",
            "amount"
        ]
    ]

    print("\nPotential duplicates:")
    print(
        duplicates.to_string(index=False)
    )

else:
    print("\nNo duplicate invoices detected.")

df.to_csv(
    "data/invoices_with_duplicates.csv",
    index=False
)

print(
    "\nSaved to "
    "data/invoices_with_duplicates.csv"
)