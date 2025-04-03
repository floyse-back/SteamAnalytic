from fastapi import APIRouter,Depends
from starlette.requests import Request

from app.schemas.user import User, UserMe
from app.repository.database import get_async_db
from app.services.auth_service import user_auth_check
from app.services.user_service import UserService
from starlette import status

router = APIRouter()

user_service = UserService()

@router.get("/user_me",response_model=UserMe,status_code=status.HTTP_200_OK)
async def user_me(request:Request,auth = Depends(user_auth_check),session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")
    return await user_service.get_user_me(token,session)

@router.put('/user_me',status_code =status.HTTP_201_CREATED)
async def update_user_me(user:User,request:Request,auth = Depends(user_auth_check),session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")
    await user_service.put_user(token=token,session=session,user=user)


@router.get("/user_profile/{user_id}")
async def user_profile(user_id:int,session = Depends(get_async_db)):
    return await user_service.get_user_public_profile(user_id,session)
