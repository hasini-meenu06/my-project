from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator using Gemini Models",
    description="Generate 5-panel AI comics from a user prompt and export them as PDF.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ComicCraft"}
