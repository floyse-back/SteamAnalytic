from app.infrastructure.celery_app.utils.steam_release_parser import SteamGamesParser
from tests.conftest import tests_logger as logger


def test_steam_release_parser(session_sync):
    steam_release_parser = SteamGamesParser(logger=logger,url="https://store.steampowered.com/search/?maxprice=free&specials=1&ndl=1")
    result = steam_release_parser.execute()
    logger.info(result)
    assert result is not None