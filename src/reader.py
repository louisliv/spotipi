import logging
from time import sleep

try:
    from mfrc522 import SimpleMFRC522
except Exception as e:
    logging.error("Failed to initialize RFID reader.")
    logging.warning("Using fake RFID reader")
    from spotipi.fake_mfrc import FakeSimpleMFRC as SimpleMFRC522

from spotipi.fake_mfrc import FakeSimpleMFRC
from spotipi.pubsub.pubsub_manager import PubSubManager
from spotipi.redis.redis_manager import RedisPubSubManager, AsyncRedisPubSubManager


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RFIDReader:
    def __init__(self):
        try:
            self.reader = SimpleMFRC522()
        except Exception as e:
            logger.error("Failed to initialize RFID reader")
            logger.warning("Using fake RFID reader")
            self.reader = FakeSimpleMFRC()

    def read(self):
        """Reads the RFID tag and returns the id and text"""
        logger.info("Waiting for record scan...")
        id, text = self.reader.read()
        print(f"Card Value is: {id}")
        logger.info(f"Card Value is: {id}")
        return str(id), text
    
    def close(self):
        self.reader.close()

class RFIDReaderListener:
    def __init__(self):
        self.reader = RFIDReader()
        self.pubsub_manager = PubSubManager()
        self.pubsub_manager.connect()

    def listen(self):
        try:
            while True:
                id, text = self.reader.read()
                message = self.build_message(id, text)
                logger.info(f"Sending message from Reader: {message}")
                self.pubsub_manager.publish("scanner", message)

                sleep(5)
        finally:
            self.close()

    def build_message(self, id, text):
        return {
            "type": "rfid_number",
            "rfid_number": id,
            "text": text
        }

    def close(self):
        self.reader.close()


def main():
    reader = RFIDReaderListener()
    reader.listen()

if __name__ == "__main__":
    main()
