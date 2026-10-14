import { useState } from "react";
import axios from "axios";


function Interview() {

  const [jobDescription, setJobDescription] = useState("");

  const [sessionId, setSessionId] = useState(null);

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [evaluation, setEvaluation] = useState("");

  const [questionNumber, setQuestionNumber] = useState(0);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  // =====================================================
  // START INTERVIEW
  // =====================================================

  const startInterview = async () => {

    if (!jobDescription.trim()) {

      setError(
        "Please paste the job description first."
      );

      return;
    }

    setLoading(true);
    setError("");
    setEvaluation("");

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/api/interview/start",
        {
          job_description: jobDescription
        }
      );

      if (response.data.error) {

        setError(response.data.error);

        return;
      }

      setSessionId(
        response.data.session_id
      );

      setQuestion(
        response.data.question
      );

      setQuestionNumber(
        response.data.question_number
      );

      setAnswer("");

    } catch (error) {

      console.error(error);

      setError(
        "Unable to start the interview. Make sure the backend is running and your resume has been uploaded."
      );

    } finally {

      setLoading(false);

    }
  };


  // =====================================================
  // SUBMIT ANSWER
  // =====================================================

  const submitAnswer = async () => {

    if (!answer.trim()) {

      setError(
        "Please write your answer first."
      );

      return;
    }

    if (!sessionId) {

      setError(
        "Please start the interview first."
      );

      return;
    }

    setLoading(true);
    setError("");

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/api/interview/answer",
        {
          session_id: sessionId,
          answer: answer
        }
      );

      if (response.data.error) {

        setError(response.data.error);

        return;
      }

      setEvaluation(
        response.data.evaluation
      );

      setQuestion(
        response.data.next_question
      );

      setQuestionNumber(
        response.data.question_number
      );

      setAnswer("");

    } catch (error) {

      console.error(error);

      setError(
        "Unable to evaluate your answer."
      );

    } finally {

      setLoading(false);

    }
  };


  // =====================================================
  // RESET
  // =====================================================

  const resetInterview = () => {

    setJobDescription("");

    setSessionId(null);

    setQuestion("");

    setAnswer("");

    setEvaluation("");

    setQuestionNumber(0);

    setError("");

  };


  // =====================================================
  // INTERVIEW NOT STARTED
  // =====================================================

  if (!sessionId) {

    return (

      <div className="interview-container">

        <div className="interview-start-card">

          <div className="interview-start-header">

            <div>

              <p className="card-label">
                AI INTERVIEWER
              </p>

              <h2>
                Practice your interview
              </h2>

              <p>
                Your AI interviewer will ask
                questions based on your resume
                and the job you are targeting.
              </p>

            </div>

            <div className="interview-icon">
              🎤
            </div>

          </div>


          <label className="interview-label">
            TARGET JOB DESCRIPTION
          </label>


          <textarea
            value={jobDescription}
            onChange={(event) =>
              setJobDescription(event.target.value)
            }
            placeholder="Paste the job description you are preparing for..."
            className="interview-job-input"
          />


          {error && (

            <div className="interview-error">
              {error}
            </div>

          )}


          <button
            className="primary-button"
            onClick={startInterview}
            disabled={loading}
          >

            {loading
              ? "Preparing Interview..."
              : "Start Interview"
            }

            {!loading && <span>→</span>}

          </button>


          <div className="interview-info">

            <div>
              <span>01</span>
              <p>Resume-based questions</p>
            </div>

            <div>
              <span>02</span>
              <p>AI evaluation</p>
            </div>

            <div>
              <span>03</span>
              <p>Adaptive next questions</p>
            </div>

          </div>

        </div>

      </div>

    );
  }


  // =====================================================
  // ACTIVE INTERVIEW
  // =====================================================

  return (

    <div className="interview-container">


      {/* =================================================
          INTERVIEW HEADER
      ================================================= */}

      <div className="interview-session-header">

        <div>

          <p className="card-label">
            LIVE AI INTERVIEW
          </p>

          <h2>
            AI Engineer Interview
          </h2>

        </div>


        <div className="question-counter">

          Question

          <strong>
            {questionNumber}
          </strong>

        </div>

      </div>


      {/* =================================================
          QUESTION
      ================================================= */}

      <div className="question-card">

        <div className="question-avatar">
          ✦
        </div>

        <div>

          <p className="interviewer-name">
            AI Interviewer
          </p>

          <h3>
            {question}
          </h3>

        </div>

      </div>


      {/* =================================================
          ANSWER
      ================================================= */}

      <div className="answer-card">

        <label>
          YOUR ANSWER
        </label>

        <textarea
          value={answer}
          onChange={(event) =>
            setAnswer(event.target.value)
          }
          placeholder="Explain your answer clearly. You can include technical details, examples and your reasoning..."
          className="answer-input"
        />


        {error && (

          <div className="interview-error">
            {error}
          </div>

        )}


        <div className="answer-actions">

          <button
            className="primary-button"
            onClick={submitAnswer}
            disabled={loading}
          >

            {loading
              ? "Evaluating..."
              : "Submit Answer"
            }

            {!loading && <span>→</span>}

          </button>


          <button
            className="clear-button"
            onClick={resetInterview}
          >
            End Interview
          </button>

        </div>

      </div>


      {/* =================================================
          EVALUATION
      ================================================= */}

      {evaluation && (

        <div className="evaluation-card">

          <div className="evaluation-header">

            <div className="evaluation-icon">
              ✓
            </div>

            <div>

              <p className="card-label">
                AI FEEDBACK
              </p>

              <h3>
                Interview Evaluation
              </h3>

            </div>

          </div>


          <div className="evaluation-content">

            {evaluation}

          </div>

        </div>

      )}

    </div>

  );
}


export default Interview;