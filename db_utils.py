import streamlit as st
import re

def is_valid_guid(guid: str) -> bool:
    pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    return re.match(pattern, guid) is not None


def run_db_tool():
    st.header("Работа с БД")

    with st.expander("История отпусков пользователя"):
        # Выбор метода фильтрации
        search_by = st.radio("Фильтровать по:", ["u.league_guid", "u.id"])

        # Поле ввода в зависимости от выбора
        if search_by == "u.league_guid":
            search_value = st.text_input("Введи значение league_guid", key="league_guid")
        else:
            search_value = st.text_input("Введи значение id", key="user_id")

        # Список доступных полей
        va_fields = ["va.id", "va.user_id", "va.rev", "va.start_date", "va.end_date", "va.vacation_type", "va.vacation_status"]
        r_fields = ["r.rev", "r.timestamp", "r.creator"]

        selected_va_fields = st.multiselect("Поля из vacation_aud (va):", va_fields, default=va_fields)
        selected_r_fields = st.multiselect("Поля из revinfo (r):", r_fields, default=r_fields)

        make_sql_btn = st.button("Сформировать SQL")

        if make_sql_btn:
            if not search_value:
                st.warning(f"Введи значение для {search_by}")
            elif search_by == "u.league_guid" and not is_valid_guid(search_value):
                st.error("Некорректный формат GUID")
            else:
                selected_fields = selected_va_fields + selected_r_fields
                if not selected_fields:
                    st.warning("Выбери хотя бы одно поле для SELECT")
                else:
                    fields_str = ", ".join(selected_fields)
                    # Экранируем значение, если нужно
                    value_str = f"'{search_value}'" if search_by == "u.league_guid" else search_value

                    sql_query = f"""
    SELECT {fields_str}
    FROM users u
    JOIN vacation_aud va ON va.user_id = u.id
    JOIN revinfo r ON va.rev = r.rev
    WHERE {search_by} = {value_str} and u.active = true
    """.strip()
                    st.code(sql_query, language='sql')
