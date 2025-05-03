from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions.exception_handler import PasswordIncorrect, UserNotFound, UserNotAuthorized, \
    BlacklistToken, TokenNotFound, UserRegisterError
from app.domain.users.repository import IUserRepository, IRefreshTokenRepository, IBlackListRepository, \
    IEmailConfirmationRepository
from app.infrastructure.exceptions.exception_handler import InfrastructureUserRegister
from app.utils.config import TokenConfig
from app.infrastructure.db.models.users_models import UserModel
from app.application.dto.user_dto import User, TokenType
from app.utils.auth_utils import create_access_token, create_refresh_token
from app.utils.utils import verify_password, decode_jwt, hashed_password


class AuthService:
    def __init__(self,user_repository:IUserRepository,email_repository:IEmailConfirmationRepository,refresh_token_repository:IRefreshTokenRepository,black_list_repository:IBlackListRepository):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.black_list_repository = black_list_repository
        self.token_config = TokenConfig()
        self.email_repository = email_repository

    async def verify_user(self,session:AsyncSession, username: str, password: str) -> UserModel:
        user = await self.user_repository.get_user(session, username)
        if not user:
            raise UserNotFound("User not found")

        if not verify_password(password, user.hashed_password):
            raise PasswordIncorrect("Password incorrect")

        return user

    async def user_auth_check(self,token, session:AsyncSession):
        "Перевіряє token і якщо він є повертає дані з цього токена"
        if not token:
            raise TokenNotFound("Token not found")

        decoded_token = decode_jwt(token)
        if await self.black_list_repository.verify_blacklist_token(token=token, session=session):
            raise BlacklistToken("Token is blacklisted")

        return decoded_token

    async def user_login(self,session:AsyncSession,user)->TokenType:
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        await self.refresh_token_repository.create_refresh_token(
            session=session,
            user_id=user.id,
            refresh_token=refresh_token
        )

        return TokenType(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def register_user(self,user:User,session:AsyncSession):
        user.hashed_password = hashed_password(user.hashed_password)

        try:
            await self.user_repository.create_user(session, user)
        except InfrastructureUserRegister:
            raise UserRegisterError("User not registered")

        return {"message":"Register successful"}

    async def delete_from_user(self,token,access_token,user_password,session:AsyncSession):
        if not access_token:
            raise UserNotAuthorized("Access token is invalid")

        refresh_token_data = decode_jwt(access_token)
        user = await self.user_repository.get_user_for_id(user_id=refresh_token_data.get("user_id"),session=session)

        #Перевірка на правильність введеного пароля
        if not user:
            raise UserNotFound(f"User Not Found")

        if not verify_password(user_password, user.hashed_password):
            raise PasswordIncorrect("Incorrect password")

        email_model = await self.email_repository.verify_confirm_token(token=token,session=session,type="delete_user")
        if not email_model:
            raise TokenNotFound("Token not found")

        await self.user_repository.delete_user(session,user)

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
