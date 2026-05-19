from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import SessionLocal, Base, engine
from app import models



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables():
    Base.metadata.create_all(engine)
    print("Database tables created successfully")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
