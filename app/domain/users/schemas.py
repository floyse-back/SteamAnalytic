from dataclasses import dataclass


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

