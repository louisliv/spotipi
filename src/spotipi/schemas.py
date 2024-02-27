from pydantic import BaseModel

class RFIDNumberBase(BaseModel):
    number: str
    spotify_token: str = None
    spotify_token_type: str = None
    spotify_name: str = None
    
class RFIDNumberCreate(RFIDNumberBase):
    pass

class RFIDNumber(RFIDNumberBase):
    id: int
    
    class Config:
        from_attributes = True
        
class Delete(BaseModel):
    message: str

class SpotifyRequest(BaseModel):
    item_id: str
    item_type: str

class PlayerRequest(BaseModel):
    rfid_number: str

class PlayerResponse(BaseModel):
    message: str
