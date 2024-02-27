import enum

from sqlalchemy import (
    Column, Integer, String, Enum,
    ForeignKey
)
from sqlalchemy.orm import relationship, backref, Mapped

from spotipi.database import Base


class TokenypeEnum(str, enum.Enum):
    album = "album"
    artist = "artist"
    playlist = "playlist"
    track = "track"
    other = "other"


class RFIDNumber(Base):
    __tablename__ = "rfid_numbers"
    
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    number: Mapped[str] = Column(String)
    spotify_token: Mapped[str] = Column(String, unique=True, index=True)
    spotify_token_type: Mapped[str] = Column(Enum(TokenypeEnum), default=TokenypeEnum.other)
    spotify_name: Mapped[str] = Column(String, default=None)
