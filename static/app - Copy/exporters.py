from pathlib import Path
from datetime import datetime
import re

from fpdf import FPDF
from PIL import Image

from app.config import BASE_DIR, EXPORTS_DIR


def _pdf_text(value):
    text = str(value or "")
    replacements = {
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "–": "-", "—": "-", "…": "...",
        "•": "-", "→": "->", "×": "x",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Prevent FPDF from failing when one token is wider than the page.
    text = re.sub(r"(\S{55})(?=\S)", r"\1 ", text)
    return text


def _absolute_image_path(image_url: str):
    if not image_url:
        return None
    if image_url.startswith("/static/"):
        return BASE_DIR / image_url.lstrip("/")
    return Path(image_url)


def _write_text(pdf, text, font_size=11, bold=False):
    pdf.set_font("Arial", "B" if bold else "", font_size)
    pdf.multi_cell(170, 7, _pdf_text(text), wrapmode="CHAR")


def save_pdf(title: str, layout: list) -> str:
    filename = f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output = EXPORTS_DIR / filename

    pdf = FPDF("P", "mm", "A4")
    pdf.set_margins(20, 15, 20)
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()

        _write_text(pdf, title, 18, True)
        _write_text(
            pdf,
            f"Panel {panel.get('panel_number', '')}: {panel.get('title', '')}",
            14,
            True,
        )

        image_path = _absolute_image_path(panel.get("image_path", ""))
        if image_path and image_path.exists():
            try:
                with Image.open(image_path) as im:
                    width, height = im.size
                ratio = height / max(width, 1)
                image_w = 170
                image_h = min(92, image_w * ratio)
                if image_h > 0:
                    pdf.image(str(image_path), x=20, w=image_w, h=image_h)
                    pdf.ln(5)
            except Exception:
                pass

        _write_text(pdf, panel.get("scene_description", ""), 10)

        if panel.get("caption"):
            _write_text(pdf, "Caption: " + panel["caption"], 10)

        if panel.get("narration"):
            _write_text(pdf, "Narration: " + panel["narration"], 10)

        if panel.get("dialogue"):
            _write_text(pdf, "Dialogue: " + panel["dialogue"], 10, True)

    pdf.output(str(output))
    return "/static/exports/" + filename
