from datetime import datetime
from math import log
from typing import Union, Optional

from app.application.dto.steam_dto import SteamUser, SteamRatingModel
from app.domain.logger import ILogger


class GetUserRatingUseCase:
    def __init__(self,logger:ILogger):
        self.logger = logger

    async def execute(self,data:SteamUser,enriched:bool=False) -> Union[SteamRatingModel,int]:
        self.logger.info("GetUserRatingUseCase: called %s",data)
        allow_games,allow_friends,allow_badges = True,True,True
        if data.get('user_games') is None:
            allow_games = False
            data["user_games"] = {
                "game_count": 0,
                "games": []
              }
        if data.get('user_friends_list') is None:
            allow_friends = False
            data['user_friends'] ={
                "friends_count": 0,
                "first_friend": None,
                "last_friend": None,
                "friends": []
            },
        if data.get('user_badges') is None:
            allow_badges = False
            data['user_badges'] = {
                "badges": [],
                "player_xp": -1,
                "player_level": -1,
                "player_xp_needed_to_level_up": -1,
                "player_xp_needed_current_level": -1
              }
        self.logger.debug("GetUserRatingUseCase: Steam User Rating first data %s",data)
        year_create_user_score = await self.__check_user_years(data["user_data"]["player"].get("timecreated",None)) * 10
        count_user_friends_score = len(data["user_friends_list"]["friends"]) * 2
        lastlogoff = await self.__count_score_last_logoff(self.__last_logoff(data["user_data"]["player"].get("lastlogoff")).days) if data["user_data"]["player"].get("lastlogoff") else 0
        profile_visible = await self.__profile_visible(data["user_data"]["player"]["personastate"]) if data["user_data"]["player"].get("personastate") else 0
        count_game_score = data["user_games"].get("game_count") * 2  if data["user_games"].get("game_count") else 0
        steam_state = data["user_data"]["player"]["communityvisibilitystate"] * 3
        user_level_score = data["user_badges"]["player_level"] * 5 if data['user_badges']['player_level'] !=-1 else 5
        badge_level_score = await self.__badges_correct(data["user_badges"]["badges"]) if data["user_badges"].get("badges") else 0
        open_user_elements = await self.__user_opening_for_steam(data["user_data"]["player"])
        count_game = await self.__game_check_result(games=data["user_games"]["games"]) if data["user_games"].get("games") else (0,0)
        count_game_time = count_game[0]
        play_time_forever = count_game[1]

        result = self.__formula_user(
            [year_create_user_score,count_user_friends_score,lastlogoff,profile_visible,count_game_score,steam_state,user_level_score,badge_level_score,open_user_elements,count_game_time]
        )*2

        if result >10000:
            result = 9999

        #Серіалізація
        if enriched:
            serialize_data = SteamRatingModel(
                steam_appid=data["user_data"]["player"]['steamid'],
                personaname=data["user_data"]["player"].get("personaname") if data["user_data"].get("player") else None,
                player_level=data["user_badges"].get("player_level",0),
                player_xp = data["user_badges"].get("player_xp",0),
                player_xp_needed_to_level_up=data["user_badges"].get("player_xp_needed_to_level_up",0),
                timecreated=data["user_data"]["player"].get("timecreated",None),
                friends_count=len(data["user_friends_list"].get("friends",[])),
                badges_count=len(data["user_badges"].get("badges",[])),
                lastlogoff=data["user_data"]["player"].get("lastlogoff",None),
                playtime=play_time_forever,
                user_rating=result,

                allow_games = allow_games,
                allow_friends = allow_friends,
                allow_badges = allow_badges,
            )
        else:
            serialize_data = result
        self.logger.info("Successfully fetched user rating: %s",serialize_data)
        return serialize_data

    def __formula_user(self,data:list)->int:
        self.logger.debug("GetUserRatingUseCase: Data: %s",data)
        return round(sum(data))

    @staticmethod
    async def __check_user_years(seconds:Optional[int]):
        if seconds is None:
            return 0.25
        dt = datetime.fromtimestamp(seconds).year
        return datetime.now().year - dt

    @staticmethod
    def __last_logoff(seconds):
        dt = datetime.fromtimestamp(seconds)
        return datetime.now() - dt

    @staticmethod
    async def __count_score_last_logoff(days)->int:
        if days == 0:
            return 30
        elif days == 1:
            return 20
        elif days < 7:
            return 10
        elif days < 14:
            return 5
        elif days < 30 :
            return 1
        return 0

    @staticmethod
    async def __profile_visible(person_state):
        if person_state !=0:
            return 5
        return 0

    @staticmethod
    async def __badges_correct(badges:list) -> int:
        rating = 0
        for badge in badges:
            rating += max(0,50 - log(badge["scarcity"],10))
        return rating

    @staticmethod
    async def __user_opening_for_steam(data:dict)->int:
        rating = 0
        open_elements = {
            "realname":30,
            "primaryclanid":25,
            "cityid":40,
            "loccountrycode":25,
            "locstatecode":20,
            "loccityid":24
        }

        for key,value in open_elements.items():
            if data.get(key):
                rating += value

        return rating

    @staticmethod
    async def __game_check_result(games:list)->tuple[int,int]:
        result = 0
        game_time_forever=0
        game_time_2weeks = 0
        for game in games:
            game_time_forever += game.get("playtime_forever") if game.get("playtime_forever") else 0
            game_time_2weeks += game.get("playtime_2weeks") if game.get("playtime_2weeks") else 0

        result += ((game_time_forever-game_time_2weeks)//60)*0.25
        result += game_time_2weeks//60 * 0.5
        return int(result),game_time_forever