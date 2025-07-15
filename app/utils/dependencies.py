from fastapi import Depends,Request
from fastapi.params import Form

from app.application.services.admin_service.admin_service import AdminService
from app.application.services.news_service.news_service import NewsService
from app.application.services.notification_service.notification_service import NotificationService
from app.application.services.steam_service.steam_service import SteamService
from app.application.services.subsctibes_service.subscribes_service import SubscribesService
from app.application.services.users_service.users_service import UserService
from app.infrastructure.celery_app.senders.celery_sender import CelerySender
from app.infrastructure.db.repository.analitic_repository import AnaliticRepository
from app.infrastructure.db.repository.blacklist_repository import BlackListRepository
from app.infrastructure.db.repository.email_confirmation_repository import EmailConfirmationRepository
from app.infrastructure.db.repository.refresh_token_repository import RefreshTokenRepository
from app.infrastructure.db.repository.steam_repository import SteamRepository
from app.infrastructure.db.repository.user_repository import UserRepository
from app.infrastructure.db.sync_repository.calendar_repository import CalendarSteamEventRepository
from app.infrastructure.db.sync_repository.news_repository import NewsRepository
from app.infrastructure.db.sync_repository.wishlist_repository import GameWishlistRepository
from app.infrastructure.logger.logger import Logger
from app.infrastructure.messages.consumer import Consumer
from app.infrastructure.redis.redis_repository import CacheRepository
from app.utils.config import STEAM_API_KEY
from app.application.services.analitic_service.analitic_service import AnalyticService
from app.infrastructure.db.database import get_async_db
from app.application.services.auth_service.auth_service import AuthService
from app.infrastructure.steam_api.client import SteamClient



"""Infrastucture Depends"""
def get_cache_repository() -> CacheRepository:
    return CacheRepository(
        logger=Logger(name="infrastructure.CacheRepository",file_path="infrastructure"),
    )

async def get_steam_client() -> SteamClient:
    return SteamClient(
        cache_repository = get_cache_repository(),
        steam_key=STEAM_API_KEY,
        logger = Logger(name="SteamClient",file_path="infrastructure")
        )


"""Service Depends"""
async def get_steam_service(steam_client:SteamClient = Depends(get_steam_client)) -> SteamService:
    return SteamService(
        steam=steam_client,
        steam_repository = SteamRepository(),
        cache_repository = get_cache_repository(),
        logger=Logger(name="application.SteamService",file_path="application")
    )

async def get_analitic_service(
        steam_client:SteamClient = Depends(get_steam_client),
) -> AnalyticService:
    return AnalyticService(
        steam = steam_client,
        cache_repository = get_cache_repository(),
        steam_repository = SteamRepository(),
        analitic_repository=AnaliticRepository(),
        logger=Logger(name="application.AnalyticService",file_path="application")
    )

async def get_users_service() -> UserService:
    return UserService(
        user_repository = UserRepository(),
        refresh_token_repository = RefreshTokenRepository(),
        blacklist_repository = BlackListRepository(),
        cache_repository = get_cache_repository(),
        logger = Logger(name="application.UserService",file_path="application")
    )

async def get_auth_service() -> AuthService:
    return AuthService(
        user_repository = UserRepository(),
        refresh_token_repository = RefreshTokenRepository(),
        black_list_repository = BlackListRepository(),
        email_repository=EmailConfirmationRepository(),
        logger=Logger(name="application.AuthService", file_path="application")
    )

async def get_admin_service() -> AdminService:
    return AdminService(
        user_repository = UserRepository(),
        logger=Logger(name="application.AdminService", file_path="application")
    )

async def get_email_service() -> NotificationService:
    return NotificationService(
        email_confirmation_repository=EmailConfirmationRepository(),
        celery_sender=CelerySender(),
        user_repository=UserRepository(),
        logger=Logger(name="application.GetEmailService", file_path="application")
    )

def get_news_service() -> NewsService:
    return NewsService(
        news_repository=NewsRepository(),
        calendar_repository = CalendarSteamEventRepository(),
        logger=Logger(name="application.NewsService",file_path="application")
    )

def get_subscribes_service() -> SubscribesService:
    return SubscribesService(
        news_repository=NewsRepository(),
        calendar_repository = CalendarSteamEventRepository(),
        wishlist_repository=GameWishlistRepository(),
        logger=Logger(name="application.SubscribesService", file_path="application")
    )

def get_consumer_rabbitmq():
    return Consumer(
        logger = Logger(name="infrastructure.rabbitmq",file_path="infrastructure")
    )

"""Other Depends"""
async def verify_user(session = Depends(get_async_db),auth_service = Depends(get_auth_service),username:str = Form,password:str = Form):
    return await auth_service.verify_user(session,username,password)

async def user_auth_check(request: Request,auth_service = Depends(get_auth_service), session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        token = request.headers.get("Authorization")

    return await auth_service.user_auth_check(token,session)

async def user_admin_check(request:Request,session=Depends(get_async_db),admin_service = Depends(get_admin_service)):
    token = request.cookies.get("refresh_token")

    return await admin_service.role_check_user(session,token)

async def user_cookie_auth(request:Request):
    if not request.cookies.get("access_token") and not request.cookies.get("refresh_token"):
        return True
    return False


