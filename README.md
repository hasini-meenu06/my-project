# ComicCraft - AI Comic Story Creator using Gemini Models

This project is rebuilt directly from the uploaded ComicCraft project document.

## Features from the document

- FastAPI backend
- Jinja2 templates
- Five-panel comic workflow
- Gemini Flash for structured outline
- Gemini Pro for narration and dialogue
- Stable Diffusion / Hugging Face Diffusers image generation
- Comic panel layout builder
- FPDF PDF export
- Form route `/generate`
- JSON route `/generate-comic/json`
- Image testing route `/test-image`
- Export success route `/export-success`
- FastAPI Swagger docs at `/docs`

## Exact project structure

```text
ComicCraft_PDF_Project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── config.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── css/style.css
│   ├── js/app.js
│   ├── panels/
│   └── exports/
├── .env.example
├── requirements.txt
└── README.md
```

## Windows installation

Open PowerShell in the project root:

```powershell
py -m venv comiccraft-env
.\comiccraft-env\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add the Gemini key:

```env
GEMINI_API_KEY=your_key_here
```

Optional Hugging Face hosted inference:

```env
HF_API_KEY=your_huggingface_token
```

## Run

```powershell
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Important model note

The uploaded project document names `gemini-1.5-flash` and `gemini-1.5-pro`. Those names are kept as the defaults so the implementation matches the document. If your Google AI account no longer exposes those model IDs, change `GEMINI_FLASH_MODEL` and `GEMINI_PRO_MODEL` in `.env` to model IDs available to your account.

## Image generation

There are three practical modes:

1. `USE_LOCAL_DIFFUSERS=true` — follows the document most literally and runs Diffusers locally. This can require a large model download and a capable GPU.
2. `HF_API_KEY=...` with `USE_LOCAL_DIFFUSERS=false` — uses Hugging Face hosted inference and avoids downloading the checkpoint locally.
3. No image key — creates a clearly labelled local demo artwork so the full college workflow can still be tested.

## Route summary

- `GET /` — home page
- `POST /generate` — HTML form comic generation
- `POST /generate-comic/json` — JSON API generation
- `POST /test-image` — direct image-generation test
- `GET /export-success` — PDF export confirmation
- `GET /docs` — FastAPI API documentation


## Windows compatibility fix

A root-level `main.py` has been included. Therefore both commands are valid:

```powershell
python -m uvicorn main:app --reload
```

```powershell
python -m uvicorn app.main:app --reload
```

The project also uses an absolute templates path, so it can be launched from the project root reliably.
