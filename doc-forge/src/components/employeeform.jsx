import { useState } from "react";
import axios from "axios";

export default function EmployeeForm() {
  const [formData, setFormData] = useState({
    name: "",
    doj: "",
    designation: "",
    salary: "",
    email: "",
  });

  // const [password, setPassword] = useState(null);

  const [pdfUrl, setPdfUrl] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_BASE}/api/generate-pdf`,
        formData,
        { responseType: "blob" }
      );

      // const passRes = await axios.get(
      //   `${process.env.REACT_APP_API_BASE}/api/get-password`
      // );
      // setPassword(passRes.data.password);

      const contentType = res.headers["content-type"];
      if (!contentType.includes("application/pdf")) {
        throw new Error("Expected a PDF, but got: " + contentType);
      }

      const blob = new Blob([res.data], { type: "application/pdf" });

      // Clean up old object URL
      if (pdfUrl) {
        URL.revokeObjectURL(pdfUrl);
      }

      const blobUrl = URL.createObjectURL(blob);
      setPdfUrl(blobUrl);
    } catch (err) {
      console.error("PDF generation error:", err);
      alert("Failed to generate PDF.");
    }
  };

  return (
    <div
      style={{
        maxWidth: "500px",
        margin: "40px auto",
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "10px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h2 style={{ textAlign: "center", color: "#333", marginBottom: "30px" }}>
        Onboarding Document Generator
      </h2>

      <form onSubmit={handleSubmit}>
        {["name", "doj", "designation", "salary", "email"].map((field) => (
          <div key={field} style={{ marginBottom: "20px" }}>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontWeight: "bold",
                color: "#555",
                textTransform: "capitalize",
              }}
            >
              {field}
            </label>
            <input
              name={field}
              value={formData[field]}
              onChange={handleChange}
              required
              style={{
                width: "100%",
                padding: "10px",
                border: "1px solid #ccc",
                borderRadius: "5px",
                fontSize: "14px",
              }}
            />
          </div>
        ))}

        <button
          type="submit"
          style={{
            width: "100%",
            padding: "12px",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "6px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Generate PDF
        </button>
      </form>

      {pdfUrl && (
        <div style={{ marginTop: "30px", textAlign: "center" }}>
          <a
            href={pdfUrl}
            download="onboarding_bundle.pdf"
            style={{
              color: "#007bff",
              textDecoration: "none",
              fontWeight: "bold",
              marginRight: "15px",
            }}
          >
            Download PDF
          </a>

          {/* <p style={{ color: "red", fontWeight: "bold" }}>
            Password to open the PDF: <code>{password}</code>
          </p> */}

          <iframe
            src={pdfUrl}
            title="PDF Preview"
            width="100%"
            height="500px"
            style={{ border: "1px solid #ccc", marginTop: "20px" }}
          />
        </div>
      )}
    </div>
  );
}
