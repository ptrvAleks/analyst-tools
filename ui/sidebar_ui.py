import streamlit as st

def show_sidebar(auth, role: str):
    from ui.db_history_sql_query_ui import run_db_tool

    tool_actions = {
        "Проверка JSON": "run_json_tool",
        "Конвертер JSON ⇄ XML": "run_converter",
        "Генератор JSON-Schema": "run_json_schema_generator",
        "Генератор JSON": "run_json_generator",
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
        else:
            db_action = None

    return choice, db_action