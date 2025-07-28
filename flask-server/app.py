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
# Password = ""

# print(sEmail,API_KEY)


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

def generate_password(length=12):
    import secrets
    import string
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

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

        #==========================================
        # password = generate_password()
        # with open("secrets/password.txt", "w") as f:
        #     f.write(password)
        # # Secure password source
        # with open("secrets/password.txt") as f:
        #     password = f.read().strip()
        #==============================================
        
        with open("secrets/password.txt", "r") as f:
            old_password = f.read().strip()
        print(old_password)
        
        password = generate_password(len(old_password))

        
        with open("secrets/password.txt", "w") as f:
            f.write(password)
        
        
        
        writer.encrypt(password)
        writer.write(final_io)
        final_io.seek(0)
        
        # email_send(Password,context["email"])
        sendEmail(context['email'],context['name'],password,final_io)

        return send_file(
            final_io,
            mimetype="application/pdf",
            download_name="onboarding_bundle.pdf"  # preview-enabled
        )

    except Exception as e:
        print("Error generating PDF:", e)
        return {"error": str(e)}, 500


# @app.route('/api/get-password', methods=['GET'])
# def get_password():
#     try:
#         with open("secrets/password.txt") as f:
#             password = f.read().strip()
#         return {"password": password}
#     except Exception as e:
#         return {"error": str(e)}, 500
    
#--------------------------------------------------------    



#-------------------------------------------------------   
# def email_send(email,password=Password):
#     url = "https://api.elasticemail.com/v2/email/send"
#     payload = {
#     "apikey": API_KEY,
#     "from": "saurabhparmar205@gmail.com",
#     "to": "saurabhparmar205@gmai.coml",
#     "subject": "Hello from Elastic Email",
#     "bodyText": f"This is a test email from localhost.\n The Password of Secret file is {password}"
#     }

#     response = requests.post(url, data=payload)
#     result = response.json()
#     if result.get('success'):
#         print("✅ Email sent successfully.")
#     else:
#         print("❌ Email failed to send.")
#         print("Error:", result.get('error'))
#         print(response.json())
    
    
def sendEmail(rEmail,rName,Password,encoded_file ):
    
    import base64
    mailjet = Client(auth=(API_KEY,API_SECRET), version='v3.1')
    file = base64.b64encode(encoded_file.read()).decode()
   
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
                    "ContentType": "application/pdf",  # MIME type
                    "Filename": "Appointment.pdf",          # Display name
                    "Base64Content": encoded_file       # Base64 content
                }
            ],
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())

if __name__ == '__main__':
    app.run(debug=False, port=5000)
