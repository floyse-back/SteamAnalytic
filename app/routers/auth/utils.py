import jwt
import bcrypt
from ...config import TokenConfig

token_config = TokenConfig()

def decode_jwt(
        encoded_jwt:str,
        public_key:str = token_config.public_key_link.read_text(),
        algorithm:str=token_config.algorithm
):
    return jwt.decode(encoded_jwt, public_key,algorithms=[algorithm])

def encode_jwt(
        payload:dict,
        private_key:str = token_config.private_key_link.read_text(),
        algorithm:str=token_config.algorithm
):
    return jwt.encode(payload, private_key, algorithm=algorithm)

def hashed_password(password:str)->bytes:
    return bcrypt.hashpw(password=password.encode("utf-8"),salt=bcrypt.gensalt())

def verify_password(password:str,hashed_password:bytes):
    check_password = bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=hashed_password)
    return check_password