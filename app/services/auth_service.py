from fastapi import Depends, Form, HTTPException
from starlette.requests import Request

from app.models.user import UserModel
from app.repository.blacklist_repository import BlackListRepository
from app.repository.database import get_async_db
from app.repository.user_repository import UserRepository
from app.repository.refresh_token_repository import RefreshTokenRepository
from app.utils.utils import verify_password, decode_jwt

users = UserRepository()
refresh_token = RefreshTokenRepository()

async def verify_user(session=Depends(get_async_db), username: str = Form(), password: str = Form()) -> UserModel:
    user = await users.get_user(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect password")

    return user


async def user_auth_check(request: Request,session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    decoded_token = decode_jwt(token)
    if await BlackListRepository.verify_blacklist_token(token=token,session=session):
        raise HTTPException(status_code=401, detail="This token is blacklisted")



    return decoded_token
