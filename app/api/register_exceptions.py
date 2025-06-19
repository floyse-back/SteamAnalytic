from fastapi import FastAPI
from app.api.http_exceptions import *

def register_exceptions(app: FastAPI):
    app.add_exception_handler(UserNotFound, user_not_found_handler)
    app.add_exception_handler(UserNotAuthorized, user_not_authorized_handler)
    app.add_exception_handler(PasswordIncorrect, password_incorrect_handler)
    app.add_exception_handler(TokenNotFound, token_not_found_handler)
    app.add_exception_handler(InfrastructureTokenNotFound, token_not_found_handler)
    app.add_exception_handler(BlacklistToken, blacklist_token_handler)
    app.add_exception_handler(ProfilePrivate, profile_private_handler)
    app.add_exception_handler(SteamUserNotFound, steam_user_not_found_handler)
    app.add_exception_handler(SteamGameNotFound, steam_game_not_found_handler)
    app.add_exception_handler(UserNotPermitions, user_not_permitions_handler)
    app.add_exception_handler(UserRegisterError, user_register_handler)
    app.add_exception_handler(InfrastructureUserRegister, user_register_handler)
    app.add_exception_handler(SteamGameAchievementsNotFoundDetails, steam_game_not_found_handler)
    app.add_exception_handler(SteamUserAchievementsNotFoundDetails, steam_user_not_found_handler)
    app.add_exception_handler(PageNotFound, page_not_found_handler)
    app.add_exception_handler(ExpiredToken, expired_token_handler)
    app.add_exception_handler(GamesNotFound, games_not_found_handler)
    app.add_exception_handler(IncorrectType, incorrect_type_handler)
    app.add_exception_handler(SteamExceptionBase,steam_base_exception_handler)
    app.add_exception_handler(SteamNginxException,steam_nginx_exception_handler)