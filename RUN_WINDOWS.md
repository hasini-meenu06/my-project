# ComicCraft - Windows Run Guide

Open PowerShell in:

```text
C:\Users\ELCOT\Downloads\ComicCraft_FIXED
```

Create the environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create `.env`:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=YOUR_KEY
GEMINI_FLASH_MODEL=gemini-1.5-flash
GEMINI_PRO_MODEL=gemini-1.5-pro
```

Optional hosted image generation:

```env
HF_API_KEY=YOUR_HUGGINGFACE_TOKEN
HF_IMAGE_MODEL=runwayml/stable-diffusion-v1-5
```

Run either command:

```powershell
python -m uvicorn main:app --reload
```

or:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## If PowerShell blocks activation

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

then:

```powershell
.\.venv\Scripts\Activate.ps1
```
