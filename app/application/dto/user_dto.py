from datetime import datetime

from pydantic import BaseModel, constr, Field
from typing import List, Optional


class RefreshToken(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    refresh_token: Optional[str]
    delete_time: Optional[datetime]

    class Config:
        from_attributes = True

class BlacklistToken(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    token: Optional[str]
    expires_at: Optional[datetime]
    reason: Optional[str]

    class Config:
        from_attributes = True

class UserModel(BaseModel):
    id: Optional[int]
    username: Optional[str]
    hashed_password: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
    role: Optional[str]
    steamid: Optional[str]
    steamname: Optional[str]

    blacklist_token: Optional[List[BlacklistToken]]
    refresh_tokens: Optional[List[RefreshToken]]

    class Config:
        from_attributes = True

class UserElementToken(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]

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

def transform_to_dto(model:BaseModel,orm):
    return model.model_validate(orm).model_dump()