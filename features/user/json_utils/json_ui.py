import streamlit as st
import re
from features.user.json_utils.json_utils import validate_json
from shared.session.cookie_session import CookieSessionManager

def display_json_result(result: dict, original_text: str):
    if result["ok"]:
        st.success("✅ JSON корректен")
        st.info(f"Количество объектов на верхнем уровне: {result['count']}")
        with st.expander("Отформатированный JSON"):
            st.json(result["data"])
    else:
        st.error("Ошибка в JSON:")
        st.code(result["error"], language="plaintext")

        match = re.search(r'строка (\d+)', result["error"])
        if match:
            line_num = int(match.group(1))

            lines = original_text.splitlines()
            start = max(0, line_num - 5)
            end = min(len(lines), line_num + 4)

            snippet = []
            for i in range(start, end):
                line_prefix = f"{i+1:>4}: "
                if i + 1 == line_num:
                    snippet.append(f"{line_prefix}👉 {lines[i]}")
                else:
                    snippet.append(f"{line_prefix}   {lines[i]}")
            st.subheader("Контекст ошибки (±4 строки):")
            st.code("\n".join(snippet), language="json")
        else:
            st.info("Не удалось определить строку с ошибкой.")


def run_json_tool(cookie_manager):
    st.header("JSON-анализатор")

    # Инициализация session_state перед виджетом
    if "json_text" not in st.session_state:
        st.session_state.json_text = cookie_manager.get_value("json_text") or ""

    if "clear_uploaded" not in st.session_state:
        st.session_state.clear_uploaded = False

    # uploader: показываем только если флаг не установлен
    if not st.session_state.clear_uploaded:
        st.session_state.uploaded_file = st.file_uploader("📂 Загрузите JSON", type="json")
        if st.session_state.uploaded_file:
            data = st.session_state.uploaded_file.getvalue().decode("utf-8")
            st.session_state.json_text = data
            cookie_manager.set_value("json_text", data)
    else:
        # Если скрыт, создаём кнопку для повторного отображения uploader
        def reset_uploader():
            st.session_state.clear_uploaded = False

        st.button("Загрузить новый файл", on_click=reset_uploader)


    # --- callback для очистки ---
    def clear_text():
        st.session_state.json_text = ""
        cookie_manager.set_value("json_text", "")
        st.session_state.clear_uploaded = True  # скрываем uploader временно

    def check_json():
        data = st.session_state.json_text
        st.session_state.result = validate_json(data)
        display_json_result(st.session_state.result, data)


    # --- текстовое поле ---
    st.text_area(
        "Вставьте JSON–текст сюда:",
        height=200,
        key="json_text"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.button("Проверить и форматировать JSON", key="check_btn")
    with col2:
        st.button("Очистить", on_click=clear_text, key="clear_btn")

    if st.session_state.check_btn:
        check_json()

# Можно сразу запускать при открытии файла
if __name__ == "__main__":
    run_json_tool()