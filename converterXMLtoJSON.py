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
            xmltodict.parse(f"<root>{text}</root>")  # оборачиваем для проверки
            return "xml"
        except Exception:
            return "unknown"

def convert_json_to_xml(json_str: str, wrap_root: bool = True) -> str:
    """Конвертирует JSON в XML, с возможностью убрать root"""
    obj = json.loads(json_str)
    if wrap_root:
        obj = {"root": obj}
    xml_str = xmltodict.unparse(obj, pretty=True)
    if not wrap_root:
        # удаляем первую и последнюю строку <root>...</root>
        lines = xml_str.strip().splitlines()
        xml_str = "\n".join(lines[1:-1])
    return xml_str

def convert_xml_to_json(xml_str: str) -> str:
    """Конвертирует XML в JSON, поддерживая multiple roots"""
    wrapped = f"<root>{xml_str}</root>"
    obj = xmltodict.parse(wrapped)
    root = obj["root"]
    # если корень — список однотипных элементов
    result = root if isinstance(root, (list, dict)) else {"root": root}
    return json.dumps(result, indent=2, ensure_ascii=False)

def run_converter():
    st.header("🔁 Конвертер JSON ⇄ XML с поддержкой multiple roots")

    input_text = st.text_area("Введите JSON или XML:", height=300)
    wrap = st.checkbox("Оборачивать JSON в <root>", value=True)

    if st.button("Конвертировать"):
        if not input_text.strip():
            st.warning("Поле ввода пустое.")
            return

        fmt = detect_format(input_text)
        try:
            if fmt == "json":
                result = convert_json_to_xml(input_text, wrap_root=wrap)
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