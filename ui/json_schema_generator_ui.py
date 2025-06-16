import streamlit as st
from logic.json_utils import validate_json
from ui.json_ui import display_json_result
from logic.json_schema_generator import json_to_json_schema

def run_json_schema_generator():
    st.header("Генератор JSON Schema")

    json_text = st.text_area("Вставьте JSON:", height=250)

    col1, col2 = st.columns(2)
    with col1:
        check_btn = st.button("Проверить и создать схему", use_container_width=True)
    with col2:
        clear_btn = st.button("Очистить", use_container_width=True)

    if clear_btn:
        st.session_state.clear()
        st.rerun()

    if check_btn:
        validation_result = validate_json(json_text)
        display_json_result(validation_result, json_text)

        if validation_result["ok"]:
            with st.spinner("Генерирую схему..."):
                schema_str = json_to_json_schema(json_text)

            st.subheader("Сгенерированная JSON Schema")
            st.code(schema_str, language="json")
        else:
            display_json_result(validation_result, json_text)