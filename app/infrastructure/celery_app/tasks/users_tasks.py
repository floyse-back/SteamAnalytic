import datetime

from sqlalchemy import delete

from app.infrastructure.celery_app.celery_app import app, logger
from app.infrastructure.celery_app.database import get_db
from app.infrastructure.db.models.users_models import EmailConfirmed, RefreshToken

@app.task(
    max_retries=3,
    time_limit=120,
)
def upgrade_tokens():
    logger.info("UserTasks: Starting task upgrade_tokens")
    db = next(get_db())

    stmt_1 = delete(EmailConfirmed).filter(EmailConfirmed.expires_at < datetime.datetime.now())
    stmt_2 = delete(RefreshToken).filter(RefreshToken.delete_time < datetime.datetime.now())
    db.execute(stmt_1)
    db.execute(stmt_2)
    db.commit()

    logger.info("UsersTask: Delete Closed Tokens")