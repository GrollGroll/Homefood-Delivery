from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .crud import get_user_by_id
from .models.database import get_db


async def get_current_user(id: int, db: Session = Depends(get_db)):
    user = await get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user
