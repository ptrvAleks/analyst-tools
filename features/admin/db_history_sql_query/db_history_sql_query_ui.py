import streamlit as st

from features.admin.db_history_sql_query.db_history_sql_query import build_sql_query, is_valid_guid

def run_db_tool():
    st.header("Работа с БД")

    with st.expander("История отпусков пользователя", expanded=True):
        search_by = st.radio("Фильтровать по:", ["u.league_guid", "u.id"])

        if search_by == "u.league_guid":
            search_value = st.text_input("Введи значение league_guid", key="league_guid")
        else:
            search_value = st.text_input("Введи значение id", key="user_id")

        va_fields = ["va.id", "va.user_id", "va.rev", "va.start_date", "va.end_date", "va.vacation_type", "va.vacation_status"]
        r_fields = ["r.rev", "r.revtstmp", "r.creator"]

        selected_va_fields = st.multiselect("Поля из vacation_aud (va):", va_fields, default=va_fields)
        selected_r_fields = st.multiselect("Поля из revinfo (r):", r_fields, default=r_fields)

        if st.button("Сформировать SQL"):
            if not search_value:
                st.warning(f"Введи значение для {search_by}")
            elif search_by == "u.league_guid" and not is_valid_guid(search_value):
                st.error("Некорректный формат GUID")
            else:
                selected_fields = selected_va_fields + selected_r_fields
                if not selected_fields:
                    st.warning("Выбери хотя бы одно поле для SELECT")
                else:
                    sql_query = build_sql_query(search_by, search_value, selected_fields)
                    st.code(sql_query, language='sql')