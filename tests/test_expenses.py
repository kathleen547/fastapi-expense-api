

def test_get_empty_expenses(client):
    response = client.get("/expenses/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_expense_with_existing_category(client, expense_data):
    response = client.post("/expenses/", json=expense_data)

    assert response.status_code == 201
    assert response.json()["title"] == expense_data["title"]
    assert response.json()["amount"] == expense_data["amount"]
    assert response.json()["notes"] == expense_data["notes"]


def test_create_expense_with_non_existing_category(client):
    expense_data = {
        "title": "Pizza",
        "amount": 35.50,
        "date": "2026-07-31",
        "category_id": 999,
        "notes": "Dinner"
    }

    response = client.post("/expenses/", json=expense_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_get_expenses_after_create(client, created_expense):
    response =  client.get("/expenses/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == created_expense["id"]
    assert response.json()[0]["title"] == "Pizza"


def test_get_expense(client, created_expense):
    expense_id = created_expense["id"]

    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["id"] == expense_id
    assert response.json()["title"] == created_expense["title"]
    assert response.json()["amount"] == created_expense["amount"]
    assert response.json()["category_id"] == created_expense["category_id"]


def test_non_existing_expense(client):
    response = client.get(f"/expenses/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_update_existing_expense(client, created_category, created_expense):
    expense_id = created_expense["id"]
    changed_expense = {
        "title": "Sushi",
        "amount": 45.50,
        "date": "2026-07-31",
        "category_id": created_category["id"],
        "notes": "Dinner",
    }

    response = client.put(f"/expenses/{expense_id}", json=changed_expense)
    assert response.status_code == 200

    get_response = client.get(f"/expenses/{expense_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Sushi"


def test_update_non_existing_expense(client, created_category):
    changed_expense = {
        "title": "Sushi",
        "amount": 45.50,
        "date": "2026-07-31",
        "category_id": created_category["id"],
        "notes": "Dinner",
    }

    response = client.put(f"/expenses/999", json=changed_expense)

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_delete_existing_expense(client, created_expense):
    expense_id = created_expense["id"]

    response = client.delete(f"/expenses/{expense_id}")

    assert response.status_code == 200


def test_delete_non_existing_expense(client):
    response = client.delete("/expenses/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

