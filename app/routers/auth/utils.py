import jwt
import bcrypt

def decode_jwt(
        encoded_jwt:str,
        public_key:str,
        algorithm:str="RS256"
):
    return jwt.decode(encoded_jwt, public_key,algorithms=[algorithm])

def encode_jwt(
        payload:dict,
        private_key:str,
        algorithm:str="RS256"
):
    return jwt.encode(payload, private_key, algorithm=algorithm)

def hashed_password(password:str)->bytes:
    return bcrypt.hashpw(password=password.encode("utf-8"),salt=bcrypt.gensalt())

def verify_password(password:str,hashed_password:bytes):
    check_password = bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=hashed_password)
    return check_password