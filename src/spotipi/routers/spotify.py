from fastapi import APIRouter, Depends, HTTPException
from spotipy import SpotifyException

import spotipi.schemas as schemas
from spotipi.services.spotify import SpotifyService

router = APIRouter(prefix="/api/spotify", tags=["spotify"])

def get_spotify_service():
    return SpotifyService()

@router.post("/item_info")
def get_item_info(item: schemas.SpotifyRequest, spotify_service: SpotifyService = Depends(get_spotify_service)):
    
    try:
        item_info = spotify_service.get_item_info(item.item_id, item.item_type)
    except SpotifyException as e:
        raise HTTPException(status_code=e.http_status, detail=e.msg)
    if not item_info:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_info

@router.get("/pause", response_model=schemas.PlayerResponse)
def pause(spotify_service: SpotifyService = Depends(get_spotify_service)):
    info = spotify_service.pause()
    return info
