
import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


PROJECT_FOLDER = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_FILE = os.path.join(
    PROJECT_FOLDER,
    "data",
    "advanced_invoices.csv"
)

MODEL_FOLDER = os.path.join(
    PROJECT_FOLDER,
    "models"
)

MODEL_FILE = os.path.join(
    MODEL_FOLDER,
    "isolation_forest.joblib"
)

FEATURES = [
    "amount",
    "quantity",
    "unit_price",
    "vendor_avg_amount",
    "vendor_std_amount",
    "vendor_avg_quantity",
    "vendor_avg_unit_price",
    "vendor_invoice_count",
    "amount_deviation",
    "quantity_deviation",
    "unit_price_deviation"
]


def train_model():

    print("Loading historical invoice data...")

    df = pd.read_csv(DATA_FILE)

    missing_features = [
        column for column in FEATURES
        if column not in df.columns
    ]

    if missing_features:
        raise ValueError(
            "Missing required features: "
            + ", ".join(missing_features)
        )

    X = df[FEATURES].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Remove rows where every feature is missing.
    X = X.dropna(how="all")

    if len(X) < 2:
        raise ValueError(
            "At least two usable historical invoices are required."
        )

    model = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "isolation_forest",
            IsolationForest(
                contamination=0.02,
                random_state=42
            )
        )
    ])

    print("Training Isolation Forest...")

    model.fit(X)

    os.makedirs(
        MODEL_FOLDER,
        exist_ok=True
    )

    model_bundle = {
        "model": model,
        "features": FEATURES
    }

    joblib.dump(
        model_bundle,
        MODEL_FILE
    )

    print("\nModel trained successfully!")
    print(f"Training invoices: {len(X)}")
    print(f"Features used: {len(FEATURES)}")
    print(f"Saved model to: {MODEL_FILE}")


if __name__ == "__main__":
    train_model()
