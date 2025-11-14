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
    
    if user is None:
        raise ValueError("Пользователь не найден, хотя is_authenticated = True")

    print(f"Вошёл пользователь {user.email} с ролью {user.role} с именем {user.first_name}")
    
    choice, db_action, generator_action = show_sidebar(auth, user.role, user.first_name)

    if choice == "Работа с БД":
        if db_action == "Просмотр":
            run_db_tool()
    if choice == "Генераторы":
        if generator_action == "Генератор JSON-Schema":
            run_json_schema_generator()
        elif generator_action == "Генератор шаблонов":
            run_template_creator()
        elif generator_action == "Генератор JSON":
            run_template_builder()
    elif choice == "Проверка JSON":
        run_json_tool(cookie_manager)
    elif choice == "Конвертер JSON ⇄ XML":
        run_converter()
    elif choice == "Создание JSON по схеме":
        run_json_generator()
    elif choice == "Пользователи":
        run_user_list()

if __name__ == "__main__":
    main()