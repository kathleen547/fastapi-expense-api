import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

from app import models


TEST_DATABASE_URL = "sqlite:///./tests/test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine

)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def category_data():
    return {
        "name": "Food",
        "description": "Groceries and restaurants",
    }


@pytest.fixture
def created_category(client, category_data):
    response = client.post("/categories/", json=category_data)

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def expense_data(created_category):
    return {
        "title": "Pizza",
        "amount": 35.50,
        "date": "2026-07-31",
        "category_id": created_category["id"],
        "notes": "Dinner",
    }


@pytest.fixture
def created_expense(client, expense_data):
    response = client.post("/expenses/", json=expense_data)

    assert response.status_code == 201

    return response.json()