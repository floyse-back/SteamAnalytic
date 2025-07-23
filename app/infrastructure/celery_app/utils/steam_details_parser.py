import datetime
import random
import time
from typing import Union, Optional, List

from sqlalchemy.orm import Session

from app.application.usecases.add_blocked_games_use_case import AddBlockedGamesUseCase
from app.application.usecases.add_safe_games_use_case import AddSafeGamesUseCase
from app.application.usecases.check_game_base_use_case import CheckGameBaseUseCase
from app.infrastructure.celery_app.celery_app import logger
from app.infrastructure.db.models.steam_models import Game, Category, Ganres, Publisher
from app.infrastructure.db.sync_repository.BlockedGamesRepository import BlockedGamesRepository
from app.infrastructure.db.sync_repository.safe_game_repository import SafeGameRepository
from app.utils.dependencies import get_steam_client
from app.utils.filter_nfsm_content import filter_nfsm_content


class SteamDetailsParser:
    MONTHS_CODE = {
        "січ.": 1,
        "лют.": 2,
        "берез.": 3,
        "квіт.": 4,
        "трав.": 5,
        "черв.": 6,
        "лип.": 7,
        "серп.": 8,
        "верес.": 9,
        "жовт.": 10,
        "листоп.": 11,
        "груд.": 12,
    }
    def __init__(self, session:Session,session_commit:bool=True):
        self.steam = get_steam_client()
        self.filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements,release_date,movies,content_descriptors'
        self.session = session
        self.session_commit = session_commit
        self.add_blocked_game_use_case = AddBlockedGamesUseCase(
            blocked_repository=BlockedGamesRepository(),
        )
        self.add_safegame_use_case = AddSafeGamesUseCase(
            safe_game_repository=SafeGameRepository(),
        )
        self.check_game_use_case = CheckGameBaseUseCase(
            safe_games_repository=SafeGameRepository(),
            blocked_repository=BlockedGamesRepository(),
        )

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

    @staticmethod
    def get_trailer_url(data:Optional[List])->str:
        logger.debug("Get Trailer URL")
        if data is None:
            logger.debug("Get Trailer URL None")
            return ""
        for movie in data:
            if movie.get("name",{"name":None}) and movie['name'].lower().find("trailer")!=-1:
                logger.debug(f"Get Trailer URL Movie Trailer {movie.get("mp4",{"mp4":{"max":""}})['max']}")
                return movie.get("mp4",{"mp4":{"max":""}})['max']

    def update_game_details(self, game, existing_game):
        logger.debug(f"Game {game}")
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
        existing_game.release_data = self.__transform_date(my_date=game.get("release_date",{"date":datetime.date.today()}).get("date"))
        existing_game.trailer_url = self.get_trailer_url(game.get("movies"))

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
        try:
            logger.info(f"{my_date}")
            month_number = cls.MONTHS_CODE[date_split[1]]
        except KeyError:
            return None
        day = int(date_split[0].replace(",",""))
        year = int(date_split[2])
        new_date = datetime.date(year=year,month=month_number,day=day)
        logger.info(f"transform_date: %s",new_date)
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
            trailer_url=self.get_trailer_url(data=game.get("movies")),
            release_data=self.__transform_date(game.get("release_date",{"date":datetime.date.today()}).get("date")),
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
    def __safe_sleep(min_delay=0.25, max_delay=0.5):
        time.sleep(random.uniform(min_delay, max_delay))

    def parse(self,game_list_appid):
        new_list = []
        filter_list_appid = self.check_game_use_case.execute(appids=game_list_appid,session=self.session)
        logger.info(f"{filter_list_appid}")
        for i in filter_list_appid:
            try:
                appid = i.get("appid")
                result = self.steam.get_game_stats(appid=appid, filters=self.filters,cc="UA")
                self.__safe_sleep()

                if result.get(f"{appid}").get("success") == False or i.get("success") == True:
                    continue

                check = filter_nfsm_content(result[f'{appid}']['data'])
                if check:
                    new_list.append(result[f'{appid}']['data'])
                    self.add_safegame_use_case.execute(
                        session=self.session,
                        appid=appid
                    )
                else:
                    logger.debug(f"Blocked game {result[f'{appid}']['data']['steam_appid']}")
                    self.add_blocked_game_use_case.execute(appid,session=self.session)
            except Exception as e:
                logger.info("Don`t parse game %s",i)
                logger.warning("SteamDetailsParser error parse game: %s Game_appid = %s",e,appid)
                time.sleep(5)


        self.create_gamesdetails_model(new_list)
