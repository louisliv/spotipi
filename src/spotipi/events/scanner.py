import logging

from spotipi.database import SessionLocal
from spotipi.services.rfid_numbers import get_scanned_rfid_number
from spotipi.player import PlayerResponses
from spotipi.utils import convert_redis_to_bool
from spotipi.redis.redis_manager import RedisPubSubManager


def scanner_consumer(message: dict):
    message_type = message["type"]
    
    if message_type == "set_reading_mode":
        return set_reading_mode(message["reading_mode"])
    if message_type == "rfid_number":
        return rfid_number_recieved(message)


def set_reading_mode(reading_mode: bool):
    redis = RedisPubSubManager()
    redis.connect()

    redis.redis_connection.set("reading_mode", str(reading_mode))


def rfid_number_recieved(message: dict):
    rfid_number = message.get("rfid_number")

    redis = RedisPubSubManager()
    redis.connect()
    
    reading_mode_redis_value = redis.redis_connection.get("reading_mode")
    
    if reading_mode_redis_value and isinstance(reading_mode_redis_value, bytes):
        reading_mode_redis_value = reading_mode_redis_value.decode()
    
    reading_mode = convert_redis_to_bool(reading_mode_redis_value)

    if not reading_mode:
        if not rfid_number:
            logging.warning(f"No RFID number found. Data: {message}")
            return
        player_message = build_player_message(rfid_number)
        redis.publish("player", player_message)
        return
    
    if rfid_number:
        message = build_scanner_message(rfid_number)
        redis.publish("rfid_number", message)


def build_scanner_message(rfid_number: str):
    db = SessionLocal()
    db_rfid_number = get_scanned_rfid_number(db, {"rfid_number": rfid_number})

    return {
        "type": "rfid_number",
        "rfid_number": db_rfid_number.dict()
    }


def build_player_message(rfid_number):
    return {
        "type": PlayerResponses.playing.value,
        "rfid_number": rfid_number
    }
