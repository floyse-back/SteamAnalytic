import datetime

from sqlalchemy import delete

from app.infrastructure.celery_app.celery_app import app, logger
from app.infrastructure.celery_app.database import SessionLocal
from app.infrastructure.db.models.users_models import EmailConfirmed, RefreshToken

@app.task(
    max_retries=3,
    time_limit=120,
)
def upgrade_tokens():
    logger.info("UserTasks: Starting task upgrade_tokens")
    with SessionLocal() as session:
        stmt_1 = delete(EmailConfirmed).filter(EmailConfirmed.expires_at < datetime.datetime.now())
        stmt_2 = delete(RefreshToken).filter(RefreshToken.delete_time < datetime.datetime.now())
        session.execute(stmt_1)
        session.execute(stmt_2)
        session.commit()

    logger.info("UsersTask: Delete Closed Tokens")