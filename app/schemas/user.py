from pydantic import BaseModel, Field,constr

class User(BaseModel):
    username: str
    hashed_password: str = constr(min_length=8)
    email: str = Field(default_factory=str)
    steamid: str = Field(default_factory=str)
    steamname: str = Field(default_factory=str)

class TokenType(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "bearer"