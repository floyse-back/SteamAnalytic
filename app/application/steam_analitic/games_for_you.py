from app.application.exceptions.exception_handler import GamesNotFound
from app.application.steam_analitic.game_you_interface import IGameForYou

class GamesForYou(IGameForYou):
    """Знаходження ігор які сподобаються користувачеві"""
    async def game_data_create(self,session,count_dict,appid_list):

        if count_dict.get("ganres_dict") == [] and count_dict.get("publishers_dict") == [] and count_dict.get("categories_dict") == []:
            raise GamesNotFound()

        data = await self.repository.games_for_you(session=session, ganres_data=count_dict.get("ganres_dict"),
                                                   category_data=count_dict.get("categories_dict"),
                                                   steam_appids=appid_list)
        return data

class SallingForYou(IGameForYou):
    """Знаходження знижок які сподобаються користувачеві"""
    async def game_data_create(self,session,count_dict,appid_list):

        if count_dict.get("ganres_dict") == [] and count_dict.get("publishers_dict") == [] and count_dict.get("categories_dict") == []:
            raise GamesNotFound()

        data = await self.repository.salling_for_you(session=session, ganres_data=count_dict.get("ganres_dict"),
                                                   category_data=count_dict.get("categories_dict"),
                                       steam_appids=appid_list)
        return data


