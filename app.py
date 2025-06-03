import streamlit as st
from account import show_login
from json_utils import count_root_objects, validate_json

def run_json_tool():
    st.header("JSON-анализатор")

    json_text = st.text_area("Вставьте JSON–текст сюда:", height=200)

    col1, col2 = st.columns(2)
    with col1:
        check_btn = st.button("Проверить и форматировать JSON")
    with col2:
        clear_btn = st.button("Очистить")

    if clear_btn:
        st.rerun()

    if check_btn:
        result = validate_json(json_text)

        if result["ok"]:
            parsed_json = result["data"]
            count = count_root_objects(json_text)

            st.success(f"JSON корректен ✅")
            st.info(f"Количество объектов на верхнем уровне: {count}")

            st.subheader("Форматированный JSON:")
            st.json(parsed_json)
        else:
            st.error(f"❌ Ошибка: {result['error']}")

def run_db_tool():
    st.header("Работа с БД (пока заглушка)")
    st.info("Здесь позже будет функционал для взаимодействия с вашей базой данных.")

def main():
    if not st.session_state.get("authenticated", False):
        show_login()
        st.stop()

    st.sidebar.title("Навигация")
    choice = st.sidebar.selectbox("Выберите инструмент:", ["Проверка JSON", "Работа с БД"])

    if choice == "Проверка JSON":
        run_json_tool()
    elif choice == "Работа с БД":
        run_db_tool()

if __name__ == "__main__":
    main()