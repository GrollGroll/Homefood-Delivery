from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import Session

import kafka_producer

from . import models, schemas


async def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


async def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password, user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()


async def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(**order.dict(),
                            owner_id=user_id,
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    user = await get_user_by_id(db, user_id)
    kafka_producer.send_order(user, db_order)
    return db_order


async def get_order(db: Session, order_id: int):
    order = await db.execute(select(models.Order).where(models.Order.id == order_id))
    return order


async def get_user_orders(db: Session, user_id: int):
    orders = await db.execute(select(models.Order).where(models.Order.owner_id == user_id))
    return orders


async def take_order(db: Session, user_id, order_id: int):
    order = await get_order(db, order_id)
    order.chef_id = user_id
    order.status = 'accepted'
    db.add(order)
    db.commit()
    db.refresh(order)
    user = await get_user_by_id(db, user_id)
    kafka_producer.send_order(user, order)
    return order


async def cancel_order(db: Session, order_id: int):
    order = await get_order(db, order_id)
    order.chef_id = None
    order.status = 'pending'
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
