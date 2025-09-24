from __future__ import annotations

from app.models import Currency


def test_create_and_list_giftcards(client):
    payload = {
        "name": "Spotify Premium",
        "brand": "Spotify",
        "country": "DRC",
        "currency": Currency.USD.value,
        "price": 12.0,
        "price_cdf": 30000.0,
        "description": "Abonnement musique",
        "image_url": "https://example.com/spotify.png",
        "inventory": 20,
    }
    create_resp = client.post("/giftcards/", json=payload)
    assert create_resp.status_code == 201, create_resp.text
    data = create_resp.json()
    assert data["name"] == payload["name"]
    list_resp = client.get("/giftcards/")
    assert list_resp.status_code == 200
    assert any(item["name"] == payload["name"] for item in list_resp.json())


def test_filter_giftcards(client):
    client.post(
        "/giftcards/",
        json={
            "name": "Amazon US",
            "brand": "Amazon",
            "country": "USA",
            "currency": Currency.USD.value,
            "price": 25.0,
            "price_cdf": 62500.0,
            "description": "",
            "image_url": "",
            "inventory": 10,
        },
    )
    response = client.get("/giftcards/", params={"brand": "amazon"})
    assert response.status_code == 200
    assert len(response.json()) == 1
