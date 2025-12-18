"""Minimal FastAPI application for Docker"""

from __future__ import annotations

from fastapi import FastAPI

# Create FastAPI application
app = FastAPI()


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """Return simple status"""
    return {"status": "ok"}