import json
import xmltodict
import streamlit as st

def detect_format(text: str) -> str:
    """Определяет формат: JSON или XML"""
    try:
        json.loads(text)
        return "json"
    except json.JSONDecodeError:
        try:
            xmltodict.parse(text)
            return "xml"
        except Exception:
            return "unknown"

def convert_json_to_xml(json_str: str) -> str:
    """Конвертирует JSON в XML"""
    obj = json.loads(json_str)
    xml_str = xmltodict.unparse({"root": obj}, pretty=True)
    return xml_str

def convert_xml_to_json(xml_str: str) -> str:
    """Конвертирует XML в JSON"""
    obj = xmltodict.parse(xml_str)
    json_str = json.dumps(obj.get("root", obj), indent=2, ensure_ascii=False)
    return json_str

def run_converter():
    st.header("🔁 Конвертер JSON ⇄ XML")

    input_text = st.text_area("Введите JSON или XML:", height=300)

    if st.button("Конвертировать"):
        if not input_text.strip():
            st.warning("Поле ввода пустое.")
            return

        fmt = detect_format(input_text)
        try:
            if fmt == "json":
                result = convert_json_to_xml(input_text)
                st.success("Результат (XML):")
                st.code(result, language="xml")
            elif fmt == "xml":
                result = convert_xml_to_json(input_text)
                st.success("Результат (JSON):")
                st.code(result, language="json")
            else:
                st.error("Не удалось определить формат. Убедитесь, что это корректный JSON или XML.")
        except Exception as e:
            st.error(f"Ошибка при конвертации: {e}")