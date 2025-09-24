# giftgo-drc-platform

MVP for GiftGo DRC – digital gift-card marketplace.

## FastAPI backend

This repository now ships with a production-ready FastAPI backend that exposes REST endpoints for managing gift cards and customer orders.

### Features

- CRUD endpoints for gift cards with filtering and search support
- Order management with automatic inventory tracking and currency-aware totals
- SQLite persistence by default (configurable via environment variables)
- Pydantic validation and typed responses
- Seed script to populate the database from `data/giftcards.json`
- Pytest suite covering the core business flows

### Getting started

1. **Install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Seed the database (optional)**

   ```bash
   python scripts/seed_data.py
   ```

3. **Run the API**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at <http://127.0.0.1:8000>. Interactive documentation is served at `/docs`.

4. **Run the automated tests**

   ```bash
   pytest
   ```

### Configuration

Configuration values can be supplied through environment variables prefixed with `GIFTGO_` or via a `.env` file. Key options include:

- `GIFTGO_DATABASE_URL`: SQLAlchemy-compatible database URL (defaults to a SQLite file `giftgo.db`)
- `GIFTGO_ALLOW_ORIGINS`: comma-separated list of origins allowed for CORS (defaults to allowing all)

### API overview

- `GET /health` – Service status check
- `GET /giftcards` – List gift cards with optional filters
- `POST /giftcards` – Create a new gift card
- `GET /giftcards/{id}` – Retrieve a single gift card
- `PUT /giftcards/{id}` – Update a gift card
- `DELETE /giftcards/{id}` – Remove a gift card
- `GET /orders` – List orders
- `POST /orders` – Place a new order
- `GET /orders/{id}` – Retrieve an order
- `PUT /orders/{id}` – Update an order
- `DELETE /orders/{id}` – Cancel an order
