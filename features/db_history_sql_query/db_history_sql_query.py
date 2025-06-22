import re

def is_valid_guid(guid: str) -> bool:
    pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    return re.match(pattern, guid) is not None


def build_sql_query(search_by: str, search_value: str, selected_fields: list[str]) -> str:
    """
    Формирует SQL-запрос на основе выбранных параметров.
    """
    fields_str = ", ".join(selected_fields)
    value_str = f"'{search_value}'"  # Простое экранирование строки
    return f"""
SELECT {fields_str}
FROM users u
JOIN vacation_aud va ON va.user_id = u.id
JOIN revinfo r ON va.rev = r.rev
WHERE {search_by} = {value_str} and u.active = true
""".strip()
