from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from database.user_dto import UserDto

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserDto) -> None: pass

    @abstractmethod
    def delete_user_data(self, user: UserDto) -> bool: pass

    @abstractmethod
    def get_conversions(self, user: UserDto) -> List[Dict[str, Any]]: pass

    @abstractmethod
    def save_conversion(self, user: UserDto, result: str) -> None: pass

    @abstractmethod
    def get_all_users(self) -> List[UserDto]: pass

    @abstractmethod
    def set_user_first_name(self, user: UserDto) -> None: pass

    @abstractmethod
    def set_user_role(self, user: UserDto) -> None: pass

    @abstractmethod
    def update_user_email(self, user: UserDto, new_email: str) -> bool: pass

    @abstractmethod
    def delete_user(self, user: UserDto) -> bool: pass

    @abstractmethod
    def delete_conversion(self, user: UserDto, document_id: str) -> bool: pass

    @abstractmethod
    def get_user_role(self, user: UserDto) -> str: pass 

    @abstractmethod
    def get_user_first_name(self, user: UserDto) -> Optional[str]: pass