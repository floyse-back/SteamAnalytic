from datetime import datetime, timezone, timedelta

from app.domain.users.models import UserModel
from app.utils.utils import token_config, encode_jwt


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
        "user_id" : user.id,
        "sub": user.username,
        "type": "access_token",
        "username": user.username,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=token_config.access_token_expires),
    }

    token = encode_jwt(payload)
    return token
