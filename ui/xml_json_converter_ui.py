import streamlit as st
from logic.xml_json_converter import detect_format, convert_json_to_xml, convert_xml_to_json
from ui.json_ui import display_json_result
from database.db_methods import get_conversions, save_conversion
from app import get_uid_cookie


def run_converter():
    get_uid_cookie()
    st.header("🔁 Конвертер JSON ⇄ XML")

    uid = st.session_state.get("uid")

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
                converted = convert_json_to_xml(input_text, item_name=item_name)
                st.success("Результат (XML):")
                st.code(converted, language="xml")
                save_conversion(uid, converted)
            elif fmt["format"] == "invalid_json":
                display_json_result({"ok": False, "error": fmt["error"]}, input_text)
            elif fmt["format"] == "xml":
                converted = convert_xml_to_json(input_text)
                st.success("Результат (JSON):")
                st.code(converted, language="json")
                save_conversion(uid, converted)
            else:
                st.error("Не удалось определить формат. Введите корректный JSON или XML.")
        except Exception as e:
            st.error(f"Ошибка при конвертации: {e}")
    st.write("UID для list_widget:", uid)

    list_widget()



def list_widget():
    uid = cookies.get("uid")
    if not uid:
        st.warning("UID не найден — пользователь не авторизован.")
        return
    if "uid" in st.session_state:
        conversions = get_conversions(st.session_state.uid)
        st.write("DEBUG: conversions", conversions)

        st.subheader("Конвертации")

        if not conversions:
            st.info("У вас пока нет сохранённых конвертаций")
        else:
            for item in conversions:
                with st.expander(
                        f"Конвертация от {item['timestamp'].strftime('%Y/%m/%d %H:%M:%S') if item['timestamp'] else '-'}"):
                    st.code(item["converted"])
