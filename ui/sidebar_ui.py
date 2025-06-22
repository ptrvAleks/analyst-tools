import streamlit as st

def show_sidebar(auth, user_role, name):

    tool_actions = {
        "Проверка JSON": "run_json_tool",
        "Конвертер JSON ⇄ XML": "run_converter",
        "Генератор JSON-Schema": "run_json_schema_generator",
        "Генератор JSON": "run_json_generator",
    }

    with st.sidebar:
        if name:
            st.header(f"Привет, {name}!")
        if st.button("Выйти"):
            auth.logout()
        st.title("Навигация")
        options = list(tool_actions.keys())
        if user_role == "admin":
            options.append("Работа с БД")
            options.append("Пользователи")
        choice = st.selectbox("Выберите инструмент:", options)

        if choice == "Работа с БД":
            db_action = st.radio("Выберите действие:", ["Просмотр"], key="db_action")
        else:
            db_action = None

    return choice, db_action