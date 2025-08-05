import random
import pytest
from app.infrastructure.celery_app.tasks.steam_tasks import update_game_icon_url, send_email, update_steam_games, \
    get_game_details, get_games_new_released
from app.infrastructure.celery_app.tasks.news_tasks import update_steam_events, news_task_creator, news_game_from_type
from app.infrastructure.celery_app.tasks.subscribes_tasks import subscribes_task
from app.infrastructure.messages.producer import EventProducer
from tests.conftest import tests_logger as logger

def test_steam_update_released_games_task():
    get_games_new_released.delay()

def test_steam_update_free_games_task():
    get_games_new_released.delay(
        type_task = "free"
    )

def test_steam_upgrade_steam_games_task():
    get_game_details.delay()

def test_steam_update_events_task():
    update_steam_events.delay()

class TestCeleryTasks:
    def test_create_very_big_tasks(self):
        update_game_icon_url.delay()
        for _ in range(10):
            r_n = random.randint(100000,999999)
            send_email.delay("floyse.fake@gmail.com",r_n,"delete_user")


class TestCeleryNewsSenderTasks:
    @pytest.mark.parametrize(
        "type_news",[
            #("news_free_games_now"),
            #("news_top_for_a_coins"),
            #("news_discounts_steam_now"),
            #("news_new_release"),
            #("news_event_history"),
            #("news_random_game"),
            #("news_calendar_event_now"),
        ]
    )
    def test_news_sender_to_queue(self,type_news):
        try:
            news_task_creator(type_news=type_news)
        except Exception as e:
            logger.error(e,exc_info=True)

    @pytest.mark.parametrize(
        "ganre_name",[
            ("Пригоди"),
            ("Стратегії"),
            ("Рольові ігри")
        ]
    )
    def test_news_ganres_to_queue(self,ganre_name):
        try:
            news_game_from_type.delay(name=ganre_name)
        except Exception as e:
            logger.error(e,exc_info=True)

    @pytest.mark.parametrize(
        "category_name",[
            ("Кооперативна гра"),
            ("Колекційні картки Steam"),
        ]
    )
    def test_news_categories_to_queue(self,category_name):
        try:
            news_game_from_type.delay(name=category_name,type="category")
        except Exception as e:
            logger.error(e,exc_info=True)

    def test_update_steam_event_calendars(self):
        try:
            update_steam_events()
            assert True
        except Exception as e:
            logger.error(e, exc_info=True)
            assert False

class TestCelerySubscribeSenderTasks:
    @pytest.mark.parametrize(
        "sub_type",[
            ("subscribe_new_release"),
            ("subscribe_free_games_now"),
            ("subscribe_hot_discount_notificate"),
            ("subscribe_steam_news")
        ]
    )
    def test_subscribing(self,sub_type):
        try:
            subscribes_task(sub_type=sub_type)
            assert True
        except Exception as e:
            logger.error(e,exc_info=True)
            assert False

    def test_wishlist(self):
        event_producer = EventProducer(logger=logger)
        event_producer.send_message(body={"type": "update_steam_games", "status": True}, queue="subscribe_queue")