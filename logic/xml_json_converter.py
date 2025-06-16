import json
import xmltodict
from logic.json_utils import validate_json
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

