from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions.exception_handler import PasswordIncorrect, UserNotFound, UserNotAuthorized, \
    BlacklistToken, TokenNotFound, UserRegisterError
from app.application.usecases.delete_user import DeleteUserUseCase
from app.application.usecases.user_login import UserLoginUseCase
from app.application.usecases.user_register import UserRegisterUseCase
from app.application.usecases.verify_user import VerifyUserUseCase
from app.domain.users.repository import IUserRepository, IRefreshTokenRepository, IBlackListRepository, \
    IEmailConfirmationRepository
from app.infrastructure.exceptions.exception_handler import InfrastructureUserRegister
from app.utils.config import TokenConfig
from app.infrastructure.db.models.users_models import UserModel
from app.application.dto.user_dto import User, TokenType
from app.utils.auth_utils import create_access_token
from app.utils.utils import verify_password, decode_jwt, hashed_password


class AuthService:
    def __init__(self,user_repository:IUserRepository,email_repository:IEmailConfirmationRepository,refresh_token_repository:IRefreshTokenRepository,black_list_repository:IBlackListRepository):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.black_list_repository = black_list_repository
        self.token_config = TokenConfig()
        self.email_repository = email_repository

        self.verify_user_use_case = VerifyUserUseCase(
            user_repository=user_repository
        )
        self.delete_user_use_case = DeleteUserUseCase(
            user_repository=user_repository,
            email_repository=email_repository
        )
        self.user_login_use_case = UserLoginUseCase(
            refresh_token_repository=refresh_token_repository
        )
        self.user_register_use_case = UserRegisterUseCase(
            user_repository=user_repository
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
        return await self.delete_user_use_case.execute(session=session,token=token,user_password=user_password)

    async def refresh_token(self,refresh_token:str,user:str,session:AsyncSession):
        user_model = await self.user_repository.get_user_for_id(user_id=int(user), session=session)

        access_token = create_access_token(user=user_model)

        return TokenType(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def verify_email(self,session,token):
        email_model = await  self.email_repository.verify_confirm_token(session=session,type="verify_email",token=token)
        if not email_model:
            raise TokenNotFound()

        user_model = await self.user_repository.get_user_for_id(session=session,user_id=email_model.user_id)
        if not user_model:
            raise UserNotFound()

        await self.user_repository.user_verify_update(session=session,status=True,user_model=user_model)
        return {"Email Verified":True}

    async def forgot_password(self,session,token,new_password):
        email_model = await self.email_repository.verify_confirm_token(session=session,type="forgot_password",token=token)
        if not email_model:
            raise TokenNotFound()

        user_model = await self.user_repository.get_user_for_id(session=session,user_id=email_model.user_id)
        if not user_model:
            raise UserNotFound()

        await self.user_repository.user_password_update(session=session,new_password=new_password,user_model=user_model)
