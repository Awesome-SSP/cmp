import os
import re
import fitz  # PyMuPDF
import pandas as pd
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# If needed, set the tesseract path (Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def extract_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    # If no text found (i.e., image-based PDF), use OCR
    if len(text.strip()) < 20:
        text = extract_text_with_ocr(file_path)

    invoice_number = re.search(r'Invoice Number[:\s]*([A-Za-z0-9-]+)', text, re.I)
    invoice_date = re.search(r'Date[:\s]*([0-9/.\-]+)', text, re.I)
    total_amount = re.search(r'Total[:\s$]*([\d,]+\.\d{2})', text, re.I)

    return {
        "File Name": os.path.basename(file_path),
        "Invoice Number": invoice_number.group(1) if invoice_number else "N/A",
        "Date": invoice_date.group(1) if invoice_date else "N/A",
        "Total": total_amount.group(1) if total_amount else "N/A"
    }

def process_all_invoices(folder="invoices"):
    records = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            try:
                data = extract_from_pdf(path)
                records.append(data)
                print(f"[✓] Processed: {file}")
            except Exception as e:
                print(f"[✗] Failed: {file} | Error: {e}")
    
    df = pd.DataFrame(records)
    df.to_excel("output.xlsx", index=False)
    print("[✓] Data written to output.xlsx")

if __name__ == "__main__":
    process_all_invoices()
