import streamlit as st
import hashlib
import requests
import firebase_admin
from firebase_admin import credentials
import json

# Firebase Realtime Database URL
FIREBASE_URL = "https://analyst-tools-65fbf-default-rtdb.europe-west1.firebasedatabase.app/"  # ← Замени на свой
# Загружаем секрет из streamlit
firebase_info = st.secrets["firebase"]

# Преобразуем его в dict
cred_dict = dict(firebase_info)

# Проверяем, инициализирован ли Firebase уже
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': f'{FIREBASE_URL}'
    })

# Хеширование пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Сохранение нового пользователя
def register_user(username, password):
    hashed = hash_password(password)
    data = { "password": hashed }
    response = requests.put(f"{FIREBASE_URL}/users/{username}.json", json=data)
    return response.status_code == 200

# Проверка логина
def login_user(username, password):
    response = requests.get(f"{FIREBASE_URL}/users/{username}.json")
    if response.status_code == 200 and response.json():
        stored_hash = response.json().get("password")
        return stored_hash == hash_password(password)
    return False

def user_exists(username):
    response = requests.get(f"{FIREBASE_URL}/users/{username}.json")
    return response.status_code == 200 and response.json() is not None

def register_user_safe(username, password):
    if user_exists(username):
        print("Пользователь уже существует.")
        return False
    return register_user(username, password)

# Streamlit UI
st.title("Firebase Login")

choice = st.selectbox("Выберите действие", ["Вход", "Регистрация"])

username = st.text_input("Имя пользователя")
password = st.text_input("Пароль", type="password")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if choice == "Регистрация":
    if st.button("Зарегистрироваться"):
        if register_user_safe(username, password):
            st.success("Пользователь зарегистрирован.")
        else:
            st.error("Ошибка регистрации.")
else:
    if st.button("Войти"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("Успешный вход!")
        else:
            st.error("Неверные учетные данные.")

if st.session_state.logged_in:
    st.write(f"Вы вошли как {username}")