from typing import Union, Dict
from uuid import uuid4
import time
import logging

from sqlalchemy.orm import Session

from spotipi.models import RFIDNumber
import spotipi.schemas as schemas

from spotipi.player import PlayerResponses

from spotipi.pubsub.pubsub_manager import PubSubManager

from spotipi.utils import Config


def get_rfid_numbers(db: Session):
    return db.query(RFIDNumber).all()


def get_rfid_number(db: Session, number: str):
    return db.query(RFIDNumber).filter(RFIDNumber.number == number).first()


def get_rfid_number_by_id(db: Session, number_id: int):
    return db.query(RFIDNumber).filter(RFIDNumber.id == number_id).first()


def create_rfid_number(db: Session, rfid_number: schemas.RFIDNumberCreate):        
    db_rfid_number = RFIDNumber(**rfid_number.dict())
    db.add(db_rfid_number)
    db.commit()
    db.refresh(db_rfid_number)
    return db_rfid_number


def update_rfid_number(db: Session, rfid_number: schemas.RFIDNumber):
    db_rfid_number = get_rfid_number_by_id(db, rfid_number.id)
    db_rfid_number.number = rfid_number.number
    db_rfid_number.spotify_token = rfid_number.spotify_token
    db_rfid_number.spotify_token_type = rfid_number.spotify_token_type
    db.commit()
    db.refresh(db_rfid_number)
    return db_rfid_number


def delete_rfid_number(db: Session, rfid_number: schemas.RFIDNumber):
    db.delete(rfid_number)
    db.commit()
    return rfid_number


def set_rfid_reading_mode(reading_mode: bool, coming_from = "unknown"):
    config = Config()
    config.set_reading_mode(reading_mode)

    manager = PubSubManager()
    manager.connect()

    manager.publish("scanner", {
        "type": "set_reading_mode",
        "reading_mode": reading_mode
    })

    if reading_mode:
        manager.publish("player", {
            "type": PlayerResponses.paused.value
        })

        manager.publish("notifications", {
            "message": "Reading mode"
        })
    else:
        manager.publish("notifications", {
            "message": "Exiting reading mode"
        })
        manager.publish("player", {
            "type": PlayerResponses.playing_current_track.value,
            "rfid_number": coming_from
        })


def scan_for_rfid(db: Session) -> Union[schemas.RFIDNumber, schemas.RFIDNumberCreate, None]:    
    # For testing purposes, we will just generate a random number
    time.sleep(5)
    id = str(uuid4())
    
    # Uncomment for production
    # id = reader.read()[0]
    logging.info("Card Value is:", id)
    
    rfid_number = get_rfid_number(db, id)
    if rfid_number:
        logging.info("No RFID number found")
        return rfid_number
    
    rfid_number = schemas.RFIDNumberCreate(number=id)

    return rfid_number


def play(rfid_number: str) -> schemas.PlayerResponse:
    manager = PubSubManager()
    manager.connect()

    manager.publish("player", {
        "type": PlayerResponses.playing.value,
        "rfid_number": rfid_number
    })

    response = f"Playing {rfid_number}"

    return schemas.PlayerResponse(message=response)


def pause() -> schemas.PlayerResponse:
    manager = PubSubManager()
    manager.connect()

    manager.publish("player", {
        "type": PlayerResponses.paused.value
    })

    response = "Pausing Spotify"

    return schemas.PlayerResponse(message=response)


def get_scanned_rfid_number(db: Session, data: Dict) -> Union[schemas.RFIDNumber, schemas.RFIDNumberCreate, None]:
    logging.info("Data: ", data)
    rfid_number = get_rfid_number(db, data["rfid_number"])

    if rfid_number:
        return rfid_number
    
    rfid_number = schemas.RFIDNumberCreate(number=data["rfid_number"])
    
    return rfid_number
