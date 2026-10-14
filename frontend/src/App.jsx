import { useState } from "react";

import Navbar from "./components/Navbar";
import UploadResume from "./components/UploadResume";
import CareerChat from "./components/CareerChat";
import JobMatch from "./components/JobMatch";
import Interview from "./components/Interview";

import "./App.css";


function App() {

  const [activePage, setActivePage] = useState("dashboard");


  return (
    <div className="app-shell">

      {/* =================================================
          SIDEBAR
      ================================================= */}

      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
      />


      {/* =================================================
          MAIN APPLICATION
      ================================================= */}

      <main className="main-content">

        {/* ===============================================
            TOP BAR
        =============================================== */}

        <header className="topbar">

          <div>
            <p className="topbar-label">
              AI CAREER AGENT
            </p>

            <h1>
              {activePage === "dashboard" && "Career Dashboard"}
              {activePage === "resume" && "Resume"}
              {activePage === "chat" && "AI Career Agent"}
              {activePage === "jobs" && "Job Match"}
              {activePage === "interview" && "Interview"}
            </h1>
          </div>


          <div className="topbar-profile">

            <div className="status-dot"></div>

            <span>
              AI Agent Online
            </span>

          </div>

        </header>


        {/* =================================================
            DASHBOARD
        ================================================= */}

        {activePage === "dashboard" && (

          <section className="dashboard-page">

            {/* Welcome */}

            <div className="welcome-card">

              <div>

                <p className="eyebrow">
                  YOUR PERSONAL AI CAREER ASSISTANT
                </p>

                <h2>
                  Welcome back 👋
                </h2>

                <p>
                  Upload your resume, understand your skills,
                  analyze job opportunities and prepare for
                  your next interview.
                </p>

              </div>

              <div className="welcome-icon">
                ✦
              </div>

            </div>


            {/* Statistics */}

            <div className="stats-grid">

              <div className="stat-card">

                <span className="stat-icon">
                  ◈
                </span>

                <div>

                  <p>
                    Resume
                  </p>

                  <h3>
                    Analyzed
                  </h3>

                </div>

              </div>


              <div className="stat-card">

                <span className="stat-icon">
                  ◆
                </span>

                <div>

                  <p>
                    Skills
                  </p>

                  <h3>
                    AI Extracted
                  </h3>

                </div>

              </div>


              <div className="stat-card">

                <span className="stat-icon">
                  ◎
                </span>

                <div>

                  <p>
                    Job Match
                  </p>

                  <h3>
                    Ready
                  </h3>

                </div>

              </div>

            </div>


            {/* Dashboard Grid */}

            <div className="dashboard-grid">

              {/* Resume Card */}

              <div className="dashboard-card resume-card">

                <div className="card-heading">

                  <div>

                    <p className="card-label">
                      RESUME
                    </p>

                    <h3>
                      Your Resume
                    </h3>

                  </div>

                  <span className="card-icon">
                    📄
                  </span>

                </div>


                <p className="card-description">
                  Upload your resume and let the AI agent
                  understand your skills, projects and experience.
                </p>


                <button
                  className="primary-button"
                  onClick={() => setActivePage("resume")}
                >
                  Manage Resume
                  <span>→</span>
                </button>

              </div>


              {/* AI Chat Card */}

              <div className="dashboard-card chat-preview-card">

                <div className="card-heading">

                  <div>

                    <p className="card-label">
                      AI ASSISTANT
                    </p>

                    <h3>
                      Career Agent
                    </h3>

                  </div>

                  <span className="card-icon">
                    ✦
                  </span>

                </div>


                <p className="card-description">
                  Ask questions about your resume,
                  skills, projects and career.
                </p>


                <button
                  className="secondary-button"
                  onClick={() => setActivePage("chat")}
                >
                  Open AI Agent
                  <span>→</span>
                </button>

              </div>


              {/* Job Match Card */}

              <div className="dashboard-card">

                <div className="card-heading">

                  <div>

                    <p className="card-label">
                      CAREER
                    </p>

                    <h3>
                      Job Match
                    </h3>

                  </div>

                  <span className="card-icon">
                    ◉
                  </span>

                </div>


                <p className="card-description">
                  Compare your resume against a job
                  description and discover your skill gaps.
                </p>


                <button
                  className="secondary-button"
                  onClick={() => setActivePage("jobs")}
                >
                  Analyze a Job
                  <span>→</span>
                </button>

              </div>


              {/* Interview Card */}

              <div className="dashboard-card">

                <div className="card-heading">

                  <div>

                    <p className="card-label">
                      PREPARATION
                    </p>

                    <h3>
                      AI Interview
                    </h3>

                  </div>

                  <span className="card-icon">
                    ◌
                  </span>

                </div>


                <p className="card-description">
                  Practice personalized AI Engineer
                  interviews using your resume.
                </p>


                <button
                  className="secondary-button"
                  onClick={() => setActivePage("interview")}
                >
                  Start Interview
                  <span>→</span>
                </button>

              </div>

            </div>


            {/* Quick Actions */}

            <div className="quick-section">

              <div className="section-heading">

                <div>

                  <p className="card-label">
                    QUICK ACCESS
                  </p>

                  <h2>
                    What would you like to do?
                  </h2>

                </div>

              </div>


              <div className="quick-grid">

                <button
                  onClick={() => setActivePage("chat")}
                >
                  <span>💬</span>

                  <div>
                    <strong>
                      Ask AI
                    </strong>

                    <small>
                      Ask anything about your career
                    </small>
                  </div>

                  <b>
                    →
                  </b>

                </button>


                <button
                  onClick={() => setActivePage("resume")}
                >
                  <span>📄</span>

                  <div>
                    <strong>
                      Resume
                    </strong>

                    <small>
                      Upload or analyze your resume
                    </small>
                  </div>

                  <b>
                    →
                  </b>

                </button>


                <button
                  onClick={() => setActivePage("jobs")}
                >
                  <span>🎯</span>

                  <div>
                    <strong>
                      Job Match
                    </strong>

                    <small>
                      Check your skill match
                    </small>
                  </div>

                  <b>
                    →
                  </b>

                </button>

              </div>

            </div>

          </section>
        )}


        {/* =================================================
            RESUME PAGE
        ================================================= */}

        {activePage === "resume" && (

          <section className="page-container">

            <div className="page-intro">

              <p className="eyebrow">
                RESUME ANALYSIS
              </p>

              <h2>
                Let your AI Career Agent
                understand your resume.
              </h2>

              <p>
                Upload your PDF resume. The system extracts
                structured information and stores it for
                AI-powered career assistance.
              </p>

            </div>


            <UploadResume />

          </section>
        )}


        {/* =================================================
            CHAT PAGE
        ================================================= */}

        {activePage === "chat" && (

          <section className="page-container chat-page">

            <div className="page-intro">

              <p className="eyebrow">
                PERSONAL AI ASSISTANT
              </p>

              <h2>
                Ask your Career Agent.
              </h2>

              <p>
                Ask about your resume, skills, projects,
                career path or interview preparation.
              </p>

            </div>


            <CareerChat />

          </section>
        )}


        {/* =================================================
    JOB MATCH PAGE
================================================= */}

{activePage === "jobs" && (

  <section className="page-container">

    <JobMatch />

  </section>

)}


        {/* =================================================
    INTERVIEW PAGE
================================================= */}

{activePage === "interview" && (

  <section className="page-container">

    <Interview />

  </section>

)}

      </main>

    </div>
  );
}


export default App;