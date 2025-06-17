import json
import xmltodict
from logic.json_utils import validate_json
from typing import Union, Optional, List, Dict, Any
import re

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

def convert_json_to_xml(json_str: str, item_name: str = "item") -> str:
    obj = json.loads(json_str)

    if not item_name:
        item_name = "item"

    # Если верхний уровень — список, оборачиваем в item_name
    if isinstance(obj, list):
        obj = {item_name: obj}
        need_wrap_root = True  # список → несколько элементов → нужен корень

    elif isinstance(obj, dict):
        # Если у словаря более одного ключа, то для корректного XML нужен корень
        need_wrap_root = len(obj) != 1
    else:
        # Для других типов (строка, число и т.п.) — оборачиваем в корень
        need_wrap_root = True

    if need_wrap_root:
        obj = {"root": obj}

    xml_str = xmltodict.unparse(obj, pretty=True)

    if not need_wrap_root:
        # Убираем корневой тег <root> (так как оборачивали по необходимости, а тут его не хотим)
        lines = xml_str.strip().splitlines()
        xml_str = "\n".join(lines[1:-1])

    return xml_str

def _postprocess_any(value: Any) -> Any:
    """
    Универсальное преобразование значений:
      • ""   → None
      • "true"/"false" → bool
      • UUID / ISO date → оставить строкой
    """
    uuid_re   = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
    date_re   = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    iso_dt_re = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

    if isinstance(value, str):
        if value == "":
            return None
        low = value.lower()
        if low == "true":
            return True
        if low == "false":
            return False
        if uuid_re.match(value) or date_re.match(value) or iso_dt_re.match(value):
            return value
    elif isinstance(value, list):
        return [_postprocess_any(v) for v in value]
    elif isinstance(value, dict):
        return {k: _postprocess_any(v) for k, v in value.items()}

    return value

# ------------------------- main -------------------------

def convert_xml_to_json(xml_str: str) -> str:
    """
    Конвертирует XML в полноценно структурированный JSON.

    • Удаляет XML‑декларацию.
    • Приводит типы значений рекурсивно.
    • Сохраняет всю структуру (data, meta и др.).
    """
    cleaned = "\n".join(
        line for line in xml_str.splitlines()
        if not line.strip().startswith("<?xml")
    )

    parsed_dict = xmltodict.parse(cleaned)

    processed = _postprocess_any(parsed_dict)

    return json.dumps(processed, indent=2, ensure_ascii=False)
