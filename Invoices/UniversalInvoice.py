import os
import re
import fitz
import pandas as pd
from pdf2image import convert_from_path
import pytesseract

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

def detect_invoice_format(text):
    if "LE TRAVENUES TECHNOLOGY LIMITED" in text:
        return "le_travenues"
    elif "MAKEMYTRIP (INDIA) PRIVATE LIMITED" in text:
        return "makemytrip"
    else:
        return "unknown"

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
        "Invoice Number": re.search(r'Invoice No\.\s*([A-Z0-9]+)', text).group(1) if re.search(r'Invoice No\.\s*([A-Z0-9]+)', text) else "N/A",
        "Booking ID": re.search(r'Booking ID\s*([A-Z0-9]+)', text).group(1) if re.search(r'Booking ID\s*([A-Z0-9]+)', text) else "N/A",
        "Invoice Date": re.search(r'Date\s*([0-9A-Za-z ]+)', text).group(1).strip() if re.search(r'Date\s*([0-9A-Za-z ]+)', text) else "N/A",
        "GSTIN": re.search(r'GSTIN\s*([0-9A-Z]+)', text).group(1) if re.search(r'GSTIN\s*([0-9A-Z]+)', text) else "N/A",
        "Customer Name": re.search(r'Customer Name\s*([A-Za-z ]+)', text).group(1).strip() if re.search(r'Customer Name\s*([A-Za-z ]+)', text) else "N/A",
        "Fare": re.search(r'Fare Charges.*?₹([\d.,]+)', text).group(1) if re.search(r'Fare Charges.*?₹([\d.,]+)', text) else "N/A",
        "Service Charges": re.search(r'Service Fees\s*₹([\d.,]+)', text).group(1) if re.search(r'Service Fees\s*₹([\d.,]+)', text) else "N/A",
        "IGST": re.search(r'IGST.*?₹([\d.,]+)', text).group(1) if re.search(r'IGST.*?₹([\d.,]+)', text) else "N/A",
        "Total Payable": re.search(r'Grand Total\s*₹([\d.,]+)', text).group(1) if re.search(r'Grand Total\s*₹([\d.,]+)', text) else "N/A",
        "CGST": "N/A",
        "SGST": "N/A"
    }

def extract_generic(text, file_name):
    return {
        "File Name": file_name,
        "Company": "Unknown",
        "Invoice Number": "N/A",
        "Booking ID": "N/A",
        "Invoice Date": "N/A",
        "GSTIN": "N/A",
        "Customer Name": "N/A",
        "Fare": "N/A",
        "Service Charges": "N/A",
        "CGST": "N/A",
        "SGST": "N/A",
        "IGST": "N/A",
        "Total Payable": "N/A"
    }

def extract_invoice_data(text, file_name):
    fmt = detect_invoice_format(text)
    if fmt == "le_travenues":
        return extract_le_travenues(text, file_name)
    elif fmt == "makemytrip":
        return extract_makemytrip(text, file_name)
    else:
        return extract_generic(text, file_name)

def process_all_invoices(folder_path):
    results = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            path = os.path.join(folder_path, file)
            print(f"Processing: {file}")
            try:
                text = extract_text_from_pdf(path)
                result = extract_invoice_data(text, file)
                results.append(result)
            except Exception as e:
                print(f"Error processing {file}: {e}")
    return results

def save_to_excel(data, filename="invoice_output.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"[✓] Saved to {filename}")

if __name__ == "__main__":
    folder_path = "invoices"
    extracted_data = process_all_invoices(folder_path)
    save_to_excel(extracted_data)
