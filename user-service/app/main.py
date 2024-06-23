# user-service/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from .database import init_db, get_session
from .models import User
from .crud import create_user, get_user, get_users, update_user, delete_user

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/users/", response_model=User)
def create_user_endpoint(user: User, session: Session = Depends(get_session)):
    return create_user(session, user)

@app.get("/users/{user_id}", response_model=User)
def get_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[User])
def get_users_endpoint(session: Session = Depends(get_session)):
    return get_users(session)

@app.put("/users/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user_data: User, session: Session = Depends(get_session)):
    updated_user = update_user(session, user_id, user_data.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    deleted_user = delete_user(session, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
