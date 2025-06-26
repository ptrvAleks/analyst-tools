import pyrebase
import streamlit as st
from repository_provider import get_user_repository
from database.user_dto import UserDto
from shared.session.cookie_session import CookieSessionManager
from authentication.cookie_firebase_uid import set_uid_cookie
from typing import Optional
from database.config import get_firebase_config, get_environment
import firebase_admin
from firebase_admin import get_app, credentials


class AuthManager:
    """Единая точка управления аутентификацией, сессией и ролями."""

    def __init__(self, cookie_manager: CookieSessionManager):
        self.cookies = cookie_manager
        if not self.cookies.ready():
            self.cookies.save()
            st.stop()

        env = get_environment()
        try:
            get_app()
        except ValueError:
            try:
                firebase_config = get_firebase_config(env)
            except Exception as e:
                st.error(f"Ошибка загрузки конфигурации Firebase для среды {env}: {e}")
                st.stop()

            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)

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
        if "role" not in st.session_state and self.is_authenticated:
            repo = get_user_repository()
            st.session_state["role"] = repo.get_user_role(UserDto(uid=st.session_state["uid"]))
        return st.session_state.get("role")

    def login(self, email: str, pwd: str) -> bool:
        try:
            user_data = self.auth.sign_in_with_email_and_password(email, pwd)
            uid = user_data.get("localId")
            if not uid:
                st.error("UID не найден в ответе Firebase.")
                return False

            repo = get_user_repository()
            user_dto = UserDto(uid=uid, email=email)
            user_dto.first_name = repo.get_user_first_name(user_dto)
            user_dto.role = repo.get_user_role(user_dto)

            self._finalize_auth(user_dto)
            return True
        except Exception as e:
            st.error(f"Ошибка при входе: {e}")
            return False

    def register(self, reg_email: str, reg_pwd: str, reg_first_name: Optional[str] = None, role: str = "user") -> bool:
        try:
            user = self.auth.create_user_with_email_and_password(reg_email, reg_pwd)
            uid = user["localId"]
            user_dto = UserDto(uid=uid, email=reg_email, first_name=reg_first_name, role=role)
            get_user_repository().create_user(user_dto)
            self._finalize_auth(user_dto)
            return True
        except Exception as e:
            print("Registration failed:", e)
            return False

    def logout(self):
        """Полный выход: очищаем session_state и куки, делаем rerun."""
        for key in ("authenticated", "username", "uid", "role", "first_name", "user", "login_submitted", "register_submitted"):
            st.session_state.pop(key, None)

        self.cookies.clear()
        st.rerun()

    # ---------------------- internal helpers ----------------------
    def _restore_session(self):
        data = self.cookies.restore()

        if data["auth"] and data["email"] and data["uid"]:
            user_dto = UserDto(
                uid=data["uid"],
                email=data["email"],
                role=data["role"] or "user",
                first_name=data["first_name"]
            )
            st.session_state.update({
                "authenticated": True,
                "user": user_dto,
                "role": data["role"],
                "first_name": data["first_name"],
                "uid": data["uid"]
            })
        else:
            st.session_state["authenticated"] = False

    def _finalize_auth(self, dto: UserDto) -> None:
        st.session_state.update({
            "authenticated": True,
            "username": dto.email,
            "uid": dto.uid,
            "role": dto.role,
            "user": dto,
            "name": dto.first_name,
        })

        self.cookies.save_user(dto)
        set_uid_cookie(dto.uid)
        st.rerun()

    @property
    def user(self) -> Optional[UserDto]:
        return st.session_state.get("user")