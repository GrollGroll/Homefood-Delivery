from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, dependencies, schemas

router = APIRouter()


@router.post('/create/', response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate,
                       current_user: schemas.User = Depends(dependencies.get_current_user),
                       db: Session = Depends(dependencies.get_db)):
    return await crud.create_order(db, order, user_id=current_user.id)


@router.get('/read/', response_model=List[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    orders = await crud.get_orders(db, skip=skip, limit=limit)
    return orders


@router.get('/status/')
async def get_order_status(order_id: int, db: Session = Depends(dependencies.get_db)):
    status = await crud.get_order_status(db, order_id)
    return status
