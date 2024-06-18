from fastapi import FastAPI
from .routers import users, orders
# from .database import engine, Base
from .core.config import app_settings

app = FastAPI(title=app_settings.project_name)

# Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
