# conftest.py
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection, AsyncTransaction, \
    async_sessionmaker
from app.infrastructure.db.database import Base, get_async_db
from app.infrastructure.db.models import users_models, steam_models
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"
engine = create_async_engine(TEST_DATABASE_URL)

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
    async_session = async_sessionmaker(connection=connection,
                                       join_transaction_mode="create_savepoint",
                                       )
    yield async_session
    await transaction.rollback()


@pytest_asyncio.fixture()
async def client(connection:AsyncConnection,transaction:AsyncTransaction):
    async def override_get_async_db() -> AsyncGenerator[AsyncSession, None]:
        async_session  = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield async_session

    app.dependency_overrides[get_async_db] = override_get_async_db
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


    del app.dependency_overrides[get_async_db]

    await transaction.rollback()
