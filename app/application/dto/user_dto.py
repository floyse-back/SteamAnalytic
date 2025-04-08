from pydantic import BaseModel, constr, Field


class User(BaseModel):
    username: str
    hashed_password: str = constr(min_length=8)
    email: str = Field(default_factory=str)
    steamid: str = Field(default_factory=str)


class TokenType(BaseModel):
    access_token: str = Field(default_factory=str)
    refresh_token: str = Field(default_factory=str)
    type: str = Field(default="bearer")


class PublicUser(BaseModel):
    username: str = Field(default_factory=str)
    steamname: str = Field(default_factory=str)


class UserMe(BaseModel):
    username: str = Field(default_factory=str)
    email: str = Field(default_factory=str)
    steamid: str = Field(default_factory=str)


class UserPublic(BaseModel):
    username: str = Field(default_factory=str)
    steamid: str = Field(default_factory=str)
