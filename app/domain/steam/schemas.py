from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import date

@dataclass(frozen=True)
class SteamUser:
    user_data: dict
    user_friends: dict
    user_badges: dict
    user_games: dict

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