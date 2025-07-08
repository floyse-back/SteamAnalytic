from app.infrastructure.celery_app.celery_app import app



@app.task(bind=True)
def news_task():
    pass