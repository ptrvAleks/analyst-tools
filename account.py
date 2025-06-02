import streamlit as st
import hashlib
import requests
import firebase_admin
from firebase_admin import credentials
import json

# Firebase Realtime Database URL
FIREBASE_URL = "https://analyst-tools-65fbf-default-rtdb.europe-west1.firebasedatabase.app/"

# Загружаем данные авторизации Firebase из secrets
firebase_info = st.secrets["firebase"]
cred_dict = dict(firebase_info)
cred = credentials.Certificate(cred_dict)

# Инициализируем Firebase только один раз
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URL
    })

# --- Утилиты хеширования и работы с БД ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    hashed = hash_password(password)
    data = {"password": hashed}
    response = requests.put(f"{FIREBASE_URL}/users/{username}.json", json=data)
    return response.status_code == 200

def user_exists(username):
    response = requests.get(f"{FIREBASE_URL}/users/{username}.json")
    return response.status_code == 200 and response.json() is not None

def register_user_safe(username, password):
    if user_exists(username):
        return False
    return register_user(username, password)

def login_user(username, password):
    response = requests.get(f"{FIREBASE_URL}/users/{username}.json")
    if response.status_code == 200 and response.json():
        stored_hash = response.json().get("password")
        return stored_hash == hash_password(password)
    return False

# --- Работа с состоянием ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Интерфейс ---
st.title("Firebase Login")

if not st.session_state.logged_in:
    choice = st.selectbox("Выберите действие", ["Вход", "Регистрация"])

    username = st.text_input("Имя пользователя", key="username_input")
    password = st.text_input("Пароль", type="password", key="password_input")

    if choice == "Регистрация":
        if st.button("Зарегистрироваться"):
            if register_user_safe(username, password):
                st.success("Пользователь зарегистрирован.")
            else:
                st.error("Пользователь уже существует или произошла ошибка.")
    else:
        if st.button("Войти"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Успешный вход!")
            else:
                st.error("Неверные учетные данные.")
else:
    st.success(f"Вы вошли как {st.session_state.username}")
    if st.button("Выйти"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()