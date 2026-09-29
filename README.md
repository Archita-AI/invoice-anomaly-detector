# Machine Learning-Based Invoice Anomaly Detector

A machine learning project designed to identify unusual invoice transactions
for human review in small-business environments.

## Project Objective

Small businesses may process a large number of invoices, making it difficult
to manually identify unusual transactions.

This project uses machine learning and vendor-based behavioral features to
identify potentially anomalous invoices.

The system flags unusual transactions for human review. It does not
automatically classify an invoice as fraudulent.

## Current Features

- Synthetic invoice dataset generation
- Realistic anomaly generation
- Vendor-based feature engineering
- Amount deviation analysis
- Quantity deviation analysis
- Unit-price deviation analysis
- Isolation Forest anomaly detection
- Local Outlier Factor comparison
- Anomaly scoring
- Precision, recall and F1-score evaluation
- Confusion matrix
- Model comparison

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter

## Project Structure

```text
data/       → datasets and model results
src/        → Python source code
notebooks/  → experiments and analysis
models/     → trained models
app/        → future dashboard

## Phase 2 — Advanced Invoice Intelligence

Phase 2 extends the anomaly detection system with additional
invoice intelligence capabilities.

### Features Added

- Duplicate invoice detection
- Vendor profiling
- Invoice date and time-based features
- Risk scoring
- Risk-level classification
- Human-readable anomaly explanations
- Integrated ML processing pipeline

### Risk Levels

Invoices are assigned a numerical risk score and categorized as:

- Low
- Medium
- High

The risk score is intended to prioritize invoices for human review.
It does not represent a probability of fraud.