from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import ASYNC_DATABASE_URL
from sqlalchemy.ext.asyncio import async_sessionmaker


engine = create_async_engine(ASYNC_DATABASE_URL, echo = True)

session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
