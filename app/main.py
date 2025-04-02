from fastapi import FastAPI
from app.api.v1 import steam, auth, analytics,users,admin

app = FastAPI()

app.include_router(steam.router, tags=["steam"])
app.include_router(analytics.router, tags=["analytics"])
app.include_router(auth.router, tags=["auth"])
app.include_router(admin.router, tags=["admin"])
app.include_router(users.router, tags=["users"])



