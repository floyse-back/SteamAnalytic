from fastapi import APIRouter,Depends

from app.infrastructure.db.database import get_async_db
from app.utils.dependencies import get_email_service, user_auth_check

router = APIRouter(prefix="/api/v1", tags=["email"])

@router.post("/send_email/{type}")
async def send_email(type:str,session=Depends(get_async_db),auth=Depends(user_auth_check),email_service = Depends(get_email_service)):
    return await email_service.send_email(type=type,id=auth.get("user_id"),session=session)