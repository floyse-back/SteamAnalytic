from sqlalchemy import select

from app.infrastructure.celery_app.utils.steam_details_parser import SteamDetailsParser
import pytest

from app.infrastructure.db.models.steam_models import BlockedGames, SafeGames


class TestSteamDetailsParser:
    @pytest.mark.parametrize(
        "appids",[
        ([3298170,2658660,3424900]),
        ([3149980,1227890])
        ]
    )
    def test_steam_parser_blocked_games_details(self,appids,session_sync):
        with session_sync() as session_sync:
            parser = SteamDetailsParser(session=session_sync)
            try:
                parser.parse(game_list_appid=appids)
                assert True
            except Exception as e:
                assert False
            stmt = select(BlockedGames.appid).filter(BlockedGames.appid.in_(appids))
            result = session_sync.execute(stmt)
            result = result.scalars().all()
            assert len(result) == len(appids)

    @pytest.mark.parametrize(
        "appids",[
            ([730,1174180,1946700,387990]),
            ([2050650,252490])
        ]
    )
    def test_steam_parser_safe_games(self,appids,session_sync):
        with session_sync() as session_sync:
            parser = SteamDetailsParser(session=session_sync)
            try:
                parser.parse(game_list_appid=appids)
                assert True
            except Exception as e:
                assert False
            stmt = select(SafeGames.appid).filter(SafeGames.appid.in_(appids))
            result = session_sync.execute(stmt)
            result = result.scalars().all()
            assert len(result) == len(appids)
