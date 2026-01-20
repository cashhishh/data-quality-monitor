import QualityBarChart from "../components/QualityBarChart";

import { useState, useEffect } from "react";

import { runQualityChecks, getLatestDataset } from "../services/api.js";

import "./QualityChecks.css";

export default function QualityChecks() {
  const [datasetId, setDatasetId] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
useEffect(() => {
  const fetchLatest = async () => {
    try {
      const data = await getLatestDataset();
      if (data.dataset_id) {
        setDatasetId(data.dataset_id);
      }
    } catch (err) {
      console.error("Failed to fetch latest dataset");
    }
  };

  fetchLatest();
}, []);

  const handleRunChecks = async () => {
    if (!datasetId) return;

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data = await runQualityChecks(datasetId);
      console.log("API RESPONSE:", data);

      // 🔁 Transform backend response → frontend-friendly format
setResult(data);

    } catch (err) {
      console.error(err);
      setError("Failed to run quality checks");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="checks-page">
      <h1>Data Quality Checks</h1>

      <div className="checks-input">
        <input
          type="number"
          placeholder={datasetId}
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
        />
        <button onClick={handleRunChecks} disabled={loading}>
          {loading ? "Running..." : "Run Checks"}
        </button>
      </div>

      {loading && <p>Running checks...</p>}
      {error && <p className="error">{error}</p>}

      {/* DEBUG VIEW (SAFE) */}
      {result && (
        <pre style={{ background: "#111", color: "#0f0", padding: "16px" }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}

      {/* UI ONLY IF checks ARRAY EXISTS */}
      {Array.isArray(result?.checks) && (
        <>
        <div className="summary-grid">
          <h2 className="section-title">Run Summary</h2>

  <div className="summary-card">
    <h3>Dataset ID</h3>
    <p className="summary-value">{result.dataset_id}</p>
  </div>

  <div className="summary-card">
    <h3>Overall Quality</h3>
    <p className="summary-value">{result.overall_score}%</p>

    <div className="progress-bar">
      <div
        className="progress-fill"
       style={{
  width: `${result.overall_score}%`,
  backgroundColor:
    result.overall_score >= 80
      ? "#22c55e"
      : result.overall_score >= 50
      ? "#facc15"
      : "#ef4444",
}}

      />
    </div>
  </div>

  <div className="summary-card">
    <h3>Total Checks</h3>
    <p className="summary-value">{result.checks.length}</p>
  </div>
</div>
          <div className="table-wrapper">
            <h2 className="section-title">Validation Results</h2>

            <table className="checks-table">
              <thead>
                <tr>
                  <th>Check Name</th>
                  <th>Status</th>
                  <th>Failed Rows</th>
                </tr>
              </thead>
              <tbody>
  {result.checks.map((check, idx) => (
    <tr key={idx}>
      <td>{check.check_name}</td>
      <td>
        <span
          className={
            check.status === "PASS"
              ? "badge badge-pass"
              : "badge badge-fail"
          }
        >
          {check.status === "PASS" ? "✔ PASS" : "✖ FAIL"}
        </span>
      </td>
      <td>{check.failed_rows}</td>
    </tr>
  ))}
  <h2 style={{ marginTop: "40px" }}>Failures by Check Type</h2>
  <h2 className="section-title">Failures by Rule</h2>


<QualityBarChart checks={result.checks} />

</tbody>

            </table>
          </div>
        </>
      )}
    </div>
  );
}
