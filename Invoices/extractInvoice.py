import os
import re
import fitz  # PyMuPDF
import pandas as pd
from pdf2image import convert_from_path
import pytesseract

# Optional (for Windows): set Tesseract/Poppler path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# poppler_path = r"C:\path\to\poppler\bin"

INVOICE_FOLDER = "invoices"
OUTPUT_FILE = "invoice_output.xlsx"

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

def extract_invoice_fields(text, file_name):
    data = {"File Name": file_name}

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

def process_all_invoices(folder_path):
    results = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            try:
                print(f"[✓] Processing {file}...")
                text = extract_text(file_path)
                record = extract_invoice_fields(text, file)
                results.append(record)
            except Exception as e:
                print(f"[✗] Failed to process {file} → {e}")

    return results

def save_to_excel(data, filename=OUTPUT_FILE):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"[✔] Extracted data saved to: {filename}")

if __name__ == "__main__":
    all_invoice_data = process_all_invoices(INVOICE_FOLDER)
    save_to_excel(all_invoice_data)
