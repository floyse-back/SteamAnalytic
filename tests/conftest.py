import random
from datetime import date
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection, AsyncTransaction, \
    async_sessionmaker
from app.infrastructure.db.database import Base, get_async_db
from app.infrastructure.db.models import steam_models
from app.infrastructure.db.models.steam_models import Game, Category, Publisher, Ganres
from app.infrastructure.db.models.users_models import UserModel
from app.main import app
from app.utils.config import TEST_DATABASE_URL
from app.utils.utils import hashed_password
import asyncio

#TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"
engine = create_async_engine(TEST_DATABASE_URL)

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest_asyncio.fixture(scope="function")
async def connection():
    async with engine.connect() as conn:
        yield conn

@pytest_asyncio.fixture()
async def transaction(connection: AsyncConnection):
    async with connection.begin() as trans:
        yield trans

@pytest_asyncio.fixture()
async def session(connection: AsyncConnection, transaction: AsyncTransaction):
    async_session = async_sessionmaker(bind=connection,
                                       join_transaction_mode="create_savepoint",
                                       expire_on_commit=False,
                                       autoflush=False,
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

@pytest_asyncio.fixture(scope="function")
async def steamgames(session: async_sessionmaker[AsyncSession]):
    async with session() as s:
        steam_games = [
            steam_models.SteamBase(
                name = f"Item {i}",
                appid = f"{i}",
                developer = f"Random Nick{i}",
                publisher= f"Random Publisher{i}",
                positive = random.randint(1,15000),
                negative = random.randint(1,15000),
                average_forever=random.randint(1,1000),
                average_2weeks=random.randint(1,200),
                median_2weeks=random.randint(1,500),
                median_forever=random.randint(1,400),
                price=random.randint(0,1000),
                discount=random.randint(0,100),
                img_url="img.connect//"
            ) for i in range(0,100)
        ]
        s.add_all(steam_games)
        await s.commit()


@pytest_asyncio.fixture(scope="function")
async def games(session: async_sessionmaker[AsyncSession]):
    async def get_or_create(s:AsyncSession,model,**kwargs):
        instance = await s.execute(select(model).filter_by(**kwargs))
        instance = instance.scalars().first()

        if instance:
            return instance
        else:
            instance = model(**kwargs)
            s.add(instance)

            await s.flush()
            return instance


    async with session() as s:
        await s.execute(text("DELETE FROM gamesdetails"))
        # await s.execute(text("DELETE FROM categories"))
        # await s.execute(text("DELETE FROM publishers"))
        # await s.execute(text("DELETE FROM ganres"))
        games_list=[]
        for i in range(100):
            game = Game(
                steam_appid=i,
                name=f"Item {i}",
                is_free=random.choice([True, False]),
                short_description=f"This is a test description for Game {i}.",
                requirements={
                    "minimum": f"Minimum system requirements for Game {i}",
                    "recommended": f"Recommended system requirements for Game {i}"
                },
                initial_price=random.randint(0, 5000),
                final_price=random.randint(0, 5000),
                final_formatted_price=f"${random.randint(0, 60)}.99",
                metacritic=str(random.randint(50, 100)) if random.choice([True, False]) else None,
                discount=random.randint(0, 90),
                achievements={"count": random.randint(0, 100)} if random.choice([True, False]) else {},
                recomendations=random.randint(0, 100000),
                img_url=f"https://cdn.fakeimage.com/game{i}.jpg",
                last_updated=date.today()
            )
            for k in range(0,random.randint(0,10)):
                game.game_categories.append(
                    await get_or_create(
                        s=s,
                        model=Category,
                        category_name=f"Random Category {k}"
                    )
                )
                game.game_publisher.append(
                    await get_or_create(
                        s=s,
                        model=Publisher,
                        publisher_name = f"Random Publisher {k}"
                    )
                )
                game.game_ganre.append(
                    await get_or_create(
                        s=s,
                        model=Ganres,
                        ganres_name = f"Random Ganre {k}"
                    )
                )

            games_list.append(
                game
            )
        s.add_all(games_list)
        await s.commit()

@pytest_asyncio.fixture(scope="function")
async def users(session: async_sessionmaker[AsyncSession]):
    async with session() as s:
        await s.execute(text("DELETE FROM users"))
        users = [
            UserModel(username="floysefake", hashed_password=hashed_password("password"),
                      email="new@_gmail.com",role="user", is_active=True, steamid="4353454336",
                      steamname="NewSte"),
            UserModel(username="admin_ivan", hashed_password=hashed_password("hashedpass1"),
                      email="ivan.admin@example.com", is_active=True, role="admin", steamid="76561198123456789",
                      steamname="AdminIvan"),
            UserModel(username="admin_olena", hashed_password=hashed_password("hashedpass2"),
                      email="olena.admin@example.com", is_active=True, role="admin", steamid="76561198123456788",
                      steamname="AdminOlena"),

            UserModel(username="user_dmytro", hashed_password=hashed_password("hashedpass3"),
                      email="dmytro.user@example.com", is_active=False, steamid="76561198123456787",
                      steamname="DmytroTheGreat"),
            UserModel(username="user_maryna", hashed_password=hashed_password("hashedpass4"),
                      email="maryna.user@example.com", is_active=True, steamid="76561198123456786",
                      steamname="MarynaM"),
            UserModel(username="user_artem", hashed_password=hashed_password("hashedpass5"),
                      email="artem.user@example.com", is_active=True, steamid="76561198123456785",
                      steamname="ArtemPlayz"),
            UserModel(username="user_natali", hashed_password=hashed_password("hashedpass6"),
                      email="natali.user@example.com", is_active=False, steamid="76561198123456784",
                      steamname="NataliGames"),
            UserModel(username="user_bohdan", hashed_password=hashed_password("hashedpass7"),
                      email="bohdan.user@example.com", is_active=True, steamid="76561198123456783",
                      steamname="BohdanK"),
            UserModel(username="user_viktor", hashed_password=hashed_password("hashedpass8"),
                      email="viktor.user@example.com", is_active=True, steamid="76561198123456782",
                      steamname="ViktorV"),
            UserModel(username="user_yana", hashed_password=hashed_password("hashedpass9"),
                      email="yana.user@example.com", is_active=False, steamid="76561198123456781",
                      steamname="YanaSmile"),
            UserModel(username="user_oleh", hashed_password=hashed_password("hashedpass10"),
                      email="oleh.user@example.com", is_active=True, steamid="76561198123456780", steamname="Oleh_Pro"),
        ]
        s.add_all(users)
        await s.commit()

@pytest_asyncio.fixture(scope="function")
async def login(client:AsyncClient,users):

    response = await client.post("/auth/login",params={"username":"floysefake","password":"password"})
    data = response.json()

    return {
        "client":client,
        "username":"floysefake",
        "access_token":data.get("access_token")
    }

@pytest_asyncio.fixture(scope="function")
async def login_admin(client:AsyncClient,users):
    response = await client.post("/auth/login",params={"username":"admin_ivan","password":"hashedpass1"})

    data = response.json()

    return {
        "client":client,
        "username":"admin_ivan",
        "access_token":data.get("access_token")
    }
