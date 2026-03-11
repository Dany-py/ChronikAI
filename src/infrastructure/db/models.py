# db/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, func
from src.infrastructure.db.database import Base
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    
    def __repr__(self):
        return f"<users(id={self.id}, username={self.username}, email={self.email})>"
 
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    session_uid = Column(String(36), index=True)  # ou Text si longueur variable
    timestamp = Column(Integer)
    app_name = Column(String(100), index=True)
    window_title = Column(String(255))  # 255 est plus courant
    duration = Column(Integer, index=True)
    entry = Column(Text)
    is_consulted = Column(Boolean, index=True, default=False)
    is_written = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime, index=True, default=func.now())

    def __repr__(self):
        return (f"<Event(id={self.id}, timestamp={self.timestamp}, "
                f"app_name={self.app_name}, session_uid={self.session_uid})>"
                f"window_title={self.window_title}, entry={self.entry}")
    
class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_uid = Column(String(36), unique=True, index=True)  # ou Text si longueur variable
    created_at = Column(DateTime, index=True, default=func.now())

    def __repr__(self):
        return f"<Session(id={self.id}, session_uid={self.session_uid})>"
    

# Classe de validation des données pour insertion en db.
class EventCreate(BaseModel):
    timestamp: int
    app_name: str
    window_title: str
    duration: int
    entry: str = ""
    session_uid: str
    is_consulted: bool
    is_written: bool

class SessionCreate(BaseModel):
    session_uid:str