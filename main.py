"""Compatibility entry point for ComicCraft.

You can run either:
    python -m uvicorn main:app --reload
or:
    python -m uvicorn app.main:app --reload
"""
from app.main import app

__all__ = ["app"]
