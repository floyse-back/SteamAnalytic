from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.middleware.middleware import log_middleware


def register_middleware(app: FastAPI):
    app.middleware("http")(log_middleware)

    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],
                       allow_methods=["*"],
                       allow_headers=["*"],
                       )

