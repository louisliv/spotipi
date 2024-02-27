import os
import logging
from io import BytesIO

from gtts import gTTS
import pydub
from pydub.playback import play

from spotipi.constants import CHIME_FILE

ENV = os.getenv('ENV', 'development')


class NotificationSound:
    def __init__(self, message: str, should_play_chime=True):
        self.should_play_chime = should_play_chime
        self.message = message
        
        try:
            self._play_notification()
        except:
            logging.exception("Error playing notification")
        
    def _play_notification(self):
        if self.should_play_chime:
            self._play_chime()
        self._play_message()
        
    def _play_chime(self):
        if ENV == 'development':
            logging.info("Chime would have played")
            return

        file_path = os.path.dirname(os.path.realpath(__file__))
        chime_file = os.path.join(file_path, CHIME_FILE)
        chime = pydub.AudioSegment.from_file(chime_file, format="ogg")
        play(chime)
        
    def _play_message(self):
        if ENV == 'development':
            logging.info(f"Notification: {self.message}")
            return

        mp3_fp = BytesIO()
        tts = gTTS(text=self.message, lang='en')
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        message_file = pydub.AudioSegment.from_file(mp3_fp, format="mp3")
        play(message_file)
