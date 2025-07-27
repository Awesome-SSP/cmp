import os
import re
import uuid
import shutil
import fitz  # PyMuPDF
import pandas as pd
from pdf2image import convert_from_path
import pytesseract

# ---------------------------
# Folder & File Configurations
# ---------------------------
INVOICE_FOLDER = r"C:\Users\GAURAV\Desktop\cmp-main\Invoices\pdfs"
PROCESSED_FOLDER = os.path.join(INVOICE_FOLDER, "processed")
OUTPUT_FILE = "invoice_output.xlsx"

os.makedirs(INVOICE_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# ---------------------------
# Helper: Move With Overwrite Safety
# ---------------------------
def safe_move(src, dst_folder):
    base = os.path.basename(src)
    name, ext = os.path.splitext(base)
    new_path = os.path.join(dst_folder, base)

    if os.path.exists(new_path):
        new_path = os.path.join(dst_folder, f"{name}_{uuid.uuid4().hex[:6]}{ext}")

    shutil.move(src, new_path)

# ---------------------------
# Text Extraction Logic
# ---------------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    if len(text.strip()) > 20:
        return text

    # Fallback to OCR
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# ---------------------------
# Format Detection
# ---------------------------
def detect_invoice_format(text):
    if "LE TRAVENUES TECHNOLOGY LIMITED" in text:
        return "le_travenues"
    elif "MAKEMYTRIP (INDIA) PRIVATE LIMITED" in text:
        return "makemytrip"
    else:
        return "unknown"

# ---------------------------
# Extraction Functions
# ---------------------------
def extract_field(text, label, group=1, default="N/A", clean=True):
    match = re.search(label, text, re.IGNORECASE | re.DOTALL)
    if not match:
        return default
    val = match.group(group).strip()
    if clean:
        val = val.replace("■", "").replace("₹", "").strip()
    return val

def extract_le_travenues(text, file_name):
    return {
        "File Name": file_name,
        "Invoice Number": extract_field(text, r'Tax Invoice[:\s]*([A-Z0-9]+)'),
        "Invoice Date": extract_field(text, r'Invoice date and time\s*:\s*(.+)', group=1).split("IST")[0].strip(),
        "Customer Name": extract_field(text, r'Name\s*:\s*(.+)'),
        "Total Payable": extract_field(text, r'Total Payable\s*([\d.,]+)'),
    }

def extract_makemytrip(text, file_name):
    return {
        "File Name": file_name,
        "Invoice Number": extract_field(text, r'Invoice No\.\s*([A-Z0-9]+)'),
        "Invoice Date": extract_field(text, r'Date\s*([0-9A-Za-z ]+)'),
        "Customer Name": extract_field(text, r'Customer Name\s*([A-Za-z ]+)'),
        "Total Payable": extract_field(text, r'Grand Total\s*₹([\d.,]+)'),
    }

def extract_generic(text, file_name):
    def find_by_label(label, lines, fallback="N/A", max_chars=100):
        for i, line in enumerate(lines):
            if label.lower() in line.lower():
                after_colon = line.split(":")[-1].strip()
                if after_colon:
                    return after_colon
                elif i + 1 < len(lines):
                    return lines[i + 1][:max_chars].strip()
        return fallback

    def find_first_match(pattern, default="N/A"):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else default

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "File Name": file_name,
        "Company": find_by_label("company", lines, fallback="Unknown"),
        "Invoice Number": find_by_label("invoice", lines),
        "Booking ID": find_by_label("booking", lines),
        "Invoice Date": find_first_match(r'(?:Invoice Date|Date)\s*[:\-]?\s*(.+?)(?:\s+|$)'),
        "GSTIN": find_first_match(r'GSTIN\s*[:\-]?\s*([0-9A-Z]{15})'),
        "Customer Name": find_by_label("customer", lines),
        "Fare": find_first_match(r'(Fare|Base Fare)[^\d]*([\d.,]+)', default="N/A"),
        "Other Charges": find_by_label("charges", lines),
        "CGST": find_first_match(r'CGST[^\d]*([\d.,]+)'),
        "SGST": find_first_match(r'SGST[^\d]*([\d.,]+)'),
        "IGST": find_first_match(r'IGST[^\d]*([\d.,]+)'),
        "Total Payable": find_first_match(r'(Total Payable|Grand Total)[^\d]*([\d.,]+)', default="N/A"),
        "Amount in Words": find_by_label("in words", lines, fallback="N/A")
    }

# ---------------------------
# Wrapper
# ---------------------------
def extract_invoice_data(text, file_name):
    fmt = detect_invoice_format(text)
    if fmt == "le_travenues":
        return extract_le_travenues(text, file_name)
    elif fmt == "makemytrip":
        return extract_makemytrip(text, file_name)
    else:
        return extract_generic(text, file_name)

# ---------------------------
# Main Processing Logic
# ---------------------------
def process_all_invoices(folder_path, processed_path):
    extracted_data = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, file)
            print(f"[→] Processing: {file}")
            try:
                text = extract_text_from_pdf(full_path)
                record = extract_invoice_data(text, file)
                extracted_data.append(record)

                # Move file
                safe_move(full_path, processed_path)
                print(f"[✓] Moved: {file}")
            except Exception as e:
                print(f"[✗] Error on {file}: {e}")
    return extracted_data

# ---------------------------
# Excel Output
# ---------------------------
def save_to_excel(data, filename=OUTPUT_FILE):
    if os.path.exists(filename):
        existing = pd.read_excel(filename)
        combined = pd.concat([existing, pd.DataFrame(data)], ignore_index=True)
    else:
        combined = pd.DataFrame(data)
    combined.to_excel(filename, index=False)
    print(f"[📄] Saved to {filename}")

# ---------------------------
# Main Run
# ---------------------------
if __name__ == "__main__":
    extracted = process_all_invoices(INVOICE_FOLDER, PROCESSED_FOLDER)
    if extracted:
        save_to_excel(extracted)
    else:
        print("[⚠️] No new invoices found.")
