from typing import Optional, Union, List

from app.application.dto.steam_dto import transform_to_dto, Game, GameShortModel, GanresOut


class GetFreeTransformUseCase:

    async def execute(self,data:Optional[Union[List,dict]]=None,game_id:int=None):
        if data is None or len(data) == 0:
            return None
        else:
            if data[f"{game_id}"]["success"] == True:
                game_short_model = self.__corected_game_short_model(data[f"{game_id}"]["data"])
            else:
                return None
            return game_short_model

    def __corected_game_short_model(self,data:Optional[dict])->GameShortModel:
        if data is None:
            return False

        game_short_model = GameShortModel(
            name=data.get("name","Steam Game"),
            steam_appid = int(data.get("steam_appid")),
            final_formatted_price = data.get("price_overview",{"final_formatted":"Free"}).get("final_formatted","0"),
            discount = int(data.get("price_overview",{"discount_percent":0}).get("discount_percent",0)),
            short_description=data.get("short_description","text"),
            url = data.get(f"capsule_image"),

            game_ganre=[GanresOut(ganres_id=int(i.get('id')),ganres_name=i.get("description")) for i in data.get("genres",[])],
        )

        return game_short_model