from pydantic import BaseModel, Field


class SteamUser(BaseModel):
    user_data: dict = Field(default=dict())
    user_friends_list: dict = Field(default=dict())
    user_badges: dict = Field(default=dict())
    user_games: dict = Field(default=dict())


"""class SteamUser_DTO():
    @staticmethod
    def transform_to_dict(user:SteamUser):
        new_user = dict()
        new_user["user_data"] = user.user_data
        new_user["user_friends"] = user.user_friends
        new_user["user_badges"] = user.user_badges
        new_user["user_games"] = user.user_games
        return new_user
    """