import os
import json
import re
from typing import List, Any

import google.generativeai as genai
from dotenv import load_dotenv

# Load .env from backend/app/ (so it works regardless of cwd when running uvicorn)
_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=_env_path)
# Fallback: load from cwd (e.g. if .env is in backend/)
load_dotenv()

from app.schemas.content import ContentRequest


def _get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


def _build_prompt(request: ContentRequest) -> str:
    return f"""Generate {request.number_of_posts} social media posts for the following business.

Business Name: {request.business_name}
Industry: {request.industry}
Target Audience: {request.target_audience}
Location: {request.location}
Business Goal: {request.business_goal.value}
Tone: {request.tone.value}

For each post, provide exactly the structure below. Return ONLY a valid JSON array of objects, no other text or markdown.
Do NOT generate actual images — only the structured AI image prompt text is required.

JSON structure for each post (one object per post):
{{
  "post_topic": "short topic title",
  "caption": "platform-neutral caption text",
  "platform_variations": {{
    "instagram": "Instagram-optimized version (concise, visual)",
    "linkedin": "LinkedIn-optimized version (professional)",
    "facebook": "Facebook-optimized version (conversational)"
  }},
  "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
  "cta": "call-to-action phrase or sentence",
  "ai_image_prompt": "Detailed prompt for DALL·E / Midjourney / Stable Diffusion to generate the post image (scene, style, mood, composition; no actual image)",
  "suggested_creative_type": "Carousel" | "Reel" | "Static Post",
  "text_overlay_suggestion": "Short phrase or line to overlay on the image",
  "color_theme_suggestion": "Suggested color palette or theme (e.g. warm earth tones, bold primary colors)"
}}

Return only the JSON array, e.g. [ {{ ... }}, {{ ... }} ]"""


def _extract_json(text: str) -> str:
    """Strip markdown code blocks if present."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_posts_with_ai(request: ContentRequest) -> List[dict[str, Any]]:
    """Call Gemini API and return structured list of posts."""
    model = _get_model()
    prompt = _build_prompt(request)
    response = model.generate_content(prompt)
    raw = response.text
    json_str = _extract_json(raw)
    data = json.loads(json_str)
    if not isinstance(data, list):
        data = [data]
    return data
