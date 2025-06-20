import streamlit as st
from authentication.auth_ui import show_login
from ui.json_schema_generator_ui import run_json_schema_generator
from ui.json_ui import run_json_tool
from ui.db_history_sql_query_ui import run_db_tool
from ui.xml_json_converter_ui import run_converter
from ui.generate_json_ui import run_json_generator
from authentication.auth_manager import AuthManager
from ui.sidebar_ui import show_sidebar

auth = AuthManager(st.secrets["cookies"]["password"])

def main():
    if not auth.is_authenticated:
        show_login(auth)
        return

    user = auth.user
    print(f"Вошёл пользователь {user.email} с ролью {user.role}")

    choice, db_action = show_sidebar(auth, user.role, user.name)

    if choice == "Работа с БД":
        if db_action == "Просмотр":
            run_db_tool()
    elif choice == "Проверка JSON":
        run_json_tool()
    elif choice == "Конвертер JSON ⇄ XML":
        run_converter()
    elif choice == "Генератор JSON-Schema":
        run_json_schema_generator()
    elif choice == "Генератор JSON":
        run_json_generator()

if __name__ == "__main__":
    main()