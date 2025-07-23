import datetime
from typing import Optional, Union, List

from app.application.dto.steam_dto import transform_to_dto, Game, GameShortModel, GanresOut, GameFullModel, CategoryOut, \
    PublisherOut
from app.domain.logger import ILogger
from app.infrastructure.db.models.steam_models import Category


class GetFreeTransformUseCase:
    MONTHS_CODE = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    """
    Трансформує дані типу GetGameStatsUseCase
    """
    def __init__(self,logger:ILogger):
        self.logger = logger

    def execute(self,data:Optional[Union[List,dict]]=None,game_id:int=None,full:bool=False):
        if data is None or len(data) == 0:
            return None
        else:
            if data[f"{game_id}"]["success"] == True:
                if full is False:
                    game_model = self.__corected_game_short_model(data[f"{game_id}"]["data"])
                else:
                    game_model = self.__correct_game_full_model(data[f"{game_id}"]["data"],steam_appid=game_id)
            else:
                return None
            return game_model

    def __corected_game_short_model(self,data:Optional[dict])->GameShortModel:
        if data is None:
            return False

        game_short_model = GameShortModel(
            name=data.get("name","Steam Game"),
            steam_appid = int(data.get("steam_appid")),
            final_formatted_price = data.get("price_overview",{"final_formatted":"Free"}).get("final_formatted","0"),
            discount = int(data.get("price_overview",{"discount_percent":0}).get("discount_percent",0)),
            short_description=data.get("short_description","text"),
            img_url= data.get(f"capsule_image"),

            game_ganre=[GanresOut(ganres_id=int(i.get('id')),ganres_name=i.get("description")) for i in data.get("genres",[])],
        )

        return game_short_model

    @classmethod
    def __transform_date(cls,my_date:Union[datetime.date,str]):
        if isinstance(my_date, datetime.date):
            return my_date
        date_split = my_date.split(" ")
        if len(date_split) < 3:
            return None
        month_number = cls.MONTHS_CODE[date_split[0]]
        day = int(date_split[1].replace(",",""))
        year = int(date_split[2])
        new_date = datetime.date(year=year,month=month_number,day=day)
        return new_date

    def __correct_game_full_model(self,data:Optional[dict],steam_appid:int)->GameFullModel:
        if data is None:
            return False
        if not data.get("price_overview"):
            data['price_overview'] = {
                "final_formatted":"Free",
            }
        game=data
        game_ganre = []
        game_categories = []
        game_publisher = []
        for ganre in game.get("genres",[]):
            game_ganre.append(
                GanresOut(
                    ganres_id=int(ganre.get('id')),
                    ganres_name = ganre.get("description")
                )
            )

        for category in game.get("categories",[]):
            game_categories.append(
                CategoryOut(
                    category_id=int(category.get("id")),
                    category_name = category.get("description")
                )
            )
        for publisher in game.get("developers",[]):
            game_publisher.append(
                PublisherOut(
                    publisher_name = str(publisher)
                )
            )

        game_full_model = GameFullModel(
            steam_appid=steam_appid,
            name=game.get("name"),
            is_free=game.get("is_free"),
            short_description=game.get("short_description"),
            final_price=game.get("price_overview", {}).get("final", 0),
            final_formatted_price=game.get("price_overview", {}).get("final_formatted", "Free"),
            discount=game.get("price_overview", {}).get("discount_percent", 0),
            metacritic=str(game.get("metacritic", {}).get("score", "-1")),
            recomendations=int(game.get("recommendations", {}).get("total", 0)),
            release_data=self.__transform_date(game.get("release_date",{"date":datetime.date.today()}).get("date")),
            img_url=game.get("header_image"),
            game_ganre = game_ganre,
            game_categories = game_categories,
            game_publisher = game_publisher
        ).model_dump()
        self.logger.info("GetFreeTransformUseCase: Data Full Games %s",data)
        return game_full_model