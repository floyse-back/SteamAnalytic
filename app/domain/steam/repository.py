from abc import ABC, abstractmethod

class ISteamRepository(ABC):
    @abstractmethod
    async def get_top_games(self):
        pass

    @abstractmethod
    async def get_most_discount_games(self):
        pass

class IAnaliticsRepository(ABC):
    @abstractmethod
    async def get_games_for_appids(self):
        pass

    @abstractmethod
    async def games_for_you(self):
        pass


