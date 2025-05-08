from app.application.dto.user_dto import UserMe, UserElementToken, TokenType
from app.application.exceptions.exception_handler import UserNotAuthorized, UserNotFound, PasswordIncorrect
from app.domain.users.repository import IUserRepository, IBlackListRepository, IRefreshTokenRepository
from app.utils.auth_utils import create_access_token, create_refresh_token
from app.utils.utils import decode_jwt, verify_password


class PutUserUseCase:
    def __init__(self,user_repository:IUserRepository,blacklist_repository:IBlackListRepository,refresh_token_repository:IRefreshTokenRepository):
        self.user_repository = user_repository
        self.blacklist_repository = blacklist_repository
        self.refresh_token_repository = refresh_token_repository

    async def execute(self,session,token,password:str,user:UserMe):
        if not token:
            raise UserNotAuthorized("User not authorized")

        id_element = decode_jwt(token).get("user_id")

        user_model = await self.user_repository.get_user_for_id(user_id=id_element,session=session)
        if user_model is None:
            raise UserNotFound("User don`t found")
        if not verify_password(password,user_model.hashed_password):
            raise PasswordIncorrect("Password incorrect")

        await self.user_repository.user_update(session=session, my_user=user_model, user=user)

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
