from typing import List

from load_dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from os import getenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv()

ASYNC_DATABASE_URL = getenv("ASYNC_DATABASE_URL")
SYNC_DATABASE_URL = getenv("SYNC_DATABASE_URL")

TEST_DATABASE_URL = getenv("TEST_DATABASE_URL")
TEST_DATABASE_SYNC_URL = getenv("TEST_DATABASE_SYNC_URL")

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")

REDIS_HOST = getenv("REDIS_HOST")
RABBITMQ_HOST = getenv("RABBITMQ_HOST")

STEAM_API_KEY = getenv("STEAM_API_KEY")

EMAIL_SERVER = getenv("EMAIL_SERVER")
EMAIL_PORT = getenv("EMAIL_PORT")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")
EMAIL_SENDER = getenv("EMAIL_SENDER")
LOGGER_LEVEL = getenv("LOGGER_LEVEL")

HOST = getenv("HOST")

HOST_PATH = getenv("HOST_PATH")
PORT = getenv("PORT")

class TokenConfig(BaseModel):
    private_key_link:Path = BASE_DIR  / "app" / "certs" / "jwt-private.pem"
    public_key_link:Path = BASE_DIR / "app" / "certs" / "jwt-public.pem"
    token_type: str = "bearer"
    algorithm: str = "RS256"

    access_token_expires: int = 15
    refresh_token_expires: int = 60


class ServiceConfig(BaseModel):
    path:str = ""
    tags:List = ""

class ServicesConfig(BaseModel):
    steam_service:ServiceConfig = ServiceConfig(
        path = "/api/v1/steam",
        tags = ["steam"]
    )
    analytic_service:ServiceConfig = ServiceConfig(
        path = "/api/v1/analytics",
        tags = ["analytics"]
    )
    auth_service:ServiceConfig = ServiceConfig(
        path = "/api/v1/auth",
        tags = ["auth"]
    )
    users_service:ServiceConfig = ServiceConfig(
        path = "/api/v1/users",
        tags = ["users"]
    )
    admin_service:ServiceConfig = ServiceConfig(
        path = "/api/v1/admin",
        tags = ["admin"]
    )
    notification_service:ServiceConfig = ServiceConfig(
        path = "/api/v1/notification",
        tags = ["notification"]
    )