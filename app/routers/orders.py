"""API routes for handling gift card orders."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[schemas.OrderRead])
def read_orders(*, db: Session = Depends(get_db)):
    """Return a list of orders."""

    return crud.list_orders(db)


@router.post("/", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(*, db: Session = Depends(get_db), payload: schemas.OrderCreate):
    """Create a new order."""

    try:
        return crud.create_order(db, payload)
    except ValueError as exc:  # pragma: no cover - defensive, triggered in tests
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{order_id}", response_model=schemas.OrderRead)
def read_order(*, db: Session = Depends(get_db), order_id: int):
    """Return details of a single order."""

    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=schemas.OrderRead)
def update_order(
    *, db: Session = Depends(get_db), order_id: int, payload: schemas.OrderUpdate
):
    """Update an existing order."""

    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    try:
        return crud.update_order(db, order=order, payload=payload)
    except ValueError as exc:  # pragma: no cover - defensive, triggered in tests
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(*, db: Session = Depends(get_db), order_id: int):
    """Delete an order and restore inventory."""

    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    crud.delete_order(db, order)
