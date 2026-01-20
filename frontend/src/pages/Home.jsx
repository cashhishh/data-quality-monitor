import "./Home.css";
import { Link } from "react-router-dom";
import heroImage from "../assets/data-quality-Monitoring-min.jpg"

function Home() {
  return (
    <div className="home">
      {/* Hero */}
     <section className="hero">
        <div className="hero-text">
          <h1>Data Quality Monitoring System</h1>
          <p>
            Upload datasets, run automated quality checks, and monitor data
            health across your data pipeline.
          </p>

          <div className="hero-actions">
            <Link to="/datasets" className="btn primary">
              Upload Dataset
            </Link>
            <Link to="/dashboard" className="btn secondary">
              View Dashboard
            </Link>
          </div>
        </div>

        <div className="hero-image">
          <img src={heroImage} alt="Data analytics illustration" />
        </div>
      </section>

      {/* Features */}
      <section className="features">
  <h2 className="section-title">Core Capabilities</h2>

  <div className="feature-grid">
    <div className="feature-card">
      <h3>Dataset Upload</h3>
      <p>
        Upload CSV datasets securely and register them for validation.
      </p>
    </div>

    <div className="feature-card t">
      <h3>Automated Quality Checks</h3>
      <p>
        Identify missing values, duplicates, and schema mismatches instantly.
      </p>
    </div>

    <div className="feature-card">
      <h3>Insights & Monitoring</h3>
      <p>
        Track data health trends and validation results over time.
      </p>
    </div>
  </div>
</section>

<section className="process">
  <h2 className="section-title">How It Works</h2>

  <div className="process-steps">
    <div className="step">
      <span className="step-number">1</span>
      <p>Upload a dataset in CSV format</p>
    </div>

    <div className="step">
      <span className="step-number">2</span>
      <p>Run automated data quality checks</p>
    </div>

    <div className="step">
      <span className="step-number">3</span>
      <p>Review issues and insights on dashboard</p>
    </div>
  </div>
</section>

      {/* Stats */}
      <section className="stats">
  <div className="stat">
    <span className="stat-number">4</span>
    <span className="stat-label">Datasets Processed</span>
  </div>
  <div className="stat">
    <span className="stat-number">12</span>
    <span className="stat-label">Checks Executed</span>
  </div>
  <div className="stat">
    <span className="stat-number">3</span>
    <span className="stat-label">Critical Issues</span>
  </div>
</section>

    </div>
  );
}

export default Home;
