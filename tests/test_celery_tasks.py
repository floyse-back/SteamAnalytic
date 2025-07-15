import random
import pytest
from app.infrastructure.celery_app.tasks.steam_tasks import update_game_icon_url,send_email
from app.infrastructure.celery_app.tasks.news_tasks import update_steam_events, news_task_creator
from tests.conftest import tests_logger as logger


class TestCeleryTasks:
    def test_create_very_big_tasks(self):
        update_game_icon_url.delay()
        for _ in range(10):
            r_n = random.randint(100000,999999)
            send_email.delay("floyse.fake@gmail.com",r_n,"delete_user")

class TestCeleryNewsSenderTasks:
    @pytest.mark.parametrize(
        "type_news",[
            #("news_new_release"),
            #("news_free_games_now"),
            #("news_event_history"),
            #("news_discounts_steam_now"),
            #("news_top_for_a_coins"),
            #("news_random_game"),
            ("news_calendar_event_now"),
        ]
    )
    def test_news_sender_to_queue(self,type_news):
        try:
            news_task_creator(type_news=type_news)
        except Exception as e:
            logger.error(e,exc_info=True)

    def test_update_steam_event_calendars(self):
        try:
            update_steam_events()
            assert True
        except Exception as e:
            logger.error(e, exc_info=True)
            assert False