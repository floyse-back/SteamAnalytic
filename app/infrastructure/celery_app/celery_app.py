from celery import Celery
from celery.schedules import crontab
from app.utils.config import CELERY_RESULT_BACKEND,CELERY_BROKER_URL
from celery.app.log import Logging

app = Celery('steam_analitics', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.timezone="Europe/Kiev"
app.conf.broker_connection_retry_on_startup=True

logger = Logging.get_default_logger(__name__)

app.conf.beat_schedule = {
    "update_every_night":{
        'task':'app.infrastructure.celery_app.tasks.steam_tasks.update_steam_games',
        'schedule':crontab(hour="17",minute="55")
    },
    "get_thousand_gamedetails":{
        'task':'app.infrastructure.celery_app.tasks.steam_tasks.get_game_details',
        'schedule':crontab(hour="18",minute="15")
    },
    "delete_refresh_tokens_by_time":{
        'task':'app.infrastructure.celery_app.tasks.steam_tasks.delete_refresh_tokens_by_time',
        'schedule': crontab(hour="3",minute="25")
    },
    "update_game_icon_url":{
        'task': 'app.infrastructure.celery_app.tasks.steam_tasks.update_game_icon_url',
        'schedule': crontab(hour ="5",minute="0")
    },
    "upgrade_tokens":{
        "task": "app.infrastructure.celery_app.tasks.users_tasks.upgrade_tokens",
        "schedule": crontab(hour="2",minute="20")
    },
    "news_new_release":{
        "task":"app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="13",minute="15"),
        "kwargs":{"type_news":"news_new_release"}
    },
    "news_free_games_now": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="13", minute="34"),
        "kwargs": {"type_news": "news_free_games_now"}
    },
    "news_event_history": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="13", minute="32"),
        "kwargs": {"type_news": "news_event_history"}
    },
    "news_discounts_steam_now": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="13", minute="33"),
        "kwargs": {"type_news": "news_discounts_steam_now"}
    },
    "news_top_for_a_coins": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="13", minute="35"),
        "kwargs": {"type_news": "news_top_for_a_coins"}
    },
    "news_random_game": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="13", minute="36"),
        "kwargs": {"type_news": "news_random_game"}
    },
}

app.autodiscover_tasks([
    "app.infrastructure.celery_app.tasks.steam_tasks",
    "app.infrastructure.celery_app.tasks.users_tasks",
    "app.infrastructure.celery_app.tasks.news_tasks",
    "app.infrastructure.celery_app.tasks.subscribes_tasks"
])