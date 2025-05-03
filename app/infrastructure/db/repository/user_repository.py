from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.users_models import UserModel
from app.application.dto.user_dto import User, UserMe
from app.domain.users.repository import IUserRepository
from app.infrastructure.exceptions.exception_handler import InfrastructureUserRegister


class UserRepository(IUserRepository):
    """Репозиторій для роботи з користувачами"""

    async def create_user(self,session:AsyncSession,user = User):
        user_model = UserModel(
                username = user.username,
                hashed_password = user.hashed_password,
                role="user",
                is_active = False,
                email = user.email,
                steamid = user.steamid,
            )

        user_check = await self.get_user(session,username=user.username,email=user.email)

        if user_check:
            raise InfrastructureUserRegister()
        session.add(user_model)
        await session.commit()

    async def get_user_for_id(self,user_id:int,session:AsyncSession) -> UserModel:
        stmt = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(stmt)

        return result.scalars().first()

    async def get_user_for_email(self,email:str,session:AsyncSession)->UserModel:
        stmt = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(stmt)

        return result.scalars().first()

    async def delete_user(self,session:AsyncSession,user:UserModel):
        await session.delete(user)
        await session.flush()
        await session.commit()

    async def get_user(self,session:AsyncSession,username:str,email :str|None = None) -> UserModel:
        if email is None:
            result = await session.execute(select(UserModel).where(UserModel.username == username))
        else:
            result = await session.execute(select(UserModel).where(or_(UserModel.username == username, UserModel.email == email)))
        return result.scalars().first()

    async def user_update(self,session,my_user,user:UserMe):
        if my_user.username == user.username and user.email == my_user.email:
            verify_unique = False
        elif my_user.username != user.username and user.email != my_user.email:
            verify_unique = await session.execute(select(UserModel).filter(UserModel.email == user.email or UserModel.username == user.username))
        elif my_user.email == user.email:
            verify_unique = await session.execute(select(UserModel).filter(UserModel.username == user.username))
        else:
            verify_unique = await session.execute(select(UserModel).filter(UserModel.email == user.email))

        if type(verify_unique)==bool or not verify_unique.scalars().first():
            my_user.username = user.username
            my_user.email = user.email
            my_user.steamid = user.steamid
        else:
             raise InfrastructureUserRegister(f"User {user.username} not found")

        await session.commit()

        if my_user:
            return my_user
        return False

    async def delete_refresh_tokens(self,session:AsyncSession,id):
        user_model = await session.execute(
            select(UserModel).filter(UserModel.id == id)
        )
        my_user = user_model.scalars().first()

        return my_user



