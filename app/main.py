from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import SessionLocal, Base, engine
from app import models
from app.routers import categories, expenses



def create_db_and_tables():
    """
        Creates all database tables defined in SQLAlchemy models.

        Tables are created automatically during application startup
        if they do not already exist.
    """
    Base.metadata.create_all(engine)
    print("Database tables created successfully")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
       Handles application startup events.

       Creates database tables before the application starts serving requests.
    """
    create_db_and_tables()
    yield


# Main FastAPI application instance.
app = FastAPI(lifespan=lifespan)

app.include_router(categories.router)
app.include_router(expenses.router)
