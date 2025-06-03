# account.py
import streamlit as st
import hashlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime


FIREBASE_URL = "https://analyst-tools-65fbf-default-rtdb.europe-west1.firebasedatabase.app/"
firebase_info = st.secrets["firebase"]
cred_dict = dict(firebase_info)
cred = credentials.Certificate(cred_dict)

# Не даём инициализировать второй раз
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': f'{FIREBASE_URL}'
    })

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

def show_login():
    st.title("Авторизация")

    # Оборачиваем поля в форму с id="login_form"
    with st.form(key="login_form"):
        # Streamlit >=1.18: можем задать autocomplete="username"
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
        # Кнопка внутри формы
        submit = st.form_submit_button("Войти")

        if submit:
            # здесь username и password уже подхватят заполненное браузером значение

            if login_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                # Куки на 7 дней
                expires = datetime.datetime.now() + datetime.timedelta(days=7)
                st.set_cookie("username", username, expires=expires)
                st.set_cookie("auth", "true", expires=expires)
                st.rerun()
            else:
                st.error("Неверные учетные данные.")
