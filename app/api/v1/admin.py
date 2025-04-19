from fastapi import APIRouter, Query, Depends

from app.application.admin_use_cases.admin_use_cases import AdminService
from app.infrastructure.db.database import get_async_db
from app.utils.dependencies import get_admin_service

router = APIRouter(prefix="/admin")


@router.get("/user_info")
async def users_details(user_id:int = None,username:str = None,admin_service:AdminService = Depends(get_admin_service),session = Depends(get_async_db)):
    return await admin_service.get_user_info(session=session,username=username,user_id=user_id)

@router.delete("/users_delete")
async def user_delete(user_id:int = None,username:str = None,admin_service:AdminService = Depends(get_admin_service),session = Depends(get_async_db)):
    return await admin_service.delete_user(session=session,username=username,user_id=user_id)
