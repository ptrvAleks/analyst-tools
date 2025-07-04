import streamlit as st
from features.user.generate_json.generate_json import process_schema
from features.user.json_utils.json_utils import validate_json
from features.user.json_utils.json_ui import display_json_result

def run_json_generator():
    st.header("Генератор JSON")

    json_text = st.text_area("Вставьте JSON-схему:", height=250)

    col1, col2 = st.columns(2)
    with col1:
        check_btn = st.button("Проверить и создать JSON", use_container_width=True)
    with col2:
        clear_btn = st.button("Очистить", use_container_width=True)

    if clear_btn:
        st.session_state.clear()
        st.rerun()

    if check_btn:
        validation_result = validate_json(json_text)
        display_json_result(validation_result, json_text)

        if validation_result["ok"]:
            with st.spinner("Генерирую JSON..."):
                json_str = process_schema(json_text)

            st.subheader("Сгенерированный JSON")
            st.json(json_str)

