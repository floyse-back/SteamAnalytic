from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from .database.database import engine
from .routers import users,steam,analytics
app = FastAPI()

app.include_router(users.router,prefix="/users",tags=["Users"])
app.include_router(steam.router,prefix="/steam",tags=["steam"])
app.include_router(analytics.router,prefix="/analytics",tags=["analytics"])

session = async_sessionmaker(bind = engine, expire_on_commit = False)


