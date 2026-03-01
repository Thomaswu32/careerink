"""
Deploy AI client for Claude API calls.
Used by Agent 2 to generate career match justification sentences.
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

AUTH_URL = "https://api-auth.dev.deploy.ai/oauth2/token"
API_URL  = "https://core-api.dev.deploy.ai"
ORG_ID   = os.getenv("ORG_ID", "1e575dfe-5315-46d4-b814-b340750dc316")
AGENT_ID = os.getenv("AGENT_ID", "GPT_4O")


def get_access_token() -> str | None:
    """Obtain OAuth2 access token using client credentials."""
    client_id     = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if not client_id or not client_secret:
        return None
    try:
        resp = requests.post(
            AUTH_URL,
            data={
                "grant_type":    "client_credentials",
                "client_id":     client_id,
                "client_secret": client_secret,
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]
    except Exception as e:
        logger.warning(f"Failed to obtain Deploy AI token: {e}")
        return None


def create_chat(access_token: str) -> str | None:
    """Create a new chat session and return chat_id."""
    try:
        resp = requests.post(
            f"{API_URL}/chats",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Org": ORG_ID,
                "Content-Type": "application/json",
            },
            json={"agentId": AGENT_ID, "stream": False},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()["id"]
    except Exception as e:
        logger.warning(f"Failed to create Deploy AI chat: {e}")
        return None


def call_agent(access_token: str, chat_id: str, prompt: str) -> str | None:
    """Send a message to the agent and return the text response."""
    try:
        resp = requests.post(
            f"{API_URL}/messages",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Org": ORG_ID,
                "Content-Type": "application/json",
            },
            json={
                "chatId": chat_id,
                "stream": False,
                "content": [{"type": "text", "value": prompt}],
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["value"]
    except Exception as e:
        logger.warning(f"Deploy AI agent call failed: {e}")
        return None


def generate_justification(
    role_name: str,
    matched_skills: list[str],
    gap_skills: list[str],
    user_traits: dict,
    final_score: float,
) -> str:
    """
    Generate a one-sentence career match justification via Deploy AI / Claude.
    Falls back to a deterministic template if credentials are unavailable.
    """
    # Build prompt
    prompt = (
        f"Write a single, motivating sentence (max 30 words) explaining why this candidate "
        f"is a good match for the {role_name} role. "
        f"Their top matched skills are: {', '.join(matched_skills[:3])}. "
        f"Their key gaps to address: {', '.join(gap_skills[:2])}. "
        f"Match score: {final_score:.0f}%. "
        f"Be specific, positive, and professional. Return only the sentence."
    )

    token = get_access_token()
    if token:
        chat_id = create_chat(token)
        if chat_id:
            result = call_agent(token, chat_id, prompt)
            if result:
                # Clean up the response
                result = result.strip().strip('"').strip("'")
                return result

    # ── Fallback template ──────────────────────────────────────────────────
    skills_str = " and ".join(matched_skills[:2]) if matched_skills else "your technical background"
    gap_str    = gap_skills[0] if gap_skills else "a few targeted skills"
    return (
        f"Your {skills_str} expertise provides a strong foundation for {role_name}, "
        f"and developing {gap_str} will complete your transition path."
    )
