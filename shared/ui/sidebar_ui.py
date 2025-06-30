import streamlit as st

def show_sidebar(auth, user_role, name):
    tool_actions = {
        "Проверка JSON": "run_json_tool",
        "Конвертер JSON ⇄ XML": "run_converter",
        "Создание JSON по схеме": "run_json_generator"
    }

    db_action = None
    generator_action = None

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
        options.append("Генераторы")

        choice = st.selectbox("Выберите инструмент:", options)

        if choice == "Работа с БД":
            db_action = st.radio("Выберите действие:", ["Просмотр"], key="db_action")
        elif choice == "Генераторы":
            generator_action = st.radio("Выберите:", ["Генератор JSON-Schema", "Генератор шаблонов", "Генератор JSON"], key="generator_action")

    return choice, db_action, generator_action