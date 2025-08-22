from abc import ABC, abstractmethod
from typing import List
from integrations.FakeApi.fake_user_dto import FakeUserDto

class IFakeUserRepository(ABC):
    @abstractmethod
    def get_fake_users(self, quantity: int = 1) -> List[FakeUserDto]:
        pass