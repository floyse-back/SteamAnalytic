import asyncio
from typing import Union, List, Optional

from bs4 import BeautifulSoup
from steam_web_api import Steam

from app.application.decorators.cache import cache_data
from app.application.exceptions.exception_handler import SteamExceptionBase
from app.domain.logger import ILogger
from app.infrastructure.exceptions.exception_handler import SteamGameNotFound, SteamUserNotFound, \
    SteamUserAchievementsNotFoundDetails, SteamNginxException
from app.infrastructure.redis.redis_repository import CacheRepository
from app.utils.config import STEAM_API_KEY
import re
from httpx import AsyncClient
import httpx

class SteamClient(Steam):
    def __init__(self, cache_repository:CacheRepository, logger:ILogger, steam_key = STEAM_API_KEY):
        super().__init__(key=steam_key)
        self.__steam_key = steam_key
        self.__steam_http = "https://api.steampowered.com/"
        self.cache_repository = cache_repository
        self.logger = logger


    @cache_data(expire=60*60*3)
    async def save_start_pool(self,func,func_name="",raise_error:bool=True,*args,**kwargs):
        try:
            data = func(*args,**kwargs)
            return data
        except Exception as e:
            if raise_error:
                raise SteamExceptionBase(exc=e)
            else:
                return None

    def __game_check_correct_data(self,response:Optional[dict],game_id:int)->Optional[dict]:
        if response is None:
            raise SteamGameNotFound("Steam game not found")
        data = response[f"{game_id}"]
        if not data["success"]:
            raise SteamGameNotFound("Steam game not found")
        else:
            return data["data"]

    @cache_data(expire=3600*3)
    async def get_global_achievements(self,game_id):
        filters = "achievements,basic,price_overview"
        response = self.apps.get_app_details(app_id=game_id,country="UA",filters=filters)

        return self.__game_check_correct_data(response,game_id)

    @cache_data(expire=3600)
    async def get_price_game_now(self,app_id:int):
        filters = "basic,price_overview"
        response = self.apps.get_app_details(app_id=app_id,filters=filters)

        return self.__game_check_correct_data(response,app_id)

    async def get_user_details(self,steam_ids:Union[int,str,List[int]])->dict:
        if type(steam_ids) == list:
            steam_ids = ",".join(map(str,steam_ids))

        async with AsyncClient(base_url=self.__steam_http,timeout=10.0) as client:
            response = await client.get(
                "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
                params={
                    "key":self.__steam_key,
                    "steamids":steam_ids,
                }
            )

        if response.status_code == 429:
            raise SteamNginxException()
        data = response.json()
        new_data= dict()
        if data.get("response") and data.get("response").get("players"):
            new_data["player"] = data["response"]["players"][0]
        else:
            raise SteamUserNotFound()

        return new_data

    @cache_data(expire=3600)
    async def get_user_info(self, user: str) -> tuple[dict, str]:
        steam_id = await self.get_vanity_user_url(user)

        await asyncio.sleep(0.05)
        user_data = await self.get_user_details(steam_id)
        if user_data is not None and user_data.get('player') is not None:
            return user_data, steam_id

        user_data = self.users.search_user(user)

        if user_data is None or isinstance(user_data,str) or user_data.get('player') is None:
            raise SteamUserNotFound(f"User {user} not found")

        steam_id = user_data["player"]["steamid"]
        return user_data, steam_id

    @cache_data(expire=60*60*5)
    async def get_vanity_user_url(self,vanity_url):
        """
        Vanity URL format: This ID from img_url
        """
        if re.fullmatch(r"7656119\d{10}", vanity_url):
            return vanity_url

        async with AsyncClient() as client:
            response = await client.get(
                f"{self.__steam_http}/ISteamUser/ResolveVanityURL/v0001/",
                params = {
                    "key": self.__steam_key,
                    "vanityurl":vanity_url
                }
            )
            data = response.json()["response"]
            if response.status_code == 200 and data["success"] == 1:
                return data["steamid"]
            raise SteamUserNotFound(f"User {vanity_url} not found")

    @cache_data(expire=60*60*2)
    async def users_get_owned_games(self,users):
        try:
            result = self.users.get_owned_games(f"{users}")
            return result
        except Exception:
            raise SteamGameNotFound(f"User {users} not found")

    @cache_data(expire=3600)
    async def users_get_achievements(self,user_id,app_id):
        try:
            data = self.apps.get_user_achievements(user_id,app_id)
            return data
        except Exception:
            raise SteamUserAchievementsNotFoundDetails("User or app not found")

    def get_game_stats(self,appid,filters,cc):
        response = httpx.get(
            "https://store.steampowered.com/api/appdetails",
            params={
                "appids":appid,
                "filters":filters,
                "cc":cc,
                "l":"ukrainian"
            }
        )
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_popular_tags(appid: int) -> list[str]:
        url = f"https://store.steampowered.com/app/{appid}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        tags = []
        tag_container = soup.find_all("a", class_="app_tag")
        for tag in tag_container:
            tag_text = tag.text.strip()
            if tag_text:
                tags.append(tag_text.lower())
        return tags[0:11]