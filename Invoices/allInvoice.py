import os
import re
import fitz
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
from PIL import Image
from fuzzywuzzy import process

# Define field keywords that may appear differently
INVOICE_FIELDS = {
    "Invoice Number": ["invoice number", "tax invoice", "inv no"],
    "Invoice Date": ["invoice date", "date of issue", "bill date"],
    "Total Amount": ["total payable", "total", "invoice total", "amount"],
    "GSTIN": ["gstin", "gst no", "gst number"],
    "Customer Name": ["name", "billed to", "recipient"],
    "Booking ID": ["booking id", "order id", "reference no"],
}

FIELD_LABELS = list(set([item for sublist in INVOICE_FIELDS.values() for item in sublist]))

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    if len(full_text.strip()) > 20:
        return full_text
    # Fallback to OCR
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def clean_lines(raw_text):
    lines = raw_text.split("\n")
    return [line.strip() for line in lines if line.strip()]

def smart_extract(lines):
    extracted = {}
    for line in lines:
        for label in FIELD_LABELS:
            if label.lower() in line.lower():
                matched_field, score = process.extractOne(label.lower(), FIELD_LABELS)
                for key, variants in INVOICE_FIELDS.items():
                    if matched_field in variants:
                        if key not in extracted:
                            value = line.split(":")[-1].strip()
                            if not value or len(value) < 2:
                                parts = re.split(r'[\s:]', line)
                                if len(parts) > 1:
                                    value = parts[-1].strip()
                            extracted[key] = value
    return extracted

def process_all_invoices(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            try:
                raw_text = extract_text_from_pdf(pdf_path)
                lines = clean_lines(raw_text)
                extracted = smart_extract(lines)
                extracted["File Name"] = filename
                results.append(extracted)
            except Exception as e:
                print(f"Failed: {filename} → {e}")
    return results

def save_to_excel(data, filename="universal_invoice_output.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"[✓] Saved to {filename}")

if __name__ == "__main__":
    folder = "invoices"
    extracted_data = process_all_invoices(folder)
    save_to_excel(extracted_data)
