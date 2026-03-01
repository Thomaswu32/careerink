"""
Agent 2 — Career Path Discovery Engine
- Loads pre-extracted career profiles from JSON
- Runs weighted 4-component matching algorithm
- Applies viability filter and diversity constraint
- Returns top 3–5 ranked career cards with justifications
- Generates downloadable PDF career report (via ReportLab)
"""

import json
import logging
import os
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "career_profiles.json")

# Weights (configurable)
W_SKILLS     = 0.40
W_TRAITS     = 0.25
W_STYLE      = 0.20
W_EXPERIENCE = 0.15

LEVEL_MAP = {"Low": 1, "Moderate": 2, "High": 3}
SENIORITY_BANDS = {"Entry": 0, "Mid": 1, "Senior": 2, "Lead": 3}
EXP_TO_BAND = lambda y: "Entry" if y <= 2 else ("Mid" if y <= 5 else ("Senior" if y <= 10 else "Lead"))

VIABILITY_SKILLS_MIN = 35
VIABILITY_FINAL_MIN  = 50
MAX_PER_FAMILY       = 2
TOP_N                = 5


def load_career_profiles() -> List[Dict]:
    """Load pre-extracted career profiles from JSON file."""
    try:
        with open(DATA_PATH) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load career profiles: {e}")
        return []


# ─── Component A: Hard Skills Match (40%) ────────────────────────────────────

def score_skills(user_skills: List[str], career_skills: List[str]) -> Tuple[float, List[str], List[str]]:
    """
    Compute skills match score (0–100), top matched skills, and top gap skills.
    Simple binary match with equal weighting (no confidence weights in static data).
    """
    if not career_skills:
        return 50.0, [], []

    user_set   = {s.lower() for s in user_skills}
    career_set = career_skills  # list preserving order/importance

    matched = [s for s in career_set if s.lower() in user_set]
    gaps    = [s for s in career_set if s.lower() not in user_set]

    score = (len(matched) / len(career_set)) * 100 if career_set else 50.0

    # Top 3 matched (first in list = most important)
    top_matched = matched[:3]
    # Top 3 gaps
    top_gaps = gaps[:3]

    return round(score, 1), top_matched, top_gaps


# ─── Component B: Personality Trait Match (25%) ──────────────────────────────

def score_traits(user_traits: Dict[str, str], career_traits: Dict[str, str]) -> float:
    """
    Compare Big Five profiles. Penalise critical mismatches (|diff| > 1).
    Returns 0–100 score.
    """
    if not career_traits:
        return 50.0

    total_penalty = 0
    count = 0
    for dim in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
        u = LEVEL_MAP.get(user_traits.get(dim, "Moderate"), 2)
        c = LEVEL_MAP.get(career_traits.get(dim, "Moderate"), 2)
        diff = abs(u - c)
        # Penalty: diff=0 → 0, diff=1 → 15, diff=2 → 35
        penalty = {0: 0, 1: 15, 2: 35}.get(diff, 35)
        total_penalty += penalty
        count += 1

    avg_penalty = total_penalty / count if count else 0
    return round(max(0, 100 - avg_penalty), 1)


# ─── Component C: Work Style & Values Match (20%) ────────────────────────────

def score_style_values(
    user_style:  Dict[str, str],
    user_values: Dict[str, str],
    career_style: Dict[str, str],
    career_values: Dict[str, str],
) -> float:
    """
    Holland Code + IT Work Preferences match.
    Returns 0–100 combined score.
    """
    # Holland Code (6 dimensions) → 0–100
    style_pts = 0
    style_max = 6 * 20  # 20 pts per dimension
    for dim in ["realistic","investigative","artistic","social","enterprising","conventional"]:
        u = LEVEL_MAP.get(user_style.get(dim, "Moderate"), 2)
        c = LEVEL_MAP.get(career_style.get(dim, "Moderate"), 2)
        diff = abs(u - c)
        style_pts += {0: 20, 1: 12, 2: 0}.get(diff, 0)
    style_score = (style_pts / style_max) * 100

    # IT Work Preferences (4 dimensions) → 0–100
    vals_pts = 0
    vals_max = 4 * 20
    for dim in ["collaboration","problem_solving","leadership_growth","dynamic_environment"]:
        u = LEVEL_MAP.get(user_values.get(dim, "Moderate"), 2)
        c = LEVEL_MAP.get(career_values.get(dim, "Moderate"), 2)
        diff = abs(u - c)
        vals_pts += {0: 20, 1: 10, 2: 0}.get(diff, 0)
    vals_score = (vals_pts / vals_max) * 100

    # 50/50 blend of style and values
    return round((style_score + vals_score) / 2, 1)


