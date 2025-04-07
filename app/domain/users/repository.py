from abc import ABC, abstractmethod

from app.domain.users.schemas import User, UserMe
from app.infrastructure.db.models.users_models import UserModel


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self,session,user:User):
        pass


    @abstractmethod
    async def get_user_for_id(self,user_id:int,session):
        pass

    @abstractmethod
    async def delete_user(self,session,user:UserModel):
        pass

    @abstractmethod
    async def user_get(self,session,username)->UserModel:
        pass

    @abstractmethod
    async def user_update(self,session,my_user,user:UserMe):
        pass

    @abstractmethod
    async def delete_refresh_tokens(self,session,id):
        pass

class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def verify_refresh_token(self,session,refresh_token):
        pass

    @abstractmethod
    async def delete_refresh_tokens(self):
        pass

    @abstractmethod
    async def delete_refresh_token(self):
        pass

    @abstractmethod
    async def create_refresh_token(self):
        pass

class IBlackListRepository(ABC):
    @abstractmethod
    async def add_blacklist_tokens(self):
        pass

    @abstractmethod
    async def verify_blacklist_token(self) -> bool:
        pass


