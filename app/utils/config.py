from typing import Annotated, List

from load_dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from os import getenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv()

ASYNC_DATABASE_URL = getenv("ASYNC_DATABASE_URL")
SYNC_DATABASE_URL = getenv("SYNC_DATABASE_URL")
TEST_DATABASE_URL = getenv("TEST_DATABASE_URL")

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")

STEAM_API_KEY = getenv("STEAM_API_KEY")
STEAMDB_URL = getenv("STEAMDB_URL")

EMAIL_SERVER = getenv("EMAIL_SERVER")
EMAIL_PORT = getenv("EMAIL_PORT")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")
EMAIL_SENDER = getenv("EMAIL_SENDER")

TEST_EMAIL_SERVER = getenv("TEST_EMAIL_SERVER")
TEST_EMAIL_PORT = getenv("TEST_EMAIL_PORT")
TEST_EMAIL_NAME = getenv("TEST_EMAIL_NAME")
TEST_EMAIL_PASSWORD = getenv("TEST_EMAIL_PASSWORD")
TEST_EMAIL_SENDER = getenv("TEST_EMAIL_SENDER")

HOST = getenv("HOST")

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