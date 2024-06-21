from fastapi import FastAPI

from .core.config import app_settings
from .routers import orders, users

app = FastAPI(title=app_settings.project_name)

app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(orders.router, prefix='/orders', tags=['orders'])
