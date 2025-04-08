from dataclasses import dataclass


@dataclass(frozen=True)
class SteamUser:
    user_data: dict
    user_friends: dict
    user_badges: dict
    user_games: dict