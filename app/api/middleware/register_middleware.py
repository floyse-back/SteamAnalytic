from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.middleware.middleware import log_middleware
from app.utils.config import ALLOW_ORIGINS


def register_middleware(app: FastAPI):
    app.middleware("http")(log_middleware)

    allows_origins = ALLOW_ORIGINS.split(",")
    app.add_middleware(CORSMiddleware,
                       allow_origins=allows_origins,
                       allow_methods=["*"],
                       allow_headers=["*"],
                       )

