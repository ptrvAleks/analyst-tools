import streamlit as st
from authentication.auth_ui import show_login
from ui.json_schema_generator_ui import run_json_schema_generator
from ui.json_ui import run_json_tool
from ui.db_history_sql_query_ui import run_db_tool
from streamlit_cookies_manager import EncryptedCookieManager
from ui.xml_json_converter_ui import run_converter
from ui.generate_json_ui import run_json_generator
from database.db_methods import get_user_role
from cookie_firebase_uid import get_uid_cookie

cookies = EncryptedCookieManager(password=st.secrets["cookies"]["password"])

def restore_session_from_cookies():
    if "authenticated" not in st.session_state:
        username_cookie = cookies.get("username")
        auth_cookie = cookies.get("auth")
        uid_cookie = cookies.get("uid")

        if auth_cookie == "true" and username_cookie and uid_cookie:
            st.session_state.authenticated = True
            st.session_state.username = username_cookie
            st.session_state.uid = uid_cookie
        else:
            st.session_state.authenticated = False

if not cookies.ready():
    st.stop()
restore_session_from_cookies()

def main():
    # Проверка, залогинен ли пользователь
    if not st.session_state.get("authenticated"):
        show_login(cookies)
    else:
        uid = get_uid_cookie()
        if "role" not in st.session_state:
            st.session_state["role"] = get_user_role(uid)

        user_role = st.session_state["role"]

        with st.sidebar:
            # Кнопка выхода
            if st.button("Выйти"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.uid = None
                cookies["username"] = ""
                cookies["auth"] = ""
                cookies.save()
                st.rerun()
            st.title("Навигация")
            tool_actions = {
                "Проверка JSON": run_json_tool,
                "Конвертер JSON ⇄ XML": run_converter,
                "Генератор JSON-Schema": run_json_schema_generator,
                "Генератор JSON": run_json_generator,
            }

            options = list(tool_actions.keys())
            if user_role == "admin":
                options.append("Работа с БД")

            choice = st.selectbox("Выберите инструмент:", options)

            if choice == "Работа с БД":
                with st.expander("Действия с БД", expanded=True):
                    db_action = st.radio("Выберите действие:", ["Просмотр"], key="db_action")

        if choice in tool_actions:
            tool_actions[choice]()
        elif choice == "Работа с БД":
            if st.session_state.get("db_action") == "Просмотр":
                run_db_tool()



if __name__ == "__main__":
    main()