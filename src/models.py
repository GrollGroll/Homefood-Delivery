import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class UserType(enum.Enum):
    CUSTOMER = 'customer'
    CHEF = 'chef'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    user_type = Column(Enum(UserType))
    telegram_chat_id = Column(Integer)

    orders = relationship('Order', back_populates='owner')


class OrderStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    COOKING = 'cooking'
    READY = 'ready'
    DELIVERED = 'delivered'


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    owner_id = Column(Integer, ForeignKey('users.id'))
    chef_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    owner = relationship('User', back_populates='orders')


class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, unique=True, nullable=False)
