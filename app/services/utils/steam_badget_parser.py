import requests
from bs4 import BeautifulSoup
# from ...config import STEAMDB_URL

STEAMDB_URL = "https://www.steamcardexchange.net/index.php?gamepage-appid-753"

class SteamBadgetParser:
    def __init__(self):
        self.url = STEAMDB_URL
        self.all_data = []

    def parse(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

        else:
             print(f"Error: {response.status_code}")


test = SteamBadgetParser()
test.parse()