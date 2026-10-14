from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.resume import router as resume_router
from app.routes.chat import router as chat_router
from app.routes.interview import router as interview_router
from app.routes.job_match import router as job_match_router


app = FastAPI(
    title="AI Career Agent",
    description="AI-powered career assistant",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# ROUTES
# =========================================================

app.include_router(
    resume_router
)

app.include_router(
    chat_router
)

app.include_router(
    interview_router
)
app.include_router(
    job_match_router
    )


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "AI Career Agent is running"
    }