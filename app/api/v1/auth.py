from fastapi import APIRouter,Request, Depends,Response
from fastapi.security import OAuth2PasswordBearer

from app.core.dependencies import verify_user
from app.services.auth_service import AuthService
from app.repository.database import get_async_db
from app.schemas.user import User
from app.schemas.user import TokenType
from starlette import status

router = APIRouter(prefix="/auth",tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_service = AuthService()

@router.post("/login",response_model = TokenType,status_code=status.HTTP_201_CREATED)
async def login_user(response: Response,session = Depends(get_async_db), user = Depends(verify_user)) -> TokenType:
    return await auth_service.user_login(response=response,session=session, user=user)

@router.get("/logout/",status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response:Response):
    response.delete_cookie("access_token",httponly=True,secure=True)
    response.delete_cookie("refresh_token",httponly=True,secure=True)


@router.post("/register_user/",status_code = status.HTTP_201_CREATED)
async def register_user(user:User,session=Depends(get_async_db)):
    return await auth_service.register_user(user=user,session=session)


@router.delete("/delete_user/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request:Request,response:Response,session = Depends(get_async_db)):
    access_token = request.cookies.get("access_token")

    await auth_service.delete_from_user(access_token=access_token,session=session)

    response.delete_cookie("access_token",httponly=True,secure=True)
    response.delete_cookie("refresh_token",httponly=True,secure=True)
