from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions.exception_handler import UserNotFound, UserNotAuthorized
from app.application.usecases.get_user import GetUserUseCase
from app.application.usecases.put_user import PutUserUseCase
from app.domain.redis_repository import ICacheRepository
from app.domain.users.repository import IUserRepository, IBlackListRepository, IRefreshTokenRepository
from app.application.dto.user_dto import UserMe, UserPublic
from app.application.decorators.cache import cache_data
from app.utils.utils import decode_jwt


class UserService:
    def __init__(self,user_repository: IUserRepository,blacklist_repository: IBlackListRepository,refresh_token_repository:IRefreshTokenRepository,cache_repository: ICacheRepository):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.blacklist_repository = blacklist_repository
        self.cache_repository = cache_repository

        self.get_user_use_case = GetUserUseCase(
            user_repository = user_repository
        )
        self.put_user_use_case = PutUserUseCase(
            user_repository = user_repository,
            blacklist_repository = blacklist_repository,
            refresh_token_repository = refresh_token_repository,
        )

    async def put_user(self,token,password:str,user:UserMe,session:AsyncSession):
        return await self.put_user_use_case.execute(token=token,password=password,user=user,session=session)

    @cache_data(expire=1200)
    async def get_user_me(self,token,session:AsyncSession)->UserMe:
        if not token:
            raise UserNotAuthorized("User not authorized")

        data = decode_jwt(token)
        user = await self.get_user_use_case.execute(session=session, username=data["username"])

        return UserMe(
            username=user.username,
            email=user.email,
            steamid=user.steamid,
        ).model_dump()

    @cache_data(expire=1200)
    async def get_user_public_profile(self,user_id:int,session:AsyncSession)->UserPublic:
        user = await self.get_user_use_case.execute(user_id=user_id,session=session)
        if not user:
            raise UserNotFound("User don`t found")

        return UserPublic(
            username=user.username,
            steamid=user.steamid
        ).model_dump()
