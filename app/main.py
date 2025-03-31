from fastapi import FastAPI
from app.api.v1 import steam, auth, analytics

app = FastAPI()

app.include_router(steam.router, tags=["steam"])
app.include_router(analytics.router, tags=["analytics"])
app.include_router(auth.router, tags=["auth"])



