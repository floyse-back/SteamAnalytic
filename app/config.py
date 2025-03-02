from load_dotenv import load_dotenv
from os import getenv

load_dotenv()

ASYNC_DATABASE_URL = getenv("ASYNC_DATABASE_URL")
SYNC_DATABASE_URL = getenv("SYNC_DATABASE_URL")

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")

STEAM_API_KEY = getenv("STEAM_API_KEY")
STEAMDB_URL = getenv("STEAMDB_URL")
