from pydantic import BaseModel, constr, Field


class User(BaseModel):
    username: str
    hashed_password: str = constr(min_length=8)
    email: str = Field(default_factory=str)
    steamid: str = Field(default_factory=str)


class TokenType(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "bearer"


class PublicUser(BaseModel):
    username: str
    steamname: str


class UserMe(BaseModel):
    username: str
    email: str = Field(default_factory=str)
    steamid: str = Field(default_factory=str)


class UserPublic(BaseModel):
    username: str
    steamid: str = Field(default_factory=str)
