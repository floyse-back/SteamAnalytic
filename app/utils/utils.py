import bcrypt
import jwt
from fastapi import HTTPException
from jwt import ExpiredSignatureError

from app.utils.config import TokenConfig

token_config = TokenConfig()


def decode_jwt(
        encoded_jwt:str,
        public_key:str = token_config.public_key_link.read_text(),
        algorithm:str=token_config.algorithm
):
    try:
        return jwt.decode(encoded_jwt, public_key,algorithms=[algorithm])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code = 401,
            detail = "Unauthorized user",
        )


def encode_jwt(
        payload:dict,
        private_key:str = token_config.private_key_link.read_text(),
        algorithm:str=token_config.algorithm
):
    return jwt.encode(payload, private_key, algorithm=algorithm)


def hashed_password(password:str)->str:
    return bcrypt.hashpw(password=password.encode("utf-8"),salt=bcrypt.gensalt()).decode("utf-8")


def verify_password(password:str,hashed_password:str)->bool:
    check_password = bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=hashed_password.encode("utf-8"))
    return check_password
