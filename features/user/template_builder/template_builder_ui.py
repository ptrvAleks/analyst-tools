import streamlit as st
import json
from features.user.template_builder.template_builder import extract_variables, render_template
from features.user.template_builder.liga_doc_document_create import run_liga_doc_create
from io import BytesIO

def run_template_builder():
    st.title("✏️ Заполнение шаблона переменными")

    # 🔽 Выбор логики обработки
    logic_choice = st.selectbox("⚙️ Логика генерации JSON", ["Документы", "Свой шаблон"])

    if logic_choice == "Документы":
        run_liga_doc_create()
        return  # ⛔️ Останавливаем дальнейшую логику

    # Логика для "Свой шаблон"
    st.markdown("Загрузите шаблон JSON с переменными вида `${variableName}`")
    uploaded = st.file_uploader("📂 Загрузите шаблон", type="json")

    if uploaded:
        try:
            raw_template = uploaded.read().decode("utf-8")
            st.code(raw_template, language="json")
            variables = extract_variables(raw_template)

            st.subheader("🔧 Введите значения переменных")
            user_inputs = {}
            for var in variables:
                user_inputs[var] = st.text_input(f"{var}", placeholder=f"Введите значение для {var}")

            if st.button("🚀 Сгенерировать JSON"):
                try:
                    result = render_template(raw_template, user_inputs)

                    st.success("✅ Сгенерированный JSON:")
                    st.json(result)

                    buffer = BytesIO()
                    buffer.write(json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8"))
                    buffer.seek(0)

                    st.download_button(
                        label="💾 Скачать результат",
                        data=buffer,
                        file_name="result.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"Ошибка генерации: {e}")
        except Exception as e:
            st.error(f"Ошибка чтения файла: {e}")