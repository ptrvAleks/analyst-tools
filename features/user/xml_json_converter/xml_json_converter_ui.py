import streamlit as st
from features.user.xml_json_converter.xml_json_converter import detect_format, convert_json_to_xml, convert_xml_to_json
from features.user.json_utils.json_ui import display_json_result
from database.user_service import UserService
from logic.user import User

service = UserService()

def run_converter():
    current_user: User | None = st.session_state.get("user")

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
                converted = convert_json_to_xml(input_text, item_name=item_name)
                st.success("Результат (XML):")
                st.code(converted, language="xml")
                service.save_conversion(current_user, converted)
            elif fmt["format"] == "invalid_json":
                display_json_result({"ok": False, "error": fmt["error"]}, input_text)
            elif fmt["format"] == "xml":
                converted = convert_xml_to_json(input_text)
                st.success("Результат (JSON):")
                st.code(converted, language="json")
                service.save_conversion(current_user, converted)
            else:
                st.error("Не удалось определить формат. Введите корректный JSON или XML.")
        except Exception as e:
            st.error(f"Ошибка при конвертации: {e}")

    list_widget()


def list_widget():
    current_user: User | None = st.session_state.get("user")

    conversions = service.get_conversions(current_user)

    st.subheader("Конвертации")

    if not conversions:
        st.info("У вас пока нет сохранённых конвертаций")
    else:
        for idx, item in enumerate(conversions):
            with st.expander(f"Конвертация от {item['timestamp'].strftime('%d.%m.%Y %H:%M:%S') if item['timestamp'] else '-'}"):
                st.code(item["converted"])
                document_id = item["id"]

                if st.button("Удалить", key=f"delete_{document_id}_{idx}"):
                    service.delete_conversion(current_user, document_id)
                    st.success("Удалено")
                    st.rerun()