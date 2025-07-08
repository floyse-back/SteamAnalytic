import random

from app.infrastructure.celery_app.tasks.steam_tasks import update_game_icon_url,send_email

class TestCeleryTasks:
    def test_create_very_big_tasks(self):
        update_game_icon_url.delay()
        for _ in range(10):
            r_n = random.randint(100000,999999)
            send_email.delay("floyse.fake@gmail.com",r_n,"delete_user")



