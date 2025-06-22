import pyrebase
import streamlit as st
from database.db_methods import get_user_role
from streamlit_cookies_manager import EncryptedCookieManager
from cookie_firebase_uid import set_uid_cookie
from logic.user import User
from typing import Optional
from config import get_firebase_config, get_environment


class AuthManager:
    """Единая точка управления аутентификацией, сессией и ролями."""

    def __init__(self, cookie_password: str):
        self.cookies = EncryptedCookieManager(password=cookie_password)
        if not self.cookies.ready():
            self.cookies.save()
            st.stop()

        env = get_environment()

        try:
            firebase_config = get_firebase_config(env)
        except Exception as e:
            st.error(f"Ошибка загрузки конфигурации Firebase для среды {env}: {e}")
            st.stop()

        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()

        self._restore_session()

    # ---------------------- public API ----------------------
    @property
    def is_authenticated(self) -> bool:
        return st.session_state.get("authenticated", False)

    @property
    def role(self):
        """Ленивая загрузка роли из БД (кешируется в session_state)."""
        if "role" not in st.session_state and self.is_authenticated:
            st.session_state["role"] = get_user_role(st.session_state["uid"])
        return st.session_state.get("role")

    # ---- основные операции ----
    def login(self, email: str, pwd: str) -> bool:
        try:
            user = self.auth.sign_in_with_email_and_password(email, pwd)
            uid = user["localId"]
            self._finalize_auth(email, uid)
            return True
        except Exception as e:
            print("Login failed:", e)
            return False

    def register(self, reg_email: str, reg_pwd: str, reg_first_name: Optional[str] = None) -> bool:
        try:
            user = self.auth.create_user_with_email_and_password(reg_email, reg_pwd)
            uid = user["localId"]
            if reg_first_name:
                User.set_user_first_name(uid, reg_first_name)
            self._finalize_auth(reg_email, uid, reg_first_name)
            return True
        except Exception as e:
            print("Registration failed:", e)
            return False

    def logout(self):
        """Полный выход: очищаем session_state и куки, делаем rerun."""
        for key in ("authenticated", "username", "uid", "role", "first_name", "user", "login_submitted", "register_submitted"):
            st.session_state.pop(key, None)

        for key in ("username", "auth", "uid", "role", "first_name"):
            self.cookies[key] = ""
        self.cookies.save()
        st.rerun()

    # ---------------------- internal helpers ----------------------
    def _restore_session(self):
        email = self.cookies.get("username")
        uid = self.cookies.get("uid")
        role = self.cookies.get("role") or "user"
        auth = self.cookies.get("auth") == "true"
        first_name = self.cookies.get("first_name")

        if auth and email and uid:
            user = User(email=email, uid=uid, role=role, first_name=first_name)
            st.session_state.update({
                "authenticated": True,
                "user": user,  # ← объект снова в сессии
            })
        else:
            st.session_state["authenticated"] = False

    def _finalize_auth(
            self,
            email: str,
            uid: str,
            first_name: Optional[str] = None,
    ) -> None:
        """Общая логика для login / register."""
        # 1. Роль всегда либо 'user', либо 'admin'
        role = get_user_role(uid) or "user"

        # 2. Если имя не передали (логин) — пробуем достать из Firestore
        if first_name is None:
            first_name = User.get_user_first_name(uid)

        # 3. Создаём объект пользователя
        user = User(email=email, uid=uid, role=role, first_name=first_name)

        # 4. Обновляем session_state
        st.session_state.update(
            {
                "authenticated": True,
                "username": email,
                "uid": uid,
                "role": role,
                "user": user,
                "name": first_name,
            }
        )

        # 5. Куки (используем единый ключ 'name')
        self.cookies["username"] = email
        self.cookies["uid"] = uid
        self.cookies["auth"] = "true"
        self.cookies["role"] = role
        if first_name:
            self.cookies["first_name"] = first_name
        self.cookies.save()

        set_uid_cookie(uid)
        st.rerun()

    @property
    def user(self) -> "User | None":
        return st.session_state.get("user")