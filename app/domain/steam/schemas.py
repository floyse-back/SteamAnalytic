from pydantic import BaseModel,Field


class SteamUser(BaseModel):
    user_data: dict = Field(default=dict())
    user_friends: dict = Field(default=dict())
    user_badges: dict = Field(default=dict())
    user_games: dict = Field(default=dict())
