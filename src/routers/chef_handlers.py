from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, dependencies
from . import auth

router = APIRouter()


def check_chef(user):
    if user.user_type != 'chef':
        raise HTTPException(403, detail='You are not chef!')
    else:
        return True


@router.post('/take_order/')
async def take_order(order_id: int, user: str = Depends(auth.read_users_me),
                     db: Session = Depends(dependencies.get_db)):
    if check_chef(user):
        taken_order = await crud.take_order(db, user.user_id, order_id)
        return taken_order


@router.post('/cancel_order/')
async def cancel_order(order_id: int, user: str = Depends(auth.read_users_me),
                       db: Session = Depends(dependencies.get_db)):
    if check_chef(user):
        taken_order = await crud.cancel_order(db, order_id)
        return taken_order
