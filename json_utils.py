import json

def count_root_objects(json_text: str) -> int:
    """
    Парсит строку json_text и возвращает количество объектов в корне.
    Если корень — не массив, возвращает 1.
    Бросает json.JSONDecodeError при неверном формате.
    """
    data = json.loads(json_text)
    return len(data) if isinstance(data, list) else 1

def validate_json(json_text: str) -> dict:
    """
    Валидирует строку JSON.
    Возвращает:
      {'ok': True, 'data': <распарсенные данные>, 'count': <объекты в корне>} — при успехе
      {'ok': False, 'error': <описание ошибки>} — при невалидном JSON
    """
    if not json_text.strip():
        return {"ok": False, "error": "Пустая строка — это невалидный JSON."}

    try:
        data = json.loads(json_text)
        count = count_root_objects(json_text)
        return {"ok": True, "data": data, "count": count}
    except json.JSONDecodeError as e:
        return {
            "ok": False,
            "error": f"Ошибка разбора JSON: {e.msg} (строка {e.lineno}, колонка {e.colno})"
        }