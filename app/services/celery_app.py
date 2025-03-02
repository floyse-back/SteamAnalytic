from celery import Celery
from celery.schedules import crontab
from ..config import CELERY_RESULT_BACKEND,CELERY_BROKER_URL

app = Celery('steam_analitics', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.timezone="Europe/Kiev"
app.conf.broker_connection_retry_on_startup=True

app.conf.beat_schedule = {
    "update_every_night":{
        'task':'app.services.tasks.update_steam_games',
        'schedule':crontab(hour=11,minute=10)
    },
    "get_thousand_gamedetails":{
        'task':'app.services.tasks.get_game_details',
        'schedule':crontab(minute=0,hour="3,5,7")
    }
}

app.autodiscover_tasks(["app.services.tasks"])