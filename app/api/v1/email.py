from fastapi import APIRouter,Depends
from starlette import status

from app.infrastructure.db.database import get_async_db
from app.utils.dependencies import get_email_service, user_auth_check

router = APIRouter(prefix="/api/v1", tags=["email"])

@router.post("/send_email/forgot_password",status_code=status.HTTP_202_ACCEPTED)
async def send_email(email,session=Depends(get_async_db),auth=Depends(user_auth_check),email_service = Depends(get_email_service)):
    return await email_service.send_email(type="forgot_password",email=email,session=session)

@router.post("/send_email/{type}",status_code=status.HTTP_202_ACCEPTED)
async def send_email(type:str,email,session=Depends(get_async_db),email_service = Depends(get_email_service)):
    return await email_service.send_email(type=type,email=email,session=session)