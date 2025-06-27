# ui.py
import streamlit as st
import json
from features.user.template_builder.template_builder import json_to_template
from io import BytesIO

def recursive_field_editor(data, path=""):
    """
    Рекурсивно рисует форму для редактирования JSON-структуры.
    Возвращает изменённый объект.
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = recursive_field_editor(value, path + "." + key if path else key)
        return result
    elif isinstance(data, list):
        result = []
        for i, item in enumerate(data):
            result.append(recursive_field_editor(item, f"{path}[{i}]"))
        return result
    else:
        return st.text_input(f"{path}", value=str(data))

def run_template_creator():
    st.title("📦 Создание шаблона на основе JSON")
    st.markdown("Вставьте JSON, и он автоматически превратится в шаблон с переменными `${ключ}`.\n"
                "Вы сможете редактировать эти значения, например заменить на `${имя_переменной}`.")

    json_input = st.text_area("📝 Вставьте JSON", height=300, placeholder='{"name": "Иван", "age": 30}')
    if json_input:
        try:
            parsed = json.loads(json_input)
            template = json_to_template(parsed)
            st.success("✅ JSON обработан в шаблон. Отредактируйте значения переменных при необходимости.")
            modified = recursive_field_editor(template)

            if st.button("💾 Скачать шаблон с переменными"):
                buffer = BytesIO()
                buffer.write(json.dumps(modified, indent=2, ensure_ascii=False).encode("utf-8"))
                buffer.seek(0)
                st.download_button(
                    label="⬇️ Скачать шаблон JSON",
                    data=buffer,
                    file_name="template.json",
                    mime="application/json"
                )
        except Exception as e:
            st.error(f"❌ Ошибка: {e}")