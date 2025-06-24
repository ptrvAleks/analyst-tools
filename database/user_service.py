from logic.user import User
from database.user_repository import UserRepository
from database.user_dto import UserDto
from typing import Optional, List

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, uid: str, email: str, first_name: Optional[str], role: str = "user") -> None:
        user_dto = UserDto(uid=uid, email=email, first_name=first_name, role=role)
        self.repo.create_user(user_dto)

    def delete_user_data(self, current_user: User, target_uid: str) -> bool:
        if not current_user.is_admin():
            return False  # Только админ может удалять

        dto = UserDto(uid=target_uid)
        return self.repo.delete_user_data(dto)

    def get_user_conversions(self, user: User):
        return self.repo.get_conversions(user.to_dto())

    def save_conversion(self, user: User, result: str):
        self.repo.save_conversion(user.to_dto(), result)

    def get_all_users(self) -> List[User]:
        user_dtos: List[UserDto] = self.repo.get_all_users()
        return [User(dto) for dto in user_dtos]

    def set_user_first_name(self, user: User, new_name: str) -> None:
        user.first_name = new_name
        self.repo.set_user_first_name(user.to_dto())

    def set_user_role(self, user: User, new_role: str) -> None:
        user.role = new_role
        self.repo.set_user_role(user.to_dto())

    def update_user_email(self, user: User, new_email: str) -> None:
        user.email = new_email
        self.repo.update_user_email(user.to_dto(), new_email)

    def delete_user(self, user: User) -> bool:
        dto = user.to_dto()
        return self.repo.delete_user(dto)