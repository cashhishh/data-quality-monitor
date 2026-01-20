import QualityPieChart from "../components/QualityPieChart";

import { useEffect, useState } from "react";
import { fetchDashboardStats } from "../services/api";
import "./Dashboard.css";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await fetchDashboardStats();
        setStats(data);
      } catch (err) {
        setError("Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) return <p style={{ padding: "24px" }}>Loading dashboard...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  const passedChecks =
  stats.total_checks - stats.failed_checks;


  return (
    <div className="dashboard-page">
      <h1 className="page-title">Dashboard</h1>

<section className="dashboard-section">
  <div className="dashboard-grid">
    <div className="dashboard-card">
      <h3>Total Datasets</h3>
      <p>{stats.total_datasets}</p>
    </div>

    <div className="dashboard-card">
      <h3>Average Quality Score</h3>
      <p>{stats.average_quality_score}%</p>
    </div>

    <div className="dashboard-card">
      <h3>Failed Checks</h3>
      <p>{stats.failed_checks}</p>
    </div>

    <div className="dashboard-card">
      <h3>Last Run</h3>
      <p>{stats.last_run || "N/A"}</p>
    </div>
  </div>
</section>

<section className="dashboard-section">
  <h2 className="section-title">Quality Overview</h2>

  <QualityPieChart
    passed={stats.total_checks - stats.failed_checks}
    failed={stats.failed_checks}
  />
</section>

    </div>
  );
}
