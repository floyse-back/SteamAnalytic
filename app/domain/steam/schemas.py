from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import date


@dataclass(frozen=True)
class SteamUser:
    user_data: dict
    user_friends: dict
    user_badges: dict
    user_games: dict

@dataclass(frozen=True)
class Ganres:
    id: int
    ganre_name: str

@dataclass(frozen=True)
class Publishers:
    id: int
    publisher_name: str

@dataclass(frozen=True)
class Categories:
    id: int
    category_name: str



@dataclass(frozen=True)
class Game:
    steam_appid: int
    name: str
    is_free: bool
    short_description: str
    requirements: Dict[str, Any]
    initial_price: int
    final_price: int
    final_formatted_price: str
    metacritic: str
    discount: int
    achievements: Dict[str, Any]
    recomendations: int
    img_url: str
    last_updated: Optional[date]

    game_ganre:List[Ganres]
    game_publisher: List[Publishers]
    game_categories: List[Categories]



@dataclass(frozen=True)
class SteamBase:
    id: int
    name: str
    appid: str
    developer: str
    publisher: str
    positive: int
    negative: int
    average_forever: int
    average_2weeks: int
    median_forever: int
    median_2weeks: int
    price: int
    discount: int
    img_url: Optional[str] = None

@dataclass(frozen=True)
class BlockedGames:
    appid:int