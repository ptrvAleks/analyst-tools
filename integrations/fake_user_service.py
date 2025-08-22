# fake_user_service.py
from integrations.i_fake_user_repository import IFakeUserRepository
from integrations.fake_user_dto import FakeUserDto

class FakeUserService:
    def __init__(self, repo: IFakeUserRepository):
        self.repo = repo

    def get_fake_users(self, quantity: int = 1) -> list[FakeUserDto]:
        raw_users = self.repo.get_fake_users(quantity)
        return [
            FakeUserDto(firstname=u.firstname, lastname=u.lastname)
            for u in raw_users
        ]