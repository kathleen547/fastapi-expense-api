
def test_get_categories(client):
    response = client.get("/categories/")

    assert response.status_code == 200
    assert response.json() == []

