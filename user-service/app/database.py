# user-service/database.py
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://ziakhan:my_password@postgres_db/mydatabase"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
