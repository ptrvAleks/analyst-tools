import json
import xmltodict
import streamlit as st
from json_utils import validate_json, display_json_result
import xml.etree.ElementTree as ET


def detect_format(text: str) -> dict:
    """
    Определяет формат текста: json, invalid_json, xml или unknown.

    Возвращает:
      {'format': 'json'}
      {'format': 'invalid_json', 'error': <описание ошибки>}
      {'format': 'xml'}
      {'format': 'unknown'}
    """
    json_result = validate_json(text)
    if json_result["ok"]:
        return {"format": "json"}

    if text.strip().startswith("{") or text.strip().startswith("["):
        return {
            "format": "invalid_json",
            "error": json_result["error"]
        }

    try:
        xmltodict.parse(f"<root>{text}</root>")
        return {"format": "xml"}
    except Exception:
        return {"format": "unknown"}

def convert_json_to_xml(json_str: str, wrap_root: bool = True, item_name: str = "item") -> str:
    """Конвертирует JSON в XML, с поддержкой списков верхнего уровня"""
    obj = json.loads(json_str)

    if not item_name:
        item_name = "item"

    # если верхний уровень — список, оборачиваем
    if isinstance(obj, list):
        obj = {item_name: obj}

    if wrap_root:
        obj = {"root": obj}

    xml_str = xmltodict.unparse(obj, pretty=True)

    if not wrap_root:
        # удаляем <root> и </root>
        lines = xml_str.strip().splitlines()
        xml_str = "\n".join(lines[1:-1])

    return xml_str

def convert_xml_to_json(xml_str: str) -> str:
    """Конвертирует XML в JSON, поддерживая multiple roots"""
    wrapped = f"<root>{xml_str}</root>"
    obj = xmltodict.parse(wrapped)
    root = obj.get("root", {})

    return json.dumps(root, indent=2, ensure_ascii=False)

def run_converter():
    st.header("🔁 Конвертер JSON ⇄ XML")

    input_text = st.text_area("Введите JSON или XML:", height=300)

    st.markdown("### ⚙️ Настройки")
    wrap = st.checkbox("Оборачивать в `<root>` (для XML)", value=True)
    item_name = st.text_input("Имя узла для массива JSON → XML", value="item")

    if st.button("Конвертировать"):
        if not input_text.strip():
            st.warning("Поле ввода пустое.")
            return

        fmt = detect_format(input_text)
        try:
            if fmt["format"] == "json":
                result = convert_json_to_xml(input_text, wrap_root=wrap, item_name=item_name)
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