from .celery_app import app

from .database import get_db
from ..database.models import SteamBase,HistoricalSteamBase
from .utils.steam_parser import SteamParser
from sqlalchemy import text

@app.task
def update_steam_games():
    print("Start task update_steam_games!")
    session = next(get_db())

    parser = SteamParser()
    generator_data = parser.page_parse()

    session.execute(text("""
        INSERT INTO historysteambase (data)
        SELECT to_jsonb(array_agg(steambase.*))
        FROM steambase;
        """))
    session.query(SteamBase).delete()

    for data in generator_data:
       session.bulk_save_objects(data)
       session.flush()

    session.commit()
    return "Finished task update_steam_games!"

@app.task
def update_game_details():
    session = next(get_db())
