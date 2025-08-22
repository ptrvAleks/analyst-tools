from logic.user import User
from repository_provider import get_user_repository
from database.i_user_repository import IUserRepository
from database.user_dto import UserDto
from typing import Optional, List, Dict, Any
import json

class UserService:
    def __init__(self, repo: Optional[IUserRepository] = None):
        self.repo = repo or get_user_repository()

    def register_user(self, uid: str, email: str, first_name: Optional[str], role: str = "user") -> None:
        user_dto = UserDto(uid=uid, email=email, first_name=first_name, role=role)
        self.repo.create_user(user_dto)

    def delete_user_data(self, current_user_dto: UserDto, target_uid: str) -> bool:
        current_user = User(current_user_dto)
        if not current_user.is_admin():
            return False
        dto = UserDto(uid=target_uid)
        return self.repo.delete_user_data(dto)

    def get_user_conversions(self, user_dto: UserDto) -> List[Dict[str, Any]]:
        return self.repo.get_conversions(user_dto)

    def save_conversion(self, user_dto: UserDto, result: str):
        self.repo.save_conversion(user_dto, result)

    def get_all_users(self) -> List[UserDto]:
        return self.repo.get_all_users()

    def set_user_first_name(self, user_dto: UserDto, new_name: str) -> None:
        user = User(user_dto)
        user.update_first_name(new_name)
        self.repo.set_user_first_name(user.to_dto())

    def set_user_role(self, user_dto: UserDto, new_role: str) -> None:
        user = User(user_dto)
        user.update_role(new_role)
        self.repo.set_user_role(user.to_dto())

    def update_user_email(self, user_dto: UserDto, new_email: str) -> None:
        user = User(user_dto)
        user.update_email(new_email)
        self.repo.update_user_email(user.to_dto(), new_email)

    def delete_user(self, user_dto: UserDto) -> bool:
        return self.repo.delete_user(user_dto)

    def get_conversions(self, user_dto: UserDto) -> List[Dict[str, Any]]:
        return self.repo.get_conversions(user_dto)

    def delete_conversion(self, user_dto: UserDto, document_id: str) -> bool:
        return self.repo.delete_conversion(user_dto, document_id)
    
    def save_template(self, user_dto: UserDto, result: str):
        self.repo.save_template(user_dto, result)
        
    def get_templates(self, user_dto: UserDto) -> List[Dict[str, Any]]:
        raw_templates = self.repo.get_templates(user_dto)
        templates: List[Dict[str, Any]] = []

        for item in raw_templates:
            template_str = item.get("template")
            template_dict = {}
            if isinstance(template_str, str):
                try:
                    template_dict = json.loads(template_str)
                except json.JSONDecodeError:
                    template_dict = {"_raw": template_str}  # fallback

            templates.append({
                "id": item.get("id"),
                "template": json.dumps(template_dict, ensure_ascii=False, indent=4),
                "timestamp": item.get("timestamp")
            })

        return templates