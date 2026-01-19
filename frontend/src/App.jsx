import { useState } from "react";
import axios from "axios";

function App() {
  const [loading, setLoading] = useState(false);

  const [file, setFile] = useState(null);
  const [datasetId, setDatasetId] = useState(null);
  const [message, setMessage] = useState("");
  const [results, setResults] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/datasets/upload",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setDatasetId(response.data.dataset_id);
      setMessage(`Upload successful! Dataset ID: ${response.data.dataset_id}`);
      setResults(null);
    } catch (error) {
      setMessage("Upload failed");
      console.error(error);
    }
  };
const runChecks = async () => {
  if (!datasetId) return;

  setLoading(true);
  setMessage("");

  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/datasets/run-checks/${datasetId}`
    );
    setResults(response.data.results);
  } catch (error) {
    setMessage("Failed to run checks");
    console.error(error);
  } finally {
    setLoading(false);
  }
};


  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Data Quality Monitoring System</h1>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload}>Upload Dataset</button>

      {datasetId && (
        <>
          <br /><br />
         <button onClick={runChecks} disabled={loading}>
  {loading ? "Running checks..." : "Run Data Quality Checks"}
</button>


        </>
      )}

      <p>{message}</p>

      {results && (
        <div>
          <h3>Quality Check Results</h3>
          <ul>
            <li>Null values: {results.null_check}</li>
            <li>Duplicate rows: {results.duplicate_check}</li>
            <li>Anomalies: {results.anomaly_check}</li>
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
