import requests
from typing import List
from integrations.i_fake_user_repository import IFakeUserRepository
from integrations.fake_user_dto import FakeUserDto

class FakerUserRepository(IFakeUserRepository):
    def get_fake_users(self, quantity: int = 1) -> List[FakeUserDto]:
        url = f"https://fakerapi.it/api/v1/persons?_quantity={quantity}"
        response = requests.get(url)

        if response.status_code != 200:
            return []

        return response.json().get("data", [])

# users = get_fake_users(3)
# print(users)
# print(users[0]['lastname'])