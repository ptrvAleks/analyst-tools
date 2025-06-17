import streamlit as st
import re
from logic.json_utils import validate_json

def display_json_result(result: dict, original_text: str):
    if result["ok"]:
        st.success("✅ JSON корректен")
        st.info(f"Количество объектов на верхнем уровне: {result['count']}")
        st.subheader("Форматированный JSON:")
        st.json(result["data"])
    else:
        st.error("Ошибка в JSON:")
        st.code(result["error"], language="plaintext")

        match = re.search(r'строка (\d+)', result["error"])
        if match:
            line_num = int(match.group(1))
            st.warning(f"Ошибка находится на строке: {line_num}")

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
            with st.expander("Отформатированный JSON"):
                st.subheader("Контекст ошибки (±4 строки):")
                st.code("\n".join(snippet), language="json")
        else:
            st.info("Не удалось определить строку с ошибкой.")

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
        result_of_validate = validate_json(json_text)
        display_json_result(result_of_validate, json_text)

# Можно сразу запускать при открытии файла
if __name__ == "__main__":
    run_json_tool()