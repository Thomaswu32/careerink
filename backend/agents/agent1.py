"""
Agent 1 — Profile Builder
- CV text analysis: NLP-based skill extraction from skill taxonomy
- Psychological assessment scoring: Big Five, Holland Code, IT Work Preferences
- User profile generation combining both data sources
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# ─── Skill Taxonomy (core list for matching) ─────────────────────────────────
SKILL_TAXONOMY: List[str] = [
    # Programming Languages
    "Python", "JavaScript", "TypeScript", "SQL", "Java", "C++", "C#", "C", "Go",
    "Rust", "Kotlin", "Swift", "Scala", "R", "Bash", "Shell Scripting", "PowerShell",
    "Dart", "CUDA", "Solidity", "Ruby", "PHP", "MATLAB",
    # Web Frameworks
    "React", "React.js", "Next.js", "Node.js", "Vue.js", "Angular", "FastAPI",
    "Django", "Flask", "Express.js", "Spring Boot", "GraphQL", "gRPC", "REST API",
    "Svelte", "Tailwind CSS", "WebSockets", "React Native", "Flutter", "Redux",
    # Cloud & Infra
    "AWS", "Azure", "GCP", "Google Cloud", "Kubernetes", "Docker", "Terraform",
    "Ansible", "Helm", "ArgoCD", "CI/CD", "GitHub Actions", "Jenkins", "GitLab CI",
    "AWS SageMaker", "Google Vertex AI", "Azure Machine Learning",
    "AWS Lambda", "EC2", "S3",
    # Data
    "Apache Spark", "Hadoop", "Kafka", "Airflow", "dbt", "Snowflake", "BigQuery",
    "Redshift", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "Cassandra", "DynamoDB", "Databricks", "Power BI", "Tableau", "Looker",
    "Pandas", "NumPy", "Matplotlib",
    # ML/AI
    "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "Hugging Face", "LangChain",
    "MLflow", "Kubeflow", "Weights & Biases", "MLOps", "RAG", "LLM",
    "Transformers", "NLP", "Computer Vision", "OpenAI API",
    # Security
    "SIEM", "Penetration Testing", "Vulnerability Assessment", "OWASP",
    "ISO 27001", "SOC 2", "Zero Trust", "OAuth", "SAML", "JWT", "NIST",
    # DevOps / Observability
    "Prometheus", "Grafana", "Datadog", "ELK Stack", "OpenTelemetry",
    "Incident Management", "Chaos Engineering", "Istio", "Nginx",
    # Design
    "Figma", "Sketch", "Adobe XD", "Prototyping", "User Research",
    "Usability Testing", "Design Systems", "A/B Testing", "Wireframing",
    # Methodologies
    "Agile", "Scrum", "Kanban", "SAFe", "ITIL", "PMP", "Design Thinking",
    "OKRs", "Product Roadmap", "Stakeholder Management", "JIRA", "Confluence",
    # Management / BA
    "People Management", "Hiring", "Risk Management", "Strategic Planning",
    "Business Analysis", "Requirements Analysis", "Excel", "Git", "GitHub",
]

SKILL_ALIASES: Dict[str, str] = {
    "k8s": "Kubernetes", "node": "Node.js", "react native": "React Native",
    "ml": "Machine Learning", "vertex ai": "Google Vertex AI",
    "sagemaker": "AWS SageMaker", "typescript": "TypeScript",
    "javascript": "JavaScript", "golang": "Go", "shell": "Bash",
    "postgres": "PostgreSQL", "elastic": "Elasticsearch",
    "openai": "OpenAI API", "langchain": "LangChain",
    "power bi": "Power BI", "scikit": "Scikit-learn",
    "huggingface": "Hugging Face",
}

SOFT_SKILLS_KEYWORDS: Dict[str, List[str]] = {
    "Leadership": ["led", "lead", "manager", "managed", "directed", "head of"],
    "Communication": ["communicated", "presented", "stakeholder", "liaison"],
    "Problem Solving": ["resolved", "diagnosed", "optimized", "improved", "solved"],
    "Teamwork": ["collaborated", "cross-functional", "team", "worked with"],
    "Project Management": ["delivered", "launched", "coordinated", "project"],
    "Mentoring": ["mentored", "coached", "trained", "onboarded"],
    "Analytical Thinking": ["analyzed", "research", "data-driven", "metrics"],
    "Adaptability": ["adapted", "pivot", "transitioned", "flexible"],
}


def extract_skills_from_cv(cv_text: str) -> Dict[str, Any]:
    """
    Parse CV text and return structured skills using the skill taxonomy.
    Returns technical skills, soft skills, experience years, current role, education level.
    """
    text_lower = cv_text.lower()

    # ── Technical Skills ─────────────────────────────────────────────────────
    technical = []
    for skill in SKILL_TAXONOMY:
        pattern = re.compile(r'\b' + re.escape(skill.lower()) + r'\b')
        if pattern.search(text_lower):
            technical.append(skill)

    # Check aliases
    for alias, canonical in SKILL_ALIASES.items():
        if re.search(r'\b' + re.escape(alias) + r'\b', text_lower):
            if canonical not in technical:
                technical.append(canonical)

    # De-duplicate preserving order
    technical = list(dict.fromkeys(technical))

    # ── Soft Skills ──────────────────────────────────────────────────────────
    soft = []
    for skill_name, keywords in SOFT_SKILLS_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            soft.append(skill_name)

    # ── Experience Years ─────────────────────────────────────────────────────
    experience_years = 0
    year_matches = re.findall(r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)', text_lower)
    if year_matches:
        experience_years = max(int(y) for y in year_matches)
    else:
        # Count year spans: e.g., "2018 – 2023"
        spans = re.findall(r'(20\d{2})\s*[–\-—]\s*(20\d{2}|present|current)', text_lower)
        total = 0
        import datetime
        current_year = datetime.datetime.now().year
        for start, end in spans:
            end_y = current_year if end in ("present", "current") else int(end)
            total += max(0, end_y - int(start))
        experience_years = min(total, 30)

    # ── Current Role ─────────────────────────────────────────────────────────
    current_role = "IT Professional"
    role_patterns = [
        r'(?:senior|lead|principal|staff|junior|mid)?\s*'
        r'(?:software|data|cloud|devops|platform|ml|ai|security|full.stack|backend|frontend|'
        r'product|project|systems?|site reliability|solutions?)\s*'
        r'(?:engineer|developer|architect|manager|analyst|scientist|designer|specialist)',
    ]
    for pattern in role_patterns:
        m = re.search(pattern, text_lower)
        if m:
            current_role = m.group(0).strip().title()
            break

    # ── Education Level ──────────────────────────────────────────────────────
    education_level = "Bachelor"
    if any(k in text_lower for k in ["phd", "ph.d", "doctorate", "doctoral"]):
        education_level = "PhD"
    elif any(k in text_lower for k in ["master", "msc", "m.sc", "mba", "m.eng"]):
        education_level = "Master"
    elif any(k in text_lower for k in ["bachelor", "b.sc", "bsc", "b.eng", "b.a."]):
        education_level = "Bachelor"
    elif any(k in text_lower for k in ["associate", "diploma", "bootcamp", "certificate"]):
        education_level = "Associate"

    return {
        "technical_skills": technical[:30],  # top 30 matched
        "soft_skills": soft,
        "experience_years": experience_years,
        "current_role": current_role,
        "education_level": education_level,
    }


# ─── Scoring Helpers ─────────────────────────────────────────────────────────

def _level(score: int, low_max: int, mod_max: int) -> str:
    """Map raw score to Low / Moderate / High."""
    if score <= low_max:
        return "Low"
    elif score <= mod_max:
        return "Moderate"
    return "High"


def score_assessment(answers: List[Dict]) -> Dict[str, Any]:
    """
    Score the 48-question assessment.

    answers: list of {question_id: int, answer: int (1–5)}

    Returns:
        bigfive_raw    – dict trait → raw sum (4–20)
        bigfive        – dict trait → Low/Moderate/High
        holland_raw    – dict type → raw sum (3–15)
        holland        – dict type → Low/Moderate/High
        work_prefs_raw – dict pref → raw sum
        work_prefs     – dict pref → Low/Moderate/High
    """
    from backend.data.questions import QUESTIONS

    # Build id→question lookup
    q_map = {q["id"]: q for q in QUESTIONS}

    # Accumulators
    bigfive_sums: Dict[str, int] = {
        "openness": 0, "conscientiousness": 0,
        "extraversion": 0, "agreeableness": 0, "neuroticism": 0
    }
    holland_sums: Dict[str, int] = {
        "realistic": 0, "investigative": 0, "artistic": 0,
        "social": 0, "enterprising": 0, "conventional": 0
    }
    work_sums: Dict[str, int] = {
        "collaboration": 0, "problem_solving": 0,
        "leadership_growth": 0, "dynamic_environment": 0
    }

    for ans in answers:
        qid  = ans["question_id"]
        val  = ans["answer"]  # 1–5
        q    = q_map.get(qid)
        if not q:
            continue

        # Reverse score if needed (Neuroticism stability questions)
        scored = (6 - val) if q["reverse"] else val

        if q["section"] == "bigfive":
            bigfive_sums[q["trait"]] += scored
        elif q["section"] == "holland":
            holland_sums[q["trait"]] += scored
        elif q["section"] == "work_prefs":
            work_sums[q["trait"]] += scored

    # ── Big Five: 4–20, thresholds 4–9 = Low, 10–14 = Mod, 15–20 = High ──
    bigfive_levels = {
        trait: _level(score, 9, 14)
        for trait, score in bigfive_sums.items()
    }

    # ── Holland Code: 3–15, rank-based labelling ───────────────────────────
    sorted_holland = sorted(holland_sums.items(), key=lambda x: x[1], reverse=True)
    holland_levels: Dict[str, str] = {}
    for rank, (trait, _) in enumerate(sorted_holland):
        if rank < 3:
            holland_levels[trait] = "High"
        elif rank < 5:
            holland_levels[trait] = "Moderate"
        else:
            holland_levels[trait] = "Low"

    # ── IT Work Preferences ────────────────────────────────────────────────
    # Collaboration / Problem-Solving: 3–15 → Low≤7, Mod≤10, High>10
    # Leadership Growth / Dynamic Env: 2–10 → Low≤4, Mod≤6, High>6
    work_levels = {
        "collaboration":      _level(work_sums["collaboration"],      7, 10),
        "problem_solving":    _level(work_sums["problem_solving"],     7, 10),
        "leadership_growth":  _level(work_sums["leadership_growth"],   4,  6),
        "dynamic_environment":_level(work_sums["dynamic_environment"], 4,  6),
    }

    return {
        "bigfive_raw":    bigfive_sums,
        "bigfive":        bigfive_levels,
        "holland_raw":    holland_sums,
        "holland":        holland_levels,
        "work_prefs_raw": work_sums,
        "work_prefs":     work_levels,
    }


def build_user_profile(
    cv_data: Dict[str, Any],
    assessment: Dict[str, Any],
    confirmed_hard_skills: List[str],
    confirmed_soft_skills: List[str],
) -> Dict[str, Any]:
    """Combine CV data and assessment scores into a complete User Profile."""
    return {
        "hard_skills":          confirmed_hard_skills,
        "soft_skills_confirmed": confirmed_soft_skills,
        "experience_years":     cv_data["experience_years"],
        "current_role":         cv_data["current_role"],
        "education_level":      cv_data["education_level"],
        "personality_traits":   assessment["bigfive"],
        "work_style":           assessment["holland"],
        "work_values":          assessment["work_prefs"],
        "bigfive_raw":          assessment["bigfive_raw"],
        "holland_raw":          assessment["holland_raw"],
        "work_prefs_raw":       assessment["work_prefs_raw"],
    }
