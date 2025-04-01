from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel
from app.schemas.user import User


class UserRepository:
    """Репозиторій для роботи з користувачами"""

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

    @staticmethod
    async def user_get(session,username) -> dict:
        result = await session.execute(select(UserModel).filter(UserModel.username == username))
        return result.scalars().first()

    @staticmethod
    async def get_user(async_session:AsyncSession,username:str) -> UserModel:
        result = await async_session.execute(select(UserModel).filter(UserModel.username == username))
        return result.scalars().first()
