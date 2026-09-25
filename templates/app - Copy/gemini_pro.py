import json
import re
from app.config import GEMINI_API_KEY, GEMINI_PRO_MODEL


def _client():
    if not GEMINI_API_KEY:
        return None
    try:
        from google import genai
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        return None


def _extract_json(text):
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.I)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("[")
    end = text.rfind("]")
    if start >= 0 and end > start:
        text = text[start:end + 1]
    return json.loads(text)


def _demo_story(outline, character_name, tone):
    for p in outline:
        n = p["panel_number"]
        p["caption"] = [
            "The adventure begins.",
            "Something unusual catches the hero's attention.",
            "The challenge becomes impossible to ignore.",
            "A brave idea changes everything.",
            "The journey ends, but another adventure waits."
        ][n - 1]
        p["narration"] = (
            f"{character_name} faces the moment with a {tone} spirit. "
            f"{p['scene_description']}"
        )
        p["dialogue"] = [
            f"{character_name}: I have a feeling this is only the beginning.",
            f"{character_name}: What is that strange sign trying to tell me?",
            f"{character_name}: I cannot turn back now.",
            f"{character_name}: There must be another way.",
            f"{character_name}: We made it. What an adventure!"
        ][n - 1]
    return outline


def generate_story(outline, character_name, tone):
    """
    Gemini Pro: expand the five-panel outline into captions, narration and dialogue.
    """
    client = _client()
    if client is None:
        return _demo_story(outline, character_name, tone)

    outline_text = json.dumps(outline, ensure_ascii=False, indent=2)
    prompt = f"""
You are ComicCraft's creative story writer.

Expand this five-panel outline into a polished comic story.

Character: {character_name}
Tone: {tone}

Outline:
{outline_text}

Return ONLY valid JSON with exactly five objects.
Keep all original panel_number, title, scene_description and image_prompt values.
Add:
caption: short atmospheric caption
narration: 2-3 engaging sentences
dialogue: one short line of character dialogue

Do not add extra keys. Keep the story coherent across all five panels.
"""
    try:
        response = client.models.generate_content(
            model=GEMINI_PRO_MODEL,
            contents=prompt,
        )
        data = _extract_json(response.text)
        if not isinstance(data, list) or len(data) != 5:
            raise ValueError("Gemini Pro did not return exactly five panels.")
        return data
    except Exception:
        return _demo_story(outline, character_name, tone)
