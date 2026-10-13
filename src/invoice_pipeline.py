
import os
import sys
import pandas as pd

PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FOLDER = os.path.dirname(os.path.abspath(__file__))

if SRC_FOLDER not in sys.path:
    sys.path.insert(0, SRC_FOLDER)

from pdf_extractor import extract_text_from_pdf
from invoice_parser import parse_invoice
from invoice_analyzer import analyze_invoice_record

def process_invoice(pdf_path):

    print("1. Extracting PDF text...")

    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        raise ValueError(
            "No selectable text found in this PDF. "
            "OCR may be required for scanned invoices."
        )

    print("2. Parsing invoice fields...")

    invoice = parse_invoice(text)

    print("3. Validating and analyzing invoice...")

    result = analyze_invoice_record(invoice)

    output_file = os.path.join(
        PROJECT_FOLDER,
        "data",
        "integrated_results.csv"
    )

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    pd.DataFrame([result]).to_csv(
        output_file,
        index=False
    )

    print("4. Result saved.")

    return result


if __name__ == "__main__":

    pdf_path = os.path.join(
        PROJECT_FOLDER,
        "invoices",
        "INV1001.pdf"
    )

    result = process_invoice(pdf_path)

    print("\n========== INVOICE ANALYSIS ==========")

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nSaved to data/integrated_results.csv")
