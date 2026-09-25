from pathlib import Path
import re
import uuid

from app.config import (
    HF_API_KEY,
    HF_IMAGE_MODEL,
    USE_LOCAL_DIFFUSERS,
    PANELS_DIR,
)


def _safe_name(prompt: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "_", prompt).strip("_").lower()
    return (base[:55] or "panel") + "_" + uuid.uuid4().hex[:8] + ".png"


def _placeholder_image(path: Path, prompt: str):
    """
    Creates a lightweight fallback image so the complete project can be tested
    without downloading a multi-GB Stable Diffusion checkpoint.
    """
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (1024, 640), (28, 32, 55))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
        small = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font = None
        small = None
    draw.rectangle((25, 25, 999, 615), outline=(230, 120, 255), width=5)
    draw.text((55, 65), "ComicCraft – Demo Artwork", fill="white", font=font)
    short = prompt[:180].replace("\n", " ")
    draw.text((55, 140), short, fill=(220, 225, 240), font=small)
    draw.text((55, 540), "Configure HF_API_KEY or USE_LOCAL_DIFFUSERS=true for AI artwork.",
              fill=(190, 195, 215), font=small)
    img.save(path)


def _local_diffusers(prompt: str, path: Path):
    import torch
    from diffusers import StableDiffusionPipeline

    pipe = StableDiffusionPipeline.from_pretrained(
        HF_IMAGE_MODEL,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    image = pipe(
        prompt,
        num_inference_steps=20,
        guidance_scale=7.0,
    ).images[0]
    image.save(path)


def _huggingface_inference(prompt: str, path: Path):
    from huggingface_hub import InferenceClient
    client = InferenceClient(token=HF_API_KEY)
    image = client.text_to_image(prompt, model=HF_IMAGE_MODEL)
    image.save(path)


def generate_image(prompt: str, art_style: str = "comic book") -> str:
    """
    Generate and save one panel image.

    Priority:
    1. Local Diffusers/Stable Diffusion when USE_LOCAL_DIFFUSERS=true.
    2. Hugging Face hosted inference when HF_API_KEY is configured.
    3. A local demo image, so the college project remains testable without
       a GPU or paid inference service.
    """
    path = PANELS_DIR / _safe_name(prompt)
    final_prompt = (
        f"{art_style} comic-style illustration, {prompt}, "
        "consistent character design, cinematic lighting, detailed environment, "
        "clean line art, no written words, no speech bubbles, no watermark"
    )

    try:
        if USE_LOCAL_DIFFUSERS:
            _local_diffusers(final_prompt, path)
        elif HF_API_KEY:
            _huggingface_inference(final_prompt, path)
        else:
            _placeholder_image(path, final_prompt)
    except Exception:
        _placeholder_image(path, final_prompt)

    # Browser-visible URL, not a filesystem path.
    return "/static/panels/" + path.name
