from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.models import PromptRequest, ImageTestRequest
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def run_comic(story_prompt, character_name, setting, tone, art_style):
    outline = generate_outline(
        story_prompt, character_name, setting, tone, art_style
    )
    story = generate_story(outline, character_name, tone)

    for panel in story:
        panel["image_path"] = generate_image(
            panel.get("image_prompt", ""),
            art_style
        )

    # The image path is generated on the expanded story objects.
    # Copy it into the corresponding outline panel before building the final layout.
    image_by_panel = {
        p["panel_number"]: p.get("image_path", "")
        for p in story
    }
    for panel in outline:
        panel["image_path"] = image_by_panel.get(panel["panel_number"], "")

    layout = build_comic_layout(outline, story)

    title = f"{character_name}: A ComicCraft Story"

    # PDF is a final export step. A PDF failure should not hide a
    # successfully generated comic preview.
    try:
        pdf_path = save_pdf(title, layout)
        pdf_error = ""
    except Exception as exc:
        pdf_path = ""
        pdf_error = f"PDF export warning: {exc}"

    return {
        "title": title,
        "layout": layout,
        "pdf_path": pdf_path,
        "pdf_error": pdf_error,
    }


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        result = run_comic(
            story_prompt, character_name, setting, tone, art_style
        )
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context=result
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)}
        )


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        result = run_comic(
            payload.story_prompt,
            payload.character_name,
            payload.setting,
            payload.tone,
            payload.art_style,
        )
        return JSONResponse(result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/test-image")
async def test_image(payload: ImageTestRequest):
    try:
        image_path = generate_image(payload.prompt, payload.art_style)
        return {"success": True, "image_path": image_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": pdf}
    )
