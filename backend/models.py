"""Pydantic models for CareerInk API request/response schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ─── Agent 1 Models ──────────────────────────────────────────────────────────

class CVAnalyzeRequest(BaseModel):
    cv_text: str = Field(..., min_length=500, description="CV content (min 500 characters)")

class SkillsResponse(BaseModel):
    technical_skills: List[str]
    soft_skills: List[str]
    experience_years: int
    current_role: str
    education_level: str

class AssessmentAnswer(BaseModel):
    question_id: int
    answer: int  # 1–5 Likert scale

class AssessmentSubmitRequest(BaseModel):
    cv_text: str
    confirmed_hard_skills: List[str]
    confirmed_soft_skills: List[str]
    experience_years: int
    current_role: str
    education_level: str
    answers: List[AssessmentAnswer]

class BigFiveScores(BaseModel):
    openness: str        # Low / Moderate / High
    conscientiousness: str
    extraversion: str
    agreeableness: str
    neuroticism: str

class HollandScores(BaseModel):
    realistic: str
    investigative: str
    artistic: str
    social: str
    enterprising: str
    conventional: str

class WorkPreferences(BaseModel):
    collaboration: str
    problem_solving: str
    leadership_growth: str
    dynamic_environment: str

class UserProfile(BaseModel):
    hard_skills: List[str]
    soft_skills_confirmed: List[str]
    experience_years: int
    current_role: str
    education_level: str
    personality_traits: BigFiveScores
    work_style: HollandScores
    work_values: WorkPreferences
    # Numeric raw scores for display
    bigfive_raw: Dict[str, int]
    holland_raw: Dict[str, int]
    work_prefs_raw: Dict[str, int]


# ─── Agent 2 Models ──────────────────────────────────────────────────────────

class CareerMatchCard(BaseModel):
    career_id: str
    role_name: str
    role_family: str
    final_score: float
    skills_score: float
    traits_score: float
    style_score: float
    experience_score: float
    top_matched_skills: List[str]
    top_gap_skills: List[str]
    justification: str
    avg_ramp_up_months: int
    salary_range: str
    growth_trajectory: str
    description_summary: str

class CareerMatchResponse(BaseModel):
    user_profile: UserProfile
    career_matches: List[CareerMatchCard]

class PDFReportRequest(BaseModel):
    user_profile: UserProfile
    career_matches: List[CareerMatchCard]
    user_name: Optional[str] = "Candidate"
    assessment_date: Optional[str] = ""

class EmailOptInRequest(BaseModel):
    email: str
    user_name: Optional[str] = ""


# ─── Question Models ─────────────────────────────────────────────────────────

class Question(BaseModel):
    id: int
    framework: str
    text: str
    section: str
    trait: str
    reverse: bool
