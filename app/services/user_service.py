from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.repository.user_repository import UserRepository, UserNotFound
from app.schemas.user import User, UserMe, UserPublic, TokenType
from app.utils.auth_utils import create_access_token, create_refresh_token
from app.utils.utils import decode_jwt


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def put_user(self,token,user:User,session:AsyncSession):
        if not token:
            raise HTTPException(
                status_code=401,
                detail="No autorization user"
            )

        id_element = decode_jwt(token).get("user_id")

        try:
            user = await self.user_repository.user_update(session=session, id=id_element, user=user)
        except UserNotFound as error:
            raise HTTPException(
                detail=f"{error}",
                status_code=status.HTTP_404_NOT_FOUND
            )

        await self.user_repository.delete_refresh_tokens(session, id_element)
        print(user)
        access_token=create_access_token(user)
        refresh_token=create_refresh_token(user)

        return TokenType(access_token=access_token, refresh_token=refresh_token)

    async def get_user_me(self,token,session:AsyncSession)->UserMe:
        if not token:
            raise HTTPException(
                status_code=401,
                detail="No autorization user"
            )

        data = decode_jwt(token)
        user = await self.user_repository.get_user(async_session=session, username=data["username"])

        return UserMe(
            username=user.username,
            email=user.email,
            steamid=user.steamid,
        )

    async def get_user_public_profile(self,user_id:int,session:AsyncSession)->UserPublic:
        user = await self.user_repository.get_user_for_id(user_id=user_id, session=session)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"No such user"
            )

        return UserPublic(
            username=user.username,
            steamid=user.steamid
        )
