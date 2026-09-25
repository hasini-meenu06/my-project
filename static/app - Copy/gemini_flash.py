import json
import re
from app.config import GEMINI_API_KEY, GEMINI_FLASH_MODEL


def _client():
    if not GEMINI_API_KEY:
        return None
    try:
        from google import genai
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        return None


def _extract_json(text: str):
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.I)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("[")
    end = text.rfind("]")
    if start >= 0 and end > start:
        text = text[start:end + 1]
    return json.loads(text)


def _demo_outline(story_prompt, character_name, setting, tone, art_style):
    beats = [
        ("The Beginning", f"{character_name} begins the adventure in the {setting}."),
        ("A Strange Discovery", f"{character_name} discovers something unexpected that changes the journey."),
        ("The Challenge", f"A difficult obstacle appears and tests {character_name}'s courage."),
        ("The Turning Point", f"{character_name} finds a clever way to overcome the challenge."),
        ("A New Beginning", f"The adventure ends with {character_name} looking toward a new future.")
    ]
    return [
        {
            "panel_number": i + 1,
            "title": title,
            "scene_description": desc,
            "image_prompt": (
                f"{art_style} comic illustration, {tone} mood, {character_name} in {setting}, "
                f"{desc} Consistent character appearance, cinematic composition, expressive pose, "
                f"clean line art, detailed background, no text, no speech bubbles, no watermark."
            )
        }
        for i, (title, desc) in enumerate(beats)
    ]


def generate_outline(story_prompt, character_name, setting, tone, art_style):
    """
    Gemini Flash: generate a structured five-panel comic outline.
    Falls back to a deterministic demo outline if no API key is configured.
    """
    client = _client()
    if client is None:
        return _demo_outline(story_prompt, character_name, setting, tone, art_style)

    prompt = f"""
You are ComicCraft's fast story-outline planner.

Create EXACTLY 5 panels for a comic.

User story:
{story_prompt}

Character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON as an array with exactly 5 objects.
Each object must contain:
panel_number, title, scene_description, image_prompt

Rules:
- panel_number must be 1,2,3,4,5
- create a coherent beginning, development, conflict, turning point and ending
- keep the same character appearance across all image prompts
- image_prompt must describe only visual content and must not contain written text
"""
    try:
        response = client.models.generate_content(
            model=GEMINI_FLASH_MODEL,
            contents=prompt,
        )
        data = _extract_json(response.text)
        if not isinstance(data, list) or len(data) != 5:
            raise ValueError("Gemini Flash did not return exactly five panels.")
        return data
    except Exception as exc:
        demo = _demo_outline(story_prompt, character_name, setting, tone, art_style)
        demo[0]["scene_description"] += f" (Demo fallback: {type(exc).__name__})"
        return demo
