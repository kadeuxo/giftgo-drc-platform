"""CRUD helpers for GiftGo data models."""
from __future__ import annotations

from decimal import Decimal
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def list_giftcards(
    db: Session,
    *,
    brand: str | None = None,
    country: str | None = None,
    active_only: bool | None = None,
    search: str | None = None,
) -> Sequence[models.GiftCard]:
    query = select(models.GiftCard)

    if brand:
        query = query.where(models.GiftCard.brand.ilike(f"%{brand}%"))
    if country:
        query = query.where(models.GiftCard.country.ilike(f"%{country}%"))
    if active_only is True:
        query = query.where(models.GiftCard.is_active.is_(True))
    if active_only is False:
        query = query.where(models.GiftCard.is_active.is_(False))
    if search:
        like = f"%{search}%"
        query = query.where(
            models.GiftCard.name.ilike(like)
            | models.GiftCard.brand.ilike(like)
            | models.GiftCard.description.ilike(like)
        )

    query = query.order_by(models.GiftCard.name.asc())
    return db.scalars(query).all()


def get_giftcard(db: Session, giftcard_id: int) -> models.GiftCard | None:
    return db.get(models.GiftCard, giftcard_id)


def create_giftcard(db: Session, payload: schemas.GiftCardCreate) -> models.GiftCard:
    data = payload.dict()
    data['currency'] = data['currency'].value
    giftcard = models.GiftCard(**data)
    db.add(giftcard)
    db.commit()
    db.refresh(giftcard)
    return giftcard


def update_giftcard(
    db: Session, *, giftcard: models.GiftCard, payload: schemas.GiftCardUpdate
) -> models.GiftCard:
    update_data = payload.dict(exclude_unset=True)
    if 'currency' in update_data and update_data['currency'] is not None:
        update_data['currency'] = update_data['currency'].value
    for field, value in update_data.items():
        setattr(giftcard, field, value)
    db.add(giftcard)
    db.commit()
    db.refresh(giftcard)
    return giftcard


def delete_giftcard(db: Session, giftcard: models.GiftCard) -> None:
    db.delete(giftcard)
    db.commit()


def _resolve_price(giftcard: models.GiftCard, currency: models.Currency) -> Decimal:
    if currency == models.Currency.USD:
        return Decimal(giftcard.price)
    if currency == models.Currency.CDF:
        return Decimal(giftcard.price_cdf)
    raise ValueError("Unsupported currency")


def create_order(db: Session, payload: schemas.OrderCreate) -> models.Order:
    giftcard = get_giftcard(db, payload.giftcard_id)
    if not giftcard:
        raise ValueError("Gift card not found")
    if giftcard.inventory < payload.quantity:
        raise ValueError("Insufficient inventory")

    total_amount = _resolve_price(giftcard, payload.currency) * payload.quantity

    order = models.Order(
        giftcard_id=payload.giftcard_id,
        quantity=payload.quantity,
        currency=payload.currency,
        total_amount=total_amount,
        customer_email=payload.customer_email,
        notes=payload.notes,
    )
    giftcard.inventory -= payload.quantity
    db.add(order)
    db.add(giftcard)
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session) -> Sequence[models.Order]:
    query = select(models.Order).order_by(models.Order.created_at.desc())
    return db.scalars(query).all()


def get_order(db: Session, order_id: int) -> models.Order | None:
    return db.get(models.Order, order_id)


def update_order(db: Session, order: models.Order, payload: schemas.OrderUpdate) -> models.Order:
    update_data = payload.dict(exclude_unset=True)
    if "quantity" in update_data:
        difference = update_data["quantity"] - order.quantity
        if order.giftcard.inventory < difference:
            raise ValueError("Insufficient inventory for requested quantity")
        order.giftcard.inventory -= difference
        order.total_amount = _resolve_price(order.giftcard, update_data.get("currency", order.currency)) * update_data[
            "quantity"
        ]
    if "currency" in update_data and update_data["currency"]:
        new_quantity = update_data.get("quantity", order.quantity)
        order.total_amount = _resolve_price(order.giftcard, update_data["currency"]) * new_quantity

    for field, value in update_data.items():
        setattr(order, field, value)

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order: models.Order) -> None:
    order.giftcard.inventory += order.quantity
    db.delete(order)
    db.commit()
