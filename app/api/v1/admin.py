from fastapi import APIRouter, Depends

from starlette import status
from app.application.admin_use_cases.admin_use_cases import AdminService
from app.infrastructure.db.database import get_async_db
from app.utils.dependencies import get_admin_service,user_admin_check

router = APIRouter(prefix="/admin")


@router.get("/user_info",status_code=status.HTTP_200_OK)
async def users_details(user_id:int = None,username:str = None,auth=Depends(user_admin_check),admin_service:AdminService = Depends(get_admin_service),session = Depends(get_async_db)):
    return await admin_service.get_user_info(session=session,username=username,user_id=user_id)
 
@router.delete("/user_delete",status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id:int = None,username:str = None,admin_service:AdminService = Depends(get_admin_service),auth=Depends(user_admin_check),session = Depends(get_async_db)):
    return await admin_service.delete_user(session=session,username=username,user_id=user_id)