# ─── Component D: Experience & Seniority Fit (15%) ───────────────────────────

def score_experience(user_years: int, career_seniority: str) -> float:
    """Band-based seniority match. Senior applying to Mid = 70 pts."""
    user_band   = EXP_TO_BAND(user_years)
    ub = SENIORITY_BANDS.get(user_band, 1)
    cb = SENIORITY_BANDS.get(career_seniority, 1)
    diff = abs(ub - cb)
    return {0: 100.0, 1: 70.0, 2: 30.0}.get(diff, 30.0)


# ─── Full Matching Algorithm ──────────────────────────────────────────────────

def match_careers(user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Run the weighted matching algorithm against all career profiles.
    Returns top 3–5 ranked matches passing viability filter + diversity constraint.
    """
    from backend.utils.deploy_ai import generate_justification

    profiles = load_career_profiles()
    if not profiles:
        logger.error("No career profiles loaded.")
        return []

    results = []
    for career in profiles:
        skills_score, top_matched, top_gaps = score_skills(
            user_profile["hard_skills"],
            career.get("required_hard_skills", []),
        )

        # Viability filter (Skills component must clear floor)
        if skills_score < VIABILITY_SKILLS_MIN:
            continue

        traits_score = score_traits(
            user_profile["personality_traits"],
            career.get("required_traits", {}),
        )

        style_score = score_style_values(
            user_profile["work_style"],
            user_profile["work_values"],
            career.get("work_style", {}),
            career.get("work_values", {}),
        )

        exp_score = score_experience(
            user_profile["experience_years"],
            career.get("seniority_level", "Mid"),
        )

        final_score = (
            W_SKILLS     * skills_score
            + W_TRAITS   * traits_score
            + W_STYLE    * style_score
            + W_EXPERIENCE * exp_score
        )

        if final_score < VIABILITY_FINAL_MIN:
            continue

        results.append({
            "career_id":    career["career_id"],
            "role_name":    career["role_name"],
            "role_family":  career["role_family"],
            "final_score":  round(final_score, 1),
            "skills_score": skills_score,
            "traits_score": traits_score,
            "style_score":  style_score,
            "experience_score": exp_score,
            "top_matched_skills": top_matched,
            "top_gap_skills":     top_gaps,
            "avg_ramp_up_months": career.get("avg_ramp_up_months", 12),
            "salary_range":       career.get("salary_range", "Market competitive"),
            "growth_trajectory":  career.get("growth_trajectory", "High"),
            "description_summary":career.get("description_summary", ""),
        })

    # Sort descending by final score
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # Diversity constraint: max 2 per role family
    family_counts: Dict[str, int] = {}
    diverse_results = []
    for r in results:
        fam = r["role_family"]
        if family_counts.get(fam, 0) < MAX_PER_FAMILY:
            diverse_results.append(r)
            family_counts[fam] = family_counts.get(fam, 0) + 1
        if len(diverse_results) >= TOP_N:
            break

    # If we have fewer than 3 after diversity, relax the constraint
    if len(diverse_results) < 3:
        for r in results:
            if r not in diverse_results:
                diverse_results.append(r)
            if len(diverse_results) >= 5:
                break

    # Generate justification sentences (one LLM call per card)
    for r in diverse_results[:TOP_N]:
        r["justification"] = generate_justification(
            role_name=r["role_name"],
            matched_skills=r["top_matched_skills"],
            gap_skills=r["top_gap_skills"],
            user_traits=user_profile["personality_traits"],
            final_score=r["final_score"],
        )

    return diverse_results[:TOP_N]


# ─── PDF Report Generation ────────────────────────────────────────────────────

def generate_pdf_report(user_profile: Dict, career_matches: List[Dict], user_name: str, assessment_date: str) -> bytes:
    """
    Generate a PDF Career Recommendations Report using ReportLab.
    Returns raw PDF bytes.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, PageBreak
    )
    from io import BytesIO
    import datetime

    buf = BytesIO()

    # Colours matching CareerInk brand
    INK     = colors.HexColor("#0d0d0d")
    PAPER   = colors.HexColor("#f5f0e8")
    CREAM   = colors.HexColor("#ede7d5")
    ACCENT  = colors.HexColor("#c8502a")
    ACCENT2 = colors.HexColor("#2a6ec8")
    MUTED   = colors.HexColor("#7a7060")
    SUCCESS = colors.HexColor("#2a8c5a")

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm,
    )

    styles = getSampleStyleSheet()
    title_style   = ParagraphStyle("Title",   fontName="Helvetica-Bold", fontSize=28, textColor=PAPER, spaceAfter=6, leading=34)
    h1_style      = ParagraphStyle("H1",      fontName="Helvetica-Bold", fontSize=18, textColor=INK, spaceAfter=8, leading=24)
    h2_style      = ParagraphStyle("H2",      fontName="Helvetica-Bold", fontSize=13, textColor=ACCENT, spaceAfter=6, leading=16)
    h3_style      = ParagraphStyle("H3",      fontName="Helvetica-Bold", fontSize=11, textColor=INK, spaceAfter=4, leading=14)
    body_style    = ParagraphStyle("Body",    fontName="Helvetica",      fontSize=10, textColor=INK, spaceAfter=4, leading=14)
    muted_style   = ParagraphStyle("Muted",   fontName="Helvetica",      fontSize=9,  textColor=MUTED, spaceAfter=3, leading=12)
    label_style   = ParagraphStyle("Label",   fontName="Helvetica-Bold", fontSize=8,  textColor=MUTED, spaceAfter=2, leading=10)
    score_style   = ParagraphStyle("Score",   fontName="Helvetica-Bold", fontSize=36, textColor=ACCENT, leading=42)

    today = assessment_date or datetime.date.today().strftime("%B %d, %Y")

    story = []

    # ── Cover Page ────────────────────────────────────────────────────────────
    # Dark background box via Table
    cover_data = [[Paragraph(f"CareerInk", ParagraphStyle("Logo", fontName="Helvetica-Bold", fontSize=32, textColor=ACCENT, leading=38))],
                  [Paragraph("Career Recommendations Report", ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=20, textColor=PAPER, leading=24))],
                  [Spacer(1, 6*mm)],
                  [Paragraph(f"Prepared for: {user_name}", ParagraphStyle("cf", fontName="Helvetica", fontSize=12, textColor=PAPER, leading=16))],
                  [Paragraph(f"Assessment Date: {today}", ParagraphStyle("cd", fontName="Helvetica", fontSize=11, textColor=colors.HexColor("#bbb5a8"), leading=14))],
                  [Spacer(1, 10*mm)],
                  [Paragraph("AI-Powered IT Career Transition Intelligence", ParagraphStyle("ct2", fontName="Helvetica-Oblique", fontSize=10, textColor=colors.HexColor("#bbb5a8"), leading=13))],
                  [Paragraph("CONFIDENTIAL — For personal use only", ParagraphStyle("conf", fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#888"), leading=10))],
                 ]
    cover_table = Table(cover_data, colWidths=[170*mm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), INK),
        ("TOPPADDING",    (0, 0), (-1, 0), 20*mm),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 15*mm),
        ("LEFTPADDING",   (0, 0), (-1, -1), 15*mm),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 15*mm),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [INK]),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # ── Page 2: Professional Profile Summary ─────────────────────────────────
    story.append(Paragraph("PROFESSIONAL PROFILE SUMMARY", label_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=6))
    story.append(Paragraph(f"<b>{user_name}</b> · {user_profile.get('current_role','IT Professional')}", h1_style))
    story.append(Paragraph(f"Experience: {user_profile.get('experience_years', 0)} years · Education: {user_profile.get('education_level','Bachelor')}", muted_style))
    story.append(Spacer(1, 4*mm))

    # Technical Skills
    story.append(Paragraph("Technical Skills", h2_style))
    hard_skills = user_profile.get("hard_skills", [])
    if hard_skills:
        skills_text = " · ".join(hard_skills[:20])
        story.append(Paragraph(skills_text, body_style))
    else:
        story.append(Paragraph("No technical skills extracted.", muted_style))
    story.append(Spacer(1, 3*mm))

    # Soft Skills
    soft_skills = user_profile.get("soft_skills_confirmed", [])
    if soft_skills:
        story.append(Paragraph("Soft Skills", h2_style))
        story.append(Paragraph(" · ".join(soft_skills), body_style))
        story.append(Spacer(1, 3*mm))

    # Big Five
    story.append(Paragraph("Personality Profile (Big Five)", h2_style))
    bf = user_profile.get("personality_traits", {})
    bf_raw = user_profile.get("bigfive_raw", {})
    bf_data = [["Trait", "Level", "Score"]]
    for trait in ["openness","conscientiousness","extraversion","agreeableness","neuroticism"]:
        level = bf.get(trait, "–")
        raw   = bf_raw.get(trait, "–")
        bf_data.append([trait.title(), level, str(raw)])
    bf_table = Table(bf_data, colWidths=[70*mm, 40*mm, 30*mm])
    bf_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), CREAM),
        ("TEXTCOLOR",   (0, 0), (-1, 0), INK),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#d8cfc0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING",  (0, 0), (-1, -1), 3),
    ]))
    story.append(bf_table)
    story.append(Spacer(1, 3*mm))

    # Holland Code
    story.append(Paragraph("Holland Code Interests (RIASEC)", h2_style))
    hc = user_profile.get("work_style", {})
    top3 = sorted(hc.items(), key=lambda x: LEVEL_MAP.get(x[1], 0), reverse=True)[:3]
    for trait, level in top3:
        story.append(Paragraph(f"<b>{trait.title()}</b> — {level}", body_style))
    story.append(Spacer(1, 3*mm))

    # Work Preferences
    story.append(Paragraph("IT Work Preferences", h2_style))
    wv = user_profile.get("work_values", {})
    for pref, level in wv.items():
        story.append(Paragraph(f"<b>{pref.replace('_',' ').title()}</b>: {level}", body_style))

    story.append(PageBreak())

    # ── Page 3: Career Matches Overview Table ─────────────────────────────────
    story.append(Paragraph("CAREER MATCHES OVERVIEW", label_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=6))
    story.append(Paragraph(f"Your Top {len(career_matches)} Career Path Recommendations", h1_style))
    story.append(Spacer(1, 4*mm))

    overview_data = [["#", "Role", "Family", "Match %", "Ramp-Up", "Salary Range"]]
    for i, cm in enumerate(career_matches, 1):
        overview_data.append([
            str(i),
            cm["role_name"],
            cm["role_family"],
            f"{cm['final_score']:.0f}%",
            f"{cm['avg_ramp_up_months']} mo.",
            cm["salary_range"],
        ])
    ov_table = Table(overview_data, colWidths=[8*mm, 55*mm, 35*mm, 20*mm, 20*mm, 35*mm])
    ov_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), INK),
        ("TEXTCOLOR",   (0, 0), (-1, 0), PAPER),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#d8cfc0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING",  (0, 0), (-1, -1), 3),
    ]))
    story.append(ov_table)
    story.append(PageBreak())

    # ── Pages 4–8: Career Detail Cards ───────────────────────────────────────
    for i, cm in enumerate(career_matches, 1):
        story.append(Paragraph(f"CAREER MATCH #{i}", label_style))
        story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=4))

        # Score + Role Name side by side
        header_data = [[
            Paragraph(f"{cm['final_score']:.0f}%", score_style),
            [
                Paragraph(cm["role_name"], h1_style),
                Paragraph(f"Role Family: {cm['role_family']}", muted_style),
                Paragraph(f"Ramp-Up: ~{cm['avg_ramp_up_months']} months  |  Salary: {cm['salary_range']}", body_style),
                Paragraph(f"Growth Trajectory: {cm['growth_trajectory']}", body_style),
            ]
        ]]
        hdr_tbl = Table(header_data, colWidths=[30*mm, 140*mm])
        hdr_tbl.setStyle(TableStyle([
            ("VALIGN",  (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0),(-1,-1), 2),
            ("BACKGROUND", (0,0), (-1,-1), CREAM),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ]))
        story.append(hdr_tbl)
        story.append(Spacer(1, 4*mm))

        story.append(Paragraph("Why You Match", h2_style))
        story.append(Paragraph(cm.get("justification", "—"), body_style))
        story.append(Spacer(1, 3*mm))

        # Matched & Gap Skills side by side
        matched_text = "<br/>".join([f"✓ {s}" for s in cm["top_matched_skills"]]) or "—"
        gap_text     = "<br/>".join([f"→ {s}" for s in cm["top_gap_skills"]]) or "—"
        skill_data = [
            [Paragraph("Top Matched Skills", h3_style), Paragraph("Key Skills to Develop", h3_style)],
            [Paragraph(matched_text, body_style),        Paragraph(gap_text, body_style)],
        ]
        skill_tbl = Table(skill_data, colWidths=[85*mm, 85*mm])
        skill_tbl.setStyle(TableStyle([
            ("GRID",        (0,0),(-1,-1), 0.5, colors.HexColor("#d8cfc0")),
            ("BACKGROUND",  (0,0),(-1,0), CREAM),
            ("LEFTPADDING", (0,0),(-1,-1), 6),
            ("TOPPADDING",  (0,0),(-1,-1), 4),
        ]))
        story.append(skill_tbl)
        story.append(Spacer(1, 3*mm))

        # Component scores breakdown
        story.append(Paragraph("Match Score Breakdown", h2_style))
        comp_data = [
            ["Component", "Score", "Weight"],
            ["Hard Skills Match",        f"{cm['skills_score']:.0f}%", "40%"],
            ["Personality Trait Match",  f"{cm['traits_score']:.0f}%", "25%"],
            ["Work Style & Values Match",f"{cm['style_score']:.0f}%",  "20%"],
            ["Experience & Seniority",   f"{cm['experience_score']:.0f}%", "15%"],
        ]
        comp_tbl = Table(comp_data, colWidths=[100*mm, 30*mm, 30*mm])
        comp_tbl.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0), INK),
            ("TEXTCOLOR",   (0,0), (-1,0), PAPER),
            ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",    (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, CREAM]),
            ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#d8cfc0")),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING",  (0,0), (-1,-1), 3),
        ]))
        story.append(comp_tbl)
        story.append(Spacer(1, 3*mm))

        story.append(Paragraph("Role Overview", h2_style))
        story.append(Paragraph(cm.get("description_summary", "—"), body_style))

        if i < len(career_matches):
            story.append(PageBreak())

    # ── Final Page: Next Steps ────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("NEXT STEPS", label_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=6))
    story.append(Paragraph("Your 3 Recommended Actions", h1_style))
    story.append(Spacer(1, 4*mm))
    steps = [
        "1. <b>Deep-dive into your #1 match</b> — Research 5 job descriptions for that role and compare required skills against your current profile.",
        "2. <b>Identify your top learning priority</b> — Focus on closing the single most critical skill gap identified in your Career Detail Card.",
        "3. <b>Network intentionally</b> — Find and connect with 3 people currently in your target role on LinkedIn to understand real-world day-to-day expectations.",
    ]
    for step in steps:
        story.append(Paragraph(step, body_style))
        story.append(Spacer(1, 3*mm))
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=CREAM, spaceAfter=4))
    story.append(Paragraph(
        "<i>This report was generated by CareerInk AI. Recommendations are based on your self-reported data and psychological assessment. "
        "Results are for career planning purposes only and do not guarantee employment outcomes.</i>",
        muted_style,
    ))
    story.append(Paragraph("careerink.io", ParagraphStyle("footer", fontName="Helvetica-Bold", fontSize=9, textColor=ACCENT)))

    doc.build(story)
    return buf.getvalue()
