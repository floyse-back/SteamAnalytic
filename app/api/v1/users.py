from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request

from app.core.config import HOST
from app.schemas.user import User, UserMe, UserPublic
from app.repository.database import get_async_db
from app.services.auth_service import user_auth_check
from app.utils.utils import decode_jwt
from app.repository.user_repository import UserRepository, UserNotFound
from httpx import AsyncClient
from starlette import status

router = APIRouter()


@router.get("/user_me",response_model=UserMe,status_code=status.HTTP_200_OK)
async def user_me(request:Request,auth = Depends(user_auth_check),session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail = "No autorization user"
        )

    data = decode_jwt(token)
    user = await UserRepository.get_user(async_session = session, username = data["username"])

    return UserMe(
        username = user.username,
        email = user.email,
        steamid= user.steamid,
    )

@router.put('/user_me',status_code =status.HTTP_201_CREATED)
async def update_user_me(user:User,request:Request,auth = Depends(user_auth_check),session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail = "No autorization user"
        )
    id_element = decode_jwt(token).get("user_id")
    try:
        await UserRepository.user_update(session=session,id=id_element,user=user)
    except UserNotFound as error:
        raise HTTPException(
            detail = f"{error}",
            status_code = status.HTTP_404_NOT_FOUND
        )
    async with AsyncClient(base_url=f"http://{HOST}") as client:
        response_logout=await client.get("/auth/logout/")
        if response_logout.status_code != 204:
            raise HTTPException(
                status_code=response_logout.status_code,
                detail = "User logout failed",
            )
        data = {
            "username": user.username,
            "password": user.hashed_password
        }
        login_response = await client.post("/auth/login/",data=data)
        if login_response.status_code != 201:
            raise HTTPException(
                status_code=login_response.status_code,
                detail = "Login failed",
            )

@router.get("/user_profile/{user_id}")
async def user_profile(user_id:int,auth = Depends(user_auth_check),session = Depends(get_async_db)):
    user = await UserRepository.get_user_for_id(user_id = user_id, session = session)
    if not user:
        raise HTTPException(
            status_code=404,
            detail = f"No such user"
        )

    return UserPublic(
        username = user.username,
        steamid = user.steamid
    )
