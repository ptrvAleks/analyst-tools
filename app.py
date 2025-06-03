import streamlit as st
from account import show_login
from json_utils import count_root_objects
import codecs
import json
# from db_utils import get_db_session

st.set_page_config(page_title="Streamlit JSON Validator", layout='wide')

def run_json_tool():

    if "input_json" not in st.session_state:
        st.session_state.input_json = '[\n\t{\n\n\t}\n]'

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("RELOAD"):
            st.rerun()  # безопасный перезапуск

    with col2:
        if st.button("CLEAR"):
            st.session_state.input_json = '[\n\t{\n\n\t}\n]'

    left, right = st.columns([1, 1])

    with left:
        st.session_state.input_json = st.text_area(
            "JSON Editor",
            st.session_state.input_json,
            height=600,
            key="json_input_area"
        )

    with right:
        try:
            input_str = json.loads(st.session_state.input_json)
            json_out = json.dumps(input_str, sort_keys=False, indent=4)

            # Сохраняем в файл, если нужно
            with codecs.open("output.json", "w", encoding="utf-8") as f:
                f.write(json_out)

            count = count_root_objects(input_str)
            st.success(f"Корневых объектов: {count}")
            st.text_area("JSON OUTPUT", json_out, height=600)

        except Exception as e:
            st.error("Ошибка разбора JSON")
            st.text_area("JSON OUTPUT", str(e), height=600)

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