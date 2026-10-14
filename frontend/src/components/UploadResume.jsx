import { useState } from "react";
import axios from "axios";

function UploadResume() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      setMessage("Please select a PDF file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select your resume first.");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      setLoading(true);
      setMessage("");

      const response = await axios.post(
        "http://127.0.0.1:8000/api/resume/upload",
        formData
      );

      setMessage(
        `✓ ${response.data.message}. ${response.data.chunks_created} resume sections processed.`
      );
    } catch (error) {
      console.error(error);

      setMessage(
        "Failed to upload resume. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="upload-section">

      <div className="upload-card">

        <p className="section-label">
          RESUME ANALYSIS
        </p>

        <h2>
          Upload your resume
        </h2>

        <p className="upload-description">
          Upload your PDF resume and let your AI Career
          Agent understand your skills, projects and experience.
        </p>


        <div className="file-input-wrapper">

          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
          />

        </div>


        {file && (
          <p className="selected-file">
            Selected: {file.name}
          </p>
        )}


        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "Uploading..." : "Upload Resume"}
        </button>


        {message && (
          <p className="upload-message">
            {message}
          </p>
        )}

      </div>

    </section>
  );
}

export default UploadResume;