"""
CareerInk — FastAPI Backend
Serves Agent 1 (Assessment) and Agent 2 (Career Discovery + PDF) APIs.
"""

import logging
import os
import random
from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles

from backend.models import (
    CVAnalyzeRequest, SkillsResponse,
    AssessmentSubmitRequest, UserProfile,
    CareerMatchResponse, PDFReportRequest,
    EmailOptInRequest, Question,
)
from backend.agents.agent1 import extract_skills_from_cv, score_assessment, build_user_profile
from backend.agents.agent2 import match_careers, generate_pdf_report
from backend.data.questions import QUESTIONS

# ─── Logging ─────────────────────────────────────────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "careerink.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CareerInk API",
    description="AI-powered IT career transition platform",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Health ───────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "service": "CareerInk API v2.0"}


# ─── Agent 1: Assessment ──────────────────────────────────────────────────────

@app.post("/api/cv/analyze")
def analyze_cv(req: CVAnalyzeRequest):
    """
    Agent 1 Step 1 — Parse CV text and extract skills, experience, and education.
    CV must be at least 500 characters.
    """
    logger.info("CV analysis requested")
    if len(req.cv_text) < 500:
        raise HTTPException(status_code=400, detail="CV text must be at least 500 characters.")

    result = extract_skills_from_cv(req.cv_text)
    logger.info(f"CV analyzed: {len(result['technical_skills'])} technical skills extracted")
    return {
        "technical_skills":  result["technical_skills"],
        "soft_skills":        result["soft_skills"],
        "experience_years":   result["experience_years"],
        "current_role":       result["current_role"],
        "education_level":    result["education_level"],
    }


@app.get("/api/assessment/questions")
def get_questions():
    """
    Return all 48 assessment questions in randomized order.
    Randomization is seeded per-request so the frontend can cache.
    """
    questions = list(QUESTIONS)  # copy
    random.shuffle(questions)
    return {"questions": questions, "total": len(questions)}


@app.post("/api/assessment/submit")
def submit_assessment(req: AssessmentSubmitRequest):
    """
    Agent 1 Step 2 — Score the 48-question assessment and build the complete user profile.
    """
    logger.info(f"Assessment submitted: {len(req.answers)} answers")

    if len(req.answers) < 48:
        raise HTTPException(
            status_code=400,
            detail=f"Expected 48 answers, received {len(req.answers)}."
        )

    answers_dicts = [{"question_id": a.question_id, "answer": a.answer} for a in req.answers]
    assessment = score_assessment(answers_dicts)

    cv_data = {
        "technical_skills": req.confirmed_hard_skills,
        "soft_skills":       req.confirmed_soft_skills,
        "experience_years":  req.experience_years,
        "current_role":      req.current_role,
        "education_level":   req.education_level,
    }

    profile = build_user_profile(
        cv_data=cv_data,
        assessment=assessment,
        confirmed_hard_skills=req.confirmed_hard_skills,
        confirmed_soft_skills=req.confirmed_soft_skills,
    )

    logger.info(f"Profile built for: {profile['current_role']}")
    return profile


# ─── Agent 2: Career Discovery ────────────────────────────────────────────────

@app.post("/api/careers/match")
def match_career_paths(profile: UserProfile):
    """
    Agent 2 Step 1 — Run the weighted matching algorithm and return 3–5 career cards.
    """
    logger.info(f"Career matching for profile: {profile.current_role}, {profile.experience_years}y exp")

    profile_dict = profile.model_dump()
    # Convert nested models to plain dicts
    profile_dict["personality_traits"] = profile.personality_traits.model_dump()
    profile_dict["work_style"]         = profile.work_style.model_dump()
    profile_dict["work_values"]        = profile.work_values.model_dump()

    matches = match_careers(profile_dict)

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No suitable career matches found. Please ensure your CV includes enough skills."
        )

    logger.info(f"Found {len(matches)} career matches")
    return {"career_matches": matches, "count": len(matches)}


@app.post("/api/report/download")
def download_pdf_report(req: PDFReportRequest):
    """
    Agent 2 Step 2 — Generate and return a PDF Career Recommendations Report.
    """
    logger.info(f"PDF report requested for: {req.user_name}")

    profile_dict = req.user_profile.model_dump()
    profile_dict["personality_traits"] = req.user_profile.personality_traits.model_dump()
    profile_dict["work_style"]         = req.user_profile.work_style.model_dump()
    profile_dict["work_values"]        = req.user_profile.work_values.model_dump()

    matches_list = [cm.model_dump() for cm in req.career_matches]

    try:
        pdf_bytes = generate_pdf_report(
            user_profile   = profile_dict,
            career_matches = matches_list,
            user_name      = req.user_name or "Candidate",
            assessment_date= req.assessment_date or date.today().strftime("%B %d, %Y"),
        )
    except Exception as e:
        logger.error(f"PDF generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    safe_name = (req.user_name or "Candidate").replace(" ", "_")
    today_str  = date.today().strftime("%Y%m%d")
    filename   = f"CareerInk_Career_Report_{safe_name}_{today_str}.pdf"

    return Response(
        content    = pdf_bytes,
        media_type = "application/pdf",
        headers    = {"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/optin")
def email_optin(req: EmailOptInRequest):
    """Capture post-MVP email opt-in for Skills Gap Analysis notification."""
    logger.info(f"Email opt-in captured: {req.email}")
    # In production: persist to database
    return {"status": "success", "message": "You're on the list! We'll notify you when Skills Gap Analysis launches."}


# ─── Serve Frontend ───────────────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "CareerInk API is running. Frontend not found."}

# Mount static files (JS, CSS, assets)
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
