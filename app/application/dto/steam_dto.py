from pydantic import BaseModel, Field
from typing import Optional,List
from datetime import date


class SteamUser(BaseModel):
    user_data: dict = Field(default=dict())
    user_friends_list: dict = Field(default=dict())
    user_badges: dict = Field(default=dict())
    user_games: dict = Field(default=dict())

class SteamBase(BaseModel):
    id: int
    name: str
    appid: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    positive: Optional[int] = None
    negative: Optional[int] = None
    average_forever: Optional[int] = None
    average_2weeks: Optional[int] = None
    median_forever: Optional[int] = None
    median_2weeks: Optional[int] = None
    price : Optional[int] = None
    discount : Optional[int] = None
    img_url: Optional[str] = None

    class Config:
        orm_mode = True

class CategoryOut(BaseModel):
    category_id: int
    category_name: str

    class Config:
        orm_mode = True

class GanresOut(BaseModel):
    ganres_id: int
    ganres_name: str

    class Config:
        orm_mode = True

class PublisherOut(BaseModel):
    publisher_id: int
    publisher_name: str

    class Config:
        orm_mode = True

class Game(BaseModel):
    steam_appid: int
    name: str
    is_free: Optional[bool] = None
    short_description: Optional[str] = None
    requirements: dict
    initial_price: Optional[int] = None
    final_price: Optional[int] = None
    final_formatted_price: Optional[str] = None
    metacritic: Optional[str] = None
    discount: Optional[int] = None
    achievements: Optional[dict] = None
    recomendations: Optional[int] = None
    img_url: Optional[str] = None
    last_update: Optional[date] = None

    game_ganre: List[GanresOut]
    game_publisher: List[PublisherOut]
    game_categories: List[CategoryOut]

    class Config:
        orm_mode = True
