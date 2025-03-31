from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    hashed_password: str = Field(min_length=8)
    email: str = Field(default_factory=str)
    steamid: str = Field(default_factory=str)
    steamname: str = Field(default_factory=str)

class TokenType(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "bearer"