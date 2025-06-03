import streamlit as st
from account import show_login
from json_utils import run_json_tool
from db_utils import run_db_tool

def main():
    if not st.session_state.get("authenticated", False):
        show_login()
        st.stop()

    st.sidebar.title("Навигация")
    choice = st.sidebar.selectbox("Выберите инструмент:", ["Проверка JSON", "Работа с БД"])

    if choice == "Проверка JSON":
        run_json_tool()
    elif choice == "Работа с БД":
        # Подпункты
        db_action = st.sidebar.radio("Выберите действие с БД:", ["Просмотр", "Добавление", "Удаление"])

        if db_action == "Просмотр":
            run_db_view()
        elif db_action == "Добавление":
            run_db_add()
        elif db_action == "Удаление":
            run_db_delete()

if __name__ == "__main__":
    main()