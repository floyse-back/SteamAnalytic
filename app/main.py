from fastapi import FastAPI
from app.routers import users,steam,analytics
from app.routers.auth import auth
app = FastAPI()

app.include_router(users.router,prefix="/users",tags=["Users"])
app.include_router(steam.router,prefix="/steam",tags=["steam"])
app.include_router(analytics.router,prefix="/analytics",tags=["analytics"])

app.include_router(auth.router)



