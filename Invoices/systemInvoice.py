import os
import re
import shutil
import fitz  # PyMuPDF
import pandas as pd
from pdf2image import convert_from_path
import pytesseract

INVOICE_FOLDER = r"C:\Users\GAURAV\Desktop\cmp-main\Invoices\pdfs"
PROCESSED_FOLDER = "processed"
OUTPUT_FILE = "invoice_output.xlsx"

os.makedirs(INVOICE_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# ---------------------
# Text Extraction Logic
# ---------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    if len(text.strip()) > 20:
        return text
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def detect_invoice_format(text):
    if "LE TRAVENUES TECHNOLOGY LIMITED" in text:
        return "le_travenues"
    elif "MAKEMYTRIP (INDIA) PRIVATE LIMITED" in text:
        return "makemytrip"
    else:
        return "unknown"

def extract_field(text, label, group=1, default="N/A", clean=True):
    match = re.search(label, text, re.IGNORECASE | re.DOTALL)
    if not match:
        return default
    val = match.group(group).strip()
    if clean:
        val = val.replace("■", "").replace("₹", "").strip()
    return val

# --------------------------
# Format-Specific Extractors
# --------------------------
def extract_le_travenues(text, file_name):
    return {
        "File Name": file_name,
        "Company": "LE TRAVENUES",
        "Invoice Number": re.search(r'Tax Invoice[:\s]*([A-Z0-9]+)', text).group(1) if re.search(r'Tax Invoice[:\s]*([A-Z0-9]+)', text) else "N/A",
        "Booking ID": re.search(r'Booking Id\s*:\s*([A-Z0-9]+)', text).group(1) if re.search(r'Booking Id\s*:\s*([A-Z0-9]+)', text) else "N/A",
        "Invoice Date": re.search(r'Invoice date and time\s*:\s*(.+)', text).group(1).split("IST")[0].strip() if re.search(r'Invoice date and time\s*:\s*(.+)', text) else "N/A",
        "GSTIN": re.search(r'GSTIN\s*:\s*([0-9A-Z]+)', text).group(1) if re.search(r'GSTIN\s*:\s*([0-9A-Z]+)', text) else "N/A",
        "Customer Name": re.search(r'Name\s*:\s*(.+)', text).group(1).strip() if re.search(r'Name\s*:\s*(.+)', text) else "N/A",
        "Fare": re.search(r'Fare \(Incl of All taxes\)\s*([\d.,]+)', text).group(1) if re.search(r'Fare \(Incl of All taxes\)\s*([\d.,]+)', text) else "N/A",
        "Service Charges": re.search(r'Other Service charges & Fees\s*([\d.,]+)', text).group(1) if re.search(r'Other Service charges & Fees\s*([\d.,]+)', text) else "N/A",
        "CGST": re.search(r'CGST.*?([\d.,]+)', text).group(1) if re.search(r'CGST.*?([\d.,]+)', text) else "N/A",
        "SGST": re.search(r'SGST.*?([\d.,]+)', text).group(1) if re.search(r'SGST.*?([\d.,]+)', text) else "N/A",
        "IGST": re.search(r'IGST.*?([\d.,]+)', text).group(1) if re.search(r'IGST.*?([\d.,]+)', text) else "N/A",
        "Total Payable": re.search(r'Total Payable\s*([\d.,]+)', text).group(1) if re.search(r'Total Payable\s*([\d.,]+)', text) else "N/A"
    }

def extract_makemytrip(text, file_name):
    return {
        "File Name": file_name,
        "Company": "MakeMyTrip",
        "Invoice Number": extract_field(text, r'Invoice No\.\s*([A-Z0-9]+)'),
        "Booking ID": extract_field(text, r'Booking ID\s*([A-Z0-9]+)'),
        "Invoice Date": extract_field(text, r'Date\s*([0-9A-Za-z ]+)'),
        "GSTIN": extract_field(text, r'GSTIN\s*([0-9A-Z]+)'),
        "Customer Name": extract_field(text, r'Customer Name\s*([A-Za-z ]+)'),
        "Fare": extract_field(text, r'Fare Charges.*?₹([\d.,]+)'),
        "Other Charges": extract_field(text, r'Service Fees\s*₹([\d.,]+)'),
        "CGST": "N/A",
        "SGST": "N/A",
        "IGST": extract_field(text, r'IGST.*?₹([\d.,]+)'),
        "Total Payable": extract_field(text, r'Grand Total\s*₹([\d.,]+)'),
        "Amount in Words": "N/A"
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
    data = {
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

    return data


def extract_invoice_data(text, file_name):
    fmt = detect_invoice_format(text)
    if fmt == "le_travenues":
        return extract_le_travenues(text, file_name)
    elif fmt == "makemytrip":
        return extract_makemytrip(text, file_name)
    else:
        return extract_generic(text, file_name)

# --------------------
# Main Extraction Flow
# --------------------
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

                # Move to processed/
                shutil.move(full_path, os.path.join(processed_path, file))
                print(f"[✓] Moved to processed/: {file}")

            except Exception as e:
                print(f"[✗] Failed on {file} → {e}")

    return extracted_data

# -------------------
# Save Output to Excel
# -------------------
def save_to_excel(data, filename=OUTPUT_FILE):
    if os.path.exists(filename):
        existing = pd.read_excel(filename)
        combined = pd.concat([existing, pd.DataFrame(data)], ignore_index=True)
    else:
        combined = pd.DataFrame(data)
    combined.to_excel(filename, index=False)
    print(f"[📄] Data saved to {filename}")

# -------------------
# Run Everything
# -------------------
if __name__ == "__main__":
    extracted = process_all_invoices(INVOICE_FOLDER, PROCESSED_FOLDER)
    if extracted:
        save_to_excel(extracted)
    else:
        print("[⚠️] No new invoices found.")
