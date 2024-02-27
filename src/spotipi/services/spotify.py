import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from spotipi.redis.redis_manager import RedisPubSubManager
import spotipi.schemas as schemas


class SpotifyService:
    def __init__(self) -> None:
        self.spotify_api = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials()
        )
        
    def get_item_info(self, item_id: str, item_type: str):
        if item_type == "track":
            return self.get_track_info(item_id)
        elif item_type == "album":
            return self.get_album_info(item_id)
        elif item_type == "artist":
            return self.get_artist_info(item_id)
        elif item_type == "playlist":
            return self.get_playlist_info(item_id)
        
        return {"message": "Item type not found"}

    def get_artist_info(self, artist_id: str):
        uri = f"spotify:artist:{artist_id}"
        return self.spotify_api.artist(uri)

    def get_album_info(self, album_id: str):
        uri = f"spotify:album:{album_id}"
        return self.spotify_api.album(uri)
    
    def get_track_info(self, track_id: str):
        uri = f"spotify:track:{track_id}"
        return self.spotify_api.track(uri)
    
    def get_playlist_info(self, playlist_id: str):
        uri = f"spotify:playlist:{playlist_id}"
        return self.spotify_api.playlist(uri)
    
    def pause(self) -> schemas.PlayerResponse:
        manager = RedisPubSubManager()
        manager.connect()

        manager.publish("player", {
            "type": "pause"
        })
