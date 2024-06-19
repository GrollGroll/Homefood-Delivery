import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from .. import dependencies
from ..models import Token, User

router = APIRouter()


# Авторизация
@router.post('/auth')
async def auth_user(form_data: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(dependencies.get_db)):
    existing_user = await db.execute(select(User).where(User.username == form_data.username))
    existing_user = existing_user.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=400, detail='User not found')
    elif not existing_user.password == form_data.password:
        raise HTTPException(status_code=400, detail='Wrong password')
    token = secrets.token_urlsafe(10)
    new_token = Token(user_id=existing_user.id, token=token)
    db.add(new_token)
    await db.commit()
    return {'access_token': token, 'token_type': 'bearer'}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')


# Вернуть информацию о пользователе
@router.get('/users/me')
async def read_users_me(token: str = Depends(oauth2_scheme),
                        db: Session = Depends(dependencies.get_db)):
    result = await db.execute(select(Token).join(User).where(Token.token == token))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid authentication credentials')
    return user
