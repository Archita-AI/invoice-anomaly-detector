import subprocess

print("\n")
print("========================================")
print(" SMALL-BUSINESS INVOICE ANOMALY DETECTOR")
print(" PHASE 2 PIPELINE")
print("========================================")

def run_script(script):

    print("\n")
    print("----------------------------------------")
    print(f"Running: {script}")
    print("----------------------------------------")

    result = subprocess.run(
        ["python", script]
    )

    if result.returncode != 0:

        print(
            f"\nERROR: {script} failed."
        )

        exit(1)



run_script(
    "src/generate_data.py"
)

run_script(
    "src/advanced_features.py"
)

run_script(
    "src/anomaly_detector.py"
)

run_script(
    "src/evaluate_model.py"
)

run_script(
    "src/compare_models.py"
)


run_script(
    "src/duplicate_detector.py"
)

run_script(
    "src/vendor_profile.py"
)

run_script(
    "src/time_features.py"
)

run_script(
    "src/risk_scoring.py"
)

run_script(
    "src/explanation_engine.py"
)


print("\n")
print("========================================")
print(" PHASE 2 PIPELINE COMPLETED")
print("========================================")