from abc import ABC, abstractmethod

class MemoryInterface(ABC):
    @abstractmethod
    def store(self, key: str, data: str):
        pass

    @abstractmethod
    def retrieve(self, key: str) -> str:
        pass

    @abstractmethod
    def search(self, query: str, top_k: int = 3) -> list:
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def list_keys(self) -> list:
        pass
