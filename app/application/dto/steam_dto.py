from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Union, Dict
from datetime import date, datetime

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
    img_url:Optional[str] = None

    game_ganre:List[GanresOut]

    class Config:
        from_attributes = True

class GameListModel(BaseModel):
    name:str
    steam_appid:Optional[int] = None
    final_formatted_price:Optional[str]
    discount:Union[int] = None

    class Config:
        from_attributes = True

class SteamAppid(BaseModel):
    steam_appid: int

class GamesForYouModel(BaseModel):
    steam_appid:Optional[int]
    name:Optional[str]
    img_url:Optional[str]
    final_formatted_price:Optional[str]
    total:Optional[int]
    discount:Union[int]
    short_description:Optional[str]
    recomendations:Optional[int]
    metacritic:Optional[str]

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

class SteamBadgeModel(BaseModel):
    badgeid:int
    level:int
    completion_time:int
    xp:int
    scarcity:int

    class Config:
        from_attributes = True

class SteamBadgesListModel(BaseModel):
    badges:List[SteamBadgeModel]
    player_xp: int
    player_level: int
    player_xp_needed_to_level_up: int
    player_xp_needed_current_level:int

    class Config:
        from_attributes = True

class PlayersLists(BaseModel):
    player:PlayerModel

    class Config:
        from_attributes = True

class PlayerModel(BaseModel):
    steamid:int
    personaname:Optional[str]
    avatarfull:Optional[str]
    personastate:Optional[int]
    communityvisibilitystate:Optional[int]
    profilestate:Optional[int]
    lastlogoff:Optional[int] = None
    #PrivateData
    realname:Optional[str] = None
    primaryclanid:Optional[int] = None
    timecreated:Optional[int] = None
    timelive:Union[int,float] = None
    gameid:Optional[int] = None
    gameextrainfo:Optional[str] = None
    loccountrycode:Optional[str] = None

    @model_validator(mode="after")
    def change_time_live(self):
        if self.timecreated:
            self.timelive = datetime.now().timestamp() - self.timecreated
        return self

    class Config:
        from_attributes = True

class FriendsListModel(BaseModel):
    friends_count:Optional[int] = None
    first_friend:Optional[FriendsShortModel] = None
    last_friend:Optional[FriendsShortModel] = None
    friends:List[FriendsShortModel]

    @model_validator(mode="after")
    def create_global_params(self):
        if isinstance(self.friends, list):
            self.friends_count = len(self.friends)
            if len(self.friends) == 0:
                return self
            min_value = self.friends[0]
            max_value = self.friends[0]
            for i in self.friends:
                if i.friend_since < min_value.friend_since:
                    min_value = i
                if i.friend_since > max_value.friend_since:
                    max_value = i
            self.first_friend = min_value
            self.last_friend = max_value

            return self

    class Config:
        from_attributes = True

class FriendsShortModel(BaseModel):
    steamid:str
    relationship:str
    friend_since:int

    class Config:
        from_attributes = True

class SteamUser(BaseModel):
    user_data: Optional[PlayersLists] = None
    user_friends_list: Optional[FriendsListModel] = None
    user_badges: Optional[SteamBadgesListModel] = None
    user_games: Optional[GamesList] = None

    class Config:
        from_attributes = True

class SteamOwnedGame(BaseModel):
    appid:Optional[int]
    name:Optional[str]
    playtime_forever:Optional[int]
    playtime_2weeks:Optional[int] = None
    rtime_last_played:Optional[int] = None

    class Config:
        from_attributes = True

class GamesList(BaseModel):
    game_count:int
    games:List[SteamOwnedGame]

    class Config:
        from_attributes = True

class SteamRatingModel(BaseModel):
    steam_appid:Optional[int]
    user_rating:int = 0
    personaname:Optional[str]
    player_level:Optional[int]
    player_xp:Optional[int]
    player_xp_needed_to_level_up:Optional[int]
    timecreated:Optional[int]
    timelive:Optional[Union[int,float]] = None
    friends_count:Optional[int]
    badges_count:Optional[int]
    lastlogoff:Optional[int]
    playtime:Optional[int]

    allow_games:bool = True
    allow_friends:bool = True
    allow_badges:bool = True

    class Config:
        from_attributes = True

    @field_validator("user_rating",mode="before")
    def user_rating_validate(cls,v):
        if isinstance(v,int):
            if v > 10000:
                return 9999
            elif v < 0:
                return 0
            return v

    @model_validator(mode="after")
    def change_time_live(self):
        if self.timecreated:
            self.timelive =datetime.now().timestamp() - self.timecreated
        return self

class ComparisonModel(BaseModel):
    user_1:Optional[Union[int,float,str]]
    user_2:Optional[Union[int,float,str]]
    difference:Optional[Union[int,float,str]]
    winner : Optional[str]

class UserComparison(BaseModel):
    user_1:str
    user_2:str
    player_level: Optional[ComparisonModel] = None
    player_xp: Optional[ComparisonModel] = None
    badge_count: Optional[ComparisonModel] = None
    total_badges_xp: Optional[ComparisonModel] = None
    game_count: Optional[ComparisonModel] = None
    total_playtime: Optional[ComparisonModel] = None
    total_rating: Optional[ComparisonModel] = None

def transform_to_dto(model:BaseModel,orm,dumping:bool = True):
    if dumping:
        return model.model_validate(orm).model_dump()
    return model.model_validate(orm)