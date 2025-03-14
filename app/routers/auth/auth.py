from fastapi import APIRouter,Request,Form,HTTPException,Depends,Response
from app.routers.auth.utils import *
from ...database.orm import UsersORM
from ...database.database import session
from ...schemas import User
from datetime import datetime,timedelta,timezone
from app.config import TokenConfig
from ...schemas import TokenType

token_config = TokenConfig()

router = APIRouter(prefix="/auth",tags=["auth"])
users = UsersORM()

async def verify_user(username:str = Form(),password:str = Form()) -> User:
    user  = await users.get_user(session,username)
    if not user:
        raise HTTPException(status_code=404,detail = "User not found")

    if not  verify_password(password,user.hashed_password.encode("utf-8")):
        print(password)
        raise HTTPException(status_code=404,detail = "Incorrect password")

    return user

def create_refresh_token(user: User) -> str:
    payload = {
        "sub": user.username,
        "type":"refresh_token",
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=token_config.refresh_token_expires),
    }

    token = encode_jwt(payload)
    return token

def create_access_token(user: User) -> str:
    payload = {
        "sub": user.username,
        "type": "access_token",
        "username": user.username,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=token_config.access_token_expires),
    }

    token = encode_jwt(payload)
    return token

@router.post("/login",response_model = TokenType)
async def login_user(response: Response,user = Depends(verify_user)):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response.set_cookie(
        key="access_token",
        value = access_token,
        httponly=True,
        max_age = token_config.access_token_expires*60
    )

    response.set_cookie(
        key="refresh_token",
        value = refresh_token,
        httponly = True,
        max_age = token_config.refresh_token_expires*60
    )

    return TokenType(
        access_token = access_token,
        refresh_token= refresh_token
    )

@router.get("/logout/")
async def logout_user(response:Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message":"Logout successful"}

@router.post("/register_user/")
async def register_user(user:User=User):
    user.hashed_password = hashed_password(user.hashed_password).decode("utf-8")
    await users.create_user(session,user)
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
