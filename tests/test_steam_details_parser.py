from app.infrastructure.celery_app.database import get_db
from app.infrastructure.celery_app.utils.steam_details_parser import SteamDetailsParser


class TestSteamDetailsParser:
    def test_steam_paser_details(self):
        session = next(get_db())
        parser = SteamDetailsParser(session)
        parser.parse(game_list_appid=[3298170,1174180,1946700,3149980,730,387990])

