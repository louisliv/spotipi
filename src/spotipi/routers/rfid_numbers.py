import json, logging
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from sqlalchemy.orm import Session

import spotipi.schemas as schemas
import spotipi.services.rfid_numbers as rfid_numbers
from spotipi.database import get_db
from spotipi.exceptions import InvalidDataException
from spotipi.websockets.websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/api/rfid_numbers", tags=["rfid_numbers"])
socket_manager = WebSocketManager()

@router.get("/", response_model=list[schemas.RFIDNumber])
def get_rfid_numbers(db: Session = Depends(get_db)):
    return rfid_numbers.get_rfid_numbers(db)

@router.get("/scan_for_rfid", response_model=Union[schemas.RFIDNumber, schemas.RFIDNumberCreate])
def scan_for_rfid(db: Session = Depends(get_db)):
    rfid_numbers.set_rfid_reading_mode(True)
    rfid_number = rfid_numbers.scan_for_rfid(db)
    rfid_numbers.set_rfid_reading_mode(False)
    if not rfid_number:
        raise HTTPException(status_code=404, detail="RFID Number not found")
    return rfid_number

@router.get("/{id}", response_model=schemas.RFIDNumber)
def get_rfid_number(id: int, db: Session = Depends(get_db)):
    db_rfid_number = rfid_numbers.get_rfid_number_by_id(db, id)
    if not db_rfid_number:
        raise HTTPException(status_code=404, detail="RFID Number not found")
    return db_rfid_number

@router.post("/", response_model=schemas.RFIDNumber)
def create_rfid_number(rfid_number: schemas.RFIDNumberCreate, db: Session = Depends(get_db)):
    db_rfid_number = rfid_numbers.get_rfid_number(db, rfid_number.number)
    if db_rfid_number:
        raise HTTPException(status_code=400, detail="RFID Number already registered")
    
    try:
        db_rfid_number = rfid_numbers.create_rfid_number(db, rfid_number)
    
        return db_rfid_number
    except InvalidDataException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}", response_model=schemas.RFIDNumber)
def update_rfid_number(id: int, rfid_number: schemas.RFIDNumber, db: Session = Depends(get_db)):
    db_rfid_number = rfid_numbers.get_rfid_number_by_id(db, id)
    if not db_rfid_number:
        raise HTTPException(status_code=404, detail="RFID Number not found")
    return rfid_numbers.update_rfid_number(db, rfid_number)

@router.delete("/{id}", response_model=schemas.Delete)
def delete_rfid_number(id: int, db: Session = Depends(get_db)):
    db_rfid_number = rfid_numbers.get_rfid_number_by_id(db, id)
    if not db_rfid_number:
        raise HTTPException(status_code=404, detail="RFID Number not found")
    rfid_numbers.delete_rfid_number(db, db_rfid_number)
    return {"message": "RFID Number deleted"}

@router.post("/play", response_model=schemas.PlayerResponse)
def play(player_request: schemas.PlayerRequest):
    response = rfid_numbers.play(player_request.rfid_number)
    return response

@router.websocket("/ws/{room_id}")
async def start_scanner_websocket(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):
    await socket_manager.add_user_to_room(room_id, websocket)
    message = {
        "room_id": room_id,
        "message": f"connected to room - {room_id}"
    }
    await socket_manager.broadcast_to_room(room_id, json.dumps(message))
    try:
        rfid_numbers.set_rfid_reading_mode(True, coming_from="connected")
        while True:
            data = await websocket.receive_text()
            rfid_number = rfid_numbers.get_scanned_rfid_number(db, data)
            message = {
                "type": "rfid_number_scanned",
                "rfid_number": rfid_number.dict()
            }
            await socket_manager.broadcast_to_room(room_id, json.dumps(message))

    except WebSocketDisconnect:
        rfid_numbers.set_rfid_reading_mode(False, coming_from="disconnected")
        await socket_manager.remove_user_from_room(room_id, websocket)

        message = {
            "room_id": room_id,
            "message": f"disconnected from room - {room_id}"
        }
        await socket_manager.broadcast_to_room(room_id, json.dumps(message))
