from abc import ABC,abstractmethod


class ICacheRepository(ABC):
    @abstractmethod
    def cache_data(self,key:str,data,expire:int = 3600):
        pass

    @abstractmethod
    def get_data(self,key):
        pass

    @abstractmethod
    def delete_data(self,key):
        pass
