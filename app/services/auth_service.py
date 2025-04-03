from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.models.user import UserModel
from app.repository.blacklist_repository import BlackListRepository
from app.repository.user_repository import UserRepository
from app.repository.refresh_token_repository import RefreshTokenRepository
from app.utils.utils import verify_password, decode_jwt

class AuthService:
    def __init__(self):
        self.users = UserRepository()
        self.black_list_repository = BlackListRepository()

    async def verify_user(self,session:AsyncSession, username: str, password: str) -> UserModel:
        user = await self.users.get_user(session, username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=404, detail="Incorrect password")

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
