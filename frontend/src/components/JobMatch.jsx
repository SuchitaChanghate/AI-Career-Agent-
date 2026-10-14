import { useState } from "react";
import axios from "axios";


function JobMatch() {

  const [jobDescription, setJobDescription] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  // =====================================================
  // ANALYZE JOB
  // =====================================================

  const analyzeJob = async () => {

    if (!jobDescription.trim()) {

      setError("Please paste a job description first.");

      return;
    }


    setLoading(true);

    setError("");

    setResult(null);


    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/api/job-match/",
        {
          job_description: jobDescription
        }
      );


      if (response.data.error) {

        setError(response.data.error);

        return;
      }


      setResult(response.data);

    } catch (error) {

      console.error(error);

      setError(
        "Unable to analyze the job. Make sure the backend is running and your resume has been uploaded."
      );

    } finally {

      setLoading(false);

    }
  };


  // =====================================================
  // CLEAR
  // =====================================================

  const clearAnalysis = () => {

    setJobDescription("");

    setResult(null);

    setError("");

  };


  // =====================================================
  // RENDER
  // =====================================================

  return (

    <div className="job-match-container">


      {/* =================================================
          INPUT CARD
      ================================================= */}

      <div className="job-input-card">

        <div className="job-input-header">

          <div>

            <p className="card-label">
              JOB INTELLIGENCE
            </p>

            <h2>
              Analyze a Job
            </h2>

            <p>
              Paste a job description and compare it
              with the skills demonstrated in your resume.
            </p>

          </div>

          <div className="job-icon">
            🎯
          </div>

        </div>


        <textarea
          value={jobDescription}
          onChange={(event) =>
            setJobDescription(event.target.value)
          }
          placeholder="Paste the complete job description here..."
          className="job-description-input"
        />


        <div className="job-actions">

          <button
            className="primary-button"
            onClick={analyzeJob}
            disabled={loading}
          >

            {loading
              ? "Analyzing..."
              : "Analyze Job"
            }

            {!loading && <span>→</span>}

          </button>


          {result && (

            <button
              className="clear-button"
              onClick={clearAnalysis}
            >
              Clear
            </button>

          )}

        </div>


        {error && (

          <div className="job-error">
            {error}
          </div>

        )}

      </div>


      {/* =================================================
          RESULTS
      ================================================= */}

      {result && (

        <div className="job-results">


          {/* =============================================
              MATCH SCORE
          ============================================= */}

          <div className="match-score-card">

            <div>

              <p className="card-label">
                AI MATCH ANALYSIS
              </p>

              <h2>
                Your Resume Match
              </h2>

              <p>
                This score estimates how closely the
                skills demonstrated in your resume align
                with this job description.
              </p>

            </div>


            <div className="match-score">

              <strong>
                {result.match_result?.match_score ?? 0}
              </strong>

              <span>
                %
              </span>

            </div>

          </div>


          {/* =============================================
              JOB ANALYSIS
          ============================================= */}

          <div className="result-card">

            <div className="result-card-header">

              <div>

                <p className="card-label">
                  JOB ANALYSIS
                </p>

                <h3>
                  What this role requires
                </h3>

              </div>

            </div>


            <div className="job-analysis-text">

              {typeof result.job_analysis === "string"
                ? result.job_analysis
                : JSON.stringify(
                    result.job_analysis,
                    null,
                    2
                  )
              }

            </div>

          </div>


          {/* =============================================
              MATCH GRID
          ============================================= */}

          <div className="match-grid">


            {/* Strong Matches */}

            <div className="match-list-card strong">

              <div className="match-list-title">

                <span>
                  ✓
                </span>

                <div>

                  <h3>
                    Strong Matches
                  </h3>

                  <p>
                    Skills clearly demonstrated
                    in your resume.
                  </p>

                </div>

              </div>


              <div className="skill-list">

                {(
                  result.match_result?.strong_matches
                  || []
                ).map((skill, index) => (

                  <div
                    className="skill-item"
                    key={index}
                  >

                    <span>
                      ✓
                    </span>

                    {skill}

                  </div>

                ))}

              </div>

            </div>


            {/* Partial Matches */}

            <div className="match-list-card partial">

              <div className="match-list-title">

                <span>
                  ◐
                </span>

                <div>

                  <h3>
                    Partial Matches
                  </h3>

                  <p>
                    Related but incomplete skills.
                  </p>

                </div>

              </div>


              <div className="skill-list">

                {(
                  result.match_result?.partial_matches
                  || []
                ).map((skill, index) => (

                  <div
                    className="skill-item"
                    key={index}
                  >

                    <span>
                      ◐
                    </span>

                    {skill}

                  </div>

                ))}

              </div>

            </div>


            {/* Missing Skills */}

            <div className="match-list-card missing">

              <div className="match-list-title">

                <span>
                  !
                </span>

                <div>

                  <h3>
                    Missing Skills
                  </h3>

                  <p>
                    Important requirements not
                    demonstrated in your resume.
                  </p>

                </div>

              </div>


              <div className="skill-list">

                {(
                  result.match_result?.missing_skills
                  || []
                ).map((skill, index) => (

                  <div
                    className="skill-item"
                    key={index}
                  >

                    <span>
                      !
                    </span>

                    {skill}

                  </div>

                ))}

              </div>

            </div>

          </div>


          {/* =============================================
              RECOMMENDATIONS
          ============================================= */}

          <div className="recommendation-card">

            <div className="recommendation-header">

              <div className="recommendation-icon">
                ✦
              </div>

              <div>

                <p className="card-label">
                  AI CAREER ADVISOR
                </p>

                <h3>
                  What should you improve?
                </h3>

              </div>

            </div>


            <div className="recommendation-list">

              {(
                result.match_result?.recommendations
                || []
              ).map((recommendation, index) => (

                <div
                  className="recommendation-item"
                  key={index}
                >

                  <span>
                    {index + 1}
                  </span>

                  <p>
                    {recommendation}
                  </p>

                </div>

              ))}

            </div>

          </div>


        </div>

      )}

    </div>
  );
}


export default JobMatch;