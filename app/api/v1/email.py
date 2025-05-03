from fastapi import APIRouter,Depends

from app.infrastructure.db.database import get_async_db
from app.utils.dependencies import get_email_service

router = APIRouter(prefix="/email", tags=["email"])


@router.get("/verify_type/{type}/")
async def verify_url(type:str,token:str,session=Depends(get_async_db),email_service = Depends(get_email_service)):
    try:
        return await email_service.verify_url(session=session,type=type,token=token)
    except KeyError:
        return False

@router.post("/send_email/{type}/")
async def send_email(receiver:str,type:str,session=Depends(get_async_db),email_service = Depends(get_email_service)):
    return await email_service.send_email(receiver=receiver,type=type,session=session)