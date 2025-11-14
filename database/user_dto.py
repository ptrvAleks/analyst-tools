from typing import Optional

class UserDto:
    def __init__(self, uid: str, email: str, first_name: Optional[str] = None, role: str = "user"):
        self.uid = uid
        self.email = email
        self.first_name = first_name
        self.role = role

    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "first_name": self.first_name,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, uid: str, data: dict):
        email = data.get("email")
        role = data.get("role", "user")  # по умолчанию user
        if email is None:
            raise ValueError("Empty email")
        return cls(
            uid=uid,
            email=email,
            first_name=data.get("first_name"),
            role=role
        )