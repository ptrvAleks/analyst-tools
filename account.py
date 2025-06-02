# account.py
import streamlit as st
import hashlib
import requests
import firebase_admin
from firebase_admin import credentials

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

def show_login():
    st.title("Авторизация")

    choice = st.selectbox("Выберите действие", ["Вход", "Регистрация"])
    username = st.text_input("Имя пользователя", key="username")
    password = st.text_input("Пароль", type="password", key="password")

    if choice == "Регистрация":
        if st.button("Зарегистрироваться"):
            if user_exists(username):
                st.error("Пользователь уже существует.")
            elif register_user(username, password):
                st.success("Пользователь зарегистрирован.")
            else:
                st.error("Ошибка регистрации.")
    else:
        if st.button("Войти"):
            if login_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("Неверные учетные данные.")