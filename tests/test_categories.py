
def test_get_empty_categories(client):
    response = client.get("/categories/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_category(client):
    response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "description": "Groceries and restaurants"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Food"


def test_create_duplicate_category(client):
    category_data = {
        "name": "Food",
        "description": "Groceries and restaurants"
    }

    client.post("/categories/", json=category_data)

    response = client.post("/categories/", json=category_data)

    assert response.status_code == 409


def test_get_categories_after_create(client):
    category_data = {
        "name": "Food",
        "description": "Groceries and restaurants"
    }

    client.post("/categories/", json=category_data)

    response = client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Food"


def test_get_existing_category(client):
    category_data = {
        "name": "Food",
        "description": "Groceries and restaurants"
    }

    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Food"


def test_get_non_existing_category(client):
    response = client.get("/categories/999")

    assert response.status_code == 404

