from fastapi import Request
from fastapi.responses import JSONResponse

from app.application.exceptions.exception_handler import *


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
        status_code=401,
        content={"detail": "Token blacklisted"}
    )