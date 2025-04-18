from datetime import datetime
from math import log

from app.application.dto.steam_dto import SteamUser

class UserRating:
    async def create_user_rating(self,data:SteamUser) -> int:
        year_create_user_score = await self.check_user_years(data["user_data"]["player"]["timecreated"]) * 10
        count_user_friends_score = len(data["user_friends_list"]["friends"]) * 2
        lastlogoff = await self.count_score_last_logoff(self.last_logoff(data["user_data"]["player"].get("lastlogoff")).days) if data["user_data"]["player"].get("lastlogoff") else 0
        profile_visible = await self.profile_visible(data["user_data"]["player"]["personastate"]) if data["user_data"]["player"].get("personastate") else 0
        count_game_score = data["user_games"].get("game_count") * 2  if data["user_games"].get("game_count") else 0
        steam_state = data["user_data"]["player"]["communityvisibilitystate"] * 3
        user_level_score = data["user_badges"]["player_level"] * 5
        badge_level_score = await self.badges_correct(data["user_badges"]["badges"]) if data["user_badges"].get("badges") else 0
        open_user_elements = await self.user_opening_for_steam(data["user_data"]["player"])
        count_game_time = await self.game_check_result(games=data["user_games"]["games"]) if data["user_games"].get("games") else 0

        result = self.formula_user(
            [year_create_user_score,count_user_friends_score,lastlogoff,profile_visible,count_game_score,steam_state,user_level_score,badge_level_score,open_user_elements,count_game_time],
        )*2

        if result >10000:
            return 9999

        return result

    def formula_user(self,data:list)->int:
        return round(sum(data))

    @staticmethod
    async def check_user_years(seconds):
        dt = datetime.fromtimestamp(seconds).year
        return datetime.now().year - dt

    @staticmethod
    def last_logoff(seconds):
        dt = datetime.fromtimestamp(seconds)
        return datetime.now() - dt

    @staticmethod
    async def count_score_last_logoff(days)->int:
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
    async def profile_visible(person_state):
        if person_state !=0:
            return 5
        return 0

    @staticmethod
    async def badges_correct(badges:list) -> int:
        rating = 0
        for badge in badges:
            rating += max(0,50 - log(badge["scarcity"],10))
        return rating

    @staticmethod
    async def user_opening_for_steam(data:dict)->int:
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
    async def game_check_result(games:list)->int:
        result = 0
        game_time_forever=0
        game_time_2weeks = 0
        for game in games:
            game_time_forever += game.get("playtime_forever") if game.get("playtime_forever") else 0
            game_time_2weeks += game.get("playtime_2weeks") if game.get("playtime_2weeks") else 0

        result += ((game_time_forever-game_time_2weeks)//60)*0.25
        result += game_time_2weeks//60 * 0.5
        return int(result)