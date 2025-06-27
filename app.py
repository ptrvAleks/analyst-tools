import streamlit as st
from authentication.auth_ui import show_login
from features.user.json_schema_generator.json_schema_generator_ui import run_json_schema_generator
from features.user.json_utils.json_ui import run_json_tool
from features.admin.db_history_sql_query.db_history_sql_query_ui import run_db_tool
from features.user.xml_json_converter.xml_json_converter_ui import run_converter
from features.user.generate_json.generate_json_ui import run_json_generator
from features.admin.users_list.users_list_ui import run_user_list
from authentication.auth_manager import AuthManager
from shared.ui.sidebar_ui import show_sidebar
from shared.session.cookie_session import CookieSessionManager
from features.user.template_builder.template_builder_ui import run_template_builder
from features.user.template_creator.template_creator_ui import run_template_creator

cookie_manager = CookieSessionManager(password=st.secrets["cookies"]["password"])
auth = AuthManager(cookie_manager)


def main():
    if not auth.is_authenticated:
        show_login(auth, cookie_manager)
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
    elif choice == "Создание JSON по схеме":
        run_json_generator()
    elif choice == "Пользователи":
        run_user_list()
    elif choice == "Генератор шаблонов":
        run_template_creator()
    elif choice == "Генератор JSON":
        run_template_builder()

if __name__ == "__main__":
    main()