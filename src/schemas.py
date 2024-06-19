import enum
from datetime import datetime

from pydantic import BaseModel


class UserType(str, enum.Enum):
    customer = 'customer'
    chef = 'chef'


class UserBase(BaseModel):
    username: str
    user_type: UserType


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class OrderStatus(str, enum.Enum):
    pending = 'pending'
    accepted = 'accepted'
    cooking = 'cooking'
    ready = 'ready'
    delivered = 'delivered'


class OrderBase(BaseModel):
    title: str
    description: str


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    status: OrderStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
