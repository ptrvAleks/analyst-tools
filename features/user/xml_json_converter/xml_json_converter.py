import json
import xmltodict
from features.user.json_utils.json_utils import validate_json
from typing import Any
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
    try:
        obj = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON: {e}")

    if not item_name:
        item_name = "item"

    need_wrap_root = True  # По умолчанию оборачиваем в <root>

    # Если верхний уровень — список, оборачиваем в item_name
    if isinstance(obj, list):
        obj = {item_name: obj}

    elif isinstance(obj, dict):
        # Если словарь только с одним ключом, то не оборачиваем
        if len(obj) == 1:
            need_wrap_root = False
        else:
            need_wrap_root = True

    else:
        # Примитив — оборачиваем обязательно
        obj = {"value": obj}
        need_wrap_root = True

    if need_wrap_root:
        obj = {"root": obj}

    xml_str = xmltodict.unparse(obj, pretty=True)

    # Если оборачивали только для генерации XML и хотим убрать <root> — делаем это
    if not need_wrap_root:
        lines = xml_str.strip().splitlines()
        if len(lines) >= 3:
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
    Конвертирует XML в JSON:
    • Удаляет XML-декларацию.
    • Убирает верхнюю обёртку <root> → {...}.
    • Преобразует "" → null, "true"/"false" → bool.
    """

    # 1. Убираем строку <?xml ... ?>
    cleaned = "\n".join(
        line for line in xml_str.splitlines()
        if not line.strip().startswith("<?xml")
    )

    # 2. Парсим XML
    parsed = xmltodict.parse(cleaned)

    # 3. Удаляем "root", если он верхний
    parsed = parsed.get("root", parsed)

    # 4. Преобразуем типы
    parsed = _postprocess_any(parsed)

    # 5. Возвращаем отформатированный JSON
    return json.dumps(parsed, indent=2, ensure_ascii=False)
