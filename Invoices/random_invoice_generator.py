import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from faker import Faker

fake = Faker()

def random_invoice_data():
    fare = round(random.uniform(2000, 20000), 2)
    service_fee = round(random.uniform(100, 500), 2)
    cgst = round(service_fee * 0.09, 2)
    sgst = round(service_fee * 0.09, 2)
    igst = 0.00
    total = round(fare + service_fee + cgst + sgst + igst, 2)

    return {
        "invoice_number": f"IXIFT{random.randint(100000000000,999999999999)}",
        "booking_id": f"IF{random.randint(10000000000000,99999999999999)}",
        "gstin": f"06{fake.bothify(text='?????????????1Z#').upper()}",
        "invoice_date": datetime.now().strftime("%a %b %d %Y %H:%M:%S IST"),
        "customer_name": fake.name(),
        "billing_address": fake.address().replace('\n', ', '),
        "fare": f"{fare:.2f}",
        "other_charges": f"{service_fee:.2f}",
        "cgst": f"{cgst:.2f}",
        "sgst": f"{sgst:.2f}",
        "igst": f"{igst:.2f}",
        "total": f"{total:.2f}"
    }

def generate_invoice_le_travenues(data, output_dir="generated_pdfs"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"Invoice_{data['invoice_number']}.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 50, "Tax Invoice: " + data["invoice_number"])

    c.setFont("Helvetica", 11)
    c.drawString(30, height - 80, "LE TRAVENUES TECHNOLOGY LIMITED")
    c.drawString(30, height - 95, "Second Floor, Veritas Building, Sector 53,")
    c.drawString(30, height - 110, "Golf Course Road, Gurgaon, Haryana, 122002")

    y = height - 150
    c.drawString(30, y, f"Booking ID: {data['booking_id']}")
    c.drawString(30, y - 15, f"GSTIN: {data['gstin']}")
    c.drawString(30, y - 30, f"Invoice Date: {data['invoice_date']}")
    c.drawString(30, y - 45, f"Customer: {data['customer_name']}")
    c.drawString(30, y - 60, f"Billing Address: {data['billing_address']}")

    y -= 100
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y, "Charges Summary")

    c.setFont("Helvetica", 11)
    c.drawString(30, y - 20, f"Fare (Incl. of Taxes): ₹{data['fare']}")
    c.drawString(30, y - 35, f"Other Charges: ₹{data['other_charges']}")
    c.drawString(30, y - 50, f"CGST: ₹{data['cgst']}")
    c.drawString(30, y - 65, f"SGST: ₹{data['sgst']}")
    c.drawString(30, y - 80, f"IGST: ₹{data['igst']}")
    c.drawString(30, y - 100, f"Total Payable: ₹{data['total']}")

    c.drawString(30, y - 130, "Thank you for booking with Le Travenues!")
    c.save()
    print(f"[✓] Generated: {file_path}")

def generate_many_invoices(count=5):
    for _ in range(count):
        data = random_invoice_data()
        generate_invoice_le_travenues(data)

if __name__ == "__main__":
    generate_many_invoices(count=700)
