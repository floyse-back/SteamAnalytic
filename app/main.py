from fastapi import FastAPI
from app.api.v1 import steam, auth, analytics,users,admin
from app.application.exceptions import *
from app.api.http_exceptions import *

app = FastAPI()

app.include_router(steam.router, tags=["steam"])
app.include_router(analytics.router, tags=["analytics"])
app.include_router(auth.router, tags=["auth"])
app.include_router(admin.router, tags=["admin"])
app.include_router(users.router, tags=["users"])

app.add_exception_handler(UserNotFound, user_not_found_handler)
app.add_exception_handler(UserNotAuthorized, user_not_authorized_handler)
app.add_exception_handler(PasswordIncorrect, password_incorrect_handler)
app.add_exception_handler(TokenNotFound, token_not_found_handler)
app.add_exception_handler(BlacklistToken, blacklist_token_handler)
app.add_exception_handler(ProfilePrivate, profile_private_handler)

