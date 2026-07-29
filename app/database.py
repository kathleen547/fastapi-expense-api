from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "api.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# SQLite database URL.
# The database file will be created locally as api.db.
#SQLALCHEMY_DATABASE_URL = "sqlite:///api.db"

# SQLAlchemy engine responsible for connecting the application to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})

# Session factory used to create database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()