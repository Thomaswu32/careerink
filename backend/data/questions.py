"""
48-question psychological assessment for CareerInk
Covers Big Five Personality, Holland Code RIASEC, and IT Work Preferences.
"""

QUESTIONS = [
    # ── Big Five — Openness (Q1–4) ──────────────────────────────────────────
    {
        "id": 1,
        "framework": "Big Five — Openness",
        "text": "I enjoy exploring new technologies and methodologies, even if they're unproven.",
        "section": "bigfive",
        "trait": "openness",
        "reverse": False
    },
    {
        "id": 2,
        "framework": "Big Five — Openness",
        "text": "I prefer working on innovative projects rather than maintaining existing systems.",
        "section": "bigfive",
        "trait": "openness",
        "reverse": False
    },
    {
        "id": 3,
        "framework": "Big Five — Openness",
        "text": "I like brainstorming creative solutions to complex business problems.",
        "section": "bigfive",
        "trait": "openness",
        "reverse": False
    },
    {
        "id": 4,
        "framework": "Big Five — Openness",
        "text": "I'm comfortable with ambiguous requirements and changing project scope.",
        "section": "bigfive",
        "trait": "openness",
        "reverse": False
    },
    # ── Big Five — Conscientiousness (Q5–8) ─────────────────────────────────
    {
        "id": 5,
        "framework": "Big Five — Conscientiousness",
        "text": "I naturally create detailed plans and follow them systematically.",
        "section": "bigfive",
        "trait": "conscientiousness",
        "reverse": False
    },
    {
        "id": 6,
        "framework": "Big Five — Conscientiousness",
        "text": "I ensure all stakeholders are aligned before moving forward with decisions.",
        "section": "bigfive",
        "trait": "conscientiousness",
        "reverse": False
    },
    {
        "id": 7,
        "framework": "Big Five — Conscientiousness",
        "text": "I consistently meet deadlines and deliverables without constant reminders.",
        "section": "bigfive",
        "trait": "conscientiousness",
        "reverse": False
    },
    {
        "id": 8,
        "framework": "Big Five — Conscientiousness",
        "text": "I document processes and decisions thoroughly for future reference.",
        "section": "bigfive",
        "trait": "conscientiousness",
        "reverse": False
    },
    # ── Big Five — Extraversion (Q9–12) ─────────────────────────────────────
    {
        "id": 9,
        "framework": "Big Five — Extraversion",
        "text": "I energize when facilitating meetings and leading team discussions.",
        "section": "bigfive",
        "trait": "extraversion",
        "reverse": False
    },
    {
        "id": 10,
        "framework": "Big Five — Extraversion",
        "text": "I prefer collaborative problem-solving over working alone.",
        "section": "bigfive",
        "trait": "extraversion",
        "reverse": False
    },
    {
        "id": 11,
        "framework": "Big Five — Extraversion",
        "text": "I enjoy presenting ideas to stakeholders and senior management.",
        "section": "bigfive",
        "trait": "extraversion",
        "reverse": False
    },
    {
        "id": 12,
        "framework": "Big Five — Extraversion",
        "text": "I'm comfortable being the primary point of contact for external clients.",
        "section": "bigfive",
        "trait": "extraversion",
        "reverse": False
    },
    # ── Big Five — Agreeableness (Q13–16) ───────────────────────────────────
    {
        "id": 13,
        "framework": "Big Five — Agreeableness",
        "text": "I prioritize team harmony when resolving conflicts between team members.",
        "section": "bigfive",
        "trait": "agreeableness",
        "reverse": False
    },
    {
        "id": 14,
        "framework": "Big Five — Agreeableness",
        "text": "I consider multiple perspectives before making decisions that affect others.",
        "section": "bigfive",
        "trait": "agreeableness",
        "reverse": False
    },
    {
        "id": 15,
        "framework": "Big Five — Agreeableness",
        "text": "I'm willing to compromise on my preferred approach for team consensus.",
        "section": "bigfive",
        "trait": "agreeableness",
        "reverse": False
    },
    {
        "id": 16,
        "framework": "Big Five — Agreeableness",
        "text": "I focus on building trust and rapport with both technical and business stakeholders.",
        "section": "bigfive",
        "trait": "agreeableness",
        "reverse": False
    },
    # ── Big Five — Neuroticism (Q17–20, reverse-scored) ─────────────────────
    {
        "id": 17,
        "framework": "Big Five — Emotional Stability",
        "text": "I remain calm when projects face unexpected technical or business challenges.",
        "section": "bigfive",
        "trait": "neuroticism",
        "reverse": True
    },
    {
        "id": 18,
        "framework": "Big Five — Emotional Stability",
        "text": "I handle criticism of my work or decisions constructively.",
        "section": "bigfive",
        "trait": "neuroticism",
        "reverse": True
    },
    {
        "id": 19,
        "framework": "Big Five — Emotional Stability",
        "text": "I maintain focus during high-pressure situations like critical releases.",
        "section": "bigfive",
        "trait": "neuroticism",
        "reverse": True
    },
    {
        "id": 20,
        "framework": "Big Five — Emotional Stability",
        "text": "I adapt well when priorities shift due to business or market changes.",
        "section": "bigfive",
        "trait": "neuroticism",
        "reverse": True
    },
    # ── Holland Code — Realistic (Q21–23) ────────────────────────────────────
    {
        "id": 21,
        "framework": "Holland Code — Realistic",
        "text": "I enjoy hands-on problem-solving with systems, code, or technical infrastructure.",
        "section": "holland",
        "trait": "realistic",
        "reverse": False
    },
    {
        "id": 22,
        "framework": "Holland Code — Realistic",
        "text": "I prefer working with concrete data and measurable outcomes.",
        "section": "holland",
        "trait": "realistic",
        "reverse": False
    },
    {
        "id": 23,
        "framework": "Holland Code — Realistic",
        "text": "I like building and optimizing tools that others can use effectively.",
        "section": "holland",
        "trait": "realistic",
        "reverse": False
    },
    # ── Holland Code — Investigative (Q24–26) ────────────────────────────────
    {
        "id": 24,
        "framework": "Holland Code — Investigative",
        "text": "I enjoy analyzing complex problems to understand root causes.",
        "section": "holland",
        "trait": "investigative",
        "reverse": False
    },
    {
        "id": 25,
        "framework": "Holland Code — Investigative",
        "text": "I like researching new technologies, market trends, or user behaviors.",
        "section": "holland",
        "trait": "investigative",
        "reverse": False
    },
    {
        "id": 26,
        "framework": "Holland Code — Investigative",
        "text": "I'm drawn to roles that require continuous learning and skill development.",
        "section": "holland",
        "trait": "investigative",
        "reverse": False
    },
    # ── Holland Code — Artistic (Q27–29) ─────────────────────────────────────
    {
        "id": 27,
        "framework": "Holland Code — Artistic",
        "text": "I enjoy creating user experiences, visual designs, or innovative solutions.",
        "section": "holland",
        "trait": "artistic",
        "reverse": False
    },
    {
        "id": 28,
        "framework": "Holland Code — Artistic",
        "text": "I like working on projects where creativity and aesthetics matter.",
        "section": "holland",
        "trait": "artistic",
        "reverse": False
    },
    {
        "id": 29,
        "framework": "Holland Code — Artistic",
        "text": "I prefer flexible work environments that encourage experimentation.",
        "section": "holland",
        "trait": "artistic",
        "reverse": False
    },
    # ── Holland Code — Social (Q30–32) ───────────────────────────────────────
    {
        "id": 30,
        "framework": "Holland Code — Social",
        "text": "I enjoy mentoring team members and helping them grow professionally.",
        "section": "holland",
        "trait": "social",
        "reverse": False
    },
    {
        "id": 31,
        "framework": "Holland Code — Social",
        "text": "I like facilitating communication between different teams or departments.",
        "section": "holland",
        "trait": "social",
        "reverse": False
    },
    {
        "id": 32,
        "framework": "Holland Code — Social",
        "text": "I'm motivated by work that directly improves user or customer experiences.",
        "section": "holland",
        "trait": "social",
        "reverse": False
    },
    # ── Holland Code — Enterprising (Q33–35) ─────────────────────────────────
    {
        "id": 33,
        "framework": "Holland Code — Enterprising",
        "text": "I enjoy leading initiatives and driving projects from concept to completion.",
        "section": "holland",
        "trait": "enterprising",
        "reverse": False
    },
    {
        "id": 34,
        "framework": "Holland Code — Enterprising",
        "text": "I like influencing stakeholders and negotiating project requirements.",
        "section": "holland",
        "trait": "enterprising",
        "reverse": False
    },
    {
        "id": 35,
        "framework": "Holland Code — Enterprising",
        "text": "I'm comfortable making strategic decisions that impact business outcomes.",
        "section": "holland",
        "trait": "enterprising",
        "reverse": False
    },
    # ── Holland Code — Conventional (Q36–38) ─────────────────────────────────
    {
        "id": 36,
        "framework": "Holland Code — Conventional",
        "text": "I enjoy creating structured processes and ensuring compliance with standards.",
        "section": "holland",
        "trait": "conventional",
        "reverse": False
    },
    {
        "id": 37,
        "framework": "Holland Code — Conventional",
        "text": "I like organizing information, requirements, or project documentation.",
        "section": "holland",
        "trait": "conventional",
        "reverse": False
    },
    {
        "id": 38,
        "framework": "Holland Code — Conventional",
        "text": "I prefer working within established frameworks and methodologies.",
        "section": "holland",
        "trait": "conventional",
        "reverse": False
    },
    # ── IT Work Preferences — Collaboration (Q39–41) ─────────────────────────
    {
        "id": 39,
        "framework": "IT Work Preferences — Collaboration",
        "text": "I prefer working in cross-functional teams rather than specialized technical teams.",
        "section": "work_prefs",
        "trait": "collaboration",
        "reverse": False
    },
    {
        "id": 40,
        "framework": "IT Work Preferences — Collaboration",
        "text": "I enjoy bridging the gap between technical teams and business stakeholders.",
        "section": "work_prefs",
        "trait": "collaboration",
        "reverse": False
    },
    {
        "id": 41,
        "framework": "IT Work Preferences — Collaboration",
        "text": "I'm most productive when I can influence both technical and business decisions.",
        "section": "work_prefs",
        "trait": "collaboration",
        "reverse": False
    },
    # ── IT Work Preferences — Problem-Solving (Q42–44) ───────────────────────
    {
        "id": 42,
        "framework": "IT Work Preferences — Problem-Solving",
        "text": "I prefer solving people and process problems over purely technical challenges.",
        "section": "work_prefs",
        "trait": "problem_solving",
        "reverse": False
    },
    {
        "id": 43,
        "framework": "IT Work Preferences — Problem-Solving",
        "text": "I enjoy breaking down complex business requirements into actionable tasks.",
        "section": "work_prefs",
        "trait": "problem_solving",
        "reverse": False
    },
    {
        "id": 44,
        "framework": "IT Work Preferences — Problem-Solving",
        "text": "I like balancing technical feasibility with business value and user needs.",
        "section": "work_prefs",
        "trait": "problem_solving",
        "reverse": False
    },
    # ── IT Work Preferences — Leadership Growth (Q45–46) ─────────────────────
    {
        "id": 45,
        "framework": "IT Work Preferences — Leadership Growth",
        "text": "I see myself growing into leadership roles that combine technical and business expertise.",
        "section": "work_prefs",
        "trait": "leadership_growth",
        "reverse": False
    },
    {
        "id": 46,
        "framework": "IT Work Preferences — Leadership Growth",
        "text": "I'm more interested in broad business impact than deep technical specialization.",
        "section": "work_prefs",
        "trait": "leadership_growth",
        "reverse": False
    },
    # ── IT Work Preferences — Dynamic Environment (Q47–48) ───────────────────
    {
        "id": 47,
        "framework": "IT Work Preferences — Dynamic Environment",
        "text": "I thrive in dynamic environments where requirements and priorities change frequently.",
        "section": "work_prefs",
        "trait": "dynamic_environment",
        "reverse": False
    },
    {
        "id": 48,
        "framework": "IT Work Preferences — Dynamic Environment",
        "text": "I prefer roles where I interact with diverse stakeholders (users, developers, executives).",
        "section": "work_prefs",
        "trait": "dynamic_environment",
        "reverse": False
    },
]
