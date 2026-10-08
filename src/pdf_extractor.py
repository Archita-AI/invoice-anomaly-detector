import pymupdf
import os




def extract_text_from_pdf(pdf_path):

    document = pymupdf.open(pdf_path)

    full_text = ""

    for page in document:
        full_text += page.get_text()

    document.close()

    return full_text



if __name__ == "__main__":

    pdf_folder = "invoices"

    pdf_files = [
        file
        for file in os.listdir(pdf_folder)
        if file.lower().endswith(".pdf")
    ]

    if len(pdf_files) == 0:

        print("No PDF invoices found.")

    else:

        pdf_path = os.path.join(
            pdf_folder,
            pdf_files[0]
        )

        print("\n================================")
        print("PDF TEXT EXTRACTION")
        print("================================")

        print(
            f"\nReading: {pdf_files[0]}"
        )

        extracted_text = extract_text_from_pdf(
            pdf_path
        )

        print("\nExtracted text:\n")

        print(extracted_text)