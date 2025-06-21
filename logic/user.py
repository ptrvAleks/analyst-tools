from pydantic import BaseModel
from typing import Literal, Optional
from firebase_admin import firestore
from database.db import db

class User(BaseModel):
    email: str
    first_name: Optional[str] = None
    role: Literal['user', 'admin'] = 'user'
    uid: str

    def is_admin(self) -> bool:
        return self.role == 'admin'

    @staticmethod
    def get_user_first_name(uid: str):
        first_name = firestore.client().collection("users").document(uid).get()
        if first_name.exists:
            return first_name.to_dict().get("first_name")
        return None

    @staticmethod
    def set_user_first_name(uid: str, first_name: str):
        if first_name:
            db.collection("users").document(uid).set(
                {"first_name": first_name},
                merge=True
            )
