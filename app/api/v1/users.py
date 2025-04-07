from fastapi import APIRouter, Depends, Request, Response, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.dependencies import user_auth_check
from app.domain.users.schemas import UserMe
from app.infrastructure.db.database import get_async_db
from app.application.user_use_cases.user_use_cases import UserUseCase
from starlette import status

router = APIRouter()

user_service = UserUseCase()

@router.get("/user_me",response_model=UserMe,status_code=status.HTTP_200_OK)
async def user_me(request:Request,auth = Depends(user_auth_check),session:AsyncSession = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")
    return await user_service.get_user_me(token,session)

@router.put('/user_me',status_code =status.HTTP_201_CREATED)
async def update_user_me(user:UserMe,request:Request,response:Response,auth = Depends(user_auth_check),password:str=Form,session:AsyncSession = Depends(get_async_db)):
    token = request.cookies.get("access_token")

    data = await user_service.put_user(token=token,session=session,user=user,password=password)

    response.set_cookie("refresh_token",value=data.refresh_token,httponly=True,secure=True)
    response.set_cookie("access_token",value=data.access_token,httponly=True,secure=True)



@router.get("/user_profile/{user_id}")
async def user_profile(user_id:int,session = Depends(get_async_db)):
    return await user_service.get_user_public_profile(user_id,session)
