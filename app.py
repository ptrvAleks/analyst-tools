import streamlit as st
from authentication.auth_ui import show_login
from features.user.json_schema_generator.json_schema_generator_ui import run_json_schema_generator
from features.user.json_utils.json_ui import run_json_tool
from features.admin.db_history_sql_query.db_history_sql_query_ui import run_db_tool
from features.user.xml_json_converter.xml_json_converter_ui import run_converter
from features.user.generate_json.generate_json_ui import run_json_generator
from features.admin.users_list.users_list_ui import run_user_list
from authentication.auth_manager import AuthManager
from ui.sidebar_ui import show_sidebar

auth = AuthManager(st.secrets["cookies"]["password"])

def main():
    if not auth.is_authenticated:
        show_login(auth)
        return

    user = auth.user
    print(f"Вошёл пользователь {user.email} с ролью {user.role} с именем {user.first_name}")

    choice, db_action = show_sidebar(auth, user.role, user.first_name)

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
    elif choice == "Пользователи":
        run_user_list()

if __name__ == "__main__":
    main()