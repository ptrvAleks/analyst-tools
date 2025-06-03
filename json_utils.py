import json
import streamlit as st

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

def run_json_tool():
    st.header("JSON-анализатор")

    json_text = st.text_area("Вставьте JSON–текст сюда:", height=200)

    col1, col2 = st.columns(2)
    with col1:
        check_btn = st.button("Проверить и форматировать JSON")
    with col2:
        clear_btn = st.button("Очистить")

    if clear_btn:
        st.rerun()

    if check_btn:
        result = validate_json(json_text)

        if result["ok"]:
            parsed_json = result["data"]
            count = count_root_objects(json_text)

            st.success("✅ JSON корректен")
            st.info(f"Количество объектов на верхнем уровне: {count}")

            st.subheader("Форматированный JSON:")
            st.json(parsed_json)
        else:
            st.error("❌ Ошибка в JSON:")
            st.code(result["error"], language="plaintext")

            # Попытка извлечь строку ошибки
            import re
            match = re.search(r'строка (\d+)', result["error"])
            if match:
                line_num = int(match.group(1))
                st.warning(f"Ошибка находится на строке: {line_num}")

                lines = json_text.splitlines()
                start = max(0, line_num - 5)
                end = min(len(lines), line_num + 4)

                snippet = []
                for i in range(start, end):
                    line_prefix = f"{i+1:>4}: "
                    if i + 1 == line_num:
                        # Подсветка строки с ошибкой
                        snippet.append(f"{line_prefix}👉 {lines[i]}")
                    else:
                        snippet.append(f"{line_prefix}   {lines[i]}")

                st.subheader("Контекст ошибки (±4 строки):")
                st.code("\n".join(snippet), language="json")
            else:
                st.info("Не удалось определить строку с ошибкой.")