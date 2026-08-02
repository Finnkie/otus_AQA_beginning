import pytest
from utils.http_client import HttpRequests

def test_get_random_dog():
    client = HttpRequests()

    response = client.get("/breeds/image/random")
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "success"
    
    assert "message" in data
    assert data["message"] is not None
    assert data["message"].endswith(".jpg")
    
    print(f"\n✅ Случайная собака: {data['message']}")