from abc import ABC, abstractmethod
from typing import List

from app.domain.users.schemas import User, UserMe,UserModel,RefreshToken

class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self,session,user:User):
        pass

    @abstractmethod
    async def get_user_for_id(self,user_id:int,session)->tuple[UserModel]:
        pass

    @abstractmethod
    async def delete_user(self,session,user:UserModel):
        pass

    @abstractmethod
    async def get_user(self,session,username:str)->UserModel:
        pass

    @abstractmethod
    async def user_update(self,session,my_user,user:UserMe):
        pass

    @abstractmethod
    async def delete_refresh_tokens(self,session,id):
        pass

    @abstractmethod
    async def get_user_for_email(self,email:str,session)->UserModel:
        pass

    @abstractmethod
    async def user_verify_update(self,session,status:bool,user_model:UserModel):
        pass

    async def user_password_update(self,session,user_model,new_password):
        pass

class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def verify_refresh_token(self,session,refresh_token):
        pass

    @abstractmethod
    async def delete_refresh_from_id(self,session,user_id):
        pass

    @abstractmethod
    async def delete_refresh_token(self,session,user_id):
        pass

    @abstractmethod
    async def create_refresh_token(self,session,user_id:int,refresh_token:str):
        pass

class IBlackListRepository(ABC):
    @abstractmethod
    async def add_blacklist_tokens(self,refresh_tokens:List[RefreshToken],session):
        pass

    @abstractmethod
    async def verify_blacklist_token(self,session,token) -> bool:
        pass

class IEmailConfirmationRepository(ABC):
    @abstractmethod
    async def create_confirm_token(self,session,token:str,type:str,user_model:UserModel):
        pass

    @abstractmethod
    async def verify_confirm_token(self,session,token:str,type:str):
        pass

    @abstractmethod
    async def delete_confirm_token(self,session,type:str,user_id:int):
        pass




