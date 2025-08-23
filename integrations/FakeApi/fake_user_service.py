# fake_user_service.py
from integrations.FakeApi.i_fake_user_repository import IFakeUserRepository
from integrations.FakeApi.fake_user_dto import FakeUserDto
from typing import List

class FakeUserService:
    def __init__(self, repo: IFakeUserRepository):
        self.repo = repo

    def get_fake_users(self, quantity: int = 1) -> List[FakeUserDto]:
        return self.repo.get_fake_users(quantity)