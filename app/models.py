from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class UserType(enum.Enum):
    CUSTOMER = "customer"
    CHEF = "chef"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_type = Column(Enum(UserType))

    orders = relationship("Order", back_populates="owner")

class OrderStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    COOKING = "cooking"
    READY = "ready"
    DELIVERED = "delivered"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    owner = relationship("User", back_populates="orders")