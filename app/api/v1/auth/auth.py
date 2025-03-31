from fastapi import APIRouter,Request, Depends,Response
from fastapi.security import OAuth2PasswordBearer

from app.api.v1.auth.utils import *
from app.api.v1.auth.verify_auth import token_config, users, verify_user, create_refresh_token, create_access_token
from app.database.database import get_async_db
from app.database.orm import RefreshTokenORM
from app.schemas.user import User
from app.schemas.user import TokenType
from starlette import status

router = APIRouter(prefix="/auth",tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

refresh_orm = RefreshTokenORM()



@router.post("/login",response_model = TokenType,status_code=status.HTTP_201_CREATED)
async def login_user(response: Response,session = Depends(get_async_db), user = Depends(verify_user)) -> TokenType:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    await refresh_orm.create_refresh_token(
        session = session,
        user_id = user.id,
        refresh_token = refresh_token
    )

    response.set_cookie(
        key="access_token",
        value = access_token,
        httponly=True,
        max_age =token_config.access_token_expires * 60
    )

    response.set_cookie(
        key="refresh_token",
        value = refresh_token,
        httponly = True,
        max_age =token_config.refresh_token_expires * 60
    )

    return TokenType(
        access_token = access_token,
        refresh_token= refresh_token
    )

@router.get("/logout/",status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response:Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


@router.post("/register_user/",status_code = status.HTTP_201_CREATED)
async def register_user(session=Depends(get_async_db),user:User=User):
    user.hashed_password = hashed_password(user.hashed_password).decode("utf-8")
    await users.create_user(session, user)
    return {"message":"Register successful"}

@router.get("/user/me")
async def user_me(request:Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail = "No autorization user"
        )

    user = decode_jwt(token)
    return user

@router.delete("/delete_user/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request:Request,response:Response,session = Depends(get_async_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail = "No autorization user"
        )
    user = decode_jwt(access_token)

    await users.delete_user(session, user.get("username"))

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


@router.get("/test")
async def user_test():
    return {}
