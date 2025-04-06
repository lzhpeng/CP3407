from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

Base = declarative_base()

# SQLAlchemy 模型
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    events = relationship("Event", back_populates="creator")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, index=True)
    event_date = Column(DateTime)
    location = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="events")

# Pydantic 模型
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    event_name: str
    event_date: datetime
    location: str
    description: str

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True

# 创建数据库引擎
engine = create_engine("sqlite:///./events.db", echo=True)

# 创建所有表
def init_db():
    Base.metadata.create_all(bind=engine) 