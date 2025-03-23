from .models import SteamBase,Game,UserModel,TokenBase
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from sqlalchemy import select,Integer,cast,delete
from datetime import datetime,timezone
from ..schemas import User
from fastapi import HTTPException


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
    async def get_user(self,async_session:AsyncSession,username:str) -> UserModel:
        result = await async_session.execute(select(UserModel).filter(UserModel.username == username))
        return result.scalars().first()

    async def create_user(self,session:AsyncSession,user:User):
        user_model = UserModel(
                username = user.username,
                hashed_password = user.hashed_password,
                email = user.email,
                steamid = user.steamid,
                steamname= user.steamname
            )

        user_check = await self.get_user(session,user_model.username)

        if user_check:
            raise HTTPException(status_code=400, detail="This username is already registered")
        session.add(user_model)
        await session.commit()

    async def delete_user(self,session:AsyncSession,username:str):
        user = await self.user_get(session,username)

        if user:
            await session.delete(user)
            await session.flush()
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail="User not found")

    async def user_get(self,session,username) -> dict:
        result = await session.execute(select(UserModel).filter(UserModel.username == username))
        return result.scalars().first()

class RefreshTokenORM:
    async def verify_refresh_token(self,session,refresh_token):
        token_get = await session.execute(select(TokenBase).filter(TokenBase.refresh_token == refresh_token))
        result = token_get.scalars().first()

        if not result:
            return False

        return True

    async def delete_refresh_token(self,session:AsyncSession,refresh_token):
        stmt = delete(TokenBase).where(TokenBase.refresh_token == refresh_token)

        await session.execute(stmt)
        await session.commit()

    async def create_refresh_token(self,session:AsyncSession,user_id,refresh_token):
        token_model  =TokenBase(
            user_id = user_id,
            refresh_token=refresh_token
        )

        session.add(token_model)
        await session.commit()
