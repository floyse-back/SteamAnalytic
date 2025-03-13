from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    hashed_password: str = Field(min_length=8)
    email: str = ""
    steamid: str = ""
    steamname: str = ""

class TokenType(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "bearer"