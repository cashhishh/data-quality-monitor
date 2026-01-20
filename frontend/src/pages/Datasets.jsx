import { useState } from "react";
import { uploadDataset } from "../services/api";

function Datasets() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const result = await uploadDataset(file);
      setMessage(`Upload successful. Dataset ID: ${result.dataset_id || "N/A"}`);
    } catch (err) {
      setError("Upload failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <h1>Upload Dataset</h1>
      <p>Select a CSV file to upload and register for quality checks.</p>

      <div style={{ marginTop: "24px" }}>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <br /><br />

        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Uploading..." : "Upload Dataset"}
        </button>
      </div>

      {message && <p style={{ color: "green", marginTop: "16px" }}>{message}</p>}
      {error && <p style={{ color: "red", marginTop: "16px" }}>{error}</p>}
    </>
  );
}

export default Datasets;
