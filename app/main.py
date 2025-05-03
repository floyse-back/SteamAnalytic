from fastapi import FastAPI
from app.api.v1 import steam, auth, analytics,users,admin,email
from app.api.http_exceptions import *
from app.infrastructure.celery_app.steam_tasks import send_email

app = FastAPI()

@app.get("/health_check")
async def health_check():
    send_email.delay("floyse.fake@gmail.com","Auth","health_check")
    return {"status": "ok"}

app.include_router(steam.router, tags=["steam"])
app.include_router(analytics.router, tags=["analytics"])
app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, tags=["users"])
app.include_router(admin.router, tags=["admin"])
app.include_router(email.router, tags=["email"])

app.add_exception_handler(UserNotFound, user_not_found_handler)
app.add_exception_handler(UserNotAuthorized, user_not_authorized_handler)
app.add_exception_handler(PasswordIncorrect, password_incorrect_handler)
app.add_exception_handler(TokenNotFound, token_not_found_handler)
app.add_exception_handler(BlacklistToken, blacklist_token_handler)
app.add_exception_handler(ProfilePrivate, profile_private_handler)
app.add_exception_handler(SteamUserNotFound, steam_user_not_found_handler)
app.add_exception_handler(SteamGameNotFound,steam_game_not_found_handler)
app.add_exception_handler(UserNotPermitions, user_not_permitions_handler)
app.add_exception_handler(UserRegisterError,user_register_handler)
app.add_exception_handler(InfrastructureUserRegister, user_register_handler)
app.add_exception_handler(SteamGameAchievementsNotFoundDetails,steam_game_not_found_handler)
app.add_exception_handler(SteamUserAchievementsNotFoundDetails,steam_user_not_found_handler)
app.add_exception_handler(PageNotFound, page_not_found_handler)
app.add_exception_handler(ExpiredToken, expired_token_handler)
app.add_exception_handler(GamesNotFound, games_not_found_handler)