from datetime import datetime

from pydantic import BaseModel, constr, Field
from typing import List, Optional


class RefreshTokenDTO(BaseModel):
    id: int
    refresh_token: str
    delete_time: datetime

    class Config:
        from_attributes = True

class BlackListDTO(BaseModel):
    id: int
    token: str
    expires_at: datetime
    reason: Optional[str]

    class Config:
        from_attributes = True


class EmailConfirmedDTO(BaseModel):
    id: int
    type: str
    token: str
    expires_at: datetime

    class Config:
        from_attributes = True


class UserModelDTO(BaseModel):
    id: Optional[int]
    username: Optional[str]
    hashed_password: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
    role: Optional[str]
    steamid: Optional[str]
    steamname: Optional[str]

    blacklist_token: Optional[List[BlackListDTO]]
    refresh_tokens: Optional[List[RefreshTokenDTO]]
    email_confirmed: Optional[List[EmailConfirmedDTO]]

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

class UserShortDTO(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_attributes = True

def transform_to_dto(model:BaseModel,orm):
    return model.model_validate(orm).model_dump()