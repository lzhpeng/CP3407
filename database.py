from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, User, Event
from datetime import datetime
from typing import List, Optional

SQLALCHEMY_DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 数据库依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 用户相关操作
def create_user(db: SessionLocal, username: str, email: str, hashed_password: str) -> User:
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: SessionLocal, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: SessionLocal, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: SessionLocal, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    from main import verify_password
    if not verify_password(password, user.hashed_password):
        return None
    return user

# 事件相关操作
def create_event(
    db: SessionLocal,
    event_name: str,
    event_date: datetime,
    location: str,
    description: str,
    creator_id: int
) -> Event:
    db_event = Event(
        event_name=event_name,
        event_date=event_date,
        location=location,
        description=description,
        creator_id=creator_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event_by_id(db: SessionLocal, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()

def get_events_by_date(db: SessionLocal, date: datetime) -> List[Event]:
    return db.query(Event).filter(Event.event_date == date).all()

def get_events_by_creator(db: SessionLocal, creator_id: int) -> List[Event]:
    return db.query(Event).filter(Event.creator_id == creator_id).all()

def update_event(
    db: SessionLocal,
    event_id: int,
    event_name: str = None,
    event_date: datetime = None,
    location: str = None,
    description: str = None
) -> Optional[Event]:
    db_event = get_event_by_id(db, event_id)
    if db_event:
        if event_name is not None:
            db_event.event_name = event_name
        if event_date is not None:
            db_event.event_date = event_date
        if location is not None:
            db_event.location = location
        if description is not None:
            db_event.description = description
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: SessionLocal, event_id: int) -> bool:
    db_event = get_event_by_id(db, event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False 