import streamlit as st
from account import show_login
from json_utils import run_json_tool
from db_utils import run_db_tool
from streamlit_cookies_manager import EncryptedCookieManager
from converterXMLtoJSON import run_converter

cookies = EncryptedCookieManager(password=st.secrets["cookies"]["password"])
if not cookies.ready():
    st.stop()

def main():
    if "authenticated" not in st.session_state:
        username_cookie = cookies.get("username")
        auth_cookie = cookies.get("auth")
        if auth_cookie == "true" and username_cookie:
            st.session_state.authenticated = True
            st.session_state.username = username_cookie
        else:
            st.session_state.authenticated = False
    # Проверка, залогинен ли пользователь
    if not st.session_state.get("authenticated"):
        show_login(cookies)
    else:
        with st.sidebar:
            # Кнопка выхода
            if st.button("Выйти"):
                st.session_state.authenticated = False
                st.session_state.username = None
                cookies["username"] = ""
                cookies["auth"] = ""
                cookies.save()
                st.rerun()
            st.sidebar.title("Навигация")
            choice = st.sidebar.selectbox("Выберите инструмент:", ["Проверка JSON", "Конвертер", "Работа с БД"])

        if choice == "Проверка JSON":
            run_json_tool()
        elif choice == "Работа с БД":
            with st.sidebar.expander("Действия с БД", expanded=True):
                db_action = st.radio("Выберите действие:", ["Просмотр",], key="db_action")
            if db_action == "Просмотр":
                run_db_tool()
        elif choice == "Конвертер":
            run_converter()



if __name__ == "__main__":
    main()