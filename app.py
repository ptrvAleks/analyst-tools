import streamlit as st
from account import show_login
from json_utils import count_root_objects
import codecs
import pyautogui
import json
# from db_utils import get_db_session

def run_json_tool():
    st.set_page_config(page_title="Streamlit JSON Validator", layout='wide')

    c_1, c_2 = st.columns([1, 1])

    with c_1:
        reload = st.button("RELOAD")

    with c_2:
        clear = st.button("CLEAR")

    def Clear():
        pyautogui.press("tab", interval=0.15)
        pyautogui.press("tab", interval=0.15)
        pyautogui.hotkey("ctrl", "a", 'del', interval=0.15)

    def refresh():
        pyautogui.press("f5", interval=0.15)

    # Clear I / referesh
    if clear: Clear()
    if reload: refresh()

    col_1, col_2 = st.columns([1, 1])

    with col_1:
        input = st.text_area("JSON Editor", "[" + "\n" + chr(9) + "{" + "\n\n" + chr(9) + "}" + "\n" + "]", height=600)

    with col_2:
        try:
            input_str = json.loads(input)
            f = codecs.open("output.json", "w", encoding="utf-8")
            json_out = json.dumps(input_str, sort_keys=False, indent=4)
            f.write(json_out)
            f.flush()
            o = open("output.json")
            ojson = o.read()
            count = count_root_objects(input_str)
            st.success(f"Корневых объектов: {count}")
            st.text_area("JSON OUTPUT", ojson, height=600)
        except Exception as e:
            st.text_area("JSON OUTPUT", e, height=600)

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