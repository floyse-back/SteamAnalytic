from load_dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from os import getenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv()

ASYNC_DATABASE_URL = getenv("ASYNC_DATABASE_URL")
SYNC_DATABASE_URL = getenv("SYNC_DATABASE_URL")

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")

STEAM_API_KEY = getenv("STEAM_API_KEY")
STEAMDB_URL = getenv("STEAMDB_URL")

EMAIL_NAME = getenv("EMAIL_NAME")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")

HOST = getenv("HOST")

class TokenConfig(BaseModel):
    private_key_link:Path = BASE_DIR  / "app" / "certs" / "jwt-private.pem"
    public_key_link:Path = BASE_DIR / "app" / "certs" / "jwt-public.pem"
    token_type: str = "bearer"
    algorithm: str = "RS256"

    access_token_expires: int = 15
    refresh_token_expires: int = 60