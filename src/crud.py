from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

async def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

async def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password, user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()

async def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(**order.dict(), owner_id=user_id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
