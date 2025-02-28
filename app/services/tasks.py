from .celery_app import app

from .database import get_db
from ..database.models import SteamBase
from .utils.SteamParser import SteamParser

@app.task
def update_steam_games():
    print("Start task update_steam_games!")
    session = next(get_db())

    parser = SteamParser()
    generator_data = parser.page_parse()

    session.query(SteamBase).delete()
    for data in generator_data:
        session.bulk_save_objects(data)
        session.flush()

    session.commit()
    return "Finished task update_steam_games!"
