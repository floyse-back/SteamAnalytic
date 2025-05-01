from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions.exception_handler import PasswordIncorrect, UserNotFound, UserNotAuthorized
from app.domain.redis_repository import ICacheRepository
from app.domain.users.repository import IUserRepository, IBlackListRepository, IRefreshTokenRepository
from app.application.dto.user_dto import TokenType, UserMe, UserPublic, UserElementToken
from app.application.decorators.cache import cache_data
from app.utils.auth_utils import create_access_token, create_refresh_token
from app.utils.utils import decode_jwt, verify_password


class UserService:
    def __init__(self,user_repository: IUserRepository,blacklist_repository: IBlackListRepository,refresh_token_repository:IRefreshTokenRepository,cache_repository: ICacheRepository):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.blacklist_repository = blacklist_repository
        self.cache_repository = cache_repository

    async def put_user(self,token,password:str,user:UserMe,session:AsyncSession):
        if not token:
            raise UserNotAuthorized("User not authorized")

        id_element = decode_jwt(token).get("user_id")

        user_model = await self.user_repository.get_user_for_id(user_id=id_element,session=session)
        if user_model is None:
            raise UserNotFound("User don`t found")
        if not verify_password(password,user_model.hashed_password):
            raise PasswordIncorrect("Password incorrect")

        new_user = await self.user_repository.user_update(session=session, my_user=user_model, user=user)

        data = UserElementToken(
            id= id_element,
            username = user.username,
            email = user.email
        )

        my_user = await self.user_repository.delete_refresh_tokens(session, id_element)
        await self.blacklist_repository.add_blacklist_tokens(refresh_tokens=my_user.refresh_tokens, session=session)
        await self.refresh_token_repository.delete_refresh_from_id(session=session, user_id=id_element)

        access_token=create_access_token(data)
        refresh_token=create_refresh_token(data)

        return TokenType(access_token=access_token, refresh_token=refresh_token)

    @cache_data(expire=1200)
    async def get_user_me(self,token,session:AsyncSession)->UserMe:
        if not token:
            raise UserNotAuthorized("User not authorized")

        data = decode_jwt(token)
        user = await self.user_repository.get_user(session=session, username=data["username"])

        return UserMe(
            username=user.username,
            email=user.email,
            steamid=user.steamid,
        ).model_dump()

    @cache_data(expire=1200)
    async def get_user_public_profile(self,user_id:int,session:AsyncSession)->UserPublic:
        user = await self.user_repository.get_user_for_id(user_id=user_id, session=session)
        if not user:
            raise UserNotFound("User don`t found")


        return UserPublic(
            username=user.username,
            steamid=user.steamid
        ).model_dump()
