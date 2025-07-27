from flask import Flask, request, send_file
from jinja2 import Template
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
import os

from flask_cors import CORS 

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})




def fill_template(template_path, context):
    with open(template_path) as f:
        template = Template(f.read())
    return template.render(**context)

def text_to_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    for i, line in enumerate(text.split('\n')):
        c.drawString(40, 800 - i * 15, line)
    c.save()
    buffer.seek(0)
    return buffer

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        context = {
            "name": data.get("name", "Unknown"),
            "doj": data.get("doj", "N/A"),
            "designation": data.get("designation", "N/A"),
            "salary": data.get("salary", "N/A")
        }

        offer_text = fill_template("templates/offer_letter.txt", context)
        nda_text = fill_template("templates/nda.txt", context)
        policy_text = fill_template("templates/policy.txt", context)

        offer_pdf = text_to_pdf(offer_text)
        nda_pdf = text_to_pdf(nda_text)
        policy_pdf = text_to_pdf(policy_text)

        merger = PdfMerger()
        merger.append(offer_pdf)
        merger.append(nda_pdf)
        merger.append(policy_pdf)

        merged_io = io.BytesIO()
        merger.write(merged_io)
        merger.close()
        merged_io.seek(0)

        final_io = io.BytesIO()
        reader = PdfReader(merged_io)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Secure password source
        with open("secrets/password.txt") as f:
            password = f.read().strip()

        writer.encrypt(password)
        writer.write(final_io)
        final_io.seek(0)

        return send_file(
            final_io,
            mimetype="application/pdf",
            download_name="onboarding_bundle.pdf"  # preview-enabled
        )

    except Exception as e:
        print("Error generating PDF:", e)
        return {"error": str(e)}, 500


@app.route('/api/get-password', methods=['GET'])
def get_password():
    try:
        with open("secrets/password.txt") as f:
            password = f.read().strip()
        return {"password": password}
    except Exception as e:
        return {"error": str(e)}, 500
    
    
if __name__ == '__main__':
    app.run(debug=False, port=5000)
