from typing import Optional
from pydantic import BaseModel

class UserDto(BaseModel):
    uid: str
    email: str
    first_name: Optional[str] = None
    role: str = "user"

    def to_dict(self):
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict):
        if "email" not in data or data["email"] is None:
            raise ValueError("Empty email")
        return cls(**data)
