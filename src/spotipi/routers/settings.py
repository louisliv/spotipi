from typing import Dict, Any

from fastapi import APIRouter, Request, Body
import spotipi.services.settings as settings

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/")
def get_all_settings():
    return settings.get_all_settings()

@router.post("/")
async def set_all_settings(request: Request):
    settings_to_set = await request.json()
    return settings.set_all_settings(settings_to_set)
