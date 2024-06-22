from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.routers import auth

from .. import crud, dependencies, schemas

router = APIRouter()


@router.post('/create/', response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate,
                       current_user: str = Depends(auth.read_users_me),
                       db: Session = Depends(dependencies.get_db)):
    return await crud.create_order(db, order, user_id=current_user.id)


@router.get('/read_own_orders/', response_model=List[schemas.Order])
async def read_owm_orders(current_user: str = Depends(auth.read_users_me),
                          db: Session = Depends(dependencies.get_db)):
    current_user_id = current_user.id
    orders = crud.get_user_orders(db, current_user_id)
    return orders


@router.get('/status/')
async def get_order_status(order_id: int, db: Session = Depends(dependencies.get_db)):
    order = await crud.get_order(db, order_id)
    return order.status
