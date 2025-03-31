from .user_rating import UserRating

class AnaliticService:
    def __init__(self):
        self.user_rating = UserRating()

    def analitic_user_rating(self,data:dict):
        return self.user_rating.create_user_rating(data=data)