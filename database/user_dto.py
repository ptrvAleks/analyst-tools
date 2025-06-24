class UserDto:
    def __init__(self, uid: str, email: str = None, first_name: str = None, role: str = None):
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
        return cls(
            uid=uid,
            email=data.get("email"),
            first_name=data.get("first_name"),
            role=data.get("role")
        )