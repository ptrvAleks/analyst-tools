import streamlit as st
from account import login_user
from json_utils import count_root_objects, validate_json
# from db_utils import get_db_session

def run_json_tool():
    st.header("JSON-анализатор")

    json_text = st.text_area("Вставьте JSON–текст сюда:", height=200)
    if st.button("Проверить JSON"):
        result = validate_json(json_text)
        if result["ok"]:
            count = count_root_objects(json_text)
            st.success(f"Корневых объектов: {count}")
            st.json(result["data"])
        else:
            st.error(f"Ошибка JSON: {result['error']}")

def run_db_tool():
    st.header("Работа с БД (пока заглушка)")
    st.info("Здесь позже будет функционал для взаимодействия с вашей базой данных.")

def main():
    st.title("Вход в систему")
    st.sidebar.title("Авторизация")

    username = st.sidebar.text_input("Имя пользователя", key="login_username")
    password = st.sidebar.text_input("Пароль", type="password", key="login_password")
    login_btn = st.sidebar.button("Войти")

    if login_btn:
        if login_user(username, password):
            st.success(f"Добро пожаловать, {username}!")
            st.write("---")

            menu = st.sidebar.radio("Выберите утилиту", ["JSON-анализатор", "Работа с БД (заготовка)"])

            if menu == "JSON-анализатор":
                run_json_tool()
            elif menu == "Работа с БД (заготовка)":
                run_db_tool()
        else:
            st.error("Неверные имя пользователя или пароль")

if __name__ == "__main__":
    main()