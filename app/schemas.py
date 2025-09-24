"""Pydantic schemas for request validation and response serialization."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

from .models import Currency, OrderStatus


class GiftCardBase(BaseModel):
    name: str = Field(..., max_length=100)
    brand: str = Field(..., max_length=100)
    country: str = Field("DRC", max_length=100)
    currency: Currency = Currency.USD
    price: Decimal = Field(..., gt=0)
    price_cdf: Decimal = Field(..., gt=0)
    description: str = Field("", max_length=1000)
    image_url: str = Field("", max_length=255)
    is_active: bool = True
    inventory: int = Field(0, ge=0)


class GiftCardCreate(GiftCardBase):
    pass


class GiftCardUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    currency: Optional[Currency] = None
    price: Optional[Decimal] = Field(None, gt=0)
    price_cdf: Optional[Decimal] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=1000)
    image_url: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    inventory: Optional[int] = Field(None, ge=0)

    @validator("name", "brand", "country", "description", "image_url", pre=True)
    def empty_strings_to_none(cls, value: Optional[str]) -> Optional[str]:  # noqa: D417
        if isinstance(value, str) and not value.strip():
            return None
        return value


class GiftCardRead(GiftCardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    giftcard_id: int
    quantity: int = Field(1, ge=1)
    currency: Currency = Currency.USD
    customer_email: EmailStr
    notes: str = ""


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    currency: Optional[Currency] = None
    customer_email: Optional[EmailStr] = None
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None


class OrderRead(OrderBase):
    id: int
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
    giftcard: GiftCardRead

    class Config:
        orm_mode = True
