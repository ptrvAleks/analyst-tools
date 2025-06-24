# logic/user.py
from database.user_dto import UserDto

class User:
    def __init__(self, dto: UserDto):
        self._dto = dto

    @property
    def uid(self) -> str:
        return self._dto.uid

    @property
    def email(self) -> str:
        return self._dto.email

    @email.setter
    def email(self, value: str) -> None:
        self._dto.email = value

    @property
    def first_name(self) -> str:
        return self._dto.first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        self._dto.first_name = value

    @property
    def role(self) -> str:
        return self._dto.role

    @role.setter
    def role(self, value: str) -> None:
        self._dto.role = value

    def is_admin(self) -> bool:
        return self.role == "admin"

    def to_dto(self) -> UserDto:
        return self._dto