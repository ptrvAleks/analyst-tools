import streamlit as st
from account import login_user, show_login
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
    if not st.session_state.get("authenticated", False):
        show_login()
        st.stop()  # Останавливаем app.py, пока пользователь не войдёт

    # Главное меню
    st.sidebar.title("Навигация")
    choice = st.sidebar.selectbox("Выберите инструмент:", ["Проверка JSON", "Работа с БД"])

    if choice == "Проверка JSON":
        run_json_tool()
    elif choice == "Работа с БД":
        run_db_tool()

if __name__ == "__main__":
    main()