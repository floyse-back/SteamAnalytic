from app.infrastructure.steam_api.client import SteamClient

red_flug_descriptors_ids = [3,4]
yellow_flug_descriptors_ids = [1,2,5]
tags_blocked_list = [
    {
        "count":1,
        "tag":"hentai"
    },
    {
        "count":0.5,
        "tag":"sexual content"
    },
    {
        "count":1,
        "tag":"nsfw"
    },
    {
        "count":0.5,
        "tag":"mature"
    },
    {
        "count":0.5,
        "tag":"nudity"
    }
]
tags_checked = [
    "казуальні ігри","рольові ігри","симулятори","пригоди","інді"
]


def ganre_check(ganres:list[dict]):
    """
    1 можливо треба перевірити
    0 не перевіряємо мало ймовірно
    """
    answer = 0
    for ganre in ganres:
        if ganre['description'].lower() in tags_checked:
            print(ganre['description'])
            answer += 1
    return 1 if answer >= 2 else 0


def tags_check(data:dict)->bool:
    tags = SteamClient.get_popular_tags(appid=data.get("steam_appid", 0))
    count_blocked = 0
    for tag in tags_blocked_list:
        if tag['tag'] in tags:
            count_blocked += tag['count']
            if count_blocked >= 1:
                return False
    return True

def filter_nfsm_content(data: dict) -> bool:
    content_descriptors = data.get("content_descriptors", {})
    block_red = 0
    block_yellow = 0

    for i in content_descriptors.get("ids", []):
        if i in red_flug_descriptors_ids:
            return False
        elif i in yellow_flug_descriptors_ids:
            block_yellow += 1

    if block_red >= 1:
        return False
    block_yellow += ganre_check(ganres=data.get("genres",[]))

    if block_yellow >= 1:
        if not tags_check(data):
            return False


    return True

