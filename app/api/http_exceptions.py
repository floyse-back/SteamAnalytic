from fastapi import Request
from fastapi.responses import JSONResponse

from app.application.exceptions.exception_handler import *
from app.infrastructure.exceptions.exception_handler import *


async def user_not_found_handler(request:Request,exc:UserNotFound):
    return JSONResponse(status_code=404,
                         content={"detail":"User Not Found"}
                         )

async def user_not_authorized_handler(request:Request,exc:UserNotAuthorized):
    return JSONResponse(status_code=401,
                         content={"detail":"User Not Authorized"}
                         )

async def password_incorrect_handler(request:Request,exc:PasswordIncorrect):
    return JSONResponse(
        status_code=401,
        content={"detail": "Incorrect password"}
    )

async def token_not_found_handler(request:Request,exc:TokenNotFound):
    return JSONResponse(
        status_code=401,
        content={"detail": "Token not found"}
    )

async def blacklist_token_handler(request:Request,exc:BlacklistToken):
    return JSONResponse(
        status_code=403,
        content={"detail": "Token blacklisted"}
    )

async def profile_private_handler(request:Request,exc:ProfilePrivate):
    return JSONResponse(
        status_code=403,
        content={"detail": f"Profile Private {exc.user_profile}"}
    )

async def steam_game_not_found_handler(request:Request,exc:SteamGameNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Steam game not found"}
    )

async def steam_user_not_found_handler(request:Request,exc:SteamUserNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Steam user not found"}
    )