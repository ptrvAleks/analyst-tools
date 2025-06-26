# shared/session/cookie_session.py

from streamlit_cookies_manager import EncryptedCookieManager
from database.user_dto import UserDto

class CookieSessionManager:
    def __init__(self, password: str):
        self._cookies = EncryptedCookieManager(password=password)

    def ready(self) -> bool:
        return self._cookies.ready()

    def save(self):
        self._cookies.save()

    def get(self, key: str):
        return self._cookies.get(key)

    def save_user(self, user: UserDto):
        self._cookies["username"] = user.email
        self._cookies["uid"] = user.uid
        self._cookies["auth"] = "true"
        self._cookies["role"] = user.role
        if user.first_name:
            self._cookies["first_name"] = user.first_name
        self._cookies.save()

    def set_value(self, key: str, value: str):
        self._cookies[key] = value  # внутреннее хранилище
        self.save()

    def get_value(self, key: str, default=None):
        return self._cookies.get(key, default)


    def clear(self):
        for key in ("username", "auth", "uid", "role", "first_name"):
            self._cookies[key] = ""
        self._cookies.save()

    def restore(self) -> dict:
        return {
            "uid": self._cookies.get("uid"),
            "email": self._cookies.get("username"),
            "role": self._cookies.get("role"),
            "auth": self._cookies.get("auth") == "true",
            "first_name": self._cookies.get("first_name")
        }