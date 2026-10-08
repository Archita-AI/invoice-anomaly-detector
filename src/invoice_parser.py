import re
import pandas as pd
import pymupdf


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def parse_invoice(text):

    invoice_data = {}

    # Invoice Number
    match = re.search(
        r"Invoice Number:\s*(\S+)",
        text,
        re.IGNORECASE
    )

    invoice_data["invoice_id"] = (
        match.group(1) if match else None
    )

    # Vendor
    match = re.search(
        r"Vendor:\s*(.+)",
        text,
        re.IGNORECASE
    )

    invoice_data["vendor"] = (
        match.group(1).strip() if match else None
    )

    # Date
    match = re.search(
        r"Date:\s*(\S+)",
        text,
        re.IGNORECASE
    )

    invoice_data["invoice_date"] = (
        match.group(1) if match else None
    )

    # Quantity
    match = re.search(
        r"Quantity:\s*(\d+)",
        text,
        re.IGNORECASE
    )

    invoice_data["quantity"] = (
        int(match.group(1)) if match else None
    )

    # Unit Price
    match = re.search(
        r"Unit Price:\s*₹?\s*([\d,.]+)",
        text,
        re.IGNORECASE
    )

    invoice_data["unit_price"] = (
        float(match.group(1).replace(",", ""))
        if match else None
    )

    # Total Amount
    match = re.search(
        r"Total Amount:\s*₹?\s*([\d,.]+)",
        text,
        re.IGNORECASE
    )

    invoice_data["amount"] = (
        float(match.group(1).replace(",", ""))
        if match else None
    )

    return invoice_data


if __name__ == "__main__":

    print("Starting invoice parser...")

    pdf_path = "invoices/INV1001.pdf"

    print("Opening PDF...")

    text = extract_text_from_pdf(pdf_path)

    print("PDF text extracted.")

    invoice = parse_invoice(text)

    print("Invoice parsed.")

    print("\n================================")
    print("PARSED INVOICE")
    print("================================")

    for key, value in invoice.items():
        print(f"{key}: {value}")

    df = pd.DataFrame([invoice])

    df.to_csv(
        "data/extracted_invoice.csv",
        index=False
    )

    print("\nInvoice data saved successfully!")

    print("File:")
    print("data/extracted_invoice.csv")