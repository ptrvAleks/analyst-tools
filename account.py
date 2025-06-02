import streamlit as st
import hashlib
import requests
import firebase_admin
from firebase_admin import credentials
import json

# Firebase Realtime Database URL
FIREBASE_URL = "https://analyst-tools-65fbf-default-rtdb.europe-west1.firebasedatabase.app/"

# Инициализация Firebase (если ещё не инициализировано)
if not firebase_admin._apps:
    cred_dict = dict(st.secrets["firebase"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URL
    })

# Функции
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(username):
    response = requests.get(f"{FIREBASE_URL}/users/{username}.json")
    return response.status_code == 200 and response.json() is not None

def register_user(username, password):
    hashed = hash_password(password)
    data = {"password": hashed}
    response = requests.put(f"{FIREBASE_URL}/users/{username}.json", json=data)
    return response.status_code == 200

def login_user(username, password):
    response = requests.get(f"{FIREBASE_URL}/users/{username}.json")
    if response.status_code == 200 and response.json():
        stored_hash = response.json().get("password")
        return stored_hash == hash_password(password)
    return False

# Состояние
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# UI
st.title("Авторизация")

choice = st.radio("Выберите действие", ["Войти", "Зарегистрироваться"])

username = st.text_input("Имя пользователя", key="username_input")
password = st.text_input("Пароль", type="password", key="password_input")

if choice == "Зарегистрироваться":
    if st.button("Зарегистрироваться"):
        if user_exists(username):
            st.error("Пользователь уже существует.")
        elif register_user(username, password):
            st.success("Успешная регистрация! Теперь войдите.")
        else:
            st.error("Ошибка при регистрации.")
else:
    if st.button("Войти"):
        if login_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.experimental_rerun()  # Обновим страницу, чтобы app.py мог запуститься
        else:
            st.error("Неверные имя пользователя или пароль.")