from fastapi import Depends,Request
from fastapi.params import Form

from app.infrastructure.db.database import get_async_db
from app.application.auth_use_cases.auth_use_cases import AuthUseCase


def get_auth_service():
    return AuthUseCase()

async def verify_user(session = Depends(get_async_db),auth_service = Depends(get_auth_service),username:str = Form,password:str = Form):
    return await auth_service.verify_user(session,username,password)

async def user_auth_check(request: Request,auth_service = Depends(get_auth_service), session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")

    return await auth_service.user_auth_check(token,session)

async def user_cookie_auth(request:Request,auth_service = Depends(get_auth_service)):
    if not request.cookies.get("access_token") and not request.cookies.get("refresh_token"):
        return True
    return False
