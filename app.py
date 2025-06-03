import streamlit as st
from account import show_login
from json_utils import run_json_tool
from db_utils import run_db_tool

def main():
    # Проверка, залогинен ли пользователь
    if not st.session_state.get("authenticated"):
        show_login()
    else:
        with st.sidebar:
            # Кнопка выхода
            if st.button("Выйти"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.rerun()
            st.sidebar.title("Навигация")
            choice = st.sidebar.selectbox("Выберите инструмент:", ["Проверка JSON", "Работа с БД"])

        if choice == "Проверка JSON":
            run_json_tool()
        elif choice == "Работа с БД":
            with st.sidebar.expander("Действия с БД", expanded=True):
                db_action = st.radio("Выберите действие:", ["Просмотр", "Добавление", "Удаление"], key="db_action")

            if db_action == "Просмотр":
                run_db_tool()
            elif db_action == "Добавление":
                run_db_add()
            elif db_action == "Удаление":
                run_db_delete()

if __name__ == "__main__":
    main()