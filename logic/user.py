# logic/user.py
from database.user_dto import UserDto

class User:
    def __init__(self, dto: UserDto):
        self._dto = dto

    def is_admin(self) -> bool:
        return self._dto.role == "admin"

    def to_dto(self) -> UserDto:
        return self._dto

    def update_email(self, new_email: str):
        self._dto.email = new_email

    def update_first_name(self, new_name: str):
        self._dto.first_name = new_name

    def update_role(self, new_role: str):
        self._dto.role = new_role