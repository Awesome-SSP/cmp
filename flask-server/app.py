from flask import Flask, request, send_file
from jinja2 import Template
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
import os
import requests
from flask_cors import CORS 
from dotenv import load_dotenv
from mailjet_rest import Client


from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# Load variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

sEmail = os.getenv('sender-email')
API_KEY = os.getenv("mailjet-api-key")
API_SECRET = os.getenv("mailjet-secret-key")

def generate_password(length=12):
    import secrets
    import string
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def fill_template(template_path, context):
    with open(template_path,encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**context)

# def text_to_pdf(text):
#     buffer = io.BytesIO()
#     c = canvas.Canvas(buffer)
#     for i, line in enumerate(text.split('\n')):
#         c.drawString(40, 800 - i * 15, line)
#     c.save()
#     buffer.seek(0)
#     return buffer

def text_to_pdf(text, logo_path=None):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    import io

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    if logo_path:
        c.drawImage(logo_path, 70, 770, width=120, height=50, preserveAspectRatio=True)

    c.setFont("Helvetica", 12)
    text_start_y = 720
    for i, line in enumerate(text.splitlines()):
        c.drawString(72, text_start_y - 18 * i, line)
    
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
            "salary": data.get("salary", "N/A"),
            "email":data.get("email","N/A")
        }

        offer_text = fill_template("templates/offer_letter.txt", context)
        nda_text = fill_template("templates/nda.txt", context)
        policy_text = fill_template("templates/policy.txt", context)

        offer_pdf = text_to_pdf(offer_text, logo_path="assets/company_logo.png")
        # offer_pdf = text_to_pdf(offer_text)
        offer_pdf.seek(0)

        nda_pdf = text_to_pdf(nda_text, logo_path="assets/company_logo.png")
        nda_pdf.seek(0)

        policy_pdf = text_to_pdf(policy_text, logo_path="assets/company_logo.png")
        policy_pdf.seek(0)

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

        # # Secure password source
        # with open("secrets/password.txt") as f:
        #     password = f.read().strip()
        
        with open("secrets/password.txt", "r") as f:
            old_password = f.read().strip()
        print(old_password)
        
        password = generate_password(len(old_password))

        
        with open("secrets/password.txt", "w") as f:
            f.write(password)

        writer.encrypt(password)
        writer.write(final_io)
        final_io.seek(0)
        
        sendEmail(context['email'],context['name'],password,final_io)

        return send_file(
            final_io,
            mimetype="application/pdf",
            download_name= "Appointment.pdf",    # preview-enabled
            as_attachment=False
        )

    except Exception as e:
        print("Error generating PDF:", e)
        return {"error": str(e)}, 500

def sendEmail(rEmail, rName, Password, encoded_file):
    import base64
    from mailjet_rest import Client
    encoded_file.seek(0)
    file_content = base64.b64encode(encoded_file.read()).decode()

 
    mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')

    # Prepare data
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sEmail,
                    "Name": "Google.com"
                },
                "To": [
                    {
                        "Email": rEmail,
                        "Name": rName
                    }
                ],
                # "Subject": f"APPOINTMENT TO THE JOB IN OUR COMPANY DEAR {rName}",
                # "TextPart": f"This is a test email sent using Mailjet and Python. The secret is {Password}",
                # "HTMLPart": f"<h3>This is a test email from <strong>Mailjet</strong>!<br><b>The Secret is:</b> {Password}</h3>",

                "Subject": f"🎉 Congratulations {rName}, Your Appointment with Our Company!",
"TextPart": (
    f"Dear {rName},\n\n"
    "We are excited to confirm your appointment to join our team at [Company Name]! "
    "This is a great step forward, and we look forward to working with you.\n\n"
    f"Your unique secret code for onboarding is: {Password}\n\n"
    "Please keep this information confidential.\n\n"
    "Best regards,\n"
    "[Company Name] HR Team"
),
"HTMLPart": (
    f"<div style='font-family: Arial, sans-serif; color: #333;'>"
    f"<h2 style='color: #2E86C1;'>Welcome to <strong>Google LLC</strong>, {rName}!</h2>"
    f"<p>We are thrilled to appoint you as a valued member of our team.</p>"
    f"<p><strong>Your secret onboarding code is:</strong> "
    f"<span style='color: #E67E22;'>{Password}</span></p>"
    f"<p>Please keep this code confidential.</p>"
    f"<br>"
    f"<p>Looking forward to an exciting journey ahead!</p>"
    f"<p><em>Best regards,<br>HR Team</em></p>"
    f"</div>"
),


                "Attachments": [
                    {
                        "ContentType": "application/pdf",
                        "Filename": "Appointment.pdf",
                        "Base64Content": file_content  # ✅ Use base64-encoded string
                    }
                ],
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }

    # Send the email
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())


# @app.route('/api/get-password', methods=['GET'])
# def get_password():
#     try:
#         with open("secrets/password.txt") as f:
#             password = f.read().strip()
#         return {"password": password}
#     except Exception as e:
#         return {"error": str(e)}, 500
    
    
if __name__ == '__main__':
    app.run(debug=False, port=5000)
