from pydantic import BaseModel, Field
from typing import Optional, List, Union, Dict
from datetime import date



class SteamUser(BaseModel):
    user_data: Optional[dict] = None
    user_friends_list: Optional[dict] = None
    user_badges: Optional[dict] = None
    user_games: Optional[dict] = None

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
        from_attributes = True

class CategoryOut(BaseModel):
    category_id: int
    category_name: str

    class Config:
        from_attributes = True

class GanresOut(BaseModel):
    ganres_id: int
    ganres_name: str

    class Config:
        from_attributes = True

class PublisherOut(BaseModel):
    publisher_id: int
    publisher_name: str

    class Config:
        from_attributes = True

class GameShortModel(BaseModel):
    name:str
    steam_appid:Optional[int] = None
    final_formatted_price:Optional[str]
    discount:Union[int,str]
    short_description:Optional[str]
    url:Optional[str] = None

    game_ganre:List[GanresOut]

    class Config:
        from_attributes = True

class AchivementModel(BaseModel):
    name:str

    class Config:
        from_attributes = True

class AchievementsModel(BaseModel):
    total:Optional[int] = None
    highlighted:List[AchivementModel]

    class Config:
        from_attributes = True

class PriceOverviewModel(BaseModel):
    initial:Optional[int] = None
    final:Optional[int] = None
    discount_percent:Optional[int] = None
    initial_formatted:Optional[str] = None
    final_formatted:Optional[str] = None

class GameAchievementsModel(BaseModel):
    name:str
    steam_appid:Optional[int]
    achievements:AchievementsModel = AchievementsModel(
        total=0,
        highlighted=[]
    )
    price_overview:Optional[PriceOverviewModel] = None
    short_description:Optional[str]

    class Config:
        from_attributes = True

class GamePriceModel(BaseModel):
    name:str
    steam_appid:Optional[int]
    short_description:Optional[str]
    price_overview:Optional[PriceOverviewModel] = None

    class Config:
        from_attributes = True

class Game(BaseModel):
    steam_appid: Optional[int]
    name: Optional[str]
    is_free: Optional[bool] = None
    short_description: Optional[str] = None
    requirements: Optional[dict] = None
    initial_price: Optional[int] = None
    final_price: Optional[int] = None
    final_formatted_price: Optional[str] = None
    metacritic: Optional[str] = None
    discount: Optional[int] = None
    achievements: Optional[Union[List,Dict]] = None
    recomendations: Optional[int] = None
    img_url: Optional[str] = None
    last_update: Optional[date] = None

    game_ganre: List[GanresOut]
    game_publisher: List[PublisherOut]
    game_categories: List[CategoryOut]

    class Config:
        from_attributes = True

def transform_to_dto(model:BaseModel,orm):
    return model.model_validate(orm).model_dump()