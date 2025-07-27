# 📄 DocForge

**DocForge** is an automated document generation tool that creates personalized onboarding bundles (Offer Letter, NDA, and Company Policy) for new employees. It fills in dynamic fields using employee data, merges all documents into a single password-protected PDF, and serves it via a Flask API with a React frontend.

---

## 🚀 Features

- 🧾 Fill dynamic placeholders in templates using employee info (name, DOJ, salary, etc.)
- 📎 Merge Offer Letter, NDA, and Policy into a single PDF
- 🔐 Password-protect final PDF using a secure Vault-based secret
- 📤 Serve PDF via Flask backend API
- 💻 Frontend in React with inline styling and blob download
- 🌐 CORS-enabled API communication
- 📦 Ready for deployment on Render (backend) and Vercel (frontend)

---

## 🧱 Tech Stack

| Layer      | Technology      |
|------------|-----------------|
| Frontend   | React.js        |
| Backend    | Flask + Flask-CORS |
| PDF Tools  | ReportLab, PyPDF2 |
| Template   | Jinja2          |
| Secrets    | File-based or Vault (extensible) |
| Hosting    | Vercel (frontend), Render or Railway (backend) |

---

## 📁 Project Structure

```bash

DocForge/
├── flask-server/
│ ├── app.py
│ ├── templates/
│ │ ├── offer_letter.txt
│ │ ├── nda.txt
│ │ └── policy.txt
│ └── requirements.txt
├── doc-forge/
│ ├── src/
│ │ ├── components
| | |  ├── employeeform.jsx
│ │ └── App.js
│ └── .env
└── README.md

```

1. Navigate to the `doc-forge/` folder:
```bash
cd doc-forge
npm install .
npm i . --force
npm start

```

OR

```bash

python -m venv venv  # create  a virtual env
source venv/bin/activate  # On Windows: venv\Scripts\activate

cd flask-server
pip install -r requirement.txt
python app.py
```

🔐 Password Management
The password used to lock the final PDF is fetched from secrets/password.txt

Can be extended to use a real secret manager like Vault, AWS Secrets Manager, or GCP Secret Manager

🌐 Deployment
Frontend:

Deploy React app to Vercel

Backend:

Deploy Flask app to Render or Railway

Replace local API base URL with production URL in .env

📥 API
POST /api/generate-pdf
Generate a PDF onboarding bundle.

Payload:
```bash
{
  "name": "John Doe",
  "doj": "2025-08-01",
  "designation": "Software Engineer",
  "salary": "₹12,00,000"
}

```
Response:
Returns a application/pdf Blob file (password-protected)

🤝 Contributing
Pull requests and suggestions are welcome! Open issues for enhancements or bugs.

## Authors

- [@SSP](https://github.com/Awesome-SSP)

## Support

For support, you can buy me a coffee

<a href="https://buymeacoffee.com/i.awesomessp" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
