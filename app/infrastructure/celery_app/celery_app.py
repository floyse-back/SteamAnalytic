from celery import Celery
from celery.schedules import crontab
from app.utils.config import CELERY_RESULT_BACKEND,CELERY_BROKER_URL

app = Celery('steam_analitics', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.timezone="Europe/Kiev"
app.conf.broker_connection_retry_on_startup=True

app.conf.beat_schedule = {
    "update_every_night":{
        'task':'app.infrastructure.celery_app.steam_tasks.update_steam_games',
        'schedule':crontab(hour="13",minute="45")
    },
    "get_thousand_gamedetails":{
        'task':'app.infrastructure.celery_app.steam_tasks.get_game_details',
        'schedule':crontab(hour="18",minute="15")
    },
    "delete_refresh_tokens_by_time":{
        'task':'app.infrastructure.celery_app.steam_tasks.delete_refresh_tokens_by_time',
        'schedule': crontab(hour="3",minute="25")
    },
    "update_game_icon_url":{
        'task': 'app.infrastructure.celery_app.steam_tasks.update_game_icon_url',
        'schedule': crontab(hour ="5",minute="0")
    },
    "upgrade_tokens":{
        "task": "app.infrastructure.celery_app.users_tasks.upgrade_tokens",
        "schedule": crontab(hour="2",minute="20")
    }
}

app.autodiscover_tasks(["app.infrastructure.celery_app.steam_tasks","app.infrastructure.celery_app.users_tasks"])