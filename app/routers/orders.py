from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, dependencies

router = APIRouter()

@router.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, current_user: schemas.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    return await crud.create_order(db, order, user_id=current_user.id)

@router.get("/orders/", response_model=List[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    orders = await crud.get_orders(db, skip=skip, limit=limit)
    return orders
