import os
import re
import fitz  # PyMuPDF
import pandas as pd
from pdf2image import convert_from_path
import pytesseract

# Set Tesseract and Poppler path if needed (Windows only)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# poppler_path = r"C:\path\to\poppler\bin"

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)  # , poppler_path=poppler_path
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    if len(text.strip()) < 20:
        return extract_text_with_ocr(pdf_path)
    return text

def extract_invoice_fields(text):
    data = {}

    # Define regex patterns
    patterns = {
        "Invoice Number": r"Tax Invoice[:\s]*([A-Z0-9]+)",
        "Booking ID": r"Booking Id\s*:\s*([A-Z0-9]+)",
        "GSTIN": r"GSTIN\s*:\s*([0-9A-Z]+)",
        "Invoice Date": r"Invoice date and time\s*:\s*(.+)",
        "Customer Name": r"Name\s*:\s*(.+)",
        "Billing Address": r"Billing Address\s*Address\s*:\s*(.*?)\s+GURGAON",
        "Fare": r"Fare \(Incl of All taxes\)\s*([\d.,]+)",
        "Other Charges": r"Other Service charges & Fees\s*([\d.,]+)",
        "Reversal Charges": r"Reversal of Other Service charges & Fees\s*-?([\d.,]+)",
        "CGST": r"CGST\s*@9% on \(a\):\s*([\d.,]+)",
        "SGST": r"SGST\s*@9% on \(a\):\s*([\d.,]+)",
        "IGST": r"IGST\s*@18% on \(a\):\s*([\d.,]+)",
        "Total Payable": r"Total Payable\s*([\d.,]+)",
        "Invoice Total": r"Invoice Total\s*:\s*([\d.,]+)",
        "Amount in Words": r"Invoice Total \(In Words\)\s*:\s*(.*?)\n"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        data[key] = match.group(1).strip() if match else "N/A"

    return data

def process_invoice(pdf_path):
    text = extract_text(pdf_path)
    return extract_invoice_fields(text)

def save_to_excel(data_list, output_file="invoice_output.xlsx"):
    df = pd.DataFrame(data_list)
    df.to_excel(output_file, index=False)
    print(f"[✓] Data saved to {output_file}")

if __name__ == "__main__":
    pdf_file = "Invoice.pdf"  # Use your file path
    result = process_invoice(pdf_file)
    save_to_excel([result])
