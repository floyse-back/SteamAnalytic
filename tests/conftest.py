import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest

from app.infrastructure.db.repository import Base
from app.infrastructure.db.models.users_models import UserModel
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///mytest.db"

test_engine = create_async_engine(DATABASE_URL)

TestingSession = async_sessionmaker(test_engine, expire_on_commit=False)

async def override_get_db():
    async with TestingSession() as session:
        yield session

@pytest_asyncio.fixture(scope = "session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def async_session(event_loop):
    session = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
    )

    async with session() as s:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

        async with session() as s:
            async with test_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

        await test_engine.dispose()

@pytest.fixture
async def register_user():
    """Фікстура для створення тестового користувача."""
    user = UserModel(
        username="john_doe",
        hashed_password="hashed_password_123",
        email="john.doe@example.com",
        steamid="123456789",
        steamname="JohnDoeGamer"
    )
    async with TestingSession() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user  # Повертаємо пов'язаний із сесією об'єкт