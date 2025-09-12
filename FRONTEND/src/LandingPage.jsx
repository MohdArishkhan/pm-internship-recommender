import React from "react";
import { FaBolt, FaArrowRight } from "react-icons/fa";
import modiImage from "./assets/modijiimg.png";
import "./App.css";
import { useNavigate } from "react-router-dom";  

function LandingPage() {
  const navigate = useNavigate(); 

  return (
    <div className="container">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="header-logo">
            <span role="img" aria-label="logo"></span>
            <div>
              <p className="header-text-small">
                भारत सरकार / Government Of India
              </p>
              <p className="header-text-large">Ministry of Corporate Affairs</p>
            </div>
          </div>
          <div className="header-internship">
            <FaBolt className="header-icon" />
            <span>AI-Based Internship Recommendation</span>
          </div>
        </div>
        <div className="header-right">
          <button 
            className="btn btn-login" 
            onClick={() => navigate("/form")}   
          >
            <FaArrowRight />
            <span>Get Started</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="left-panel">
          <h1 className="main-title">Find Your Perfect Internship</h1>
          <p className="subtitle">AI-powered internship recommendations.</p>
          <p className="description">
            Our intelligent system analyzes your skills, interests, and career
            goals to recommend the perfect internship opportunities just for you.
          </p>
          <button 
            className="btn-discover" 
            onClick={() => navigate("/form")}  
          >
            <FaBolt />
            <span>Discover Matches</span>
          </button>
        </div>
        <div className="right-panel">
          <div className="modi-container">
            <img
              src={modiImage}
              alt="Narendra Modi"
              className="modi-image"
              width="150"
              height="100"
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default LandingPage;
