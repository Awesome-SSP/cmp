import os
import fitz  # PyMuPDF
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import re
from PIL import Image

# === Config ===
PDF_FOLDER = r"C:\Users\GAURAV\Desktop\cmp-main\Invoices\pdfs"
OUTPUT_CSV = "output.csv"
TESSERACT_CMD = "/usr/local/bin/tesseract"  # adjust for your system
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# === Helper Functions ===

def extract_text_fitz(pdf_path):
    """Try extracting text using PyMuPDF (structured)"""
    try:
        text = ""
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"[fitz error]: {e}")
        return ""

def extract_text_ocr(pdf_path):
    """Fallback OCR using pdf2image + Tesseract"""
    try:
        images = convert_from_path(pdf_path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"[OCR error]: {e}")
        return ""

def extract_field(patterns, text, fallback="N/A"):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return fallback

def extract_invoice_data(file_path):
    file_name = os.path.basename(file_path)
    
    text = extract_text_fitz(file_path)
    if len(text.strip()) < 100:
        print(f"[Fallback OCR] for {file_name}")
        text = extract_text_ocr(file_path)

    # === Extraction Patterns ===
    invoice_number = extract_field([r"Invoice\s*Number[:\-]?\s*([A-Z0-9\-\/]+)"], text)
    invoice_date = extract_field([r"Invoice\s*Date[:\-]?\s*([A-Za-z0-9,\/\-\s]+)"], text)
    gstin = extract_field([r"GSTIN[:\-]?\s*([0-9A-Z]+)"], text)
    hsn_sac = extract_field([r"HSN/?SAC[:\-]?\s*([0-9]+)"], text)
    service_description = extract_field([r"Description\s*[:\-]?\s*(.+?)\n"], text)
    fare = extract_field([r"(?:Fare|Amount|Total Fare)[\s:]*₹?([\d,]+\.\d{2})"], text)
    service_fees = extract_field([r"Service\s*Fee[s]?\s*[:\-]?\s*₹?([\d,]+\.\d{2})"], text)
    cgst = extract_field([r"CGST\s*\(?[%]?\)?\s*[:\-]?\s*([0-9.]+)"], text)
    sgst = extract_field([r"SGST\s*\(?[%]?\)?\s*[:\-]?\s*([0-9.]+)"], text)
    igst = extract_field([r"IGST\s*\(?[%]?\)?\s*[:\-]?\s*([0-9.]+)"], text)
    total_amount = extract_field([r"(?:Total\s*Amount|Total\s*Payable)[:\-]?\s*₹?([\d,]+\.\d{2})"], text)
    payment_mode = extract_field([r"Payment\s*Mode[:\-]?\s*([\w\s]+)"], text)
    customer_name = extract_field([r"Customer\s*Name[:\-]?\s*([A-Za-z\s]+)"], text)

    return {
        "File Name": file_name,
        "Customer Name": customer_name,
        "Invoice Number": invoice_number,
        "Invoice Date": invoice_date,
        "GSTIN": gstin,
        "HSN/SAC": hsn_sac,
        "Service Description": service_description,
        "Fare / Item Charges": fare,
        "Service Fees": service_fees,
        "CGST": cgst,
        "SGST": sgst,
        "IGST": igst,
        "Total Amount": total_amount,
        "Payment Mode": payment_mode
    }

# === Main Pipeline ===

def process_all_pdfs(pdf_dir):
    results = []
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(pdf_dir, filename)
            print(f"Processing: {filename}")
            data = extract_invoice_data(path)
            results.append(data)
    return results

if __name__ == "__main__":
    data = process_all_pdfs(PDF_FOLDER)
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Extracted data saved to: {OUTPUT_CSV}")