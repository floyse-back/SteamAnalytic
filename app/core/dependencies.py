from fastapi import Depends,Request
from fastapi.params import Form

from app.repository.database import get_async_db
from app.services.auth_service import AuthService


def get_auth_service():
    return AuthService()

async def verify_user(session = Depends(get_async_db),auth_service = Depends(get_auth_service),username:str = Form,password:str = Form):
    return await auth_service.verify_user(session,username,password)

async def user_auth_check(request: Request,auth_service = Depends(get_auth_service), session = Depends(get_async_db)):
    return await auth_service.user_auth_check(request,session)
