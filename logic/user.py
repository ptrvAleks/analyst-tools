from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class User(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    role: Literal['user', 'admin'] = 'user'
    uid: str

    def is_admin(self) -> bool:
        return self.role == 'admin'

