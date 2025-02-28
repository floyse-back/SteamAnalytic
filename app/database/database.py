from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import ASYNC_DATABASE_URL


engine = create_async_engine(ASYNC_DATABASE_URL, echo = True)

class Base(DeclarativeBase):
    pass
