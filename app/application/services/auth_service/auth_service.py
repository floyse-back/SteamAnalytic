from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions.exception_handler import \
    BlacklistToken, TokenNotFound
from app.application.usecases.delete_user import DeleteUserUseCase
from app.application.usecases.email_verify_confirm import EmailVerifyConfirmUseCase
from app.application.usecases.get_refresh_token import GetRefreshTokenUseCase
from app.application.usecases.put_forgot_password import PutForgotPasswordUseCase
from app.application.usecases.user_login import UserLoginUseCase
from app.application.usecases.user_register import UserRegisterUseCase
from app.application.usecases.verify_email import VerifyEmailUseCase
from app.application.usecases.verify_user import VerifyUserUseCase
from app.domain.users.repository import IUserRepository, IRefreshTokenRepository, IBlackListRepository, \
    IEmailConfirmationRepository
from app.infrastructure.db.models.users_models import UserModel
from app.application.dto.user_dto import User, TokenType
from app.utils.utils import decode_jwt


class AuthService:
    def __init__(self,user_repository:IUserRepository,email_repository:IEmailConfirmationRepository,refresh_token_repository:IRefreshTokenRepository,black_list_repository:IBlackListRepository):
        self.black_list_repository = black_list_repository

        self.verify_user_use_case = VerifyUserUseCase(
            user_repository=user_repository
        )
        self.delete_user_use_case = DeleteUserUseCase(
            user_repository=user_repository,
        )
        self.user_login_use_case = UserLoginUseCase(
            refresh_token_repository=refresh_token_repository
        )
        self.user_register_use_case = UserRegisterUseCase(
            user_repository=user_repository
        )
        self.get_refresh_token_use_case = GetRefreshTokenUseCase(
            user_repository = user_repository
        )

        self.email_verify_confirm_use_case = EmailVerifyConfirmUseCase(
            email_repository=email_repository,
            user_repository=user_repository
        )
        self.verify_email_use_case = VerifyEmailUseCase(
            user_repository=user_repository
        )
        self.put_forgot_password_use_case = PutForgotPasswordUseCase(
            user_repository=user_repository,
        )

    async def verify_user(self,session:AsyncSession, username: str, password: str) -> UserModel:
        return await self.verify_user_use_case.execute(session,username,password)

    async def user_auth_check(self,token, session:AsyncSession):
        "Перевіряє token і якщо він є повертає дані з цього токена"
        if not token:
            raise TokenNotFound("Token not found")

        decoded_token = decode_jwt(token)
        if await self.black_list_repository.verify_blacklist_token(token=token, session=session):
            raise BlacklistToken("Token is blacklisted")

        return decoded_token

    async def user_login(self,session:AsyncSession,user)->TokenType:
        return await self.user_login_use_case.execute(session,user)

    async def register_user(self,user:User,session:AsyncSession):
        return await self.user_register_use_case.execute(session,user=user)

    async def delete_from_user(self,token,user_password,session:AsyncSession):
        user_model = await self.email_verify_confirm_use_case.execute(session,type="delete_user",token=token)
        return await self.delete_user_use_case.execute(session=session,user_password=user_password,user_model=user_model)

    async def refresh_token(self,refresh_token:str,user:str,session:AsyncSession):
        return await self.get_refresh_token_use_case.execute(refresh_token=refresh_token,user=user,session=session)

    async def verify_email(self,session,token):
        user_model = await self.email_verify_confirm_use_case.execute(session=session,type="verify_email",token=token)
        await self.verify_email_use_case.execute(session=session,status=True,user_model=user_model)
        return {"Email Verified":True}

    async def forgot_password(self,session,token,new_password):
        user_model = await self.email_verify_confirm_use_case.execute(session=session,type="forgot_password",token=token)
        await self.put_forgot_password_use_case.execute(session=session,user_model=user_model,new_password=new_password)
