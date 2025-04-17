from app.application.dto.steam_dto import SteamUser
from app.application.steam_analitic.user_rating import UserRating


class UsersBattle:
    def __init__(self):
        self.user_rating = UserRating()

    """Порівняння 2 профілів"""
    async def users_battle(self, user1_data: SteamUser, user2_data: SteamUser):
        data = dict()

        print(user1_data,type(user1_data))
        self.user1_id = user1_data.user_data["player"].get("steamid")
        self.user2_id = user2_data.user_data["player"].get("steamid")

        # Перевірка на наявність steamid (базова інформація)
        if not self.user1_id or not self.user2_id:
            return data  # Немає ID - не можемо порівнювати

        # user_data
        player1 = user1_data.user_data.get("player")
        player2 = user2_data.user_data.get("player")

        if player1 and player2:
            self.generate_dict_element(
                data=data,
                title="community_visibility_state",
                user1_element=player1.get("communityvisibilitystate"),
                user2_element=player2.get("communityvisibilitystate"),
            )
            self.generate_dict_element(
                data=data,
                title="profilestate",
                user1_element=player1.get("profilestate"),
                user2_element=player2.get("profilestate"),
            )
            self.generate_dict_element(
                data=data,
                title="commentpermission",
                user1_element=player1.get("commentpermission"),
                user2_element=player2.get("commentpermission"),
            )
            self.generate_dict_element(
                data=data,
                title="personastate",
                user1_element=player1.get("personastate"),
                user2_element=player2.get("personastate"),
            )
            self.generate_dict_element(
                data=data,
                title="timecreated",
                user1_element=player1.get("timecreated"),
                user2_element=player2.get("timecreated"),
            )
            self.generate_dict_element(
                data=data,
                title="personastateflags",
                user1_element=player1.get("personastateflags"),
                user2_element=player2.get("personastateflags"),
            )
            self.generate_dict_element(
                data=data,
                title="loccountrycode",
                user1_element=player1.get("loccountrycode"),
                user2_element=player2.get("loccountrycode"),
            )
            self.generate_dict_element(
                data=data,
                title="locstatecode",
                user1_element=player1.get("locstatecode"),
                user2_element=player2.get("locstatecode"),
            )
            self.generate_dict_element(
                data=data,
                title="loccityid",
                user1_element=player1.get("loccityid"),
                user2_element=player2.get("loccityid"),
            )

        # user_badges
        badges1 = user1_data.user_badges
        badges2 = user2_data.user_badges

        if badges1 and badges2:
            self.generate_dict_element(
                data=data,
                title="player_level",
                user1_element=badges1.get("player_level"),
                user2_element=badges2.get("player_level"),
            )
            self.generate_dict_element(
                data=data,
                title="player_xp",
                user1_element=badges1.get("player_xp"),
                user2_element=badges2.get("player_xp"),
            )
            self.generate_dict_element(
                data=data,
                title="badge_count",
                user1_element=len(badges1.get("badges", [])),
                user2_element=len(badges2.get("badges", [])),
            )
            total_xp_user1_badges = sum(badge.get("xp", 0) for badge in badges1.get("badges", []))
            total_xp_user2_badges = sum(badge.get("xp", 0) for badge in badges2.get("badges", []))
            self.generate_dict_element(
                data=data,
                title="total_badges_xp",
                user1_element=total_xp_user1_badges,
                user2_element=total_xp_user2_badges,
            )

        # user_games
        games1 = user1_data.user_games
        games2 = user2_data.user_games

        if games1 and games2:
            self.generate_dict_element(
                data=data,
                title="game_count",
                user1_element=games1.get("game_count"),
                user2_element=games2.get("game_count"),
            )
            total_playtime_user1 = sum(game.get("playtime_forever", 0) for game in games1.get("games", []))
            total_playtime_user2 = sum(game.get("playtime_forever", 0) for game in games2.get("games", []))
            self.generate_dict_element(
                data=data,
                title="total_playtime",
                user1_element=total_playtime_user1,
                user2_element=total_playtime_user2,
            )

        user1_rating = await self.user_rating.create_user_rating(user1_data)
        user2_rating = await self.user_rating.create_user_rating(user2_data)
        self.generate_dict_element(
            data=data,
            title="total_rating",
            user1_element=user1_rating,
            user2_element=user2_rating,
        )

        return data

    def generate_dict_element(self, data: dict, title: str, user1_element: any, user2_element: any):
        difference = None
        winner = None

        if isinstance(user1_element, (int, float)) and isinstance(user2_element, (
        int, float)) and user1_element is not None and user2_element is not None:
            difference = abs(user1_element - user2_element)
            if user1_element > user2_element:
                winner = self.user1_id
            elif user2_element > user1_element:
                winner = self.user2_id
            else:
                winner = "draw"  # Або None, або інше позначення нічиєї

        data[f"{title}"] = {
            f"{self.user1_id}": user1_element,
            f"{self.user2_id}": user2_element,
            f"": difference,
            "winner": winner,
        }
        return data