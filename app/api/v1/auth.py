from fastapi import APIRouter, Request, Depends, Response, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.dependencies import verify_user, user_auth_check, user_cookie_auth
from app.application.auth_use_cases.auth_use_cases import AuthService
from app.infrastructure.db.database import get_async_db
from app.domain.users.schemas import User
from app.domain.users.schemas import TokenType
from starlette import status

router = APIRouter(prefix="/auth",tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_service = AuthService()

@router.post("/login",response_model = TokenType,status_code=status.HTTP_201_CREATED)
async def login_user(response: Response,session = Depends(get_async_db), user = Depends(verify_user)) -> TokenType:
    return await auth_service.user_login(response=response,session=session, user=user)

@router.get("/logout/",status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response:Response,is_cookie_auth = Depends(user_cookie_auth)):
    if is_cookie_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    response.delete_cookie("access_token",httponly=True,secure=True)
    response.delete_cookie("refresh_token",httponly=True,secure=True)


@router.post("/register_user/",status_code = status.HTTP_201_CREATED)
async def register_user(user:User,session=Depends(get_async_db)):
    return await auth_service.register_user(user=user,session=session)


@router.delete("/delete_user/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request:Request,response:Response,password:str=Form(),session = Depends(get_async_db)):
    access_token = request.cookies.get("access_token")

    await auth_service.delete_from_user(access_token=access_token,user_password=password,session=session)

    response.delete_cookie("access_token",httponly=True,secure=True)
    response.delete_cookie("refresh_token",httponly=True,secure=True)

@router.post("/refresh_token",status_code=status.HTTP_201_CREATED)
async def refresh_token(request:Request,response:Response,auth:dict=Depends(user_auth_check),session:AsyncSession = Depends(get_async_db)):
    refresh_token = request.cookies.get("refresh_token")

    return await auth_service.refresh_token(refresh_token=refresh_token,user=auth.get("user_id"),session=session,response=response)

