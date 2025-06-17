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


def _find_main_array(parsed: Dict[str, Any]) -> List[Any]:
    """
    Возвращает первый список элементов в JSON‑структуре.
    1) Сначала пробует популярные пути (data, root.item, items…).
    2) Если не найдено — рекурсивно ищет первый list в дереве.
    """

    common_paths = [
        ["data"],
        ["root", "item"],
        ["items"],
        ["list"],
        ["results"],
    ]

    # 1. По избранным путям
    for path in common_paths:
        current: Union[Dict[str, Any], List[Any]] = parsed
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                break           # путь оборвался
        else:                    # дошли до конца пути
            # одиночный <item> мог прийти как dict → делаем list
            return current if isinstance(current, list) else [current]

    # 2. Fallback: первый встретившийся list
    def deep_search(obj: Any) -> List[Any] | None:
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            for value in obj.values():
                found = deep_search(value)
                if found:
                    return found
        return None

    return deep_search(parsed) or []


def _postprocess(items: List[Any]) -> List[Any]:
    """
    Приводит строки к нужным типам:
      • ""   → None
      • "true"/"false" (регистронезависимо) → bool
      • такие строки, похожие на UUID или ISO‑дату, оставляет как str (без изменений)
    """
    uuid_re   = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
    date_re   = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    iso_dt_re = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

    def convert(value: Any) -> Any:
        if isinstance(value, str):
            if value == "":
                return None
            low = value.lower()
            if low == "true":
                return True
            if low == "false":
                return False
            # uuid / date / iso‑datetime оставляем строками
            if uuid_re.match(value) or date_re.match(value) or iso_dt_re.match(value):
                return value
        if isinstance(value, list):
            return [convert(v) for v in value]
        if isinstance(value, dict):
            return {k: convert(v) for k, v in value.items()}
        return value

    return [convert(item) for item in items]

# ------------------------- main -------------------------

def convert_xml_to_json(xml_str: str) -> str:
    """
    Конвертирует XML в JSON‑массив.

    • Удаляет XML‑декларацию.
    • Универсально ищет «главный» массив данных (data / root.item / items …).
    • Преобразует "" → null, "true"/"false" → bool.
    """

    # 1. Убираем строку <?xml …?>
    cleaned = "\n".join(
        line for line in xml_str.splitlines()
        if not line.strip().startswith("<?xml")
    )

    # 2. Парсим XML → dict
    parsed = xmltodict.parse(cleaned)

    # 3. Находим нужный список элементов
    items = _find_main_array(parsed)

    # 4. Приводим типы
    items = _postprocess(items)

    # 5. Возвращаем красиво отформатированную JSON‑строку
    return json.dumps(items, indent=2, ensure_ascii=False)
