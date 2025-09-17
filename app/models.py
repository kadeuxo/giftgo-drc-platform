"""Database models for the GiftGo platform."""
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Currency(str, enum.Enum):
    """Supported currencies for transactions."""

    USD = "USD"
    CDF = "CDF"


class OrderStatus(str, enum.Enum):
    """Lifecycle statuses for an order."""

    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class GiftCard(Base):
    """Gift card product available for purchase."""

    __tablename__ = "giftcards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    country = Column(String(100), default="DRC", nullable=False)
    currency = Column(String(3), default=Currency.USD.value, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    price_cdf = Column(Numeric(12, 2), nullable=False)
    description = Column(Text, default="", nullable=False)
    image_url = Column(String(255), default="", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    inventory = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    orders = relationship("Order", back_populates="giftcard", cascade="all,delete-orphan")


class Order(Base):
    """Customer order for a gift card."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    giftcard_id = Column(Integer, ForeignKey("giftcards.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    currency = Column(Enum(Currency), default=Currency.USD, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    customer_email = Column(String(255), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    notes = Column(Text, default="", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    giftcard = relationship("GiftCard", back_populates="orders")
