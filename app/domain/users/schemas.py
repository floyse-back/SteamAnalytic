from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    username: str
    hashed_password: str
    email: str
    steamid: str

@dataclass(frozen=True)
class TokenType:
    access_token: str
    refresh_token: str
    type:str

@dataclass(frozen=True)
class PublicUser:
    username:str
    steamname:str

@dataclass(frozen=True)
class UserMe:
    username: str
    email: str
    steamid: str

@dataclass(frozen=True)
class UserPublic:
    username: str
    steamid: str

@dataclass(frozen=True)
class UserModel:
    id: int
    username: str
    steamid: str
    email: str
    steam_name:str
    hashed_password: str

@dataclass(frozen=True)
class RefreshToken:
    pass

@dataclass(frozen=True)
class EmailConfirmation:
    token: str
    email: str
    expire_at: datetime