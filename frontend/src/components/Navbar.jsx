import { Link } from "react-router-dom";
import { useState } from "react";
import "./Navbar.css";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="logo">Data Quality Monitor</div>

        <div className={`nav-links ${open ? "open" : ""}`}>
          <Link to="/" onClick={() => setOpen(false)}>Home</Link>
          <Link to="/datasets" onClick={() => setOpen(false)}>Datasets</Link>
          <Link to="/checks" onClick={() => setOpen(false)}>Quality Checks</Link>
          <Link to="/dashboard" onClick={() => setOpen(false)}>Dashboard</Link>
        </div>

        <div className="menu-btn" onClick={() => setOpen(!open)}>
          ☰
        </div>
      </div>
    </nav>
  );
}
