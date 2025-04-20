from fastapi import Depends,Request
from fastapi.params import Form

from app.application.admin_use_cases.admin_use_cases import AdminService
from app.application.steam_use_cases.steam_use_cases import SteamService
from app.application.user_use_cases.user_use_cases import UserService
from app.infrastructure.db.repository.blacklist_repository import BlackListRepository
from app.infrastructure.db.repository.refresh_token_repository import RefreshTokenRepository
from app.infrastructure.db.repository.steam_repository import SteamRepository
from app.infrastructure.db.repository.user_repository import UserRepository
from app.utils.config import STEAM_API_KEY
from app.application.steam_analitic.analitic_use_cases import AnaliticService
from app.infrastructure.db.database import get_async_db
from app.application.auth_use_cases.auth_use_cases import AuthService
from app.infrastructure.steam_api.client import SteamClient



"""Infrastucture Depends"""
async def get_steam_client() -> SteamClient:
    return SteamClient(STEAM_API_KEY)


"""Service Depends"""
async def get_steam_service(steam_client:SteamClient = Depends(get_steam_client)):
    return SteamService(
        steam=steam_client,
        steam_repository = SteamRepository(),
    )

async def get_analitic_service(
        steam_client:SteamClient = Depends(get_steam_client),
        steam_service:SteamService = Depends(get_steam_service),
):
    return AnaliticService(
        steam = steam_client,
        steam_service = steam_service
    )

async def get_users_service():
    return UserService(
        user_repository = UserRepository(),
        refresh_token_repository = RefreshTokenRepository(),
        blacklist_repository = BlackListRepository(),
    )

async def get_auth_service():
    return AuthService(
        user_repository = UserRepository(),
        refresh_token_repository = RefreshTokenRepository(),
        black_list_repository = BlackListRepository()
    )

async def get_admin_service():
    return AdminService(
        user_repository = UserRepository()
    )



"""Other Depends"""
async def verify_user(session = Depends(get_async_db),auth_service = Depends(get_auth_service),username:str = Form,password:str = Form):
    return await auth_service.verify_user(session,username,password)

async def user_auth_check(request: Request,auth_service = Depends(get_auth_service), session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")

    return await auth_service.user_auth_check(token,session)

async def user_admin_check(request:Request,session=Depends(get_async_db),admin_service = Depends(get_admin_service)):
    token = request.cookies.get("refresh_token")

    return await admin_service.role_check_user(session,token)

async def user_cookie_auth(request:Request):
    if not request.cookies.get("access_token") and not request.cookies.get("refresh_token"):
        return True
    return False


