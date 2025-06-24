import pyrebase
import streamlit as st
from database.user_repository import UserRepository
from database.user_dto import UserDto
from streamlit_cookies_manager import EncryptedCookieManager
from cookie_firebase_uid import set_uid_cookie
from typing import Optional
from config import get_firebase_config, get_environment
import firebase_admin
from firebase_admin import get_app, credentials
from logic.user import User


class AuthManager:
    """Единая точка управления аутентификацией, сессией и ролями."""

    def __init__(self, cookie_password: str):
        self.cookies = EncryptedCookieManager(password=cookie_password)
        if not self.cookies.ready():
            self.cookies.save()
            st.stop()

        env = get_environment()
        try:
            get_app()  # Если уже инициализировано — ничего не делаем
        except ValueError:
            # Firebase Admin: только если ещё не был инициализирован
            try:
                firebase_config = get_firebase_config(env)
            except Exception as e:
                st.error(f"Ошибка загрузки конфигурации Firebase для среды {env}: {e}")
                st.stop()

            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)

        # Firebase Web SDK (Pyrebase): инициализируем в любом случае
        try:
            firebase_config = get_firebase_config(env)  # второй вызов, на всякий случай
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
        if "role" not in st.session_state and self.is_authenticated:
            repo = UserRepository()
            st.session_state["role"] = repo.get_user_role(UserDto(uid=st.session_state["uid"]))
        return st.session_state.get("role")

    # ---- основные операции ----
    def login(self, email: str, pwd: str) -> bool:
        try:
            user_data = self.auth.sign_in_with_email_and_password(email, pwd)
            uid = user_data["localId"]
            repo = UserRepository()

            user_dto = UserDto(uid=uid, email=email)
            user_dto.first_name = repo.get_user_first_name(user_dto)
            user_dto.role = repo.get_user_role(user_dto)

            user = User(user_dto)  # Domain entity

            self._finalize_auth(user)
            return True
        except Exception as e:
            print("Login failed:", e)
            return False

    def register(self, reg_email: str, reg_pwd: str, reg_first_name: Optional[str] = None, role: str = "user") -> bool:
        try:
            user = self.auth.create_user_with_email_and_password(reg_email, reg_pwd)
            uid = user["localId"]
            user_dto = UserDto(uid=uid, email=reg_email, first_name=reg_first_name, role=role)
            UserRepository().create_user(user_dto)
            user = User(user_dto)
            self._finalize_auth(user)
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
        auth_status = self.cookies.get("auth") == "true"
        first_name = self.cookies.get("first_name")

        if auth_status and email and uid:
            user_dto = UserDto(uid=uid, email=email, role=role, first_name=first_name)
            user = User(user_dto)
            st.session_state.update({
                "authenticated": True,
                "user": user
            })
        else:
            st.session_state["authenticated"] = False


    def _finalize_auth(self, user: User) -> None:
        dto = user.to_dto()
        st.session_state.update({
            "authenticated": True,
            "username": dto.email,
            "uid": dto.uid,
            "role": dto.role,
            "user": user,
            "name": dto.first_name,
        })

        self.cookies["username"] = dto.email
        self.cookies["uid"] = dto.uid
        self.cookies["auth"] = "true"
        self.cookies["role"] = dto.role
        if dto.first_name:
            self.cookies["first_name"] = dto.first_name
        self.cookies.save()

        set_uid_cookie(dto.uid)
        st.rerun()

    @property
    def user(self) -> "User | None":
        return st.session_state.get("user")