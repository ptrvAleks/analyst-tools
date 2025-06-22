from pydantic import BaseModel
from typing import Literal, Optional, List
from firebase_admin import firestore, auth
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

    @staticmethod
    def set_user_role(uid: str, role: Optional[str] = "user"):
        role_to_set = role if role else "user"
        db.collection("users").document(uid).set({"role": role_to_set}, merge=True)

    @classmethod
    def get_all_users(cls) -> List["User"]:
        users = []
        page = auth.list_users()
        while page:
            for user_record in page.users:
                uid = user_record.uid
                email = user_record.email or ""
                # Получаем доп. данные из Firestore
                doc = db.collection("users").document(uid).get()
                extra = doc.to_dict() if doc.exists else {}
                users.append(
                    cls(
                        uid=uid,
                        email=email,
                        first_name=extra.get("first_name"),
                        role=extra.get("role", "user")
                    )
                )
            page = page.get_next_page()
        return users

    @staticmethod
    def delete_user(uid: str) -> bool:
        try:
            auth.delete_user(uid)
            print(f"Пользователь с uid={uid} удалён из Firebase Auth")
            return True
        except Exception as e:
            print(f"Ошибка удаления пользователя из Firebase Auth: {e}")
            return False

    def update_user_email(uid: str, new_email: str) -> bool:
        try:
            auth.update_user(uid, email=new_email)
            print(f"Email пользователя {uid} изменён на {new_email}")
            return True
        except Exception as e:
            print(f"Ошибка при обновлении email: {e}")
            return False