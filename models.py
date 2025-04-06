from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import os

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
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    creator = relationship("User", back_populates="events")

# Pydantic 模型
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

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
    created_at: datetime

    class Config:
        from_attributes = True

# 创建数据库引擎
engine = create_engine("sqlite:///./events.db", echo=True)

def reset_db():
    """重置数据库"""
    # 如果数据库文件存在，则删除它
    if os.path.exists("./events.db"):
        try:
            os.remove("./events.db")
            print("已删除现有数据库文件")
        except Exception as e:
            print(f"删除数据库文件时出错: {e}")
            return False
    
    # 创建新的数据库和表
    try:
        Base.metadata.create_all(bind=engine)
        print("已创建新的数据库")
        return True
    except Exception as e:
        print(f"创建新数据库时出错: {e}")
        return False

# 创建所有表
def init_db():
    """初始化数据库"""
    try:
        Base.metadata.create_all(bind=engine)
        print("数据库初始化成功")
        return True
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        return False 