from abc import abstractmethod
import os
import enum
import logging
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

from spotipi.database import SessionLocal
from spotipi.models import RFIDNumber
from spotipi.utils import Settings
from spotipi.pubsub.pubsub_manager import PubSubManager
from spotipi.notification import NotificationSound


SPOTIFY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIFY_DEVICE_ID = os.getenv("SPOTIFY_DEVICE_ID")
SPOTIFY_REDIRECT_URI = os.getenv(
    "SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback"
)
SPOTIFY_AUTH_TOKEN = os.getenv("SPOTIFY_AUTH_TOKEN")
SPOTIFY_SCOPE = "user-read-playback-state,user-modify-playback-state"
SPOTIFY_USERNAME = os.getenv("SPOTIFY_USERNAME")


class PlayerResponses(enum.Enum):
    playing = "playing"
    paused = "paused"
    stopped = "stopped"
    no_rfid = "no_rfid"
    not_shuffled = "not_shuffled"
    shuffled = "shuffled"
    playing_current_track = "playing_current_track"


class BasePlayer:
    def __init__(self, device_id: str = SPOTIFY_DEVICE_ID) -> None:
        logging.info(f"SpotifyPlayer: Initializing player with device_id: {device_id}")
        self.device_id = device_id
        self.db = SessionLocal()
        self.settings = Settings()
        self.pubsub_manager = PubSubManager()
        self.pubsub_manager.connect()

    def handle_message(self, message: dict):
        try:
            message_type = message["type"]
            if message_type == PlayerResponses.playing.value:
                return self.play(message.get("rfid_number"))
            elif message_type == PlayerResponses.paused.value:
                return self.pause()
            elif message_type == PlayerResponses.playing_current_track.value:
                return self.play_current_track()
            elif message_type == "stop":
                return self.stop()
        except Exception as e:
            self.handle_error_from_spotify(e)

    def handle_error_from_spotify(self, error: Exception):
        logging.exception(error)
        if type(error) == SpotifyException:
            # Log the error
            if error.http_status == 403:
                self.play_notification("Spotify is not available")
                return
            elif error.http_status == 404:
                self.play_notification(
                    "The device is not available. Please start Spotify on your device."
                )
                return
            self.play_notification("An unexpected error occurred")
            return
        self.play_notification("An unexpected error occurred")

    def play_notification(self, message: str):
        NotificationSound(message)

    @abstractmethod
    def play(self, id: str) -> PlayerResponses:
        pass

    @abstractmethod
    def pause(self) -> PlayerResponses:
        pass

    @abstractmethod
    def stop(self) -> PlayerResponses:
        pass

    @abstractmethod
    def play_current_track(self) -> PlayerResponses:
        pass

    @abstractmethod
    def set_shuffle_state(self) -> None:
        pass

    @abstractmethod
    def get_playback_state(self) -> dict:
        pass


class FakePlayer(BasePlayer):
    def play(self, id: str) -> PlayerResponses:
        rfid_number: Optional[RFIDNumber] = (
            self.db.query(RFIDNumber).filter(RFIDNumber.number == str(id)).first()
        )

        if not rfid_number:
            error_msg = "No RFID number found"
            logging.error(error_msg)
            self.play_notification(error_msg)
            self.play_current_track()
            return PlayerResponses.no_rfid.value

        logging.info(f"Playing {rfid_number.spotify_name}")
        self.play_notification(f"Playing {rfid_number.spotify_name}")
        return PlayerResponses.playing.value

    def pause(self) -> PlayerResponses:
        logging.info("Pausing")
        return PlayerResponses.paused.value

    def stop(self) -> PlayerResponses:
        logging.info("Stopping")
        return PlayerResponses.stopped.value

    def play_current_track(self) -> PlayerResponses:
        logging.info("Playing current track")
        return PlayerResponses.playing.value

    def set_shuffle_state(self) -> None:
        current_shuffle_state = self.settings.get_value("shuffle")
        logging.info(f"Setting shuffle state to {not current_shuffle_state}")
        self.settings.set_value("shuffle", not current_shuffle_state)

    def get_playback_state(self) -> dict:
        return {"is_playing": True, "shuffle_state": self.settings.get_value("shuffle")}


class SpotifyPlayer(BasePlayer):
    def __init__(self, device_id: str = SPOTIFY_DEVICE_ID) -> None:
        super().__init__(device_id)
        self.spotify_player = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                open_browser=False,
                redirect_uri=SPOTIFY_REDIRECT_URI,
                scope=SPOTIFY_SCOPE,
                username=SPOTIFY_USERNAME,
            )
        )

    def play(self, id: str = None) -> PlayerResponses:
        self.spotify_player.transfer_playback(
            device_id=self.device_id, force_play=False
        )

        if not id:
            # If no id is provided, play the current track. This usually happens
            # when the play command is sent from the cmd line application without
            # an rfid given.
            self.play_current_track()
            return PlayerResponses.playing_current_track.value

        rfid_number: Optional[RFIDNumber] = (
            self.db.query(RFIDNumber).filter(RFIDNumber.number == str(id)).first()
        )

        if not rfid_number:
            error_msg = "No RFID number found"
            logging.error(error_msg)
            self.play_notification(error_msg)
            self.play_current_track()
            return PlayerResponses.no_rfid.value

        spotify_uri = f"spotify:{rfid_number.spotify_token_type.value}:{rfid_number.spotify_token}"

        self.play_notification(f"Playing {rfid_number.spotify_name}")

        self.set_shuffle_state()

        self.spotify_player.start_playback(
            device_id=self.device_id, context_uri=spotify_uri
        )

        return PlayerResponses.playing.value

    def pause(self) -> PlayerResponses:
        self.spotify_player.pause_playback(device_id=self.device_id)
        return PlayerResponses.paused.value

    def stop(self) -> PlayerResponses:
        self.spotify_player.pause_playback(device_id=self.device_id)
        return PlayerResponses.stopped.value

    def play_current_track(self) -> PlayerResponses:
        current_state = self.get_playback_state()
        if current_state.get("is_playing"):
            return PlayerResponses.playing.value
        self.spotify_player.start_playback(device_id=self.device_id)
        return PlayerResponses.playing.value

    def set_shuffle_state(self) -> None:
        current_state = self.get_playback_state()
        settings_shuffle_value = self.settings.get_value("shuffle")

        shuffle_state = current_state.get("shuffle_state")

        if shuffle_state == settings_shuffle_value:
            return

        self.spotify_player.shuffle(settings_shuffle_value, device_id=self.device_id)

    def get_playback_state(self) -> dict:
        return self.spotify_player.current_playback()
