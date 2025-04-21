# conftest.py
import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection, AsyncTransaction
from sqlalchemy.orm import sessionmaker
from app.infrastructure.db.database import Base
from app.infrastructure.db.models import users_models, steam_models

TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"
engine = create_async_engine(TEST_DATABASE_URL, echo=True)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest_asyncio.fixture(scope="session")
async def connection():
    async with engine.connect() as conn:
        yield conn

@pytest_asyncio.fixture()
async def transaction(connection: AsyncConnection):
    async with connection.begin() as trans:
        yield trans

@pytest_asyncio.fixture()
async def session(connection: AsyncConnection, transaction: AsyncTransaction):
    async_session = AsyncSession(bind=connection, join_transaction_mode="create_savepoint")
    yield async_session
    await transaction.rollback()

