import streamlit as st
from auth import get_authenticator
from json_utils import count_root_objects, validate_json


# из db_utils можно импортировать функции, когда понадобится
# from db_utils import get_db_session

def main():
    # ==== Авторизация ====
    authenticator = get_authenticator()
    name, auth_status, username = authenticator.login(location='main')

    if auth_status:
        st.success(f"Добро пожаловать, {name}!")
    elif auth_status is False:
        st.error("Неверное имя пользователя или пароль")
    else:
        st.warning("Пожалуйста, введите имя пользователя и пароль")

    # Пользователь авторизован
    st.success(f"Добро пожаловать, {name}!")
    st.write("---")

    # ==== Основное меню ====
    st.title("Утилиты системного аналитика")

    menu = st.sidebar.radio("Выберите утилиту", ["JSON-анализатор", "Работа с БД (заготовка)"])

    if menu == "JSON-анализатор":
        run_json_tool()
    elif menu == "Работа с БД (заготовка)":
        run_db_tool()


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
    # Пример: сделать кнопку, которая вытягивает первые 5 строк из таблицы
    # if st.button("Получить 5 записей из users"):
    #     with get_db_session() as db:
    #         rows = db.execute("SELECT * FROM users LIMIT 5").fetchall()
    #         st.write(rows)


if __name__ == "__main__":
    main()