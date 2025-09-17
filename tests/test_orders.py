from __future__ import annotations

from decimal import Decimal

from app.models import Currency


def create_giftcard(client):
    payload = {
        "name": "Disney+",
        "brand": "Disney",
        "country": "DRC",
        "currency": Currency.USD.value,
        "price": 10.0,
        "price_cdf": 25000.0,
        "description": "",
        "image_url": "",
        "inventory": 5,
    }
    response = client.post("/giftcards/", json=payload)
    return response.json()["id"]


def test_create_order(client):
    giftcard_id = create_giftcard(client)
    payload = {
        "giftcard_id": giftcard_id,
        "quantity": 2,
        "currency": Currency.USD.value,
        "customer_email": "test@example.com",
        "notes": "Urgent",
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert Decimal(data["total_amount"]) == Decimal("20.00")
    assert data["giftcard"]["inventory"] == 3


def test_order_inventory_validation(client):
    giftcard_id = create_giftcard(client)
    payload = {
        "giftcard_id": giftcard_id,
        "quantity": 20,
        "currency": Currency.USD.value,
        "customer_email": "test@example.com",
        "notes": "",
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 400
    assert "Insufficient" in response.json()["detail"]
