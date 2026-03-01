# CareerInk — AI-Powered IT Career Transition Platform

> From CV to personalized career roadmap in 30–45 minutes.

## 🚀 Live Demo

**👉 [https://q7fdu7oc.run.complete.dev](https://q7fdu7oc.run.complete.dev)**

---

## Screenshots

### Landing Page
![CareerInk Landing Page](docs/screenshot_1_landing.png)

### Step 1 — CV Analysis (Agent 1)
![CV Input](docs/screenshot_2_cv.png)

### Step 2 — Psychological Assessment (Agent 1)
![48-Question Assessment](docs/screenshot_3_assessment.png)

---

## Overview

CareerInk is a 2-agent AI system that helps IT professionals navigate internal career transitions through personalized assessment and career path discovery.

---

## How It Works

| Step | Agent | Description |
|---|---|---|
| 1 | Agent 1 | Paste your CV → NLP skill extraction |
| 2 | Agent 1 | 48-question psychological assessment (Big Five, Holland Code, IT Work Preferences) |
| 3 | Agent 2 | Weighted career matching algorithm → 3–5 ranked career cards |
| 4 | Agent 2 | Downloadable PDF Career Recommendations Report |

---

## Tech Stack

- **Backend:** Python 3.12 · FastAPI · ReportLab (PDF)
- **Frontend:** Vanilla HTML/CSS/JS
- **AI:** Deploy AI (Claude) for career justification sentences
- **Data:** 17 pre-extracted IT career profiles (JSON)

---

## Project Structure

```
careerink/
├── backend/
│   ├── main.py                  # FastAPI app + all routes
│   ├── models.py                # Pydantic request/response schemas
│   ├── agents/
│   │   ├── agent1.py            # CV analysis + assessment scoring
│   │   └── agent2.py            # Career matching + PDF generation
│   ├── data/
│   │   ├── questions.py         # 48 assessment questions
│   │   └── career_profiles.json # Pre-extracted IT career profiles
│   └── utils/
│       └── deploy_ai.py         # Deploy AI / Claude API client
├── frontend/
│   └── index.html               # Full single-page frontend
├── docs/                        # Screenshots
├── requirements.txt
└── .gitignore
```

---

## Setup & Installation

### Prerequisites

- Python 3.10 or higher
- pip3
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Thomaswu32/careerink.git
cd careerink
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

Create a `.env` file in the project root for Claude-powered justification sentences:

```env
CLIENT_ID=your_deploy_ai_client_id
CLIENT_SECRET=your_deploy_ai_client_secret
ORG_ID=your_org_id
AUTH_URL=https://api-auth.dev.deploy.ai/oauth2/token
API_URL=https://core-api.dev.deploy.ai
```

> Without these, the app automatically falls back to template-based justifications — all other features work normally.

### 5. Run the Application

```bash
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Open in Browser

```
http://localhost:8000
```

---

## Running in Production (Background)

```bash
nohup python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 > logs/server.log 2>&1 &
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/cv/analyze` | Extract skills from CV text (min 500 chars) |
| `GET` | `/api/assessment/questions` | Get 48 randomized assessment questions |
| `POST` | `/api/assessment/submit` | Score assessment → build user profile |
| `POST` | `/api/careers/match` | Run matching algorithm → return career cards |
| `POST` | `/api/report/download` | Generate PDF career report |
| `POST` | `/api/optin` | Capture email opt-in |

---

## Matching Algorithm

| Component | Weight |
|---|---|
| Hard Skills Match | 40% |
| Personality Trait Match (Big Five) | 25% |
| Work Style & Values Match (Holland Code) | 20% |
| Experience & Seniority Fit | 15% |

- **Viability filter:** Skills Score ≥ 35 AND Final Score ≥ 50
- **Diversity constraint:** Max 2 recommendations per role family

---

## Psychological Frameworks

- **Big Five:** Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism (20 questions)
- **Holland Code RIASEC:** Realistic, Investigative, Artistic, Social, Enterprising, Conventional (18 questions)
- **IT Work Preferences:** Collaboration, Problem-Solving, Leadership Growth, Dynamic Environment (10 questions)

---

Built for the **Team Jobonauts AI Hackathon** · 2026
