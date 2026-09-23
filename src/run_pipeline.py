import subprocess

print("\n==============================")
print("INVOICE ANOMALY DETECTOR")
print("FULL ML PIPELINE")
print("==============================")

print("\n1. Generating invoice data...")
subprocess.run(
    ["python", "src/generate_data.py"]
)

print("\n2. Creating advanced features...")
subprocess.run(
    ["python", "src/advanced_features.py"]
)

print("\n3. Running anomaly detection...")
subprocess.run(
    ["python", "src/anomaly_detector.py"]
)

print("\n4. Evaluating model...")
subprocess.run(
    ["python", "src/evaluate_model.py"]
)

print("\n5. Comparing models...")
subprocess.run(
    ["python", "src/compare_models.py"]
)

print("\n==============================")
print("PIPELINE COMPLETED")
print("==============================")