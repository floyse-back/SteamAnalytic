


class AnaliticGameForYou:
    def __init__(self,data:list):
        self.data = data

    def filter_data(self):
        return self.data.sort(key=lambda x:x['playtime_forever'])
