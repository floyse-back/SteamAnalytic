from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel
from app.schemas.user import User
from app.utils.utils import hashed_password, verify_password


class UserNotFound(Exception):
    pass


class UserRepository:
    """Репозиторій для роботи з користувачами"""

    async def create_user(self,session:AsyncSession,user = User):
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

    @staticmethod
    async def get_user_for_id(user_id:int,session:AsyncSession):
        stmt = select(UserModel).filter(UserModel.id==user_id)
        result =await session.execute(stmt)

        return result.scalars().first()

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

    @staticmethod
    async def user_update(session,id:int,user:User):
        user_model = await session.execute(select(UserModel).filter(UserModel.id == id))
        my_user = user_model.scalars().first()
        if verify_password(user.hashed_password, my_user.hashed_password):
            if my_user.username != user.username:
                verify_unique = await session.execute(select(UserModel).filter(UserModel.email == user.email or UserModel.username == user.username))
            else:
                verify_unique = await session.execute(select(UserModel).filter(UserModel.email == user.email))

            if not verify_unique.scalars().first():
                my_user.username = user.username
                my_user.email = user.email
                my_user.steamid = user.steamid
            else:
                 raise UserNotFound(f"User {user.username} not found")
        else:
             raise UserNotFound("User password is incorrect")

        await session.commit()
