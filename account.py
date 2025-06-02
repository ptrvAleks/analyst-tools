import streamlit as st
import hashlib
import requests
import firebase_admin
from firebase_admin import credentials
import json

# --- Константы ---
FIREBASE_URL = "https://analyst-tools-65fbf-default-rtdb.europe-west1.firebasedatabase.app/"

# --- Firebase Init ---
firebase_info = st.secrets["firebase"]
cred_dict = dict(firebase_info)
cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URL
    })

# --- Утилиты ---
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

# --- Состояние ---
if "page" not in st.session_state:
    st.session_state.page = "login"  # или "main"
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Обработчики кнопок ---
def handle_login(username, password):
    if login_user(username, password):
        st.session_state.username = username
        st.session_state.page = "main"
    else:
        st.error("Неверные учетные данные.")

def handle_register(username, password):
    if register_user_safe(username, password):
        st.success("Пользователь зарегистрирован. Теперь войдите.")
    else:
        st.error("Пользователь уже существует.")

def logout():
    st.session_state.page = "login"
    st.session_state.username = ""

# --- UI ---
st.title("🔥 Firebase Login System")

if st.session_state.page == "login":
    tab_login, tab_register = st.tabs(["Вход", "Регистрация"])

    with tab_login:
        login_user_input = st.text_input("Имя пользователя", key="login_username")
        login_pass_input = st.text_input("Пароль", type="password", key="login_password")
        if st.button("Войти"):
            handle_login(login_user_input, login_pass_input)

    with tab_register:
        reg_user_input = st.text_input("Новый пользователь", key="register_username")
        reg_pass_input = st.text_input("Пароль", type="password", key="register_password")
        if st.button("Зарегистрироваться"):
            handle_register(reg_user_input, reg_pass_input)

elif st.session_state.page == "main":
    st.success(f"Вы вошли как {st.session_state.username}")
    st.button("Выйти", on_click=logout)
    # Здесь размести основную функциональность