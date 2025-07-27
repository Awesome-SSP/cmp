// src/components/EmployeeForm.jsx
import { useState } from 'react';
import axios from 'axios';

export default function EmployeeForm() {
  const [formData, setFormData] = useState({
    name: '',
    doj: '',
    designation: '',
    salary: ''
  });

  const [pdfUrl, setPdfUrl] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:5000/api/generate-pdf', formData, {
        responseType: 'blob'
      });
      const file = new Blob([res.data], { type: 'application/pdf' });
      setPdfUrl(URL.createObjectURL(file));
    } catch (err) {
      alert("Error generating PDF");
    }
  };

  return (
    <div>
      <h2>Onboarding Document Generator</h2>
      <form onSubmit={handleSubmit}>
        {['name', 'doj', 'designation', 'salary'].map((field) => (
          <div key={field}>
            <label>{field}</label>
            <input name={field} value={formData[field]} onChange={handleChange} required />
          </div>
        ))}
        <button type="submit">Generate PDF</button>
      </form>

      {pdfUrl && (
        <div>
          <a href={pdfUrl} download="onboarding_bundle.pdf">Download PDF</a>
        </div>
      )}
    </div>
  );
}
