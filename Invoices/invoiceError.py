import logging

logging.basicConfig(filename='errors.log', level=logging.ERROR)

# Inside process_all_invoices:
try:
    data = extract_from_pdf(path)
    records.append(data)
    print(f"[✓] Processed: {file}")
except Exception as e:
    logging.error(f"Failed: {file} | Error: {str(e)}")
    print(f"[✗] Failed: {file}")
