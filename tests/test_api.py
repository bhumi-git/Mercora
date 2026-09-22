def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Mercora API is running"

def test_campaigns_endpoint_empty(client):
    response = client.get("/api/v1/campaigns")
    assert response.status_code == 200
    assert response.json() == []

def test_upload_requires_api_key(client):
    response = client.post("/api/v1/datasets", files={"file": ("test.csv", "a,b\n1,2", "text/csv")})
    assert response.status_code in (401, 422)