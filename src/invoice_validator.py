import pandas as pd



df = pd.read_csv(
    "data/extracted_invoice.csv"
)



required_columns = [
    "invoice_id",
    "vendor",
    "invoice_date",
    "quantity",
    "unit_price",
    "amount"
]


print("\n================================")
print("INVOICE VALIDATION")
print("================================")


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print(
        "\nMissing columns:"
    )

    print(
        missing_columns
    )

else:

    print(
        "\nAll required fields are present."
    )



missing_values = (
    df[required_columns]
    .isnull()
    .sum()
)


print(
    "\nMissing values:"
)

print(
    missing_values
)


df["calculated_amount"] = (
    df["quantity"]
    * df["unit_price"]
)


df["amount_difference"] = (
    df["amount"]
    - df["calculated_amount"]
).abs()


df["amount_valid"] = (
    df["amount_difference"] <= 0.01
)


print(
    "\nAmount validation:"
)

print(
    df[
        [
            "invoice_id",
            "amount",
            "calculated_amount",
            "amount_difference",
            "amount_valid"
        ]
    ]
)



df.to_csv(
    "data/validated_invoice.csv",
    index=False
)


print(
    "\nValidated invoice saved to:"
)

print(
    "data/validated_invoice.csv"
)