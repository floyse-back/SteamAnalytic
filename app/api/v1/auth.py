from fastapi import APIRouter, Request, Depends, Response, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.config import TokenConfig
from app.utils.dependencies import verify_user, user_auth_check, user_cookie_auth, get_auth_service
from app.infrastructure.db.database import get_async_db
from app.application.dto.user_dto import User, TokenType
from starlette import status

router = APIRouter(prefix="/auth",tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

token_config = TokenConfig()

@router.post("/login",response_model = TokenType,status_code=status.HTTP_201_CREATED)
async def login_user(response: Response,session = Depends(get_async_db),auth_service = Depends(get_auth_service), user = Depends(verify_user)) -> TokenType:
    result = await auth_service.user_login(session=session, user=user)

    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        max_age=token_config.access_token_expires * 60
    )

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        max_age=token_config.refresh_token_expires * 60
    )

    return result

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
async def register_user(user:User,auth_service = Depends(get_auth_service),session=Depends(get_async_db)):
    return await auth_service.register_user(user=user,session=session)


@router.delete("/delete_user/{token}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(token:str,password:str,request:Request,response:Response,auth_service = Depends(get_auth_service),session = Depends(get_async_db)):
    access_token = request.cookies.get("access_token")

    await auth_service.delete_from_user(token=token,access_token=access_token,user_password=password,session=session)

    response.delete_cookie("access_token",httponly=True,secure=True)
    response.delete_cookie("refresh_token",httponly=True,secure=True)

@router.post("/refresh_token",status_code=status.HTTP_201_CREATED)
async def refresh_token(request:Request,response:Response,auth_service = Depends(get_auth_service),auth:dict=Depends(user_auth_check),session:AsyncSession = Depends(get_async_db)):
    refresh_token = request.cookies.get("refresh_token")

    result = await auth_service.refresh_token(refresh_token=refresh_token,user=auth.get("user_id"),session=session)

    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        max_age = token_config.access_token_expires * 60
    )

    return result

@router.get("/verify_email/{token}",status_code=status.HTTP_200_OK)
async def verify_email(token:str,auth=Depends(user_auth_check),auth_service=Depends(get_auth_service),session=Depends(get_async_db)):
    return await auth_service.verify_email(session=session,token=token)

@router.put("/forgot_password/{token}")
async def forgot_password(token:str,new_password,auth_service=Depends(get_auth_service),session=Depends(get_async_db)):
    return await auth_service.forgot_password(session=session,token=token,new_password=new_password)

