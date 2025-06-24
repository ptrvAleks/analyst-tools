# database/user_repository.py
from datetime import datetime, timedelta, timezone
from database.db import db
from google.cloud.firestore import Query
from typing import List, Optional
from firebase_admin import auth
from database.user_dto import UserDto

class UserRepository:
    MSK = timezone(timedelta(hours=3))

    def save_conversion(self, user: UserDto, result):
        db.collection("users").document(user.uid).collection("conversions").add({
            "converted": result,
            "timestamp": datetime.now(self.MSK)
        })

    def get_conversions(self, user: UserDto):
        docs = db.collection("users").document(user.uid).collection("conversions") \
            .order_by("timestamp", direction=Query.DESCENDING).stream()

        conversions = []
        for doc in docs:
            data = doc.to_dict()
            ts = data.get("timestamp")
            if ts and hasattr(ts, "to_datetime"):
                data["timestamp"] = ts.to_datetime()
            conversions.append({"id": doc.id, **data})
        return conversions

    def delete_conversion(self, user: UserDto, document_id):
        db.collection("users").document(user.uid).collection("conversions").document(document_id).delete()

    def delete_user_data(self, user: UserDto) -> bool:
        try:
            user_ref = db.collection("users").document(user.uid)
            conversions_ref = user_ref.collection("conversions").stream()

            for doc in conversions_ref:
                user_ref.collection("conversions").document(doc.id).delete()

            user_ref.delete()

            print(f"Данные пользователя {user.uid} успешно удалены")
            return True
        except Exception as e:
            print(f"Ошибка при удалении данных пользователя {user.uid}: {e}")
            return False

    def get_user_role(self, user: UserDto) -> str:
        doc = db.collection("users").document(user.uid).get()
        if doc.exists:
            return doc.to_dict().get("role", "user")
        return "user"

    def get_user_first_name(self, user: UserDto) -> Optional[str]:
        doc = db.collection("users").document(user.uid).get()
        if doc.exists:
            return doc.to_dict().get("first_name")
        return None

    def set_user_first_name(self, user: UserDto):
        if user.first_name:
            db.collection("users").document(user.uid).set({"first_name": user.first_name}, merge=True)

    def set_user_role(self, user: UserDto):
        role_to_set = user.role if user.role else "user"
        db.collection("users").document(user.uid).set({"role": role_to_set}, merge=True)

    def create_user(self, user: UserDto):
        db.collection("users").document(user.uid).set(user.to_dict(), merge=True)

    @classmethod
    def get_all_users(cls) -> List[UserDto]:
        users = []
        page = auth.list_users()
        while page:
            for user_record in page.users:
                uid = user_record.uid
                email = user_record.email or ""
                doc = db.collection("users").document(uid).get()
                extra = doc.to_dict() if doc.exists else {}
                users.append(UserDto(uid=uid, email=email, first_name=extra.get("first_name"), role=extra.get("role", "user")))
            page = page.get_next_page()
        return users

    def delete_user(self, user: UserDto) -> bool:
        try:
            auth.delete_user(user.uid)
            print(f"Пользователь с uid={user.uid} удалён из Firebase Auth")
            return True
        except Exception as e:
            print(f"Ошибка удаления пользователя из Firebase Auth: {e}")
            return False

    def update_user_email(self, user: UserDto, new_email: str) -> bool:
        try:
            auth.update_user(user.uid, email=new_email)
            print(f"Email пользователя {user.uid} изменён на {new_email}")
            return True
        except Exception as e:
            print(f"Ошибка при обновлении email: {e}")
            return False