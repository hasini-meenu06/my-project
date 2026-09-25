import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# The project document specifies Gemini 1.5 Flash / Pro.
# If those models are unavailable for your API account, change these two
# values in .env to models currently available in your account.
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-1.5-flash").strip()
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-pro").strip()

HF_API_KEY = os.getenv("HF_API_KEY", "").strip()
HF_IMAGE_MODEL = os.getenv(
    "HF_IMAGE_MODEL", "runwayml/stable-diffusion-v1-5"
).strip()

USE_LOCAL_DIFFUSERS = os.getenv("USE_LOCAL_DIFFUSERS", "false").lower() == "true"

PANELS_DIR = BASE_DIR / "static" / "panels"
EXPORTS_DIR = BASE_DIR / "static" / "exports"
PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
