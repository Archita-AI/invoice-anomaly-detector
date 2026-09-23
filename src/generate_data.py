import pandas as pd
import numpy as np

np.random.seed(42)

n = 1000

vendors = [
    "ABC Supplies",
    "XYZ Traders",
    "Global Office",
    "Tech World",
    "Prime Stationery"
]

categories = [
    "Stationery",
    "Electronics",
    "Office Equipment",
    "Software",
    "Furniture"
]

data = {
    "invoice_id": [f"INV{i:04d}" for i in range(1, n + 1)],
    "vendor": np.random.choice(vendors, n),
    "category": np.random.choice(categories, n),
    "quantity": np.random.randint(1, 30, n),
    "unit_price": np.random.uniform(200, 5000, n)
}

df = pd.DataFrame(data)

df["amount"] = (
    df["quantity"] * df["unit_price"]
).round(2)

df["actual_anomaly"] = 0



anomaly_indices = np.random.choice(
    df.index,
    20,
    replace=False
)

amount_anomalies = anomaly_indices[:7]
quantity_anomalies = anomaly_indices[7:14]
combined_anomalies = anomaly_indices[14:20]


df.loc[amount_anomalies, "unit_price"] *= np.random.uniform(
    5,
    10,
    len(amount_anomalies)
)



df.loc[quantity_anomalies, "quantity"] *= np.random.randint(
    5,
    10,
    len(quantity_anomalies)
)



df.loc[combined_anomalies, "quantity"] *= np.random.randint(
    3,
    7,
    len(combined_anomalies)
)

df.loc[combined_anomalies, "unit_price"] *= np.random.uniform(
    3,
    6,
    len(combined_anomalies)
)

df.loc[anomaly_indices, "actual_anomaly"] = 1

df["amount"] = (
    df["quantity"] * df["unit_price"]
).round(2)

df["unit_price"] = df["unit_price"].round(2)

df.to_csv(
    "data/invoices.csv",
    index=False
)



print("Dataset created successfully!")

print(f"Total invoices: {len(df)}")

print(
    f"Artificial anomalies: "
    f"{df['actual_anomaly'].sum()}"
)

print("\nAnomaly types:")

print(
    f"High unit price: "
    f"{len(amount_anomalies)}"
)

print(
    f"High quantity: "
    f"{len(quantity_anomalies)}"
)

print(
    f"High quantity + high unit price: "
    f"{len(combined_anomalies)}"
)

print("\nChecking amount calculation:")

calculation_check = np.isclose(
    df["amount"],
    df["quantity"] * df["unit_price"],
    atol=0.01
)

print(
    "All amounts consistent:",
    calculation_check.all()
)

print("\nFirst 5 invoices:")
print(df.head())