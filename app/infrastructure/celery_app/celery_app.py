from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange

from app.utils.config import CELERY_RESULT_BACKEND,CELERY_BROKER_URL
from celery.app.log import Logging

app = Celery('steam_analitics', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.timezone="Europe/Kiev"
app.conf.broker_connection_retry_on_startup=True
app.conf.task_default_queue = "steam_analytic"
app.conf.task_default_exchange = "steam_analytic"
app.conf.task_default_routing_key = "steam_analytic"

app.conf.task_queues = (
    Queue(
        "steam_analytic", Exchange("steam_analytic"), routing_key="steam_analytic"
    ),
    Queue(
        "subscribe_analytic", Exchange("notificate"), routing_key="app.infrastructure.celery_app.tasks.subscribes_tasks"
    ),
    Queue(
        "news_analytic", Exchange("notificate"), routing_key="app.infrastructure.celery_app.tasks.news_tasks"
    ),
)


logger = Logging.get_default_logger(__name__)

app.conf.task_routes = {
    'app.infrastructure.celery_app.tasks.subscribes_tasks.*': {
        'queue': 'subscribe_analytic',
        'routing_key': 'app.infrastructure.celery_app.tasks.subscribes_tasks'
    },
    'app.infrastructure.celery_app.tasks.news_tasks.*': {
        'queue': 'news_analytic',
        'routing_key': 'app.infrastructure.celery_app.tasks.news_tasks'
    },
    'app.infrastructure.celery_app.tasks.steam_tasks.*': {
        'queue': 'steam_analytic',
        'routing_key': 'steam_analytic'
    },
    'app.infrastructure.celery_app.tasks.users_tasks.*': {
        'queue': 'steam_analytic',
        'routing_key': 'steam_analytic'
    }
}

app.conf.beat_schedule = {
    # 🔄 Щоденне оновлення
    "update_every_night": {
        'task': 'app.infrastructure.celery_app.tasks.steam_tasks.update_steam_games',
        'schedule': crontab(hour="7", minute="38")
    },

    # 🔒 Токени
    "upgrade_tokens": {
        "task": "app.infrastructure.celery_app.tasks.users_tasks.upgrade_tokens",
        "schedule": crontab(hour="12", minute="20")
    },
    "delete_refresh_tokens_by_time": {
        'task': 'app.infrastructure.celery_app.tasks.steam_tasks.delete_refresh_tokens_by_time',
        'schedule': crontab(hour="3", minute="25")
    },

    # 🖼️ Іконки
    "update_game_icon_url": {
        'task': 'app.infrastructure.celery_app.tasks.steam_tasks.update_game_icon_url',
        'schedule': crontab(hour="5", minute="0")
    },
    # 📰 Новини (міксовані і рівномірні)
    "news_free_games_now": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="12", minute="20"),
        "kwargs": {"type_news": "news_free_games_now"}
    },
    "news_ganre_strategy": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_game_from_ganre",
        "schedule": crontab(hour="12", minute="25"),
        "kwargs": {"ganre_name": "Стратегії"}
    },
    "news_new_release": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="12", minute="30"),
        "kwargs": {"type_news": "news_new_release"}
    },
    "news_ganre_fights": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_game_from_ganre",
        "schedule": crontab(hour="12", minute="35"),
        "kwargs": {"ganre_name": "Бойовики"}
    },
    "news_top_for_a_coins": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="12", minute="40"),
        "kwargs": {"type_news": "news_top_for_a_coins"}
    },
    "news_ganre_adventure": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_game_from_ganre",
        "schedule": crontab(hour="13", minute="42"),
        "kwargs": {"ganre_name": "Пригоди"}
    },
    "news_event_history": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="12", minute="43"),
        "kwargs": {"type_news": "news_event_history"}
    },
    "news_discounts_steam_now": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="12", minute="44"),
        "kwargs": {"type_news": "news_discounts_steam_now"}
    },
    "news_random_game": {
        "task": "app.infrastructure.celery_app.tasks.news_tasks.news_task_creator",
        "schedule": crontab(hour="12", minute="45"),
        "kwargs": {"type_news": "news_random_game"}
    },
    "subscribe_new_release": {
        "task": "app.infrastructure.celery_app.tasks.subscribes_tasks.subscribes_task",
        "schedule": crontab(hour="12", minute="47"),
        "kwargs": {"sub_type": "subscribe_new_release"}
    },
    "subscribe_free_games": {
        "task": "app.infrastructure.celery_app.tasks.subscribes_tasks.subscribes_task",
        "schedule": crontab(hour="12", minute="50"),
        "kwargs": {"sub_type": "subscribe_free_games_now"}
    },
    "subscribe_hot_discount_notificate": {
        "task": "app.infrastructure.celery_app.tasks.subscribes_tasks.subscribes_task",
        "schedule": crontab(hour="12", minute="53"),
        "kwargs": {"sub_type": "subscribe_hot_discount_notificate"}
    },
    "subscribe_steam_news": {
        "task": "app.infrastructure.celery_app.tasks.subscribes_tasks.subscribes_task",
        "schedule": crontab(hour="12", minute="55"),
        "kwargs": {"sub_type": "subscribe_steam_news"}
    }
}

app.autodiscover_tasks([
    "app.infrastructure.celery_app.tasks.steam_tasks",
    "app.infrastructure.celery_app.tasks.users_tasks",
    "app.infrastructure.celery_app.tasks.news_tasks",
    "app.infrastructure.celery_app.tasks.subscribes_tasks"
])
