from fastapi import FastAPI
from app.api.v1 import analytics, steam
from app.api.v1.auth import auth

app = FastAPI()

app.include_router(steam.router, tags=["steam"])
app.include_router(analytics.router, tags=["analytics"])

app.include_router(auth.router)



