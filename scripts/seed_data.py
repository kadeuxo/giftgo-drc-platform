"""Utility script to seed the database with gift card data from JSON."""
from __future__ import annotations

import json
from pathlib import Path

from app import crud, database, schemas, models

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "giftcards.json"


def run() -> None:
    database.Base.metadata.create_all(bind=database.engine)
    with database.SessionLocal() as session:
        existing = session.query(models.GiftCard).count()
        if existing:
            print("Gift cards already present, skipping seeding.")
            return
        raw = json.loads(DATA_FILE.read_text())
        for item in raw:
            payload = schemas.GiftCardCreate(**item)
            crud.create_giftcard(session, payload)
        print(f"Seeded {len(raw)} gift cards.")


if __name__ == "__main__":
    run()
