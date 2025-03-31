from celery import Celery
from celery.schedules import crontab
from app.core.config import CELERY_RESULT_BACKEND,CELERY_BROKER_URL

app = Celery('steam_analitics', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.timezone="Europe/Kiev"
app.conf.broker_connection_retry_on_startup=True

app.conf.beat_schedule = {
    "update_every_night":{
        'task':'app.tasks.steam_tasks.update_steam_games',
        'schedule':crontab(hour="15",minute="25")
    },
    "get_thousand_gamedetails":{
        'task':'app.tasks.steam_tasks.get_game_details',
        'schedule':crontab(hour="3,5,7",minute="0")
    },
    "delete_refresh_tokens_by_time":{
        'task':'app.tasks.steam_tasks.delete_refresh_tokens_by_time',
        'schedule': crontab(hour="11",minute="53")
    },
    "update_game_icon_url":{
        'task': 'app.tasks.steam_tasks.update_game_icon_url',
        'schedule': crontab(hour ="21",minute="21")
    }
}

app.autodiscover_tasks(["app.tasks.steam_tasks"])