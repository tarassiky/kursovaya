import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Water Delivery API is running"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_order():
    payload = {"customer_name": "Иван", "address": "Ленина 1", "bottles": 3}
    response = client.post("/orders", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Иван"
    assert data["status"] == "pending"
    assert "id" in data

def test_get_order():
    payload = {"customer_name": "Петр", "address": "Садовая 5", "bottles": 2}
    create_resp = client.post("/orders", json=payload)
    order_id = create_resp.json()["id"]
    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["customer_name"] == "Петр"

def test_get_not_found():
    response = client.get("/orders/999")
    assert response.status_code == 404