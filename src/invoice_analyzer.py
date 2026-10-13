
import os
import joblib
import pandas as pd


PROJECT_FOLDER = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_FILE = os.path.join(
    PROJECT_FOLDER, "data", "invoices.csv"
)

MODEL_FILE = os.path.join(
    PROJECT_FOLDER, "models", "isolation_forest.joblib"
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


def analyze_invoice_record(invoice):

    history = pd.read_csv(DATA_FILE)

    required = [
        "invoice_id",
        "vendor",
        "invoice_date",
        "quantity",
        "unit_price",
        "amount"
    ]

    for field in required:
        if pd.isna(invoice.get(field)):
            raise ValueError(
                f"Missing required field: {field}"
            )

    quantity = int(invoice["quantity"])
    unit_price = float(invoice["unit_price"])
    amount = float(invoice["amount"])

    if quantity <= 0 or unit_price < 0 or amount < 0:
        raise ValueError(
            "Quantity must be positive; price and amount "
            "cannot be negative."
        )

    calculated_amount = quantity * unit_price

    if abs(amount - calculated_amount) > 0.01:
        raise ValueError(
            "Invoice total does not match quantity × unit price."
        )

    # Find this vendor's historical transactions.
    vendor_history = history[
        history["vendor"].astype(str).str.casefold()
        == str(invoice["vendor"]).casefold()
    ]

    # If the vendor is new, use the overall reference data.
    reference = (
        vendor_history
        if not vendor_history.empty
        else history
    )

    avg_amount = float(reference["amount"].mean())
    std_amount = float(reference["amount"].std())
    avg_quantity = float(reference["quantity"].mean())
    avg_price = float(reference["unit_price"].mean())

    if pd.isna(std_amount):
        std_amount = 0.0

    new_row = {
        "amount": amount,
        "quantity": quantity,
        "unit_price": unit_price,
        "vendor_avg_amount": avg_amount,
        "vendor_std_amount": std_amount,
        "vendor_avg_quantity": avg_quantity,
        "vendor_avg_unit_price": avg_price,
        "vendor_invoice_count": len(vendor_history),
        "amount_deviation": abs(amount - avg_amount),
        "quantity_deviation": abs(quantity - avg_quantity),
        "unit_price_deviation": abs(unit_price - avg_price)
    }

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            "Saved model missing. Run "
            "'python src/train_model.py' first."
        )

    bundle = joblib.load(MODEL_FILE)
    model = bundle["model"]
    features = bundle["features"]

    X_new = pd.DataFrame(
        [new_row], columns=features
    ).apply(pd.to_numeric, errors="coerce")

    prediction = int(model.predict(X_new)[0])
    anomaly_score = float(model.decision_function(X_new)[0])

    # Relative risk ranking against the training score distribution.
    training = pd.read_csv(
        os.path.join(
            PROJECT_FOLDER,
            "data",
            "advanced_invoices.csv"
        )
    )

    X_train = training[features].apply(
        pd.to_numeric, errors="coerce"
    )

    transformed_training = model.named_steps[
        "imputer"
    ].transform(X_train)

    training_scores = model.named_steps[
        "isolation_forest"
    ].decision_function(transformed_training)

    score_min = float(training_scores.min())
    score_max = float(training_scores.max())

    if score_max > score_min:
        risk_score = (
            (score_max - anomaly_score)
            / (score_max - score_min)
        ) * 100
    else:
        risk_score = 0.0

    risk_score = round(
        max(0.0, min(100.0, risk_score)), 2
    )

    if prediction == -1 or risk_score >= 75:
        risk_level = "High"
    elif risk_score >= 50:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Check for a matching historical transaction.
    duplicate = (
        (
            history["vendor"].astype(str).str.casefold()
            == str(invoice["vendor"]).casefold()
        )
        & (history["quantity"] == quantity)
        & (
            (history["unit_price"] - unit_price).abs()
            <= 0.01
        )
    ).any()

    reasons = []

    if abs(amount - avg_amount) > max(avg_amount * 0.5, 1):
        reasons.append(
            "Invoice amount differs substantially from the reference average."
        )

    if abs(quantity - avg_quantity) > max(avg_quantity * 0.5, 1):
        reasons.append(
            "Invoice quantity differs substantially from the reference average."
        )

    if abs(unit_price - avg_price) > max(avg_price * 0.5, 1):
        reasons.append(
            "Unit price differs substantially from the reference average."
        )

    if prediction == -1:
        reasons.append(
            "The Isolation Forest model identified an unusual pattern."
        )

    if duplicate:
        reasons.append(
            "A similar vendor, quantity and unit price appear in historical data."
        )

    if vendor_history.empty:
        reasons.append(
            "This vendor has no history; overall historical averages were used."
        )

    if not reasons:
        reasons.append(
            "No major unusual pattern was identified by the configured checks."
        )

    return {
        **invoice,
        "anomaly_prediction": (
            "Anomaly" if prediction == -1 else "Normal"
        ),
        "anomaly_score": round(anomaly_score, 6),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "is_duplicate": bool(duplicate),
        "explanation": " ".join(reasons)
    }
