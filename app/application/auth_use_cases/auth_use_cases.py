from fastapi import HTTPException,Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.utils.config import TokenConfig
from app.domain.users.models import UserModel
from app.infrastructure.db.repository.blacklist_repository import BlackListRepository
from app.infrastructure.db.repository.refresh_token_repository import RefreshTokenRepository
from app.infrastructure.db.repository.user_repository import UserRepository
from app.domain.users.schemas import TokenType, User
from app.utils.auth_utils import create_access_token, create_refresh_token
from app.utils.utils import verify_password, decode_jwt, hashed_password


class AuthService:
    def __init__(self):
        self.users = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()
        self.black_list_repository = BlackListRepository()
        self.token_config = TokenConfig()

    async def check_cookie_auth(self,request: Request):
        if not request.cookies.get("access_token") and not request.cookies.get("refresh_token"):
            return True
        return False

    async def verify_user(self,session:AsyncSession, username: str, password: str) -> UserModel:
        user = await self.users.get_user(session, username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return user

    async def user_auth_check(self,request: Request, session:AsyncSession):
        "Перевіряє token і якщо він є повертає дані з цього токена"
        token = request.cookies.get("refresh_token")
        if not token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        decoded_token = decode_jwt(token)
        if await self.black_list_repository.verify_blacklist_token(token=token, session=session):
            raise HTTPException(status_code=401, detail="This token is blacklisted")

        return decoded_token

    async def user_login(self,response:Response,session:AsyncSession,user)->TokenType:
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        await self.refresh_token_repository.create_refresh_token(
            session=session,
            user_id=user.id,
            refresh_token=refresh_token
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=self.token_config.access_token_expires * 60
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=self.token_config.refresh_token_expires * 60
        )

        return TokenType(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def register_user(self,user:User,session:AsyncSession):
        user.hashed_password = hashed_password(user.hashed_password).decode("utf-8")
        await self.users.create_user(session, user)
        return {"message":"Register successful"}

    async def delete_from_user(self,access_token,user_password,session:AsyncSession):
        if not access_token:
            raise HTTPException(
                status_code=401,
                detail="No autorization user"
            )
        refresh_token_data = decode_jwt(access_token)

        user = await self.users.get_user_for_id(user_id=refresh_token_data.get("user_id"),session=session)

        #Перевірка на правильність введеного пароля
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        if not verify_password(user_password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect password",
            )

        await self.users.delete_user(session,user)

    async def refresh_token(self,response:Response,refresh_token:str,user:str,session:AsyncSession):
        user_model = await self.users.get_user_for_id(user_id=int(user), session=session)

        access_token = create_access_token(user=user_model)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=self.token_config.access_token_expires * 60
        )

        return TokenType(
            access_token=access_token,
            refresh_token=refresh_token
        )

