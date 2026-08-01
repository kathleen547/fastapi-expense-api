
def test_get_empty_categories(client):
    response = client.get("/categories/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_category(client, category_data):
    response = client.post(
        "/categories/",
        json=category_data
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Food"


def test_create_duplicate_category(client, category_data):
    client.post("/categories/", json=category_data)

    response = client.post("/categories/", json=category_data)

    assert response.status_code == 409


def test_get_categories_after_create(client, created_category):
    response = client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Food"


def test_get_existing_category(client, created_category):
    category_id = created_category["id"]

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Food"


def test_get_non_existing_category(client):
    response = client.get("/categories/999")

    assert response.status_code == 404


def test_update_existing_category(client, created_category):
    category_id = created_category["id"]

    changed_data = {
        "name": "Pizza",
        "description": "Groceries and restaurants"
    }

    response = client.put(f"/categories/{category_id}", json=changed_data)

    assert response.status_code == 200

    get_response = client.get(f"/categories/{category_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == category_id
    assert get_response.json()["name"] == "Pizza"


def test_update_non_existing_category(client):
    changed_data = {
        "name": "Pizza",
        "description": "Groceries and restaurants"
    }
    response = client.put("/categories/999", json=changed_data)
    assert response.status_code == 404


def test_delete_existing_category(client, created_category):
    category_id = created_category["id"]
    response = client.delete(f"/categories/{category_id}")

    assert response.status_code == 200


def test_delete_non_existing_category(client):
    response = client.delete("/categories/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"







