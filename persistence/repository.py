from abc import ABC, abstractmethod
from domain.user import User

class UserRepository(ABC):

    @abstractmethod
    async def list(self) -> list[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> None:
        pass
