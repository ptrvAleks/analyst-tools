import json
import xmltodict
import streamlit as st
from json_utils import validate_json, display_json_result
from typing import Any


def detect_format(text: str) -> dict:
    """
    Определяет формат текста: json, invalid_json, xml или unknown.
    """
    # Проверка JSON
    json_result = validate_json(text)
    if json_result["ok"]:
        return {"format": "json"}

    if text.strip().startswith("{") or text.strip().startswith("["):
        return {
            "format": "invalid_json",
            "error": json_result["error"]
        }

    # Удаляем XML-декларацию
    cleaned_text = "\n".join(
        line for line in text.splitlines()
        if not line.strip().startswith("<?xml")
    )

    try:
        xmltodict.parse(cleaned_text)
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

def _postprocess(value: Any) -> Any:
    """Рекурсивно приводит строки '' → None, 'true'/'false' → bool."""
    if isinstance(value, dict):
        return {k: _postprocess(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_postprocess(v) for v in value]
    if value == "":
        return None
    if isinstance(value, str) and value.lower() in ("true", "false"):
        return value.lower() == "true"
    return value

def convert_xml_to_json(xml_str: str) -> str:
    """
    Конвертирует XML вида <root><item>…</item>…</root> → JSON‑массив.
    • Удаляет XML‑декларацию.
    • Выкидывает обёртки root/item.
    • Преобразует "" → null, "true"/"false" → bool.
    """
    # 1. убираем строку <?xml …?>
    cleaned = "\n".join(
        line for line in xml_str.splitlines()
        if not line.strip().startswith("<?xml")
    )

    # 2. парсим
    parsed = xmltodict.parse(cleaned)

    # 3. достаём список <item>
    items = parsed.get("root", {}).get("item", [])

    # xmltodict возвращает dict, если item один ― превращаем в список
    if not isinstance(items, list):
        items = [items]

    # 4. пост‑обработка типов
    items = _postprocess(items)

    # 5. JSON‑строка
    return json.dumps(items, indent=2, ensure_ascii=False)

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