import pyrebase
import streamlit as st
from database.db_methods import get_user_role
from streamlit_cookies_manager import EncryptedCookieManager
from cookie_firebase_uid import set_uid_cookie



class AuthManager:
    """Единая точка управления аутентификацией, сессией и ролями."""
    # Инициализация Firebase


    def __init__(self, cookie_password: str):
        # Инициализируем и проверяем CookieManager
        self.cookies = EncryptedCookieManager(password=cookie_password)
        if not self.cookies.ready():
            self.cookies.save()  # создаём пустые
            st.stop()
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
        username = self.cookies.get("username")
        auth_flag = self.cookies.get("auth")
        uid = self.cookies.get("uid")

        if auth_flag == "true" and username and uid:
            st.session_state.update({
                "authenticated": True,
                "username": username,
                "uid": uid,
            })
        else:
            st.session_state["authenticated"] = False

    def _finalize_auth(self, email: str, uid: str):
        """Общая логика для login / register."""
        st.session_state.update({
            "authenticated": True,
            "username": email,
            "uid": uid,
        })
        set_uid_cookie(uid)

        self.cookies["username"] = email
        self.cookies["uid"] = uid
        self.cookies["auth"] = "true"
        self.cookies["role"] = st.session_state.get("role", "")
        self.cookies.save()

        st.rerun()