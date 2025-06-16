import streamlit as st
from account import show_login
from ui.json_schema_generator_ui import run_json_schema_generator
from ui.json_ui import run_json_tool
from ui.db_history_sql_query_ui import run_db_tool
from streamlit_cookies_manager import EncryptedCookieManager
from ui.xml_json_converter_ui import run_converter

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
            tool_actions = {
                "Проверка JSON": run_json_tool,
                "Конвертер": run_converter,
                "JSON-Schema": run_json_schema_generator,
            }
            choice = st.sidebar.selectbox("Выберите инструмент:", list(tool_actions.keys()) + ["Работа с БД"])

    if choice in tool_actions:
        tool_actions[choice]()  # вызываем соответствующую функцию

    elif choice == "Работа с БД":
        with st.sidebar.expander("Действия с БД", expanded=True):
            db_action = st.radio("Выберите действие:", ["Просмотр"], key="db_action")

        if db_action == "Просмотр":
            run_db_tool()



if __name__ == "__main__":
    main()