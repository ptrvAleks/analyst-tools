import json

def count_root_objects(json_text: str) -> int:
    """
    Парсит строку json_text и возвращает количество объектов в корне.
    Если корень — не массив, возвращает 1.
    Бросает json.JSONDecodeError при неверном формате.
    """
    data = json.loads(json_text)
    if isinstance(data, list):
        return len(data)
    return 1

def validate_json(json_text: str) -> dict:
    """
    Пытается распарсить JSON.
    Возвращает {'ok': True, 'data': <parsed_data>} при успехе,
    или {'ok': False, 'error': <текст ошибки>} при невалидном JSON.
    """
    try:
        data = json.loads(json_text)
        return {"ok": True, "data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}