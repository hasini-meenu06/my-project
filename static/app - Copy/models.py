from typing import List
from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=5, max_length=3000)
    character_name: str = Field(..., min_length=1, max_length=100)
    setting: str = Field(..., min_length=1, max_length=150)
    tone: str = Field(..., min_length=1, max_length=80)
    art_style: str = Field(..., min_length=1, max_length=100)


class ImageTestRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=2000)
    art_style: str = "comic book"


class Panel(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
    caption: str = ""
    narration: str = ""
    dialogue: str = ""
    image_path: str = ""


class ComicResponse(BaseModel):
    title: str
    layout: List[Panel]
    pdf_path: str = ""
