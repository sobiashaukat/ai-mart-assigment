# user-service/crud.py
from sqlmodel import Session, select
from .models import User
from .kafka_utils import produce_event
import asyncio

def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    asyncio.run(produce_event("user-events", {"event": "UserCreated", "user": user.dict()}))
    return user

def update_user(session: Session, user_id: int, user_data: dict):
    user = session.get(User, user_id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        session.commit()
        session.refresh(user)
        asyncio.run(produce_event("user-events", {"event": "UserUpdated", "user": user.dict()}))
        return user
    return None

def delete_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        asyncio.run(produce_event("user-events", {"event": "UserDeleted", "user": user.dict()}))
        return user
    return None
