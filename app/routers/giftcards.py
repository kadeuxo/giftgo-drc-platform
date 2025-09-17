"""API routes for working with gift cards."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/giftcards", tags=["giftcards"])


@router.get("/", response_model=list[schemas.GiftCardRead])
def read_giftcards(
    *,
    db: Session = Depends(get_db),
    brand: str | None = Query(None, description="Filter by brand name"),
    country: str | None = Query(None, description="Filter by country"),
    active_only: bool | None = Query(None, description="Show only active or inactive cards"),
    search: str | None = Query(None, description="Search by name, brand or description"),
):
    """Return a filtered list of gift cards."""

    return crud.list_giftcards(
        db,
        brand=brand,
        country=country,
        active_only=active_only,
        search=search,
    )


@router.post("/", response_model=schemas.GiftCardRead, status_code=status.HTTP_201_CREATED)
def create_giftcard(*, db: Session = Depends(get_db), payload: schemas.GiftCardCreate):
    """Create a new gift card."""

    return crud.create_giftcard(db, payload)


@router.get("/{giftcard_id}", response_model=schemas.GiftCardRead)
def read_giftcard(*, db: Session = Depends(get_db), giftcard_id: int):
    """Return a single gift card by identifier."""

    giftcard = crud.get_giftcard(db, giftcard_id)
    if not giftcard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift card not found")
    return giftcard


@router.put("/{giftcard_id}", response_model=schemas.GiftCardRead)
def update_giftcard(
    *, db: Session = Depends(get_db), giftcard_id: int, payload: schemas.GiftCardUpdate
):
    """Update an existing gift card."""

    giftcard = crud.get_giftcard(db, giftcard_id)
    if not giftcard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift card not found")
    return crud.update_giftcard(db, giftcard=giftcard, payload=payload)


@router.delete("/{giftcard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_giftcard(*, db: Session = Depends(get_db), giftcard_id: int):
    """Delete a gift card."""

    giftcard = crud.get_giftcard(db, giftcard_id)
    if not giftcard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift card not found")
    crud.delete_giftcard(db, giftcard)
