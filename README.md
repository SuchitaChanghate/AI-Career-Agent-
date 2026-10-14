# AI Career Agent

An AI-powered career assistant designed to help candidates analyze resumes, understand job requirements, identify skill gaps, and prepare for interviews using Large Language Models (LLMs) and prompt engineering.

> **Project status:** In development.

## Overview

AI Career Agent aims to simplify job preparation through AI-assisted workflows.

- **Resume Analysis:** Extract and organize candidate information from resumes.
- **Job Description Analysis:** Identify important skills and role requirements.
- **Skill Matching:** Compare candidate skills with job requirements.
- **Interview Preparation:** Generate relevant interview questions.
- **Interview Practice:** Support answer evaluation and follow-up questions as features are developed.

## Technology Stack

| Component | Technologies |
|---|---|
| Programming Language | Python |
| Backend | FastAPI, REST APIs |
| Frontend | React, JavaScript, Vite |
| AI | LLM APIs, Prompt Engineering |
| Tools | Git, GitHub, Uvicorn, npm |

## Architecture

The application separates the frontend interface from the backend API.

- **Frontend:** Provides the user interface for resume uploads and career assistance.
- **Backend:** Handles API requests and application logic.
- **AI Layer:** Supports LLM-based analysis and generation workflows.

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- Required LLM API key

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/SuchitaChanghate/AI-Career-Agent-.git
cd AI-Career-Agent-
\`\`\`

### 2. Start the backend

\`\`\`bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
\`\`\`

Backend URL: `http://127.0.0.1:8000`

API documentation, if enabled: `http://127.0.0.1:8000/docs`

### 3. Start the frontend

Open a second terminal:

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Open the local URL displayed by Vite in the terminal.

### 4. Configure environment variables

Add the required LLM API credentials to your local environment configuration. Follow the variable names expected by your application.

**Never commit API keys, passwords, or secrets to GitHub.**

## Planned Improvements

- Resume parsing and structured analysis
- Job description and skill matching
- Personalized interview question generation
- Interview answer evaluation
- Improved error handling and testing

## Author

**Suchita Changhate**

[GitHub Profile](https://github.com/SuchitaChanghate)

---

*Exploring practical applications of Generative AI to build smarter career preparation tools.*
