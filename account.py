# account.py
import streamlit as st
import hashlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

FIREBASE_URL = "https://analyst-tools-65fbf-default-rtdb.europe-west1.firebasedatabase.app/"

# ✅ Новый способ кэширования — как ресурс
@st.cache_resource
def init_firebase():
    cred_dict = dict(st.secrets["firebase"])
    cred = credentials.Certificate(cred_dict)

    # Не даём инициализировать второй раз
    if not firebase_admin._apps:
        return firebase_admin.initialize_app(cred, {
            'databaseURL': FIREBASE_URL
        })
    else:
        return firebase_admin.get_app()

# ⚙️ Инициализация один раз при запуске
init_firebase()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(username):
    ref = db.reference(f"users/{username}")
    return ref.get() is not None

def register_user(username, password):
    hashed = hash_password(password)
    ref = db.reference(f"users/{username}")
    ref.set({"password": hashed})
    return True

def login_user(username, password):
    ref = db.reference(f"users/{username}")
    user_data = ref.get()
    if user_data:
        stored_hash = user_data.get("password")
        return stored_hash == hash_password(password)
    return False

def show_login(cookies):
    st.title("Авторизация")

    with st.form(key="login_form"):
        username = st.text_input(
            "Имя пользователя",
            key="login_username",
            autocomplete="username"
        )
        password = st.text_input(
            "Пароль",
            type="password",
            key="password",
            autocomplete="current-password"
        )
        submit = st.form_submit_button("Войти")

        if submit and login_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username

            # Куки на 7 дней
            expires = datetime.datetime.now() + datetime.timedelta(days=7)
            cookies["username"] = username
            cookies["auth"] = "true"
            cookies.save()
            st.rerun()
        elif submit:
            st.error("Неверные данные")