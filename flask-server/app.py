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
            "salary": data.get("salary", "N/A"),
            "email":data.get("email","N/A")
        }

        offer_text = fill_template("templates/offer_letter.txt", context)
        nda_text = fill_template("templates/nda.txt", context)
        policy_text = fill_template("templates/policy.txt", context)

        offer_pdf = text_to_pdf(offer_text)
        offer_pdf.seek(0)

        nda_pdf = text_to_pdf(nda_text)
        nda_pdf.seek(0)

        policy_pdf = text_to_pdf(policy_text)
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
                    "Name": "Saurabh"
                },
                "To": [
                    {
                        "Email": rEmail,
                        "Name": rName
                    }
                ],
                "Subject": "Hello from Mailjet",
                "TextPart": f"This is a test email sent using Mailjet and Python. The secret is {Password}",
                "HTMLPart": f"<h3>This is a test email from <strong>Mailjet</strong>!<br><b>The Secret is:</b> {Password}</h3>",
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
