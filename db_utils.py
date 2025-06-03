import streamlit as st
import re

def is_valid_guid(guid: str) -> bool:
    pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    return re.match(pattern, guid) is not None


def run_db_tool():
    st.header("Работа с БД")

    with st.expander("История отпусков пользователя"):
        league_guid = st.text_input(
            "Лига гуид пользователя",
            key="league_guid"
        )

        # Список доступных полей
        va_fields = ["va.id", "va.user_id", "va.rev", "va.start_date", "va.end_date", "va.vacation_type", "va.vacation_status"]
        r_fields = ["r.rev", "r.timestamp", "r.creator"]

        selected_va_fields = st.multiselect("Поля из vacation_aud (va):", va_fields, default=va_fields)
        selected_r_fields = st.multiselect("Поля из revinfo (r):", r_fields, default=r_fields)

        make_sql_btn = st.button("Сформировать SQL")

        if make_sql_btn:
            if not league_guid:
                st.warning("Введи USERS.LEAGUE_GUID")
            elif not is_valid_guid(league_guid):
                st.error("Некорректный формат GUID")
            else:
                selected_fields = selected_va_fields + selected_r_fields
                if not selected_fields:
                    st.warning("Выбери хотя бы одно поле для SELECT")
                else:
                    fields_str = ", ".join(selected_fields)
                    sql_query = f"""
    SELECT {fields_str}
    FROM users u
    JOIN vacation_aud va ON va.user_id = u.id
    JOIN revinfo r ON va.rev = r.rev
    WHERE u.league_guid = '{league_guid}'
    """.strip()
                    st.code(sql_query, language='sql')
