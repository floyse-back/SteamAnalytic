import datetime
import random
import time
from typing import Union

from sqlalchemy.orm import Session
from steam_web_api import Steam

from app.infrastructure.celery_app.celery_app import logger
from app.infrastructure.db.models.steam_models import Game, Category, Ganres, Publisher
from app.utils.config import STEAM_API_KEY

class SteamDetailsParser:
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
    def __init__(self, session:Session,session_commit:bool=True):
        self.steam = Steam(STEAM_API_KEY)
        self.filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements,release_date'
        self.session = session
        self.session_commit = session_commit

    @staticmethod
    def steam_id_unique(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return False
        else:
            return True

    def session_commit_func(self):
        if self.session_commit:
            self.session.commit()
        else:
            self.session.flush()

    @staticmethod
    def get_or_create(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            return instance

    def update_game_details(self, game, existing_game):
        """Функція для оновлення деталей гри."""
        existing_game.is_free = game.get("is_free")
        existing_game.name = game.get("name")
        existing_game.short_description = game.get("short_description")
        existing_game.requirements = game.get("steam_requirements")
        existing_game.initial_price = game.get("price_overview", {}).get("initial", 0)
        existing_game.final_price = game.get("price_overview", {}).get("final", 0)
        existing_game.final_formatted_price = game.get("price_overview", {}).get("final_formatted", "Free")
        existing_game.discount = game.get("price_overview", {}).get("discount_percent", 0)
        existing_game.metacritic = game.get("metacritic", {}).get("score", -1)
        existing_game.achievements = game.get("achievements", {}).get("highlighted", {})
        existing_game.recomendations = int(game.get("recommendations", {}).get("total", 0))
        existing_game.img_url = game.get("capsule_image")
        existing_game.last_updated = datetime.datetime.today().date()
        existing_game.release_data = self.__transform_date(game.get("release_data",{"date":datetime.date.today()}).get("date"))

        # Оновлення категорій, жанрів та видавців
        if game.get("categories"):
            for category in game.get("categories"):
                category_name = category.get("description")
                category_obj = self.get_or_create(self.session, Category, category_name=category_name)
                if category_obj not in existing_game.game_categories:
                    existing_game.game_categories.append(category_obj)

        if game.get("publishers"):
            for publisher in game.get("publishers"):
                publisher_name = publisher.get("name")
                publisher_obj = self.get_or_create(self.session, Publisher, publisher_name=publisher_name)
                if publisher_obj not in existing_game.game_publisher:
                    existing_game.game_publisher.append(publisher_obj)

        if game.get("genres"):
            for genre in game.get("genres"):
                ganres_name = genre.get("description")
                ganres_obj = self.get_or_create(self.session, Ganres, ganres_name=ganres_name)
                if ganres_obj not in existing_game.game_ganre:
                    existing_game.game_ganre.append(ganres_obj)

        self.session_commit_func()

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
        logger.debug(f"transform_date: %s",new_date)
        return new_date

    def add_new_game(self,game,steam_appid):
        new_game = Game(
            steam_appid=steam_appid,
            name=game.get("name"),
            is_free=game.get("is_free"),
            short_description=game.get("short_description"),
            requirements=game.get("steam_requirements"),
            initial_price=game.get("price_overview", {}).get("initial", 0),
            final_price=game.get("price_overview", {}).get("final", 0),
            final_formatted_price=game.get("price_overview", {}).get("final_formatted", "Free"),
            discount=game.get("price_overview", {}).get("discount_percent", 0),
            metacritic=game.get("metacritic", {}).get("score", -1),
            achievements=game.get("achievements", {}).get("highlighted", {}),
            recomendations=int(game.get("recommendations", {}).get("total", 0)),
            img_url=game.get("capsule_image"),
            release_data=self.__transform_date(game.get("release_date",{"date":datetime.date.today()}).get("date"))
        )

        # Додаємо категорії, жанри та видавців
        if game.get("categories"):
            for category in game.get("categories"):
                category_name = category.get("description")
                new_game.game_categories.append(
                    self.get_or_create(session=self.session, model=Category, category_name=category_name))

        if game.get("publishers"):
            for publisher in game.get("publishers"):
                publisher_name = publisher.get("name")
                new_game.game_publisher.append(
                    self.get_or_create(session=self.session, model=Publisher, publisher_name=publisher_name))

        if game.get("genres"):
            for genre in game.get("genres"):
                ganres_name = genre.get("description")
                new_game.game_ganre.append(
                    self.get_or_create(session=self.session, model=Ganres, ganres_name=ganres_name))

        self.session.add(new_game)
        self.session_commit_func()

    def create_gamesdetails_model(self, game_list):
        if not isinstance(game_list, list):
            raise ValueError("Game list must be a list")

        for game in game_list:
            steam_appid = game.get("steam_appid")
            existing_game = self.session.query(Game).filter_by(steam_appid=steam_appid).first()

            if existing_game:
                self.update_game_details(game, existing_game)
            else:
                self.add_new_game(game,steam_appid)

    @staticmethod
    def __safe_sleep(min_delay=0.8, max_delay=1.3):
        time.sleep(random.uniform(min_delay, max_delay))

    def parse(self,game_list_appid):
        new_list = []
        for i in game_list_appid:
            try:
                result = self.steam.apps.get_app_details(int(i), filters=self.filters)

                if result.get(f"{i}").get("success") == False:
                    continue

                new_list.append(result[f'{i}']['data'])
                self.__safe_sleep()
            except:
                logger.debug("Don`t parse game appid %s",i)
                time.sleep(5)


        self.create_gamesdetails_model(new_list)
