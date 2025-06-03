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
        make_sql_btn = st.button("Сформировать SQL")

        if make_sql_btn:
            if not league_guid:
                st.warning("Введи USERS.LEAGUE_GUID")
            elif not is_valid_guid(league_guid):
                st.error("Некорректный формат GUID")
            else:
                sql_query = f"SELECT va.*, r.* FROM users u JOIN vacation_aud va on va.user_id = u.id JOIN revinfo r on va.rev = r.rev WHERE u.league_guid = '{league_guid}'"
                st.code(sql_query, language='sql')
