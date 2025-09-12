import { Brain, ArrowRight, Shield } from "lucide-react";
import { useNavigate } from "react-router-dom";
import "./HomePage.css"; // CSS import

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="homepage">
      {/* Header */}
      <header className="header">
        <div className="header-container">
          <div className="logo-section">
            <div className="logo-icon">
              <Brain className="icon" />
            </div>
            <div>
              <h1 className="logo-title">InternAI</h1>
              <p className="logo-subtitle">Powered by PM Modi Portal</p>
            </div>
          </div>

          <nav className="nav">
            <button className="btn-primary" onClick={() => navigate("/form")}>
              Get Started
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-container">
          <span className="badge">
            <Shield className="badge-icon" />
            Government Affiliated Platform
          </span>

          <h1 className="hero-title">
            Empowering Your Future with{" "}
            <span className="highlight">AI-Driven</span> Internship Opportunities
          </h1>

          <p className="hero-desc">
            Discover personalized internship recommendations powered by pm internship scheme
          </p>

          <div className="hero-buttons">
            <button className="btn-primary-lg" onClick={() => navigate("/form")}>
              Find My Perfect Internship
              <ArrowRight className="btn-icon" />
            </button>
          </div>

          <div className="hero-image">
          </div>
        </div>
      </section>
    </div>
  );
}
