import pyrebase
import streamlit as st
from pydantic import EmailStr

from database.db_methods import get_user_role
from streamlit_cookies_manager import EncryptedCookieManager
from cookie_firebase_uid import set_uid_cookie
from logic.user import User


class AuthManager:
    """Единая точка управления аутентификацией, сессией и ролями."""


    def __init__(self, cookie_password: str):
        # Инициализируем и проверяем CookieManager
        self.cookies = EncryptedCookieManager(password=cookie_password)
        if not self.cookies.ready():
            self.cookies.save()  # создаём пустые
            st.stop()
        # Инициализация Firebase
        self.firebase = pyrebase.initialize_app(dict(st.secrets["firebaseConfig"]))
        self.auth = self.firebase.auth()

        if not self.cookies.ready():
            st.stop()

        # Восстанавливаем сессию (если куки валидны)
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

    def register(self, reg_email: str, reg_pwd: str) -> bool:
        try:
            user = self.auth.create_user_with_email_and_password(reg_email, reg_pwd)
            uid = user["localId"]
            self._finalize_auth(reg_email, uid)
            return True
        except Exception as e:
            print("Registration failed:", e)
            return False

    def logout(self):
        """Полный выход: очищаем session_state и куки, делаем rerun."""
        for key in ("authenticated", "username", "uid", "role"):
            st.session_state.pop(key, None)

        for key in ("username", "auth", "uid", "role"):
            self.cookies[key] = ""
        self.cookies.save()
        st.rerun()

    # ---------------------- internal helpers ----------------------
    def _restore_session(self):
        email = self.cookies.get("username")
        uid = self.cookies.get("uid")
        role = self.cookies.get("role") or "user"
        auth = self.cookies.get("auth") == "true"

        if auth and email and uid:
            user = User(email=email, uid=uid, role=role)
            st.session_state.update({
                "authenticated": True,
                "user": user,  # ← объект снова в сессии
            })
        else:
            st.session_state["authenticated"] = False

    def _finalize_auth(self, email: str, uid: str):
        """Общая логика для login / register."""
        role = get_user_role(uid)
        user = User(email=email, uid=uid, role=role)

        # Сохраняем в session_state
        st.session_state.update({
            "authenticated": True,
            "username": email,
            "uid": uid,
            "role": role,
            "user": user
        })

        # Устанавливаем cookie
        self.cookies["username"] = email
        self.cookies["uid"] = uid
        self.cookies["auth"] = "true"
        self.cookies["role"] = role
        self.cookies.save()

        set_uid_cookie(uid)
        st.rerun()

    @property
    def user(self) -> "User | None":
        return st.session_state.get("user")