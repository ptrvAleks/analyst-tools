import streamlit as st
from ui.json_schema_generator_ui import run_json_schema_generator
from ui.json_ui import run_json_tool
from ui.db_history_sql_query_ui import run_db_tool
from ui.xml_json_converter_ui import run_converter
from ui.generate_json_ui import run_json_generator
from authentication.auth_manager import AuthManager
from ui.main_sidebar import sidebar

def sidebar():
    auth = AuthManager(st.secrets["cookies"]["password"])

    role = auth.role
    tool_actions = {
        "Проверка JSON": run_json_tool,
        "Конвертер JSON ⇄ XML": run_converter,
        "Генератор JSON-Schema": run_json_schema_generator,
        "Генератор JSON": run_json_generator,
    }
    with st.sidebar:
        if st.button("Выйти"):
            auth.logout()
        st.title("Навигация")
        options = list(tool_actions.keys())
        if role == "admin":
            options.append("Работа с БД")
        choice = st.selectbox("Выберите инструмент:", options)

        if choice == "Работа с БД":
            db_action = st.radio("Выберите действие:", ["Просмотр"], key="db_action")

    # Основной контент
    if choice == "Работа с БД":
        if st.session_state.get("db_action") == "Просмотр":
            run_db_tool()
    elif choice in tool_actions:
        tool_actions[choice]()