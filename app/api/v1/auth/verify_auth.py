from datetime import datetime, timezone, timedelta

from app.database.orm import UsersORM
from app.models.user import UserModel
from fastapi import Form, Depends, HTTPException
from app.database.database import get_async_db
from .utils import verify_password, token_config, encode_jwt


async def verify_user_account(users_db,username:str = Form(),password:str = Form()):
    pass


users = UsersORM()

async def verify_user(session = Depends(get_async_db),username:str = Form(),password:str = Form()) -> UserModel:
    user  = await users.get_user(session,username)
    if not user:
        raise HTTPException(status_code=404,detail = "User not found")

    if not verify_password(password,user.hashed_password.encode("utf-8")):
        raise HTTPException(status_code=404,detail = "Incorrect password")

    return user


def create_refresh_token(user: UserModel) -> str:
    payload = {
        "user_id": user.id,
        "sub": user.username,
        "type":"refresh_token",
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=token_config.refresh_token_expires),
    }

    token = encode_jwt(payload)
    return token


def create_access_token(user: UserModel) -> str:
    payload = {
        "sub": user.username,
        "type": "access_token",
        "username": user.username,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=token_config.access_token_expires),
    }

    token = encode_jwt(payload)
    return token
