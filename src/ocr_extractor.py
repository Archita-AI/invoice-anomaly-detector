import fitz
import pytesseract

from PIL import Image


def extract_text_with_ocr(pdf_path):

    document = fitz.open(
        pdf_path
    )

    full_text = ""

    for page in document:

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image = Image.frombytes(
            "RGB",
            [
                pix.width,
                pix.height
            ],
            pix.samples
        )

        text = pytesseract.image_to_string(
            image
        )

        full_text += text

    document.close()

    return full_text


if __name__ == "__main__":

    pdf_path = (
        "invoices/scanned_invoice.pdf"
    )

    text = extract_text_with_ocr(
        pdf_path
    )

    print("\n================================")
    print("OCR RESULT")
    print("================================")

    print(text)