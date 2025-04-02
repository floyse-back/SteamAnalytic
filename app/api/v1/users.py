from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request

from app.schemas.user import User
from app.repository.database import get_async_db
from app.utils.utils import decode_jwt
from app.repository.user_repository import UserRepository

router = APIRouter()


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

@router.put('/user_me/')
async def update_user_me(user:User,session = Depends(get_async_db)):
    return await UserRepository.user_update(session=session,user=user)

@router.get("/user_profile/{user_id}")
async def user_profile(user_id:int):
    return {'user_id': user_id}
