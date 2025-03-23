from celery import Celery
from celery.schedules import crontab
from ..config import CELERY_RESULT_BACKEND,CELERY_BROKER_URL

app = Celery('steam_analitics', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.timezone="Europe/Kiev"
app.conf.broker_connection_retry_on_startup=True

app.conf.beat_schedule = {
    "update_every_night":{
        'task':'app.services.tasks.update_steam_games',
        'schedule':crontab(hour="0",minute="0")
    },
    "get_thousand_gamedetails":{
        'task':'app.services.tasks.get_game_details',
        'schedule':crontab(hour="3,5,7",minute="0")
    },
    "delete_refresh_tokens_by_time":{
        'task':'app.services.tasks.delete_refresh_tokens_by_time',
        'schedule': crontab(hour="11",minute="53")
    }
}

app.autodiscover_tasks(["app.services.tasks"])