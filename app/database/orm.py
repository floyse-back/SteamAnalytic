from .models import SteamBase,Game,UserModel
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from sqlalchemy import select,Integer,cast
from ..schemas import User


class ORM:
    async def get_most_played_page(self,async_session:async_sessionmaker[AsyncSession],page:int,limit:int):
        statement = select(SteamBase).order_by(SteamBase.positive).offset((page - 1) * limit).limit(limit)

        async with async_session() as session:
            result = await session.execute(statement)
            return result.scalars().all()

    async def get_most_discount_games(self,async_session:async_sessionmaker[AsyncSession],page:int,limit:int):
        statement = select(SteamBase).order_by(SteamBase.discount).filter(SteamBase.discount > 80).offset((page - 1) * limit).limit(limit)

        async with async_session() as session:
            result = await session.execute(statement)
            return result.scalars().all()

    async def left_join_where_games(self,async_session:async_sessionmaker[AsyncSession]):
        statements =select(SteamBase).\
        join(Game, cast(SteamBase.appid, Integer) == cast(Game.steam_appid, Integer), isouter=True).\
        filter(Game.steam_appid.is_(None))

        async with async_session() as session:
            result = await session.execute(statements)
            return result.scalars().all()

class UsersORM:
    async def get_user(self,async_session:async_sessionmaker[AsyncSession],username:str):
        async with async_session() as session:
            return await session.execute(select(UserModel).filter(UserModel.username == username))

    async def create_user(self,async_session:async_sessionmaker[AsyncSession],user:User):
        async with async_session() as session:
            user_model = UserModel(
                username = user.username,
                hashed_password = user.hashed_password,
                email = user.email,
                steamid = user.steamid,
                steamname= user.steamname
            )

            session.add(user_model)
            await session.commit()