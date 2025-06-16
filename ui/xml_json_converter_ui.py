import streamlit as st
from logic.xml_json_converter import detect_format, convert_json_to_xml, convert_xml_to_json
from ui.json_ui import display_json_result

def run_converter():
    st.header("🔁 Конвертер JSON ⇄ XML")

    input_text = st.text_area("Введите JSON или XML:", height=300)

    st.markdown("### ⚙️ Настройки")
    item_name = st.text_input("Имя узла для массива JSON → XML", value="item")

    if st.button("Конвертировать"):
        if not input_text.strip():
            st.warning("Поле ввода пустое.")
            return

        fmt = detect_format(input_text)
        try:
            if fmt["format"] == "json":
                result = convert_json_to_xml(input_text, item_name=item_name)
                st.success("Результат (XML):")
                st.code(result, language="xml")
            elif fmt["format"] == "invalid_json":
                display_json_result({"ok": False, "error": fmt["error"]}, input_text)
            elif fmt["format"] == "xml":
                result_json = convert_xml_to_json(input_text)
                st.success("Результат (JSON):")
                st.code(result_json, language="json")
            else:
                st.error("Не удалось определить формат. Введите корректный JSON или XML.")
        except Exception as e:
            st.error(f"Ошибка при конвертации: {e}")