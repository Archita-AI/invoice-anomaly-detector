import os
import sys
import io
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import joblib

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# Project paths
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
SRC_FOLDER = PROJECT_FOLDER / "src"
MODEL_FILE = PROJECT_FOLDER / "models" / "isolation_forest.joblib"

sys.path.insert(0, str(SRC_FOLDER))

from invoice_pipeline import process_invoice


# Load trained model
model_bundle = None

app = FastAPI(
    title="Invoice Anomaly Detector API",
    description="API for analysing invoices using Machine Learning",
    version="1.0"
)


# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Features expected by the trained model
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


def get_model():

    global model_bundle

    if model_bundle is None:

        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                "Trained model not found. Run train_model.py first."
            )

        model_bundle = joblib.load(MODEL_FILE)

    return model_bundle


def convert_to_json(value):

    if isinstance(value, dict):
        return {
            str(key): convert_to_json(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [convert_to_json(item) for item in value]

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, np.generic):
        return convert_to_json(value.item())

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, float) and not np.isfinite(value):
        return None

    if pd.isna(value):
        return None

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value


def engineer_features(df):

    df = df.copy()

    required_columns = [
        "invoice_id",
        "vendor",
        "amount",
        "quantity",
        "unit_price"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    # Convert numeric columns
    for column in ["amount", "quantity", "unit_price"]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    if df[["amount", "quantity", "unit_price"]].isna().any().any():
        raise ValueError(
            "Amount, quantity and unit_price must contain valid numbers."
        )

    if df["vendor"].isna().any():
        raise ValueError("Vendor names cannot be empty.")

    # Vendor statistics
    df["vendor_avg_amount"] = (
        df.groupby("vendor")["amount"].transform("mean")
    )

    df["vendor_std_amount"] = (
        df.groupby("vendor")["amount"].transform("std")
    )

    df["vendor_avg_quantity"] = (
        df.groupby("vendor")["quantity"].transform("mean")
    )

    df["vendor_avg_unit_price"] = (
        df.groupby("vendor")["unit_price"].transform("mean")
    )

    df["vendor_invoice_count"] = (
        df.groupby("vendor")["invoice_id"].transform("count")
    )

    # Deviations
    df["amount_deviation"] = (
        df["amount"] - df["vendor_avg_amount"]
    ).abs()

    df["quantity_deviation"] = (
        df["quantity"] - df["vendor_avg_quantity"]
    ).abs()

    df["unit_price_deviation"] = (
        df["unit_price"] - df["vendor_avg_unit_price"]
    ).abs()

    return df


@app.get("/")
def home():
    return {
        "message": "Invoice Anomaly Detector API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# PDF ANALYSIS
@app.post("/analyze")
async def analyze_invoice(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF invoice."
        )

    temp_path = None

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty."
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        result = process_invoice(temp_path)

        return {
            "success": True,
            "filename": file.filename,
            "analysis": convert_to_json(result)
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# CSV ANALYSIS
@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file."
        )

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="The uploaded CSV is empty."
            )

        # Read CSV
        df = pd.read_csv(io.BytesIO(contents))

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="The CSV contains no invoice records."
            )

        # Engineer features
        df = engineer_features(df)

        # Load trained model
        bundle = get_model()

        model = bundle["model"]
        features = bundle["features"]

        # Prepare model input
        X = df[features].apply(
            pd.to_numeric,
            errors="coerce"
        )

        # Predict anomalies
        df["prediction"] = model.predict(X)

        df["anomaly_score"] = model.decision_function(X)

        df["model_result"] = df["prediction"].apply(
            lambda x: "Anomaly" if x == -1 else "Normal"
        )

        # Summary
        total = len(df)

        anomaly_count = int(
            (df["model_result"] == "Anomaly").sum()
        )

        normal_count = int(
            (df["model_result"] == "Normal").sum()
        )

        # Convert results into JSON-safe records
        records = df.astype(object).where(
            pd.notna(df),
            None
        ).to_dict(orient="records")

        return {
            "success": True,
            "filename": file.filename,
            "summary": {
                "total_invoices": total,
                "normal_invoices": normal_count,
                "anomaly_invoices": anomaly_count
            },
            "results": convert_to_json(records)
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )